from flet import *
from services.singleton import Singleton
from xilowidgets import XDialog

from presentation.states.dialogs_state import *
from presentation.states.animation_disable_state import AnimationDisableState
from presentation.states.language_state import LanguageState

class RegistrationDialog(XDialog, metaclass=Singleton):
    FIELD_WIDTH: float = 300
    FIELD_RADIUS: float = 100
    
    def __init__(self):
        super().__init__()
        self.dia_state = DialogState()
        self.ad_state = AnimationDisableState()
        self.lang_state = LanguageState()

        self.ad_state.on_change = lambda: setattr(self, 'open_duration', 300 if self.ad_state.state else 0)

        self.bgcolor = "#ededed"
        self.width = 320
        self.height = 540
        self.open_duration = 300 if self.ad_state.state else 0

        self.on_dismiss = lambda e: setattr(self.dia_state, 'state', Dialogs.CLOSE)
        
    def build(self):
        self.content = Container(
            padding=padding.only(0, 16),
            border_radius=16,
            height=540,
            width=320,
            content=Column(
                alignment=MainAxisAlignment.START,
                horizontal_alignment=CrossAxisAlignment.START,
                spacing=10,
                controls=[
                    Row(
                        alignment=MainAxisAlignment.START,
                        controls=[
                            Image(
                                src="/user_icon.png",
                                width=90,
                                height=90
                            )
                        ]
                    ),
                    Text(
                        value="Register",
                        size=40,
                        weight=FontWeight.BOLD,
                        color="#1D2357",
                        text_align=TextAlign.LEFT,
                        style=TextStyle(font_family="Inter")
                    ),
                    Container(
                        margin=margin.only(top=5),
                        content=Text(
                            value="Create your account",
                            weight=FontWeight.BOLD,
                            size=14,
                            color="black",
                            text_align=TextAlign.LEFT,
                            style=TextStyle(font_family="Inter")
                        )
                    ),
                    self._create_button("SIGN UP WITH GOOGLE"),
                    self._create_text_field("Name", Icons.PERSON),
                    self._create_text_field("Email", Icons.EMAIL),
                    self._create_text_field("Password", Icons.LOCK, password=True),
                    self._create_button("REGISTER"),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            TextButton(
                                content=Text(
                                    value="Already have an account? Sign In",
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
            )
        )
        super().build()
    
    def did_mount(self):
        super().did_mount()
        self.lang_state.on_lang_updated = self.update_lang
        self.update_lang()

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
    
    def update_lang(self):
        lang_values = self.lang_state.lang_values
        self.content.content.controls[1].value = lang_values["register_title"]
        self.content.content.controls[2].content.value = lang_values["create_account"]
        self.content.content.controls[3].content.value = lang_values["sign_up_google"]
        self.content.content.controls[4].label = lang_values["name_field"]
        self.content.content.controls[5].label = lang_values["email_field"]
        self.content.content.controls[6].label = lang_values["password_field"]
        self.content.content.controls[7].content.value = lang_values["register_button"]
        self.content.content.controls[8].controls[0].content.value = lang_values["sign_in_link"]
        self.update()