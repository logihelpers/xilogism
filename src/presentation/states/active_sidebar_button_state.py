from enum import Enum
from flet import *

from services.singleton import Singleton

class ActiveSideBarButtonState(metaclass = Singleton):
    def __init__(self):
        self._active__: str = ""
        self._pin: str = ""
    
    @property
    def active(self) -> str:
        return self._active__
    
    @active.setter
    def active(self, active: str):
        self._active__ = active
        self.on_change()
    
    def on_change(self):
        pass

    @property
    def pin(self) -> str:
        return self._pin
    
    @pin.setter
    def pin(self, value: str):
        self._pin = value
        self.on_pin()
    
    def on_pin(self):
        pass