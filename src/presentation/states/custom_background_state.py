from services.singleton import Singleton

class CustomBackgroundState(metaclass = Singleton):
    def __init__(self):
        self._active: str = None
    
    @property
    def active(self) -> str:
        return self._active
    
    @active.setter
    def active(self, active: str):
        self._active = active
        self.on_change()
    
    def on_change(self):
        pass