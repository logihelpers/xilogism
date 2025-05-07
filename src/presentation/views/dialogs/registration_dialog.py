from flet import *

from utils.singleton import Singleton
from xilowidgets import XDialog
from presentation.states.auth_state import AuthState
from presentation.states.dialogs_state import Dialogs, DialogState

class RegistrationDialog(XDialog, metaclass=Singleton):
    FIELD_WIDTH: float = 300
    FIELD_RADIUS: float = 100

    def __init__(self):
        super().__init__()
        self.bgcolor = "#ededed"
        self.width = 320
        self.height = 540
        self.open_duration = 300
        self.auth_state = AuthState()
        self.dia_state = DialogState()

    def build(self):
        self.name_field = self._create_text_field("Name", Icons.PERSON)
        self.email_field = self._create_text_field("Email", Icons.EMAIL)
        self.password_field = self._create_text_field("Password", Icons.LOCK, password=True)

        self.google_register_button = self._create_button(
            "SIGN UP WITH GOOGLE", self._on_google_signup_click
        )
        self.register_button = self._create_button(
            "REGISTER", self._on_register_click
        )

        self.content = Container(
            padding=padding.only(0, 16),
            border_radius=16,
            height=self.height,
            width=self.width,
            content=Column(
                spacing=10,
                controls=[
                    Row(controls=[Image(src="/user_icon.png", width=90, height=90)]),
                    Text("Register", size=40, weight=FontWeight.BOLD, color="#1D2357"),
                    Text("Create your account", size=14, weight=FontWeight.BOLD),
                    self.google_register_button,
                    self.name_field,
                    self.email_field,
                    self.password_field,
                    self.register_button,
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            TextButton(
                                content=Text(
                                    "Already have an account? Sign In",
                                    style=TextStyle(
                                        decoration=TextDecoration.UNDERLINE,
                                        weight=FontWeight.BOLD,
                                        color="#1D2357"
                                    )
                                ),
                                on_click=self._on_back_to_login_click
                            )
                        ]
                    ),
                ],
            )
        )

        super().build()

    def _create_text_field(self, label, icon, password=False):
        return TextField(
            label=label,
            prefix_icon=icon,
            password=password,
            bgcolor="white",
            border_radius=self.FIELD_RADIUS,
            border_color="#B2B2B2",
            content_padding=padding.all(12),
            width=self.FIELD_WIDTH,
        )

    def _create_button(self, text, on_click):
        return ElevatedButton(
            content=Text(text, color="white"),
            bgcolor="#1D2357",
            width=self.FIELD_WIDTH,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=self.FIELD_RADIUS),
                padding=padding.all(15),
            ),
            on_click=on_click
        )

    def _on_register_click(self, e):
        name = self.name_field.value.strip()
        email = self.email_field.value.strip()
        password = self.password_field.value.strip()

        if not (name and email and password):
            self.page.open(SnackBar(Text("Please fill all fields.")))
            self.page.update()
            return

        self.auth_state.request_register_email(name, email, password)
        self.dia_state.state = Dialogs.CLOSE
        self.page.open(SnackBar(Text("Registered successfully!")))
        self.page.update()

    def _on_google_signup_click(self, e):
        self.auth_state.request_google_login()

    def _on_back_to_login_click(self, e):
        self.dia_state.state = Dialogs.LOGIN