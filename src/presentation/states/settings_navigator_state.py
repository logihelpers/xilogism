from utils.singleton import Singleton

class SettingsNavigatorState(metaclass = Singleton):
    def __init__(self):
        self._active__: int = 0
    
    @property
    def active(self) -> int:
        return self._active__
    
    @active.setter
    def active(self, active: int):
        self._active__ = active
        self.on_change()
    
    def on_change(self):
        pass