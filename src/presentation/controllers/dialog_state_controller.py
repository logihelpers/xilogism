from flet import *
from presentation.states.dialogs_state import *
from presentation.views.dialogs.settings_dialog import SettingsDialog
from presentation.views.dialogs.login_dialog import LoginDialog
from presentation.views.dialogs.registration_dialog import RegistrationDialog
from presentation.views.dialogs.export_print_dialog import ExportPrintDialog
from presentation.views.dialogs.create_new_dialog import CreateNewDialog
from presentation.views.dialogs.tutorial_dialog import TutorialDialog
from presentation.views.dialogs.bom_dialog import BOMDialog
from presentation.views.dialogs.profile_dialog import ProfileDialog

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
                self.active_dialog.open = False
            case Dialogs.SETTINGS:
                self.active_dialog = self.settings_dialog
                self.page.open(self.active_dialog)
            case Dialogs.LOGIN:
                self.active_dialog = LoginDialog()
                self.page.open(self.active_dialog)
            case Dialogs.REGISTER:
                self.active_dialog = RegistrationDialog()
                self.page.open(self.active_dialog)
            case Dialogs.EXPORT:
                self.active_dialog = ExportPrintDialog()
                self.page.open(self.active_dialog)
            case Dialogs.CREATE_NEW:
                self.active_dialog = CreateNewDialog()
                self.page.open(self.active_dialog)
            case Dialogs.TUTORIAL:
                self.active_dialog = TutorialDialog()
                self.page.open(self.active_dialog)
            case Dialogs.BOM:
                self.active_dialog = BOMDialog()
                self.page.open(self.active_dialog)
            case Dialogs.PROFILE:
                self.active_dialog = ProfileDialog()
                self.page.open(self.active_dialog)
        
        self.page.update()
        self.dia_state.done_build = active