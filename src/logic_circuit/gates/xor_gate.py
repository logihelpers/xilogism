import flet as ft
import flet.canvas as cv
import numpy as np
from scipy.interpolate import CubicSpline

from ..abstract_gate import LogicElement

class XORGate(LogicElement):
    input_coord: list = []
    output_coord: tuple = None

    FULL_SIDE_LENGTH = 50
    INPUT_ARM_WIDTH: int = 20
    OUTPUT_ARM_WIDTH: int = 20

    __CIRCLE_DIAMETER: int = 10

    __XOR_ADJUSTMENT: int = 5

    def __init__(self, start_x: int, start_y: int, input_count: int = 2, xnor: bool = False):
        super().__init__()

        scale = 1

        if input_count > 4:
            scale = 1 + ((input_count - 4) * 0.2)
            self.FULL_SIDE_LENGTH *= scale
            self.__CIRCLE_DIAMETER *= scale

        symbol_elements = [
            cv.Path.MoveTo(start_x, start_y),
            cv.Path.QuadraticTo(start_x + (self.FULL_SIDE_LENGTH / 2), start_y, start_x + self.FULL_SIDE_LENGTH, start_y + (self.FULL_SIDE_LENGTH / 2), 1.5),
            cv.Path.MoveTo(start_x + self.FULL_SIDE_LENGTH, start_y + (self.FULL_SIDE_LENGTH / 2)),
            cv.Path.QuadraticTo(start_x + (self.FULL_SIDE_LENGTH / 2), start_y + self.FULL_SIDE_LENGTH, start_x, start_y + self.FULL_SIDE_LENGTH, 1.5),
            cv.Path.MoveTo(start_x, start_y + self.FULL_SIDE_LENGTH),
            cv.Path.QuadraticTo(start_x + (self.FULL_SIDE_LENGTH / 2), start_y + (self.FULL_SIDE_LENGTH / 2), start_x, start_y),
            cv.Path.MoveTo(start_x - self.__XOR_ADJUSTMENT, start_y + self.FULL_SIDE_LENGTH),
            cv.Path.QuadraticTo(start_x + (self.FULL_SIDE_LENGTH / 2) - self.__XOR_ADJUSTMENT, start_y + (self.FULL_SIDE_LENGTH / 2), start_x - self.__XOR_ADJUSTMENT, start_y),
            cv.Path.MoveTo(start_x + self.FULL_SIDE_LENGTH, start_y + (self.FULL_SIDE_LENGTH / 2))
        ]

        dot = None

        output_line = cv.Path.LineTo(start_x + self.FULL_SIDE_LENGTH + self.INPUT_ARM_WIDTH, start_y + (self.FULL_SIDE_LENGTH / 2))

        if xnor:
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

        y_values = np.array([50, 25, 37.5, 12.5]) * scale
        x_values = np.array([0, 12.5, 9, 9]) * scale

        sorted_indices = np.argsort(y_values)
        y_sorted = y_values[sorted_indices]
        x_sorted = x_values[sorted_indices]

        spline = CubicSpline(y_sorted, x_sorted)

        for point in points:
            x = spline(point)
            move = cv.Path.MoveTo(start_x + x - self.__XOR_ADJUSTMENT, start_y + point)
            input_line = cv.Path.LineTo(start_x - self.INPUT_ARM_WIDTH - self.__XOR_ADJUSTMENT, start_y + point)

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

        if xnor:
            self.shapes.append(dot)
    
    def get_spaced_points(self, total: float, divisions: int):
        step = total / (divisions + 1)
        return [round(step * i, 5) for i in range(1, divisions + 1)]