from flet import *
from xilowidgets import XDialog

from presentation.states.dialogs_state import *
from presentation.states.animation_disable_state import AnimationDisableState
from presentation.states.language_state import LanguageState
from utils.singleton import Singleton
from presentation.states.dialogs_state import Dialogs, DialogState
from presentation.states.auth_state import AuthState
from presentation.states.accent_color_state import AccentColorState

class LoginDialog(XDialog, metaclass=Singleton):
    FIELD_WIDTH: float = 300
    FIELD_RADIUS: float = 100

    def __init__(self):
        super().__init__()
        self.ad_state = AnimationDisableState()
        self.ad_state.on_change = lambda: setattr(self, 'open_duration', 300 if self.ad_state.state else 0)
        self.lang_state = LanguageState()
        self.ac_state = AccentColorState()

        self.bgcolor = "#ededed"
        self.width = 320
        self.height = 500
        self.open_duration = 300

        self.auth_state = AuthState()
        self.dia_state = DialogState()

    def build(self):
        self.email_field = self._create_text_field("Email", Icons.EMAIL)
        self.password_field = self._create_text_field("Password", Icons.LOCK, password=True)

        self.login_text = Text("Login", size=40, weight=FontWeight.BOLD, color="#1D2357")
        self.pls_text = Text("Please log in to continue", size=14, weight=FontWeight.BOLD)

        self.forgot_text = Text(
            "Forgot your password?",
            style=TextStyle(
                decoration=TextDecoration.UNDERLINE,
                weight=FontWeight.BOLD,
                color="#1D2357"
            )
        )

        self.dont_have_acct_text = Text(
            "Don't have an account? Sign Up",
            style=TextStyle(
                decoration=TextDecoration.UNDERLINE,
                weight=FontWeight.BOLD,
                color="#1D2357"
            )
        )

        self.content = Container(
            padding=padding.all(16),
            border_radius=16,
            width=self.width,
            height=self.height,
            content=Column(
                spacing=10,
                controls=[
                    Row(controls=[Image(src="/user_icon.png", width=90, height=90)]), #0
                    self.login_text, #1
                    self.pls_text,#2
                    self.email_field,#3
                    self.password_field,#4
                    Row(#5
                        alignment=MainAxisAlignment.END,
                        controls=[
                            TextButton(
                                content=self.forgot_text,
                                on_click=self._on_forgot_password_click
                            )
                        ]
                    ),
                    self._create_button("LOGIN", self._on_login_click), #6
                    self._create_button("LOGIN WITH GOOGLE", self._on_google_login_click), #7
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            TextButton(
                                content=self.dont_have_acct_text,
                                on_click=self._on_go_to_register_click
                            )
                        ]
                    ),
                ]
            )
        )
        super().build()
    
    def did_mount(self):
        super().did_mount()
        self.lang_state.on_lang_updated = self.update_lang
        self.update_lang()
        self.ac_state.on_colors_updated = self.update_colors
        self.update_colors()
    
    def update_colors(self):
        colors = self.ac_state.color_values
        self.bgcolor = colors["bg_color"]
        self.content.content.controls[1].color = colors["primary_color"]  # Login title
        self.content.content.controls[2].color = colors["text_color"]  # Please log in
        self.email_field.bgcolor = colors["field_bgcolor"]
        self.email_field.border_color = colors["field_border_color"]
        self.password_field.bgcolor = colors["field_bgcolor"]
        self.password_field.border_color = colors["field_border_color"]
        self.content.content.controls[6].bgcolor = colors["primary_color"]  # LOGIN button
        self.content.content.controls[6].content.color = colors["text_color_alt"]
        self.content.content.controls[6].style = ButtonStyle(
            shape=RoundedRectangleBorder(radius=self.FIELD_RADIUS),
            padding=padding.all(15),
        )
        self.content.content.controls[7].bgcolor = colors["primary_color"]  # LOGIN WITH GOOGLE button
        self.content.content.controls[7].content.color = colors["text_color_alt"]
        self.content.content.controls[7].style = ButtonStyle(
            shape=RoundedRectangleBorder(radius=self.FIELD_RADIUS),
            padding=padding.all(15),
        )
        self.content.content.controls[5].controls[0].content.style.color = colors["primary_color"]  # Forgot password
        self.content.content.controls[8].controls[0].content.style.color = colors["primary_color"]  # Sign Up link
        self.update()

    def _create_text_field(self, label, icon, password=False):
        return TextField(
            label=label,
            prefix_icon=icon,
            password=password,
            can_reveal_password=True,
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

    def _on_login_click(self, e):
        email = self.email_field.value.strip()
        pw = self.password_field.value.strip()
        if email and pw:
            self.auth_state.request_login(email, pw)
        else:
            self.page.open(
                SnackBar(
                    content=Row(
                        controls=[
                            Icon(Icons.CLOSE, color="red"),
                            Text("Please fill in both email and password.")
                        ]
                    )
                )
            )

    def update_lang(self):
        lang_values = self.lang_state.lang_values
        self.login_text.value = lang_values["login_title"]
        self.pls_text.value = lang_values["please_login"]
        self.email_field.label = lang_values["email_field"]
        self.password_field.label = lang_values["password_field"]
        self.forgot_text.value = lang_values["forgot_password"]
        self.content.content.controls[6].content.value = lang_values["login_button"]
        self.content.content.controls[7].content.value = lang_values["google_login_button"]
        self.dont_have_acct_text.value = lang_values["sign_up_link"]
        self.update()

    def _on_google_login_click(self, e):
        self.auth_state.request_google_login()

    def _on_forgot_password_click(self, e):
        email = self.email_field.value.strip()
        if not email:
            self.page.open(
                SnackBar(
                    content=Row(
                        controls=[
                            Icon(Icons.CLOSE, color="red"),
                            Text("Please enter your email to reset password.")
                        ]
                    )
                )
            )
        else:
            self.auth_state.request_pw_change(email)
            self._show_info_dialog(
                "Password Reset",
                "We've sent a reset link to your email. Please check your inbox."
            )

    def _show_info_dialog(self, title: str, message: str):
        dialog = AlertDialog(
            modal=True,
            title=Text(title),
            content=Text(message),
            actions=[
                TextButton("OK", on_click=lambda e: setattr(self.dia_state, 'state', Dialogs.CLOSE))
            ],
            actions_alignment=MainAxisAlignment.END
        )
        # Use page.open / page.close instead of overlay list manipulation
        self.page.open(dialog)
        self.page.update()

    def _on_go_to_register_click(self, e):
        self.dia_state.state = Dialogs.REGISTER