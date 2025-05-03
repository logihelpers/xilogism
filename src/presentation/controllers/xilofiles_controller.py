from presentation.states.xilofile_state import XiloFileState
from presentation.states.editor_content_state import EditorContentState, CodeState
from presentation.states.active_sidebar_button_state import ActiveSideBarButtonState
from presentation.controllers.editor_view_fonts_controller import EditorViewFontsController
from presentation.controllers.expand_canvas_controller import ExpandCanvasController
from presentation.controllers.editor_content_state_controller import EditorContentStateController
from presentation.views.widgets.sidebar.sidebar import *
from xilowidgets import Switcher
from models.xilofile_model import XiloFile
from presentation.views.editor_view import EditorView
from presentation.views.open_existing_view import OpenExistingView
from presentation.views.widgets.existing_view.local_button import LocalButton
from presentation.views.window_view import WindowView
from typing import List
from flet import *
import json

from presentation.controllers.controller import Controller, Priority

class XiloFilesController(Controller):
    extra_controllers: list = []
    pinned_list: list = []
    priority = Priority.LAST
    already_loaded = False
    def __init__(self, page: Page):
        self.page = page

        self.xf_state = XiloFileState()
        self.xf_state.on_files_change = self.load_views
        self.xf_state.on_file_appended = self.append_view
        self.asb_state = ActiveSideBarButtonState()
        self.ec_state = EditorContentState()

        window: WindowView = self.page.session.get("window")
        self.switcher: Switcher = window.switcher
        self.sidebar: SideBar = self.page.session.get("sidebar")
        self.existing_view: OpenExistingView = window.open_view

        try:
            self.pinned_list: list = list(self.page.client_storage.get("pinned_files"))
            print(self.pinned_list)
        except:
            self.pinned_list = []
            self.page.client_storage.set("pinned_files", [])

    def load_views(self):
        if XiloFilesController.already_loaded:
            return

        xilo_files: List[XiloFile] = self.xf_state.files
        self.switcher.controls = self.switcher.controls[:3]
        self.sidebar.local_files.controls = []
        self.sidebar.pinned_files.controls = []
        XiloFilesController.extra_controllers = []
        self.page.update()
        for xilofile in xilo_files:
            self.append_view(xilofile)
        
        XiloFilesController.already_loaded = True
    
    def append_view(self, xilofile: XiloFile):
        with open(xilofile.path, "r", encoding="utf-8") as f:
            json_file = json.load(f)

            name = json_file['name']
            content = json_file['content']

            self.ec_state.content[name] = content
            self.ec_state.code_state[name] = CodeState.BLANK

            editor = EditorView(name)
            self.switcher.controls.append(editor)
            self.switcher.update()

            XiloFilesController.extra_controllers.append(EditorViewFontsController(self.page, editor))
            XiloFilesController.extra_controllers.append(ExpandCanvasController(self.page, editor))
            XiloFilesController.extra_controllers.append(EditorContentStateController(self.page, name, editor))

            button = SideBarButton(
                "icons_light/document.png",
                name,
                on_button_press=lambda e: setattr(self.asb_state, 'active', e.control.label),
                on_pin=lambda label: setattr(self.asb_state, 'pin', label)
            )
            button.tooltip = xilofile.path

            if xilofile.path in self.pinned_list:
                self.sidebar.pinned_files.controls.append(button)
                self.sidebar.pinned_files.update()
            else:
                self.sidebar.local_files.controls.append(button)
                self.sidebar.local_files.update()

                local_button = LocalButton(
                    title=xilofile.title,
                    path=xilofile.path,
                    date=xilofile.date,
                    on_press=lambda e: setattr(self.asb_state, 'active', e.control.title),
                )
                
                self.existing_view.local_list.controls.append(local_button)
                self.existing_view.local_list.update()