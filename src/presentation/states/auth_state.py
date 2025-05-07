from utils.singleton import Singleton

class AuthState(metaclass=Singleton):
    def __init__(self):
        self._user = ""
        self._user_change_cb: list = []
        self._google_creds = ""
    
    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, value):
        self._user = value
        for cb in self._user_change_cb:
            cb()
    
    @user.deleter
    def user(self):
        self._user = None
        for cb in self._user_change_cb:
            cb()
    
    @property
    def google_creds(self):
        return self._google_creds
    
    @google_creds.setter
    def google_creds(self, value):
        self._google_creds = value
        self.on_creds_set()
    
    def on_creds_set(self):
        pass
    
    @property
    def on_user_change(self):
        return self._user_change_cb
    
    @on_user_change.setter
    def on_user_change(self, cb):
        if cb not in self._user_change_cb:
            self._user_change_cb.append(cb)
    
    def request_logout(self):
        self.on_request_logout()
    
    def on_request_logout(self):
        pass

    def request_login(self, email: str, password: str):
        self.on_request_login(email, password)
    
    def on_request_login(self, email: str, password: str):
        pass

    def request_google_login(self):
        self.on_request_google_login()
    
    def on_request_google_login(self):
        pass

    def request_pw_change(self, email: str):
        self.on_request_pw_change(email)
    
    def on_request_pw_change(self, email: str):
        pass

    def request_register_email(self, name: str, email: str, password: str) -> bool:
        return self.on_request_register_email(name, email, password)
    
    def on_request_register_email(self, name, email: str, password: str) -> bool:
        pass