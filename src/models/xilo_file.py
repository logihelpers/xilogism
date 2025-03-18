class XiloFile:
    all_files: list = []
    def __init__(self, title: str = None, path: str = None, date: str = None, size: str = None, thumbnail: str = None):
        self._title__ = title
        self._path__ = path
        self._date__ = date
        self._size__ = size
        self._thumbnail__ = thumbnail

        XiloFile.all_files.append(self.as_dict())
    
    @property
    def title(self) -> str:
        return self._title__
    
    @title.setter
    def title(self, new_title):
        self._title__ = new_title
    
    @property
    def path(self) -> str:
        return self._path__
    
    @path.setter
    def path(self, new_path):
        self._path__ = new_path

    @property
    def date(self) -> str:
        return self._date__
    
    @date.setter
    def date(self, new_date):
        self._date__ = new_date

    @property
    def size(self) -> str:
        return self._size__
    
    @size.setter
    def size(self, new_size):
        self._size__ = new_size
    
    @property
    def thumbnail(self) -> str:
        return self._thumbnail__
    
    @thumbnail.setter
    def thumbnail(self, new_thumbnail):
        self._thumbnail__ = new_thumbnail
    
    def as_dict(self):
        return {
            self.title : {
                "path": self.path,
                "date": self.date,
                "size": self.size,
                "thumbnail": self.thumbnail
            }
        }