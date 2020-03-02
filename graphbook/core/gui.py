from graphbook.util.logs import get_logger
from graphbook.core.json_object import JsonObject, FloatField

logger = get_logger('gui log')


class Box(JsonObject):
    x = FloatField(default=0)
    y = FloatField(default=0)
    width = FloatField(default=100)
    height = FloatField(default=100)
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 100
        self.height = 100
        self.node = None

    def json(self):
        result = dict(
            x=self.x, y=self.y, 
            width=self.width,
            height=self.height,
        )
        if self.node is not None:
            input = [(node.name, outputName, inputName)
                for node, outputName, inputName in self.node.inputs]
            output = None
            if isinstance(self.node.output, dict):
                output = list(self.node.output.keys())
            else:
                output = ['_']
            result.update(dict(input=input, output=output))
        return result

    def from_json(self, json):
        pass
        
