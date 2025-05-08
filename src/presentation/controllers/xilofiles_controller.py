from presentation.states.xilofile_state import XiloFileState
from presentation.states.editor_content_state import EditorContentState, CodeState
from presentation.states.active_sidebar_button_state import ActiveSideBarButtonState
from presentation.states.auth_state import AuthState
from presentation.states.accent_color_state import AccentColorState
from presentation.states.dark_mode_state import *
from presentation.controllers.editor_view_fonts_controller import EditorViewFontsController
from presentation.controllers.expand_canvas_controller import ExpandCanvasController
from presentation.controllers.editor_content_state_controller import EditorContentStateController
from presentation.views.widgets.sidebar.sidebar import *
from presentation.views.editor_view import EditorView
from presentation.views.open_existing_view import OpenExistingView
from presentation.views.widgets.existing_view.local_button import LocalButton
from presentation.views.widgets.existing_view.pinned_button import PinnedButton
from presentation.views.window_view import WindowView
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import io
from googleapiclient.http import MediaIoBaseDownload

from models.xilofile_model import XiloFile, StorageType

from xilowidgets import Switcher
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
        self.auth_state = AuthState()
        self.ac_state = AccentColorState()
        self.dm_state = DarkModeState()
        self.dm_state.on_change = self.update_icons_color

        window: WindowView = self.page.session.get("window")
        self.switcher: Switcher = window.switcher
        self.sidebar: SideBar = self.page.session.get("sidebar")
        self.existing_view: OpenExistingView = window.open_view

        try:
            self.pinned_list: list = list(self.page.client_storage.get("pinned_files"))
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
        if xilofile.storage_type == StorageType.LOCAL:
            with open(xilofile.path, "r", encoding="utf-8") as f:
                json_file = json.load(f)

                self.create_view(json_file, xilofile)
        else:
            service = build('drive', 'v3', credentials=self.auth_state.google_creds)
            request = service.files().get_media(fileId = xilofile.path)
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()
            
            file_content.seek(0)

            json_file = json.loads(file_content.read().decode())
            self.create_view(json_file, xilofile)
    
    def create_view(self, json_file, xilofile: XiloFile):
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

            pinned_button = PinnedButton(
                title=xilofile.title,
                thumbnail=xilofile.thumbnail,
                date=xilofile.date,
                on_press=lambda e: setattr(self.asb_state, 'active', e.control.title),
            )
            
            self.existing_view.pinned_list.controls.append(pinned_button)
            self.existing_view.pinned_list.update()
        else:
            if xilofile.storage_type == StorageType.LOCAL:
                self.sidebar.local_files.controls.append(button)
                self.sidebar.local_files.update()
            else:
                self.sidebar.gdrive_files.controls.append(button)
                self.sidebar.gdrive_files.update()
                return

            local_button = LocalButton(
                title=xilofile.title,
                path=xilofile.path,
                date=xilofile.date,
                on_press=lambda e: setattr(self.asb_state, 'active', e.control.title),
            )
            
            self.existing_view.local_list.controls.append(local_button)
            self.existing_view.local_list.update()
    
        editor.update_colors()

        self.update_icons_color()
    
    def update_icons_color(self):
        dark_mode = self.dm_state.active == DarkModeScheme.DARK
        button: SideBarButton = None
        for name, button in SideBarButton.refs:
            button._button_image.src = button.path if not dark_mode else button.path.replace("light", "dark")
            button._button_image.update()
            button.update_colors()