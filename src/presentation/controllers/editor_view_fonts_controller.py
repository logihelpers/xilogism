from flet import *

from presentation.views.editor_view import EditorView
from presentation.states.active_font_state import ActiveFontState
from data.fonts import Fonts
from models.font_model import FontType

from presentation.controllers.controller import Controller, Priority

class EditorViewFontsController(Controller):
    priority = Priority.LAST
    def __init__(self, page: Page, editor_view: EditorView = None):
        self.page = page
        self.fonts = Fonts()

        if editor_view is None:
            self.editor_view: EditorView = page.session.get("editor_view")
        else:
            self.editor_view = editor_view

        self.af_state = ActiveFontState()

        self.load_font_options()
        self.load_default()

        self.af_state.on_font_change = self.change_font
        self.af_state.on_size_change = self.change_font
    
    def change_font(self):
        self.editor_view.code_editor.font_family = self.af_state.active_font.font_name
        self.editor_view.code_editor.font_size = self.af_state.font_size
        self.editor_view.code_editor.update()

        self.editor_view.font_size_tf.size_tf.value = self.af_state.font_size
        self.editor_view.font_size_tf.size_tf.update()
    
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

        target_font_type = FontType.UI if dyslexic_friendly_mode else FontType.MONOSPACE

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