from flet import SnackBar, Text, ElevatedButton, Icons, Page
from presentation.states.drive_state import DriveState

class GoogleDriveController:
    def __init__(self, page: Page):
        self.page = page
        self.creds = None
        self.state = DriveState()
        self.state.on_change = self.on_files_change
        self.file_buttons = []

    def on_files_change(self):
        self.file_buttons.clear()
        for file in self.state.files:
            btn = ElevatedButton(
                text=file["name"],
                icon=Icons.DESCRIPTION,
                on_click=lambda e, file_id=file["id"]: self._open_file(file_id)
            )
            self.file_buttons.append(btn)
        if self.page:
            self.page.update()

    def get_file_buttons(self):
        return self.file_buttons

    def _open_file(self, file_id):
        print(f"Open file from Drive: {file_id}")
        self.page.open(SnackBar(Text(f"Opening file {file_id}...")))
        self.page.update()
