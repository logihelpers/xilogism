from flet import *

class SideBarButton(FilledButton):
        refs: list = list()
        active: bool = False
        widget_scale: float = 1.0
        def __init__(self, path: str, label: str, on_button_press = None):
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

            self.content = Container(
                content = Row(
                    controls=[
                        Image(
                            src=self.path,
                            width=16 * self.widget_scale,
                            height=16 * self.widget_scale
                        ),
                        Text(self.label, weight=FontWeight.W_500, color="black", size=14 * self.widget_scale, no_wrap=False)
                    ],
                    vertical_alignment=CrossAxisAlignment.CENTER
                ),
                padding=padding.symmetric(8 * self.widget_scale, 16 * self.widget_scale)
            )

            # SideBarButton.refs[self.label] = self
            SideBarButton.refs.append((self.label, self))

            if self.label == "Start":
                self.active = True
                self.bgcolor = "#4d191f51"
        
        def __hover(self, event: ControlEvent):
            button: SideBarButton = event.control
            if button.active:
                return

            button.bgcolor = "#4d191f51" if event.data == "true" else "#d9d9d9"
            button.update()
        
        def on_button_press(self, event: ControlEvent):
            pass

        @staticmethod
        def scale_all(scale: float):
            button: SideBarButton = None
            for name, button in SideBarButton.refs.items():
                button.widget_scale = scale
                button.build()
                button.update()