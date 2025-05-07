from utils.singleton import Singleton

class AnimationDisableState(metaclass = Singleton):
    def __init__(self):
        self._state: bool = None
        self._change_cb: list = []
    
    @property
    def state(self) -> bool:
        return self._state
    
    @state.setter
    def state(self, state: bool):
        self._state = state
        for callback in self._change_cb:
            callback()
    
    @property
    def on_change(self):
        return self._change_cb
    
    @on_change.setter
    def on_change(self, callback):
        if callback not in self._change_cb:
            self._change_cb.append(callback)