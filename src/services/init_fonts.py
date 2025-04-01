from flet import Page
from data.fonts import Fonts

def InitFonts(page: Page):
    fonts = Fonts()
    page.fonts = dict()

    for font in fonts.all_fonts:
        page.fonts[font.font_name] = font.font_file
