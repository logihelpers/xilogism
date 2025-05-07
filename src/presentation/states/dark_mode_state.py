from utils.singleton import Singleton
from enum import Enum

class DarkModeScheme(Enum):
    LIGHT = False
    DARK = True

class DarkModeState(metaclass = Singleton):
    def __init__(self):
        self._active: DarkModeScheme = None
        self._follow_system_active: bool = None
        self._on_change_callbacks: list = []
        self._on_followsys_change_cb: list = []
    
    @property
    def active(self) -> DarkModeScheme:
        return self._active
    
    @active.setter
    def active(self, active: DarkModeScheme):
        self._active = active
        for callback in self._on_change_callbacks:
            callback()
    
    @property
    def follow_system_active(self) -> bool:
        return self._follow_system_active
    
    @follow_system_active.setter
    def follow_system_active(self, active: bool):
        self._follow_system_active = active
        for callback in self._on_followsys_change_cb:
            callback()
    
    @property
    def on_change(self):
        return self._on_change_callbacks
    
    @on_change.setter
    def on_change(self, callback):
        if callback not in self._on_change_callbacks:
            self._on_change_callbacks.append(callback)

    @property
    def on_follow_system_change(self):
        return self._on_followsys_change_cb

    @on_follow_system_change.setter
    def on_follow_system_change(self, callback):
        if callback not in self._on_followsys_change_cb:
            self._on_followsys_change_cb.append(callback)