from xilowidgets import Drawboard
from presentation.views.widgets.circuit_components.abstract_element import LogicElement
from presentation.states.dark_mode_state import DarkModeState, DarkModeScheme

class Canvas(Drawboard):
    def __init__(self, expand: bool = True):
        super().__init__(
            expand=expand
        )

        self.dm_state = DarkModeState()
        self.dm_state.on_change = self.update_color

    def add_to_canvas(self, *argv):
        logic_gate: LogicElement = None
        for logic_gate in argv:
            self.shapes.extend(logic_gate.shapes)
    
    def clear(self):
        self.shapes = []
    
    def update_color(self):
        self.update()