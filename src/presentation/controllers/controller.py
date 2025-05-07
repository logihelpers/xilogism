from enum import Enum
from flet import Page

class Priority(Enum):
    ENTRY_POINT = 0
    VIEW_BOUND = 1
    WIDGET_BOUND = 2
    DIALOG_BOUND = 3
    SETTINGS_BOUND = 4
    NONE = 5
    LAST = 6

class Controller:
    instances: list = []
    priority: Priority = Priority.NONE
    def __init__(self, target: Page = None):
        self.target = target
        self.call_subclasses()
    
    def call_subclasses(self):
        subclasses = [(subclass, getattr(subclass, 'priority', Priority.NONE)) for subclass in self.__class__.__subclasses__()]
        subclasses.sort(key=lambda x: x[1].value)

        Controller.instances = []
        for subclass, priority in subclasses:
            instance = subclass(self.target)
            Controller.instances.append(instance)

    @staticmethod
    def initialize_controllers(target: Page = None):
        Controller(target)