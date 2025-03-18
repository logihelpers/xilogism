from presentation.states.active_sidebar_button_state import *
from presentation.views.widgets.sidebar.button import SideBarButton

from models.xilo_file import XiloFile

from flet import Page

class ActiveSideBarButtonController:
    def __init__(self, page: Page):
        self.page = page

        self.asbb_state = ActiveSideBarButtonState()

        self.asbb_state.on_change = self.change_active
    
    def change_active(self):
        active: str = self.asbb_state.active

        name: str = ""
        widget: SideBarButton = None
        for name, widget in SideBarButton.refs.items():
            if name == active:
                widget.bgcolor = "#4d191f51"
                widget.active = True
                self.open_file(name)
                widget.update()
            else:
                if widget.bgcolor == "#d9d9d9":
                    continue

                widget.bgcolor = "#d9d9d9"
                widget.active = False
                widget.update()
        
        self.page.update()
    
    def open_file(self, filename: str):
        files: list = XiloFile.all_files
        file: XiloFile = None
        for file in files:
            if file.title == filename:
                # editor_view.load(file)
                return