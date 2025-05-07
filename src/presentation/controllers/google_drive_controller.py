from googleapiclient.discovery import build
from flet import SnackBar, Text, ElevatedButton, Icons, Page
from presentation.states.drive_state import DriveState

class GoogleDriveController:
    def __init__(self, page: Page):
        self.page = page
        self.creds = None  # Google OAuth credentials
        self.state = DriveState()
        self.state.on_change = self._on_files_change
        self.file_buttons = []

    def login_with_creds(self, creds):
        """
        Receive and store the Google credentials passed from AuthController.
        """
        self.creds = creds
        self.page.open(SnackBar(Text("Drive credentials authenticated!")))
        self.page.update()

        self.list_files()  # List files on Google Drive after authentication

    def list_files(self, page_size=20):
        if not self.creds:
            raise Exception("Not authenticated to Google Drive")

        try:
            service = build('drive', 'v3', credentials=self.creds)
            res = service.files().list(
                pageSize=page_size,
                fields="files(id, name, mimeType)"
            ).execute()

            files = res.get('files', [])
            xlg_files = [f for f in files if f["name"].endswith(".xlg")]
            self.state.files = xlg_files
            return xlg_files
        except Exception as e:
            print(f"[Drive File List Error] {e}")
            return []

    def _on_files_change(self):
        # Automatically rebuild UI elements (e.g., buttons) when files update
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
        # Returns a list of UI buttons for use in the sidebar
        return self.file_buttons

    def _open_file(self, file_id):
        # Placeholder: Add logic to open or download the file from Drive
        print(f"Open file from Drive: {file_id}")
        self.page.open(SnackBar(Text(f"Opening file {file_id}...")))
        self.page.update()
