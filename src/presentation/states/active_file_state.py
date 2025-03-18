from enum import Enum
from flet import *

from services.singleton import Singleton
from models.xilo_file import XiloFile

class ActiveFileState(metaclass = Singleton):
    def __init__(self):
        self._active__: XiloFile | str = None
    
    @property
    def active(self) -> XiloFile | str:
        return self._active__
    
    @active.setter
    def active(self, active: XiloFile | str):
        self._active__ = active
        self.on_change()
    
    def on_change(self):
        pass