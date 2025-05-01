from presentation.views.window_view import WindowView
from presentation.states.sidebar_hide_state import *
from presentation.states.media_query_state import MediaQueryState
from presentation.states.active_sidebar_button_state import ActiveSideBarButtonState
from presentation.states.active_file_state import ActiveFileState
from presentation.states.editor_content_state import EditorContentState

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
        self.af_state = ActiveFileState()
        self.asbb_state = ActiveSideBarButtonState()
        self.ec_state = EditorContentState()
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
        elif (event.key == "S" and event.ctrl):
            if self.af_state.active == "New Xilogism" and self.ec_state.content["New"] != "":
                self.asbb_state.active = "Start"
    
    def update_icon_size(self):
        width = self.mq_state.size[0]
        scale = width / 1011

        self.window.start_view.logo_icon.width = 360 * scale
        self.window.start_view.logo_icon.height = 360 * scale
        self.window.start_view.logo_icon.update()