import json
import asyncio
import traceback
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from flet import SnackBar, Text, Page
import pyrebase
from presentation.states.auth_state import AuthState
from presentation.states.dialogs_state import Dialogs, DialogState
from presentation.controllers.controller import Controller, Priority
from presentation.controllers.google_drive_controller import GoogleDriveController
from services.auth.auth_persistence import AuthPersistence
from utils.singleton import Singleton

class AuthController(Controller, metaclass=Singleton):
    priority = Priority.NONE

    GOOGLE_CLIENT_SECRET_FILE = 'src/assets/credentials.json'
    GOOGLE_SCOPES = [
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        'https://www.googleapis.com/auth/drive'
    ]

    def __init__(self, page: Page):
        self.page = page
        self._is_restoring_session = False

        with open('src/assets/firebase_config.json') as f:
            self.firebase_config = json.load(f)

        self.firebase = pyrebase.initialize_app(self.firebase_config)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()
        self.storage = self.firebase.storage()

        self.user_token = None
        self.user_uid = None
        self.refresh_token = None

        self.state = AuthState()
        self.state.on_request_google_login = self.login_google
        self.dia_state = DialogState()
        self.state.on_request_logout = lambda: asyncio.run(self.logout())
    
    async def logout(self):
        self.dia_state.state = Dialogs.CLOSE
        await asyncio.sleep(0.2)
        self.dia_state.state = Dialogs.LOGIN

    def restore_session(self):
        self._is_restoring_session = True
        try:
            auth_data = AuthPersistence.load_firebase_auth()
            if auth_data:
                self.user_token = auth_data["token"]
                self.user_uid = auth_data["uid"]
                self.refresh_token = auth_data["refreshToken"]
                user_data = auth_data["user"]

                try:
                    self.auth.get_account_info(self.user_token)
                except Exception as e:
                    print(f"Token validation failed: {e}")
                    if self.refresh_token:
                        try:
                            refreshed = self.auth.refresh(self.refresh_token)
                            self.user_token = refreshed["idToken"]
                            self.refresh_token = refreshed["refreshToken"]
                            self.user_uid = refreshed["userId"]
                            AuthPersistence.save_firebase_auth(
                                self.user_token, self.user_uid, user_data, self.refresh_token
                            )
                        except Exception as refresh_error:
                            print(f"Token refresh failed: {refresh_error}")
                            self.user_token = None
                            self.user_uid = None
                            AuthPersistence.clear_firebase_auth()
                            del self.state.user
                            return False
                    else:
                        print("No refresh token available.")
                        return False

                self.state.user = user_data
                return True
        except Exception as e:
            print(f"Failed to restore auth session: {e}")
            traceback.print_exc()
            AuthPersistence.clear_firebase_auth()
        finally:
            self._is_restoring_session = False
        return False

    def login_google(self):
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.GOOGLE_CLIENT_SECRET_FILE,
                scopes=self.GOOGLE_SCOPES
            )
            creds = flow.run_local_server(port=0)
            session = requests.Session()
            session.headers.update({'Authorization': f'Bearer {creds.token}'})

            profile_info = session.get('https://www.googleapis.com/userinfo/v2/me').json()

            firebase_resp = requests.post(
                f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={self.firebase_config['apiKey']}",
                headers={"Content-Type": "application/json"},
                json={
                    "postBody": f"id_token={creds.id_token}&providerId=google.com",
                    "requestUri": "http://localhost",
                    "returnIdpCredential": True,
                    "returnSecureToken": True
                }
            )

            if firebase_resp.status_code != 200:
                raise Exception(firebase_resp.json().get("error", {}).get("message", "Google login failed"))

            result = firebase_resp.json()
            self.user_token = result["idToken"]
            self.user_uid = result["localId"]
            self.refresh_token = result["refreshToken"]

            user_data = self.db.child("users").child(self.user_uid).get().val()
            if not user_data:
                self.db.child("users").child(self.user_uid).set({
                    "name": profile_info["name"],
                    "email": profile_info["email"],
                    "photoUrl": profile_info["picture"]
                })

            user_data = {
                "displayName": profile_info["name"],
                "email": profile_info["email"],
                "photoUrl": profile_info["picture"]
            }

            self.state.user = user_data
            AuthPersistence.save_firebase_auth(self.user_token, self.user_uid, user_data, self.refresh_token)
            if creds:
                self.page.open(SnackBar(Text("Drive credentials authenticated!")))
            else:
                self.page.open(SnackBar(Text("Drive credentials not authenticated!")))
            
            self.state.google_creds = creds
        except Exception as e:
            self._snack(f"Google login failed: {e}")
            print(f"[Google Login Error] {e}")
            traceback.print_exc()

    def _snack(self, message: str):
        if self.page:
            snackbar = SnackBar(Text(message))
            self.page.open(snackbar)
            self.page.update()
        else:
            print(f"[SnackBar] {message}")