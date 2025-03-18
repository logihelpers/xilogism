from models.xilo_file import XiloFile
from presentation.states.active_file_state import ActiveFileState

from presentation.views.window_view import WindowView

from flet import *

class ActiveFileController:
    def __init__(self, page: Page):
        self.page = page

        self.af_state = ActiveFileState()

        self.af_state.on_change = self.switch_file
    
    def switch_file(self):
        if type(self.af_state.active) is str:
            self.switch_main_views(self.af_state.active)
        elif type(self.af_state.active) is XiloFile:
            print(self.af_state.active.title)
        # load file
    
    def switch_main_views(self, active_view: str):
        window: WindowView = self.page.session.get("window")
        
        match active_view:
            case "Start":
                window.switcher.content = window.start_view
                window.update()
            case "Open Xilogism":
                window.switcher.content = window.open_view
                window.update()
            case "New Xilogism":
                #display yung new view dito
                pass
            case _:
                print("HOW DID WE EVEN REACH THIS POINT???")