import flet as ft
import flet.canvas as cv
import math

from ..abstract_gate import LogicElement

class ANDGate(LogicElement):
    input_coord: list = []
    output_coord: tuple = None

    FULL_SIDE_LENGTH = 50
    INPUT_ARM_WIDTH: int = 20
    OUTPUT_ARM_WIDTH: int = 20

    __CIRCLE_DIAMETER: int = 10

    def __init__(self, start_x: int, start_y: int, input_count: int = 2, nand: bool = False):
        super().__init__()

        scale = 1

        if input_count > 4:
            scale = 1 + ((input_count - 4) * 0.2)
            self.FULL_SIDE_LENGTH *= scale
            self.__CIRCLE_DIAMETER *= scale
        
        symbol_elements = [
            cv.Path.MoveTo(start_x, start_y),
            cv.Path.LineTo(start_x + (self.FULL_SIDE_LENGTH / 2), start_y),
            cv.Path.ArcTo(start_x + (self.FULL_SIDE_LENGTH / 2), start_y + self.FULL_SIDE_LENGTH, (self.FULL_SIDE_LENGTH / 2), math.pi / 2),
            cv.Path.LineTo(start_x, start_y + self.FULL_SIDE_LENGTH),
            cv.Path.LineTo(start_x, start_y),
            cv.Path.MoveTo(start_x + self.FULL_SIDE_LENGTH, start_y + (self.FULL_SIDE_LENGTH / 2)),
        ]

        dot = None

        output_line = cv.Path.LineTo(start_x + self.FULL_SIDE_LENGTH + self.INPUT_ARM_WIDTH, start_y + (self.FULL_SIDE_LENGTH / 2))

        if nand:
            dot = cv.Circle(
                start_x + self.FULL_SIDE_LENGTH + (self.__CIRCLE_DIAMETER / 2),
                start_y + (self.FULL_SIDE_LENGTH) / 2,
                (self.__CIRCLE_DIAMETER / 2),
                paint=ft.Paint(
                    stroke_width=2,
                    style=ft.PaintingStyle.STROKE,
                )
            )

            move = cv.Path.MoveTo(start_x + self.FULL_SIDE_LENGTH + self.__CIRCLE_DIAMETER, start_y + (self.FULL_SIDE_LENGTH / 2))
            symbol_elements.append(move)
            output_line = cv.Path.LineTo(start_x + self.FULL_SIDE_LENGTH + self.INPUT_ARM_WIDTH + self.__CIRCLE_DIAMETER, start_y + (self.FULL_SIDE_LENGTH / 2))

        symbol_elements.append(output_line)
        self.output_coord = (output_line.x, output_line.y)

        points = self.get_spaced_points(self.FULL_SIDE_LENGTH, input_count)

        for point in points:
            move = cv.Path.MoveTo(start_x, start_y + point)
            input_line = cv.Path.LineTo(start_x - self.INPUT_ARM_WIDTH, start_y + point)

            symbol_elements.append(move)
            symbol_elements.append(input_line)

            self.input_coord.append((input_line.x, input_line.y))

        self.shapes = [
            cv.Path(
                elements=symbol_elements,
                paint=ft.Paint(
                    stroke_width=2,
                    style=ft.PaintingStyle.STROKE,
                )
            ),
        ]

        if nand:
            self.shapes.append(dot)
    
    def get_spaced_points(self, total: float, divisions: int):
        step = total / (divisions + 1)
        return [round(step * i, 5) for i in range(1, divisions + 1)]