from presentation.states.expand_canvas_state import ExpandCanvasState

from flet import *

from presentation.controllers.controller import Controller, Priority

from presentation.views.editor_view import EditorView

class ExpandCanvasController(Controller):
    priority = Priority.VIEW_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.ec_state = ExpandCanvasState()

        self.ec_state.on_change = self.change_view

        self.editor_view: EditorView = self.page.session.get("editor_view")

    def change_view(self):
        expand: bool = self.ec_state.expand

        self.editor_view.code_pane.content.opacity = 0 if expand else 1
        self.editor_view.code_pane.content.update()
        self.editor_view.code_pane.content_hidden = expand
        self.editor_view.code_pane.update()
        