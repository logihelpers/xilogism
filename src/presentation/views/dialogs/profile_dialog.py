from flet import *
from xilowidgets import XDialog
from presentation.states.dialogs_state import Dialogs, DialogState
from presentation.states.auth_state import AuthState
from presentation.states.language_state import LanguageState
from presentation.states.accent_color_state import AccentColorState

class ProfileDialog(XDialog):
    def __init__(self):
        super().__init__()

        self.dia_state = DialogState()
        self.auth_state = AuthState()
        self.lang_state = LanguageState()
        self.ac_state = AccentColorState()

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
        self.ac_state.on_colors_updated = self.update_colors
        self.update_colors()
    
    def update_colors(self):
        colors = self.ac_state.color_values
        self.bgcolor = colors["bg_color"]
        self.profile_text.color = colors["text_color"]
        self.content.color = colors["text_color"]
        self.icon_button.icon_color = colors["text_color"]
        self.actions[0].style = ButtonStyle(
            color = colors["text_color"]
        )
        self.update()
    
    def update_lang(self):
        lang_values = self.lang_state.lang_values
        self.profile_text.value = lang_values["profile"]
        self.icon_button.tooltip = lang_values["close_button"]
        try:
            user = self.auth_state.user.get('displayName')
        except:
            user = "Guest User"
        self.content.value = lang_values["signed_in_as"] + f" {user}"
        self.actions[0].text = lang_values["logout"]
        self.update()