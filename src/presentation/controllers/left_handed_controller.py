from presentation.states.left_handed_state import LeftHandedState
from presentation.views.widgets.settings.settings_image_button import SettingsImageButton

from flet import *

from presentation.controllers.controller import Controller, Priority

class LeftHandedController(Controller):
    group_id: str = "sidebar_pos"
    priority = Priority.SETTINGS_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.lh_state = LeftHandedState()

        self.lh_state.on_change = self.change_state

    def change_state(self):
        active: bool = self.lh_state.state

        button: SettingsImageButton = None
        for button in SettingsImageButton.refs[self.group_id]:
            if (button.text == "Left-Handed" and active) or (button.text == "Default" and not active):
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