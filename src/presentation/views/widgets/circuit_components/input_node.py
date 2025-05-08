from flet import *
import flet.canvas as cv

from presentation.views.widgets.circuit_components.abstract_element import LogicElement
from presentation.states.dark_mode_state import DarkModeState, DarkModeScheme

class InputNode(LogicElement):
    FULL_LENGTH: int = 50
    OUTPUT_ARM_WIDTH: int = 20

    __CIRCLE_DIAMETER: int = 30
    __INNER_CIRCLE_DIAMETER: int = 20
    FULL_WIDTH: int = FULL_LENGTH + __CIRCLE_DIAMETER

    def __init__(self, start_x: int, start_y: int):
        super().__init__()

        self.dm_state = DarkModeState()
        self.dm_state.on_change = self.update_color

        output_line = cv.Path.LineTo(start_x + (InputNode.__CIRCLE_DIAMETER / 2), start_y + InputNode.__CIRCLE_DIAMETER + InputNode.OUTPUT_ARM_WIDTH)

        self.shapes = [
            cv.Circle(
                start_x + (InputNode.__CIRCLE_DIAMETER / 2),
                start_y + (InputNode.__CIRCLE_DIAMETER / 2),
                InputNode.__CIRCLE_DIAMETER / 2,
                paint=Paint(
                    stroke_width=2,
                    style=PaintingStyle.STROKE,
                )
            ),
            cv.Circle(
                start_x + (InputNode.__CIRCLE_DIAMETER / 2),
                start_y + (InputNode.__CIRCLE_DIAMETER / 2),
                InputNode.__INNER_CIRCLE_DIAMETER / 2,
                paint=Paint(
                    stroke_width=2,
                    style=PaintingStyle.STROKE,
                )
            ),
            cv.Path(
                elements=[
                    cv.Path.MoveTo(start_x + (InputNode.__CIRCLE_DIAMETER / 2), start_y + InputNode.__CIRCLE_DIAMETER),
                    output_line,
                ],
                paint=Paint(
                    stroke_width=2,
                    style=PaintingStyle.STROKE,
                )
            ),
        ]

        self.output_coord = (output_line.x, output_line.y)
        
        self.output_node_position = LogicElement.Position.BOTTOM
    
    def update_color(self):
        dark_mode = self.dm_state.active == DarkModeScheme.DARK
        for shape in self.shapes:
            shape.paint.color = "white" if dark_mode else "dark"