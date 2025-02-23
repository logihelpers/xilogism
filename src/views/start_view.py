import flet as ft
from sidebar import SideBar, SideBarButton
from flet_route import Params, Basket

class StartView(ft.Container):
    def __init__(self):
        super().__init__()

        self.content = ft.Row(
            controls=[
                SideBar(),
                ft.Container(
                    content = ft.Column(
                        controls=[
                            ft.Text("Good Evening, Owen!", weight=ft.FontWeight.W_900, size=32),
                            SideBarButton(ft.Icons.SEARCH, "Search", "#d8d8d8", "#666666"),
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
                            # canvas
                        ]
                    ),
                    expand = True,
                    padding=ft.padding.all(16)
                )
            ],
            expand=True
        )