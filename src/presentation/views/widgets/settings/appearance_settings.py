from flet import *
from xilowidgets import Revealer, Editor, EditorTheme

from presentation.views.widgets.settings.settings_image_button import SettingsImageButton
from presentation.views.widgets.settings.accent_color_button import AccentColorButton
from presentation.states.dark_mode_state import DarkModeState
from presentation.states.editor_theme_state import EditorThemeState
from presentation.states.accent_color_state import AccentColorState, AccentColors

class AppearanceSettings(Column):
    THEME_BUTTON_SCALE: float = 1
    def __init__(self):
        super().__init__()

        self.dm_state = DarkModeState()
        self.et_state = EditorThemeState()
        self.ac_state = AccentColorState()

        self.scroll=ScrollMode.ALWAYS
        self.expand=True
        self.spacing = 16

        self.dark_mode_options = Revealer(
            orientation=Revealer.Orientation.VERTICAL,
            content_length=200,
            content = Row(
                spacing = 24,
                controls = [
                    SettingsImageButton("/screenshot_light.png", "Default", "theme_mode", on_button_press=self.switch_dark_mode),
                    SettingsImageButton("/screenshot_dark.png", "Dark", "theme_mode", on_button_press=self.switch_dark_mode)
                ]
            )
        )

        self.editor_sample = Editor(
            value="Hi, from Xilogism!!!\n\nฅ՞•ﻌ•՞ฅ\n\n",
            gutter_width=48,
            font_family="Inter",
            font_size=14,
            editor_theme=EditorTheme.OBSIDIAN
        )

        self.controls=[
            Text("Dark Mode", weight=FontWeight.BOLD),
            Column(
                spacing = 0,
                controls = [
                    self.dark_mode_options,
                    Container(
                        content = Switch(
                            label="Follow System Dark Mode Settings:      ", 
                            label_position=LabelPosition.LEFT,
                            on_change=self.hide_panel
                        ),
                        padding=padding.only(top = 8)
                    )
                ]
            ),
            Text("Accent Color", weight=FontWeight.BOLD),
            Row(
                controls=[AccentColorButton(color, on_button_press=self.switch_accent) for color in AccentColors]
            ),
            Text("Editor Theme", weight=FontWeight.BOLD),
            Row(
                vertical_alignment=CrossAxisAlignment.START,
                alignment=MainAxisAlignment.CENTER,
                controls = [
                    Container(
                        expand = True,
                        width=200,
                        height=180,
                        border=border.all(1, "black"),
                        clip_behavior=ClipBehavior.ANTI_ALIAS,
                        border_radius=8,
                        content = Container(
                            border_radius=8,
                            content = Row(
                                expand = True,
                                controls = [
                                    self.editor_sample
                                ]
                            )
                        )
                    ),
                    Container(
                        expand = True,
                        margin = margin.only(right=16),
                        border_radius = 8,
                        content = ListView(
                            expand = True,
                            controls = [ThemeButton(theme, theme.name, self.switch_theme) for theme in EditorTheme],
                            height=180,
                            divider_thickness=1
                        ),
                        border=border.all(1, Colors.BLACK)
                    )
                ]
            )
        ]
    
    def hide_panel(self, event: ControlEvent):
        self.dark_mode_options.content_hidden = (event.data == "true")
        self.update()

        self.dm_state.follow_system_active = (event.data == "true")
                
    def switch_dark_mode(self, event: ControlEvent):
        button: SettingsImageButton = event.control

        self.dm_state.active = (button.text == "Dark")
    
    def switch_theme(self, event: ControlEvent):
        button: ThemeButton = event.control
        self.et_state.theme = button.key

        button.leading.opacity = 1
        button.leading.update()

        self.editor_sample.editor_theme = button.key
        self.editor_sample.update()
    
    def switch_accent(self, event: ControlEvent):
        button: AccentColorButton = event.control

        self.ac_state.active = button.color

class ThemeButton(ListTile):
    refs: list = []
    active: bool = False
    def __init__(self, key: EditorTheme = None, name: str = None, on_button_press = None):
        super().__init__()

        self.key = key
        self.name = name

        self.leading = Icon(
            Icons.CHECK,
            color=Colors.BLACK,
            size=32,
            opacity=0
        )

        self.title = Text(name)

        self.on_click = lambda event: self.on_button_press(event)
        self.on_button_press = on_button_press

        if len(ThemeButton.refs) > 0:
            ThemeButton.refs.append(self)
        else:
            self.active = True
            
            self.leading.opacity = 1

            ThemeButton.refs.append(self)
    
    def on_button_press(self, event: ControlEvent):
        pass
