from typing import Optional, List
from models.xilofile_model import XiloFile, StorageType
from services.singleton import Singleton
from pathlib import Path
from datetime import datetime
from presentation.states.xilofile_state import XiloFileState

import os
import json

class Files(metaclass=Singleton):
    all_files: List[XiloFile] = []

    def __init__(self):
        self.xf_state = XiloFileState()

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
    
    def process_local(self, file_path: str):
        with open(file_path, "r") as file:
            file = json.load(file)
            stats = os.stat(file_path)
            self.append(
                XiloFile(
                    title=file['name'],
                    path=file_path,
                    date=datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    size=stats.st_size,
                    storage_type=StorageType.LOCAL
                )
            )

    def retrieve_files_gdrive(self):
        pass

    def append(self, file: XiloFile):
        Files.all_files.append(file)

    @staticmethod
    def parse(title: str) -> Optional['XiloFile']:
        for file in Files.all_files:
            if file.title == title:
                return file
        return None