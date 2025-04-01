from flet import *

from presentation.views.editor_view import EditorView
from data.fonts import Fonts
from models.font_model import FontType, Font

class EditorViewFontsController:
    def __init__(self, page: Page):
        self.page = page
        self.fonts = Fonts()

        self.editor_view: EditorView = page.session.get("editor_view")

        self.load_font_options()
        self.load_default()
    
    def load_default(self):
        default_font: str = None
        try:
            default_font = self.page.session.get("editor_font")
        except:
            pass

        default_font = "Iosevka" if default_font is None else default_font

        self.editor_view.font_family_chooser.value = default_font
    
    def load_font_options(self):
        dyslexic_friendly_mode = False
        try:
            dyslexic_friendly_mode = self.page.session.get("dyslexic_friendly_mode")
        except:
            pass

        target_font_type = FontType.DYSLEXIA_FRIENDLY if dyslexic_friendly_mode else FontType.MONOSPACE

        self.editor_view.font_family_chooser.options = [
            DropdownOption(
                key=font.font_name,
                content = Text(
                    font.font_name, 
                    style=TextStyle(
                        font_family=font.font_name
                    )
                ),
            ) 
            
            for font in self.fonts.all_fonts if font.font_type == target_font_type
        ]