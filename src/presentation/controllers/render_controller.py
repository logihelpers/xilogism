from presentation.states.render_state import RenderState
from models.xilofile_model import XiloFile

from flet import *

from presentation.controllers.controller import Controller, Priority

from presentation.views.widgets.logic_circuit.input_node import InputNode
from presentation.views.widgets.logic_circuit.output_node import OutputNode
from presentation.views.widgets.logic_circuit.wire import Wire

class RenderController(Controller):
    priority = Priority.NONE
    def __init__(self, page: Page):
        self.page = page

        self.render_state = RenderState()
        self.render_state.on_input_change = self.process_input

    def process_input(self, input: dict):
        key_name, input_dict = input.popitem()
        nodes = []

        for input_name, gate_info in input_dict.items():
            gate_type = gate_info["type"]
            match gate_type:
                case "INPUT_NODE":
                    nodes.append(InputNode(30, 50))
                case "OUTPUT_NODE":
                    nodes.append(OutputNode(200, 80))
                # case "WIRE":
                    # print("WIRE:", gate_info)
        
        self.render_state.output[key_name] = nodes