from enum import Enum
from flet import *

from typing import List
from models.xilofile_model import XiloFile, StorageType
from services.singleton import Singleton

class XiloFileState(metaclass=Singleton):
    def __init__(self):
        self._files__: List[XiloFile] = []
    
    @property
    def files(self) -> List[XiloFile]:
        return self._files__
    
    @files.setter
    def files(self, files: List[XiloFile]):
        self._files__ = files
        self.on_files_change()
    
    def on_files_change(self):
        pass