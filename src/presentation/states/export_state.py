from flet import *
from enum import Enum

from utils.singleton import Singleton

class FileFormat:
    PDF = 0
    PNG = 1
    DOCX = 2
    RAW_PNG = 3

class ExportState(metaclass=Singleton):
    def __init__(self):
        self._format: FileFormat = FileFormat.PDF
        self._margin: bool = True
        self._titleblock_enable: bool = True
        self._proj_name: str = "Sample"
        self._creator: str = "Xilogism"
        self._date: str = "04/07/2025"

    @property
    def format(self) -> FileFormat:
        return self._format

    @format.setter
    def format(self, format: FileFormat):
        self._format = format
        self.on_change()

    @property
    def margin(self) -> bool:
        return self._margin

    @margin.setter
    def margin(self, margin: bool):
        self._margin = margin
        self.on_change()

    @property
    def titleblock_enable(self) -> bool:
        return self._titleblock_enable

    @titleblock_enable.setter
    def titleblock_enable(self, enable: bool):
        self._titleblock_enable = enable
        self.on_change()

    @property
    def proj_name(self) -> str:
        return self._proj_name

    @proj_name.setter
    def proj_name(self, name: str):
        self._proj_name = name
        self.on_change()

    @property
    def creator(self) -> str:
        return self._creator

    @creator.setter
    def creator(self, creator: str):
        self._creator = creator
        self.on_change()

    @property
    def date(self) -> str:
        return self._date

    @date.setter
    def date(self, date: str):
        self._date = date
        self.on_change()

    def on_change(self):
        pass

    def export(self):
        self.on_export()
    
    def on_export(self):
        pass

    def print(self):
        self.on_print()
    
    def on_print(self):
        pass