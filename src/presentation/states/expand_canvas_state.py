from flet import *

from services.singleton import Singleton

class ExpandCanvasState(metaclass = Singleton):
    def __init__(self):
        self._expand: bool = False
    
    @property
    def expand(self) -> bool:
        return self._expand
    
    @expand.setter
    def expand(self, expand: bool):
        self._expand = expand
        self.on_change()
    
    def on_change(self):
        pass