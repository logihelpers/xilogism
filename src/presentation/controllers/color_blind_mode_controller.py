from flet import *
from presentation.states.color_blind_state import ColorBlindState, ColorModes
from presentation.views.widgets.settings.settings_image_button import SettingsImageButton
from presentation.states.dialogs_state import Dialogs, DialogState
from presentation.controllers.controller import Controller, Priority
from presentation.views.dialogs.settings_dialog import SettingsDialog

class ColorBlindModeController(Controller):
    old_active: ColorModes = None
    group_id: str = "vision"
    priority = Priority.SETTINGS_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.cb_state = ColorBlindState()
        self.cb_state.on_change = self.change_mode
        self.dia_state = DialogState()
        self.dia_state.on_done_build = self.update_view

        self.settings_dialog: SettingsDialog = self.page.session.get("window").settings_dialog

        color_mode: str = self.page.client_storage.get("color_mode")
        try:
            self.cb_state.active = ColorModes(color_mode)
        except ValueError:
            self.cb_state.active = ColorModes.NORMAL
            self.page.client_storage.set("color_mode", ColorModes.NORMAL.value)
    
    def update_view(self):
        if self.dia_state.done_build == Dialogs.SETTINGS:
            self.old_active = None
            self.cb_state.active = ColorModes(self.page.client_storage.get("color_mode"))

    def change_mode(self):
        active: ColorModes = self.cb_state.active

        if self.old_active == active:
            return
        
        self.old_active = active
        
        try:
            button: SettingsImageButton = None
            for button in SettingsImageButton.refs[self.group_id]:
                if ColorModes(button.text) == active:
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

        self.page.client_storage.set("color_mode", active.value)