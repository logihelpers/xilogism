from flet import *

from presentation.views.dialogs.registration_dialog import RegistrationDialog
from presentation.views.widgets.sidebar.title import SideBarTitle
from presentation.views.widgets.sidebar.button import SideBarButton

from presentation.states.active_sidebar_button_state import ActiveSideBarButtonState

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
        self.border=border.only(right=BorderSide(1, color="#6d6d6d"))

        self.active_sidebar_button_state = ActiveSideBarButtonState()

        self.pinned_files = Column(
            expand=True,
            spacing=0,
            scroll=True,
            controls=[
                SideBarButton("icons_light/logo.png", "Xilogism 1", on_button_press=self.active_changed),
                SideBarButton("icons_light/logo.png", "Logic Circuit 1", on_button_press=self.active_changed),
                SideBarButton("icons_light/logo.png", "Xilogism 2", on_button_press=self.active_changed),
            ]
        )

        self.recent_files = Column(
            expand=True,
            spacing=0,
            scroll=True,
            controls = [
                SideBarButton("icons_light/logo.png", "LCD - Lab 1", on_button_press=self.active_changed),
                SideBarButton("icons_light/logo.png", "LCD - Lab 2", on_button_press=self.active_changed),
                SideBarButton("icons_light/logo.png", "FMSS - CIRCUIT", on_button_press=self.active_changed)
            ]
        )

        self.gdrive_files = Column(
            expand=True,
            spacing=0,
            scroll=True,
            controls = [
                SideBarButton("icons_light/logo.png", "LCD - Lab 4", on_button_press=self.active_changed),
                SideBarButton("icons_light/logo.png", "LCD - Lab 5", on_button_press=self.active_changed),
                SideBarButton("icons_light/logo.png", "FM CIRCUITS", on_button_press=self.active_changed)
            ]
        )

        top_column = Column(
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
                                    Text("Guest User", weight=FontWeight.W_700, color="black", size=18 * self.widget_scale)
                                ]
                            ),
                            on_click=self.open_account_settings_dialog
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
                        SideBarTitle("Recent Files"),
                        self.recent_files,
                        SideBarTitle("Google Drive"),
                        self.gdrive_files
                    ],
                    expand=True,
                    spacing=0,
                    scroll=True
                )
            ],
            expand=True,
            spacing=0
        )
        
        self.content = top_column
    
    def active_changed(self, event: ControlEvent):
        control: SideBarButton = event.control

        self.active_sidebar_button_state.active = control.label
    
    def open_account_settings_dialog(self, event):
        dialog = RegistrationDialog()
        self.page.open(dialog)

    def scale_all(self, scale: float):
        if abs(scale - self.old_scale) > 0.05:
            self.widget_scale = scale
            self.build()
            self.update()

            SideBarTitle.scale_all(scale)
            SideBarButton.scale_all(scale)

            self.old_scale = scale