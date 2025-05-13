from flet import *

from presentation.controllers import Controller
from services.init.init_fonts import InitFonts
from services.init.init_files import InitFiles
from services.init.init_login import InitLogin

def main(page: Page):
    page.theme_mode = ThemeMode.LIGHT
    page.theme = Theme(
        color_scheme_seed = "#4169e1",
        dialog_theme= DialogTheme(
            shape=RoundedRectangleBorder(radius=8)
        ),
        font_family="Inter"
    )

    InitFonts(page)
    InitFiles(page)

    Controller.initialize_controllers(target=page)

    page.window.title_bar_hidden = True
    page.padding = padding.all(0)
    page.window.min_height = 640
    page.window.min_width = 1024
    page.window.width = 1024
    page.window.height = 640
    page.spacing = 0
    page.window.center()

    InitLogin(page)

app(main)