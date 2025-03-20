import flet as ft

class StartView(ft.Container):
    widget_scale: float = 1.0
    old_scale: float = 1.0
    def __init__(self):
        super().__init__()
        self.widget_scale = 1.0
    
    def build(self):
        self.padding = ft.padding.all(16)
        self.expand = True
        self.expand_loose = True
        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            controls=[
                ft.Container(
                    content = ft.Image(
                        src="/icons_light/logo.png",
                        width=(320 * self.widget_scale) * 1.10,
                        height=(320 * self.widget_scale) * 1.10
                    ),
                    expand=True
                ),
                ft.Column(
                    expand=True,
                    alignment = ft.MainAxisAlignment.CENTER,
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    spacing = 0,
                    controls = [
                        ft.Text(
                            spans=[
                                ft.TextSpan(
                                    text="GET YOUR HANDS DIRTY WITH\n",
                                    style=ft.TextStyle(
                                        size=16 * self.widget_scale,
                                        italic=True
                                    )
                                ),
                                ft.TextSpan(
                                    text="XILOGISM",
                                    style=ft.TextStyle(
                                        size=72 * self.widget_scale,
                                        weight=ft.FontWeight.W_800,
                                    )
                                )
                            ],
                            text_align=ft.TextAlign.START,
                            no_wrap=True
                        ),
                        ft.Text(
                            value="CODES TO CIRCUITS, XILOGIZED!",
                            size=20,
                            weight=ft.FontWeight.W_700,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(
                            padding = ft.padding.all(16 * self.widget_scale),
                            margin = ft.margin.symmetric(8 * self.widget_scale, 16 * self.widget_scale),
                            width=480 * self.widget_scale,
                            height=128 * self.widget_scale,
                            content = ft.FilledButton(
                                content=ft.Container(
                                    padding = ft.padding.all(16 * self.widget_scale),
                                    content = ft.Row(
                                        controls=[
                                            ft.Image(
                                                src="/icons_light/new.png",
                                                width=56 * self.widget_scale,
                                                height=56 * self.widget_scale
                                            ),
                                            ft.Text(
                                                spans=[
                                                    ft.TextSpan(
                                                        text="CREATE MY XILOGISM\n",
                                                        style=ft.TextStyle(
                                                            size=16 * self.widget_scale,
                                                            color="black",
                                                            weight=ft.FontWeight.W_600
                                                        )
                                                    ),
                                                    ft.TextSpan(
                                                        text="Pseudocode Format",
                                                        style=ft.TextStyle(
                                                            size=12 * self.widget_scale,
                                                            color="black",
                                                            italic=True
                                                        )
                                                    )
                                                ],
                                                text_align=ft.TextAlign.CENTER,
                                                expand=True
                                            )
                                        ]
                                    )
                                ),
                                style=ft.ButtonStyle(
                                    bgcolor="#4d191f51",
                                    shape=ft.RoundedRectangleBorder(16 * self.widget_scale)
                                )
                            )
                        ),
                        ft.Container(
                            padding=ft.padding.symmetric(0, 80 * self.widget_scale),
                            width=480 * self.widget_scale,
                            height=48 * self.widget_scale,
                            content = ft.FilledButton(
                                content=ft.Container(
                                    padding = ft.padding.symmetric(8 * self.widget_scale, 16 * self.widget_scale),
                                    content = ft.Row(
                                        controls = [
                                            ft.Image(
                                                src="/icons_light/open.png",
                                                width=16 * self.widget_scale,
                                                height=16 * self.widget_scale
                                            ),
                                            ft.Text(
                                                value="OPEN EXISTING",
                                                weight=ft.FontWeight.W_600,
                                                color="black",
                                                text_align=ft.TextAlign.CENTER,
                                                expand=True
                                            )
                                        ],
                                    )
                                ),
                                bgcolor="#26191f51"
                            )
                        )
                    ]
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