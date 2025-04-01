from flet import *

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