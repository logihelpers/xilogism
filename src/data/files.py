from typing import Optional, List
from models.xilofile_model import XiloFile
from services.singleton import Singleton

class Files(metaclass=Singleton):
    all_files: List[XiloFile] = []

    def append(self, file: XiloFile):
        self.all_files.append(file)
        self.file_added(file)
    
    def file_added(self, file: XiloFile):
        pass

    @staticmethod
    def parse(title: str) -> Optional['XiloFile']:
        for file in Files.all_files:
            if file.title == title:
                return file
        return None