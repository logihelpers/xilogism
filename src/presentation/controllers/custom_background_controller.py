from flet import *
from presentation.states.custom_background_state import CustomBackgroundState

from presentation.controllers.controller import Controller, Priority

class CustomBackgroundController(Controller):
    priority = Priority.SETTINGS_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.cb_state = CustomBackgroundState()
        self.cb_state.on_change = self.change_bg

        self.main_container: Container = self.page.session.get("window").main_container
    
    def change_bg(self):
        if not self.cb_state:
            self.main_container.image = None
            self.main_container.update()
            return
        
        self.main_container.image = DecorationImage(
            src=self.cb_state.active,
            fit= ImageFit.FILL
        )

        self.main_container.update()