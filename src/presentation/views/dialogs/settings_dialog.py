from flet import *
from xilowidgets import Switcher, XDialog

from presentation.views.widgets.settings.appearance_settings import AppearanceSettings
from presentation.views.widgets.settings.accessibility_settings import AccessibilitySettings
from presentation.views.widgets.settings.language_settings import LanguageSettings

from presentation.states.language_state import LanguageState
from presentation.states.dialogs_state import DialogState, Dialogs
from presentation.states.animation_disable_state import AnimationDisableState
from presentation.states.settings_navigator_state import SettingsNavigatorState
from presentation.states.accent_color_state import AccentColorState
from presentation.states.dark_mode_state import DarkModeState, DarkModeScheme

from utils.singleton import Singleton

class SettingsDialog(XDialog, metaclass = Singleton):
    def __init__(self):
        super().__init__()

        self.dia_state = DialogState()
        self.sn_state = SettingsNavigatorState()
        self.lang_state = LanguageState()

        self.appearance_settings = AppearanceSettings()
        self.accessibility_settings = AccessibilitySettings()
        self.language_settings = LanguageSettings()
        self.ad_state = AnimationDisableState()
        self.ad_state.on_change = self.update_animations
        self.ac_state = AccentColorState()
        self.dm_state = DarkModeState()

        self.content_padding = 0
        self.title_padding = 0
        self.action_button_padding = 0
        self.elevation = 0
        self.actions = []
        self.actions_padding = 0
        self.clip_behavior = ClipBehavior.HARD_EDGE
        self.open_duration = 300 if self.ad_state.state else 0
        self.animation_curve = AnimationCurve.ELASTIC_IN_OUT
        self.on_dismiss = self.revert_index

        self.bgcolor = "#ededed"

        self.switcher = Switcher(
            orientation = Switcher.Orientation.HORIZONTAL,
            animation_curve=AnimationCurve.EASE_IN_OUT_CUBIC,
            animation_duration=500,
            controls = [
                self.appearance_settings,
                self.accessibility_settings,
                self.language_settings
            ]
        )

        self.navigator = SegmentedButton(
            padding=padding.symmetric(16, 128),
            on_change=self.change_view,
            selected={"0"},
            segments=[
                Segment(
                    value="0",
                    label=Text("Appearance"),
                ),
                Segment(
                    value="1",
                    label=Text("Accessibility"),
                ),
                Segment(
                    value="2",
                    label=Text("Language"),
                )
            ],
        )

        self.title = self.navigator
        self.actions = [
            FilledButton(
                "Close", 
                width=128,
                style=ButtonStyle(
                    color="black",
                    shape=RoundedRectangleBorder(8),
                    padding=8,
                    bgcolor="#4d191f51"
                ),
                on_click=lambda e: setattr(self.dia_state, 'state', Dialogs.CLOSE)
            )
        ]

        self.title_padding = 0
        self.actions_padding = padding.only(right=16, bottom=16)

        self.modal = True
        self.content=Container(
            padding = 8,
            height=600,
            width=720,
            expand=True,
            content = Column(
                horizontal_alignment=CrossAxisAlignment.STRETCH,
                controls=[
                    Container(
                        padding = padding.only(left=16, bottom=16, right=16),
                        expand=True,
                        content = self.switcher
                    )
                ]
            )
        )
    
    def change_view(self, event: ControlEvent):
        self.sn_state.active = int(event.data[2])
    
    def update_animations(self):
        try:
            animate = self.ad_state.state
            self.switcher.animation_duration = 500 if animate else 25
            self.open_duration = 300 if animate else 0
            self.update()
        except:
            pass
    
    def revert_index(self, _):
        self.navigator.selected={"0"}
        self.navigator.update()
    
    def did_mount(self):
        super().did_mount()
        self.lang_state.on_lang_updated = self.update_lang
        self.update_lang()
        self.ac_state.on_colors_updated = self.update_colors
        self.update_colors()
        if self.ac_state.active == DarkModeScheme.DARK:
            self.bgcolor = "#333333"
            self.update()
    
    def update_lang(self):
        lang_values = self.lang_state.lang_values
        self.navigator.segments[0].label.value = lang_values["appearance_label"]
        self.navigator.segments[1].label.value = lang_values["accessibility_label"]
        self.navigator.segments[2].label.value = lang_values["language_label"]
        self.actions[0].text = lang_values["close_button"]
        self.update()
    
    def update_colors(self):
        colors = self.ac_state.color_values
        self.bgcolor = colors["bg_color"]
        self.actions[0].style.color = colors["text_color"]
        self.actions[0].style.bgcolor = colors["button_bgcolor"]
        self.update()