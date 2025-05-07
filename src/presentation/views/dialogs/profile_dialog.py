from flet import *
from xilowidgets import XDialog
from presentation.states.dialogs_state import Dialogs, DialogState
from presentation.states.auth_state import AuthState
from presentation.states.language_state import LanguageState

class ProfileDialog(XDialog):
    def __init__(self):
        super().__init__()

        self.dia_state = DialogState()
        self.auth_state = AuthState()
        self.lang_state = LanguageState()

        self.profile_text = Text("Profile")
        self.icon_button = IconButton(icon=Icons.CLOSE, tooltip="Close", on_click=lambda e: setattr(self.dia_state, 'state', Dialogs.CLOSE))

        self.modal=True
        self.title=Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                self.profile_text,
                self.icon_button
            ]
        )

        self.content=Text(f"Signed in as {self.auth_state.user.get('displayName')}")
        self.actions=[
            TextButton("Logout", on_click=lambda e: self.auth_state.request_logout())
        ]
        
        self.actions_alignment=MainAxisAlignment.END
        self.on_dismiss=lambda e: setattr(self.dia_state, 'state', Dialogs.CLOSE)
    
    def did_mount(self):
        super().did_mount()
        self.lang_state.on_lang_updated = self.update_lang
        self.update_lang()
    
    def update_lang(self):
        lang_values = self.lang_state.lang_values
        self.profile_text.value = lang_values["profile"]
        self.icon_button.tooltip = lang_values["close_button"]
        self.content.value = lang_values["signed_in_as"] + f" {self.auth_state.user.get('displayName')}"
        self.actions[0].text = lang_values["logout"]
        self.update()