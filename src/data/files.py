from typing import Optional, List
from models.xilofile_model import XiloFile
from services.singleton import Singleton

class Files(metaclass=Singleton):
    all_files: List[XiloFile] = []

    def retrieve_files_local(self):
        pass

    def retrieve_files_gdrive(self):
        pass

    def append(self, file: XiloFile):
        self.all_files.append(file)

    @staticmethod
    def parse(title: str) -> Optional['XiloFile']:
        for file in Files.all_files:
            if file.title == title:
                return file
        return None