from flet import *
from xiloswitcher import XiloSwitcher

from presentation.views.widgets.settings.appearance_settings import AppearanceSettings
from presentation.views.widgets.settings.accessibility_settings import AccessibilitySettings
from presentation.views.widgets.settings.language_settings import LanguageSettings
from presentation.views.widgets.settings.settings_navigator import SettingsNavigator

from presentation.states.dialogs_state import DialogState, Dialogs

from services.singleton import Singleton

class SettingsDialog(AlertDialog, metaclass = Singleton):
    def __init__(self):
        super().__init__()

        self.dia_state = DialogState()

        self.content_padding = 0
        self.title_padding = 0
        self.action_button_padding = 0
        self.elevation = 0
        self.actions = []
        self.actions_padding = 0
        self.clip_behavior = ClipBehavior.HARD_EDGE

        self.appearance_settings = AppearanceSettings()
        self.accessibility_settings = AccessibilitySettings()
        self.language_settings = LanguageSettings()

        self.switcher = XiloSwitcher(
            orientation = XiloSwitcher.Orientation.HORIZONTAL,
            controls = [
                self.appearance_settings,
                self.accessibility_settings,
                self.language_settings
            ]
        )

        self.title = WindowDragArea(content=SettingsNavigator())
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
            ),
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