from presentation.states.dyslexia_friendly_state import DyslexiaFriendlyState
from presentation.views.widgets.settings.settings_image_button import SettingsImageButton
from presentation.states.dialogs_state import Dialogs, DialogState
from presentation.views.dialogs.settings_dialog import SettingsDialog

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

        if self.old_active == active:
            return
        
        self.old_active = active

        try:
            button: SettingsImageButton = None
            for button in SettingsImageButton.refs[self.group_id]:
                if (button.text == "Readable" and active) or (button.text == "Default" and not active):
                    button.active = True

                    button.bgcolor = "#4d191f51"
                    button.check_box.bgcolor = "#af191f51"
                    button.border = border.all(1, "#191f51")
                    button.label.weight = FontWeight.BOLD
                else:
                    button.active = False

                    button.bgcolor = "#00191f51"
                    button.check_box.bgcolor = "#00191f51"
                    button.border = border.all(1, "#006b6b6b")
                    button.label.weight = FontWeight.NORMAL

                button.update()
        except:
            pass

        self.page.theme.font_family = "OpenDyslexic" if active else "Inter"
        self.page.update()

        self.page.client_storage.set("use_dyslexic", active)