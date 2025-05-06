from xilowidgets import Drawboard
from presentation.views.widgets.circuit_components.abstract_element import LogicElement

class ElectricCanvas(Drawboard):
    def __init__(self, expand: bool = True):
        super().__init__(
            expand=expand
        )

    def add_to_canvas(self, *argv):
        integrated_circuit: LogicElement = None
        for integrated_circuit in argv:
            self.shapes.extend(integrated_circuit.shapes)
    
    def clear(self):
        self.shapes = []