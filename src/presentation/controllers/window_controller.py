from presentation.views.window_view import WindowView
from presentation.states.sidebar_hide_state import *

from flet import *

from presentation.controllers.controller import *

class WindowController(Controller):
    priority = Priority.ENTRY_POINT
    def __init__(self, page: Page):
        self.page = page

        window = WindowView()
        self.page.add(window)

        self.sbh_state = SideBarHideState()

        self.page.session.set("window", window)
        self.page.session.set("sidebar", window.sidebar)
        self.page.session.set("editor_view", window.editor_view)
        self.page.session.set("titlebar", window.titlebar)

        self.page.on_keyboard_event = self.handle_keyboard_events

        dummy_kb_receiver = TextField(width=0, height=0, autofocus=True)

        self.page.add(dummy_kb_receiver)
        self.page.spacing = 0
    
    def handle_keyboard_events(self, event: KeyboardEvent):
        if (event.key == "\\" and event.control):
            self.sbh_state.invert(event)