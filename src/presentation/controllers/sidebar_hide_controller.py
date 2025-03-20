import asyncio
from presentation.states.sidebar_hide_state import *
from presentation.views.window_view import WindowView

from flet import Page, transform

class SideBarHideController:
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

        self.window.slidable_panel.toggle_panel(state.value)
        
        self.page.update()