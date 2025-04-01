from dataclasses import dataclass
from models.xilofile_model import XiloFile

from typing import List

@dataclass
class User:
    email: str
    password: str
    username: str
    gdrive_files: List[XiloFile]