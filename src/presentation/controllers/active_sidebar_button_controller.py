from presentation.states.active_sidebar_button_state import *
from presentation.states.active_file_state import ActiveFileState
from presentation.states.editor_content_state import EditorContentState
from presentation.states.new_save_state import NewSaveState
from presentation.states.dialogs_state import DialogState, Dialogs
from models.xilofile_model import StorageType
from presentation.views.widgets.sidebar.button import SideBarButton
from presentation.views.widgets.titlebar import TitleBar
from presentation.views.window_view import WindowView
from presentation.views.open_existing_view import OpenExistingView
from presentation.views.widgets.sidebar.sidebar import SideBar
from presentation.views.widgets.existing_view.local_button import LocalButton
from presentation.views.widgets.existing_view.pinned_button import PinnedButton

from data.files import Files

from flet import Page

from presentation.controllers.controller import Controller, Priority

class ActiveSideBarButtonController(Controller):
    priority = Priority.WIDGET_BOUND
    creating_new: bool = False
    save_state_changed: bool = False
    def __init__(self, page: Page):
        self.page = page

        self.asbb_state = ActiveSideBarButtonState()
        self.af_state = ActiveFileState()
        self.dia_state = DialogState()
        self.ns_state = NewSaveState()
        self.ec_state = EditorContentState()

        self.asbb_state.on_change = self.change_active
        self.asbb_state.on_pin = self.button_pinned
        self.ns_state.on_change = lambda: setattr(self, 'save_state_changed', True)

        self.titlebar: TitleBar = self.page.session.get("titlebar")
        self.window: WindowView = self.page.session.get("window")
        self.sidebar: SideBar = self.window.sidebar
        self.existing: OpenExistingView = self.window.open_view

        try:
            self.pinned_list = list(self.page.client_storage.get("pinned_files"))
        except:
            self.pinned_list = []
    
    def button_pinned(self):
        pinned_name = self.asbb_state.pin
        xilofile = Files.parse(pinned_name)

        if xilofile.storage_type == StorageType.GDRIVE:
            self.page.open(
                SnackBar(
                    Text("File cannot be pinned because it cannot be tracked..."),
                    duration=3000
                )
            )
            return

        if xilofile.path not in self.pinned_list: # ADD
            name: str = ""
            for index, (name, widget) in enumerate(SideBarButton.refs):
                if name == pinned_name:
                    SideBarButton.refs.pop(index)
                    if xilofile.storage_type == StorageType.LOCAL:
                        length_pinned = len(self.sidebar.pinned_files.controls)
                        SideBarButton.refs.insert(3 + length_pinned, (pinned_name, widget))
                        self.sidebar.local_files.controls.remove(widget)
                        self.sidebar.pinned_files.controls.append(widget)
                        view = self.window.switcher.controls.pop(index)
                        self.window.switcher.controls.insert(3 + length_pinned, view)
                        self.window.update()
                        break
            
            local_button: LocalButton = None
            for local_button in self.existing.local_list.controls:
                if local_button.title == pinned_name:
                    self.existing.pinned_list.controls.append(
                        PinnedButton(
                            thumbnail=xilofile.thumbnail,
                            title=xilofile.title,
                            date=xilofile.date,
                            on_press=lambda e: setattr(self.asbb_state, 'active', e.control.title)
                        )
                    )
                    self.existing.local_list.controls.remove(local_button)
                    break
            self.existing.update()
            
            self.pinned_list.append(xilofile.path)
            self.page.client_storage.set("pinned_files", self.pinned_list)
        else:
            name: str = ""
            for index, (name, widget) in enumerate(SideBarButton.refs):
                if name == pinned_name:
                    SideBarButton.refs.pop(index)
                    
                    if xilofile.storage_type == StorageType.LOCAL:
                        length_pinned = len(self.sidebar.pinned_files.controls)
                        length_local = len(self.sidebar.local_files.controls)
                        SideBarButton.refs.insert(2 + length_pinned + length_local, (pinned_name, widget))
                        if widget in self.sidebar.pinned_files.controls:
                            self.sidebar.pinned_files.controls.remove(widget)
                        self.sidebar.local_files.controls.append(widget)
                        view = self.window.switcher.controls.pop(3 + index)
                        self.window.switcher.controls.insert(3 + length_pinned + index, view)
                        self.window.update()
                        break
            
            pinned_button: PinnedButton = None
            for pinned_button in self.existing.pinned_list.controls:
                if pinned_button.title == pinned_name:
                    self.existing.local_list.controls.append(
                        LocalButton(
                            path=xilofile.path,
                            title=xilofile.title,
                            date=xilofile.date,
                            on_press=lambda e: setattr(self.asbb_state, 'active', e.control.title)
                        )
                    )
                    self.existing.pinned_list.controls.remove(pinned_button)
                    break
            self.existing.update()
            
            self.pinned_list.remove(xilofile.path)
            self.page.client_storage.set("pinned_files", self.pinned_list)
    
    def change_active(self):
        active: str = self.asbb_state.active

        name: str = ""
        widget: SideBarButton = None
        for name, widget in SideBarButton.refs:
            if name == active:
                if widget.active:
                    return
                
                if self.creating_new and self.ec_state.content["New"] != "":
                    self.dia_state.state = Dialogs.CREATE_NEW
                    while not self.save_state_changed:
                        self.creating_new = True
                    self.creating_new = False
                    self.ns_state.state = False
                    self.save_state_changed = False

                widget.bgcolor = "#4d191f51"
                widget.active = True

                if active == "Start" or active == "Open Xilogism" or active == "New Xilogism":
                    if active == "New Xilogism":
                        self.creating_new = True

                    self.titlebar.filename_tf.disabled = True
                    self.titlebar.filename_tf.suffix_icon = None
                    self.titlebar.filename_tf.border=InputBorder.NONE
                    self.titlebar.filename_tf.content_padding = None
                    self.titlebar.filename_tf.update()

                    self.af_state.active = active
                    widget.update()
                    continue
                else:
                    self.af_state.active = Files.parse(name)

                self.titlebar.filename_tf.disabled = False
                self.titlebar.filename_tf.border=InputBorder.OUTLINE
                self.titlebar.filename_tf.content_padding = padding.only(left=8, top=4, right=4, bottom=4)
                self.titlebar.filename_tf.suffix_icon = Icons.EDIT
                self.titlebar.filename_tf.update()
            else:
                if widget.bgcolor == "#d9d9d9":
                    continue

                widget.bgcolor = "#d9d9d9"
                widget.active = False

            try:
                widget.update()
            except:
                pass
        
        self.page.update()

        self.titlebar.filename_tf.value = active.upper()
        self.titlebar.filename_tf.update()