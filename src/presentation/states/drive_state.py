from utils.singleton import Singleton

class DriveState(metaclass=Singleton):
    def __init__(self):
        self._files = []
        self.on_change = lambda: None

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, value):
        self._files = value
        self.on_change()
