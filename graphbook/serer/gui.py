from graphbook.util.logs import get_logger
from graphbook.core.json_object import (
    JsonObject, FloatField, StringField,
    UUIDField, IntField, ListField,
    StringOptionField
)

logger = get_logger('gui log')


class Wire(JsonObject):
    output_from_node_uuid = StringField()
    output_from_node_output_type = StringOptionField(value_list=['value', 'dict', 'list'])
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
    name = StringField(default='') #name of instance or function/package name
    uuid = UUIDField()
    box_type = StringOptionField(value_list=['function', 'instance'])
    num_input_args = IntField()
    kwargs = ListField(dtype=StringField)
    output_type = StringOptionField(value_list=['value', 'dict', 'list'])
    output_list_number = IntField()
    output_keywords = ListField(dtype=StringField)



def add_wire(out_box, in_box, out_index=None, in_index=0):
    return Wire(
        output_from_node_uuid=out_box.uuid,
        output_from_node_output_type='value',
        output_from_node_output_key=out_index if out_box.output_type == 'dict' else '',
        output_from_node_output_index=out_index if out_box.output_type == 'list' else 0,
        input_to_node_uuid=in_box.uuid,
        input_to_node_input_type='args' if isinstance(in_index, int) else 'kwargs',
        input_to_node_input_key=in_index if isinstance(in_index, str) else '',
        input_to_node_input_index=in_index if isinstance(in_index, int) else 0,
    )
