from enum import Enum
from flet import *

from services.singleton import Singleton

class CodeState(Enum):
    BLANK = "blank"
    CORRECT = "correct"
    WRONG = "wrong"

class EditorContentState(metaclass = Singleton):
    def __init__(self):
        self._content__: str = ""
        self._code_state: CodeState = CodeState.BLANK
    
    @property
    def content(self) -> str:
        return self._content__
    
    @content.setter
    def content(self, content: str):
        self._content__ = content
        self.on_change()
    
    def on_change(self):
        pass

    @property
    def code_state(self) -> CodeState:
        return self._code_state
    
    @code_state.setter
    def code_state(self, content: CodeState):
        self._code_state = content
        self.on_code_state_change()
    
    def on_code_state_change(self):
        pass