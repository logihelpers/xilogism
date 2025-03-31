from flet import *
from slidablepanel import SlidablePanel

class AppearanceSettings(Column):
    def __init__(self):
        super().__init__()

        self.scroll=ScrollMode.ALWAYS
        self.expand=True
        self.spacing = 16

        self.dark_mode_options = SlidablePanel(
            orientation=SlidablePanel.Orientation.VERTICAL,
            content_length=200,
            content = Row(
                spacing = 24,
                controls = [
                    SettingsImageButton("/screenshot_light.png", "Default", "theme_mode"),
                    SettingsImageButton("/screenshot_dark.png", "Dark", "theme_mode")
                ]
            )
        )

        self.controls=[
            Text("Dark Mode", weight=FontWeight.BOLD),
            Column(
                spacing = 0,
                controls = [
                    self.dark_mode_options,
                    Container(
                        content = Switch(
                            label="Follow System Dark Mode Settings:      ", 
                            label_position=LabelPosition.LEFT,
                            on_change=self.hide_panel
                        ),
                        padding=padding.only(top = 8)
                    )
                ]
            ),
            Text("Accent Color", weight=FontWeight.BOLD),
            Row(
                controls = [
                    Container(content = Text(""), width=32, height=32, bgcolor=Colors.random(), border_radius=16, border=border.all(0.5, "black")),
                    Container(content = Text(""), width=32, height=32, bgcolor=Colors.random(), border_radius=16, border=border.all(0.5, "black")),
                    Container(content = Text(""), width=32, height=32, bgcolor=Colors.random(), border_radius=16, border=border.all(0.5, "black")),
                    Container(content = Text(""), width=32, height=32, bgcolor=Colors.random(), border_radius=16, border=border.all(0.5, "black")),
                    Container(content = Text(""), width=32, height=32, bgcolor=Colors.random(), border_radius=16, border=border.all(0.5, "black")),
                    Container(content = Text(""), width=32, height=32, bgcolor=Colors.random(), border_radius=16, border=border.all(0.5, "black"))
                ]
            ),
            Text("Sidebar Position", weight=FontWeight.BOLD),
            Row(
                spacing = 24,
                controls = [
                    SettingsImageButton("/screenshot_light.png", "Default", "sidebar_pos"),
                    SettingsImageButton("/sidebar_right_light.png", "Right", "sidebar_pos")
                ]
            ),
        ]
    
    def hide_panel(self, event: ControlEvent):
        self.dark_mode_options.content_hidden = True if event.data == "true" else False
        self.update()

class SettingsImageButton(Container):
    active: bool = False
    refs: dict = {}
    def __init__(self, image: str, text: str, group_id: str):
        super().__init__()
        self.group_id = group_id
        self.text = text

        self.label = Text(text)

        self.content = Column(
            controls = [
                Image(
                    src=image,
                    width=240,
                    height=135,
                    anti_alias=True
                ),
                self.label
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER
        )

        self.padding=16
        self.bgcolor="#006b6b6b"
        self.border=border.all(1, "#006b6b6b")
        self.border_radius=16
        self.on_hover = self._hover
        self.on_click = self.set_active
    
    def build(self):
        try:
            group: list = SettingsImageButton.refs[self.group_id]
            group.append(self)
        except KeyError:
            self.active = True
            self.bgcolor = "#1a191f51"
            self.border = border.all(1, "#191f51")
            self.label.weight = FontWeight.BOLD

            SettingsImageButton.refs[self.group_id] = [self]
        
        super().build()
    
    def _hover(self, event: ControlEvent):
        button: SettingsImageButton = event.control
        
        iter_button: SettingsImageButton = None
        for iter_button in SettingsImageButton.refs[button.group_id]:
            if iter_button.text == button.text:
                if button.active:
                    button.bgcolor = "#1a191f51"
                    button.border = border.all(1, "#191f51")
                    button.label.weight = FontWeight.BOLD
                else:
                    button.bgcolor = "#1a191f51" if event.data == "true" else "#006b6b6b"
                    button.border = border.all(1, "#191f51") if event.data == "true" else border.all(1, "#006b6b6b")
                    button.label.weight = FontWeight.BOLD if event.data == "true" else FontWeight.NORMAL
                button.update()
    
    def set_active(self, event: ControlEvent):
        button: SettingsImageButton = event.control
        
        iter_button: SettingsImageButton = None
        for iter_button in SettingsImageButton.refs[button.group_id]:
            if iter_button.text == button.text:
                if button.active:
                    return
                
