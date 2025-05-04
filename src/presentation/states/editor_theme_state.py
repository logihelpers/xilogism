from flet import *

from services.singleton import Singleton

from xilowidgets.editor import EditorTheme

class EditorThemeState(metaclass = Singleton):
    def __init__(self):
        self._theme__: EditorTheme = EditorTheme.DEFAULT
        self._editor_theme: EditorTheme = EditorTheme.DEFAULT
        self._on_change: list[callable] = []
        self._on_theme_change: list[callable] = []
        self._on_done_build: list[callable] = []
    
    @property
    def theme(self) -> EditorTheme:
        return self._theme__
    
    @theme.setter
    def theme(self, theme: EditorTheme):
        self._theme__ = theme
        self.call_content_change_callbacks()
    
    @property
    def editor_theme(self) -> EditorTheme:
        return self._editor_theme
    
    @editor_theme.setter
    def editor_theme(self, theme: EditorTheme):
        self._editor_theme = theme
        for callback in self._on_theme_change:
            callback()
    
    @property
    def done_build(self) -> bool:
        return self._done_build
    
    @done_build.setter
    def done_build(self, done: bool):
        self._done_build = done
        for callback in self._on_done_build:
            callback()
    
    @property
    def on_change(self):
        return self._on_change
    
    @on_change.setter
    def on_change(self, callback):
        if callback not in self.on_change:
            self._on_change.append(callback)
    
    @property
    def on_theme_change(self):
        return self._on_theme_change
    
    @on_theme_change.setter
    def on_theme_change(self, callback):
        if callback not in self.on_theme_change:
            self._on_theme_change.append(callback)

    @property
    def on_done_build(self):
        return self._on_done_build
    
    @on_done_build.setter
    def on_done_build(self, callback):
        if callback not in self._on_done_build:
            self._on_done_build.append(callback)

    def call_content_change_callbacks(self):
        for callback in self._on_change:
            callback()