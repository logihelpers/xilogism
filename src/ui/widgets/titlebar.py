import flet as ft

class TitleBar(ft.Container):
    widget_scale: float = 1.0
    old_scale: float = 1.0
    sidebar_hide_button: ft.FilledButton = None
    def __init__(self):
        super().__init__()

        self.sidebar_hide_button = ft.FilledButton(
            bgcolor="#00ffffff"
        )

        self.build()
    
    def build(self):
        self.sidebar_hide_button.content = ft.Image(
            src="/icons_light/sidebar_show.png",
            width=16 * self.widget_scale,
            height=16 * self.widget_scale,
        )

        self.settings_button = ft.FilledButton(
            content = ft.Image(
                src="/icons_light/setting.png",
                width=16 * self.widget_scale,
                height=16 * self.widget_scale,
            ),
            bgcolor="#00ffffff"
        )

        self.content = ft.WindowDragArea(
            content = ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            self.sidebar_hide_button,
                            ft.Container(
                                ft.Text(
                                    value="START XILOGISM",
                                    weight=ft.FontWeight.W_600,
                                    size=16 * self.widget_scale
                                ),
                                padding=ft.padding.only(left=16 * self.widget_scale),
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
                                    width=16 * self.widget_scale,
                                    height=16 * self.widget_scale,
                                ),
                                bgcolor="#00ffffff",
                                on_click = self.minimize
                            ),
                            ft.FilledButton(
                                content = ft.Image(
                                    src="/icons_light/maximize_new.png",
                                    width=16 * self.widget_scale,
                                    height=16 * self.widget_scale,
                                ),
                                bgcolor="#00ffffff",
                                on_click = self.maximize
                            ),
                            ft.FilledButton(
                                content = ft.Image(
                                    src="/icons_light/close_new.png",
                                    width=16 * self.widget_scale,
                                    height=16 * self.widget_scale,
                                ),
                                bgcolor="#00ffffff",
                                on_click = lambda e: self.page.window.close()
                            ),
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )

        super().build()

    def minimize(self, event):
        self.page.window.minimized = True
        self.page.update()

    def maximize(self, event):
        self.page.window.maximized = not self.page.window.maximized
        self.page.update()
    
    def scale_all(self, scale: float):
        if abs(scale - self.old_scale) > 0.05:
            self.widget_scale = scale
            self.build()
            self.update()

            self.old_scale = scale