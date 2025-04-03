from services.singleton import Singleton

class DarkModeState(metaclass = Singleton):
    def __init__(self):
        self._active: bool = None
        self._follow_system_active: bool = None
    
    @property
    def active(self) -> bool:
        return self._active
    
    @active.setter
    def active(self, active: bool):
        self._active = active
        self.on_change()
    
    @property
    def follow_system_active(self) -> bool:
        return self._follow_system_active
    
    @follow_system_active.setter
    def follow_system_active(self, active: bool):
        self._follow_system_active = active
        self.on_follow_system_change()
    
    def on_change(self):
        pass

    def on_follow_system_change(self):
        pass