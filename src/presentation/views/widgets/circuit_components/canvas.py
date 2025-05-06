from xilowidgets import Drawboard
from presentation.views.widgets.circuit_components.abstract_element import LogicElement

class Canvas(Drawboard):
    def __init__(self, expand: bool = True):
        super().__init__(
            expand=expand
        )

    def add_to_canvas(self, *argv):
        logic_gate: LogicElement = None
        for logic_gate in argv:
            self.shapes.extend(logic_gate.shapes)
    
    def clear(self):
        self.shapes = []