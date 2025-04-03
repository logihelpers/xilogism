from flet import *
from xilowidgets import Revealer

from presentation.views.widgets.settings.settings_image_button import SettingsImageButton
from presentation.states.dark_mode_state import DarkModeState

class AppearanceSettings(Column):
    def __init__(self):
        super().__init__()

        self.dm_state = DarkModeState()

        self.scroll=ScrollMode.ALWAYS
        self.expand=True
        self.spacing = 16

        self.dark_mode_options = Revealer(
            orientation=Revealer.Orientation.VERTICAL,
            content_length=200,
            content = Row(
                spacing = 24,
                controls = [
                    SettingsImageButton("/screenshot_light.png", "Default", "theme_mode", on_button_press=self.switch_active),
                    SettingsImageButton("/screenshot_dark.png", "Dark", "theme_mode", on_button_press=self.switch_active)
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
            Text("Sidebar Position", weight=FontWeight.BOLD),
            Row(
                spacing = 24,
                controls = [
                    SettingsImageButton("/screenshot_light.png", "Default", "sidebar_pos", on_button_press=self.switch_active),
                    SettingsImageButton("/sidebar_right_light.png", "Right", "sidebar_pos", on_button_press=self.switch_active)
                ]
            ),
        ]
    
    def hide_panel(self, event: ControlEvent):
        self.dark_mode_options.content_hidden = (event.data == "true")
        self.update()

        self.dm_state.follow_system_active = (event.data == "true")
                
    def switch_active(self, event: ControlEvent):
        button: SettingsImageButton = event.control

        self.dm_state.active = (button.text == "Dark") if button.group_id == "theme_mode" else self.dm_state.active