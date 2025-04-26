from flet import *
from presentation.states.editor_content_state import EditorContentState, CodeState
from presentation.states.sidebar_hide_state import *

from services.ast_converter import *
from services.ast_validator import *
from services.new_pseudocode_parser import PseudocodeParser
from services.pygenerator import PythonGenerator
from services.validator import PythonValidator
from services.boolean_converter import BooleanConverter

from presentation.controllers.controller import Controller, Priority
from presentation.views.editor_view import EditorView

import json

class EditorContentStateController(Controller):
    priority = Priority.VIEW_BOUND
    old_active: str = ""
    def __init__(self, page: Page):
        self.page = page

        self.ec_state = EditorContentState()
        self.sbh_state = SideBarHideState()
        self.ec_state.on_change = self.parse_content

        self.editor_view: EditorView = self.page.session.get("editor_view")
        self.parser = PseudocodeParser()
        self.pygen = PythonGenerator()
        self.validator = PythonValidator()
        self.boolean_converter = BooleanConverter()

    def parse_content(self):
        active: str = self.ec_state.content

        if self.old_active == active:
            return

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
            output = self.parser.parse(active)
            generated = self.pygen.generate(output)
            
            errors = self.validator.validate(generated)

            converted = self.boolean_converter.convert(generated)

            self.editor_view.dummy_text.value = f"{generated}\n\n\n{converted}\n\n\n\n{self.parser.errors}\n\n\n{errors}"
            self.editor_view.dummy_text.update()

            self.ec_state.code_state = CodeState.CORRECT

            with open("nin.json", "w") as f:
                json.dump(converted, f, indent=4)

            if len(self.parser.errors) > 0:
                self.ec_state.code_state = CodeState.WRONG
        except:
            self.ec_state.code_state = CodeState.WRONG

        # try:
        #     output = self.parser.parse(active)
        #     # ast: PseudocodeParser = self.transformer.transform(tree)

        #     # validator = ASTValidator()

        #     # valid, mistakes = validator.validate(ast)

        #     for overlay in self.page.overlay:
        #         self.page.close(overlay)

        #     if valid and mistakes == None:
        #         self.ec_state.code_state = CodeState.CORRECT

        #         converter = BooleanAlgebraConverter()
        #         bool_exprs = converter.convert_ast_to_boolean(ast)

        #         self.editor_view.dummy_text.value = f"{bool_exprs}"
        #         self.editor_view.dummy_text.update()
        #     else:
        #         self.ec_state.code_state = CodeState.WRONG

        #         message = ""
        #         if len(mistakes) == 1:
        #             message = mistakes[0]
        #         else:
        #             message = f"{len(mistakes)} errors detected. Please fix immediately."

        #         self.page.open(
        #             SnackBar(
        #                 content=Text(message), 
        #                 behavior=SnackBarBehavior.FLOATING, 
        #                 duration=5000,
        #                 show_close_icon=True,
        #                 margin=margin.all(12) if not self.sbh_state.state.value else margin.only(left=212, top=12, right=12, bottom=12)
        #             )
        #         )
        # except Exception as err:
        #     self.editor_view.dummy_text.value = f"{str(err)}"
        #     self.editor_view.dummy_text.update()

        #     self.ec_state.code_state = CodeState.WRONG
    
        self.old_active = active