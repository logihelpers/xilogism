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
        self._color_values: dict = {}
        self._colors_updated_callbacks: list = []
    
    @property
    def active(self) -> AccentColors:
        return self._active
    
    @active.setter
    def active(self, active: AccentColors):
        self._active = active
        self.on_change()
    
    def on_change(self):
        pass

    @property
    def color_values(self) -> dict:
        return self._color_values
    
    @color_values.setter
    def color_values(self, value: dict):
        self._color_values.update(value)
        for callback in self._colors_updated_callbacks:
            callback()
    
    @property
    def on_colors_updated(self):
        return self._colors_updated_callbacks
    
    @on_colors_updated.setter
    def on_colors_updated(self, callback):
        if callback not in self._colors_updated_callbacks:
            self._colors_updated_callbacks.append(callback)