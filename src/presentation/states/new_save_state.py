from enum import Enum
from flet import *

from services.singleton import Singleton

class NewSaveState(metaclass = Singleton):
    def __init__(self):
        self._state: bool = False
    
    @property
    def state(self) -> bool:
        return self._state__
    
    @state.setter
    def state(self, state: bool):
        self._state__ = state
        self.on_change()
    
    def on_change(self):
        pass