from flet import *
from math import pi

from presentation.states.active_font_state import ActiveFontState
from presentation.states.accent_color_state import AccentColorState
from presentation.states.dark_mode_state import DarkModeState, DarkModeScheme

class FontSizeTextField(Container):
    def __init__(self):
        super().__init__()

        self.af_state = ActiveFontState()
        self.ac_state = AccentColorState()
        self.dm_state = DarkModeState()

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

        self.arrow_icon = Image(
            src="/icons_light/arrow_down.png",
            width=12,
            height=12,
        )

        self.arrow_up_icon = Image(
            src="/icons_light/arrow_down.png",
            width=12,
            height=12,
            rotate=Rotate(angle=pi)
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
                            content=self.arrow_up_icon,
                            on_click = lambda e: setattr(self.af_state, 'font_size', self.af_state.font_size + 1)
                        ),
                        Container(
                            key="SIZE_DECREASE",
                            expand=True,
                            width=24,
                            bgcolor = "#1a191f51",
                            on_hover=self._hover__,
                            content=self.arrow_icon,
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
    
    def did_mount(self):
        super().did_mount()
        self.ac_state.on_colors_updated = self.update_colors
    
    def update_colors(self):
        colors = self.ac_state.color_values
        dark_mode = self.dm_state.active == DarkModeScheme.DARK
        self.bgcolor = colors["options_bgcolor"]
        self.size_tf.cursor_color = colors["cursor_color"]
        self.content.controls[1].color = colors["border_color"]  # VerticalDivider
        self.content.controls[2].controls[0].bgcolor = colors["options_bgcolor"]  # SIZE_INCREASE # SIZE_INCREASE Image
        self.content.controls[2].controls[1].bgcolor = colors["options_bgcolor"]  # SIZE_DECREASE
        self.content.controls[2].controls[1].border = border.only(top=BorderSide(1, colors["border_color"]))  # SIZE_DECREASE
        def _hover__(event: ControlEvent):
            button: Container = event.control
            button.bgcolor = colors["hover_bgcolor"] if event.data == "true" else colors["options_bgcolor"]
            button.update()
        self.content.controls[2].controls[0].on_hover = _hover__  # SIZE_INCREASE
        self.content.controls[2].controls[1].on_hover = _hover__  # SIZE_DECREASE

        self.arrow_icon.src = "/icons_light/arrow_down.png" if not dark_mode else "/icons_dark/arrow_down.png"
        self.arrow_up_icon.src = "/icons_light/arrow_down.png" if not dark_mode else "/icons_dark/arrow_down.png"
        self.update()