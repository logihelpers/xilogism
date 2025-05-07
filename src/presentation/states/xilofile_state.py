from enum import Enum
from flet import *

from typing import List
from models.xilofile_model import XiloFile, StorageType
from utils.singleton import Singleton

class XiloFileState(metaclass=Singleton):
    def __init__(self):
        self._files__: List[XiloFile] = []
        self._appended_file: XiloFile = None
    
    @property
    def files(self) -> List[XiloFile]:
        return self._files__
    
    @files.setter
    def files(self, files: List[XiloFile]):
        self._files__ = files
        self.on_files_change()
    
    def on_files_change(self):
        pass

    @property
    def appended_file(self):
        return self._appended_file
    
    @appended_file.setter
    def appended_file(self, file: XiloFile):
        self._appended_file = file
        self.on_file_appended(file)
    
    def on_file_appended(file: XiloFile):
        pass