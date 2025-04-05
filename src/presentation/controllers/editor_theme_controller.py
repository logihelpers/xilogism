from flet import *
from presentation.states.editor_theme_state import EditorThemeState
from presentation.views.widgets.settings.settings_image_button import SettingsImageButton

from presentation.controllers.controller import Controller, Priority
from xilowidgets import EditorTheme

class EditorThemeStateController(Controller):
    group_id: str = "editor_theme"
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
        active: str = self.et_state.theme

        active_value = active.lower().replace(" ", "-")
        self.active_value = "androidstudio" if active_value == "android-studio" else active_value

        for theme in EditorTheme:
            if theme.value == active_value:
                self.et_state.editor_theme = theme
                self.page.client_storage.set("editor_theme", theme.value)
                break
        
        button: SettingsImageButton = None
        for button in SettingsImageButton.refs[self.group_id]:
            if button.text == active:
                button.active = True

                button.bgcolor = "#4d191f51"
                button.check_box.bgcolor = "#af191f51"
                button.border = border.all(1, "#191f51")
                button.label.weight = FontWeight.BOLD
                button.update()
            else:
                button.active = False

                button.bgcolor = "#00191f51"
                button.check_box.bgcolor = "#00191f51"
                button.border = border.all(1, "#006b6b6b")
                button.label.weight = FontWeight.NORMAL
                button.update()
    
    def update_button_states(self):
        self.et_state.theme = "Android Studio" if \
            self.active_value == "androidstudio" else \
            self.active_value.replace("-", " ").title()