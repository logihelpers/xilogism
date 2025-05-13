from xilowidgets import Drawboard
from presentation.views.widgets.circuit_components.abstract_element import LogicElement
from presentation.states.dark_mode_state import DarkModeState, DarkModeScheme

class Canvas(Drawboard):
    def __init__(self, expand: bool = True):
        super().__init__(
            expand=expand
        )

        self.logic_elements = list()

        self.dm_state = DarkModeState()
        self.dm_state.on_change = self.update_color

    def add_to_canvas(self, *argv):
        logic_gate: LogicElement = None
        for logic_gate in argv:
            self.shapes.extend(logic_gate.shapes)
            self.logic_elements.append(logic_gate)
            self.update_color()
    
    def clear(self):
        self.shapes = []
        self.logic_elements.clear()
    
    def update_color(self):
        element: LogicElement = None
        for element in self.logic_elements:
            element.update_colors()
        self.update()