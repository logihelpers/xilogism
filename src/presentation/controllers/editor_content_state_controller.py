from flet import *
from presentation.states.editor_content_state import EditorContentState, CodeState
from presentation.states.sidebar_hide_state import *

from services.ast_validator import *
from services.pseudocode_parser import PseudocodeParser, grammar
from lark import Lark, v_args

from presentation.controllers.controller import Controller, Priority
from presentation.views.editor_view import EditorView

class EditorContentStateController(Controller):
    priority = Priority.VIEW_BOUND
    old_active: str = ""
    def __init__(self, page: Page):
        self.page = page

        self.ec_state = EditorContentState()
        self.sbh_state = SideBarHideState()
        self.ec_state.on_change = self.parse_content

        self.editor_view: EditorView = self.page.session.get("editor_view")

        self.pseudo_parser = Lark(grammar, parser="lalr")
        self.transformer = PseudocodeParser()

    def parse_content(self):
        active: str = self.ec_state.content

        if self.old_active == active:
            return

        self.transformer.clear()

        """
INPUT ok
OUTPUT uk

IF ok < 10 AND ok > 0 THEN
  assign uk = 10 
ELIF ok < 0 AND ok > -10 THEN
  assign uk = -10
ELSE
  assign uk = 10
        """

        if active == "":
            self.ec_state.code_state = CodeState.BLANK
            return

        try:
            tree = self.pseudo_parser.parse(active)
            ast: PseudocodeParser = self.transformer.transform(tree)

            validator = ASTValidator()

            errors, mistakes = validator.validate(ast)

            if errors and mistakes == None:
                self.ec_state.code_state = CodeState.CORRECT
            else:
                self.ec_state.code_state = CodeState.WRONG

                message = ""
                if len(mistakes) == 1:
                    message = mistakes[0]
                else:
                    message = f"{len(mistakes)} errors detected. Please fix immediately."

                self.page.open(
                    SnackBar(
                        content=Text(message), 
                        behavior=SnackBarBehavior.FLOATING, 
                        duration=5000,
                        show_close_icon=True,
                        margin=margin.all(12) if not self.sbh_state.state.value else margin.only(left=212, top=12, right=12, bottom=12)
                    )
                )

            self.editor_view.dummy_text.value = f"{ast}"
            self.editor_view.dummy_text.update()
        except Exception as err:
            self.editor_view.dummy_text.value = f"{str(err)}"
            self.editor_view.dummy_text.update()

            self.ec_state.code_state = CodeState.WRONG
    
        self.old_active = active