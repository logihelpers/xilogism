from flet import *
from presentation.states.language_state import LanguageState
from presentation.states.accent_color_state import AccentColorState
from presentation.states.dark_mode_state import *

class ExportButton(Container):
    def __init__(self):
        super().__init__()

        self.lang_state = LanguageState()
        self.ac_state = AccentColorState()
        self.dm_state = DarkModeState()

        self.export_icon = Image(
            src="/icons_light/export.png",
            width=16,
            height=16
        )

        self.border=border.all(1, "black")
        self.border_radius=8
        self.bgcolor="#4d191f51"
        self.height=32
        self.padding=padding.symmetric(4, 8)
        self.content=Row(
            controls=[
                Text(
                    value="Export",
                    weight=FontWeight.BOLD
                ),
                self.export_icon
            ]
        )

        self.on_hover = self._hover__
    
    def _hover__(self, event: ControlEvent):
        colors = self.ac_state.color_values
        button: Container = event.control
        if "4d" in colors["button_bgcolor"]:
            button.bgcolor = colors["button_bgcolor"].replace("4d", "73") if event.data == "true" else colors["button_bgcolor"]
        else:
            button.bgcolor = colors["button_bgcolor"].replace("#", "#73") if event.data == "true" else colors["button_bgcolor"]
        button.update()
    
    def update_lang(self):
        lang_values = self.lang_state.lang_values
        self.content.controls[0].value = lang_values["export_label"]
        self.update()
    
    def did_mount(self):
        super().did_mount()
        self.ac_state.on_colors_updated = self.update_colors
    
    def update_colors(self):
        colors = self.ac_state.color_values
        dark_mode = self.dm_state.active == DarkModeScheme.DARK
        self.border = border.all(1, colors["text_color"])
        self.bgcolor = colors["button_bgcolor"]
        self.content.controls[0].color = colors["text_color"]  # Text # Image
        # def _hover__(event: ControlEvent):
        #     button: Container = event.control
        #     button.bgcolor = colors["sidebar_color_deeper"] if event.data == "true" else colors["button_bgcolor"]
        #     button.update()
        # self.on_hover = _hover__

        self.export_icon.src = "/icons_light/export.png" if not dark_mode else "/icons_dark/export.png"
        self.update()