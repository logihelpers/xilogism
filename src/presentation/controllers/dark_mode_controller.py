from presentation.states.dark_mode_state import DarkModeState, DarkModeScheme
from presentation.states.dialogs_state import *
from presentation.states.accent_color_state import AccentColors, AccentColorState
from presentation.views.widgets.settings.settings_image_button import SettingsImageButton
from data.colors import get_colors
from flet import *

from presentation.controllers.controller import Controller, Priority

class DarkModeController(Controller):
    old_active: DarkModeScheme = None
    group_id: str = "theme_mode"
    priority = Priority.SETTINGS_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.dm_state = DarkModeState()
        self.dia_state = DialogState()
        self.ac_state = AccentColorState()

        self.dm_state.on_change = self.change_active
        self.dm_state.on_follow_system_change = self.follow_system_change
        self.dia_state.on_done_build = self.update_view

        if not self.page.client_storage.contains_key("dark_mode"):
            self.page.client_storage.set("dark_mode", DarkModeScheme.LIGHT.value) # Default to Light Mode

        if not self.page.client_storage.contains_key("follow_sysdark_mode"):
            self.page.client_storage.set("follow_sysdark_mode", False) # Default to Manual
        
        dark_mode = DarkModeScheme(self.page.client_storage.get("dark_mode"))
        try:
            self.dm_state.active = dark_mode
        except ValueError:
            self.dm_state.active = DarkModeScheme.LIGHT
            self.page.client_storage.set("dark_mode", DarkModeScheme.LIGHT)
    
    def update_view(self):
        if self.dia_state.done_build == Dialogs.SETTINGS:
            self.old_active = None
            self.dm_state.active = DarkModeScheme(bool(self.page.client_storage.get("dark_mode")))
            self.dm_state.follow_system_active = bool(self.page.client_storage.get("follow_sysdark_mode"))

    def follow_system_change(self):
        active = self.dm_state.follow_system_active

        self.page.theme_mode = ThemeMode.SYSTEM if \
            active else ThemeMode.DARK if DarkModeScheme(self.page.client_storage.get("dark_mode")) == DarkModeScheme.DARK else \
            ThemeMode.LIGHT
        
        self.page.client_storage.set("follow_sysdark_mode", active)
        self.page.update()

    def change_active(self):
        active = DarkModeScheme(self.dm_state.active)

        if self.old_active == active:
            return
        
        self.old_active = active

        self.page.theme_mode = ThemeMode.DARK if active == DarkModeScheme.DARK else ThemeMode.LIGHT

        colors = get_colors(active, self.ac_state.active)
        self.ac_state.color_values = colors
        
        accent_color = self.ac_state.active.value
        bg_color = colors["bg_color"]
        divider_color = colors["divider_color"]

        try:
            button: SettingsImageButton = None
            for button in SettingsImageButton.refs[self.group_id]:
                if (button.text == "Dark" and active.value) or (button.text == "Default" and not active.value):
                    button.active = True

                    button.bgcolor = accent_color
                    button.check_box.bgcolor = accent_color
                    button.border = border.all(1, divider_color)
                    button.label.weight = FontWeight.BOLD
                    button.update()

                    self.page.update()
                else:
                    button.active = False

                    button.bgcolor = bg_color
                    button.check_box.bgcolor = bg_color
                    button.border = border.all(1, divider_color)
                    button.label.weight = FontWeight.NORMAL
                    button.update()

                    self.page.update()
        except:
            pass
        
        self.page.client_storage.set("dark_mode", active.value)
