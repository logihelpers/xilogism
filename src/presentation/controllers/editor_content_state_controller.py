from flet import *
from presentation.states.editor_content_state import EditorContentState

from presentation.controllers.controller import Controller, Priority

class EditorContentStateController(Controller):
    priority = Priority.VIEW_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.ec_state = EditorContentState()
        self.ec_state.on_change = self.parse_content

    def parse_content(self):
        active: str = self.ec_state.content
        
        print(active)

        # USE PARSER