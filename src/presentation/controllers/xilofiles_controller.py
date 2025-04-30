from presentation.states.xilofile_state import XiloFileState
from presentation.states.editor_content_state import EditorContentState, CodeState
from presentation.states.active_file_state import ActiveFileState
from presentation.states.active_sidebar_button_state import ActiveSideBarButtonState
from presentation.controllers.editor_view_fonts_controller import EditorViewFontsController
from presentation.controllers.expand_canvas_controller import ExpandCanvasController
from presentation.controllers.editor_content_state_controller import EditorContentStateController
from presentation.views.widgets.sidebar.sidebar import *
from xilowidgets import Switcher
from models.xilofile_model import XiloFile
from presentation.views.editor_view import EditorView
from typing import List
from flet import *
import json

from presentation.controllers.controller import Controller, Priority

class XiloFilesController(Controller):
    extra_controllers: list = []
    priority = Priority.NONE
    def __init__(self, page: Page):
        self.page = page

        self.xf_state = XiloFileState()
        self.xf_state.on_files_change = self.load_views
        self.asb_state = ActiveSideBarButtonState()
        self.ec_state = EditorContentState()

        self.switcher: Switcher = self.page.session.get("window").switcher
        self.sidebar: SideBar = self.page.session.get("sidebar")

    def load_views(self):
        xilo_files: List[XiloFile] = self.xf_state.files
        self.switcher.controls = self.switcher.controls[:3]
        self.sidebar.recent_files.controls = []
        XiloFilesController.extra_controllers = []
        for xilofile in xilo_files:
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
                    on_button_press=lambda e, name=name: setattr(self.asb_state, 'active', name)
                )

                self.sidebar.recent_files.controls.append(button)
                self.sidebar.recent_files.update()