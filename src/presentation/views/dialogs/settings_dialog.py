from flet import *
from slidablepanel import SlidablePanel

class SettingsDialog(AlertDialog):
    def __init__(self):
        super().__init__()
    
    def build(self):
        super().build()
        self.content_padding = 0
        self.title_padding = 0
        self.action_button_padding = 0
        self.elevation = 0
        self.actions = []
        self.actions_padding = 0
        self.clip_behavior = ClipBehavior.HARD_EDGE

        self.page.theme.dialog_theme = DialogTheme(
            bgcolor="#fafafa",
            shape=RoundedRectangleBorder(radius=8),
        )

        self.dark_mode_options = SlidablePanel(
            orientation=SlidablePanel.Orientation.VERTICAL,
            content_length=200,
            content = Row(
                spacing = 24,
                controls = [
                    Container(
                        content = Column(
                            controls = [
                                Image(
                                    src="/screenshot_light.png",
                                    width=240,
                                    height=135,
                                    anti_alias=True
                                ),
                                Text("Default")
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER
                        ),
                        padding=16,
                        bgcolor="#1a191f51",
                        border=border.all(1, "#191f51"),
                        border_radius=16
                    ),
                    Container(
                        content = Column(
                            controls = [
                                Image(
                                    src="/screenshot_dark.png",
                                    width=240,
                                    height=135,
                                    anti_alias=True
                                ),
                                Text("Dark")
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER
                        ),
                        padding=16,
                        bgcolor="#006b6b6b",
                        border=border.all(1, "#006b6b6b"),
                        border_radius=16,
                    )
                ]
            )
        )

        # self.modal = True
        self.modal = False
        self.content=WindowDragArea(
            height=600,
            width=800,
            expand=True,
            content = Row(
                width=800,
                height=600,
                expand=True,
                controls=[
                    Container(
                        content = Column(
                            expand = True,
                            controls=[
                                Container(Text("Appearance"), bgcolor="#d9d9d9",expand = True, padding=8)
                            ],
                            width=150,
                            horizontal_alignment=CrossAxisAlignment.STRETCH
                        ),
                        border=border.only(right=BorderSide(1, "black")),
                    ),
                    Container(
                        padding = 8,
                        height = 600,
                        expand=True,
                        content = Column(
                            horizontal_alignment=CrossAxisAlignment.STRETCH,
                            controls=[
                                Row(
                                    controls = [
                                        Image(src="/icons_light/personalization.png", width = 32, height = 32),
                                        Text(
                                            spans = [
                                                TextSpan(
                                                    text="Appearance\n",
                                                    style=TextStyle(
                                                        size=20,
                                                        weight=FontWeight.BOLD
                                                    )
                                                ),
                                                TextSpan(
                                                    text="Personalize the User Interface of Xilogism!",
                                                    style=TextStyle(
                                                        size=12
                                                    )
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                Container(
                                    padding = padding.only(top=16, bottom = 16),
                                    expand=True,
                                    content = Column(
                                        scroll=ScrollMode.ALWAYS,
                                        expand=True,
                                        spacing = 16,
                                        controls=[
                                            Text("Dark Mode", weight=FontWeight.BOLD),
                                            self.dark_mode_options,
                                            Switch(
                                                label="Follow System Dark Mode Settings:      ", 
                                                label_position=LabelPosition.LEFT,
                                                on_change=self.hide_panel
                                            ),
                                            Text("Accent Color", weight=FontWeight.BOLD),
                                            Row(
                                                controls = [
                                                    Container(content = Text(""), width=32, height=32, bgcolor=Colors.random(), border_radius=16, border=border.all(0.5, "black")),
                                                    Container(content = Text(""), width=32, height=32, bgcolor=Colors.random(), border_radius=16, border=border.all(0.5, "black")),
                                                    Container(content = Text(""), width=32, height=32, bgcolor=Colors.random(), border_radius=16, border=border.all(0.5, "black")),
                                                    Container(content = Text(""), width=32, height=32, bgcolor=Colors.random(), border_radius=16, border=border.all(0.5, "black")),
                                                    Container(content = Text(""), width=32, height=32, bgcolor=Colors.random(), border_radius=16, border=border.all(0.5, "black")),
                                                    Container(content = Text(""), width=32, height=32, bgcolor=Colors.random(), border_radius=16, border=border.all(0.5, "black"))
                                                ]
                                            ),
                                            Text("Sidebar Position", weight=FontWeight.BOLD),
                                            Row(
                                                spacing = 24,
                                                controls = [
                                                    Container(
                                                        content = Column(
                                                            controls = [
                                                                Image(
                                                                    src="/screenshot_light.png",
                                                                    width=240,
                                                                    height=135,
                                                                    anti_alias=True
                                                                ),
                                                                Text("Default")
                                                            ],
                                                            horizontal_alignment=CrossAxisAlignment.CENTER
                                                        ),
                                                        padding=16,
                                                        bgcolor="#1a191f51",
                                                        border=border.all(1, "#191f51"),
                                                        border_radius=16
                                                    ),
                                                    Container(
                                                        content = Column(
                                                            controls = [
                                                                Image(
                                                                    src="/sidebar_right_light.png",
                                                                    width=240,
                                                                    height=135,
                                                                    anti_alias=True
                                                                ),
                                                                Text("Right")
                                                            ],
                                                            horizontal_alignment=CrossAxisAlignment.CENTER
                                                        ),
                                                        padding=16,
                                                        bgcolor="#006b6b6b",
                                                        border=border.all(1, "#006b6b6b"),
                                                        border_radius=16,
                                                    )
                                                ]
                                            ),
                                        ]
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )

    def handle_close(self, e: ControlEvent):
        e.control.page.close(self)
    
    def hide_panel(self, event: ControlEvent):
        self.dark_mode_options.content_hidden = True if event.data == "true" else False
        self.dark_mode_options.update()