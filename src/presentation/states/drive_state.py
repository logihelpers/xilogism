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
    
    def on_change(self):
        pass

    def request_files(self):
        self.on_request_files()
    
    def on_request_files(self):
        pass