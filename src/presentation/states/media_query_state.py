from enum import Enum
from flet import *
from typing import Tuple, Optional

from utils.singleton import Singleton

class MediaQueryState(metaclass = Singleton):
    def __init__(self):
        self._system_theme_mode__: ThemeMode = ThemeMode.LIGHT
        self._size: Tuple[int, int] = (0, 0)
    
    @property
    def system_theme_mode(self) -> ThemeMode:
        return self._system_theme_mode__
    
    @system_theme_mode.setter
    def system_theme_mode(self, system_theme_mode: ThemeMode):
        self._system_theme_mode__ = system_theme_mode
        self.on_system_theme_change()
    
    def on_system_theme_change(self):
        pass

    @property
    def size(self) -> Optional[Tuple[int, int]]:
        return self._size
    
    @size.setter
    def size(self, new_size: Optional[Tuple[int, int]]):
        self._size = new_size
        self.on_size_change()
    
    def on_size_change(self):
        pass