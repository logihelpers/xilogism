from presentation.states.dyslexia_friendly_state import DyslexiaFriendlyState
from presentation.views.widgets.settings.settings_image_button import SettingsImageButton
from presentation.states.dialogs_state import Dialogs, DialogState
from presentation.views.dialogs.settings_dialog import SettingsDialog
from presentation.states.accent_color_state import AccentColorState
from presentation.states.dark_mode_state import *

from flet import *

from presentation.controllers.controller import Controller, Priority

class DyslexiaFriendlyController(Controller):
    old_active: bool = None
    group_id: str = "dyslexia"
    priority = Priority.SETTINGS_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.df_state = DyslexiaFriendlyState()
        self.df_state.on_change = self.change_active
        self.dia_state = DialogState()
        self.dia_state.on_done_build = self.update_view
        self.ac_state = AccentColorState()
        self.dm_state = DarkModeState()
        self.ac_state.on_colors_updated = self.change_active
        self.dm_state.on_change = self.change_active

        self.settings_dialog: SettingsDialog = self.page.session.get("window").settings_dialog

        use_dyslexic = bool(self.page.client_storage.get("use_dyslexic"))
        try:
            self.df_state.active = use_dyslexic
        except ValueError:
            self.df_state.active = False
            self.page.client_storage.set("use_dyslexic", False)

    def update_view(self):
        if self.dia_state.done_build == Dialogs.SETTINGS:
            self.old_active = None
            self.df_state.active = bool(self.page.client_storage.get("use_dyslexic"))

    def change_active(self):
        active: bool = self.df_state.active

        colors = self.ac_state.color_values
        dark_mode = self.dm_state.active == DarkModeScheme.DARK

        try:
            button: SettingsImageButton = None
            for button in SettingsImageButton.refs[self.group_id]:
                if (button.text == "Readable" and active) or (button.text == "Default" and not active):
                    button.active = True

                    button.bgcolor = colors["button_bgcolor"].replace("4d", "00") if dark_mode else colors["button_bgcolor"]
                    button.check_box.bgcolor = colors["button_bgcolor"].replace("4d", "af") if not dark_mode else "white"
                    button.check_box.border = border.all(colors["button_bgcolor"].replace("4d", "73"))
                    button.border = border.all(1, colors["button_bgcolor"].replace("4d", ""))
                    button.label.weight = FontWeight.BOLD
                else:
                    button.active = False

                    button.bgcolor = "#00191f51"
                    button.check_box.bgcolor = "#00191f51"
                    button.check_box.border = border.all(colors["button_bgcolor"].replace("4d", "73"))
                    button.border = border.all(1, "#006b6b6b")
                    button.label.weight = FontWeight.NORMAL

                button.update()
        except:
            pass

        self.page.theme.font_family = "OpenDyslexic" if active else "Inter"
        self.page.update()

        self.page.client_storage.set("use_dyslexic", active)