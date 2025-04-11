from flet import *
from enum import Enum

from presentation.states.settings_navigator_state import SettingsNavigatorState

class Position(Enum):
    START = 0
    MIDDLE = 1
    END = 2

class NavigatorButton(Container):
    ACTIVE_STYLE = {"bgcolor" : "#effafafa", "shadow_color" : "#191f51", "border_color" : "#191f51", "weight": FontWeight.W_600}
    INACTIVE_STYLE = {"bgcolor" : "#fafafa", "shadow_color" : "#6b6b6b", "border_color" : "#6b6b6b", "weight": FontWeight.W_400}
    refs: list = []
    def __init__(self, name: str, pos: Position):
        super().__init__()

        self.name = name
        self.pos = pos

        self.sn_state = SettingsNavigatorState()

        self.animate=animation.Animation(250, AnimationCurve.BOUNCE_OUT)
        self.content = Text(name, size=14)
        self.padding=4
        self.bgcolor="#fafafa"
        self.width=128
        self.alignment=alignment.center
        self.shadow=BoxShadow(0.1, 2, "#6b6b6b")

        match pos:
            case Position.START:
                self.border = border.all(1, "#6b6b6b")
                self.border_radius = border_radius.only(4, 0, 4, 0)
                self.content.weight = FontWeight.W_600
            case Position.MIDDLE:
                self.border= border.symmetric(vertical = BorderSide(1, "#6b6b6b"))
            case Position.END:
                self.border=border.all(1, "#6b6b6b")
                self.border_radius=border_radius.only(0, 4, 0, 4)
        
        self.on_click = self.switch
        
        NavigatorButton.refs.append(self)
    
    def apply_button_style(self, button: Container, style: dict, position: Position):
        button.bgcolor = style["bgcolor"]
        button.shadow = BoxShadow(0.1, 2, style["shadow_color"])
        button.content.weight = style["weight"]
        
        match position:
            case Position.START:
                button.border = border.all(1, style["border_color"])
                button.border_radius = border_radius.only(4, 0, 4, 0)
            case Position.MIDDLE:
                button.border = border.symmetric(vertical=BorderSide(1, style["border_color"]))
            case Position.END:
                button.border = border.all(1, style["border_color"])
                button.border_radius = border_radius.only(0, 4, 0, 4)

    def switch(self, event: ControlEvent):
        clicked_name = event.control.name
        
        for index, button in enumerate(NavigatorButton.refs):
            is_active = button.name == clicked_name
            style = NavigatorButton.ACTIVE_STYLE if is_active else NavigatorButton.INACTIVE_STYLE
            
            self.apply_button_style(button, style, button.pos)
            
            if is_active:
                self.sn_state.active = index
            
            button.update()