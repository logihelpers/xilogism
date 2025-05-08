from flet import *
from presentation.states.dark_mode_state import DarkModeState, DarkModeScheme
from presentation.states.accent_color_state import AccentColorState

class PinnedButton(Container):
    def __init__(self, thumbnail: str, title: str, date: str, on_press):
        super().__init__()
        self.title = title

        self.ac_state = AccentColorState()
        self.dm_state = DarkModeState()
        self.ac_state.on_colors_updated = self.update_colors

        self.bgcolor = "#00191f51"
        self.width = 144
        self.height = 200
        self.padding = padding.symmetric(12, 8)
        self.animate_scale=animation.Animation(250, AnimationCurve.BOUNCE_OUT)

        self.thumbnail_image = Image(
            src_base64=f"{thumbnail}",
            width=144,
            height=180,
            border_radius=8
        )

        self.project_name = TextSpan(
            text=f"{title}\n",
            style=TextStyle(
                size=12,
                weight=FontWeight.W_500
            )
        )

        self.date = TextSpan(
            text=f"Modified: {date}",
            style=TextStyle(
                size=8,
                weight=FontWeight.W_500,
                color="#6b6b6b"
            )
        )

        self.docu_icon = Image(
            "/icons_light/Document.png",
            width=24,
            height=24
        )

        self.content = Column(
            spacing=0,
            controls=[
                Container(
                    Stack(
                        controls=[
                            self.thumbnail_image,
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
                        self.docu_icon,
                        Text(
                            spans=[
                                self.project_name,
                                self.date
                            ]
                        )
                    ]
                )
            ]
        )
    
        self.on_hover = self.__hover
        self.on_click = on_press
    
    def __hover(self, event: ControlEvent):
        event.control.scale = 1.05 if event.data == "true" else 1
        event.control.update()
    
    def update_colors(self):
        dark_mode = self.dm_state.active == DarkModeScheme.DARK
        self.docu_icon.src = "/icons_light/Document.png" if not dark_mode else "/icons_dark/Document.png"
        self.update()