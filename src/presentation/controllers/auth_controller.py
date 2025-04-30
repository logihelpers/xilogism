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
from presentation.controllers.controller import Priority

# Load Firebase configuration from JSON file
with open('src/assets/firebase_config.json') as f:
    firebase_config = json.load(f)

class AuthController:
    _instance = None
    priority = Priority.SETTINGS_BOUND

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
        AuthController._instance = self
        self.page = page
        self.auth_dialog = auth_dialog

        self.firebase = pyrebase.initialize_app(firebase_config)
        self.auth    = self.firebase.auth()
        self.db      = self.firebase.database()
        self.storage = self.firebase.storage()

        self.user_token = None
        self.user_uid   = None

        self.state = AuthState()
        self.state.register_listener(self.on_auth_change)

    def register_email(self, name: str, email: str, password: str):
        try:
            user = self.auth.create_user_with_email_and_password(email, password)
            self.user_token = user['idToken']
            self.user_uid   = user['localId']

            self.db.child("users").child(self.user_uid).set({
                "name": name,
                "email": email,
                "photoUrl": ""
            })

            self.state.set_user({
                "displayName": name,
                "email": email,
                "photoUrl": ""
            })

            self._close_dialog()
            self._snack("Registered successfully!")
            return user
        except Exception as e:
            self._snack(f"Registration failed: {e}")
            return None

    def login_email(self, email: str, password: str):
        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            self.user_token = user['idToken']
            self.user_uid   = user['localId']

            info = self.auth.get_account_info(self.user_token)['users'][0]
            db_user = self.db.child("users").child(self.user_uid).get().val() or {}
            display_name = db_user.get("name") or info.get("displayName") or info.get("email")
            photo_url    = db_user.get("photoUrl") or info.get("photoUrl", "")

            self.state.set_user({
                "displayName": display_name,
                "email": info.get("email"),
                "photoUrl": photo_url
            })

            self._close_dialog()
            self._snack("Logged in successfully!")
            return user
        except Exception as e:
            self._snack(f"Login failed: {e}")
            return None

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
            self.user_uid   = result["localId"]

            user_data = self.db.child("users").child(self.user_uid).get().val()
            if not user_data:
                self.db.child("users").child(self.user_uid).set({
                    "name": profile_info["name"],
                    "email": profile_info["email"],
                    "photoUrl": profile_info["picture"]
                })

            self.state.set_user({
                "displayName": profile_info["name"],
                "email": profile_info["email"],
                "photoUrl": profile_info["picture"]
            })

            self._close_dialog()
            self._snack("Signed in with Google!")
        except Exception as e:
            self._snack(f"Google login failed: {e}")
            print(f"[Google Login Error] {e}")

    def upload_profile_picture(
        self,
        file_path: str,
        content_type: str = "image/jpeg",
        max_size: tuple = (512, 512),
        quality: int = 75
    ):
        if not (self.user_token and self.user_uid):
            self._snack("You must be signed in to upload.")
            return

        try:
            with Image.open(file_path) as img:
                img.thumbnail(max_size)
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=quality)
                raw_data = buffer.getvalue()

            base64_str = base64.b64encode(raw_data).decode('utf-8')
            data_uri = f"data:{content_type};base64,{base64_str}"

            self.db.child("users") \
                .child(self.user_uid) \
                .update({
                    "photoBase64": base64_str,
                    "photoUrl": data_uri
                })

            requests.post(
                f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={firebase_config['apiKey']}",
                headers={"Content-Type": "application/json"},
                json={
                    "idToken": self.user_token,
                    "photoUrl": data_uri,
                    "returnSecureToken": True
                }
            )

            user = self.state.user.copy()
            user["photoUrl"] = data_uri
            self.state.set_user(user)

            print("Profile picture uploaded.")
            self._snack("Profile picture uploaded successfully!")
        except Exception as e:
            traceback.print_exc()
            self._snack(f"Upload failed: {e}")

    def forgot_password(self, email: str):
        try:
            self.auth.send_password_reset_email(email)
            self._snack("Password reset email sent—check your inbox.")
        except Exception as e:
            err = str(e)
            if "PASSWORD_LOGIN_NOT_SUPPORTED" in err or "USER_NOT_FOUND" in err:
                self._snack(
                    "This account is managed by Google Sign-In. "
                    "Please use Google account recovery instead."
                )
            else:
                self._snack(f"Could not send reset email: {e}")
        finally:
            self._close_dialog()  # <- Always close dialog after handling

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
