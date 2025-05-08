from flet import *
from presentation.states.bom_state import BOMState
from presentation.states.accent_color_state import AccentColorState
from presentation.states.dark_mode_state import *

class GenerateBOMButton(Container):
    def __init__(self):
        super().__init__()

        self.bom_state = BOMState()
        self.ac_state = AccentColorState()
        self.dm_state = DarkModeState()

        self.content = Image(
            src="/icons_light/generate_bom.png",
            width=24,
            height=24
        )

        self.scale = 1
        self.animate_scale=animation.Animation(250, AnimationCurve.BOUNCE_OUT)
        self.rotate=transform.Rotate(0, alignment.center)
        self.animate_rotation=animation.Animation(250, AnimationCurve.EASE_IN_OUT)
        self.padding = 8
        self.border_radius = 16
        self.on_animation_end=self._rerotate
        self.on_click = self.update_expand
        self.on_hover=self._hover
    
    def _hover(self, event: ControlEvent):
        button: FilledButton = event.control

        hovered = event.data == "true"

        button.rotate.angle = 3.14159 / 6 if hovered else 0
        button.scale = 1.25 if hovered else 1
        button.bgcolor = "#4d191f51" if hovered else "#00191f51"
        button.update()
    
    def _rerotate(self, event: ControlEvent):
        button: FilledButton = event.control

        button.rotate.angle = 0
        button.scale = 1
        button.update()
    
    def update_expand(self, _):
        self.bom_state.show_bom = True
    
    def did_mount(self):
        super().did_mount()
        self.ac_state.on_colors_updated = self.update_colors
    
    def update_colors(self):
        colors = self.ac_state.color_values
        dark_mode = self.dm_state.active == DarkModeScheme.DARK
        self.bgcolor = colors["options_bgcolor"]
        self.content.src = "/icons_light/generate_bom.png" if not dark_mode else "/icons_dark/generate_bom.png"
        def _hover(event: ControlEvent):
            button: Container = event.control
            hovered = event.data == "true"
            button.rotate.angle = 3.14159 / 6 if hovered else 0
            button.scale = 1.25 if hovered else 1
            button.bgcolor = colors["hover_bgcolor"] if hovered else colors["options_bgcolor"]
            button.update()
        self.on_hover = _hover
        self.update()