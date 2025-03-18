import asyncio
from presentation.states.sidebar_hide_state import *
from presentation.views.widgets.sidebar.sidebar import SideBar

from flet import Page, transform

class SideBarHideController:
    def __init__(self, page: Page):
        self.page = page

        try:
            self.sidebar: SideBar = self.page.session.get("sidebar")
        except:
            print("Sidebar is not initalized. Cannot hide.")
            return
        
        self.sidebar.on_animation_end = self.hide_fully

        self.sbh_state = SideBarHideState()

        self.sbh_state.on_change = self.hide_reveal_sidebar
    
    async def hide_reveal_sidebar(self):
        state: SideBarState = self.sbh_state.state

        if state is SideBarState.SHOWN and not self.sidebar.visible:
            self.sidebar.visible = True
            self.sidebar.update()
            await asyncio.sleep(0.05)

        self.sidebar.offset = transform.Offset(-1, 0) if self.sidebar.offset.x == 0 else transform.Offset(0, 0)
        
        self.page.update()
    
    async def hide_fully (self, event):
        if self.sidebar.offset == transform.Offset(-1, 0):
            self.sidebar.visible = False if self.sidebar.visible else True
            self.sidebar.update()