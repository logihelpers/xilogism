from presentation.states.left_handed_state import LeftHandedState
from presentation.views.widgets.settings.settings_image_button import SettingsImageButton
from presentation.states.dialogs_state import Dialogs, DialogState
from presentation.views.window_view import WindowView
from presentation.states.accent_color_state import AccentColorState
from xilowidgets import Revealer

from flet import *

from presentation.controllers.controller import Controller, Priority

class LeftHandedController(Controller):
    group_id: str = "sidebar_pos"
    priority = Priority.SETTINGS_BOUND
    old_active: bool = None
    def __init__(self, page: Page):
        self.page = page

        self.lh_state = LeftHandedState()
        self.lh_state.on_change = self.change_state
        self.dia_state = DialogState()
        self.dia_state.on_done_build = self.update_view
        self.ac_state = AccentColorState()

        self.window: WindowView = self.page.session.get("window")

        if not self.page.client_storage.contains_key("left_handed"):
            self.page.client_storage.set("left_handed", False)

        left_handed = bool(self.page.client_storage.get("left_handed"))
        try:
            self.lh_state.state = left_handed
        except ValueError:
            self.lh_state.state = False
            self.page.client_storage.set("left_handed", False)
    
    def update_view(self):
        if self.dia_state.done_build == Dialogs.SETTINGS:
            self.old_active = None
            self.lh_state.state = bool(self.page.client_storage.get("left_handed"))

    def change_state(self):
        active: bool = self.lh_state.state

        if self.old_active == active:
            return
        
        self.old_active = active

        middle_widget = self.window.controls[1]
        last_widget = self.window.controls[2]

        if active and isinstance(middle_widget, Revealer):
            self.window.controls.append(self.window.controls.pop(1))
            self.window.sidebar.border = border.only(left=BorderSide(1, self.ac_state.color_values["divider_color"]))
        elif not active and isinstance(last_widget, Revealer):
            self.window.controls.insert(1, self.window.controls.pop())
            self.window.sidebar.border = border.only(right=BorderSide(1, self.ac_state.color_values["divider_color"]))
        self.window.update()

        try:
            button: SettingsImageButton = None
            for button in SettingsImageButton.refs[self.group_id]:
                if (button.text == "Left-Handed" and active) or (button.text == "Default" and not active):
                    button.active = True

                    button.bgcolor = "#4d191f51"
                    button.check_box.bgcolor = "#af191f51"
                    button.border = border.all(1, "#191f51")
                    button.label.weight = FontWeight.BOLD
                else:
                    button.active = False

                    button.bgcolor = "#00191f51"
                    button.check_box.bgcolor = "#00191f51"
                    button.border = border.all(1, "#006b6b6b")
                    button.label.weight = FontWeight.NORMAL

                button.update()
        except:
            pass

        self.page.client_storage.set("left_handed", active)