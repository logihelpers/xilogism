from flet import *

from presentation.states.accent_color_state import AccentColorState
from presentation.states.language_state import LanguageState
from presentation.views.widgets.sidebar.title import SideBarTitle
from presentation.views.widgets.sidebar.button import SideBarButton
from presentation.states.active_sidebar_button_state import ActiveSideBarButtonState
from presentation.states.dialogs_state import *
from presentation.states.auth_state import AuthState
from presentation.controllers.google_drive_controller import GoogleDriveController

class SideBar(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.active = "Start"        
        self.bgcolor = "#d9d9d9"
        self.width = 180
        self.offset = transform.Offset(0, 0)
        self.padding = padding.all(0)
        self.margin = margin.all(0)
        self.border = border.only(
            right=BorderSide(1, color="#6d6d6d"), 
            left=BorderSide(1, color="#6d6d6d")
        )

        self.active_sidebar_button_state = ActiveSideBarButtonState()
        self.auth_state = AuthState()
        self.auth_state.on_user_change = self.refresh_user_profile
        self.dia_state = DialogState()
        self.ac_state = AccentColorState()
        self.ac_state.on_colors_updated = self.update_colors
        self.lang_state = LanguageState()
        self.lang_state.on_lang_updated = self.update_lang

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

        self.user_image = Image(
            src="icons_light/guest_user.png",
            width=32,
            height=32,
            border_radius=16
        )

        self.user_text = Text(
            "Guest User", 
            weight=FontWeight.W_700, 
            color="black", 
            size=16, 
            expand=True,
            text_align=TextAlign.CENTER
        )

        self.profile_button = FilledButton(
            bgcolor="#00191f51",
            content = Row(
                controls=[
                    self.user_image,
                    self.user_text
                ]
            ),
            on_click=self.on_profile_button_clicked
        )

        top_column = Column(
            controls = [
                WindowDragArea(
                    content=Container(
                        border=border.only(bottom=BorderSide(1, "#6b6b6b")),
                        padding=padding.all(16),
                        content=self.profile_button
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
        
        self.content = top_column
    
    def active_changed(self, event: ControlEvent):
        control: SideBarButton = event.control
        self.active_sidebar_button_state.active = control.label

    def update_colors(self):
        colors = self.ac_state.color_values
        self.bgcolor = colors["sidebar_color"]
        self.border = border.only(
            right=BorderSide(1, color=colors["divider_color"]), 
            left=BorderSide(1, color=colors["divider_color"])
        )

        self.update()

    def update_lang(self):
        lang_values = self.lang_state.lang_values
        for title in SideBarTitle.refs:
            if title == "Home":
                SideBarTitle.refs[title].content.controls[0].value = lang_values["home_title"]
            elif title == "Pinned":
                SideBarTitle.refs[title].content.controls[0].value = lang_values["pinned_title"]
            elif title == "Local Files":
                SideBarTitle.refs[title].content.controls[0].value = lang_values["local_files_title"]
            elif title == "Google Drive":
                SideBarTitle.refs[title].content.controls[0].value = lang_values["gdrive_title"]
        # Update Guest User text
        self.content.controls[0].content.content.content.controls[1].value = lang_values["guest_user"]
        self.update()

    def on_profile_button_clicked(self, _):
        user = self.auth_state.user
        if not user:
            self.dia_state.state = Dialogs.LOGIN
            return

        self.dia_state.state = Dialogs.PROFILE

    def refresh_user_profile(self):
        user = self.auth_state.user
        if user:
            self.user_text.value = user["displayName"]
            picture = user.get("photoUrl", "icons_light/guest_user.png")
            if picture == "":
                self.user_image.src = "icons_light/guest_user.png"
            else:
                self.user_image.src = user.get("photoUrl", "icons_light/guest_user.png")
        else:
            self.user_text.value = "Guest User"
            self.user_image.src = "icons_light/guest_user.png"
        self.page.update()
