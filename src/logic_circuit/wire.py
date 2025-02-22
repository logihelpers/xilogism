import flet as ft
import flet.canvas as cv

from .abstract_gate import LogicElement

class Wire(LogicElement):
    def __init__(self, start_coord: tuple, end_coord: tuple):
        super().__init__()

        x0, y0 = start_coord
        x1, y1 = end_coord

        self.shapes = [
            cv.Path(
                elements=[
                    cv.Path.MoveTo(x0, y0),
                    cv.Path.LineTo(x1, y0),
                    cv.Path.LineTo(x1, y1)
                ],
                paint=ft.Paint(
                    stroke_width=2,
                    style=ft.PaintingStyle.STROKE,
                )
            )
        ]