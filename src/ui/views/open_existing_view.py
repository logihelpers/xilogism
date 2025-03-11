import flet as ft

class OpenExistingView(ft.Container):
    widget_scale: float = 1.0
    old_scale: float = 1.0
    def __init__(self):
        super().__init__()
        self.widget_scale = 1.0
    
    def build(self):
        self.padding = ft.padding.all(16 * self.widget_scale)
        # self.expand = True
        self.content = ft.Column(
            controls = [
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            "Buon giorno, Amico!",
                            color="black",
                            weight=ft.FontWeight.W_700,
                            italic=True,
                            size=28
                        ),
                        ft.Container(
                            padding = ft.padding.symmetric(8, 24),
                            border_radius=32,
                            bgcolor="#4d191f51",
                            border=ft.border.all(1, "black"),
                            content=ft.Row(
                                controls=[
                                    ft.Image(
                                        src="/icons_light/search.png",
                                        width=16,
                                        height=16
                                    ),
                                    ft.Text(
                                        "Search",
                                        color="black",
                                        weight=ft.FontWeight.W_500,
                                        size=14,
                                        width=128
                                    )
                                ]
                            )
                        )
                    ]
                ),
                ft.Text(
                    "Pinned Projects",
                    weight=ft.FontWeight.W_500,
                    size=14
                ),
                ft.Row( # Pinned row
                    controls=[],
                    scroll=True
                ),
                ft.Container(
                    content = ft.Text(
                        "Recent Projects",
                        weight=ft.FontWeight.W_500,
                        size=14
                    ),
                    padding=ft.padding.only(top=16)
                ),
                ft.Divider(1, color="#6b6b6b"),
                ft.Column( # Recents Column
                    controls=[

                    ],
                    expand=True
                )
            ]
        )

        super().build()
    
    def scale_all(self, scale: float):
        if abs(scale - self.old_scale) > 0.05:
            self.widget_scale = scale
            self.build()
            self.update()

            self.old_scale = scale
    
    class PinnedButton(ft.FilledButton):
        def __init__(self):
            super.__init__()
    
    class RecentsButton(ft.FilledButton):
        def __init__(self):
            super.__init__()