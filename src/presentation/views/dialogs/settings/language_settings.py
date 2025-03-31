from flet import *
from presentation.views.widgets.settings_image_button import SettingsImageButton

class LanguageSettings(Column):
    def __init__(self):
        super().__init__()

        self.scroll=ScrollMode.ALWAYS
        self.expand=True
        self.spacing = 16

        self.controls=[
            Text("English", weight=FontWeight.BOLD),
            SettingsImageButton("/screenshot_light.png", None, "language", 0.75),
            Text("Tagalog", weight=FontWeight.BOLD),
            SettingsImageButton("/screenshot_light.png", None, "language", 0.75),
            Text("Cebuano", weight=FontWeight.BOLD),
            SettingsImageButton("/screenshot_light.png", None, "language", 0.75),
            Text("Spanish", weight=FontWeight.BOLD),
            SettingsImageButton("/screenshot_light.png", None, "language", 0.75),
            Text("French", weight=FontWeight.BOLD),
            SettingsImageButton("/screenshot_light.png", None, "language", 0.75),
            Text("Japanese", weight=FontWeight.BOLD),
            SettingsImageButton("/screenshot_light.png", None, "language", 0.75),
            Text("Mandarin", weight=FontWeight.BOLD),
            SettingsImageButton("/screenshot_light.png", None, "language", 0.75),
        ]