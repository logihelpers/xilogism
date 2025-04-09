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
        self.content = Row(
            alignment=MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=CrossAxisAlignment.CENTER,
            expand=True,
            controls=[
                Container(
                    content = Image(
                        src="/icons_light/logo.png",
                        width=(320 * self.widget_scale) * 1.10,
                        height=(320 * self.widget_scale) * 1.10
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
                                            size=16 * self.widget_scale,
                                            weight=FontWeight.W_600,
                                            italic=True
                                        )
                                    ),
                                    TextSpan(
                                        text="XILOGISM",
                                        style=TextStyle(
                                            size=72 * self.widget_scale,
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
                                padding = padding.all(16 * self.widget_scale),
                                margin = margin.symmetric(8 * self.widget_scale, 0),
                                width=480 * self.widget_scale,
                                height=128 * self.widget_scale,
                                content = FilledButton(
                                    key = "New Xilogism",
                                    on_click = lambda event: setattr(self.active_sidebar_button_state, 'active', event.control.key),
                                    content=Container(
                                        padding = padding.all(16 * self.widget_scale),
                                        content = Row(
                                            controls=[
                                                Image(
                                                    src="/icons_light/new.png",
                                                    width=56 * self.widget_scale,
                                                    height=56 * self.widget_scale
                                                ),
                                                Text(
                                                    spans=[
                                                        TextSpan(
                                                            text="CREATE MY XILOGISM\n",
                                                            style=TextStyle(
                                                                size=18 * self.widget_scale,
                                                                color="black",
                                                                weight=FontWeight.W_700
                                                            )
                                                        ),
                                                        TextSpan(
                                                            text="Pseudocode Format",
                                                            style=TextStyle(
                                                                size=12 * self.widget_scale,
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
                                        shape=RoundedRectangleBorder(16 * self.widget_scale),
                                        side=BorderSide(1, "#1a191f51")
                                    )
                                )
                            ),
                            Container(
                                padding=padding.only(left=96 * self.widget_scale, right=16 * self.widget_scale),
                                width=480 * self.widget_scale,
                                height=48 * self.widget_scale,
                                content = FilledButton(
                                    key = "Open Xilogism",
                                    content=Container(
                                        padding = padding.symmetric(8 * self.widget_scale, 16 * self.widget_scale),
                                        content = Row(
                                            controls = [
                                                Image(
                                                    src="/icons_light/open.png",
                                                    width=16 * self.widget_scale,
                                                    height=16 * self.widget_scale
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
                                    on_click = lambda event: setattr(self.active_sidebar_button_state, 'active', event.control.key),
                                    style=ButtonStyle(
                                        bgcolor="#26191f51",
                                        shape=RoundedRectangleBorder(16 * self.widget_scale),
                                        side=BorderSide(1, "#1a191f51")
                                    )
                                ),
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