from .en import text_values as en_val
from .tl import text_values as tag_val
from .ceb import text_values as ceb_val
from .ja import text_values as jp_val
from .es import text_values as span_val

import flet as ft

class Language:
    instance = None
    def __init__(self, page: ft.Page):
        self.page = page
        if self.page.client_storage.get("lang") is None:
            self.page.client_storage.set("lang", "en")
        
        self.language: str = self.page.client_storage.get("lang")
    
    def get_text_values(self):
        match self.language:
            case "en":
                return en_val
            case "tag":
                return tag_val
            case "ceb":
                return ceb_val
            case "jp":
                return jp_val
            case "esp":
                return span_val
            case _:
                return None