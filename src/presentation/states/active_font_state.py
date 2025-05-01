from services.singleton import Singleton
from models.font_model import Font, FontType
from data.fonts import Fonts

class ActiveFontState(metaclass = Singleton):
    def __init__(self):
        self._active_font__: Font = Fonts.parse("Iosevka")
        self._font_size__: int = 16
        self._on_font_change: list[callable] = []
        self._on_size_change: list[callable] = []
    
    @property
    def active_font(self) -> Font:
        return self._active_font__
    
    @active_font.setter
    def active_font(self, active: str):
        self._active_font__ = Fonts.parse(active)
        for callback in self._on_font_change:
            callback()
    
    @property
    def font_size(self) -> int:
        return self._font_size__
    
    @font_size.setter
    def font_size(self, size: int):
        self._font_size__ = size
        for callback in self._on_size_change:
            callback()
    
    @property
    def on_font_change(self):
        return self._on_font_change

    @on_font_change.setter
    def on_font_change(self, callback):
        if callback not in self._on_font_change:
            self._on_font_change.append(callback)

    @property
    def on_size_change(self):
        return self._on_size_change
    
    @on_size_change.setter
    def on_size_change(self, callback):
        if callback not in self._on_size_change:
            self._on_size_change.append(callback)