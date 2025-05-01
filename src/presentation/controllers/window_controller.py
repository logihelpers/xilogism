from presentation.views.window_view import WindowView
from presentation.states.sidebar_hide_state import *
from presentation.states.media_query_state import MediaQueryState

from flet import *

from presentation.controllers.controller import *

class WindowController(Controller):
    priority = Priority.ENTRY_POINT
    def __init__(self, page: Page):
        self.page = page

        self.window = WindowView()
        self.page.add(self.window)

        self.sbh_state = SideBarHideState()
        self.mq_state = MediaQueryState()
        self.mq_state.on_size_change = self.update_icon_size

        self.page.session.set("window", self.window)
        self.page.session.set("sidebar", self.window.sidebar)
        self.page.session.set("editor_view", self.window.editor_view)
        self.page.session.set("titlebar", self.window.titlebar)

        self.page.on_keyboard_event = self.handle_keyboard_events

        dummy_kb_receiver = TextField(width=0, height=0, autofocus=True)

        self.page.add(dummy_kb_receiver)
        self.page.spacing = 0
    
    def handle_keyboard_events(self, event: KeyboardEvent):
        if (event.key == "\\" and event.ctrl):
            self.sbh_state.invert(event)
    
    def update_icon_size(self):
        width = self.mq_state.size[0]
        scale = width / 1011

        self.window.start_view.widget_scale = scale
        self.window.start_view.build()
        self.window.start_view.update()