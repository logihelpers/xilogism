from abc import ABC

class LogicElement(ABC):
    class Position:
        TOP: int = 0
        LEFT: int = 1
        BOTTOM: int = 2
        RIGHT: int = 3

    shapes: list = None
    rect: tuple = None
    output_node_position: Position = None
    output_coord: tuple = None
    input_coord: list = None