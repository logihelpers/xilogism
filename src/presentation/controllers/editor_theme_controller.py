from flet import *
from presentation.states.editor_theme_state import EditorThemeState
from presentation.views.widgets.settings.appearance_settings import ThemeButton

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

        self.active_value: str = self.page.client_storage.get("editor_theme")

        self.et_state.editor_theme = EditorTheme(self.active_value)
        
        self.et_state.on_done_build = self.update_button_states

    def change_theme(self):
        active: EditorTheme = self.et_state.theme

        self.active_value = active.value

        self.et_state.editor_theme = active
        self.page.client_storage.set("editor_theme", self.active_value)
        
        button: ThemeButton = None
        for button in ThemeButton.refs:
            if button.key == active:
                button.active = True

                button.leading.opacity = 1
            else:
                button.active = False

                button.leading.opacity = 0
            button.update()
    
    def update_button_states(self):
        self.et_state.theme = EditorTheme(self.active_value)