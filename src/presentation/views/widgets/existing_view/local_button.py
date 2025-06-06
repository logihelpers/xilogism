from flet import *
from presentation.states.accent_color_state import AccentColorState
from presentation.states.dark_mode_state import *

class LocalButton(Container):
    def __init__(self, title: str, path: str, date: str, on_press):
        super().__init__()
        self.title = title

        self.ac_state = AccentColorState()
        self.dm_state = DarkModeState()
        self.ac_state.on_colors_updated = self.update_colors

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

        self.docu_icon = Image(
            src="/icons_light/Document.png",
            width=40,
            height=40,
            fit=ImageFit.COVER
        )

        self.content = Row(
            spacing=8,
            controls=[
                self.docu_icon,
                Text(
                    expand=True,
                    spans=[
                        self.title_text,
                        self.path_text,
                        self.date_text
                    ]
                )
            ]
        )
    
        self.on_hover = self.__hover
        self.on_click = on_press
    
    def __hover(self, event: ControlEvent):
        colors = self.ac_state.color_values
        if "4d" in colors["button_bgcolor"]:
            event.control.bgcolor = colors["button_bgcolor"].replace("4d", "73") if event.data == "true" else None
        else:
            event.control.bgcolor = colors["button_bgcolor"].replace("#", "#73") if event.data == "true" else None
        event.control.update()
    
    def update_colors(self):
        colors = self.ac_state.color_values
        dark_mode = self.dm_state.active == DarkModeScheme.DARK
        self.title_text.style.color = colors["text_color"]
        self.path_text.style.color = colors["text_color"]
        self.date_text.style.color = colors["text_color"]
        self.docu_icon.src = "/icons_light/Document.png" if not dark_mode else "/icons_dark/Document.png"
        self.update()
    
    def did_mount(self):
        super().did_mount()
        self.update_colors()