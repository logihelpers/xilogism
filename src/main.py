import flet as ft
import splash
import titlebar as tb
import sidebar as sb
import flet.canvas as cv

from logic_circuit.gates.not_gate import NOTGate
from logic_circuit.gates.and_gate import ANDGate
from logic_circuit.gates.or_gate import ORGate
from logic_circuit.gates.xor_gate import XORGate
from logic_circuit.input_node import InputNode
from logic_circuit.output_node import OutputNode
from logic_circuit.wire import Wire
from logic_circuit.canvas import LogicCanvas

async def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme_seed = "#4169e1"
    )
    page.fonts = {
        "Product Sans" : "/Product Sans Regular.ttf",
        "Inter" : "/Inter.ttf"
    }
    page.theme = ft.Theme(color_scheme_seed = "#4169e1", font_family="Inter")
    page.window.title_bar_hidden = True
    page.window.center()
    page.padding = ft.padding.all(0)
    page.window.width = 1280
    page.window.height = 768
    page.spacing = 0
    page.bgcolor = "#ededed"

    page.appbar = tb.Titlebar()
    
    ng = NOTGate(30, 50)
    ag = ANDGate(120, 50, input_count=5)
    nag = ANDGate(230, 50, nand=True)
    og = ORGate(340, 50)
    nog = ORGate(450, 50, nor=True, input_count=4)
    xg = XORGate(560, 50)
    xog = XORGate(670, 50, xnor=True, input_count=3)

    inn = InputNode(780, 50)
    onn = OutputNode(830, 50)

    wire = Wire(inn.output_coord, onn.input_coord)

    canvas = LogicCanvas()
    canvas.add_to_canvas(ng)
    canvas.add_to_canvas(ag)
    canvas.add_to_canvas(nag)
    canvas.add_to_canvas(og)
    canvas.add_to_canvas(nog)
    canvas.add_to_canvas(xg)
    canvas.add_to_canvas(xog)
    canvas.add_to_canvas(inn)
    canvas.add_to_canvas(onn)
    canvas.add_to_canvas(wire)
    
    page.add(
        ft.Row(
            controls=[
                sb.SideBar(),
                ft.Container(
                    content = ft.Column(
                        controls=[
                            ft.Text("Good Evening, Owen!", weight=ft.FontWeight.W_900, size=32),
                            sb.SideBarButton(ft.Icons.SEARCH, "Search", "#d8d8d8", "#666666"),
                            ft.Text("Pinned Projects", size=16),
                            ft.Row(
                                controls=[
                                    ft.Container(ft.Text(""), width=128, height = 160, bgcolor="#d9d9d9"),
                                    ft.Container(ft.Text(""), width=128, height = 160, bgcolor="#d9d9d9"),
                                    ft.Container(ft.Text(""), width=128, height = 160, bgcolor="#d9d9d9"),
                                    ft.Container(ft.Text(""), width=128, height = 160, bgcolor="#d9d9d9"),
                                    ft.Container(ft.Text(""), width=128, height = 160, bgcolor="#d9d9d9"),
                                    ft.Container(ft.Text(""), width=128, height = 160, bgcolor="#d9d9d9"),
                                    ft.Container(ft.Text(""), width=128, height = 160, bgcolor="#d9d9d9")
                                ],
                                scroll=True
                            ),
                            ft.Text("Recent Projects", size=16),
                            ft.Divider(),
                            canvas
                        ]
                    ),
                    expand = True,
                    padding=ft.padding.all(16)
                )
            ],
            expand=True
        )
    )

    first_login = await page.client_storage.get_async("first-login")
    if first_login is None:
        await page.client_storage.set_async("first-login", False)

# ft.app(splash.app)
ft.app(main)