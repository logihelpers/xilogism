from flet import *
from presentation.states.language_state import LanguageState, Languages
from presentation.states.dialogs_state import DialogState, Dialogs
from presentation.views.widgets.settings.language_settings import LanguageButton
from presentation.views.dialogs.settings_dialog import SettingsDialog
from lang import get_text_values

from presentation.controllers.controller import Controller, Priority

class LanguageController(Controller):
    old_active: Languages = None
    priority = Priority.VIEW_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.lang_state = LanguageState()
        self.lang_state.on_change = self.change_lang
        self.dia_state = DialogState()
        self.dia_state.on_done_build = self.update_view

        self.settings_dialog: SettingsDialog = self.page.session.get("window").settings_dialog

        lang: str = self.page.client_storage.get("language")
        try:
            self.lang_state.active = Languages(lang)
        except ValueError:
            self.lang_state.active = Languages.ENGLISH
            self.page.client_storage.set("language", Languages.ENGLISH.value)
    
    def update_view(self):
        if self.dia_state.done_build == Dialogs.SETTINGS:
            self.old_active = None
            self.lang_state.active = Languages(self.page.client_storage.get("language"))

    def change_lang(self):
        active: Languages = self.lang_state.active

        if self.old_active == active:
            return
        
        self.old_active = active

        self.lang_state.lang_values = get_text_values(active.value)
        
        try:
            button: LanguageButton = None
            for button in LanguageButton.refs:
                if button.language == active:
                    button.active = True
                    self.settings_dialog.language_settings.preview_image.src = f"/icons_light/language_{button.language.name.lower()}.png"
                    self.settings_dialog.language_settings.preview_image.update()
                    button.leading.opacity = 1
                else:
                    button.active = False

                    button.leading.opacity = 0
                button.update()
        except:
            pass

        self.page.client_storage.set("language", active.value)