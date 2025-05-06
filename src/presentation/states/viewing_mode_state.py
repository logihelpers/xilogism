from enum import Enum
from flet import *

from services.singleton import Singleton

class ViewingMode(Enum):
    LOGIC = "Logic Diagram"
    CIRCUIT = "Circuit Diagram"

class ViewingModeState(metaclass = Singleton):
    def __init__(self):
        self._state: ViewingMode = ViewingMode.LOGIC
        self._on_change_callbacks: list = []
    
    @property
    def state(self) -> bool:
        return self._state
    
    @state.setter
    def state(self, state: bool):
        self._state = state
        for callback in self._on_change_callbacks:
            callback()
    
    @property
    def on_change(self):
        return self._on_change_callbacks

    @on_change.setter
    def on_change(self, callback):
        if callback not in self._on_change_callbacks:
            self._on_change_callbacks.append(callback)