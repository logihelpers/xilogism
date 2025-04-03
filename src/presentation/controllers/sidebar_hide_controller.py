from presentation.states.sidebar_hide_state import *
from presentation.views.window_view import WindowView

from flet import Page

from presentation.controllers.controller import *

class SideBarHideController(Controller):
    priority = Priority.VIEW_BOUND
    def __init__(self, page: Page):
        self.page = page

        try:
            self.window: WindowView = self.page.session.get("window")
        except:
            print("Sidebar is not initalized. Cannot hide.")
            return

        self.sbh_state = SideBarHideState()

        self.sbh_state.on_change = self.hide_reveal_sidebar
    
    def hide_reveal_sidebar(self):
        state: SideBarState = self.sbh_state.state

        self.window.slidable_panel.content_hidden = state.value
        self.window.editor_view.hidden_options.content_hidden = not state.value

        self.window.titlebar.sidebar_hide_button.content.content = self.window.titlebar.sidebar_show_button_content if state.value else self.window.titlebar.sidebar_hide_button_content
        
        self.page.update()