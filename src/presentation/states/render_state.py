from services.singleton import Singleton

class RenderState(metaclass = Singleton):
    def __init__(self):
        self._input: dict = []
        self._output: list = []
        self._image: str = ""
    
    @property
    def input(self) -> dict:
        return self._input
    
    @input.setter
    def input(self, input: dict):
        self._input = input
        self.on_input_change()
    
    @property
    def output(self) -> list:
        return self._output
    
    @output.setter
    def output(self, output: list):
        self._output = output
        self.on_output_change()
    
    @property
    def image(self) -> str:
        return self._image
    
    @image.setter
    def image(self, image: str):
        self._image = image
        self.on_image_change()
    
    def on_input_change(self):
        pass

    def on_output_change(self):
        pass

    def on_image_change(self):
        pass