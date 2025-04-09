from presentation.states.animation_disable_state import AnimationDisableState

from flet import *

from presentation.controllers.controller import Controller, Priority

class AnimationDisableController(Controller):
    priority = Priority.SETTINGS_BOUND
    def __init__(self, page: Page):
        self.page = page

        self.anim_state = AnimationDisableState()

        self.anim_state.on_change = self.change_active

    def change_active(self):
        state: bool = self.anim_state.state

        print(state)