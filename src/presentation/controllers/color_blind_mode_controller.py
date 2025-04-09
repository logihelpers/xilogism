from flet import *
from presentation.states.color_blind_state import ColorBlindState, ColorModes
from presentation.views.widgets.settings.settings_image_button import SettingsImageButton

from presentation.controllers.controller import Controller, Priority
from xilowidgets import EditorTheme

class ColorBlindModeController(Controller):
    group_id: str = "vision"
    priority = Priority.SETTINGS_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.cb_state = ColorBlindState()
        self.cb_state.on_change = self.change_mode

    def change_mode(self):
        active: ColorModes = self.cb_state.active
        
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