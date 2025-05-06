from flet import *
from presentation.views.dialogs.registration_dialog import RegistrationDialog
from presentation.views.widgets.sidebar.title import SideBarTitle
from presentation.views.widgets.sidebar.button import SideBarButton
from presentation.states.active_sidebar_button_state import ActiveSideBarButtonState
from presentation.states.auth_state import AuthState
from presentation.controllers.auth_controller import AuthController
from presentation.controllers.google_drive_controller import GoogleDriveController  # <-- import

class SideBar(Container):
    widget_scale: float = 1.0

    def __init__(self, page):
        super().__init__()
        self.page = page
        self.bgcolor = "#d9d9d9"
        self.width = 180 * self.widget_scale
        self.border = border.only(
            right=BorderSide(1, "#6d6d6d"),
            left=BorderSide(1, "#6d6d6d")
        )

        self.active_sidebar_button_state = ActiveSideBarButtonState()
        self.auth_state = AuthState()
        self.auth_state.register_listener(self._on_auth_change)

        self.drive_controller = GoogleDriveController(page=self.page)

        self._profile_menu = None
        self._file_picker = None

        self.user_image = Container(
            width=40 * self.widget_scale,
            height=40 * self.widget_scale,
            border_radius=50,
            clip_behavior=ClipBehavior.HARD_EDGE,
            content=Image(
                src="icons_light/guest_user.png",
                fit=ImageFit.COVER,
                width=40 * self.widget_scale,
                height=40 * self.widget_scale,
            )
        )

        self.user_text = Text(
            "Guest User",
            weight="bold",
            size=18 * self.widget_scale,
            color="black"
        )

        self.profile_button = FilledButton(
            bgcolor="#00191f51",
            content=Row(
                vertical_alignment=CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[self.user_image, self.user_text]
            ),
            on_click=self._on_profile_button_click
        )

        self.pinned_files = Column(expand=True, spacing=0, scroll=True)
        self.recent_files = Column(expand=True, spacing=0, scroll=True)
        self.gdrive_files = Column(expand=True, spacing=0, scroll=True)

        self.content = Column(
            controls=[
                WindowDragArea(
                    content=Container(
                        border=border.only(bottom=BorderSide(1, "#6b6b6b")),
                        padding=padding.all(16 * self.widget_scale),
                        content=self.profile_button
                    )
                ),
                Column(
                    controls=[
                        SideBarTitle("Home", is_home=True),
                        SideBarButton("icons_light/start.png", "Start", on_button_press=self._on_nav),
                        SideBarButton("icons_light/new.png", "New Xilogism", on_button_press=self._on_nav),
                        SideBarButton("icons_light/open.png", "Open Xilogism", on_button_press=self._on_nav),
                        SideBarTitle("Pinned"), self.pinned_files,
                        SideBarTitle("Recent Files"), self.recent_files,
                        SideBarTitle("Google Drive"), self.gdrive_files,
                    ],
                    expand=True, spacing=0, scroll=ScrollMode.HIDDEN
                )
            ],
            expand=True, spacing=0
        )

        self.load_gdrive_files()

    def _on_nav(self, e):
        self.active_sidebar_button_state.active = e.control.label

    def _on_profile_button_click(self, e):
        user = self.auth_state.user
        if not user:
            dlg = RegistrationDialog()
            dlg.page = self.page
            self.page.overlay.append(dlg)
            dlg.open = True
            dlg.update()
            self.page.update()
            return

        self._profile_menu = AlertDialog(
            modal=True,
            title=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Text("Profile"),
                    IconButton(icon=icons.CLOSE, tooltip="Close", on_click=self._close_profile_menu)
                ]
            ),
            content=Text(f"Signed in as {user.get('displayName')}"),
            actions=[
                TextButton("Change Picture", on_click=self._on_change_picture),
                TextButton("Logout", on_click=self._confirm_logout)
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=self._close_profile_menu
        )
        self.page.open(self._profile_menu)

    def _close_profile_menu(self, e):
        if self._profile_menu:
            self.page.close(self._profile_menu)
            self.page.update()

    def _on_change_picture(self, e):
        self._close_profile_menu(e)
        self._file_picker = FilePicker(on_result=self._on_file_picker_result)
        self.page.overlay.append(self._file_picker)
        self.page.update()
        self._file_picker.pick_files(
            allow_multiple=False,
            file_type=FilePickerFileType.IMAGE,
            allowed_extensions=["jpg", "jpeg", "png"]
        )

    def _on_file_picker_result(self, e):
        if e.files:
            file_path = e.files[0].path
            auth_ctrl = AuthController.get_instance() or AuthController(page=self.page)
            auth_ctrl.page = self.page
            auth_ctrl.upload_profile_picture(file_path)

        self.page.overlay.remove(self._file_picker)
        self.page.update()

    def _confirm_logout(self, e):
        self.auth_controller = AuthController.get_instance()
        self.auth_controller.logout()
        self.page.update()

    def refresh_user_profile(self):
        user = self.auth_state.user
        if user:
            self.user_text.value = user["displayName"]
            self.user_image.content = Image(
                src=user.get("photoUrl", "icons_light/guest_user.png"),
                fit=ImageFit.COVER
            )
        else:
            self.user_text.value = "Guest User"
            self.user_image.content = Image(
                src="icons_light/guest_user.png",
                fit=ImageFit.COVER
            )
        self.page.update()

    def _on_auth_change(self, user):
        self.refresh_user_profile()

    def load_gdrive_files(self):
        try:
            files = self.drive_controller.list_files()
            self.gdrive_files.controls.clear()
            for file in files:
                btn = SideBarButton(
                    icon="icons_light/file.png",
                    text=file["name"],
                    on_button_press=lambda e, fid=file["id"]: self._on_gdrive_file_click(fid)
                )
                self.gdrive_files.controls.append(btn)
            self.page.update()
        except Exception as e:
            print("[GDrive Load Error]", e)

    def _on_gdrive_file_click(self, file_id):
        print(f"Clicked Google Drive file: {file_id}")
