import flet as ft

class Titlebar(ft.WindowDragArea):
    def __init__(self):
        super().__init__(
            content=ft.Container(
                content = ft.Row(
                    controls = [
                        ft.Text("Logihelp", size=24, color="white", weight=ft.FontWeight.BOLD),
                        ft.Row(
                            controls = [
                                ft.Container(
                                    content=AccountButton(),
                                    padding=ft.padding.only(right=24),
                                ),
                                ft.IconButton(ft.Icons.MINIMIZE, on_click=self.minimize, icon_size=16, width=32, height=32, icon_color=ft.Colors.WHITE),
                                ft.IconButton(ft.Icons.CROP_SQUARE, on_click=self.maximize, icon_size=16, width=32, height=32, icon_color=ft.Colors.WHITE),
                                ft.IconButton(ft.Icons.CLOSE, icon_size=16, icon_color=ft.Colors.WHITE, width=32, height=32, on_click=lambda e: self.page.window.close())
                            ]
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                bgcolor="#191f51",
                padding = ft.padding.symmetric(8, 16)
            )
        )
    

    def minimize(self, event):
        self.page.window.minimized = True
        self.page.update()

    def maximize(self, event):
        self.page.window.maximized = not self.page.window.maximized
        self.page.update()

class AccountButton(ft.PopupMenuButton):
    def __init__(self):
        super().__init__()
        self.icon = ft.Icons.PERSON
        self.icon_color = ft.Colors.WHITE