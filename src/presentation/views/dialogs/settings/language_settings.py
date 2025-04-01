from flet import *
from presentation.views.widgets.settings_image_button import SettingsImageButton

class LanguageSettings(Column):
    def __init__(self):
        super().__init__()

        self.scroll=ScrollMode.ALWAYS
        self.expand=True
        self.spacing = 16

        self.controls=[
            Text("Language", weight=FontWeight.BOLD),
            Row(
                spacing = 16,
                wrap=True,
                controls = [
                    SettingsImageButton("/icons_light/language_english.png", "English", "language", 0.75),
                    SettingsImageButton("/icons_light/language_tagalog.png", "Tagalog", "language", 0.75),
                    SettingsImageButton("/icons_light/language_cebuano.png", "Cebuano", "language", 0.75),
                    SettingsImageButton("/icons_light/language_spanish.png", "Spanish", "language", 0.75),
                    SettingsImageButton("/icons_light/language_french.png", "French", "language", 0.75),
                    SettingsImageButton("/icons_light/language_japanese.png", "Japanese", "language", 0.75),
                    SettingsImageButton("/icons_light/language_chinese.png", "Mandarin", "language", 0.75),
                    SettingsImageButton("/icons_light/language_brainrot.png", "Brainrot", "language", 0.75),
                ]
            )
        ]