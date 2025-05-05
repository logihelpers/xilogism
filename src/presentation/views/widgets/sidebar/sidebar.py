from flet import *

from presentation.states.accent_color_state import AccentColorState

from presentation.views.widgets.sidebar.title import SideBarTitle
from presentation.views.widgets.sidebar.button import SideBarButton

from presentation.states.active_sidebar_button_state import ActiveSideBarButtonState
from presentation.states.dialogs_state import *

class SideBar(Container):
    widget_scale: float = 1.0
    old_scale: float = 1.0
    def __init__(self):
        super().__init__()
        self.active = "Start"        
        self.bgcolor = "#d9d9d9"
        self.width = 180 * self.widget_scale
        self.offset = transform.Offset(0, 0)
        self.padding = padding.all(0)
        self.margin = margin.all(0)
        self.border = border.only(
            right=BorderSide(1, color="#6d6d6d"),
        )

        self.active_sidebar_button_state = ActiveSideBarButtonState()
        self.dia_state = DialogState()
        self.ac_state = AccentColorState()
        self.ac_state.on_colors_updated = self.update_colors

        self.pinned_files = Column(
            expand=True,
            spacing=0,
            scroll=True,
            controls=[
            ]
        )

        self.local_files = Column(
            expand=True,
            spacing=0,
            scroll=True,
            controls = [
            ]
        )

        self.gdrive_files = Column(
            expand=True,
            spacing=0,
            scroll=True,
            controls = [
            ]
        )

        self.top_column = Column(
            controls = [
                WindowDragArea(
                    content=Container(
                        border=border.only(bottom=BorderSide(1, "#6b6b6b")),
                        padding=padding.all(16 * self.widget_scale),
                        content=FilledButton(
                            bgcolor="#00191f51",
                            content = Row(
                                controls=[
                                    Image(
                                        src="icons_light/guest_user.png",
                                        width=24 * self.widget_scale,
                                        height=24 * self.widget_scale
                                    ),
                                    Text("Guest User", weight=FontWeight.W_700, color="black", size=18 * self.widget_scale, expand=True)
                                ]
                            ),
                            on_click=lambda e: setattr(self.dia_state, 'state', Dialogs.REGISTER)
                        )
                    )
                ),
                Column(
                    controls = [
                        SideBarTitle("Home", is_home=True),
                        SideBarButton("icons_light/start.png", "Start", on_button_press=self.active_changed),
                        SideBarButton("icons_light/new.png", "New Xilogism", on_button_press=self.active_changed),
                        SideBarButton("icons_light/open.png", "Open Xilogism", on_button_press=self.active_changed),
                        SideBarTitle("Pinned"),
                        self.pinned_files,
                        SideBarTitle("Local Files"),
                        self.local_files,
                        SideBarTitle("Google Drive"),
                        self.gdrive_files
                    ],
                    expand=True,
                    spacing=0,
                    scroll=ScrollMode.HIDDEN,
                )
            ],
            expand=True,
            spacing=0
        )
        
        self.content = self.top_column
    
    def active_changed(self, event: ControlEvent):
        control: SideBarButton = event.control

        self.active_sidebar_button_state.active = control.label

    def update_colors(self):
        colors = self.ac_state.color_values
        self.top_column = colors["text_color"]
        self.bgcolor = colors["sidebar_color"]
        self.border = border.only(
            right=BorderSide(1, color=colors["divider_color"])
        )
        self.update()