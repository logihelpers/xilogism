from flet import *
from random_word import RandomWords

class RecentsButton(Container):
    def __init__(self):
        super().__init__()

        self.bgcolor = "#1a191f51"
        self.padding = 8
        self.border_radius = 16

        r = RandomWords()

        self.content = Row(
            spacing=0,
            controls=[
                Image(
                    src="/icons_light/Document.png",
                    width=36,
                    height=36,
                    fit=ImageFit.COVER
                ),
                Text(
                    expand=True,
                    spans=[
                        TextSpan(
                            text=f"{r.get_random_word()}.xlg\n",
                            style=TextStyle(
                                size=16,
                                weight=FontWeight.W_400,
                                color=Colors.BLACK
                            )
                        ),
                        TextSpan(
                            text="Modified: 2/2/25 8:54 PM",
                            style=TextStyle(
                                size=12,
                                weight=FontWeight.W_500,
                                color="#6b6b6b"
                            )
                        )
                    ]
                ),
                Image(
                    src="/icons_light/settings_more.png",
                    width=24,
                    height=24
                ),
            ]
        )
    
        self.on_hover = self.__hover
    
    def __hover(self, event: ControlEvent):
        event.control.bgcolor = "#4d191f51" if event.data == "true" else None
        event.control.update()