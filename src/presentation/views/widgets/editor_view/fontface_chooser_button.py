from flet import *
from presentation.states.active_font_state import ActiveFontState
from presentation.states.accent_color_state import AccentColorState
from presentation.states.dark_mode_state import *

from xilowidgets import XDropdown

class FontFaceChooserButton(XDropdown):
    def __init__(self):
        super().__init__()

        self.ac_state = AccentColorState()
        self.dm_state = DarkModeState()

        self.border_radius=8
        self.filled = True
        self.width=160
        self.border_width=1
        self.border_color="black"
        self.content_padding=padding.only(left=8,right=4)
        self.dense = True
        self.collapsed = True
        self.height = 32

        self.text_size = 14

        self.trailing_icon=Container(
            content = Image(
                src="/icons_light/arrow_down.png",
                width=16,
                height=16
            ),
            padding = 4,
            bgcolor="#00191f51",
            on_hover=self._hover__
        )

        self.af_state = ActiveFontState()
        self.on_change = lambda event: setattr(self.af_state, 'active_font', event.data)
    
    def _hover__(self, event: ControlEvent):
        colors = self.ac_state.color_values
        button: Container = event.control
        button.bgcolor = colors["button_bgcolor"] if event.data == "true" else "#00191f51"
        button.padding = 4
        button.shape = BoxShape.CIRCLE
        button.update()
    
    def did_mount(self):
        super().did_mount()
        self.ac_state.on_colors_updated = self.update_colors
    
    def update_colors(self):
        colors = self.ac_state.color_values
        dark_mode = self.dm_state.active == DarkModeScheme.DARK
        self.text_style = TextStyle(color=colors["text_color"])  # For dropdown options
        self.trailing_icon.content.src = "/icons_light/arrow_down.png" if not dark_mode else "/icons_dark/arrow_down.png"
        self.update()