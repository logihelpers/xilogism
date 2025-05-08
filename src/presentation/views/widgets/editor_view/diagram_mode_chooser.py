from flet import *
from presentation.states.viewing_mode_state import ViewingMode, ViewingModeState
from presentation.states.language_state import LanguageState
from presentation.states.accent_color_state import AccentColorState
from presentation.states.dark_mode_state import *

class DiagramModeChooser(DropdownM2):
    def __init__(self):
        super().__init__()

        self.vm_state = ViewingModeState()
        self.lang_state = LanguageState()
        self.ac_state = AccentColorState()
        self.dm_state = DarkModeState()

        self.value="Logic Diagram"
        self.border_radius=8
        self.width=148
        self.border_width=1
        self.border_color="black"

        self.text_size = 14

        self.arrow_icon = Image(
            src="/icons_light/arrow_down.png",
            width=16,
            height=16
        )

        self.content_padding=padding.only(left=8,right=4)
        self.select_icon=Container(
            content = self.arrow_icon,
            padding = 4,
            bgcolor="#00191f51",
            on_hover=self._hover__
        )

        self.filled=True
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

        self.options=[
            DropdownOption(
                key=mode.value,
                content=Text(mode.value)
            ) for mode in ViewingMode
        ]

        self.on_change = self.change_state
    
    def _hover__(self, event: ControlEvent):
        button: Container = event.control
        button.bgcolor = "#4d191f51" if event.data == "true" else "#00191f51"
        button.shape = BoxShape.CIRCLE
        button.padding = 4
        button.update()
    
    def change_state(self, event: ControlEvent):
        self.vm_state.state = ViewingMode(event.data)
    
    def did_mount(self):
        super().did_mount()
        self.ac_state.on_colors_updated = self.update_colors
        
    def update_colors(self):
        colors = self.ac_state.color_values
        dark_mode = self.dm_state.active == DarkModeScheme.DARK
        self.border_color = colors["text_color"]
        self.arrow_icon.src = "/icons_light/arrow_down.png" if not dark_mode else "/icons_dark/arrow_down.png"
        self.update()