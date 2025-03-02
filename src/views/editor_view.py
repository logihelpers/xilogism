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

class EditorView(ft.Container):
    def __init__(self):
        super().__init__()

        self.imageshow = ft.Image(
            src="https://picsum.photos/200/200?3",
            width=200,
            height=200,
            fit=ft.ImageFit.NONE,
            repeat=ft.ImageRepeat.NO_REPEAT,
            border_radius=ft.border_radius.all(10),
        )

        ng = NOTGate(30, 50)
        ag = ANDGate(120, 50, input_count=5)
        nag = ANDGate(230, 50, nand=True, input_count=3)

        wire2 = Wire(ng, ag, 0)
        wire4 = Wire(ag, nag, 2)

        canvas = LogicCanvas()
        canvas.on_capture = self.display_canvas
        canvas.add_to_canvas(ng, ag, nag)
        canvas.add_to_canvas(wire2, wire4)
        canvas.height=250

        self.save_button = ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.SAVE),
                    ft.Text("Save")
                ]
            ),
            width=96,
            on_click= lambda x: canvas.capture()
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
                                ft.Container(canvas, expand=True),
                                ft.Text("Circuit Diagram"),
                                self.imageshow,
                                ft.Text("                Bill of Materials"),
                                ft.Container(
                                    content = ft.DataTable(
                                        bgcolor="white",
                                        border=ft.border.all(2, "black"),
                                        border_radius=10,
                                        vertical_lines=ft.BorderSide(2, "black"),
                                        horizontal_lines=ft.BorderSide(1, "black"),
                                        columns=[
                                            ft.DataColumn(ft.Text("Amount"), numeric=True),
                                            ft.DataColumn(ft.Text("Gate Type")),
                                            ft.DataColumn(ft.Text("Component")),
                                        ],
                                        rows=[
                                            ft.DataRow(
                                                cells=[
                                                    ft.DataCell(ft.Text("5")),
                                                    ft.DataCell(ft.Text("AND")),
                                                    ft.DataCell(ft.Text("74xx")),
                                                ],
                                            ),
                                            ft.DataRow(
                                                cells=[
                                                    ft.DataCell(ft.Text("9")),
                                                    ft.DataCell(ft.Text("NOR")),
                                                    ft.DataCell(ft.Text("74xx")),
                                                ],
                                            ),
                                            ft.DataRow(
                                                cells=[
                                                    ft.DataCell(ft.Text("11")),
                                                    ft.DataCell(ft.Text("XNOR")),
                                                    ft.DataCell(ft.Text("748x")),
                                                ],
                                            ),
                                        ],
                                    ),
                                    padding=ft.padding.symmetric(16, 64)
                                )
                            ],
                            expand=True,
                            scroll=True,
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
    
    def display_canvas(self, event):
        self.imageshow.src_base64 = event.data
        self.imageshow.update()