from flet import *
import flet.canvas as cv

from presentation.views.widgets.circuit_components.abstract_element import LogicElement
from presentation.states.dark_mode_state import DarkModeState, DarkModeScheme

class XOR74x6(LogicElement):
    FULL_SIDE_LENGTH = 140
    FULL_SIDE_WIDTH = 80
    INPUT_ARM_WIDTH: int = 20
    OUTPUT_ARM_WIDTH: int = 20

    FULL_WIDTH: int = FULL_SIDE_WIDTH + INPUT_ARM_WIDTH

    def __init__(self, start_x: int, start_y: int, xnor: bool = False):
        super().__init__()

        self.dm_state = DarkModeState()
        self.dm_state.on_change = self.update_color

        self.input_coord: list = []
        self.output_coord: list = []

        label = "7486 IC"
        if xnor:
            label = "747266 IC"
        
        symbol_elements = [
            cv.Path.MoveTo(start_x, start_y),
            cv.Path.LineTo(start_x, start_y + self.FULL_SIDE_LENGTH),
            cv.Path.LineTo(start_x + self.FULL_SIDE_WIDTH, start_y + self.FULL_SIDE_LENGTH),
            cv.Path.LineTo(start_x + self.FULL_SIDE_WIDTH, start_y),
            cv.Path.LineTo(start_x, start_y),
            cv.Path.MoveTo(start_x + (self.FULL_SIDE_WIDTH / 2), start_y),
            cv.Path.LineTo(start_x + (self.FULL_SIDE_WIDTH / 2), start_y - 20),
            cv.Path.MoveTo(start_x + (self.FULL_SIDE_WIDTH / 4), start_y - 20),
            cv.Path.LineTo(start_x + ((self.FULL_SIDE_WIDTH * 3) / 4), start_y - 20),
            cv.Path.MoveTo(start_x + (self.FULL_SIDE_WIDTH / 2), start_y + self.FULL_SIDE_LENGTH),
            cv.Path.LineTo(start_x + (self.FULL_SIDE_WIDTH / 2), start_y + 20 + self.FULL_SIDE_LENGTH),
            cv.Path.MoveTo(start_x + (self.FULL_SIDE_WIDTH / 4), start_y + 20 + self.FULL_SIDE_LENGTH),
            cv.Path.LineTo(start_x + ((self.FULL_SIDE_WIDTH * 3) / 4), start_y + 20 + self.FULL_SIDE_LENGTH),
        ]

        for x in range(1, 13):
            coord = (start_x, start_y + (x * 11))
            symbol_elements.append(cv.Path.MoveTo(coord[0], coord[1]))
            symbol_elements.append(cv.Path.LineTo(coord[0] - self.INPUT_ARM_WIDTH, coord[1]))
            coord = (coord[0] - self.INPUT_ARM_WIDTH, coord[1])
            self.input_coord.append(coord)
        
        for x in range(1, 5):
            coord = (start_x + self.FULL_SIDE_WIDTH, start_y + (x * 28))
            symbol_elements.append(cv.Path.MoveTo(coord[0], coord[1]))
            symbol_elements.append(cv.Path.LineTo(coord[0] + self.INPUT_ARM_WIDTH, coord[1]))
            coord = (coord[0] + self.INPUT_ARM_WIDTH, coord[1])
            self.output_coord.append(coord)

        self.shapes = [
            cv.Text(start_x + (self.FULL_SIDE_WIDTH / 4) + 5, start_y - 40, "VCC"),
            cv.Text(start_x + (self.FULL_SIDE_WIDTH / 4) + 5, start_y + 20 + self.FULL_SIDE_LENGTH, "GND"),
            cv.Path(
                elements=symbol_elements,
                paint=Paint(
                    stroke_width=2,
                    style=PaintingStyle.STROKE,
                )
            ),
            cv.Text(start_x + 15 if not xnor else start_x + 5, start_y + 60, label),
            cv.Text(start_x + 30, start_y + 5, "14"),
            cv.Text(start_x + 30, start_y + self.FULL_SIDE_LENGTH - 20, "7")
        ]
    
    def update_color(self):
        dark_mode = self.dm_state.active == DarkModeScheme.DARK
        for shape in self.shapes:
            if type(shape) == cv.Text:
                shape.style.color = "white" if dark_mode else "dark"
            else:
                shape.paint.color = "white" if dark_mode else "dark"