from flet import *
import splash

from presentation.controllers import InitControllers
from services.fonts import InitFonts

class Xilogism(Page):
    def __init__(self, page: Page):
        self = page

        page.theme_mode = ThemeMode.LIGHT
        self.theme = Theme(
            color_scheme_seed = "#4169e1"
        )

        InitFonts(self)
        
        self.theme = Theme(color_scheme_seed = "#4169e1", font_family="Inter")
        self.window.title_bar_hidden = True
        self.window.center()
        self.padding = padding.all(0)
        self.window.min_height = 600
        self.window.min_width = 980
        self.window.width = 980
        self.window.height = 600
        self.spacing = 0
        self.bgcolor = "#ededed"

        InitControllers(target=self)

# app(splash.app)
app(Xilogism)