from flet import *
import splash

from presentation.controllers import Controller
from services.init_fonts import InitFonts

class Xilogism(Page):
    def __init__(self, page: Page):
        self = page

        self.theme_mode = ThemeMode.LIGHT
        self.theme = Theme(
            color_scheme_seed = "#4169e1",
            dialog_theme= DialogTheme(
                bgcolor="#fafafa",
                shape=RoundedRectangleBorder(radius=8)
            )
        )

        InitFonts(self)
        
        self.theme = Theme(color_scheme_seed = "#4169e1", font_family="Inter")
        self.window.title_bar_hidden = True
        self.window.center()
        self.padding = padding.all(0)
        self.window.min_height = 620
        self.window.min_width = 980
        self.window.width = 980
        self.window.height = 620
        self.spacing = 0
        self.bgcolor = "#ededed"

        Controller.initialize_controllers(target=self)

# app(splash.app)
app(Xilogism)