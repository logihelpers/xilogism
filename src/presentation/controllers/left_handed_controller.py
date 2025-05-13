from presentation.states.left_handed_state import LeftHandedState
from presentation.views.widgets.settings.settings_image_button import SettingsImageButton
from presentation.states.dialogs_state import Dialogs, DialogState
from presentation.states.accent_color_state import AccentColorState
from presentation.states.dark_mode_state import DarkModeScheme, DarkModeState
from presentation.views.window_view import WindowView
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
        self.dm_state = DarkModeState()
        self.ac_state.on_colors_updated = self.change_state
        self.dm_state.on_change = self.change_state

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

        middle_widget = self.window.controls[1]
        last_widget = self.window.controls[2]

        if active and isinstance(middle_widget, Revealer):
            self.window.controls.append(self.window.controls.pop(1))
        elif not active and isinstance(last_widget, Revealer):
            self.window.controls.insert(1, self.window.controls.pop())
        self.window.update()

        colors = self.ac_state.color_values
        dark_mode = self.dm_state.active == DarkModeScheme.DARK

        try:
            button: SettingsImageButton = None
            for button in SettingsImageButton.refs[self.group_id]:
                if (button.text == "Left-Handed" and active) or (button.text == "Default" and not active):
                    button.active = True

                    button.bgcolor = colors["button_bgcolor"].replace("4d", "00") if dark_mode else colors["button_bgcolor"]
                    button.check_box.bgcolor = colors["button_bgcolor"].replace("4d", "af") if not dark_mode else "white"
                    button.check_box.border = border.all(colors["button_bgcolor"].replace("4d", "73"))
                    button.border = border.all(1, colors["button_bgcolor"].replace("4d", ""))
                    button.label.weight = FontWeight.BOLD
                else:
                    button.active = False

                    button.bgcolor = "#00191f51"
                    button.check_box.bgcolor = "#00191f51"
                    button.check_box.border = border.all(colors["button_bgcolor"].replace("4d", "73"))
                    button.border = border.all(1, "#006b6b6b")
                    button.label.weight = FontWeight.NORMAL

                button.update()
        except:
            pass

        self.page.client_storage.set("left_handed", active)