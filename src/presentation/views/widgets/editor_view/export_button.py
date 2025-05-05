from flet import *
from presentation.states.accent_color_state import AccentColorState

class ExportButton(Container):
    def __init__(self):
        super().__init__()

        self.ac_state = AccentColorState()

        self.ac_state.on_colors_updated = self.update_colors

        self.border=border.all(1, "black")
        self.border_radius=8
        self.bgcolor="#4d191f51"
        self.height=32
        self.padding=padding.symmetric(4, 8)
        self.content=Row(
            controls=[
                Text(
                    value="Export",
                    weight=FontWeight.BOLD
                ),
                Image(
                    src="/icons_light/export.png",
                    width=16,
                    height=16
                )
            ]
        )

        self.on_hover = self._hover__
    
    def _hover__(self, event: ControlEvent):
        button: Container = event.control
        button.bgcolor = "#73191f51" if event.data == "true" else "#4d191f51"
        button.update()

    def update_colors(self):
        colors = self.ac_state.color_values
        self.bgcolor = colors["accent_color_1"]
        self.color = colors["text_color"]