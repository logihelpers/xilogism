from presentation.states.dyslexia_friendly_state import DyslexiaFriendlyState
from presentation.views.widgets.settings.settings_image_button import SettingsImageButton

from flet import *

from presentation.controllers.controller import Controller, Priority

class DyslexiaFriendlyController(Controller):
    group_id: str = "dyslexia"
    priority = Priority.SETTINGS_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.df_state = DyslexiaFriendlyState()

        self.df_state.on_change = self.change_active

    def change_active(self):
        active: bool = self.df_state.active

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