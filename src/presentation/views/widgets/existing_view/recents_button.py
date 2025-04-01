from flet import *

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