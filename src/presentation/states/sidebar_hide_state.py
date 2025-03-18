import asyncio

from enum import Enum
from flet import *

from services.singleton import Singleton

class SideBarState(Enum):
    SHOWN = 1
    HIDDEN = 2

class SideBarHideState(metaclass=Singleton):
    def __init__(self):
        self._state__ = SideBarState.SHOWN
        self._on_change = None
    
    @property
    def state(self) -> SideBarState:
        return self._state__
    
    @state.setter
    def state(self, state: SideBarState):
        self._state__ = state
        if self._on_change:
            if asyncio.iscoroutinefunction(self._on_change):
                asyncio.ensure_future(self._on_change())
            else:
                self._on_change()
    
    async def invert(self, event: ControlEvent):
        self.state = SideBarState.HIDDEN if self.state is SideBarState.SHOWN else SideBarState.SHOWN
    
    @property
    def on_change(self):
        return self._on_change
    
    @on_change.setter
    def on_change(self, callback):
        self._on_change = callback