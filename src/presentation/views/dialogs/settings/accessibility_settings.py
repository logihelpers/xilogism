from flet import *
from presentation.views.widgets.settings_image_button import SettingsImageButton

class AccessibilitySettings(Column):
    def __init__(self):
        super().__init__()

        self.scroll=ScrollMode.ALWAYS
        self.expand=True
        self.spacing = 16

        self.controls = [
            Text("Dyslexia-Friendly Options", weight=FontWeight.BOLD),
            Row(
                spacing = 16,
                controls = [
                    SettingsImageButton("/screenshot_light.png", "Default", "dyslexia", 0.75),
                    SettingsImageButton("/screenshot_dark.png", "Readable", "dyslexia", 0.75)
                ]
            ),
            Text("Vision Friendly Settings", weight=FontWeight.BOLD),
            Row(
                spacing = 16,
                wrap=True,
                controls = [
                    SettingsImageButton("/screenshot_light.png", "Default", "vision", 0.75),
                    SettingsImageButton("/screenshot_light.png", "High-Contrast", "vision", 0.75),
                    SettingsImageButton("/screenshot_dark.png", "Deuteranomaly", "vision", 0.75),
                    SettingsImageButton("/screenshot_dark.png", "Protanomaly", "vision", 0.75),
                    SettingsImageButton("/screenshot_dark.png", "Tritanomaly", "vision", 0.75),
                ]
            ),
            Text("Animation Settings", weight=FontWeight.BOLD),
            Switch(
                label="Disable Animations:      ", 
                label_position=LabelPosition.LEFT,
            ),
            Text("Keyboard Shortcuts", weight=FontWeight.BOLD),
            DataTable(
                columns=[
                    DataColumn(
                        Text("Action")
                    ),
                    DataColumn(
                        Text("Shortcut")
                    )
                ],
                rows=[
                    DataRow(
                        cells=[
                            DataCell(content = Text("Hide Sidebar")),
                            DataCell(content = Text("Ctrl + \\"))
                        ]
                    )
                ]
            )
        ]