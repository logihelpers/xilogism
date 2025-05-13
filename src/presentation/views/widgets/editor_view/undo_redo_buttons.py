from flet import *
from presentation.states.accent_color_state import AccentColorState
from presentation.states.dark_mode_state import *

class UndoRedoButtons(Container):
    def __init__(self):
        super().__init__()

        self.ac_state = AccentColorState()
        self.dm_state = DarkModeState()

        self.border=border.all(1, "black")
        self.bgcolor="#1a191f51"
        self.border_radius=8
        self.content=Row(
            spacing=0,
            controls=[
                Container(
                    width = 32,
                    height = 32,
                    padding = 4,
                    on_hover = self._hover__, 
                    content=Image(
                        src="/icons_light/undo.png",
                        width=16,
                        height=16
                    )
                ),
                VerticalDivider(1, color="black"),
                Container(
                    width = 32,
                    height = 32,
                    padding = 4,
                    on_hover = self._hover__,
                    content=Image(
                        src="/icons_light/redo.png",
                        width=16,
                        height=16
                    )
                ),
            ]
        )
    
    def _hover__(self, event: ControlEvent):
        button: Container = event.control
        button.bgcolor = "#4d191f51" if event.data == "true" else "#00191f51"
        button.update()
    
    def did_mount(self):
        super().did_mount()
        self.ac_state.on_colors_updated = self.update_colors
    
    def update_colors(self):
        colors = self.ac_state.color_values
        dark_mode = self.dm_state.active == DarkModeScheme.DARK
        self.border = border.all(1, colors["text_color"])
        self.bgcolor = colors["button_bgcolor"].replace("4d", "0f") if "4d" in colors["button_bgcolor"] else colors["button_bgcolor"].replace("#", "#73")
        # self.content.controls[0].bgcolor = colors["options_bgcolor"]  # Undo Container
        self.content.controls[0].content.src = "/icons_light/undo.png" if not dark_mode else "/icons_dark/undo.png"  # Undo Image
        self.content.controls[1].color = colors["text_color"]  # VerticalDivider
        # self.content.controls[2].bgcolor = colors["options_bgcolor"]  # Redo Container
        self.content.controls[2].content.src = "/icons_light/redo.png" if not dark_mode else "/icons_dark/redo.png"
        # def _hover__(event: ControlEvent):
        #     button: Container = event.control
        #     button.bgcolor = colors["sidebar_color_deeper"] if event.data == "true" else colors["options_bgcolor"]
        #     button.update()
        # self.content.controls[0].on_hover = _hover__  # Undo Container
        # self.content.controls[2].on_hover = _hover__  # Redo Container
        self.update()