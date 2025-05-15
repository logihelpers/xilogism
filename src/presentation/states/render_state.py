from utils.singleton import Singleton
from typing import Tuple

class RenderDict(dict):
    def __init__(self, on_change_callback=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._on_change_callback = on_change_callback
        self._suppress_callback = False

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if self._on_change_callback and not self._suppress_callback:
            self._on_change_callback({key: value})
    
    def update_without_callback(self, content: dict):
        self._suppress_callback = True
        try:
            self.update(content)
        finally:
            self._suppress_callback = False

class RenderState(metaclass = Singleton):
    def __init__(self):
        self._input: RenderDict[str, dict] = RenderDict(self.call_input_change_callbacks, {"New": {}})
        self._output: RenderDict[str, list] = RenderDict(self.call_output_change_callbacks, {"New": []})
        self._image: RenderDict[str, str] = RenderDict(self.call_image_change_callbacks, {"New": ""})
        self._on_input_change: list[callable] = []
        self._on_output_change: list[callable] = []
        self._on_image_change: list[callable] = []
    
    @property
    def input(self) -> RenderDict[str, dict]:
        return self._input
    
    @input.setter
    def input(self, input: RenderDict[str, dict] | Tuple[RenderDict[str, dict], bool]):
        if isinstance(input, RenderDict):
            self._input.update(input)
            self.call_input_change_callbacks()
        elif isinstance(input, tuple):
            data, suppress_callback = input
            if suppress_callback:
                self._input.update_without_callback(data)
            else:
                self._input.update(data)
                self.call_input_change_callbacks()
    
    @property
    def output(self) -> RenderDict[str, list]:
        return self._output
    
    @output.setter
    def output(self, output: RenderDict[str, list] | Tuple[RenderDict[str, list], bool]):
        if isinstance(output, RenderDict):
            self._output.update(output)
            self.call_output_change_callbacks()
        elif isinstance(output, tuple):
            data, suppress_callback = output
            if suppress_callback:
                self._output.update_without_callback(data)
            else:
                self._output.update(data)
                self.call_output_change_callbacks()
    
    @property
    def image(self) -> RenderDict[str, str]:
        return self._image
    
    @image.setter
    def image(self, image: RenderDict[str, str] | Tuple[RenderDict[str, str], bool]):
        if isinstance(image, RenderDict) or isinstance(image, dict):
            self._image.update(image)
            self.call_image_change_callbacks(image)
        elif isinstance(image, tuple):
            data, suppress_callback = image
            if suppress_callback:
                self._image.update_without_callback(data)
            else:
                self._image.update(data)
                self.call_image_change_callbacks(data)
    
    @property
    def on_input_change(self):
        return self._on_input_change
    
    @on_input_change.setter
    def on_input_change(self, callback):
        if callback not in self._on_input_change:
            self._on_input_change.append(callback)

    @property
    def on_output_change(self):
        return self._on_output_change
    
    @on_output_change.setter
    def on_output_change(self, callback):
        if callback not in self._on_output_change:
            self._on_output_change.append(callback)

    @property
    def on_image_change(self):
        return self._on_image_change
    
    @on_image_change.setter
    def on_image_change(self, callback):
        if callback not in self._on_image_change:
            self._on_image_change.append(callback)
    
    def call_input_change_callbacks(self, input_dict):
        for callback in self._on_input_change:
            callback(input_dict)
    
    def call_output_change_callbacks(self, output_dict):
        for callback in self._on_output_change:
            callback(output_dict)
    
    def call_image_change_callbacks(self, image_dict: dict):
        for callback in self._on_image_change:
            callback(image_dict)