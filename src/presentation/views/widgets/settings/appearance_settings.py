from flet import *
from xilowidgets import Revealer

from presentation.views.widgets.settings.settings_image_button import SettingsImageButton
from presentation.states.dark_mode_state import DarkModeState
from presentation.states.editor_theme_state import EditorThemeState

class AppearanceSettings(Column):
    THEME_BUTTON_SCALE: float = 1.5
    def __init__(self):
        super().__init__()

        self.dm_state = DarkModeState()
        self.et_state = EditorThemeState()

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
                controls = [
                    Container(content = Text(""), width=32, height=32, bgcolor=Colors.random(), border_radius=16, border=border.all(0.5, "black")),
                    Container(content = Text(""), width=32, height=32, bgcolor=Colors.random(), border_radius=16, border=border.all(0.5, "black")),
                    Container(content = Text(""), width=32, height=32, bgcolor=Colors.random(), border_radius=16, border=border.all(0.5, "black")),
                    Container(content = Text(""), width=32, height=32, bgcolor=Colors.random(), border_radius=16, border=border.all(0.5, "black")),
                    Container(content = Text(""), width=32, height=32, bgcolor=Colors.random(), border_radius=16, border=border.all(0.5, "black")),
                    Container(content = Text(""), width=32, height=32, bgcolor=Colors.random(), border_radius=16, border=border.all(0.5, "black"))
                ]
            ),
            Text("Editor Theme", weight=FontWeight.BOLD),
            Row(
                spacing = 16,
                scroll = ScrollMode.ALWAYS,
                controls = [
                    SettingsImageButton("/editor_themes/DEFAULT.png", "Default", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/DARK.png", "Dark", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/A11Y_DARK.png", "A11y Dark", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/A11Y_LIGHT.png", "A11y Light", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/AGATE.png", "Agate", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/ANDROIDSTUDIO.png", "Android Studio", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/ARTA.png", "Arta", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/ASCETIC.png", "Ascetic", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/ATOM_ONE_DARK.png", "Atom One Dark", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/ATOM_ONE_LIGHT.png", "Atom One Light", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/IDEA.png", "Idea", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/MONOKAI.png", "Monokai", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/MONOKAI_SUBLIME.png", "Monokai Sublime", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
                    SettingsImageButton("/editor_themes/OBSIDIAN.png", "Obsidian", "editor_theme", self.THEME_BUTTON_SCALE, self.switch_theme),
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

        self.dm_state.active = (button.text == "Dark") if button.group_id == "theme_mode" else self.dm_state.active
    
    def switch_theme(self, event: ControlEvent):
        button: SettingsImageButton = event.control

        self.et_state.theme = button.text.lower().replace(" ", "-")