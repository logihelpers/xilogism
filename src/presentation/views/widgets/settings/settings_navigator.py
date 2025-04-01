from flet import *
from presentation.views.widgets.settings.navigator_button import NavigatorButton, Position

class SettingsNavigator(Container):
    def __init__(self):
        super().__init__()

        if len(NavigatorButton.refs) > 0:
            NavigatorButton.refs = []

        self.alignment = alignment.center
        self.padding = 16

        self.content = Row(
            controls = [
                NavigatorButton("Appearance", Position.START),
                NavigatorButton("Accessibility", Position.MIDDLE),
                NavigatorButton("Language", Position.END)
            ],
            spacing = 0,
            alignment=MainAxisAlignment.CENTER
        )
    
    def build(self):
        super().build()

        first_button: NavigatorButton = NavigatorButton.refs[0]
        first_button.bgcolor = "#d9fafafa"
        first_button.shadow=BoxShadow(0.1, 2, "#191f51")
        
        match first_button.pos:
            case Position.START:
                first_button.border = border.all(1, "#191f51")
                first_button.border_radius = border_radius.only(4, 0, 4, 0)
            case Position.MIDDLE:
                first_button.border= border.symmetric(vertical = BorderSide(1, "#191f51"))
            case Position.END:
                first_button.border=border.all(1, "#191f51")
                first_button.border_radius=border_radius.only(0, 4, 0, 4)