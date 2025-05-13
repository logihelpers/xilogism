from typing import Optional, List
from models.xilofile_model import XiloFile, StorageType
from utils.singleton import Singleton
from pathlib import Path
from datetime import datetime
from presentation.states.xilofile_state import XiloFileState
from presentation.states.auth_state import AuthState
from presentation.states.drive_state import DriveState
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload
import base64
import os
import json

class Files(metaclass=Singleton):
    all_files: List[XiloFile] = []

    def __init__(self):
        self.xf_state = XiloFileState()
        self.auth_state = AuthState()
        self.drive_state = DriveState()
        self.auth_state.on_creds_set = self.retrieve_files_gdrive
        self.drive_state.on_change = self.process_gdrive

    def retrieve_files_local(self):
        Files.all_files.clear()
        home_dir = Path.home()
    
        # Define directories to scan
        directories = [
            home_dir / "Downloads",
            home_dir / "Documents",
            home_dir / "Desktop",
        ]

        for directory in directories:
            if directory.exists() and directory.is_dir():
                for file_path in directory.rglob("*.xlg"):
                    self.process_local(str(file_path))
                self.xf_state.files = Files.all_files
            else:
                print(f"Directory not found: {directory}")
    
    def append_file(self, file_path: Path):
        xilofile = self.process_local(str(file_path))
        self.xf_state.appended_file = xilofile
    
    def process_local(self, file_path: str):
        with open(file_path, "r") as file:
            file = json.load(file)
            stats = os.stat(file_path)

            filename = file['name']
            base64_string = None
            if os.path.exists(f"thumbnails/thumbnail_{filename}.png"):
                with open(f"thumbnails/thumbnail_{filename}.png", "rb") as image_file:
                    base64_string = base64.b64encode(image_file.read()).decode("utf-8")

            xilofile = XiloFile(
                title=filename,
                path=file_path,
                date=datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                size=stats.st_size,
                storage_type=StorageType.LOCAL,
                thumbnail=base64_string
            )

            self.append(xilofile)
            return xilofile

    def retrieve_files_gdrive(self):
        page_size = 1000
        try:
            service = build('drive', 'v3', credentials=self.auth_state.google_creds)
            res = service.files().list(
                pageSize=page_size,
                fields="files(id, name, mimeType)"
            ).execute()

            files = res.get('files', [])
            xlg_files = [f for f in files if f["name"].endswith(".xlg")]
            self.drive_state.files = xlg_files
            return xlg_files
        except Exception as e:
            print(f"[Drive File List Error] {e}")
            return []
    
    def process_gdrive(self):
        for file in self.drive_state.files:
            service = build('drive', 'v3', credentials=self.auth_state.google_creds)
            request = service.files().get_media(fileId = file["id"])
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()
            
            file_content.seek(0)

            json_file = json.loads(file_content.read().decode())

            xilofile = XiloFile(
                title=json_file["name"],
                path=file["id"],
                date="N/A",
                size="N/A",
                storage_type=StorageType.GDRIVE
            )

            self.append(xilofile)
            self.xf_state.appended_file = xilofile

    def append(self, file: XiloFile):
        Files.all_files.append(file)

    @staticmethod
    def parse(title: str) -> Optional['XiloFile']:
        for file in Files.all_files:
            if file.title == title:
                return file
        return None