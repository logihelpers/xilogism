from presentation.states.accent_color_state import *
from presentation.views.widgets.settings.accent_color_button import AccentColorButton

from flet import *

from presentation.controllers.controller import Controller, Priority

class AccentColorController(Controller):
    priority = Priority.SETTINGS_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.ac_state = AccentColorState()

        self.ac_state.on_change = self.change_active

    def change_active(self):
        active: AccentColors = self.ac_state.active

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