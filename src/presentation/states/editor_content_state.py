from enum import Enum
from flet import *

from services.singleton import Singleton

class CodeState(Enum):
    BLANK = "blank"
    CORRECT = "correct"
    WRONG = "wrong"

class ContentDict(dict):
    def __init__(self, on_change_callback=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._on_change_callback = on_change_callback

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if self._on_change_callback:
            self._on_change_callback()

    def __delitem__(self, key):
        super().__delitem__(key)
        if self._on_change_callback:
            self._on_change_callback()

class EditorContentState(metaclass = Singleton):
    def __init__(self):
        self._contents: ContentDict[str, str] = ContentDict(self.call_content_change_callbacks, {"New":""})
        self._code_state: ContentDict[str, CodeState] = ContentDict(self.call_code_state_change_callbacks, {"New":CodeState.BLANK})
        self._on_change: list[callable] = []
        self._on_code_state_change: list[callable] = []
    
    @property
    def content(self) -> ContentDict[str, str]:
        return self._contents
    
    @content.setter
    def content(self, content: ContentDict[str, str]):
        self._contents.update(content)
        self.call_content_change_callbacks()
    
    def call_content_change_callbacks(self):
        for callback in self._on_change:
            callback()
    
    @property
    def on_change(self):
        return self._on_change
    
    @on_change.setter
    def on_change(self, callback):
        if callback not in self.on_change:
            self._on_change.append(callback)

    @property
    def code_state(self) -> ContentDict[str, CodeState]:
        return self._code_state
    
    @code_state.setter
    def code_state(self, content: ContentDict[str, CodeState]):
        self._code_state.update(content)
        self.call_code_state_change_callbacks()
    
    @property
    def on_code_state_change(self):
        return self._on_code_state_change
    
    @on_code_state_change.setter
    def on_code_state_change(self, callback):
        if callback not in self._on_code_state_change:
            self._on_code_state_change.append(callback)
    
    def call_code_state_change_callbacks(self):
        for callback in self._on_code_state_change:
            callback()