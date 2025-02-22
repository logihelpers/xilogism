import flet as ft
import flet.canvas as cv

from .abstract_gate import LogicElement

class OutputNode(LogicElement):
    input_coord: tuple = None

    FULL_LENGTH: int = 50
    OUTPUT_ARM_WIDTH: int = 20

    __CIRCLE_DIAMETER: int = 30
    __INNER_CIRCLE_DIAMETER: int = 20
    FULL_WIDTH: int = FULL_LENGTH + __CIRCLE_DIAMETER

    def __init__(self, start_x: int, start_y: int):
        super().__init__()

        input_line = cv.Path.LineTo(start_x - OutputNode.OUTPUT_ARM_WIDTH, start_y + (OutputNode.__CIRCLE_DIAMETER / 2))

        self.shapes = [
            cv.Circle(
                start_x + (OutputNode.__CIRCLE_DIAMETER / 2),
                start_y + (OutputNode.__CIRCLE_DIAMETER / 2),
                OutputNode.__CIRCLE_DIAMETER / 2,
                paint=ft.Paint(
                    stroke_width=2,
                    style=ft.PaintingStyle.STROKE,
                )
            ),
            cv.Circle(
                start_x + (OutputNode.__CIRCLE_DIAMETER / 2),
                start_y + (OutputNode.__CIRCLE_DIAMETER / 2),
                OutputNode.__INNER_CIRCLE_DIAMETER / 2,
                paint=ft.Paint(
                    stroke_width=2,
                    style=ft.PaintingStyle.STROKE,
                )
            ),
            cv.Path(
                elements=[
                    cv.Path.MoveTo(start_x, start_y + (OutputNode.__CIRCLE_DIAMETER / 2)),
                    input_line
                ],
                paint=ft.Paint(
                    stroke_width=2,
                    style=ft.PaintingStyle.STROKE,
                )
            ),
        ]

        self.input_coord = (input_line.x, input_line.y)