from flet import *
from math import pi
from presentation.states.title_button_state import *
from presentation.states.sidebar_hide_state import *
from presentation.states.language_state import LanguageState
from presentation.states.accent_color_state import AccentColorState
from presentation.states.dark_mode_state import DarkModeState, DarkModeScheme

from xilowidgets import Revealer

class TitleBar(Container):
    widget_scale: float = 1.0
    old_scale: float = 1.0
    sidebar_hide_button: FilledButton = None
    title: str = "START"
    def __init__(self):
        super().__init__()

        self.title_button_state = TitleButtonState()
        self.sidebar_hide_state = SideBarHideState()
        self.lang_state = LanguageState()
        self.lang_state.on_lang_updated = self.update_lang
        self.ac_state = AccentColorState()
        self.dm_state = DarkModeState()
        self.ac_state.on_colors_updated = self.update_colors

        self.sidebar_hide_button_content = Image(
            src="/icons_light/sidebar_hide.png",
            width=16 * self.widget_scale,
            height=16 * self.widget_scale,
            tooltip="Hide the side bar"
        )

        self.sidebar_show_button_content = Image(
            src="/icons_light/sidebar_show.png",
            width=16 * self.widget_scale,
            height=16 * self.widget_scale,
            tooltip="Show the side bar"
        )

        self.sidebar_hide_button = FilledButton(
            height=32,
            width=32,
            bgcolor="#00ffffff",
            scale = 1,
            animate_scale=Animation(250, AnimationCurve.BOUNCE_OUT),
            rotate=Rotate(0, alignment.center),
            animate_rotation=Animation(250, AnimationCurve.EASE_IN_OUT),
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
        
        self.tutorial_button = FilledButton(
            height=32,
            width=32,
            content = Image(
                src="/icons_light/tutorial.png",
                width=16 * self.widget_scale,
                height=16 * self.widget_scale,
            ),
            bgcolor="#00ffffff",
            scale = 1,
            animate_scale=Animation(250, AnimationCurve.BOUNCE_OUT),
            rotate=Rotate(0, alignment.center),
            animate_rotation=Animation(250, AnimationCurve.EASE_IN_OUT),
            on_animation_end=self._rerotate,
            on_click=lambda e: setattr(self.title_button_state, 'state', WindowState.TUTORIAL),
            on_hover=self._rotate_buttons,
            tooltip="Application Tutorial"
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
            animate_scale=Animation(250, AnimationCurve.BOUNCE_OUT),
            rotate=Rotate(0, alignment.center),
            animate_rotation=Animation(250, AnimationCurve.EASE_IN_OUT),
            on_animation_end=self._rerotate,
            on_click=lambda e: setattr(self.title_button_state, 'state', WindowState.SETTINGS),
            on_hover=self._rotate_buttons,
            tooltip="Application Settings"
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
                        width=24,
                        height=24,
                    ),
                    bgcolor="#00ffffff",
                    scale = 1,
                    animate_scale=Animation(250, AnimationCurve.BOUNCE_OUT),
                    rotate=Rotate(0, alignment.center),
                    animate_rotation=Animation(250, AnimationCurve.EASE_IN_OUT),
                    on_animation_end=self._rerotate,
                    on_click=lambda e: setattr(self.title_button_state, 'state', WindowState.PROFILE),
                    on_hover=self._rotate_buttons,
                    tooltip="User settings"
                )
            )
        )

        self.filename_tf = TextField(
            value=self.title,
            text_size=16 * self.widget_scale,
            text_style=TextStyle(
                weight=FontWeight.W_600,
            ),
            height = 32,
            fit_parent_size=True,
            border=InputBorder.NONE,
            border_color="white",
            multiline=False,
            expand=True,
            expand_loose= True,
            disabled=True,
            color="#000000",
            on_change = lambda e: setattr(self.title_button_state, 'title', e.data)
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
                                    content = Row(
                                        controls = [
                                            self.filename_tf
                                        ],
                                        width=180
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
                            self.tutorial_button,
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
                                animate_scale=Animation(250, AnimationCurve.BOUNCE_OUT),
                                rotate=Rotate(0, alignment.center),
                                on_animation_end=self._rerotate,
                                animate_rotation=Animation(250, AnimationCurve.EASE_IN_OUT),
                                on_click = lambda e: setattr(self.title_button_state, 'state', WindowState.MINIMIZE),
                                on_hover=self._rotate_buttons,
                                tooltip="Minimize the app"
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
                                animate_scale=Animation(250, AnimationCurve.BOUNCE_OUT),
                                rotate=Rotate(0, alignment.center),
                                animate_rotation=Animation(250, AnimationCurve.EASE_IN_OUT),
                                on_animation_end=self._rerotate,
                                on_click = lambda e: setattr(self.title_button_state, 'state', WindowState.MAXIMIZE),
                                on_hover=self._rotate_buttons,
                                tooltip="Maximize the app"
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
                                animate_scale=Animation(250, AnimationCurve.BOUNCE_OUT),
                                rotate=Rotate(0, alignment.center),
                                animate_rotation=Animation(250, AnimationCurve.EASE_IN_OUT),
                                on_animation_end=self._rerotate,
                                on_click = lambda e: setattr(self.title_button_state, 'state', WindowState.CLOSE),
                                on_hover=self._rotate_buttons,
                                tooltip="Close the app"
                            ),
                        ]
                    )
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN
            )
        )
    
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
    
    def update_lang(self):
        lang_values = self.lang_state.lang_values
        self.sidebar_hide_button_content.tooltip = lang_values["hide_sidebar_tooltip"]
        self.sidebar_show_button_content.tooltip = lang_values["show_sidebar_tooltip"]
        self.tutorial_button.tooltip = lang_values["tutorial_tooltip"]
        self.settings_button.tooltip = lang_values["settings_tooltip"]
        self.hidden_profile_button_revealer.content.content.tooltip = lang_values["user_settings_tooltip"]
        self.content.content.controls[1].controls[3].tooltip = lang_values["minimize_tooltip"]
        self.content.content.controls[1].controls[4].tooltip = lang_values["maximize_tooltip"]
        self.content.content.controls[1].controls[5].tooltip = lang_values["close_tooltip"]
        self.filename_tf.value = lang_values["default_title"]
        self.update()
    
    def update_colors(self):
        colors = self.ac_state.color_values
        dark_mode = self.dm_state.active == DarkModeScheme.DARK
        self.filename_tf.color = colors["text_color"]
        self.filename_tf.border_color = colors["text_color"]
        buttons = [
            self.sidebar_hide_button,
            self.tutorial_button,
            self.settings_button,
            self.hidden_profile_button_revealer.content.content,  # Profile button inside Revealer
            self.content.content.controls[1].controls[3],  # Minimize
            self.content.content.controls[1].controls[4],  # Maximize
            self.content.content.controls[1].controls[5]   # Close
        ]
        for button in buttons:
            button.style = ButtonStyle(
                bgcolor=colors["button_bgcolor"],
            )
        self.sidebar_hide_button_content.src = "/icons_light/sidebar_hide.png" if not dark_mode else "/icons_dark/sidebar_hide.png"
        self.sidebar_show_button_content.src = "/icons_light/sidebar_show.png" if not dark_mode else "/icons_dark/sidebar_show.png"
        self.tutorial_button.content.src = "/icons_light/tutorial.png" if not dark_mode else "/icons_dark/tutorial.png"
        self.settings_button.content.src = "/icons_light/setting.png" if not dark_mode else "/icons_dark/setting.png"
        self.content.content.controls[1].controls[3].content.src = "/icons_light/minimize_new.png" if not dark_mode else "/icons_dark/minimize_new.png"
        self.content.content.controls[1].controls[4].content.src = "/icons_light/maximize_new.png" if not dark_mode else "/icons_dark/maximize_new.png"
        self.content.content.controls[1].controls[5].content.src = "/icons_light/close_new.png" if not dark_mode else "/icons_dark/close_new.png"
        self.hidden_profile_button_revealer.content.content.content.src = "/icons_light/guest_user.png" if not dark_mode else "/icons_dark/guest_user.png"
        self.update()