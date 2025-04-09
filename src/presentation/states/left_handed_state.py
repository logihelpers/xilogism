from services.singleton import Singleton

class LeftHandedState(metaclass = Singleton):
    def __init__(self):
        self._state: bool = None
    
    @property
    def state(self) -> bool:
        return self._state
    
    @state.setter
    def state(self, state: bool):
        self._state = state
        self.on_change()
    
    def on_change(self):
        pass