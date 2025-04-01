from services.singleton import Singleton
from typing import List
from models.font_model import Font, FontType

class Fonts(metaclass = Singleton):
    def __init__(self):
        self._all_fonts: List[Font] = []

        ui_fonts_list = [
            ("Product Sans", "/fonts/Product Sans Regular.ttf"),
            ("Inter", "/fonts/Inter.ttf")
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
            ("Space Mono", "/fonts/SpaceMono.ttf")
        ]

        dyslexic_fonts = []

        self.add_fonts(ui_fonts_list, FontType.UI)
        self.add_fonts(mono_fonts_list, FontType.MONOSPACE)
        self.add_fonts(dyslexic_fonts, FontType.DYSLEXIA_FRIENDLY)
    
    def add_fonts(self, fonts_list: list, type: FontType):
        for current_font, current_font_location in fonts_list:
            font = Font(current_font, type, current_font_location)
            self._all_fonts.append(font)
    
    @property
    def all_fonts(self) -> List[Font]:
        return self._all_fonts