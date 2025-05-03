from presentation.states.title_button_state import *
from presentation.states.dialogs_state import *
from flet import Page

from presentation.controllers.controller import *

class TitleButtonsController(Controller):
    priority = Priority.VIEW_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.tb_state = TitleButtonState()
        self.dia_state = DialogState()

        self.tb_state.on_change = self.control_buttons
    
    def control_buttons(self):
        state: WindowState = self.tb_state.state

        match state:
            case WindowState.CLOSE:
                self.page.window.close()
            case WindowState.MAXIMIZE:
                self.page.window.maximized = not self.page.window.maximized
            case WindowState.MINIMIZE:
                self.page.window.minimized = True
            case WindowState.SETTINGS:
                self.dia_state.state = Dialogs.SETTINGS
            case WindowState.PROFILE:
                self.dia_state.state = Dialogs.LOGIN
            case WindowState.TUTORIAL:
                self.dia_state.state = Dialogs.TUTORIAL
        
        self.page.update()