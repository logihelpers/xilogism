from enum import Enum
from flet import *

from services.singleton import Singleton

class Dialogs(Enum):
    CLOSE = 0
    LOGIN = 1
    REGISTER = 2
    SETTINGS = 3
    EXPORT = 4
    CREATE_NEW = 5

class DialogState(metaclass=Singleton):
    def __init__(self):
        self._state__ = Dialogs.CLOSE
        self._done_build_callbacks: list = []
    
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
        for callback in self._done_build_callbacks:
            callback()
    
    @property
    def on_done_build(self):
        return self._done_build_callbacks
    
    @on_done_build.setter
    def on_done_build(self, callback):
        if callback not in self._done_build_callbacks:
            self._done_build_callbacks.append(callback)