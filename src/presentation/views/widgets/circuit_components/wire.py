import flet.canvas as cv
import random
from flet import *
from presentation.views.widgets.circuit_components.abstract_element import LogicElement

light_mode_colors = [
    "#B30000", "#B31A00", "#B33300", "#B34D00", "#B36600", "#B38000", "#B39A00", "#B3B300",
    "#9AB300", "#80B300", "#66B300", "#4DB300", "#33B300", "#1AB300", "#00B300", "#00B31A",
    "#00B333", "#00B34D", "#00B366", "#00B380", "#00B39A", "#00B3B3", "#009AB3", "#0080B3",
    "#0066B3", "#004DB3", "#0033B3", "#001AB3", "#0000B3", "#1A00B3", "#3300B3", "#4D00B3",
    "#6600B3", "#8000B3", "#9A00B3", "#B300B3", "#B3009A", "#B30080", "#B30066", "#B3004D",
    "#B30033", "#B3001A", "#B31A1A", "#B3331A", "#B34D1A", "#B3661A", "#B3801A", "#B39A1A",
    "#B3B31A", "#9AB31A", "#80B31A", "#66B31A", "#4DB31A", "#33B31A", "#1AB31A", "#00B31A",
    "#00B333", "#00B34D", "#00B366", "#00B380", "#00B39A", "#00B3B3", "#009AB3", "#0080B3"
]

dark_mode_colors = [
    "#FF3333", "#FF4D33", "#FF6633", "#FF8033", "#FF9933", "#FFB333", "#FFCC33", "#FFE633",
    "#E6FF33", "#CCFF33", "#B3FF33", "#99FF33", "#80FF33", "#66FF33", "#4DFF33", "#33FF33",
    "#33FF4D", "#33FF66", "#33FF80", "#33FF99", "#33FFB3", "#33FFCC", "#33FFE6", "#33FFFF",
    "#33E6FF", "#33CCFF", "#33B3FF", "#3399FF", "#3380FF", "#3366FF", "#334DFF", "#3333FF",
    "#4D33FF", "#6633FF", "#8033FF", "#9933FF", "#B333FF", "#CC33FF", "#E633FF", "#FF33FF",
    "#FF33E6", "#FF33CC", "#FF33B3", "#FF3399", "#FF3380", "#FF3366", "#FF4D4D", "#FF6666",
    "#FF8066", "#FF9966", "#FFB366", "#FFCC66", "#FFE666", "#FFFF66", "#E6FF66", "#CCFF66",
    "#B3FF66", "#99FF66", "#80FF66", "#66FF66", "#4DFF66", "#33FF66", "#33FF80", "#33FF99"
]

class Wire(LogicElement):
    def __init__(self, start_element: LogicElement, end_element: LogicElement, multiple_input_index: int = 0):
        super().__init__()
        
        # Handle output coordinates from start element
        # For ICs, output_coord is a list of tuples; for gates, it's a single tuple
        if isinstance(start_element.output_coord, list) and len(start_element.output_coord) > 0:
            # For ICs, use the first output pin by default
            # Ideally, this could be parameterized to select specific output pins
            x0, y0 = start_element.output_coord[0]
        else:
            # For standard gates
            x0, y0 = start_element.output_coord
        
        # Handle input coordinates for end element
        # Ensure the index is within range
        if multiple_input_index >= len(end_element.input_coord):
            multiple_input_index = 0  # Default to first input if index is out of range
            
        x1, y1 = end_element.input_coord[multiple_input_index]
        
        wire_elements = [
            cv.Path.MoveTo(x0, y0)
        ]
        
        # Determine routing based on start element's output position
        # Default to RIGHT if not specified
        output_position = getattr(start_element, 'output_node_position', LogicElement.Position.RIGHT)
        
        if output_position == LogicElement.Position.BOTTOM:
            wire_elements.extend([
                cv.Path.LineTo(x0, y1),
                cv.Path.LineTo(x1, y1)
            ])
        else:  # Default to RIGHT positioning
            # Calculate midpoint for better routing
            mid = (x1 - x0) / 2
            wire_elements.extend([
                cv.Path.LineTo(x0 + mid, y0),
                cv.Path.LineTo(x0 + mid, y1),
                cv.Path.LineTo(x1, y1)
            ])

        self.shapes = [
            cv.Path(
                elements=wire_elements,
                paint=Paint(
                    stroke_width=2,
                    style=PaintingStyle.STROKE,
                    color=random.choice(light_mode_colors)
                )
            )
        ]