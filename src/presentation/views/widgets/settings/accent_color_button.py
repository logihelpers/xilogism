from flet import *
from typing import List

from presentation.states.accent_color_state import AccentColors

class AccentColorButton(Container):
    refs: List['AccentColorButton'] = []
    active: bool = False
    def __init__(self, color: AccentColors, on_button_press = None):
        super().__init__()
        self.color = color

        self.main_content = Container(
            content=Text("", size=24, text_align=TextAlign.CENTER, offset=Offset(x=0, y=0.10)),
            width=48,
            height=48,
            bgcolor=color.value,
            border_radius=24,
            border=border.all(0.5, "black")
        )

        self.name_text = Text(
            color.name.capitalize()
        )

        self.content = Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                self.main_content,
                self.name_text
            ]
        )

        self.on_hover = self._hover
        self.on_click = lambda event: self.on_button_press(event)
        self.on_button_press = on_button_press

        if len(AccentColorButton.refs) > 0:
            AccentColorButton.refs.append(self)
        else:
            self.active = True
            
            self.main_content.border=border.all(2, "black")
            self.main_content.content.value = "✓"
            self.name_text.weight = FontWeight.W_600

            AccentColorButton.refs.append(self)
    
    def _hover(self, event: ControlEvent):
        button: AccentColorButton = event.control
        
        iter_button: AccentColorButton = None
        for iter_button in AccentColorButton.refs:
            if iter_button.color == button.color:
                if button.active:
                    continue
                else:
                    button.main_content.border = border.all(1.5, Colors.BLACK) if event.data == "true" else border.all(0.5, Colors.BLACK)
                    button.main_content.content.value = "✓" if event.data == "true" else ""
                    button.main_content.content.color = "#6b6b6b" if event.data == "true" else "black"
                    button.main_content.content.update()

                    button.name_text.weight = FontWeight.W_600 if event.data == "true" else FontWeight.W_400
                    button.name_text.update()
                button.update()
    
    def on_button_press(self, event: ControlEvent):
        pass