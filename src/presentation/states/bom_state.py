from flet import *
from enum import Enum

from services.singleton import Singleton

class BOMState(metaclass=Singleton):
    def __init__(self):
        self._counts: dict = {}
        self._show_bom: bool = False

    @property
    def counts(self) -> dict:
        return self._counts

    @counts.setter
    def counts(self, counts: dict):
        self._counts = counts
        self.on_count_change()

    def on_count_change(self):
        pass
    
    @property
    def show_bom(self) -> bool:
        return self._show_bom

    @show_bom.setter
    def show_bom(self, show_bom: bool):
        self._show_bom = show_bom
        self.on_bom_request()
    
    def on_bom_request(self):
        pass