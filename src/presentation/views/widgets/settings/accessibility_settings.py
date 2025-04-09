from flet import *
from presentation.views.widgets.settings.settings_image_button import SettingsImageButton
from presentation.states.animation_disable_state import AnimationDisableState
from presentation.states.color_blind_state import ColorBlindState, ColorModes
from presentation.states.dyslexia_friendly_state import DyslexiaFriendlyState
from presentation.states.left_handed_state import LeftHandedState

class AccessibilitySettings(Column):
    def __init__(self):
        super().__init__()

        self.ad_state = AnimationDisableState()
        self.cb_state = ColorBlindState()
        self.df_state = DyslexiaFriendlyState()
        self.lh_state = LeftHandedState()

        self.scroll=ScrollMode.ALWAYS
        self.expand=True
        self.spacing = 16

        self.controls = [
            Text("Dyslexia-Friendly Options", weight=FontWeight.BOLD),
            Row(
                spacing = 16,
                controls = [
                    SettingsImageButton("/mode_default.png", "Default", "dyslexia", 0.75, on_button_press=self.switch_readability),
                    SettingsImageButton("/mode_dyslexic_friendly.png", "Readable", "dyslexia", 0.75, on_button_press=self.switch_readability)
                ]
            ),
            Text("Vision Friendly Settings", weight=FontWeight.BOLD),
            Row(
                spacing = 16,
                wrap=True,
                controls = [
                    SettingsImageButton("/icons_light/color_settings_normal.png", "Default", "vision", 0.5, on_button_press=self.switch_vision),
                    SettingsImageButton("/icons_light/color_settings_high_contrast.png", "High-Contrast", "vision", 0.5, on_button_press=self.switch_vision),
                    SettingsImageButton("/icons_light/color_settings_deuteranopia.png", "Deuteranopia", "vision", 0.5, on_button_press=self.switch_vision),
                    SettingsImageButton("/icons_light/color_settings_protanopia.png", "Protanopia", "vision", 0.5, on_button_press=self.switch_vision),
                    SettingsImageButton("/icons_light/color_settings_tritanopia.png", "Tritanopia", "vision", 0.5, on_button_press=self.switch_vision),
                ]
            ),
            Text("Left-Handed Mode", weight=FontWeight.BOLD),
            Row(
                spacing = 24,
                controls = [
                    SettingsImageButton("/screenshot_light.png", "Default", "sidebar_pos", on_button_press=self.toggle_left_handed),
                    SettingsImageButton("/sidebar_right_light.png", "Left-Handed", "sidebar_pos", on_button_press=self.toggle_left_handed)
                ]
            ),
            Text("Animation Settings", weight=FontWeight.BOLD),
            Switch(
                label="Disable Animations:      ", 
                label_position=LabelPosition.LEFT,
                on_change=lambda e: setattr(self.ad_state, 'state', (e.data == "true"))
            ),
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
                    )
                ]
            )
        ]
    
    def switch_vision(self, event: ControlEvent):
        button: SettingsImageButton = event.control

        self.cb_state.active = ColorModes(button.text)
    
    def switch_readability(self, event: ControlEvent):
        button: SettingsImageButton = event.control

        self.df_state.active = (button.text == "Readable")
    
    def toggle_left_handed(self, event: ControlEvent):
        button: SettingsImageButton = event.control

        self.lh_state.state = (button.text == "Left-Handed")