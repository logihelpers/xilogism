from flet import *
from presentation.states.accent_color_state import AccentColorState

class UndoRedoButtons(Container):
    def __init__(self):
        super().__init__()

        self.ac_state = AccentColorState()

        self.ac_state.on_colors_updated = self.update_colors

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

    def update_colors(self):
        colors = self.ac_state.color_values
        self.bgcolor = colors["accent_color_1"]
        self.border = border.all(1, colors["divider_color"])

