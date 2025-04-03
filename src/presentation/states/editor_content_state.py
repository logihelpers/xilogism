from enum import Enum
from flet import *

from services.singleton import Singleton

class EditorContentState(metaclass = Singleton):
    def __init__(self):
        self._content__: str = ""
    
    @property
    def content(self) -> str:
        return self._content__
    
    @content.setter
    def content(self, content: str):
        self._content__ = content
        self.on_change()
    
    def on_change(self):
        pass