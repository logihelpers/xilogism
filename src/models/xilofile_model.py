from dataclasses import dataclass
from typing import Optional
from enum import Enum

class StorageType(Enum):
    LOCAL = 0
    GDRIVE = 1

@dataclass
class XiloFile:
    title: Optional[str] = None
    path: Optional[str] = None
    date: Optional[str] = None
    size: Optional[str] = None
    thumbnail: Optional[str] = None
    storage_type: Optional[StorageType] = None