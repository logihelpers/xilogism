from flet import *
from presentation.states.settings_navigator_state import SettingsNavigatorState
from presentation.views.dialogs.settings_dialog import SettingsDialog

class SettingsNavigatorController:
    def __init__(self, page: Page):
        self.page = page

        self.settings_dialog = SettingsDialog()

        self.sn_state = SettingsNavigatorState()
        self.sn_state.on_change = self.switch_settings
    
    def switch_settings(self):
        active: int = self.sn_state.active

        self.settings_dialog.switcher.switch(active)
        self.settings_dialog.switcher.update()