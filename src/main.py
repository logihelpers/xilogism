import flet as ft
import splash
import titlebar as tb
import sidebar as sb
from gates.not_gate import NOTGate
from gates.and_gate import ANDGate
from gates.or_gate import ORGate
from gates.xor_gate import XORGate

async def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme_seed = "#4169e1"
    )
    page.fonts = {"Product Sans" : "/Product Sans Regular.ttf"}
    page.theme = ft.Theme(color_scheme_seed = "#4169e1", font_family="Product Sans")
    page.window.title_bar_hidden = True
    page.window.center()
    page.padding = ft.padding.all(0)
    page.window.width = 960
    page.window.height = 600
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
    
    print("Input Coordinates", ag.input_coord)
    print("Output Coordinates", ag.output_coord)

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
                            ft.Row([ng, ag, nag, og, nog, xg, xog], scroll=True)
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