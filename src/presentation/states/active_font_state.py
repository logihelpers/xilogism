from services.singleton import Singleton
from models.font_model import Font, FontType
from data.fonts import Fonts

class ActiveFontState(metaclass = Singleton):
    def __init__(self):
        self._active_font__: Font = Fonts.parse("Iosevka")
        self._font_size__: int = 16
    
    @property
    def active_font(self) -> Font:
        return self._active_font__
    
    @active_font.setter
    def active_font(self, active: str):
        self._active_font__ = Fonts.parse(active)
        self.on_font_change()
    
    @property
    def font_size(self) -> int:
        return self._font_size__
    
    @font_size.setter
    def font_size(self, size: int):
        self._font_size__ = size
        self.on_size_change()
    
    def on_font_change(self):
        pass

    def on_size_change(self):
        pass