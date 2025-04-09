from presentation.states.dark_mode_state import *
from presentation.states.dialogs_state import *
from presentation.states.media_query_state import MediaQueryState
from presentation.views.widgets.settings.settings_image_button import SettingsImageButton

from flet import *

from presentation.controllers.controller import Controller, Priority

class DarkModeController(Controller):
    group_id: str = "theme_mode"
    priority = Priority.SETTINGS_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.dm_state = DarkModeState()
        self.dia_state = DialogState()
        self.mq_state = MediaQueryState()

        self.dm_state.on_change = self.change_active
        self.dm_state.on_follow_system_change = self.follow_system_change
        self.dia_state.on_done_build = self.update_view

        if not self.page.client_storage.contains_key("dark_mode"):
            self.page.client_storage.set("dark_mode", False) # Default to Dark Mode

        if not self.page.client_storage.contains_key("follow_sysdark_mode"):
            self.page.client_storage.set("follow_sysdark_mode", False) # Default to Manual
    
    def update_view(self):
        if self.dia_state.done_build == Dialogs.SETTINGS:
            self.dm_state.active = bool(self.page.client_storage.get("dark_mode"))
            self.dm_state.follow_system_active = bool(self.page.client_storage.get("follow_sysdark_mode"))

    def follow_system_change(self):
        active: bool = self.dm_state.follow_system_active

        self.page.theme_mode = ThemeMode.SYSTEM if \
            active else ThemeMode.DARK if bool(self.page.client_storage.get("dark_mode")) else \
            ThemeMode.LIGHT
        
        self.page.client_storage.set("follow_sysdark_mode", active)

        self.page.update()

    def change_active(self):
        active: bool = self.dm_state.active

        button: SettingsImageButton = None
        for button in SettingsImageButton.refs[self.group_id]:
            if (button.text == "Dark" and active) or (button.text == "Default" and not active):
                button.active = True

                button.bgcolor = "#4d191f51"
                button.check_box.bgcolor = "#af191f51"
                button.border = border.all(1, "#191f51")
                button.label.weight = FontWeight.BOLD
                button.update()

                self.page.theme_mode = ThemeMode.DARK
                self.page.update()
            else:
                button.active = False

                button.bgcolor = "#00191f51"
                button.check_box.bgcolor = "#00191f51"
                button.border = border.all(1, "#006b6b6b")
                button.label.weight = FontWeight.NORMAL
                button.update()

                self.page.theme_mode = ThemeMode.LIGHT
                self.page.update()
        
        self.page.client_storage.set("dark_mode", active)