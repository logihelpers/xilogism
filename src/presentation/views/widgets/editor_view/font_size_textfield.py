from flet import *
from math import pi

from presentation.states.active_font_state import ActiveFontState

class FontSizeTextField(Container):
    def __init__(self):
        super().__init__()

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