from flet import *
from presentation.states.active_font_state import ActiveFontState
from presentation.states.accent_color_state import AccentColorState

class FontFaceChooserButton(DropdownM2):
    def __init__(self):
        super().__init__()

        self.ac_state = AccentColorState()

        self.ac_state.on_colors_updated = self.update_colors

        self.border_radius=8
        self.filled = True
        self.width=160
        self.border_width=1
        self.border_color="black"
        self.content_padding=padding.only(left=8,right=4)

        self.max_menu_height = 256
        self.text_size = 14

        self.select_icon=Container(
            content = Image(
                src="/icons_light/arrow_down.png",
                width=16,
                height=16
            ),
            padding = 4,
            bgcolor="#00191f51",
            on_hover=self._hover__
        )

        self.bgcolor={
            ControlState.DEFAULT: "#1a191f51",
            ControlState.DISABLED: "#1a191f51",
            ControlState.DRAGGED: "#1a191f51",
            ControlState.ERROR: "#1a191f51",
            ControlState.FOCUSED: "#1a191f51",
            ControlState.HOVERED: "#1a191f51",
            ControlState.PRESSED: "#1a191f51",
            ControlState.SELECTED: "#1a191f51"
        }

        self.fill_color={
            ControlState.DEFAULT: "#1a191f51",
            ControlState.DISABLED: "#1a191f51",
            ControlState.DRAGGED: "#1a191f51",
            ControlState.ERROR: "#1a191f51",
            ControlState.FOCUSED: "#1a191f51",
            ControlState.HOVERED: "#1a191f51",
            ControlState.PRESSED: "#1a191f51",
            ControlState.SELECTED: "#1a191f51"
        }

        self.af_state = ActiveFontState()
        self.on_change = lambda event: setattr(self.af_state, 'active_font', event.data)
    
    def _hover__(self, event: ControlEvent):
        button: Container = event.control
        button.bgcolor = "#4d191f51" if event.data == "true" else "#00191f51"
        button.shape = BoxShape.CIRCLE
        button.padding = 4
        button.update()

    def update_colors(self):
        colors = self.ac_state.color_values
        self.bgcolor = colors["accent_color_1"]
        self.border = border.all(1, colors["divider_color"])
    