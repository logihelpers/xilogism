from flet import *
from presentation.views.widgets.existing_view import *

class OpenExistingView(Container):
    widget_scale: float = 1.0
    old_scale: float = 1.0
    def __init__(self):
        super().__init__()
        self.widget_scale = 1.0
        self.padding = padding.all(16 * self.widget_scale)
        self.expand = True
        self.content = Column(
            controls = [
                Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Text(
                            "Buon giorno, Amico!",
                            color="black",
                            weight=FontWeight.W_700,
                            italic=True,
                            size=28
                        ),
                        Container(
                            padding = padding.symmetric(4, 24),
                            border_radius=32,
                            bgcolor="#4d191f51",
                            border=border.all(1, "black"),
                            content=Row(
                                controls=[
                                    Image(
                                        src="/icons_light/search.png",
                                        width=24,
                                        height=24
                                    ),
                                    Text(
                                        "Search",
                                        color="black",
                                        weight=FontWeight.W_500,
                                        size=14,
                                        width=128
                                    )
                                ]
                            )
                        )
                    ]
                ),
                Text(
                    "Pinned Projects",
                    weight=FontWeight.W_500,
                    size=14
                ),
                Row( # Pinned row
                    controls=[
                        PinnedButton(),
                        PinnedButton(),
                        PinnedButton(),
                        PinnedButton(),
                        PinnedButton(),
                        PinnedButton()
                    ],
                    scroll=True,
                    spacing=16
                ),
                Container(
                    content = Text(
                        "Recent Projects",
                        weight=FontWeight.W_500,
                        size=14
                    ),
                    padding=padding.only(top=16)
                ),
                Divider(1, color="#6b6b6b"),
                Container(
                    padding=padding.only(top=8, right=8, bottom=0, left=8),
                    content = Column( # Recents Column
                        controls=[
                            RecentsButton(),
                            RecentsButton(),
                            RecentsButton(),
                            RecentsButton(),
                            RecentsButton(),
                            RecentsButton(),
                            RecentsButton()
                        ],
                        expand=True,
                        scroll=True
                    ),
                    expand=True
                )
            ]
        )
    
    def scale_all(self, scale: float):
        if abs(scale - self.old_scale) > 0.05:
            self.widget_scale = scale
            self.build()
            self.update()

            self.old_scale = scale