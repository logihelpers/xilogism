import flet as ft
from sidebar import SideBar, SideBarButton

from logic_circuit.gates.not_gate import NOTGate
from logic_circuit.gates.and_gate import ANDGate
from logic_circuit.gates.or_gate import ORGate
from logic_circuit.gates.xor_gate import XORGate
from logic_circuit.input_node import InputNode
from logic_circuit.output_node import OutputNode
from logic_circuit.wire import Wire
from logic_circuit.canvas import LogicCanvas

from flet_screenshot import FletScreenshot

class EditorView(ft.Container):
    def __init__(self):
        super().__init__()

        ng = NOTGate(30, 50)
        ag = ANDGate(120, 50, input_count=5)
        nag = ANDGate(230, 50, nand=True, input_count=3)

        wire2 = Wire(ng, ag, 0)
        wire4 = Wire(ag, nag, 2)

        canvas = LogicCanvas()
        canvas.add_to_canvas(ng, ag, nag)
        canvas.add_to_canvas(wire2, wire4)
        canvas.height=250

        self.screenshoter = FletScreenshot(
            content=ft.Container(canvas, expand=True),
            expand=True
        )
        self.screenshoter.on_capture = lambda e: print(e.data)

        self.save_button = ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.SAVE),
                    ft.Text("Save")
                ]
            ),
            width=96,
            on_click= lambda x: self.screenshoter.capture()
        )

        self.main_column = ft.Column(
            controls=[
                ft.Card(
                    content = ft.Container(
                        content = ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.ElevatedButton(
                                            content=ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.ADD),
                                                    ft.Text("New")
                                                ]
                                            ),
                                            width=96
                                        ),
                                        ft.ElevatedButton(
                                            content=ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.FILE_OPEN),
                                                    ft.Text("Open")
                                                ]
                                            ),
                                            width=96
                                        )
                                    ]
                                ),
                                ft.VerticalDivider(color=ft.Colors.BLACK, width=9, thickness=16),
                                ft.Column(
                                    controls=[
                                        self.save_button,
                                        ft.ElevatedButton(
                                            content=ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.SAVE_AS),
                                                    ft.Text("Save as")
                                                ]
                                            ),
                                            width=96
                                        )
                                    ]
                                )
                            ]
                        ),
                        padding=16
                    )
                ),
                ft.Row(
                    controls=[
                        ft.TextField(
                            expand=True,
                            multiline=True,
                            fit_parent_size=True,
                            text_vertical_align=ft.VerticalAlignment.START
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("Logic Diagram"),
                                self.screenshoter,
                                ft.Text("Circuit Diagram"),
                                ft.Container(canvas, expand=True)
                            ],
                            expand=True,
                            scroll=True
                        )
                    ],
                    expand=True
                )
            ]
        )

        self.content = ft.Row(
            controls=[
                ft.Container(
                    content = self.main_column,
                    expand = True,
                    padding=ft.padding.all(16)
                )
            ],
            expand=True
        )