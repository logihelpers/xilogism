from presentation.states.title_button_state import TitleButtonState
from presentation.states.active_file_state import ActiveFileState
from presentation.states.editor_content_state import EditorContentState
from presentation.views.widgets.sidebar.button import SideBarButton
from presentation.controllers.editor_content_state_controller import EditorContentStateController
from presentation.states.active_sidebar_button_state import ActiveSideBarButtonState
from presentation.states.render_state import RenderState
from presentation.views.editor_view import EditorView

from presentation.views.window_view import WindowView
from presentation.controllers.controller import Controller, Priority

from flet import *
import json

class TitleChangeController(Controller):
    old_active: str = ""
    priority = Priority.LAST
    def __init__(self, page: Page):
        self.page = page

        self.af_state = ActiveFileState()
        self.asbb_state = ActiveSideBarButtonState()
        self.tb_state = TitleButtonState()
        self.ec_state = EditorContentState()
        self.render_state = RenderState()
        self.tb_state.on_title_change = self.process_title_change

        self.window: WindowView = self.page.session.get("window")

    def process_title_change(self):
        self.old_active = self.af_state.active.title
        new = self.tb_state.title

        if self.old_active == new.strip():
            return
        
        self.af_state.active.title = new

        button_name: str = None
        button: SideBarButton = None
        for index, (button_name, button) in enumerate(SideBarButton.refs):
            if button_name == self.old_active:
                button.label = new
                button.button_label.value = new
                button.button_label.update()

                SideBarButton.refs[index] = (new, button)
                break

        
        if self.old_active in EditorContentStateController.instances:
            controller = EditorContentStateController.instances.pop(self.old_active)
            controller.key_name = new
            EditorContentStateController.instances[new] = controller

        self.window.titlebar.filename_tf.value = new
        self.window.titlebar.filename_tf.update()
        
        instance: EditorView = None
        for instance in EditorView.instances:
            if instance.key_name == self.old_active:
                instance.key_name = new
                break

        self.ec_state.content = ({new: self.ec_state.content[self.old_active]}, True)
        self.ec_state.code_state = ({new: self.ec_state.code_state[self.old_active]}, True)
        del self.ec_state.content[self.old_active]
        del self.ec_state.code_state[self.old_active]

        try:
            self.render_state.input = ({new: self.render_state.input[self.old_active]}, True)
            del self.render_state.input[self.old_active]
        except:
            pass

        try:
            self.render_state.output = ({new: self.render_state.output[self.old_active]}, True)
            del self.render_state.output[self.old_active]
        except KeyError:
            pass

        try:
            self.render_state.image = ({new: self.render_state.image[self.old_active]}, True)
            del self.render_state.image[self.old_active]
        except KeyError:
            pass

        json_file: dict = {}
        json_file['name'] = new
        json_file['content'] = self.ec_state.content[new]
        with open(self.af_state.active.path, "w", encoding="utf-8") as f:
            json.dump(json_file, f, indent=4)
        
        self.old_active = new