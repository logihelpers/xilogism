from flet import *

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
                        OpenExistingView.PinnedButton(),
                        OpenExistingView.PinnedButton(),
                        OpenExistingView.PinnedButton(),
                        OpenExistingView.PinnedButton(),
                        OpenExistingView.PinnedButton(),
                        OpenExistingView.PinnedButton()
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
                            OpenExistingView.RecentsButton(),
                            OpenExistingView.RecentsButton(),
                            OpenExistingView.RecentsButton(),
                            OpenExistingView.RecentsButton(),
                            OpenExistingView.RecentsButton(),
                            OpenExistingView.RecentsButton(),
                            OpenExistingView.RecentsButton()
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
    
    class PinnedButton(Container):
        def __init__(self):
            super().__init__()

            self.bgcolor = "#00191f51"
            self.width = 144
            self.height = 200
            self.content = Column(
                spacing=0,
                controls=[
                    Container(
                        Stack(
                            controls=[
                                Image(
                                    src="/icons_light/white.jpg",
                                    width=144,
                                    height=180,
                                    border_radius=8
                                ),
                                Image(
                                    src="/icons_light/Heart.png",
                                    width=24,
                                    height=24,
                                    bottom=4,
                                    right=4
                                )
                            ]
                        ),
                        expand=True,
                        bgcolor="#f4f4f4",
                        border_radius=8,
                        border=border.all(1, Colors.BLACK)
                    ),
                    Row(
                        spacing=0,
                        controls = [
                            Image(
                                "/icons_light/Document.png",
                                width=24,
                                height=24
                            ),
                            Text(
                                spans=[
                                    TextSpan(
                                        text="My First Project\n",
                                        style=TextStyle(
                                            size=12,
                                            weight=FontWeight.W_500
                                        )
                                    ),
                                    TextSpan(
                                        text="Modified: 1/26/20 8:54 AM",
                                        style=TextStyle(
                                            size=8,
                                            weight=FontWeight.W_500,
                                            color="#6b6b6b"
                                        )
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        
            self.on_hover = self.__hover
        
        def __hover(self, event: ControlEvent):
            event.control.bgcolor = "#4d191f51" if event.data == "true" else None
            event.control.update()
    
    class RecentsButton(Container):
        def __init__(self):
            super().__init__()
            self.bgcolor = "#00191f51"

            self.content = Row(
                spacing=0,
                controls=[
                    Image(
                        src="/icons_light/Document.png",
                        width=40,
                        height=40,
                        fit=ImageFit.COVER
                    ),
                    Text(
                        expand=True,
                        spans=[
                            TextSpan(
                                text="Untitled Design\n",
                                style=TextStyle(
                                    size=12,
                                    weight=FontWeight.W_500,
                                    color=Colors.BLACK
                                )
                            ),
                            TextSpan(
                                text="C:\\Users\\Arlecchino\\Downloads\n",
                                style=TextStyle(
                                    size=10,
                                    weight=FontWeight.W_500,
                                    color="#6b6b6b"
                                )
                            ),
                            TextSpan(
                                text="Modified: 2/2/25 8:54 PM",
                                style=TextStyle(
                                    size=10,
                                    weight=FontWeight.W_500,
                                    color="#6b6b6b"
                                )
                            )
                        ]
                    ),
                    Image(
                        src="/icons_light/settings_more.png",
                        width=32,
                        height=32
                    ),
                ]
            )
        
            self.on_hover = self.__hover
        
        def __hover(self, event: ControlEvent):
            event.control.bgcolor = "#4d191f51" if event.data == "true" else None
            event.control.update()