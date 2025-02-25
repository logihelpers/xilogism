import flet as ft
from sidebar import SideBar, SideBarButton

class EditorView(ft.Container):
    def __init__(self):
        super().__init__()

        self.main_column = ft.Column(
            controls=[
                ft.Card(
                    ft.Row([ft.Text("AHAHA")])
                ),
                ft.Row(
                    controls=[
                        ft.TextField(expand=True),
                        ft.Column(
                            controls=[
                                ft.Text("Logic Circuit"),
                                ft.Text("Circuit Diagram")
                            ],
                            expand=True
                        )
                    ]
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