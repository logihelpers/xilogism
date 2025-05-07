from flet import *
from xilowidgets import XDialog
from presentation.states.dialogs_state import Dialogs, DialogState
from presentation.states.auth_state import AuthState
from presentation.states.language_state import LanguageState

class ProfileDialog(XDialog):
    FIELD_WIDTH: float = 300
    FIELD_RADIUS: float = 100

    def __init__(self):
        super().__init__()
        self.dia_state = DialogState()
        self.auth_state = AuthState()
        self.lang_state = LanguageState()

        self.profile_text = Text("Profile")
        self.icon_button = IconButton(icon=Icons.CLOSE, tooltip="Close", on_click=lambda e: setattr(self.dia_state, 'state', Dialogs.CLOSE))

        # Initialize image preview with current photoUrl or default

        picture = self.auth_state.user.get('photoUrl', '/user_icon.png')
        self.selected_image_path = None

        if picture == "":
            picture = "icons_light/guest_user.png"

        self.image_preview = Image(
            src=picture,
            width=90,
            height=90
        )

        self.modal = True
        self.title = Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                self.profile_text,
                self.icon_button
            ]
        )

        self.file_picker = FilePicker(on_result=self._on_file_picker_result)
        self.upload_picture_button = ElevatedButton(
            content=Text("UPLOAD PICTURE", color="white"),
            bgcolor="#1D2357",
            width=self.FIELD_WIDTH,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=self.FIELD_RADIUS),
                padding=padding.all(15)
            ),
            on_click=self._on_upload_picture_click
        )

        self.content = Container(
            padding=padding.only(0, 16),
            content=Column(
                spacing=10,
                controls=[
                    Row(controls=[self.image_preview], alignment=MainAxisAlignment.CENTER),
                    Text(
                        f"Signed in as {self.auth_state.user.get('displayName', 'User')}",
                        weight=FontWeight.BOLD,
                        size=16
                    ),
                    self.upload_picture_button
                ]
            )
        )

        self.actions = [
            TextButton("Logout", on_click=lambda e: self.auth_state.request_logout())
        ]
        self.actions_alignment = MainAxisAlignment.END
        self.on_dismiss = lambda e: setattr(self.dia_state, 'state', Dialogs.CLOSE)
    
    def did_mount(self):
        super().did_mount()
        self.page.overlay.append(self.file_picker)
        self.lang_state.on_lang_updated = self.update_lang
        self.auth_state.on_user_change = self._on_user_change
        self.update_lang()
    
    def _on_user_change(self):
        # Update image preview and display name when user data changes
        self.image_preview.src = self.auth_state.user.get('photoUrl', '/user_icon.png')
        self.content.content.controls[1].value = (
            self.lang_state.lang_values["signed_in_as"] + 
            f" {self.auth_state.user.get('displayName', 'User')}"
        )
        self.update()

    def _on_upload_picture_click(self, e):
        self.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["png", "jpg", "jpeg"]
        )

    def _on_file_picker_result(self, e: FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            self.selected_image_path = e.files[0].path
            self.image_preview.src = self.selected_image_path
            self.image_preview.update()
            # Automatically trigger upload after selection
            self.auth_state.request_update_profile(photo_path=self.selected_image_path)
        else:
            self.selected_image_path = None
            self.image_preview.src = self.auth_state.user.get('photoUrl', '/user_icon.png')
            self.image_preview.update()

    def update_lang(self):
        lang_values = self.lang_state.lang_values
        self.profile_text.value = lang_values["profile"]
        self.icon_button.tooltip = lang_values["close_button"]
        self.content.content.controls[1].value = (
            lang_values["signed_in_as"] + 
            f" {self.auth_state.user.get('displayName', 'User')}"
        )
        self.content.content.controls[2].content.value = lang_values["upload_picture_button"]
        self.actions[0].text = lang_values["logout"]
        self.update()