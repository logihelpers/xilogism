import flet as ft
import flet.canvas as cv

from .abstract_element import LogicElement

class LogicCanvas(cv.Canvas):
    def __init__(self):
        super().__init__()

    def add_to_canvas(self, *argv):
        logic_gate: LogicElement = None
        for logic_gate in argv:
            self.shapes.extend(logic_gate.shapes)