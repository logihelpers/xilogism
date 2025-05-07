from flet import *
from presentation.states.viewing_mode_state import ViewingMode, ViewingModeState
from presentation.states.language_state import LanguageState

class DiagramModeChooser(DropdownM2):
    def __init__(self):
        super().__init__()

        self.vm_state = ViewingModeState()
        self.lang_state = LanguageState()

        self.value="Logic Diagram"
        self.border_radius=8
        self.width=148
        self.border_width=1
        self.border_color="black"

        self.text_size = 14

        self.content_padding=padding.only(left=8,right=4)
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