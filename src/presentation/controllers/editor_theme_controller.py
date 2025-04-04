from flet import *
from presentation.states.editor_theme_state import EditorThemeState

from presentation.controllers.controller import Controller, Priority
from xilowidgets import EditorTheme

class EditorThemeStateController(Controller):
    priority = Priority.SETTINGS_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.et_state = EditorThemeState()
        self.et_state.on_change = self.change_theme

        if not self.page.client_storage.contains_key("editor_theme"):
            self.page.client_storage.set("editor_theme", EditorTheme.DEFAULT.value)

        self.et_state.editor_theme = EditorTheme(self.page.client_storage.get("editor_theme"))

    def change_theme(self):
        active: str = self.et_state.theme

        active = "androidstudio" if active == "android-studio" else active

        for theme in EditorTheme:
            if theme.value == active:
                self.et_state.editor_theme = theme
                self.page.client_storage.set("editor_theme", theme.value)
                break