import flet as ft
from sidebar import SideBar, SideBarButton

class EditorView(ft.Container):
    def __init__(self):
        super().__init__()

        self.main_column = ft.Column(
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