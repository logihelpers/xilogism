import flet as ft
import flet.canvas as cv

class NOTGate(cv.Canvas):
    input_coord: tuple = None
    output_coord: tuple = None

    FULL_HEIGHT: int = 50
    INPUT_ARM_WIDTH: int = 20
    OUTPUT_ARM_WIDTH: int = 20

    __TRIANGLE_WIDTH: int = 50
    __CIRCLE_DIAMETER: int = 10
    FULL_WIDTH: int = __TRIANGLE_WIDTH + __CIRCLE_DIAMETER

    def __init__(self, start_x: int, start_y: int):
        super().__init__()

        self.shapes = [
            cv.Path(
                [
                    cv.Path.MoveTo(start_x, start_y),
                    cv.Path.LineTo(start_x  + (NOTGate.__TRIANGLE_WIDTH / 2), start_y + (NOTGate.FULL_HEIGHT / 2)),
                    cv.Path.LineTo(start_x, start_y + NOTGate.FULL_HEIGHT),
                    cv.Path.LineTo(start_x, start_y),
                    cv.Path.MoveTo(start_x, start_y + (NOTGate.FULL_HEIGHT / 2)),
                    cv.Path.LineTo(start_x - NOTGate.INPUT_ARM_WIDTH, start_y + (NOTGate.FULL_HEIGHT / 2)),
                    cv.Path.MoveTo(start_x + (NOTGate.__TRIANGLE_WIDTH / 2) + NOTGate.__CIRCLE_DIAMETER, start_y + (NOTGate.FULL_HEIGHT / 2)),
                    cv.Path.LineTo(start_x + (NOTGate.__CIRCLE_DIAMETER / 2) + NOTGate.__TRIANGLE_WIDTH, start_y + (NOTGate.FULL_HEIGHT / 2))
                ],
                paint=ft.Paint(
                    stroke_width=2,
                    style=ft.PaintingStyle.STROKE,
                )
            ),
            cv.Circle(
                start_x + (NOTGate.__TRIANGLE_WIDTH / 2) + (NOTGate.__CIRCLE_DIAMETER / 2),
                start_y + (NOTGate.FULL_HEIGHT / 2),
                NOTGate.__CIRCLE_DIAMETER / 2,
                paint=ft.Paint(
                    stroke_width=2,
                    style=ft.PaintingStyle.STROKE,
                )
            )
        ]

        self.input_coord = (start_x - 20, start_y + 25)
        self.output_coord = (start_x + 55, start_y + 25)