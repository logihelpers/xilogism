import flet as ft
import flet.canvas as cv

from .abstract_element import LogicElement

class Wire(LogicElement):
    def __init__(self, start_element: LogicElement, end_element: LogicElement, multiple_input_index: int = 0):
        super().__init__()

        x0, y0 = start_element.output_coord
        x1, y1 = end_element.input_coord[multiple_input_index]

        wire_elements = [
            cv.Path.MoveTo(x0, y0)
        ]
        
        if start_element.output_node_position == LogicElement.Position.BOTTOM:
            wire_elements.extend([
                cv.Path.LineTo(x1, y0),
                cv.Path.LineTo(x1, y1)
            ])
        elif start_element.output_node_position == LogicElement.Position.RIGHT:
            mid = (x1 - x0) / 2
            wire_elements.extend([
                cv.Path.LineTo(x0 + mid, y0),
                cv.Path.LineTo(x0 + mid, y1),
                cv.Path.LineTo(x1, y1)
            ])

        self.shapes = [
            cv.Path(
                elements=wire_elements,
                paint=ft.Paint(
                    stroke_width=2,
                    style=ft.PaintingStyle.STROKE,
                )
            )
        ]