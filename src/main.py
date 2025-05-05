from flet import *
import splash

from presentation.controllers import Controller
from services.init_fonts import InitFonts
from services.init_files import InitFiles

class Xilogism(Page):
    def __init__(self, page: Page):
        self = page

        self.theme_mode = ThemeMode.LIGHT
        self.theme = Theme(
            dialog_theme= DialogTheme(
                shape=RoundedRectangleBorder(radius=8),
                bgcolor="#ededed",
                surface_tint_color="#ededed"
            ),
            font_family="Inter"
        )

        InitFonts(self)
        InitFiles(self)

        Controller.initialize_controllers(target=self)

        self.window.title_bar_hidden = True
        self.padding = padding.all(0)
        self.window.min_height = 640
        self.window.min_width = 1024
        self.window.width = 1024
        self.window.height = 640
        self.spacing = 0
        self.window.center()

# app(splash.app)
app(Xilogism)