from flet import *
from xilowidgets import XDialog
from presentation.states.dialogs_state import Dialogs, DialogState
from presentation.states.auth_state import AuthState

class ProfileDialog(XDialog):
    def __init__(self):
        super().__init__()

        self.dia_state = DialogState()
        self.auth_state = AuthState()

        self.modal=True
        self.title=Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                Text("Profile"),
                IconButton(icon=Icons.CLOSE, tooltip="Close", on_click=lambda e: setattr(self.dia_state, 'state', Dialogs.CLOSE))
            ]
        )

        self.content=Text(f"Signed in as {self.auth_state.user.get('displayName')}")
        self.actions=[
            TextButton("Logout", on_click=lambda e: self.auth_state.request_logout())
        ]
        
        self.actions_alignment=MainAxisAlignment.END
        self.on_dismiss=lambda e: setattr(self.dia_state, 'state', Dialogs.CLOSE)