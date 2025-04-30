from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from flet import SnackBar, Text
from presentation.states.drive_state import DriveState
from presentation.controllers.controller import Priority

class GoogleDriveController:
    priority = Priority.SETTINGS_BOUND

    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    CREDENTIALS_FILE = 'src/assets/credentials.json'

    def __init__(self, target=None):
        self.page = target
        self.creds = None
        self.state = DriveState()
        self.state.on_change = self._on_files_change

    def login_google(self):
        flow = InstalledAppFlow.from_client_secrets_file(self.CREDENTIALS_FILE, self.SCOPES)
        self.creds = flow.run_local_server(port=0)
        self.page.snack_bar = SnackBar(Text("Google auth successful!"))
        self.page.snack_bar.open = True
        self.page.update()
        return self.creds

    def list_files(self, page_size=20):
        if not self.creds:
            raise Exception("Not authenticated to Google Drive")
        service = build('drive', 'v3', credentials=self.creds)
        res = service.files().list(pageSize=page_size, fields="files(id, name)").execute()
        files = res.get('files', [])
        self.state.files = files
        return files

    def _on_files_change(self):
        pass
