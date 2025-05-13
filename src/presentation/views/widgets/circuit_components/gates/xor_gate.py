from flet import *
import flet.canvas as cv
import numpy as np
from scipy.interpolate import CubicSpline

from presentation.views.widgets.circuit_components.abstract_element import LogicElement
from presentation.states.dark_mode_state import DarkModeState, DarkModeScheme

class XORGate(LogicElement):
    FULL_SIDE_LENGTH = 50
    INPUT_ARM_WIDTH: int = 20
    OUTPUT_ARM_WIDTH: int = 20

    __CIRCLE_DIAMETER: int = 10

    __XOR_ADJUSTMENT: int = 5

    FULL_WIDTH: int = FULL_SIDE_LENGTH + __CIRCLE_DIAMETER + INPUT_ARM_WIDTH + OUTPUT_ARM_WIDTH + __XOR_ADJUSTMENT

    def __init__(self, start_x: int, start_y: int, input_count: int = 2, xnor: bool = False):
        super().__init__()

        self.dm_state = DarkModeState()
        self.dm_state.on_change = self.update_colors

        self.input_coord = []
        scale = 1

        if input_count > 4:
            scale = 1 + ((input_count - 4) * 0.25)
            self.FULL_SIDE_LENGTH *= scale
            self.__CIRCLE_DIAMETER *= scale
            self.__XOR_ADJUSTMENT *= scale
            self.FULL_WIDTH = self.FULL_SIDE_LENGTH + self.INPUT_ARM_WIDTH + self.OUTPUT_ARM_WIDTH + self.__XOR_ADJUSTMENT

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
                paint=Paint(
                    stroke_width=2,
                    style=PaintingStyle.STROKE,
                )
            )

            move = cv.Path.MoveTo(start_x + self.FULL_SIDE_LENGTH + self.__CIRCLE_DIAMETER, start_y + (self.FULL_SIDE_LENGTH / 2))
            symbol_elements.append(move)
            output_line = cv.Path.LineTo(start_x + self.FULL_SIDE_LENGTH + self.INPUT_ARM_WIDTH + self.__CIRCLE_DIAMETER, start_y + (self.FULL_SIDE_LENGTH / 2))

        symbol_elements.append(output_line)
        self.output_coord = (output_line.x, output_line.y)

        points_template = [
            (0 * scale, 50 * scale),    # (x, y)
            (12.5 * scale, 25 * scale),
            (9 * scale, 37.5 * scale),
            (9 * scale, 12.5 * scale)
        ]
        points = [(x * scale, y * scale) for x, y in points_template]
        sorted_points = sorted(points, key=lambda p: p[1])

        def interpolate_y(y, points):
            for i in range(len(points) - 1):
                x0, y0 = points[i]
                x1, y1 = points[i + 1]
                if y0 <= y <= y1 or y1 <= y <= y0:
                    if y1 != y0:
                        return x0 + (x1 - x0) * (y - y0) / (y1 - y0)
            return points[-1][0]

        y_points = self.get_spaced_points(self.FULL_SIDE_LENGTH, input_count)

        for point in y_points:
            x = interpolate_y(point, sorted_points)
            move = cv.Path.MoveTo(start_x + x - self.__XOR_ADJUSTMENT, start_y + point)
            input_line = cv.Path.LineTo(start_x - self.INPUT_ARM_WIDTH - self.__XOR_ADJUSTMENT, start_y + point)

            symbol_elements.append(move)
            symbol_elements.append(input_line)

            self.input_coord.append((input_line.x, input_line.y))

        self.shapes = [
            cv.Path(
                elements=symbol_elements,
                paint=Paint(
                    stroke_width=2,
                    style=PaintingStyle.STROKE,
                )
            ),
        ]

        if xnor:
            self.shapes.append(dot)
            self.FULL_WIDTH += self.__CIRCLE_DIAMETER
        
        self.rect = (start_x, start_y, self.FULL_WIDTH, self.FULL_SIDE_LENGTH)
        self.output_node_position = LogicElement.Position.RIGHT
    
    def get_spaced_points(self, total: float, divisions: int):
        step = total / (divisions + 1)
        return [round(step * i, 5) for i in range(1, divisions + 1)]
    
    def update_colors(self):
        dark_mode = self.dm_state.active == DarkModeScheme.DARK
        for shape in self.shapes:
            if type(shape) == cv.Text:
                shape.style = TextStyle(color = "white" if dark_mode else "black")
            else:
                shape.paint.color = "white" if dark_mode else "dark"