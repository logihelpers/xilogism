from utils.singleton import Singleton

class CustomBackgroundState(metaclass = Singleton):
    def __init__(self):
        self._active: str = None
        self._change_callbacks: list = []
    
    @property
    def active(self) -> str:
        return self._active
    
    @active.setter
    def active(self, active: str):
        self._active = active
        for callback in self._change_callbacks:
            callback()
    
    @property
    def on_change(self):
        return self._change_callbacks
    
    @on_change.setter
    def on_change(self, callback):
        if callback not in self._change_callbacks:
            self._change_callbacks.append(callback)