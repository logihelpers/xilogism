from flet import *

from services.singleton import Singleton

from xilowidgets.editor import EditorTheme

class EditorThemeState(metaclass = Singleton):
    def __init__(self):
        self._theme__: EditorTheme = EditorTheme.DEFAULT
        self._editor_theme: EditorTheme = EditorTheme.DEFAULT
    
    @property
    def theme(self) -> EditorTheme:
        return self._theme__
    
    @theme.setter
    def theme(self, theme: EditorTheme):
        self._theme__ = theme
        self.on_change()
    
    @property
    def editor_theme(self) -> EditorTheme:
        return self._editor_theme
    
    @editor_theme.setter
    def editor_theme(self, theme: EditorTheme):
        self._editor_theme = theme
        self.on_theme_change()
    
    @property
    def done_build(self) -> bool:
        return self._done_build
    
    @done_build.setter
    def done_build(self, done: bool):
        self._done_build = done
        self.on_done_build()
    
    def on_change(self):
        pass
    
    def on_theme_change(self):
        pass

    def on_done_build(self):
        pass