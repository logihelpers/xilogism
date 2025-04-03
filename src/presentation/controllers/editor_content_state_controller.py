from flet import *
from presentation.states.editor_content_state import EditorContentState

class EditorContentStateController:
    def __init__(self, page: Page):
        self.page = page

        self.ec_state = EditorContentState()
        self.ec_state.on_change = self.parse_content

    def parse_content(self):
        active: str = self.ec_state.content
        
        print(active)

        # USE PARSER