import json
import base64
import traceback
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from flet import SnackBar, Text
import pyrebase
from PIL import Image
import io
from presentation.states.auth_state import AuthState
from presentation.controllers.controller import Controller, Priority
from presentation.controllers.google_drive_controller import GoogleDriveController
from services.auth_persistence import AuthPersistence

# Load Firebase configuration from JSON file
with open('src/assets/firebase_config.json') as f:
    firebase_config = json.load(f)

class AuthController(Controller):
    _instance = None
    priority = Priority.ENTRY_POINT

    GOOGLE_CLIENT_SECRET_FILE = 'src/assets/credentials.json'
    GOOGLE_SCOPES = [
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile"
    ]

    @classmethod
    def get_instance(cls):
        return cls._instance

    def __init__(self, page=None, auth_dialog=None):
        super().__init__(page)
        AuthController._instance = self
        self.page = page
        self.auth_dialog = auth_dialog

        self._is_restoring_session = False

        self.firebase = pyrebase.initialize_app(firebase_config)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()
        self.storage = self.firebase.storage()

        self.user_token = None
        self.user_uid = None
        self.refresh_token = None

        self.state = AuthState()
        self.state.register_listener(self.on_auth_change)

        if page:
            page.after = self._restore_session
        else:
            self._restore_session()

    def _restore_session(self):
        print("Attempting to restore auth session...")
        self._is_restoring_session = True

        try:
            auth_data = AuthPersistence.load_firebase_auth()
            if auth_data:
                self.user_token = auth_data["token"]
                self.user_uid = auth_data["uid"]
                self.refresh_token = auth_data.get("refreshToken")
                user_data = auth_data["user"]

                try:
                    self.auth.get_account_info(self.user_token)
                    print(f"Token validated for user {user_data.get('displayName', 'Unknown')}")
                except Exception as e:
                    print(f"Token validation failed: {e}")
                    if self.refresh_token:
                        try:
                            refreshed = self.auth.refresh(self.refresh_token)
                            self.user_token = refreshed["idToken"]
                            self.refresh_token = refreshed["refreshToken"]
                            self.user_uid = refreshed["userId"]
                            print("Token refreshed successfully.")
                            AuthPersistence.save_firebase_auth(
                                self.user_token, self.user_uid, user_data, self.refresh_token
                            )
                        except Exception as refresh_error:
                            print(f"Token refresh failed: {refresh_error}")
                            self.user_token = None
                            self.user_uid = None
                            AuthPersistence.clear_firebase_auth()
                            self.state.clear()
                            return False
                    else:
                        print("No refresh token available.")
                        return False

                self.state.set_user(user_data)
                print(f"Authentication session restored for {user_data.get('displayName', 'Unknown')}")

                if self.page and hasattr(self.page, "sidebar"):
                    self.page.sidebar.refresh_user_profile()
                    self.page.update()

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
                f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={firebase_config['apiKey']}",
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

            self.state.set_user(user_data)
            AuthPersistence.save_firebase_auth(self.user_token, self.user_uid, user_data, self.refresh_token)

            self._close_dialog()
            self._snack("Signed in with Google!")

            # After Google login, pass the credentials to GoogleDriveController
            if self.page:
                # Assuming page has a GoogleDriveController instance.
                drive_controller = GoogleDriveController(page=self.page)
                drive_controller.login_with_creds(creds)  # Pass Google credentials to the drive controller
        except Exception as e:
            self._snack(f"Google login failed: {e}")
            print(f"[Google Login Error] {e}")
            traceback.print_exc()

    def _close_dialog(self):
        if self.auth_dialog:
            self.auth_dialog.open = False
            self.auth_dialog.update()
        if self.page:
            self.page.update()

    def _snack(self, message: str):
        if self.page:
            self.page.snack_bar = SnackBar(Text(message))
            self.page.snack_bar.open = True
            self.page.update()
        else:
            print(f"[SnackBar] {message}")

    def on_auth_change(self, user):
        if self.page and hasattr(self.page, "sidebar"):
            self.page.sidebar.refresh_user_profile()
            self.page.update()
