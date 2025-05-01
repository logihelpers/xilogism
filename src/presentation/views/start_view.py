from flet import *
from presentation.states.active_sidebar_button_state import ActiveSideBarButtonState

class StartView(Container):
    widget_scale: float = 1.0
    old_scale: float = 1.0
    def __init__(self):
        super().__init__()
        self.widget_scale = 1.0

        self.active_sidebar_button_state = ActiveSideBarButtonState()
    
    def build(self):
        self.padding = padding.all(16)
        self.expand = True
        self.expand_loose = True

        self.new_button = FilledButton(
            on_click = lambda event: setattr(self.active_sidebar_button_state, 'active', "New Xilogism"),
            scale=transform.Scale(scale=1),
            animate_scale=animation.Animation(250, AnimationCurve.BOUNCE_OUT),
            content=Container(
                padding = padding.all(16),
                content = Row(
                    controls=[
                        Image(
                            src="/icons_light/new.png",
                            width=56,
                            height=56
                        ),
                        Text(
                            spans=[
                                TextSpan(
                                    text="CREATE MY XILOGISM\n",
                                    style=TextStyle(
                                        size=18,
                                        color="black",
                                        weight=FontWeight.W_700
                                    )
                                ),
                                TextSpan(
                                    text="Pseudocode Format",
                                    style=TextStyle(
                                        size=12,
                                        color="black"
                                    )
                                )
                            ],
                            text_align=TextAlign.START,
                            expand=True
                        )
                    ]
                )
            ),
            style=ButtonStyle(
                bgcolor="#26191f51",
                shape=RoundedRectangleBorder(16),
                side=BorderSide(1, "#1a191f51")
            ),
            on_hover=self._hover
        )

        self.open_button = FilledButton(
            scale=transform.Scale(scale=1),
            animate_scale=animation.Animation(250, AnimationCurve.BOUNCE_OUT),
            content=Container(
                padding = padding.symmetric(8 * self.widget_scale, 16),
                content = Row(
                    controls = [
                        Image(
                            src="/icons_light/open.png",
                            width=16,
                            height=16
                        ),
                        Text(
                            value="OPEN EXISTING",
                            weight=FontWeight.W_600,
                            color="black",
                            text_align=TextAlign.START,
                            expand=True
                        )
                    ],
                )
            ),
            on_click = lambda event: setattr(self.active_sidebar_button_state, 'active', "Open Xilogism"),
            style=ButtonStyle(
                bgcolor="#26191f51",
                shape=RoundedRectangleBorder(16),
                side=BorderSide(1, "#1a191f51")
            ),
            on_hover=self._hover
        )

        self.content = Row(
            alignment=MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=CrossAxisAlignment.CENTER,
            expand=True,
            controls=[
                Container(
                    content = Image(
                        src="light_mode.gif",
                        width=(320 * self.widget_scale) * 1.10,
                        height=(320 * self.widget_scale) * 1.10,
                    ),
                    expand=True,
                ),
                Container(
                    expand = True,
                    content = Column(
                        expand=True,
                        alignment = MainAxisAlignment.CENTER,
                        horizontal_alignment = CrossAxisAlignment.CENTER,
                        spacing = 0,
                        controls = [
                            Text(
                                spans=[
                                    TextSpan(
                                        text="GET YOUR HANDS DIRTY WITH\n",
                                        style=TextStyle(
                                            size=16,
                                            weight=FontWeight.W_600,
                                            italic=True
                                        )
                                    ),
                                    TextSpan(
                                        text="XILOGISM",
                                        style=TextStyle(
                                            size=72,
                                            weight=FontWeight.W_800,
                                        )
                                    )
                                ],
                                text_align=TextAlign.CENTER,
                                no_wrap=True
                            ),
                            Text(
                                value="CODES TO CIRCUITS, XILOGIZED!",
                                size=20,
                                weight=FontWeight.W_700,
                                text_align=TextAlign.CENTER,
                            ),
                            Container(
                                padding = padding.all(16),
                                margin = margin.symmetric(8, 0),
                                width=480,
                                height=128,
                                content = self.new_button
                            ),
                            Container(
                                padding=padding.only(left=96, right=16),
                                width=480,
                                height=48,
                                content = self.open_button,
                            )
                        ]
                    )
                )
            ]
        )

        super().build()
    
    def scale_all(self, scale: float):
        if abs(scale - self.old_scale) > 0.05:
            self.widget_scale = scale
            self.build()
            self.update()

            self.old_scale = scale
    
    def _hover(self, event: ControlEvent):
        button: FilledButton = event.control

        button.scale = 1.10 if event.data == "true" else 1
        button.update()