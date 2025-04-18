from flet import *
from presentation.states.dialogs_state import DialogState, Dialogs

class ExportButton(Container):
    def __init__(self):
        super().__init__()

        self.dia_state = DialogState()

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
        self.on_click = lambda e: setattr(self.dia_state, 'state', Dialogs.EXPORT)
    
    def _hover__(self, event: ControlEvent):
        button: Container = event.control
        button.bgcolor = "#73191f51" if event.data == "true" else "#4d191f51"
        button.update()