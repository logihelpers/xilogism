from flet import *
from presentation.states.expand_canvas_state import ExpandCanvasState
from presentation.states.accent_color_state import AccentColorState

class ExpandButton(Container):
    def __init__(self, top, right):
        super().__init__(top=top, right=right)

        self.ac_state = AccentColorState()

        self.ac_state.on_colors_updated = self.update_colors

        self.expand_state = ExpandCanvasState()

        self.content = Image(
            src="/icons_light/full-size.png",
            width=16,
            height=16
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
        self.expand_state.expand = not self.expand_state.expand
        self.content.src = "/icons_light/shrink.png" if self.expand_state.expand else "/icons_light/full-size.png"
        self.content.update()

    def update_colors(self):
        colors = self.ac_state.color_values
        self.bgcolor = colors["accent_color_1"]
        self.border = border.all(1, colors["divider_color"])