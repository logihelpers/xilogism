import flet as ft
import xilocanvas as xv

from .abstract_element import LogicElement

class LogicCanvas(xv.Xilocanvas):
    def __init__(self):
        super().__init__()

    def add_to_canvas(self, *argv):
        logic_gate: LogicElement = None
        for logic_gate in argv:
            self.shapes.extend(logic_gate.shapes)