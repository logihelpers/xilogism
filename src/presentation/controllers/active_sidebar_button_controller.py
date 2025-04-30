from presentation.states.active_sidebar_button_state import *
from presentation.states.active_file_state import ActiveFileState

from presentation.views.widgets.sidebar.button import SideBarButton
from presentation.views.widgets.titlebar import TitleBar

from models.xilofile_model import XiloFile
from data.files import Files

from flet import Page

from presentation.controllers.controller import Controller, Priority

class ActiveSideBarButtonController(Controller):
    priority = Priority.WIDGET_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.asbb_state = ActiveSideBarButtonState()
        self.af_state = ActiveFileState()

        self.asbb_state.on_change = self.change_active

        self.titlebar: TitleBar = self.page.session.get("titlebar")
    
    def change_active(self):
        active: str = self.asbb_state.active

        self.titlebar.title = active.upper()
        self.titlebar.build()
        self.titlebar.update()

        name: str = ""
        widget: SideBarButton = None
        for index, (name, widget) in enumerate(SideBarButton.refs):
            if name == active:
                if widget.active:
                    return

                widget.bgcolor = "#4d191f51"
                widget.active = True

                if active == "Start" or active == "Open Xilogism" or active == "New Xilogism":
                    self.titlebar.filename_tf.disabled = True
                    self.titlebar.filename_tf.suffix_icon = None
                    self.titlebar.filename_tf.update()

                    self.af_state.active = active
                    widget.update()
                    continue
                else:
                    self.af_state.active = Files.parse(name)

                self.titlebar.filename_tf.disabled = False
                self.titlebar.filename_tf.suffix_icon = Icons.EDIT
                self.titlebar.filename_tf.update()
            else:
                if widget.bgcolor == "#d9d9d9":
                    continue

                widget.bgcolor = "#d9d9d9"
                widget.active = False

            widget.update()
        
        self.page.update()