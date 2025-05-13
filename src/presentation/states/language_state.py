from utils.singleton import Singleton
from enum import Enum

class Languages(Enum):
    English = "English"
    Tagalog = "Tagalog"
    Cebuano = "Cebuano"
    Español = "Spanish"
    Français = "French"
    日本語 = "Japanese"
    官话 = "Mandarin"
    BRAINROT = "Brainrot"

class LanguageState(metaclass = Singleton):
    def __init__(self):
        self._active: Languages = Languages.English
        self._on_change_callbacks: list = []
        self._lang_values: dict = {}
        self._lang_updated_callbacks: list = []
    
    @property
    def active(self) -> Languages:
        return self._active
    
    @active.setter
    def active(self, active: Languages):
        self._active = active
        for callback in self._on_change_callbacks:
            callback()
    
    @property
    def on_change(self):
        return self._on_change_callbacks

    @on_change.setter
    def on_change(self, callback):
        if callback not in self._on_change_callbacks:
            self._on_change_callbacks.append(callback)
    
    @property
    def lang_values(self) -> dict:
        return self._lang_values
    
    @lang_values.setter
    def lang_values(self, value: dict):
        self._lang_values.update(value)
        for callback in self._lang_updated_callbacks:
            callback()
    
    @property
    def on_lang_updated(self):
        return self._lang_updated_callbacks
    
    @on_lang_updated.setter
    def on_lang_updated(self, callback):
        if callback not in self._lang_updated_callbacks:
            self._lang_updated_callbacks.append(callback)