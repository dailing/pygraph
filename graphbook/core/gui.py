from graphbook.util.logs import get_logger
from graphbook.core.json_object import (
    JsonObject, FloatField, StringField,
    UUIDField, IntField, ListField,
    StringOptionField
)

logger = get_logger('gui log')


class Wire(JsonObject):
    output_from_node_uuid = StringField()
    output_from_node_output_type = StringOptionField(value_list=['dict', 'list', 'value'])
    output_from_node_output_key = StringField()
    output_from_node_output_index = IntField(default=0)
    input_to_node_uuid = StringField()
    input_to_node_input_type = StringOptionField(value_list=['kwargs', 'args'])
    input_to_node_input_key = StringField()
    input_to_node_input_index = IntField(default=0)
    uuid=UUIDField()


class Box(JsonObject):
    x = FloatField(default=10)
    y = FloatField(default=10)
    width = FloatField(default=200)
    height = FloatField(default=100)
    name = StringField(default='')
    uuid = UUIDField()
    box_type = StringOptionField(value_list=['function', 'instance'])
    num_input_args = IntField()
    kwargs = ListField(dtype=StringField)
    output_type = StringOptionField(value_list=['dict', 'list', 'value'])
    output_list_number = IntField()
    output_keywords = ListField(dtype=StringField)
