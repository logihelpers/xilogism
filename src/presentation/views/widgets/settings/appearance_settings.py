from flet import *
from slidablepanel import SlidablePanel

from presentation.views.widgets.settings.settings_image_button import SettingsImageButton

class AppearanceSettings(Column):
    def __init__(self):
        super().__init__()

        self.scroll=ScrollMode.ALWAYS
        self.expand=True
        self.spacing = 16

        self.dark_mode_options = SlidablePanel(
            orientation=SlidablePanel.Orientation.VERTICAL,
            content_length=200,
            content = Row(
                spacing = 24,
                controls = [
                    SettingsImageButton("/screenshot_light.png", "Default", "theme_mode"),
                    SettingsImageButton("/screenshot_dark.png", "Dark", "theme_mode")
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
                    SettingsImageButton("/screenshot_light.png", "Default", "sidebar_pos"),
                    SettingsImageButton("/sidebar_right_light.png", "Right", "sidebar_pos")
                ]
            ),
        ]
    
    def hide_panel(self, event: ControlEvent):
        self.dark_mode_options.content_hidden = True if event.data == "true" else False
        self.update()
                
