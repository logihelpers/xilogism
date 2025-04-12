from flet import *

class SideBarTitle(Container):
    refs: dict = dict()
    widget_scale: float = 1.0
    def __init__(self, title: str, is_home: bool = False, on_menu_clicked = None):
        super().__init__()
        self.title = title
        self.is_home = is_home
        self.content = Row(
            controls = [
                Text(self.title, weight=FontWeight.W_700, color="black", size=14 * self.widget_scale, no_wrap=False),
                Container(
                    content=PopupMenuButton(
                        content = Image(
                            src="/icons_light/settings_more.png",
                            width=16 * self.widget_scale,
                            height=16 * self.widget_scale
                        ),
                        items = [
                            PopupMenuItem(
                                icon = Icons.HIDE_SOURCE,
                                text = "Hide Group"
                            ),
                            PopupMenuItem(
                                icon = Icons.RESTART_ALT,
                                text = "Reload"
                            )
                        ],
                        icon_color="black"
                    ),
                    offset=transform.Offset(-0.5, 0),
                    bgcolor="#00191f51",
                    visible = not self.is_home,
                    shape=BoxShape.CIRCLE,
                    on_hover=self._on_title_hover
                )
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN
        )
        self.padding = padding.only(
            8 * self.widget_scale, 
            12 * self.widget_scale, 
            8 * self.widget_scale, 
            8 * self.widget_scale
        )

        SideBarTitle.refs[self.title] = self
    
    def _on_title_hover(self, event: ControlEvent):
        control: SideBarTitle = event.control
        control.bgcolor = "#4d191f51" if event.data == "true" else "#d9d9d9"
        control.update()
    
    @staticmethod
    def scale_all(scale: float):
        button: SideBarTitle = None
        for name, button in SideBarTitle.refs.items():
            button.widget_scale = scale
            button.build()
            button.update()