# import json
# import os
# import pickle
# from pathlib import Path

# class AuthPersistence:
#     FIREBASE_AUTH_FILE = os.path.join("src", "assets", "auth.json")
#     GOOGLE_TOKEN_FILE = os.path.join("src", "assets", "google_token.pickle")

#     @classmethod
#     def save_firebase_auth(cls, token, uid, user_data, refresh_token=None):
#         os.makedirs(os.path.dirname(cls.FIREBASE_AUTH_FILE), exist_ok=True)

#         auth_data = {
#             "token": token,
#             "uid": uid,
#             "refreshToken": refresh_token,
#             "user": user_data
#         }

#         try:
#             with open(cls.FIREBASE_AUTH_FILE, 'w') as f:
#                 json.dump(auth_data, f)
#             return True
#         except Exception as e:
#             print(f"Error saving Firebase auth data: {e}")
#             return False

#     @classmethod
#     def load_firebase_auth(cls):
#         if not os.path.exists(cls.FIREBASE_AUTH_FILE):
#             return None

#         try:
#             with open(cls.FIREBASE_AUTH_FILE, 'r') as f:
#                 data = json.load(f)
#             return data
#         except (json.JSONDecodeError, IOError) as e:
#             print(f"Error loading Firebase auth data: {e}")
#             return None

#     @classmethod
#     def clear_firebase_auth(cls):
#         if os.path.exists(cls.FIREBASE_AUTH_FILE):
#             try:
#                 os.remove(cls.FIREBASE_AUTH_FILE)
#                 return True
#             except Exception as e:
#                 print(f"Error clearing Firebase auth data: {e}")
#                 return False
#         return True

#     @classmethod
#     def save_google_credentials(cls, credentials):
#         os.makedirs(os.path.dirname(cls.GOOGLE_TOKEN_FILE), exist_ok=True)
#         try:
#             with open(cls.GOOGLE_TOKEN_FILE, 'wb') as f:
#                 pickle.dump(credentials, f)
#             return True
#         except Exception as e:
#             print(f"Error saving Google credentials: {e}")
#             return False

#     @classmethod
#     def load_google_credentials(cls):
#         if not os.path.exists(cls.GOOGLE_TOKEN_FILE):
#             print(f"Google credentials file not found: {cls.GOOGLE_TOKEN_FILE}")
#             return None

#         try:
#             with open(cls.GOOGLE_TOKEN_FILE, 'rb') as f:
#                 credentials = pickle.load(f)
#             return credentials
#         except Exception as e:
#             print(f"Error loading Google credentials: {e}")
#             return None

#     @classmethod
#     def clear_google_credentials(cls):
#         if os.path.exists(cls.GOOGLE_TOKEN_FILE):
#             try:
#                 os.remove(cls.GOOGLE_TOKEN_FILE)
#                 return True
#             except Exception as e:
#                 print(f"Error clearing Google credentials: {e}")
#                 return False
#         return True


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
from utils.singleton import Singleton
import os
import pickle
from pathlib import Path

class AuthPersistence:
    FIREBASE_AUTH_FILE = os.path.join("src", "assets", "auth.json")
    GOOGLE_TOKEN_FILE = os.path.join("src", "assets", "google_token.pickle")

    @classmethod
    def save_firebase_auth(cls, token, uid, user_data, refresh_token=None):
        os.makedirs(os.path.dirname(cls.FIREBASE_AUTH_FILE), exist_ok=True)

        auth_data = {
            "token": token,
            "uid": uid,
            "refreshToken": refresh_token,
            "user": user_data
        }

        try:
            with open(cls.FIREBASE_AUTH_FILE, 'w') as f:
                json.dump(auth_data, f)
            return True
        except Exception as e:
            print(f"Error saving Firebase auth data: {e}")
            return False

    @classmethod
    def load_firebase_auth(cls):
        if not os.path.exists(cls.FIREBASE_AUTH_FILE):
            return None

        try:
            with open(cls.FIREBASE_AUTH_FILE, 'r') as f:
                data = json.load(f)
            return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading Firebase auth data: {e}")
            return None

    @classmethod
    def clear_firebase_auth(cls):
        if os.path.exists(cls.FIREBASE_AUTH_FILE):
            try:
                os.remove(cls.FIREBASE_AUTH_FILE)
                return True
            except Exception as e:
                print(f"Error clearing Firebase auth data: {e}")
                return False
        return True

    @classmethod
    def save_google_credentials(cls, credentials):
        os.makedirs(os.path.dirname(cls.GOOGLE_TOKEN_FILE), exist_ok=True)
        try:
            with open(cls.GOOGLE_TOKEN_FILE, 'wb') as f:
                pickle.dump(credentials, f)
            return True
        except Exception as e:
            print(f"Error saving Google credentials: {e}")
            return False

    @classmethod
    def load_google_credentials(cls):
        if not os.path.exists(cls.GOOGLE_TOKEN_FILE):
            print(f"Google credentials file not found: {cls.GOOGLE_TOKEN_FILE}")
            return None

        try:
            with open(cls.GOOGLE_TOKEN_FILE, 'rb') as f:
                credentials = pickle.load(f)
            return credentials
        except Exception as e:
            print(f"Error loading Google credentials: {e}")
            return None

    @classmethod
    def clear_google_credentials(cls):
        if os.path.exists(cls.GOOGLE_TOKEN_FILE):
            try:
                os.remove(cls.GOOGLE_TOKEN_FILE)
                return True
            except Exception as e:
                print(f"Error clearing Google credentials: {e}")
                return False
        return True