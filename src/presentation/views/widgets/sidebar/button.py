from flet import *
from presentation.states.accent_color_state import AccentColorState
from presentation.states.dark_mode_state import *

class SideBarButton(FilledButton):
    refs: list = list()
    active: bool = False
    widget_scale: float = 1.0
    always_update_bg: bool = False
    def __init__(self, path: str, label: str, on_button_press = None, on_pin = None):
        super().__init__()
        self.label = label
        self.path = path
        self.tooltip = path

        self.dm_state = DarkModeState()
        self.ac_state = AccentColorState()
        self.ac_state.on_colors_updated = self.update_colors

        self.on_hover = self.__hover
        self.on_click = lambda event: self.on_button_press(event)
        self.on_button_press = on_button_press

        self.style = ButtonStyle(
            shape=ContinuousRectangleBorder()
        )
        
        self.bgcolor = "#d9d9d9"

        self._button_image = Image(
            src=self.path,
            width=24 * self.widget_scale,
            height=24 * self.widget_scale,
            rotate=transform.Rotate(0, alignment.center),
            animate_rotation=animation.Animation(250, AnimationCurve.EASE_IN_OUT),
            on_animation_end=self._revert_state
        )

        self.button_label = Text(
            self.label,
            weight=FontWeight.W_500,
            color="black",
            size=14 * self.widget_scale,
            no_wrap=False,
            expand=True,
            max_lines=1,
            overflow=TextOverflow.ELLIPSIS
        )

        self.pin_button = Container(
            content = Image(
                src="icons_light/pin.png",
                width=16,
                height=16
            ),
            width=24,
            height=24,
            visible=False,
            on_hover=self._pin_hover,
            shape=BoxShape.CIRCLE,
            padding=4,
            on_click=lambda e: on_pin(e.control.parent.parent.parent.label)
        )

        self.content = Container(
            content = Row(
                controls=[
                    self._button_image,
                    self.button_label,
                ],
                vertical_alignment=CrossAxisAlignment.CENTER
            ),
            padding=padding.symmetric(8 * self.widget_scale, 16 * self.widget_scale)
        )

        if label != "Start" and label != "New Xilogism" and label != "Open Xilogism":
            self.content.content.controls.append(self.pin_button)

        if (self.label, self) not in SideBarButton.refs:
            SideBarButton.refs.append((self.label, self))

        if self.label == "Start":
            self.active = True
            self.bgcolor = "#4d191f51"
    
    def __hover(self, event: ControlEvent):
        colors = self.ac_state.color_values
        try:
            button: SideBarButton = event.control
            button.pin_button.visible = True if event.data == "true" else False

            button._button_image.rotate.angle = 3.14159 / 6 if event.data == "true" else 0
            button._button_image.update()

            if button.active:
                return

            button.bgcolor = colors["button_bgcolor"] if event.data == "true" else colors["sidebar_color"]
            button.update()
        except:
            pass
    
    def _revert_state(self, event: ControlEvent):
        try:
            image: Image = event.control
            image.rotate.angle = 0
            image.update()
        except:
            pass
    
    def on_button_press(self, event: ControlEvent):
        pass

    def _pin_hover(self, event: ControlEvent):
        colors = self.ac_state.color_values
        try:
            button: Container = event.control
            button.bgcolor = colors["sidebar_color_deeper"] if event.data == "true" else "#00000000"
            button.update()
        except:
            pass
    
    def update_colors(self):
        colors = self.ac_state.color_values
        dark_mode = self.dm_state.active == DarkModeScheme.DARK
        self.button_label.color = colors["text_color"]
        self.pin_button.bgcolor = colors["button_bgcolor"]
        self.pin_button.content.src = "icons_light/pin.png" if not dark_mode else "icons_dark/pin.png"
        self.bgcolor = colors["sidebar_color"] if not self.active else colors["button_bgcolor"]
        self.update()