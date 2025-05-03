from flet import *

class LocalButton(Container):
    def __init__(self, title: str, path: str, date: str, on_press):
        super().__init__()
        self.title = title

        self.bgcolor = "#00191f51"
        self.border_radius = 16
        self.padding = 8

        self.title_text = TextSpan(
            text=title + "\n",
            style=TextStyle(
                size=12,
                weight=FontWeight.W_500,
                color=Colors.BLACK
            )
        )

        self.path_text = TextSpan(
            text=path + "\n",
            style=TextStyle(
                size=10,
                weight=FontWeight.W_500,
                color="#6b6b6b"
            )
        )

        self.date_text = TextSpan(
            text=f"Modified: {date}",
            style=TextStyle(
                size=10,
                weight=FontWeight.W_500,
                color="#6b6b6b"
            )
        )

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
                        self.title_text,
                        self.path_text,
                        self.date_text
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
        self.on_click = on_press
    
    def __hover(self, event: ControlEvent):
        event.control.bgcolor = "#4d191f51" if event.data == "true" else None
        event.control.update()