from dataclasses import dataclass
from enum import Enum

class FontType(Enum):
    MONOSPACE = False
    DYSLEXIA_FRIENDLY = True
    UI = 2

@dataclass
class Font:
    font_name: str
    font_type: FontType
    font_file: str