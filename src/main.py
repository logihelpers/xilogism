from flet import *
import splash

from presentation.controllers import Controller
from services.init.init_fonts import InitFonts
from services.init.init_files import InitFiles
from services.init.init_login import InitLogin

class Xilogism:
    def __init__(self, page: Page):
        this = page

        this.theme_mode = ThemeMode.LIGHT
        this.theme = Theme(
            color_scheme_seed = "#4169e1",
            dialog_theme= DialogTheme(
                shape=RoundedRectangleBorder(radius=8)
            ),
        )

        InitFonts(this)
        InitFiles(this)

        Controller.initialize_controllers(target=this)

        this.theme = Theme(font_family="Inter")
        this.window.title_bar_hidden = True
        this.padding = padding.all(0)
        this.window.min_height = 640
        this.window.min_width = 1024
        this.window.width = 1024
        this.window.height = 640
        this.spacing = 0
        this.window.center()

        InitLogin(this)

# app(splash.app)
app(Xilogism)