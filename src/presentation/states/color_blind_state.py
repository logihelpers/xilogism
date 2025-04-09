from services.singleton import Singleton
from enum import Enum

class ColorModes(Enum):
    NORMAL = "Default"
    HIGH_CONTRAST = "High-Contrast"
    DEUTERANOPIA = "Deuteranopia"
    PROTANOPIA = "Protanopia"
    TRITANOPIA = "Tritanopia"

class ColorBlindState(metaclass = Singleton):
    def __init__(self):
        self._active: ColorModes = ColorModes.NORMAL
    
    @property
    def active(self) -> ColorModes:
        return self._active
    
    @active.setter
    def active(self, active: ColorModes):
        self._active = active
        self.on_change()
    
    def on_change(self):
        pass