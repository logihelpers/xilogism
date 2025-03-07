import flet as ft
import base64
from PIL import Image
from io import BytesIO
import os

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
            width=500,
            height=300,
            fit=ft.ImageFit.NONE,
            repeat=ft.ImageRepeat.NO_REPEAT,
            border_radius=ft.border_radius.all(10),
        )

        self.canvas = LogicCanvas()
        self.canvas.on_capture = self.display_canvas
        self.canvas.height=250

        self.save_button = ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.SAVE),
                    ft.Text("Save")
                ]
            ),
            width=96,
            on_click= lambda x: self.canvas.capture(500, 300)
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
                                ft.Container(self.canvas, expand=True),
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

        save_to_png = ft.TextButton("Save", on_click=self.save_to_png)

        dlg_modal = ft.AlertDialog(
            title=ft.Text("Export"),
            content=ft.Image(
                src_base64=event.data,
                width=500,
                height=300,
                fit=ft.ImageFit.NONE,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(10),
            ),
            actions_alignment=ft.MainAxisAlignment.END,
            actions=[save_to_png]
        )

        self.page.open(dlg_modal)
    
    def save_to_png(self, event: ft.ControlEvent):
        img_data = base64.b64decode(self.imageshow.src_base64)
        img = Image.open(BytesIO(img_data))

        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Get the bounding box of non-transparent content
        alpha = img.split()[3]  # Get alpha channel
        bbox = alpha.getbbox()  # Returns (left, upper, right, lower) of non-transparent area
        
        if bbox:
            # Crop to content
            content = img.crop(bbox)
            
            # Get original dimensions
            width, height = img.size
            
            # Calculate new position to center the content
            content_width = bbox[2] - bbox[0]
            content_height = bbox[3] - bbox[1]
            
            left = (width - content_width) // 2
            top = (height - content_height) // 2
            
            # Create new transparent image
            centered_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            
            # Paste content in centered position
            centered_img.paste(content, (left, top))
    
            centered_img.save("ss.png", "PNG")
            centered_img.save("ss.pdf", "PDF")
    
    def build(self):
        self.page.run_task(self.populate_canvas)
        super().build()
    
    async def populate_canvas(self):
        ng = NOTGate(30, 50)
        ag = ANDGate(120, 50, input_count=5)
        nag = ANDGate(230, 50, nand=True, input_count=3)

        wire2 = Wire(ng, ag, 0)
        wire4 = Wire(ag, nag, 2)

        self.canvas.add_to_canvas(ng, ag, nag)
        self.canvas.add_to_canvas(wire2, wire4)
        self.canvas.update()