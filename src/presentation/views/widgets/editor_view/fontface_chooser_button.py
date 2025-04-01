from flet import *

class FontFaceChooserButton(DropdownM2):
    def __init__(self):
        super().__init__()

        self.border_radius=8
        self.filled = True
        self.width=160
        self.border_width=1
        self.border_color="black"
        self.content_padding=padding.only(left=8,right=8)

        self.select_icon=Container(
            content = Image(
                src="/icons_light/arrow_down.png",
                width=16,
                height=16
            )
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