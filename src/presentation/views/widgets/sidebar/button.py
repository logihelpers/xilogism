from flet import *

class SideBarButton(FilledButton):
    refs: list = list()
    active: bool = False
    widget_scale: float = 1.0
    def __init__(self, path: str, label: str, on_button_press = None, on_pin = None):
        super().__init__()
        self.label = label
        self.path = path
        self.tooltip = path

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
        button: SideBarButton = event.control
        button.pin_button.visible = True if event.data == "true" else False

        button._button_image.rotate.angle = 3.14159 / 6 if event.data == "true" else 0
        button._button_image.update()

        if button.active:
            return

        button.bgcolor = "#4d191f51" if event.data == "true" else "#d9d9d9"
        button.update()
    
    def _revert_state(self, event: ControlEvent):
        image: Image = event.control
        image.rotate.angle = 0
        image.update()
    
    def on_button_press(self, event: ControlEvent):
        pass

    def _pin_hover(self, event: ControlEvent):
        button: Container = event.control
        button.bgcolor = "#26191f51" if event.data == "true" else "#00000000"
        button.update()