from flet import *
from presentation.states.language_state import LanguageState, Languages
from presentation.views.widgets.settings.language_settings import LanguageButton

from presentation.controllers.controller import Controller, Priority

class LanguageController(Controller):
    priority = Priority.SETTINGS_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.lang_state = LanguageState()
        self.lang_state.on_change = self.change_lang

    def change_lang(self):
        active: Languages = self.lang_state.active
        
        button: LanguageButton = None
        for button in LanguageButton.refs:
            if button.language == active:
                button.active = True

                button.leading.opacity = 1
            else:
                button.active = False

                button.leading.opacity = 0
            button.update()