from flet import *
from services.singleton import Singleton

from presentation.states.dialogs_state import *

class LoginDialog(AlertDialog, metaclass=Singleton):
    FIELD_WIDTH: float = 300
    FIELD_RADIUS: float = 100
    
    def __init__(self):
        super().__init__()
        self.bgcolor = "#FFFFFF"
        self.width = 320
        self.height = 720

        self.dia_state = DialogState()
        self.on_dismiss = lambda e: setattr(self.dia_state, 'state', Dialogs.CLOSE)
        
    def build(self):
        self.content = Container(
            content=Column(
                alignment=MainAxisAlignment.START,
                horizontal_alignment=CrossAxisAlignment.START,
                spacing=10,
                controls=[
                    Row(
                        alignment=MainAxisAlignment.START,
                        controls=[
                            Image(
                                src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
                                width=90,
                                height=90
                            )
                        ]
                    ),
                    Text(
                        value="Login",
                        size=40,
                        weight=FontWeight.BOLD,
                        color="#1D2357",
                        text_align=TextAlign.LEFT,
                        style=TextStyle(font_family="Inter")
                    ),
                    Container(
                        margin=margin.only(top=5),
                        content=Text(
                            value="Please log in to continue",
                            weight=FontWeight.BOLD,
                            size=14,
                            color="black",
                            text_align=TextAlign.LEFT,
                            style=TextStyle(font_family="Inter")
                        )
                    ),
                    self._create_text_field("Email", Icons.EMAIL),
                    self._create_text_field("Password", Icons.LOCK, password=True),
                    Row(
                        alignment=MainAxisAlignment.END,
                        controls=[
                            TextButton(
                                content=Text(
                                    value="Forgot your password?",
                                    color="#1D2357",
                                    style=TextStyle(
                                        decoration=TextDecoration.UNDERLINE,
                                        weight=FontWeight.BOLD,
                                        font_family="Inter"
                                    )
                                )
                            )
                        ]
                    ),
                    self._create_button("LOGIN"),
                    self._create_button("LOGIN WITH GOOGLE"),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            TextButton(
                                content=Text(
                                    value="Don't have an account? Sign Up",
                                    color="#1D2357",
                                    style=TextStyle(
                                        decoration=TextDecoration.UNDERLINE,
                                        weight=FontWeight.BOLD,
                                        font_family="Inter"
                                    )
                                )
                            )
                        ]
                    )
                ]
            ),
            padding=padding.all(16),
            border_radius=15,
            bgcolor="lightgray",
            width=320
        )
        super().build()

    def _create_text_field(self, label: str, icon, password: bool = False):
        return TextField(
            label=label,
            prefix_icon=icon,
            bgcolor="white",
            color="black",
            border_radius=self.FIELD_RADIUS,
            border_color="#B2B2B2",
            content_padding=padding.only(left=15, top=10, right=10, bottom=10),
            password=password,
            width=self.FIELD_WIDTH,
            label_style=TextStyle(
                color="black",
                font_family="Inter"
            )
        )

    def _create_button(self, text: str, icon=None, bgcolor: str = "#1D2357", text_color: str = "white"):
        return ElevatedButton(
            content=Text(
                value=text,
                color=text_color,
                style=TextStyle(font_family="Inter")
            ),
            icon=icon,
            bgcolor=bgcolor,
            width=self.FIELD_WIDTH,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=self.FIELD_RADIUS),
                padding=padding.all(15)
            )
        )