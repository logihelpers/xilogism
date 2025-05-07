from flet import *

from utils.singleton import Singleton

class ExpandCanvasState(metaclass = Singleton):
    def __init__(self):
        self._expand: bool = False
        self._on_change_callbacks = []
    
    @property
    def expand(self) -> bool:
        return self._expand
    
    @expand.setter
    def expand(self, expand: bool):
        self._expand = expand
        for callback in self._on_change_callbacks:
            callback()
    
    @property
    def on_change(self):
        return self._on_change_callbacks
    
    @on_change.setter
    def on_change(self, callback):
        if callback not in self._on_change_callbacks:
            self._on_change_callbacks.append(callback)