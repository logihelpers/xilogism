from flet import *
from presentation.states.editor_content_state import EditorContentState

from services.pseudo_parser import PseudocodeParser

from presentation.controllers.controller import Controller, Priority
from presentation.views.editor_view import EditorView

class EditorContentStateController(Controller):
    priority = Priority.VIEW_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.ec_state = EditorContentState()
        self.ec_state.on_change = self.parse_content

        self.editor_view: EditorView = self.page.session.get("editor_view")

        self.parser = PseudocodeParser()

    def parse_content(self):
        active: str = self.ec_state.content
        
        result = self.parser.parse_pseudocode(active)

        self.editor_view.dummy_text.value = self.parser.variable_map.__str__()
        self.editor_view.dummy_text.update()
        self.editor_view.update()