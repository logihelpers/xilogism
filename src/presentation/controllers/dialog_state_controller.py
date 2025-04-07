from flet import *
from presentation.states.dialogs_state import *
from presentation.views.dialogs.settings_dialog import SettingsDialog
from presentation.views.dialogs.login_dialog import LoginDialog
from presentation.views.dialogs.registration_dialog import RegistrationDialog

from presentation.controllers.controller import Controller, Priority

class DialogStateController(Controller):
    priority = Priority.DIALOG_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.dia_state = DialogState()
        self.dia_state.on_change = self.control_dialogs

        self.settings_dialog: SettingsDialog = self.page.session.get("window").settings_dialog

    def control_dialogs(self):
        active: Dialogs = self.dia_state.state
        
        match active:
            case Dialogs.CLOSE:
                [self.page.close(overlay) for overlay in self.page.overlay] # One liner close all dialogs
            case Dialogs.SETTINGS:
                self.page.open(self.settings_dialog)
            case Dialogs.LOGIN:
                self.page.open(LoginDialog())
            case Dialogs.REGISTER:
                self.page.open(RegistrationDialog())
        
        self.dia_state.done_build = active