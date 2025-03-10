import flet as ft

class TitleBar(ft.WindowDragArea):
    def __init__(self):
        self.sidebar_hide_button = ft.FilledButton(
            content = ft.Image(
                src="/icons_light/sidebar_show.png",
                width=16,
                height=16,
            ),
            bgcolor="#00ffffff"
        )

        self.settings_button = ft.FilledButton(
            content = ft.Image(
                src="/icons_light/setting.png",
                width=16,
                height=16,
            ),
            bgcolor="#00ffffff"
        )

        self.content = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        self.sidebar_hide_button,
                        ft.Container(
                            ft.Text(
                                value="START XILOGISM",
                                weight=ft.FontWeight.W_600,
                                size=16
                            ),
                            padding=ft.padding.only(left=16),
                        )
                    ],
                    expand=True
                ),
                ft.Row(
                    spacing = 0,
                    controls=[
                        self.settings_button,
                        ft.FilledButton(
                            content = ft.Image(
                                src="/icons_light/minimize_new.png",
                                width=16,
                                height=16,
                            ),
                            bgcolor="#00ffffff",
                            on_click = self.minimize
                        ),
                        ft.FilledButton(
                            content = ft.Image(
                                src="/icons_light/maximize_new.png",
                                width=16,
                                height=16,
                            ),
                            bgcolor="#00ffffff",
                            on_click = self.maximize
                        ),
                        ft.FilledButton(
                            content = ft.Image(
                                src="/icons_light/close_new.png",
                                width=16,
                                height=16,
                            ),
                            bgcolor="#00ffffff",
                            on_click = lambda e: self.page.window.close()
                        ),
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        super().__init__(content=self.content)

    def minimize(self, event):
        self.page.window.minimized = True
        self.page.update()

    def maximize(self, event):
        self.page.window.maximized = not self.page.window.maximized
        self.page.update()

    def print_size(self, event):
        print(event.data)

class AccountButton(ft.IconButton):
    def __init__(self):
        super().__init__()
        self.icon = ft.Icons.PERSON
        self.icon_color = ft.Colors.WHITE