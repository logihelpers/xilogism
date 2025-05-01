from presentation.states.active_sidebar_button_state import *
from presentation.states.active_file_state import ActiveFileState
from presentation.states.editor_content_state import EditorContentState
from presentation.states.new_save_state import NewSaveState
from presentation.states.dialogs_state import DialogState, Dialogs

from presentation.views.widgets.sidebar.button import SideBarButton
from presentation.views.widgets.titlebar import TitleBar

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
        self.ns_state.on_change = lambda: setattr(self, 'save_state_changed', True)

        self.titlebar: TitleBar = self.page.session.get("titlebar")
    
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