from flet import *
from xiloswitcher import XiloSwitcher
from enum import Enum

from presentation.views.dialogs.settings.appearance_settings import AppearanceSettings
from presentation.views.dialogs.settings.accessibility_settings import AccessibilitySettings
from presentation.views.dialogs.settings.language_settings import LanguageSettings

class SettingsDialog(AlertDialog):
    def __init__(self):
        super().__init__()
    
    def build(self):
        super().build()
        self.content_padding = 0
        self.title_padding = 0
        self.action_button_padding = 0
        self.elevation = 0
        self.actions = []
        self.actions_padding = 0
        self.clip_behavior = ClipBehavior.HARD_EDGE

        self.page.theme.dialog_theme = DialogTheme(
            bgcolor="#fafafa",
            shape=RoundedRectangleBorder(radius=8)
        )

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

        self.title = SettingsNavigator(self.switcher)
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
                on_click=self.handle_close
            ),
        ]

        self.title_padding = 0
        self.actions_padding = padding.only(right=16, bottom=16)

        self.modal = True
        self.content=WindowDragArea(
            height=600,
            width=620,
            expand=True,
            content = Container(
                padding = 8,
                height=600,
                width=620,
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
        )

    def handle_close(self, e: ControlEvent):
        e.control.page.close(self)

class SettingsNavigator(Container):
    class Button(Container):
        refs: list = []

        class Position(Enum):
            START = 0
            MIDDLE = 1
            END = 2

        def __init__(self, name: str, pos: Position, switcher: XiloSwitcher):
            super().__init__()
            self.name = name
            self.pos = pos
            self.switcher = switcher

            self.animate=animation.Animation(250, AnimationCurve.BOUNCE_OUT)
            self.content = Text(name, size=14)
            self.padding=4
            self.bgcolor="#fafafa"
            self.width=128
            self.alignment=alignment.center
            self.shadow=BoxShadow(0.1, 2, "#6b6b6b")

            match pos:
                case SettingsNavigator.Button.Position.START:
                    self.border = border.all(1, "#6b6b6b")
                    self.border_radius = border_radius.only(4, 0, 4, 0)
                case SettingsNavigator.Button.Position.MIDDLE:
                    self.border= border.symmetric(vertical = BorderSide(1, "#6b6b6b"))
                case SettingsNavigator.Button.Position.END:
                    self.border=border.all(1, "#6b6b6b")
                    self.border_radius=border_radius.only(0, 4, 0, 4)
            
            self.on_click = self.switch
            
            SettingsNavigator.Button.refs.append(self)
        
        def switch(self, event: ControlEvent):
            button: SettingsNavigator.Button = None
            for index, button in enumerate(SettingsNavigator.Button.refs):
                if button.name == event.control.name:
                    button.bgcolor = "#d9fafafa"
                    button.shadow=BoxShadow(0.1, 2, "#191f51")
                    match button.pos:
                        case SettingsNavigator.Button.Position.START:
                            button.border = border.all(1, "#191f51")
                            button.border_radius = border_radius.only(4, 0, 4, 0)
                        case SettingsNavigator.Button.Position.MIDDLE:
                            button.border= border.symmetric(vertical = BorderSide(1, "#191f51"))
                        case SettingsNavigator.Button.Position.END:
                            button.border=border.all(1, "#191f51")
                            button.border_radius=border_radius.only(0, 4, 0, 4)

                    switcher: XiloSwitcher = button.switcher
                    switcher.switch(index)

                else:
                    button.bgcolor="#fafafa"
                    button.shadow=BoxShadow(0.1, 2, "#6b6b6b")

                    match button.pos:
                        case SettingsNavigator.Button.Position.START:
                            button.border = border.all(1, "#6b6b6b")
                            button.border_radius = border_radius.only(4, 0, 4, 0)
                        case SettingsNavigator.Button.Position.MIDDLE:
                            button.border= border.symmetric(vertical = BorderSide(1, "#6b6b6b"))
                        case SettingsNavigator.Button.Position.END:
                            button.border=border.all(1, "#6b6b6b")
                            button.border_radius=border_radius.only(0, 4, 0, 4)

                button.update()

    def __init__(self, switcher: XiloSwitcher):
        super().__init__()

        if len(SettingsNavigator.Button.refs) > 0:
            SettingsNavigator.Button.refs = []

        self.alignment = alignment.center
        self.padding = 16

        self.content = Row(
            controls = [
                SettingsNavigator.Button("Appearance", SettingsNavigator.Button.Position.START, switcher),
                SettingsNavigator.Button("Accessibility", SettingsNavigator.Button.Position.MIDDLE, switcher),
                SettingsNavigator.Button("Language", SettingsNavigator.Button.Position.END, switcher)
            ],
            spacing = 0,
            alignment=MainAxisAlignment.CENTER
        )
    
    def build(self):
        super().build()

        first_button: SettingsNavigator.Button = SettingsNavigator.Button.refs[0]
        first_button.bgcolor = "#d9fafafa"
        first_button.shadow=BoxShadow(0.1, 2, "#191f51")
        
        match first_button.pos:
            case SettingsNavigator.Button.Position.START:
                first_button.border = border.all(1, "#191f51")
                first_button.border_radius = border_radius.only(4, 0, 4, 0)
            case SettingsNavigator.Button.Position.MIDDLE:
                first_button.border= border.symmetric(vertical = BorderSide(1, "#191f51"))
            case SettingsNavigator.Button.Position.END:
                first_button.border=border.all(1, "#191f51")
                first_button.border_radius=border_radius.only(0, 4, 0, 4)