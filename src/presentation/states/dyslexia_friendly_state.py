from utils.singleton import Singleton

class DyslexiaFriendlyState(metaclass = Singleton):
    def __init__(self):
        self._active: bool = None
    
    @property
    def active(self) -> bool:
        return self._active
    
    @active.setter
    def active(self, active: bool):
        self._active = active
        self.on_change()
    
    def on_change(self):
        pass