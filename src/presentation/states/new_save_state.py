from enum import Enum
from flet import *

from utils.singleton import Singleton

class NewSaveState(metaclass = Singleton):
    def __init__(self):
        self._state: bool = False
        self._on_change_callbacks: list = []
        self._project_name: str = ""
        self._filename: str = ""
    
    @property
    def project_name(self) -> str:
        return self._project_name
    
    @project_name.setter
    def project_name(self, value: str):
        self._project_name = value
    
    @property
    def filename(self) -> str:
        return self._filename
    
    @filename.setter
    def filename(self, value: str):
        self._filename = value
    
    @property
    def state(self) -> bool:
        return self._state__
    
    @state.setter
    def state(self, state: bool):
        self._state__ = state
        for callback in self._on_change_callbacks:
            callback()
    
    @property
    def on_change(self):
        return self._on_change_callbacks

    @on_change.setter
    def on_change(self, callback):
        if callback not in self._on_change_callbacks:
            self._on_change_callbacks.append(callback)