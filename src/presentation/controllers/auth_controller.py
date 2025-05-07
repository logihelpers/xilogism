from services.auth.auth_persistence import AuthPersistence
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
from utils.singleton import Singleton
import os
import pickle
from pathlib import Path

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
        self.state.on_request_login = self.login_email
        self.state.on_request_register_email = self.register_email
        self.dia_state = DialogState()
        self.state.on_request_logout = lambda: asyncio.run(self.logout())
    
    async def logout(self):
        """
        Logs the user out by clearing all authentication tokens,
        credentials from persistence, and resetting the application state.
        """
        try:
            # Clear Firebase authentication data from persistence
            firebase_cleared = AuthPersistence.clear_firebase_auth()
            
            # Clear Google credentials from persistence
            google_cleared = AuthPersistence.clear_google_credentials()
            
            # Reset controller state
            self.user_token = None
            self.user_uid = None
            self.refresh_token = None
            
            # Clear user data from state
            if hasattr(self.state, 'user'):
                del self.state.user
            
            # Clear Google credentials from state
            if hasattr(self.state, 'google_creds'):
                self.state.google_creds = None
            
            # Show success message
            if firebase_cleared and google_cleared:
                self._snack("Logged out successfully")
            else:
                self._snack("Logout completed with some issues")
            
            # Close current dialog and show login dialog
            self.dia_state.state = Dialogs.CLOSE
            
            return True
        except Exception as e:
            print(f"Logout failed: {e}")
            traceback.print_exc()
            self._snack(f"Logout failed: {str(e)}")
            return False

    def login_email(self, email: str, password: str):
        """
        Authenticates a user using email and password with Firebase.
        
        Args:
            email: User's email address
            password: User's password
            
        Returns:
            bool: True if login was successful, False otherwise
        """
        try:
            # Validate inputs
            if not email or not password:
                self._snack("Email and password are required")
                return False
                
            # Authenticate with Firebase
            user = self.auth.sign_in_with_email_and_password(email, password)
            if not user:
                self._snack("Login failed: Invalid credentials")
                return False
                
            # Store authentication tokens
            self.user_token = user['idToken']
            self.user_uid = user['localId']
            self.refresh_token = user.get('refreshToken')
            
            # Get user data from Realtime Database
            user_data = self.db.child("users").child(self.user_uid).get(token=self.user_token).val()
            
            # If no user data exists (first login), create basic profile
            if not user_data:
                user_data = {
                    "email": email,
                    "displayName": email.split('@')[0],  # Basic display name from email
                    "photoUrl": "",  # No photo URL for email users by default
                    "createdAt": {".sv": "timestamp"}  # Correct server timestamp
                }
                self.db.child("users").child(self.user_uid).set(user_data, token=self.user_token)
            
            # Save user data to state and persistence
            self.state.user = user_data
            AuthPersistence.save_firebase_auth(
                self.user_token, self.user_uid, user_data, self.refresh_token
            )
            
            # Close login dialog
            self.dia_state.state = Dialogs.CLOSE
            self._snack(f"Welcome, {user_data.get('displayName', 'User')}!")
            
            return True
        except Exception as e:
            error_message = str(e)
            # Handle common Firebase errors
            if "INVALID_PASSWORD" in error_message:
                self._snack("Invalid password")
            elif "EMAIL_NOT_FOUND" in error_message:
                self._snack("Email not found")
            elif "INVALID_EMAIL" in error_message:
                self._snack("Invalid email format")
            elif "TOO_MANY_ATTEMPTS_TRY_LATER" in error_message:
                self._snack("Too many failed attempts. Try again later")
            elif "INVALID_LOGIN_CREDENTIALS" in error_message:
                self._snack(f"Email/Password might be wrong.")
            else:
                self._snack(f"Login failed: {error_message}")
            
            print(f"[Email Login Error] {e}")
            traceback.print_exc()
            return False

    def register_email(self, display_name: str, email: str, password: str):
        """
        Registers a new user with email, password and display name.
        
        Args:
            email: User's email address
            password: User's password
            display_name: User's display name
            
        Returns:
            bool: True if registration was successful, False otherwise
        """
        try:
            # Validate inputs
            if not email or not password:
                self._snack("Email and password are required")
                return False
                
            if len(password) < 6:
                self._snack("Password must be at least 6 characters")
                return False
            
            # Create user in Firebase Authentication
            user = self.auth.create_user_with_email_and_password(email, password)
            if not user:
                self._snack("Registration failed")
                return False
                
            # Store authentication tokens
            self.user_token = user['idToken']
            self.user_uid = user['localId']
            self.refresh_token = user.get('refreshToken')
            
            # Create user profile in Realtime Database
            user_data = {
                "email": email,
                "displayName": display_name or email.split('@')[0],  # Use displayName or extract from email
                "photoUrl": "",  # No photo URL for email users by default
                "createdAt": {".sv": "timestamp"}  # Correct server timestamp
            }
            
            self.db.child("users").child(self.user_uid).set(user_data, token=self.user_token)
            
            # Save user data to state and persistence
            self.state.user = user_data
            AuthPersistence.save_firebase_auth(
                self.user_token, self.user_uid, user_data, self.refresh_token
            )
            
            # Close registration dialog
            self.dia_state.state = Dialogs.CLOSE
            self._snack(f"Welcome, {user_data.get('displayName', 'User')}!")
            
            return True
        except Exception as e:
            error_message = str(e)
            # Handle common Firebase errors
            if "EMAIL_EXISTS" in error_message:
                self._snack("Email already in use")
            elif "WEAK_PASSWORD" in error_message:
                self._snack("Password is too weak")
            elif "INVALID_EMAIL" in error_message:
                self._snack("Invalid email format")
            else:
                self._snack(f"Registration failed: {error_message}")
            
            print(f"[Email Registration Error] {e}")
            traceback.print_exc()
            return False

    def update_user_profile(self, display_name=None, photo_url=None):
        """
        Updates the user's profile information in Firebase Realtime Database.
        
        Args:
            display_name: New display name (optional)
            photo_url: New photo URL (optional)
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            if not self.user_uid or not self.user_token:
                self._snack("You must be logged in to update your profile")
                return False
                
            updates = {}
            if display_name:
                updates["displayName"] = display_name
            if photo_url:
                updates["photoUrl"] = photo_url
                
            if not updates:
                return True  # Nothing to update
                
            # Update database
            self.db.child("users").child(self.user_uid).update(updates, token=self.user_token)
            
            # Update local state
            current_user = self.state.user.copy() if hasattr(self.state, 'user') else {}
            current_user.update(updates)
            self.state.user = current_user
            
            # Update persistence
            AuthPersistence.save_firebase_auth(
                self.user_token, self.user_uid, current_user, self.refresh_token
            )
            
            self._snack("Profile updated successfully")
            return True
        except Exception as e:
            self._snack(f"Failed to update profile: {e}")
            print(f"[Profile Update Error] {e}")
            traceback.print_exc()
            return False

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
                            if hasattr(self.state, 'user'):
                                del self.state.user
                            return False
                    else:
                        print("No refresh token available.")
                        return False

                self.state.user = user_data
                
                # Restore Google credentials if available
                google_creds = AuthPersistence.load_google_credentials()
                if google_creds:
                    self.state.google_creds = google_creds
                else:
                    print("No Google credentials found, proceeding without Drive access.")
                
                return True
        except Exception as e:
            print(f"Failed to restore auth session: {e}")
            traceback.print_exc()
            AuthPersistence.clear_firebase_auth()
            return False
        finally:
            self._is_restoring_session = False

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
                user_data = {
                    "name": profile_info["name"],
                    "email": profile_info["email"],
                    "photoUrl": profile_info["picture"],
                    "createdAt": {".sv": "timestamp"},  # Correct server timestamp for pyrebase
                    "provider": "google"
                }
                self.db.child("users").child(self.user_uid).set(user_data)

            user_data = {
                "displayName": profile_info["name"],
                "email": profile_info["email"],
                "photoUrl": profile_info["picture"],
                "provider": "google"
            }

            self.state.user = user_data
            AuthPersistence.save_firebase_auth(self.user_token, self.user_uid, user_data, self.refresh_token)
            
            # Save Google credentials for future use
            if creds:
                AuthPersistence.save_google_credentials(creds)
                self.state.google_creds = creds
                self._snack(f"Welcome, {user_data['displayName']}! Google Drive authenticated!")
            else:
                self._snack(f"Welcome, {user_data['displayName']}! Google Drive not authenticated.")

            # Close dialog
            self.dia_state.state = Dialogs.CLOSE
            
        except Exception as e:
            self._snack(f"Google login failed: {e}")
            print(f"[Google Login Error] {e}")
            traceback.print_exc()

    def reset_password(self, email: str):
        """
        Sends a password reset email to the user.
        
        Args:
            email: User's email address
            
        Returns:
            bool: True if reset email was sent successfully, False otherwise
        """
        try:
            if not email:
                self._snack("Email is required")
                return False
                
            self.auth.send_password_reset_email(email)
            self._snack(f"Password reset email sent to {email}")
            return True
        except Exception as e:
            error_message = str(e)
            if "EMAIL_NOT_FOUND" in error_message:
                self._snack("Email not found")
            else:
                self._snack(f"Failed to send reset email: {error_message}")
            
            print(f"[Password Reset Error] {e}")
            traceback.print_exc()
            return False

    def _snack(self, message: str):
        if self.page:
            snackbar = SnackBar(Text(message))
            self.page.open(snackbar)
            self.page.update()
        else:
            print(f"[SnackBar] {message}")