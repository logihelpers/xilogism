import flet as ft
import flet.canvas as cv

from .abstract_gate import LogicElement

class LogicCanvas(cv.Canvas):
    def __init__(self):
        super().__init__()

    def add_to_canvas(self, logic_gate: LogicElement):
        self.shapes.extend(logic_gate.shapes)