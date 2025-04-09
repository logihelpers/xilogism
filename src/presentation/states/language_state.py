from services.singleton import Singleton
from enum import Enum

class Languages(Enum):
    ENGLISH = "English"
    TAGALOG = "Tagalog"
    CEBUANO = "Cebuano"
    SPANISH = "Spanish"
    FRENCH = "French"
    JAPANESE = "Japanese"
    MANDARIN = "Mandarin"
    BRAINROT = "Brainrot"

class LanguageState(metaclass = Singleton):
    def __init__(self):
        self._active: Languages = Languages.ENGLISH
    
    @property
    def active(self) -> Languages:
        return self._active
    
    @active.setter
    def active(self, active: Languages):
        self._active = active
        self.on_change()
    
    def on_change(self):
        pass