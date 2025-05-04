from presentation.states.animation_disable_state import AnimationDisableState
from presentation.states.dialogs_state import DialogState, Dialogs
from flet import *

from presentation.controllers.controller import Controller, Priority

class AnimationDisableController(Controller):
    priority = Priority.SETTINGS_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.anim_state = AnimationDisableState()
        self.anim_state.on_change = self.change_active
        self.dia_state = DialogState()
        self.dia_state.on_done_build = self.update_view

        if not self.page.client_storage.contains_key("enable_anim"):
            self.page.client_storage.set("enable_anim", True)

        enable_anim = bool(self.page.client_storage.get("enable_anim"))
        try:
            self.anim_state.state = enable_anim
        except ValueError:
            self.anim_state.state = True
            self.page.client_storage.set("enable_anim", True)
    
    def update_view(self):
        if self.dia_state.done_build == Dialogs.SETTINGS:
            self.anim_state.state = bool(self.page.client_storage.get("enable_anim"))

    def change_active(self):
        state: bool = self.anim_state.state
        self.page.client_storage.set("enable_anim", state)