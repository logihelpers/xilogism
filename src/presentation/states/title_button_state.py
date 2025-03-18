from enum import Enum
from flet import *

from services.singleton import Singleton

class WindowState(Enum):
    CLOSE = 1
    MINIMIZE = 2
    MAXIMIZE = 3

class TitleButtonState(metaclass = Singleton):
    def __init__(self):
        self._state__: WindowState = ""
    
    @property
    def state(self) -> WindowState:
        return self._state__
    
    @state.setter
    def state(self, state: WindowState):
        self._state__ = state
        self.on_change()
    
    def on_change(self):
        pass