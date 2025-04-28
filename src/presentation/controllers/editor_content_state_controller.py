from flet import *
from presentation.states.editor_content_state import EditorContentState, CodeState
from presentation.states.sidebar_hide_state import *
from presentation.states.render_state import *

from services.pseudocode_parser import PseudocodeParser
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
        self.render_state = RenderState()
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
        
        self.old_active = active

        if active == "":
            self.ec_state.code_state = CodeState.BLANK
            return

        try:
            output = self.parser.parse(active)
            generated = self.pygen.generate(output)
            
            errors = self.validator.validate(generated)

            if len(errors) > 0 or len(self.parser.errors) > 0:
                self.show_errors(errors + self.parser.errors)
                self.ec_state.code_state = CodeState.WRONG
                return

            converted = self.boolean_converter.convert(generated)
            self.render_state.input = converted

            self.ec_state.code_state = CodeState.CORRECT
        except Exception as err:
            self.show_errors([str(err)])
            self.ec_state.code_state = CodeState.WRONG
    
    def show_errors(self, errors: list):
        message = ""
        if len(errors) == 1:
            message = errors[0]
        else:
            message = f"{len(errors)} errors detected. Please fix immediately."

        self.page.open(
            SnackBar(
                content=Text(message), 
                behavior=SnackBarBehavior.FLOATING, 
                duration=5000,
                show_close_icon=True,
                margin=margin.all(12) if not self.sbh_state.state.value else margin.only(left=212, top=12, right=12, bottom=12)
            )
        )