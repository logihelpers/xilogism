from enum import Enum
from flet import *

from services.singleton import Singleton

class MediaQueryState(metaclass = Singleton):
    def __init__(self):
        self._system_theme_mode__: ThemeMode = ThemeMode.LIGHT
    
    @property
    def system_theme_mode(self) -> ThemeMode:
        return self._system_theme_mode__
    
    @system_theme_mode.setter
    def system_theme_mode(self, system_theme_mode: ThemeMode):
        self._system_theme_mode__ = system_theme_mode
        self.on_system_theme_change()
    
    def on_system_theme_change(self):
        pass