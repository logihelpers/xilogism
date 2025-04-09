from services.singleton import Singleton
from enum import Enum

class AccentColors(Enum):
    SORA = "#4d191f51"
    SAKURA = "#4d4d1c43"
    SUNA = "#4d4d1f23"
    CHA = "#4d512e1c"
    NORI = "#4d1c512e"
    KAKI = "#4d51431c"

class AccentColorState(metaclass = Singleton):
    def __init__(self):
        self._active: AccentColors = AccentColors.SORA
    
    @property
    def active(self) -> AccentColors:
        return self._active
    
    @active.setter
    def active(self, active: AccentColors):
        self._active = active
        self.on_change()
    
    def on_change(self):
        pass