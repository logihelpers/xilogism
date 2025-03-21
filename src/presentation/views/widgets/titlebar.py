from flet import *
from presentation.states.title_button_state import *
from presentation.states.sidebar_hide_state import *

class TitleBar(Container):
    widget_scale: float = 1.0
    old_scale: float = 1.0
    sidebar_hide_button: FilledButton = None
    def __init__(self):
        super().__init__()

        self.title_button_state = TitleButtonState()
        self.sidebar_hide_state = SideBarHideState()

        self.sidebar_hide_button = FilledButton(
            bgcolor="#00ffffff",
            on_click=self.sidebar_hide_state.invert
        )

        self.sidebar_hide_button.content = Image(
            src="/icons_light/sidebar_show.png",
            width=16 * self.widget_scale,
            height=16 * self.widget_scale,
        )

        self.settings_button = FilledButton(
            content = Image(
                src="/icons_light/setting.png",
                width=16 * self.widget_scale,
                height=16 * self.widget_scale,
            ),
            bgcolor="#00ffffff"
        )

        self.content = WindowDragArea(
            content = Container(
                padding=padding.symmetric(0, 8),
                content = Row(
                    controls=[
                        Row(
                            controls=[
                                self.sidebar_hide_button,
                                Container(
                                    Text(
                                        value="START XILOGISM",
                                        weight=FontWeight.W_600,
                                        size=16 * self.widget_scale,
                                    ),
                                    padding=padding.only(left=16 * self.widget_scale),
                                )
                            ],
                            expand=True
                        ),
                        Row(
                            spacing = 0,
                            controls=[
                                self.settings_button,
                                FilledButton(
                                    content = Image(
                                        src="/icons_light/minimize_new.png",
                                        width=16 * self.widget_scale,
                                        height=16 * self.widget_scale,
                                    ),
                                    bgcolor="#00ffffff",
                                    on_click = self.minimize
                                ),
                                FilledButton(
                                    content = Image(
                                        src="/icons_light/maximize_new.png",
                                        width=16 * self.widget_scale,
                                        height=16 * self.widget_scale,
                                    ),
                                    bgcolor="#00ffffff",
                                    on_click = self.maximize
                                ),
                                FilledButton(
                                    content = Image(
                                        src="/icons_light/close_new.png",
                                        width=16 * self.widget_scale,
                                        height=16 * self.widget_scale,
                                    ),
                                    bgcolor="#00ffffff",
                                    on_click = self.close_app
                                ),
                            ]
                        )
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN
                )
            )
        )

    def minimize(self, event):
        self.title_button_state.state = WindowState.MINIMIZE

    def maximize(self, event):
        self.title_button_state.state = WindowState.MAXIMIZE
    
    def close_app(self, event):
        self.title_button_state.state = WindowState.CLOSE
    
    def scale_all(self, scale: float):
        if abs(scale - self.old_scale) > 0.05:
            self.widget_scale = scale
            self.build()
            self.update()

            self.old_scale = scale