import flet as ft

class OpenExistingView(ft.Container):
    widget_scale: float = 1.0
    old_scale: float = 1.0
    def __init__(self):
        super().__init__()
        self.widget_scale = 1.0
    
    def build(self):
        self.padding = ft.padding.all(16 * self.widget_scale)
        self.expand = True
        self.content = ft.Column(
            controls = [
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            "Buon giorno, Amico!",
                            color="black",
                            weight=ft.FontWeight.W_700,
                            italic=True,
                            size=28
                        ),
                        ft.Container(
                            padding = ft.padding.symmetric(4, 24),
                            border_radius=32,
                            bgcolor="#4d51431C",
                            border=ft.border.all(1, "black"),
                            content=ft.Row(
                                controls=[
                                    ft.Image(
                                        src="/icons_light/search.png",
                                        width=24,
                                        height=24
                                    ),
                                    ft.Text(
                                        "Search",
                                        color="black",
                                        weight=ft.FontWeight.W_500,
                                        size=14,
                                        width=128
                                    )
                                ]
                            )
                        )
                    ]
                ),
                ft.Text(
                    "Pinned Projects",
                    weight=ft.FontWeight.W_500,
                    size=14
                ),
                ft.Row( # Pinned row
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
                ft.Container(
                    content = ft.Text(
                        "Recent Projects",
                        weight=ft.FontWeight.W_500,
                        size=14
                    ),
                    padding=ft.padding.only(top=16)
                ),
                ft.Divider(1, color="#6b6b6b"),
                ft.Container(
                    padding=ft.padding.only(top=8, right=8, bottom=0, left=8),
                    content = ft.Column( # Recents Column
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

        super().build()
    
    def scale_all(self, scale: float):
        if abs(scale - self.old_scale) > 0.05:
            self.widget_scale = scale
            self.build()
            self.update()

            self.old_scale = scale
    
    class PinnedButton(ft.Container):
        def __init__(self):
            super().__init__()

            self.bgcolor = "#0051431C"
            self.width = 144
            self.height = 200
            self.content = ft.Column(
                spacing=0,
                controls=[
                    ft.Container(
                        ft.Stack(
                            controls=[
                                ft.Image(
                                    src="/icons_light/white.jpg",
                                    width=144,
                                    height=180,
                                    border_radius=8
                                ),
                                ft.Image(
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
                        border=ft.border.all(1, ft.Colors.BLACK)
                    ),
                    ft.Row(
                        spacing=0,
                        controls = [
                            ft.Image(
                                "/icons_light/Document.png",
                                width=24,
                                height=24
                            ),
                            ft.Text(
                                spans=[
                                    ft.TextSpan(
                                        text="My First Project\n",
                                        style=ft.TextStyle(
                                            size=12,
                                            weight=ft.FontWeight.W_500
                                        )
                                    ),
                                    ft.TextSpan(
                                        text="Modified: 1/26/20 8:54 AM",
                                        style=ft.TextStyle(
                                            size=8,
                                            weight=ft.FontWeight.W_500,
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
        
        def __hover(self, event: ft.ControlEvent):
            event.control.bgcolor = "#4d51431C" if event.data == "true" else None
            event.control.update()
    
    class RecentsButton(ft.Container):
        def __init__(self):
            super().__init__()
            self.bgcolor = "#0051431C"

            self.content = ft.Row(
                spacing=0,
                controls=[
                    ft.Image(
                        src="/icons_light/Document.png",
                        width=40,
                        height=40,
                        fit=ft.ImageFit.COVER
                    ),
                    ft.Text(
                        expand=True,
                        spans=[
                            ft.TextSpan(
                                text="Untitled Design\n",
                                style=ft.TextStyle(
                                    size=12,
                                    weight=ft.FontWeight.W_500,
                                    color=ft.Colors.BLACK
                                )
                            ),
                            ft.TextSpan(
                                text="C:\\Users\\Arlecchino\\Downloads\n",
                                style=ft.TextStyle(
                                    size=10,
                                    weight=ft.FontWeight.W_500,
                                    color="#6b6b6b"
                                )
                            ),
                            ft.TextSpan(
                                text="Modified: 2/2/25 8:54 PM",
                                style=ft.TextStyle(
                                    size=10,
                                    weight=ft.FontWeight.W_500,
                                    color="#6b6b6b"
                                )
                            )
                        ]
                    ),
                    ft.Image(
                        src="/icons_light/settings_more.png",
                        width=32,
                        height=32
                    ),
                ]
            )
        
            self.on_hover = self.__hover
        
        def __hover(self, event: ft.ControlEvent):
            event.control.bgcolor = "#4d51431C" if event.data == "true" else None
            event.control.update()