from utils.singleton import Singleton
from typing import List, Optional
from models.font_model import Font, FontType

class Fonts(metaclass = Singleton):
    all_fonts: List[Font] = []
    def __init__(self):
        ui_fonts_list = [
            ("Product Sans", "/fonts/Product Sans Regular.ttf"),
            ("Inter", "/fonts/Inter.ttf"),
            ("OpenDyslexic", "/fonts/OpenDyslexic.otf")
        ]

        mono_fonts_list = [
            ("Iosevka", "/fonts/Iosevka.ttf"),
            ('Fira Code', "/fonts/FiraCode.ttf"),
            ("Hasklig", "/fonts/Hasklig.ttf"),
            ("IBM Plex Mono", "/fonts/IBMPlexMono.ttf"),
            ("Inconsolata", "/fonts/Iconsolata.ttf"),
            ("Fantasque Sans Mono", "/fonts/FantasqueSansMono.ttf"),
            ("JetBrains Mono", "/fonts/JetBrainsMono.ttf"),
            ("Roboto Mono", "/fonts/RobotoMono.ttf"),
            ("Source Code Pro", "/fonts/SourceCodePro.ttf"),
            ("Space Mono", "/fonts/SpaceMono.ttf"),
            ("OpenDyslexic Mono", "/fonts/OpenDyslexicMono.otf")
        ]

        self.add_fonts(ui_fonts_list, FontType.UI)
        self.add_fonts(mono_fonts_list, FontType.MONOSPACE)
    
    def add_fonts(self, fonts_list: list, type: FontType):
        for current_font, current_font_location in fonts_list:
            font = Font(current_font, type, current_font_location)
            Fonts.all_fonts.append(font)
    
    @staticmethod
    def parse(name: str) -> Optional[Font]:
        for font in Fonts.all_fonts:
            if font.font_name == name:
                return font
        return None