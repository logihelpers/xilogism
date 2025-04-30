class AuthState:
    _instance = None
    _listeners = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthState, cls).__new__(cls)
            cls._instance.user = None
            cls._instance._listeners = []
        return cls._instance

    def register_listener(self, callback):
        if callback not in self._listeners:
            self._listeners.append(callback)

    def _notify_listeners(self):
        for callback in self._listeners:
            callback(self.user)

    def set_user(self, user):
        self.user = user
        self._notify_listeners()

    def clear(self):
        self.user = None
        self._notify_listeners()
