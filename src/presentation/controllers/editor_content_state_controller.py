from flet import *
from presentation.states.editor_content_state import EditorContentState

# from services.pseudocode_parser import parse_pseudocode
from services.pseudocode_parser import PseudocodeParser, grammar
from lark import Lark, v_args

from presentation.controllers.controller import Controller, Priority
from presentation.views.editor_view import EditorView

class EditorContentStateController(Controller):
    priority = Priority.VIEW_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.ec_state = EditorContentState()
        self.ec_state.on_change = self.parse_content

        self.editor_view: EditorView = self.page.session.get("editor_view")

        self.pseudo_parser = Lark(grammar, parser="lalr")
        self.transformer = PseudocodeParser()

    def parse_content(self):
        active: str = self.ec_state.content

        self.transformer.clear()

        if active == "":
            self.editor_view.edit_status_icon.image.src = "/icons_light/blank.png"
            self.editor_view.edit_status_icon.tooltip = "Content is currently blank..."
            self.editor_view.edit_status_icon.update()
            return

        try:
            tree = self.pseudo_parser.parse(active)
            ast: PseudocodeParser = self.transformer.transform(tree)

            self.editor_view.dummy_text.value = f"{ast}"
            self.editor_view.dummy_text.update()

            self.editor_view.edit_status_icon.image.src = "/icons_light/correct.png"
            self.editor_view.edit_status_icon.tooltip = "Content is correct..."
            self.editor_view.edit_status_icon.update()
        except Exception as err:
            self.editor_view.dummy_text.value = f"{str(err)}"
            self.editor_view.dummy_text.update()

            self.editor_view.edit_status_icon.image.src = "/icons_light/wrong.png"
            self.editor_view.edit_status_icon.tooltip = "Content is containing errors..."
            self.editor_view.edit_status_icon.update()