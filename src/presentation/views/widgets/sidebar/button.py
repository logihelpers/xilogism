from flet import *

class SideBarButton(FilledButton):
        refs: dict = dict()
        active: bool = False
        widget_scale: float = 1.0
        def __init__(self, path: str, label: str, on_button_press = None):
            super().__init__()
            self.label = label
            self.path = path
            self.tooltip = path

            self.on_hover = self.__hover
            self.on_click = self._on_button_press
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
                        Text(self.label, weight=FontWeight.W_500, color="black", size=14 * self.widget_scale)
                    ],
                    vertical_alignment=CrossAxisAlignment.CENTER
                ),
                padding=padding.symmetric(8 * self.widget_scale, 16 * self.widget_scale)
            )

            SideBarButton.refs[self.label] = self

            if self.label == "Start":
                SideBarButton.refs["Start"].active = True
                SideBarButton.refs["Start"].bgcolor = "#4d191f51"
        
        def __hover(self, event: ControlEvent):
            button: SideBarButton = event.control
            if button.active:
                return

            button.bgcolor = "#4d191f51" if event.data == "true" else "#d9d9d9"
            button.update()
        
        def _on_button_press(self, event: ControlEvent):
            self.on_button_press(event)
        
        def on_button_press(self, event: ControlEvent):
            pass

        @staticmethod
        def scale_all(scale: float):
            button: SideBarButton = None
            for name, button in SideBarButton.refs.items():
                button.widget_scale = scale
                button.build()
                button.update()