from flet import *
from math import pi
from presentation.states.title_button_state import *
from presentation.states.sidebar_hide_state import *

from xilowidgets import Revealer

class TitleBar(Container):
    widget_scale: float = 1.0
    old_scale: float = 1.0
    sidebar_hide_button: FilledButton = None
    title: str = "START XILOGISM"
    def __init__(self):
        super().__init__()

        self.title_button_state = TitleButtonState()
        self.sidebar_hide_state = SideBarHideState()
    
    def build(self):
        super().build()

        self.sidebar_hide_button_content = Image(
            src="/icons_light/sidebar_hide.png",
            width=16 * self.widget_scale,
            height=16 * self.widget_scale,
        )

        self.sidebar_show_button_content = Image(
            src="/icons_light/sidebar_show.png",
            width=16 * self.widget_scale,
            height=16 * self.widget_scale,
        )

        self.sidebar_hide_button = FilledButton(
            height=32,
            width=32,
            bgcolor="#00ffffff",
            scale = 1,
            animate_scale=animation.Animation(250, AnimationCurve.BOUNCE_OUT),
            rotate=transform.Rotate(0, alignment.center),
            animate_rotation=animation.Animation(250, AnimationCurve.EASE_IN_OUT),
            on_animation_end=self._rerotate,
            on_click=self.sidebar_hide_state.invert,
            on_hover=self._rotate_buttons,
            content=AnimatedSwitcher(
                content=self.sidebar_hide_button_content,
                transition=AnimatedSwitcherTransition.FADE,
                duration=250,
                reverse_duration=250,
                switch_in_curve=AnimationCurve.LINEAR,
                switch_out_curve=AnimationCurve.LINEAR,
            )
        )

        self.settings_button = FilledButton(
            height=32,
            width=32,
            content = Image(
                src="/icons_light/setting.png",
                width=16 * self.widget_scale,
                height=16 * self.widget_scale,
            ),
            bgcolor="#00ffffff",
            scale = 1,
            animate_scale=animation.Animation(250, AnimationCurve.BOUNCE_OUT),
            rotate=transform.Rotate(0, alignment.center),
            animate_rotation=animation.Animation(250, AnimationCurve.EASE_IN_OUT),
            on_animation_end=self._rerotate,
            on_click=lambda e: setattr(self.title_button_state, 'state', WindowState.SETTINGS),
            on_hover=self._rotate_buttons,
        )

        self.hidden_profile_button_revealer = Container(
            height=32,
            width=32,
            padding=0,
            content=Revealer(
                content_hidden=True,
                content_length=32,
                padding=0,
                orientation=Revealer.Orientation.HORIZONTAL,
                content=FilledButton(
                    content = Image(
                        src="/icons_light/guest_user.png",
                        width=16 * self.widget_scale,
                        height=16 * self.widget_scale,
                    ),
                    bgcolor="#00ffffff",
                    scale = 1,
                    animate_scale=animation.Animation(250, AnimationCurve.BOUNCE_OUT),
                    rotate=transform.Rotate(0, alignment.center),
                    animate_rotation=animation.Animation(250, AnimationCurve.EASE_IN_OUT),
                    on_animation_end=self._rerotate,
                    on_click=lambda e: setattr(self.title_button_state, 'state', WindowState.PROFILE),
                    on_hover=self._rotate_buttons,
                )
            )
        )

        self.content = Container(
            padding=padding.symmetric(0, 8),
            content = Row(
                controls=[
                    Row(
                        controls=[
                            self.sidebar_hide_button,
                            WindowDragArea(
                                expand = True,
                                content = Container(
                                    Text(
                                        value=self.title,
                                        weight=FontWeight.W_600,
                                        size=16 * self.widget_scale,
                                    ),
                                    expand = True,
                                    padding=padding.only(left=16 * self.widget_scale),
                                )
                            )
                        ],
                        expand=True
                    ),
                    Row(
                        spacing = 16,
                        controls=[
                            self.hidden_profile_button_revealer,
                            self.settings_button,
                            FilledButton(
                                height=32,
                                width=32,
                                content = Image(
                                    src="/icons_light/minimize_new.png",
                                    width=16 * self.widget_scale,
                                    height=16 * self.widget_scale,
                                ),
                                bgcolor="#00ffffff",
                                scale = 1,
                                animate_scale=animation.Animation(250, AnimationCurve.BOUNCE_OUT),
                                rotate=transform.Rotate(0, alignment.center),
                                on_animation_end=self._rerotate,
                                animate_rotation=animation.Animation(250, AnimationCurve.EASE_IN_OUT),
                                on_click = lambda e: setattr(self.title_button_state, 'state', WindowState.MINIMIZE),
                                on_hover=self._rotate_buttons,
                            ),
                            FilledButton(
                                height=32,
                                width=32,
                                content = Image(
                                    src="/icons_light/maximize_new.png",
                                    width=16 * self.widget_scale,
                                    height=16 * self.widget_scale,
                                ),
                                bgcolor="#00ffffff",
                                scale = 1,
                                animate_scale=animation.Animation(250, AnimationCurve.BOUNCE_OUT),
                                rotate=transform.Rotate(0, alignment.center),
                                animate_rotation=animation.Animation(250, AnimationCurve.EASE_IN_OUT),
                                on_animation_end=self._rerotate,
                                on_click = lambda e: setattr(self.title_button_state, 'state', WindowState.MAXIMIZE),
                                on_hover=self._rotate_buttons,
                            ),
                            FilledButton(
                                height=32,
                                width=32,
                                content = Image(
                                    src="/icons_light/close_new.png",
                                    width=16 * self.widget_scale,
                                    height=16 * self.widget_scale,
                                ),
                                bgcolor="#00ffffff",
                                scale = 1,
                                animate_scale=animation.Animation(250, AnimationCurve.BOUNCE_OUT),
                                rotate=transform.Rotate(0, alignment.center),
                                animate_rotation=animation.Animation(250, AnimationCurve.EASE_IN_OUT),
                                on_animation_end=self._rerotate,
                                on_click = lambda e: setattr(self.title_button_state, 'state', WindowState.CLOSE),
                                on_hover=self._rotate_buttons,
                            ),
                        ]
                    )
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN
            )
        )
    
    def scale_all(self, scale: float):
        if abs(scale - self.old_scale) > 0.05:
            self.widget_scale = scale
            self.build()
            self.update()

            self.old_scale = scale
    
    def _rotate_buttons(self, event: ControlEvent):
        button: FilledButton = event.control

        button.rotate.angle = pi / 6 if event.data == "true" else 0
        button.scale = 1.25 if event.data == "true" else 1
        button.update()
    
    def _rerotate(self, event: ControlEvent):
        button: FilledButton = event.control

        button.rotate.angle = 0
        button.scale = 1
        button.update()