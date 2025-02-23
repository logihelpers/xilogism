import flet as ft
import flet.canvas as cv

from .abstract_element import LogicElement

class InputNode(LogicElement):
    FULL_LENGTH: int = 50
    OUTPUT_ARM_WIDTH: int = 20

    __CIRCLE_DIAMETER: int = 30
    __INNER_CIRCLE_DIAMETER: int = 20
    FULL_WIDTH: int = FULL_LENGTH + __CIRCLE_DIAMETER

    def __init__(self, start_x: int, start_y: int):
        super().__init__()

        output_line = cv.Path.LineTo(start_x + (InputNode.__CIRCLE_DIAMETER / 2), start_y + InputNode.__CIRCLE_DIAMETER + InputNode.OUTPUT_ARM_WIDTH)

        self.shapes = [
            cv.Circle(
                start_x + (InputNode.__CIRCLE_DIAMETER / 2),
                start_y + (InputNode.__CIRCLE_DIAMETER / 2),
                InputNode.__CIRCLE_DIAMETER / 2,
                paint=ft.Paint(
                    stroke_width=2,
                    style=ft.PaintingStyle.STROKE,
                )
            ),
            cv.Circle(
                start_x + (InputNode.__CIRCLE_DIAMETER / 2),
                start_y + (InputNode.__CIRCLE_DIAMETER / 2),
                InputNode.__INNER_CIRCLE_DIAMETER / 2,
                paint=ft.Paint(
                    stroke_width=2,
                    style=ft.PaintingStyle.STROKE,
                )
            ),
            cv.Path(
                elements=[
                    cv.Path.MoveTo(start_x + (InputNode.__CIRCLE_DIAMETER / 2), start_y + InputNode.__CIRCLE_DIAMETER),
                    output_line,
                ],
                paint=ft.Paint(
                    stroke_width=2,
                    style=ft.PaintingStyle.STROKE,
                )
            ),
        ]

        self.output_coord = (output_line.x, output_line.y)
        
        self.output_node_position = LogicElement.Position.BOTTOM