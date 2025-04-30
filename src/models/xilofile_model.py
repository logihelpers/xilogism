from dataclasses import dataclass
from typing import Optional
from enum import Enum

class StorageType(Enum):
    LOCAL = 0
    GDRIVE = 1

class XiloFile:
    def __init__(
            self, 
            title: Optional[str] = None,
            path: Optional[str] = None,
            date: Optional[str] = None,
            size: Optional[str] = None,
            thumbnail: Optional[str] = None,
            storage_type: Optional[StorageType] = None
        ):

        self._title = title
        self._path = path
        self._date = date
        self._size = size
        self._thumbnail = thumbnail
        self._storage_type = storage_type

    @property
    def title(self) -> Optional[str]:
        return self._title
    
    @title.setter
    def title(self, value: Optional[str]):
        self._title = value

    @property
    def path(self) -> Optional[str]:
        return self._path
    
    @path.setter
    def path(self, value: Optional[str]):
        self._path = value

    @property
    def date(self) -> Optional[str]:
        return self._date
    
    @date.setter
    def date(self, value: Optional[str]):
        self._date = value

    @property
    def size(self) -> Optional[str]:
        return self._size
    
    @size.setter
    def size(self, value: Optional[str]):
        self._size = value

    @property
    def thumbnail(self) -> Optional[str]:
        return self._thumbnail
    
    @thumbnail.setter
    def thumbnail(self, value: Optional[str]):
        self._thumbnail = value

    @property
    def storage_type(self) -> Optional[StorageType]:
        return self._storage_type
    
    @storage_type.setter
    def storage_type(self, value: Optional[StorageType]):
        self._storage_type = value
    
    def __str__(self) -> str:
        return (f"XiloFile(title={self._title}, path={self._path}, date={self._date}, "
                f"size={self._size}, thumbnail={self._thumbnail}, storage_type={self._storage_type})")