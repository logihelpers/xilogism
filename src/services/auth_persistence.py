import json
import os
import pickle
from pathlib import Path

class AuthPersistence:
    """Handles persisting and retrieving authentication credentials for Firebase and Google Drive"""

    # Firebase auth file
    FIREBASE_AUTH_FILE = os.path.join("src", "assets", "auth.json")

    # Google Drive token pickle file
    GOOGLE_TOKEN_FILE = os.path.join("src", "assets", "google_token.pickle")

    @classmethod
    def save_firebase_auth(cls, token, uid, user_data, refresh_token=None):
        """Save Firebase authentication data to local storage"""
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
            print(f"Firebase auth data saved to {cls.FIREBASE_AUTH_FILE}")
            return True
        except Exception as e:
            print(f"Error saving Firebase auth data: {e}")
            return False

    @classmethod
    def load_firebase_auth(cls):
        """Load Firebase authentication data from local storage"""
        if not os.path.exists(cls.FIREBASE_AUTH_FILE):
            print(f"Firebase auth file not found: {cls.FIREBASE_AUTH_FILE}")
            return None

        try:
            with open(cls.FIREBASE_AUTH_FILE, 'r') as f:
                data = json.load(f)
            print(f"Firebase auth data loaded successfully from {cls.FIREBASE_AUTH_FILE}")
            return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading Firebase auth data: {e}")
            return None

    @classmethod
    def clear_firebase_auth(cls):
        """Clear Firebase authentication data"""
        if os.path.exists(cls.FIREBASE_AUTH_FILE):
            try:
                os.remove(cls.FIREBASE_AUTH_FILE)
                print(f"Firebase auth data cleared from {cls.FIREBASE_AUTH_FILE}")
                return True
            except Exception as e:
                print(f"Error clearing Firebase auth data: {e}")
                return False
        return True

    @classmethod
    def save_google_credentials(cls, credentials):
        """Save Google credentials using pickle"""
        os.makedirs(os.path.dirname(cls.GOOGLE_TOKEN_FILE), exist_ok=True)
        try:
            with open(cls.GOOGLE_TOKEN_FILE, 'wb') as f:
                pickle.dump(credentials, f)
            print(f"Google credentials saved to {cls.GOOGLE_TOKEN_FILE}")
            return True
        except Exception as e:
            print(f"Error saving Google credentials: {e}")
            return False

    @classmethod
    def load_google_credentials(cls):
        """Load Google credentials from pickle"""
        if not os.path.exists(cls.GOOGLE_TOKEN_FILE):
            print(f"Google credentials file not found: {cls.GOOGLE_TOKEN_FILE}")
            return None

        try:
            with open(cls.GOOGLE_TOKEN_FILE, 'rb') as f:
                credentials = pickle.load(f)
            print(f"Google credentials loaded successfully from {cls.GOOGLE_TOKEN_FILE}")
            return credentials
        except Exception as e:
            print(f"Error loading Google credentials: {e}")
            return None

    @classmethod
    def clear_google_credentials(cls):
        """Clear Google credentials"""
        if os.path.exists(cls.GOOGLE_TOKEN_FILE):
            try:
                os.remove(cls.GOOGLE_TOKEN_FILE)
                print(f"Google credentials cleared from {cls.GOOGLE_TOKEN_FILE}")
                return True
            except Exception as e:
                print(f"Error clearing Google credentials: {e}")
                return False
        return True
