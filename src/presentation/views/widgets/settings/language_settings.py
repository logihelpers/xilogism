from flet import *
from presentation.views.widgets.settings.settings_image_button import SettingsImageButton
from presentation.states.language_state import Languages, LanguageState
from presentation.states.dark_mode_state import *
from presentation.states.accent_color_state import AccentColorState

class LanguageSettings(Column):
    def __init__(self):
        super().__init__()

        self.scroll=ScrollMode.ALWAYS
        self.expand=True
        self.spacing = 16

        self.lang_state = LanguageState()
        self.ac_state = AccentColorState()
        self.dm_state = DarkModeState()

        self.preview_image = Image(
            "/icons_light/language_english.png",
            width=600,
            # height=250,
            scale=0.9,
            expand = True,
            fit=ImageFit.FIT_WIDTH
        )

        self.lang_chooser = RadioGroup(
            on_change = self.switch_lang,
            content = Column(
                spacing=16,
                expand=True,
                scroll = ScrollMode.ALWAYS,
                controls=[
                    Radio(value=lang.value, label=lang.name)
                        for lang in Languages
                ]
            )
        )

        self.controls=[
            Text("Language", weight=FontWeight.BOLD),
            Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                alignment=MainAxisAlignment.CENTER,
                expand = True,
                controls = [
                    self.preview_image,
                    Container(
                        expand = True,
                        margin = margin.only(right=16),
                        border_radius = 8,
                        content = self.lang_chooser,
                        padding=8
                    )
                ]
            ),
        ]
    
    def switch_lang(self, event: ControlEvent):
        self.lang_state.active = Languages(event.data)
    
    def did_mount(self):
        super().did_mount()
        self.lang_state.on_lang_updated = self.update_lang
        self.ac_state.on_colors_updated = self.update_colors
        self.update_colors()
    
    def update_lang(self):
        lang_values = self.lang_state.lang_values
        self.lang_chooser.value = self.lang_state.active.value
        self.controls[0].value = lang_values["language_title"]
        self.update()
    
    def update_colors(self):
        dark_mode = self.dm_state.active == DarkModeScheme.DARK
        self.controls[1].controls[1].border = border.all(1, "white" if dark_mode else "black")
        self.update()