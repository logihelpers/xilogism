from flet import *

class UndoRedoButtons(Container):
    def __init__(self):
        super().__init__()

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
                    content=Image(
                        src="/icons_light/redo.png",
                        width=16,
                        height=16
                    )
                ),
            ]
        )