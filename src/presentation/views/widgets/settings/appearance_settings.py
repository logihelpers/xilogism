from flet import *
from xilowidgets import Revealer

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
                spacing = 16,
                wrap=True,
                scroll = ScrollMode.ALWAYS,
                controls = [
                    SettingsImageButton("/editor_themes/DEFAULT.png", "Default", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/DARK.png", "Dark", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/A11Y_DARK.png", "A11y Dark", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/A11Y_LIGHT.png", "A11y Light", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/AGATE.png", "Agate", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/ANDROIDSTUDIO.png", "Android Studio", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/ARTA.png", "Arta", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/ATOM_ONE_DARK.png", "Atom One Dark", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/IDEA.png", "Idea", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/MONOKAI.png", "Monokai", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/MONOKAI_SUBLIME.png", "Monokai Sublime", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/OBSIDIAN.png", "Obsidian", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/SOLARIZED_LIGHT.png", "Solarized Light", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/SOLARIZED_DARK.png", "Solarized Dark", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/VS2015.png", "VS2015", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/XCODE.png", "XCode", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                ]
            ),
        ]
    
    def hide_panel(self, event: ControlEvent):
        self.dark_mode_options.content_hidden = (event.data == "true")
        self.update()

        self.dm_state.follow_system_active = (event.data == "true")
                
    def switch_dark_mode(self, event: ControlEvent):
        button: SettingsImageButton = event.control

        self.dm_state.active = (button.text == "Dark")
    
    def switch_theme(self, event: ControlEvent):
        button: SettingsImageButton = event.control

        self.et_state.theme = button.text
    
    def switch_accent(self, event: ControlEvent):
        button: AccentColorButton = event.control

        self.ac_state.active = button.color