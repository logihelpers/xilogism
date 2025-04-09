from flet import *
from typing import List

class AccentColorButton(Container):
    refs: List['AccentColorButton'] = []
    active: bool = False
    def __init__(self, color: str, on_switch = None):
        super().__init__()
        self.color = color

        self.content = Text("", text_align=TextAlign.CENTER, offset=transform.Offset(x=0, y=0.1))
        self.width=32
        self.height=32
        self.bgcolor=color
        self.border_radius=16
        self.border=border.all(0.5, "black")

        self.on_hover = self._hover

        if len(AccentColorButton.refs) > 0:
            AccentColorButton.refs.append(self)
        else:
            self.active = True
            
            self.border=border.all(2, "black")
            self.content.value = "A"

            AccentColorButton.refs.append(self)
    
    def _hover(self, event: ControlEvent):
        button: AccentColorButton = event.control
        
        iter_button: AccentColorButton = None
        for iter_button in AccentColorButton.refs:
            if iter_button.color == button.color:
                if button.active:
                    button.border = border.all(1.5, Colors.BLACK) if event.data == "true" else border.all(2, Colors.BLACK)
                else:
                    button.border = border.all(1.5, Colors.BLACK) if event.data == "true" else border.all(0.5, Colors.BLACK)
                button.update()