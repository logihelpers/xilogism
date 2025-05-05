from flet import *
from math import pi

from presentation.states.active_font_state import ActiveFontState
from presentation.states.accent_color_state import AccentColorState

class FontSizeTextField(Container):
    def __init__(self):
        super().__init__()

        self.ac_state = AccentColorState()
        self.ac_state.on_colors_updated = self.update_colors

        self.af_state = ActiveFontState()

        self.border=border.all(1, "black")
        self.bgcolor="#1a191f51"
        self.border_radius=8

        self.size_tf = TextField(
            input_filter=NumbersOnlyInputFilter(),
            value=self.af_state.font_size,
            border=0,
            border_color="#00000000",
            width=36,
            content_padding=padding.only(left=8, right=8),
            cursor_color=Colors.BLACK,
            on_submit = lambda e: setattr(self.af_state, 'font_size', int(e.data))
        )

        self.content=Row(
            spacing=0,
            controls=[
                self.size_tf,
                VerticalDivider(1, color="black"),
                Column(
                    expand=True,
                    spacing = 0,
                    controls=[
                        Container(
                            key="SIZE_INCREASE",
                            expand=True,
                            width=24,
                            bgcolor = "#1a191f51",
                            on_hover=self._hover__,
                            content=Image(
                                src="/icons_light/arrow_down.png",
                                width=12,
                                height=12,
                                rotate=Rotate(angle=pi)
                            ),
                            on_click = lambda e: setattr(self.af_state, 'font_size', self.af_state.font_size + 1)
                        ),
                        Container(
                            key="SIZE_DECREASE",
                            expand=True,
                            width=24,
                            bgcolor = "#1a191f51",
                            on_hover=self._hover__,
                            content=Image(
                                src="/icons_light/arrow_down.png",
                                width=12,
                                height=12,
                            ),
                            border=border.only(top=BorderSide(1, "black")),
                            on_click = lambda e: setattr(self.af_state, 'font_size', self.af_state.font_size - 1)
                        )
                    ]
                )
            ]
        )
    
    def _hover__(self, event: ControlEvent):
        button: Container = event.control
        button.bgcolor = "#4d191f51" if event.data == "true" else "#1a191f51"
        button.update()

    def update_colors(self):
        colors = self.ac_state.color_values
        self.bgcolor = colors["accent_color_1"]
        self.border = border.all(1, colors["divider_color"])