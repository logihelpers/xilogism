from presentation.states.accent_color_state import *
from presentation.views.widgets.settings.accent_color_button import AccentColorButton
from presentation.states.dialogs_state import Dialogs, DialogState
from presentation.states.dark_mode_state import DarkModeState, DarkModeScheme
from data.colors import get_colors

from flet import *

from presentation.controllers.controller import Controller, Priority

class AccentColorController(Controller):
    old_active: AccentColors = None
    priority = Priority.SETTINGS_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.ac_state = AccentColorState()
        self.ac_state.on_change = self.change_active
        self.dia_state = DialogState()
        self.dia_state.on_done_build = self.update_view
        self.dm_state = DarkModeState()

        if not self.page.client_storage.contains_key("accent_color"):
            self.page.client_storage.set("accent_color", AccentColors.SORA.value) # default to sora

        accent = AccentColors(self.page.client_storage.get("accent_color"))
        try:
            self.ac_state.active = accent
        except ValueError:
            self.ac_state.active = AccentColors.SORA
            self.page.client_storage.set("accent_color", AccentColors.SORA.value)
    
    def update_view(self):
        if self.dia_state.done_build == Dialogs.SETTINGS:
            self.old_active = None
            self.ac_state.active = AccentColors(self.page.client_storage.get("accent_color"))

    def change_active(self):
        active: AccentColors = self.ac_state.active

        colors = get_colors(self.dm_state.active, active)
        self.ac_state.color_values = colors

        self.page.theme.color_scheme_seed = colors["button_bgcolor"].replace("4d", "")
        self.page.update()

        self.dm_state.active = self.dm_state.active

        try:
            button: AccentColorButton = None
            for button in AccentColorButton.refs:
                if button.color == active:
                    button.active = True

                    button.main_content.border = border.all(1.5, Colors.BLACK)
                    button.main_content.update()

                    button.main_content.content.value = "✓"
                    button.main_content.content.color = "black"
                    button.main_content.content.update()

                    button.name_text.weight = FontWeight.W_600
                    button.name_text.update()
                else:
                    button.active = False

                    button.main_content.border = border.all(0.5, Colors.BLACK)
                    button.main_content.update()

                    button.main_content.content.value = ""
                    button.main_content.content.color = "black"
                    button.main_content.content.update()

                    button.name_text.weight = FontWeight.W_400
                    button.name_text.update()
        except:
            pass
        
        self.page.client_storage.set("accent_color", active.value)