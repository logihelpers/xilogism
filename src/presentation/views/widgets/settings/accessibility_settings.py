from flet import *
from presentation.views.widgets.settings.settings_image_button import SettingsImageButton
from presentation.states.animation_disable_state import AnimationDisableState
from presentation.states.color_blind_state import ColorBlindState, ColorModes
from presentation.states.dyslexia_friendly_state import DyslexiaFriendlyState
from presentation.states.left_handed_state import LeftHandedState
from presentation.states.language_state import LanguageState

class AccessibilitySettings(Column):
    def __init__(self):
        super().__init__()

        self.ad_state = AnimationDisableState()
        self.ad_state.on_change = self.update_anim_disable_switch
        self.cb_state = ColorBlindState()
        self.df_state = DyslexiaFriendlyState()
        self.lh_state = LeftHandedState()
        self.lang_state = LanguageState()

        self.scroll=ScrollMode.ALWAYS
        self.expand=True
        self.spacing = 16

        self.anim_disable_switch = Switch(
            label="Animations:      ", 
            label_position=LabelPosition.LEFT,
            on_change=lambda e: setattr(self.ad_state, 'state', (e.data == "true"))
        )

        self.controls = [
            Text("Dyslexia-Friendly Options", weight=FontWeight.BOLD),
            Row(
                spacing = 16,
                # alignment=MainAxisAlignment.CENTER,
                expand = True,
                controls = [
                    SettingsImageButton("/mode_default.png", "Default", "dyslexia", 0.75, on_button_press=self.switch_readability),
                    SettingsImageButton("/mode_dyslexic_friendly.png", "Readable", "dyslexia", 0.75, on_button_press=self.switch_readability)
                ]
            ),
            Text("Left-Handed Mode", weight=FontWeight.BOLD),
            Row(
                spacing = 24,
                expand = True,
                controls = [
                    SettingsImageButton("/screenshot_light.png", "Default", "sidebar_pos", 0.75, on_button_press=self.toggle_left_handed),
                    SettingsImageButton("/sidebar_right_light.png", "Left-Handed", "sidebar_pos", 0.75, on_button_press=self.toggle_left_handed)
                ]
            ),
            Text("Animation Settings", weight=FontWeight.BOLD),
            self.anim_disable_switch,
            Text("Keyboard Shortcuts", weight=FontWeight.BOLD),
            DataTable(
                columns=[
                    DataColumn(
                        Text("Action")
                    ),
                    DataColumn(
                        Text("Shortcut")
                    )
                ],
                rows=[
                    DataRow(
                        cells=[
                            DataCell(content = Text("Hide Sidebar")),
                            DataCell(content = Text("Ctrl + \\"))
                        ]
                    ),
                    DataRow(
                        cells=[
                            DataCell(content = Text("Save Xilogism")),
                            DataCell(content = Text("Ctrl + S"))
                        ]
                    )
                ]
            )
        ]
    
    def did_mount(self):
        super().did_mount()
        self.lang_state.on_lang_updated = self.update_lang
    
    def switch_vision(self, event: ControlEvent):
        button: SettingsImageButton = event.control

        self.cb_state.active = ColorModes(button.text)
    
    def switch_readability(self, event: ControlEvent):
        button: SettingsImageButton = event.control

        self.df_state.active = (button.text == "Readable")
    
    def toggle_left_handed(self, event: ControlEvent):
        button: SettingsImageButton = event.control

        self.lh_state.state = (button.text == "Left-Handed")
    
    def update_anim_disable_switch(self):
        try:
            self.anim_disable_switch.value = self.ad_state.state
            self.anim_disable_switch.update()
        except:
            pass
    
    def update_lang(self):
        lang_values = self.lang_state.lang_values
        self.controls[0].value = lang_values["dyslexia_friendly_title"]
        self.controls[2].value = lang_values["left_handed_title"]
        self.controls[4].value = lang_values["animation_settings_title"]
        self.controls[5].label = lang_values["animations_label"]
        self.controls[6].value = lang_values["keyboard_shortcuts_title"]
        self.controls[1].controls[0].label.value = lang_values["default_dyslexia"]
        self.controls[1].controls[1].label.value = lang_values["readable_dyslexia"]
        self.controls[3].controls[0].label.value = lang_values["default_sidebar"]
        self.controls[3].controls[1].label.value = lang_values["left_handed_sidebar"]
        self.controls[7].rows[0].cells[0].content.value = lang_values["hide_sidebar_action"]
        self.controls[7].rows[0].cells[1].content.value = lang_values["hide_sidebar_shortcut"]
        self.controls[7].rows[1].cells[0].content.value = lang_values["save_xilogism_action"]
        self.controls[7].rows[1].cells[1].content.value = lang_values["save_xilogism_shortcut"]
        self.update()