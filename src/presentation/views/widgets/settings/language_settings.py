from flet import *
from presentation.views.widgets.settings.settings_image_button import SettingsImageButton
from presentation.states.language_state import Languages, LanguageState

class LanguageSettings(Column):
    def __init__(self):
        super().__init__()

        self.scroll=ScrollMode.ALWAYS
        self.expand=True
        self.spacing = 16

        self.lang_state = LanguageState()

        self.preview_image = Image(
            "/icons_light/language_english.png",
            width=200,
            height=180,
            expand = True,
            fit=ImageFit.FILL
        )

        self.controls=[
            Text("Language", weight=FontWeight.BOLD),
            Row(
                vertical_alignment=CrossAxisAlignment.START,
                alignment=MainAxisAlignment.CENTER,
                controls = [
                    self.preview_image,
                    Container(
                        expand = True,
                        margin = margin.only(right=16),
                        border_radius = 8,
                        content = ListView(
                            expand = True,
                            controls = [LanguageButton(language, self.switch_lang) for language in Languages],
                            height=180,
                            divider_thickness=1
                        ),
                        border=border.all(1, Colors.BLACK)
                    )
                ]
            ),
        ]
    
    def switch_lang(self, event: ControlEvent):
        button: LanguageButton = event.control
        self.lang_state.active = button.language

        button.leading.opacity = 1
        button.leading.update()

        self.preview_image.src = f"/icons_light/language_{button.language.name.lower()}.png"
        self.preview_image.update()

class LanguageButton(ListTile):
    refs: list = []
    active: bool = False
    def __init__(self, language: Languages = None, on_button_press = None):
        super().__init__()

        self.language = language

        self.leading = Icon(
            Icons.CHECK,
            color=Colors.BLACK,
            size=32,
            opacity=0
        )

        self.title = Text(language.name)

        self.on_click = lambda event: self.on_button_press(event)
        self.on_button_press = on_button_press

        if len(LanguageButton.refs) > 0:
            LanguageButton.refs.append(self)
        else:
            self.active = True
            
            self.leading.opacity = 1

            LanguageButton.refs.append(self)
    
    def on_button_press(self, event: ControlEvent):
        pass