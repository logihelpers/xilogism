from models.xilofile_model import XiloFile
from presentation.states.active_file_state import ActiveFileState

from presentation.views.window_view import WindowView
from presentation.views.widgets.sidebar.button import SideBarButton
from presentation.controllers.controller import Controller, Priority

from flet import *

class ActiveFileController(Controller):
    old_active: str = ""
    priority = Priority.NONE
    def __init__(self, page: Page):
        self.page = page

        self.af_state = ActiveFileState()

        self.window: WindowView = self.page.session.get("window")

        self.af_state.on_change = self.switch_file

    def switch_file(self):
        if type(self.af_state.active) is str:
            self.switch_main_views(self.af_state.active)
        elif type(self.af_state.active) is XiloFile:
            self.switch_to_editor_view(self.af_state.active)
    
    def switch_main_views(self, active_view: str):
        match active_view:
            case "Start":
                self.window.switcher.switch(0)
            case "Open Xilogism":
                self.window.switcher.switch(2)
            case "New Xilogism":
                self.window.switcher.switch(1)
            
        self.window.update()
    
    def switch_to_editor_view(self, file: XiloFile):
        name: str = ""
        for index, (name, _) in enumerate(SideBarButton.refs):
            if name == file.title:
                self.window.switcher.switch(index)