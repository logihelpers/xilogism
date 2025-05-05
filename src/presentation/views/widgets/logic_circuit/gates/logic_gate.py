import flet as ft
import flet.canvas as cv
from typing import List

from ..abstract_element import LogicElement
from .and_gate import ANDGate
from .not_gate import NOTGate

class LogicGate(LogicElement):
    """Factory class that creates the appropriate logic gate based on type"""
    
    def __init__(self, start_x: int, start_y: int, gate_type: str = "AND", label: str = "", input_count: int = 2):
        super().__init__()
        
        # Create the appropriate gate
        self.gate = self._create_gate(start_x, start_y, gate_type, input_count)
        self.label = label
        self.gate_type = gate_type
        
        # Copy properties from the created gate
        self.shapes = self.gate.shapes
        self.input_coord = self.gate.input_coord
        self.output_coord = self.gate.output_coord
        self.output_node_position = self.gate.output_node_position
        
        # Add a label to the gate if provided
        if label:
            self._add_label(start_x, start_y)
    
    def _create_gate(self, x: int, y: int, gate_type: str, input_count: int) -> LogicElement:
        """Create the appropriate gate based on the specified type"""
        if gate_type == "AND":
            return ANDGate(x, y, input_count=input_count)
        elif gate_type == "NAND":
            return ANDGate(x, y, input_count=input_count, nand=True)
        elif gate_type == "OR":
            return self._create_or_gate(x, y, input_count)
        elif gate_type == "NOR":
            return self._create_nor_gate(x, y, input_count)
        elif gate_type == "NOT":
            return NOTGate(x, y)
        elif gate_type == "XOR":
            return self._create_xor_gate(x, y, input_count)
        elif gate_type == "XNOR":
            return self._create_xnor_gate(x, y, input_count)
        elif gate_type in ["ADDER", "SUBTRACTOR", "MULTIPLIER", "DIVIDER", "MODULO"]:
            return self._create_arithmetic_gate(x, y, gate_type, input_count)
        elif gate_type == "COMPARATOR":
            return self._create_comparator_gate(x, y)
        elif gate_type in ["SHIFT_LEFT", "SHIFT_RIGHT"]:
            return self._create_shift_gate(x, y, gate_type)
        else:
            # Default to AND gate for unknown types
            return ANDGate(x, y, input_count=input_count)
    
    def _add_label(self, x: int, y: int):
        """Add a label text to the gate"""
        # Label positioning depends on gate type
        label_x = x
        label_y = y - 20  # Position above the gate
        
        # Create text element and add to shapes
        text = cv.Text(
            self.label,
            x=label_x,
            y=label_y,
            font_size=12,
            color=ft.colors.BLACK,
            text_align="center",
        )
        
        self.shapes.append(text)
    
    def _create_or_gate(self, x: int, y: int, input_count: int) -> LogicElement:
        """Create an OR gate"""
        # Create a custom OR gate (curved shape)
        gate = LogicElement()
        
        width = 50
        height = 50
        input_arm = 20
        output_arm = 20
        
        # Scale for more inputs
        if input_count > 4:
            scale = 1 + ((input_count - 4) * 0.25)
            height *= scale
        
        # OR gate has a curved left side
        path_elements = [
            # Left curved side
            cv.Path.MoveTo(x, y),
            cv.Path.QuadraticTo(x + 25, y + (height / 2), x, y + height),
            
            # Bottom curve
            cv.Path.QuadraticTo(x + 10, y + height, x + 20, y + height),
            
            # Right side
            cv.Path.LineTo(x + width, y + (height / 2)),
            
            # Top curve
            cv.Path.LineTo(x + 20, y),
            cv.Path.QuadraticTo(x + 10, y, x, y),
            
            # Output line
            cv.Path.MoveTo(x + width, y + (height / 2)),
            cv.Path.LineTo(x + width + output_arm, y + (height / 2))
        ]
        
        # Create input lines
        gate.input_coord = []
        points = self._get_spaced_points(height, input_count)
        
        for point in points:
            # Add input line
            path_elements.append(cv.Path.MoveTo(x + 5, y + point))
            path_elements.append(cv.Path.LineTo(x - input_arm, y + point))
            
            # Store input coordinates
            gate.input_coord.append((x - input_arm, y + point))
        
        # Create shape
        gate.shapes = [
            cv.Path(
                elements=path_elements,
                paint=ft.Paint(
                    stroke_width=2,
                    style=ft.PaintingStyle.STROKE,
                )
            )
        ]
        
        # Set output coordinates
        gate.output_coord = (x + width + output_arm, y + (height / 2))
        gate.output_node_position = LogicElement.Position.RIGHT
        
        return gate
    
    def _create_nor_gate(self, x: int, y: int, input_count: int) -> LogicElement:
        """Create a NOR gate (OR gate with bubble)"""
        # Create OR gate first
        gate = self._create_or_gate(x, y, input_count)
        
        # Add NOT bubble
        circle_size = 10
        output_x, output_y = gate.output_coord
        
        # Adjust output coordinate
        circle_x = output_x - 25
        circle_y = output_y
        
        # Add circle
        gate.shapes.append(
            cv.Circle(
                circle_x,
                circle_y,
                circle_size / 2,
                paint=ft.Paint(
                    stroke_width=2,
                    style=ft.PaintingStyle.STROKE,
                )
            )
        )
        
        return gate
    
    def _create_xor_gate(self, x: int, y: int, input_count: int) -> LogicElement:
        """Create an XOR gate"""
        # XOR is like OR but with an extra curve at the input side
        gate = self._create_or_gate(x, y, input_count)
        
        # Add the extra curve that distinguishes XOR
        width = 50
        height = 50
        
        # Scale for more inputs
        if input_count > 4:
            scale = 1 + ((input_count - 4) * 0.25)
            height *= scale
        
        # Add the distinguishing XOR curve (5px offset from main curve)
        xor_curve = cv.Path(
            elements=[
                cv.Path.MoveTo(x - 5, y),
                cv.Path.QuadraticTo(x + 20, y + (height / 2), x - 5, y + height),
            ],
            paint=ft.Paint(
                stroke_width=2,
                style=ft.PaintingStyle.STROKE,
            )
        )
        
        gate.shapes.append(xor_curve)
        return gate
    
    def _create_xnor_gate(self, x: int, y: int, input_count: int) -> LogicElement:
        """Create an XNOR gate (XOR with bubble)"""
        # Create XOR gate first
        gate = self._create_xor_gate(x, y, input_count)
        
        # Add NOT bubble
        circle_size = 10
        output_x, output_y = gate.output_coord
        
        # Adjust output coordinate
        circle_x = output_x - 25
        circle_y = output_y
        
        # Add circle
        gate.shapes.append(
            cv.Circle(
                circle_x,
                circle_y,
                circle_size / 2,
                paint=ft.Paint(
                    stroke_width=2,
                    style=ft.PaintingStyle.STROKE,
                )
            )
        )
        
        return gate
    
    def _create_arithmetic_gate(self, x: int, y: int, gate_type: str, input_count: int) -> LogicElement:
        """Create an arithmetic gate (represented as a rectangular box with label)"""
        gate = LogicElement()
        
        width = 60
        height = 50
        input_arm = 20
        output_arm = 20
        
        # Scale height for more inputs
        if input_count > 2:
            scale = 1 + ((input_count - 2) * 0.5)
            height *= scale
        
        # Create box
        box = cv.Path(
            elements=[
                cv.Path.MoveTo(x, y),
                cv.Path.LineTo(x + width, y),
                cv.Path.LineTo(x + width, y + height),
                cv.Path.LineTo(x, y + height),
                cv.Path.LineTo(x, y),
            ],
            paint=ft.Paint(
                stroke_width=2,
                style=ft.PaintingStyle.STROKE,
            )
        )
        
        # Add operation symbol text
        symbol = ""
        if gate_type == "ADDER":
            symbol = "+"
        elif gate_type == "SUBTRACTOR":
            symbol = "-"
        elif gate_type == "MULTIPLIER":
            symbol = "×"
        elif gate_type == "DIVIDER":
            symbol = "÷"
        elif gate_type == "MODULO":
            symbol = "%"
        
        text = cv.Text(
            symbol,
            x=x + (width / 2) - 5,
            y=y + (height / 2) + 5,
            font_size=18,
            color=ft.colors.BLACK,
        )
        
        # Add output line
        output_line = cv.Path(
            elements=[
                cv.Path.MoveTo(x + width, y + (height / 2)),
                cv.Path.LineTo(x + width + output_arm, y + (height / 2)),
            ],
            paint=ft.Paint(
                stroke_width=2,
                style=ft.PaintingStyle.STROKE,
            )
        )
        
        # Create input lines
        gate.input_coord = []
        points = self._get_spaced_points(height, input_count)
        
        input_lines = []
        for point in points:
            # Add input line
            input_lines.extend([
                cv.Path.MoveTo(x, y + point),
                cv.Path.LineTo(x - input_arm, y + point),
            ])
            
            # Store input coordinates
            gate.input_coord.append((x - input_arm, y + point))
        
        input_path = cv.Path(
            elements=input_lines,
            paint=ft.Paint(
                stroke_width=2,
                style=ft.PaintingStyle.STROKE,
            )
        )
        
        # Add all shapes
        gate.shapes = [box, text, output_line, input_path]
        
        # Set output coordinate
        gate.output_coord = (x + width + output_arm, y + (height / 2))
        gate.output_node_position = LogicElement.Position.RIGHT
        
        return gate
    
    def _create_comparator_gate(self, x: int, y: int) -> LogicElement:
        """Create a comparator gate (represented as a box with comparison symbol)"""
        # Similar to arithmetic but with comparison symbol
        gate = LogicElement()
        
        width = 60
        height = 50
        input_arm = 20
        output_arm = 20
        
        # Create box
        box = cv.Path(
            elements=[
                cv.Path.MoveTo(x, y),
                cv.Path.LineTo(x + width, y),
                cv.Path.LineTo(x + width, y + height),
                cv.Path.LineTo(x, y + height),
                cv.Path.LineTo(x, y),
            ],
            paint=ft.Paint(
                stroke_width=2,
                style=ft.PaintingStyle.STROKE,
            )
        )
        
        # Comparison symbol (=?)
        text = cv.Text(
            "?=",
            x=x + (width / 2) - 10,
            y=y + (height / 2) + 5,
            font_size=16,
            color=ft.colors.BLACK,
        )
        
        # Add output line
        output_line = cv.Path(
            elements=[
                cv.Path.MoveTo(x + width, y + (height / 2)),
                cv.Path.LineTo(x + width + output_arm, y + (height / 2)),
            ],
            paint=ft.Paint(
                stroke_width=2,
                style=ft.PaintingStyle.STROKE,
            )
        )
        
        # Create input lines (two inputs)
        input_lines = [
            cv.Path.MoveTo(x, y + (height / 3)),
            cv.Path.LineTo(x - input_arm, y + (height / 3)),
            cv.Path.MoveTo(x, y + (height * 2 / 3)),
            cv.Path.LineTo(x - input_arm, y + (height * 2 / 3)),
        ]
        
        input_path = cv.Path(
            elements=input_lines,
            paint=ft.Paint(
                stroke_width=2,
                style=ft.PaintingStyle.STROKE,
            )
        )
        
        # Store input coordinates
        gate.input_coord = [
            (x - input_arm, y + (height / 3)),
            (x - input_arm, y + (height * 2 / 3))
        ]
        
        # Add all shapes
        gate.shapes = [box, text, output_line, input_path]
        
        # Set output coordinate
        gate.output_coord = (x + width + output_arm, y + (height / 2))
        gate.output_node_position = LogicElement.Position.RIGHT
        
        return gate
    
    def _create_shift_gate(self, x: int, y: int, gate_type: str) -> LogicElement:
        """Create a shift left/right gate"""
        gate = LogicElement()
        
        width = 60
        height = 50
        input_arm = 20
        output_arm = 20
        
        # Create box
        box = cv.Path(
            elements=[
                cv.Path.MoveTo(x, y),
                cv.Path.LineTo(x + width, y),
                cv.Path.LineTo(x + width, y + height),
                cv.Path.LineTo(x, y + height),
                cv.Path.LineTo(x, y),
            ],
            paint=ft.Paint(
                stroke_width=2,
                style=ft.PaintingStyle.STROKE,
            )
        )
        
        # Shift symbol
        symbol = "<<" if gate_type == "SHIFT_LEFT" else ">>"
        text = cv.Text(
            symbol,
            x=x + (width / 2) - 10,
            y=y + (height / 2) + 5,
            font_size=16,
            color=ft.colors.BLACK,
        )
        
        # Add output line
        output_line = cv.Path(
            elements=[
                cv.Path.MoveTo(x + width, y + (height / 2)),
                cv.Path.LineTo(x + width + output_arm, y + (height / 2)),
            ],
            paint=ft.Paint(
                stroke_width=2,
                style=ft.PaintingStyle.STROKE,
            )
        )
        
        # Create input lines (two inputs)
        input_lines = [
            cv.Path.MoveTo(x, y + (height / 3)),
            cv.Path.LineTo(x - input_arm, y + (height / 3)),
            cv.Path.MoveTo(x, y + (height * 2 / 3)),
            cv.Path.LineTo(x - input_arm, y + (height * 2 / 3)),
        ]
        
        input_path = cv.Path(
            elements=input_lines,
            paint=ft.Paint(
                stroke_width=2,
                style=ft.PaintingStyle.STROKE,
            )
        )
        
        # Store input coordinates
        gate.input_coord = [
            (x - input_arm, y + (height / 3)),
            (x - input_arm, y + (height * 2 / 3))
        ]
        
        # Add all shapes
        gate.shapes = [box, text, output_line, input_path]
        
        # Set output coordinate
        gate.output_coord = (x + width + output_arm, y + (height / 2))
        gate.output_node_position = LogicElement.Position.RIGHT
        
        return gate
    
    def _get_spaced_points(self, total: float, divisions: int) -> List[float]:
        """Calculate evenly spaced points along a line"""
        step = total / (divisions + 1)
        return [round(step * i, 5) for i in range(1, divisions + 1)]