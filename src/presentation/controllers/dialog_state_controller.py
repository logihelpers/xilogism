from flet import *
from presentation.states.dialogs_state import *
from presentation.views.dialogs.settings_dialog import SettingsDialog
from presentation.views.dialogs.login_dialog import LoginDialog
from presentation.views.dialogs.registration_dialog import RegistrationDialog
from presentation.views.dialogs.export_print_dialog import ExportPrintDialog
from presentation.views.dialogs.create_new_dialog import CreateNewDialog
from presentation.views.dialogs.tutorial_dialog import TutorialDialog

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
                try:
                    [self.page.close(overlay) for overlay in self.page.overlay] # One liner close all dialogs
                except:
                    pass
            case Dialogs.SETTINGS:
                self.page.open(self.settings_dialog)
            case Dialogs.LOGIN:
                self.page.open(LoginDialog())
            case Dialogs.REGISTER:
                self.page.open(RegistrationDialog())
            case Dialogs.EXPORT:
                self.page.open(ExportPrintDialog())
            case Dialogs.CREATE_NEW:
                self.page.open(CreateNewDialog())
            case Dialogs.TUTORIAL:
                self.page.open(TutorialDialog())
        
        self.dia_state.done_build = active