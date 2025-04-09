from enum import Enum
from flet import *

from services.singleton import Singleton

class Dialogs(Enum):
    CLOSE = 0
    LOGIN = 1
    REGISTER = 2
    SETTINGS = 3
    PRINT = 4

class DialogState(metaclass=Singleton):
    def __init__(self):
        self._state__ = Dialogs.CLOSE
    
    @property
    def state(self) -> Dialogs:
        return self._state__
    
    @state.setter
    def state(self, state: Dialogs):
        self._state__ = state
        self.on_change()
    
    def on_change(self):
        pass

    @property
    def done_build(self) -> Dialogs:
        return self._done_build__

    @done_build.setter
    def done_build(self, done_build: Dialogs):
        self._done_build__ = done_build
        self.on_done_build()
    
    def on_done_build(self):
        pass