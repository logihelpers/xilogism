from flet import *

class SettingsImageButton(Container):
    active: bool = False
    refs: dict = {}
    def __init__(self, image: str = None, text: str = None, group_id: str= None, image_scale: float = 1.0):
        super().__init__()
        self.group_id = group_id
        self.text = text

        self.label = Text(
            value = text,
            visible = (text != None)
        )

        self.content = Column(
            controls = [
                Image(
                    src=image,
                    width=240 * image_scale,
                    height=135 * image_scale,
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