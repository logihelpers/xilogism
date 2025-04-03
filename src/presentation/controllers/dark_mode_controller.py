from presentation.states.dark_mode_state import *
from presentation.views.widgets.settings.settings_image_button import SettingsImageButton

from flet import *

class DarkModeController:
    group_id: str = "theme_mode"
    previous_saved_mode: ThemeMode = None
    def __init__(self, page: Page):
        self.page = page

        self.dm_state = DarkModeState()

        self.dm_state.on_change = self.change_active
        self.dm_state.on_follow_system_change = self.follow_system_change
    
    def follow_system_change(self):
        active: bool = self.dm_state.follow_system_active

        self.previous_saved_mode = self.page.theme_mode if active else self.previous_saved_mode
        self.page.theme_mode = ThemeMode.SYSTEM if active else self.previous_saved_mode
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