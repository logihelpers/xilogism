from flet import *
from xilowidgets import XDialog
from services.singleton import Singleton
from presentation.controllers.auth_controller import AuthController

class LoginDialog(XDialog, metaclass=Singleton):
    FIELD_WIDTH: float = 300
    FIELD_RADIUS: float = 100

    def __init__(self):
        super().__init__()
        self.bgcolor = "#ededed"
        self.width = 320
        self.height = 500
        self.open_duration = 300
        self.auth_controller: AuthController | None = None

    def build(self):
        if not self.auth_controller:
            self.auth_controller = AuthController(page=self.page, auth_dialog=self)

        self.email_field = self._create_text_field("Email", Icons.EMAIL)
        self.password_field = self._create_text_field("Password", Icons.LOCK, password=True)

        self.content = Container(
            padding=padding.all(16),
            border_radius=16,
            width=self.width,
            height=self.height,
            content=Column(
                spacing=10,
                controls=[
                    Row(controls=[Image(src="/user_icon.png", width=90, height=90)]),
                    Text("Login", size=40, weight=FontWeight.BOLD, color="#1D2357"),
                    Text("Please log in to continue", size=14, weight=FontWeight.BOLD),
                    self.email_field,
                    self.password_field,
                    Row(
                        alignment=MainAxisAlignment.END,
                        controls=[
                            TextButton(
                                content=Text(
                                    "Forgot your password?",
                                    style=TextStyle(
                                        decoration=TextDecoration.UNDERLINE,
                                        weight=FontWeight.BOLD,
                                        color="#1D2357"
                                    )
                                ),
                                on_click=self._on_forgot_password_click
                            )
                        ]
                    ),
                    self._create_button("LOGIN", self._on_login_click),
                    self._create_button("LOGIN WITH GOOGLE", self._on_google_login_click),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            TextButton(
                                content=Text(
                                    "Don't have an account? Sign Up",
                                    style=TextStyle(
                                        decoration=TextDecoration.UNDERLINE,
                                        weight=FontWeight.BOLD,
                                        color="#1D2357"
                                    )
                                ),
                                on_click=self._on_go_to_register_click
                            )
                        ]
                    ),
                ]
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

    def _on_login_click(self, e):
        email = self.email_field.value.strip()
        pw = self.password_field.value.strip()
        if email and pw:
            self.auth_controller.login_email(email, pw)
        else:
            self.page.snack_bar = SnackBar(
                content=Row(controls=[
                    Icon(icons.CLOSE, color="red"),
                    Text("Please fill in both email and password.")
                ])
            )
            self.page.snack_bar.open = True
            self.page.update()

    def _on_google_login_click(self, e):
        self.auth_controller.login_google()

    def _on_forgot_password_click(self, e):
        email = self.email_field.value.strip()
        if not email:
            self.page.snack_bar = SnackBar(
                content=Row(controls=[
                    Icon(icons.CLOSE, color="red"),
                    Text("Please enter your email to reset password.")
                ])
            )
            self.page.snack_bar.open = True
            self.page.update()
        else:
            self.auth_controller.forgot_password(email)
            self._show_info_dialog(
                "Password Reset",
                "We've sent a reset link to your email. Please check your inbox."
            )

    def _show_info_dialog(self, title: str, message: str):
        """Shows an info dialog with the provided title and message."""
        dialog = AlertDialog(
            modal=True,
            title=Text(title),
            content=Text(message),
            actions=[
                TextButton("OK", on_click=lambda e: self._close_info_dialog(dialog))
            ],
            actions_alignment=MainAxisAlignment.END
        )
        # Use page.open / page.close instead of overlay list manipulation
        self.page.open(dialog)
        self.page.update()

    def _close_info_dialog(self, dialog: AlertDialog):
        """Closes the info dialog cleanly via page.close."""
        self.page.close(dialog)
        self.page.update()

    def _on_go_to_register_click(self, e):
        self.open = False
        self.update()
        from presentation.views.dialogs.registration_dialog import RegistrationDialog
        reg_dlg = RegistrationDialog()
        reg_dlg.page = self.page
        self.page.open(reg_dlg)
        self.page.update()
