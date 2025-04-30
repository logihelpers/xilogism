from flet import *
from presentation.states.expand_canvas_state import ExpandCanvasState

class ExpandButton(Container):
    def __init__(self, top, right):
        super().__init__(top=top, right=right)

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
        self.on_click = lambda e: setattr(self.expand_state, 'expand', not self.expand_state.expand)
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