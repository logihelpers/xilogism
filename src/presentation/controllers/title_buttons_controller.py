from presentation.states.title_button_state import *
from presentation.views.dialogs.settings_dialog import SettingsDialog
from flet import Page

class TitleButtonsController:
    def __init__(self, page: Page):
        self.page = page

        self.tb_state = TitleButtonState()

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
                self.page.open(SettingsDialog())
        
        self.page.update()