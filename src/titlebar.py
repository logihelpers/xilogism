import flet as ft

class Titlebar(ft.WindowDragArea):
    def __init__(self):
        self.account_button = AccountButton()
        self.home_button = ft.IconButton (icon = ft.Icons.HOME, icon_color = ft.Colors.WHITE, visible=False)

        super().__init__(
            content=ft.Container(
                content = ft.Row(
                    controls = [
                        ft.Row(
                            controls=[
                                self.home_button,
                                ft.Text("Logihelp", size=24, color="white", weight=ft.FontWeight.BOLD)
                            ]
                        ),
                        ft.Row(
                            controls = [
                                ft.Container(
                                    content=self.account_button,
                                    padding=ft.padding.only(right=24),
                                ),
                                ft.Container(
                                    ft.TextButton("", on_click=self.minimize, width=16, height=16),
                                    bgcolor="#9bdb4d",
                                    shape=ft.BoxShape.CIRCLE,
                                    border=ft.border.all(2, "#3a9104")
                                ),
                                ft.Container(
                                    ft.TextButton("", on_click=self.maximize, width=16, height=16),
                                    bgcolor="#ffe16b",
                                    shape=ft.BoxShape.CIRCLE,
                                    border=ft.border.all(2, "#d48e15")
                                ),
                                ft.Container(
                                    ft.TextButton("", width=16, height=16, on_click=lambda x: self.page.window.close()),
                                    bgcolor="#ed5353",
                                    shape=ft.BoxShape.CIRCLE,
                                    border=ft.border.all(2, "#a10705")
                                ),
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

class AccountButton(ft.IconButton):
    def __init__(self):
        super().__init__()
        self.icon = ft.Icons.PERSON
        self.icon_color = ft.Colors.WHITE