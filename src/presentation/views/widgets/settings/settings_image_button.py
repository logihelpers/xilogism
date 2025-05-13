from flet import *
from typing import Dict, List
from presentation.states.accent_color_state import AccentColorState

class SettingsImageButton(Container):
    _active: bool = False
    refs: Dict[str, List['SettingsImageButton']] = {}
    def __init__(self, image: str = None, text: str = None, group_id: str= None, image_scale: float = 1.0, on_button_press = None):
        super().__init__()

        self.ac_state = AccentColorState()

        self.group_id = group_id
        self.text = text
        self.check_box = Container(
            content = Text(""),
            width=16,
            height=16, 
            bgcolor="#00191f51", 
            border_radius=16, 
            border=border.all(2, "#73191f51")
        )

        self.label = Text(
            value = text,
            visible = (text != None)
        )

        self.content = Column(
            width = 280 * image_scale,
            controls = [
                Row(
                    controls = [
                        self.check_box,
                        Image(
                            src=image,
                            width=240 * image_scale,
                            height=135 * image_scale,
                            anti_alias=True
                        )
                    ]
                ),
                self.label
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER
        )

        self.padding=16
        self.bgcolor="#006b6b6b"
        self.border=border.all(1, "#006b6b6b")
        self.border_radius=16
        self.on_hover = self._hover
        self.on_click = lambda event: self.on_button_press(event)
        self.on_button_press = on_button_press

        try:
            SettingsImageButton.refs[self.group_id].append(self)
        except KeyError:
            self.active = True
            self.bgcolor = "#4d191f51"
            self.label.weight = FontWeight.BOLD
            self.check_box.bgcolor = "#af191f51"
            self.border = border.all(1, "#191f51")

            SettingsImageButton.refs[self.group_id] = [self]
    
    def _hover(self, event: ControlEvent):
        button: SettingsImageButton = event.control
        colors = self.ac_state.color_values
        
        iter_button: SettingsImageButton = None
        for iter_button in SettingsImageButton.refs[button.group_id]:
            if iter_button.text == button.text:
                if button.active:
                    continue
                else:
                    button.bgcolor = colors["button_bgcolor"].replace("4d", "05") if event.data == "true" else "#006b6b6b"
                    button.border = border.all(1, colors["button_bgcolor"].replace("4d", "")) if event.data == "true" else border.all(1, "#006b6b6b")
                    button.label.weight = FontWeight.BOLD if event.data == "true" else FontWeight.NORMAL
                button.update()
    
    def on_button_press(self, event: ControlEvent):
        pass

    @property
    def active(self) -> bool:
        return self._active
    
    @active.setter
    def active(self, value: bool):
        self._active = value