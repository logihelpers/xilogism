class AuthState:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthState, cls).__new__(cls)
            cls._instance.user = None
            cls._instance.listeners = []
        return cls._instance
    
    def set_user(self, user):
        """
        Set the current user and notify all listeners
        """
        self.user = user
        self._notify_listeners()
    
    def clear(self):
        """
        Clear the current user and notify all listeners
        """
        self.user = None
        self._notify_listeners()
    
    def register_listener(self, listener):
        """
        Register a listener function to be called when the user changes
        """
        if listener not in self.listeners:
            self.listeners.append(listener)
    
    def unregister_listener(self, listener):
        """
        Unregister a previously registered listener
        """
        if listener in self.listeners:
            self.listeners.remove(listener)
    
    def _notify_listeners(self):
        """
        Notify all registered listeners about the user change
        """
        for listener in self.listeners:
            try:
                listener(self.user)
            except Exception as e:
                print(f"Error notifying listener: {e}")