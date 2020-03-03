from graphbook.util.logs import get_logger
from graphbook.core.json_object import JsonObject, FloatField, StringField

logger = get_logger('gui log')


class Box(JsonObject):
    x = FloatField(default=10)
    y = FloatField(default=10)
    width = FloatField(default=200)
    height = FloatField(default=100)
    name = StringField(default='')
    
