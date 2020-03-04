from graphbook.core.json_object import (
    JsonObject, IntField, ListField,
    UUIDField, StringOptionField)
import pytest
from graphbook.core.gui import Box

class IntObject(JsonObject):
    int_field = IntField(default=10)


def test_int_field():
    o1 = IntObject()
    assert o1.int_field == 10
    o1.int_field = 100
    assert o1.int_field == 100
    jsondict = o1.get_json()
    o2 = IntObject()
    o2.from_json(jsondict)
    assert o2.int_field == 100

def test_set_attr_int_field():
    o2 = IntObject(int_field = 10000)
    assert o2.int_field == 10000


class ListObject(JsonObject):
    list1 = ListField(IntField)


def test_list_field():
    l1 = ListObject()
    assert len(l1.list1) == 0
    l1.list1.append('10')
    assert l1.list1[0] == 10
    assert len(l1.list1) == 1
    l2 = ListObject()
    assert(l2)
    l2.from_json(l1.get_json())
    assert len(l2.list1) == 1
    assert l2.list1[0] == 10


class UUIDObject(JsonObject):
    uuid = UUIDField()


def test_uuid():
    uuidobj = UUIDObject()
    assert len(uuidobj.uuid) > 0
    assert isinstance(uuidobj.uuid, str)


class StringOpetion(JsonObject):
    option = StringOptionField(value_list=['a', 'b'])


def test_string_option():
    option = StringOpetion()
    assert option.option == 'a'
    option.option = 'b'
    assert option.option == 'b'
    with pytest.raises(Exception):
        option.option = 'c'


cross_object_field_int = IntField(default=10)


class CrossObject1(JsonObject):
    int_field1 = cross_object_field_int


class CrossObject2(JsonObject):
    int_field2 = cross_object_field_int


class CrossObject3(JsonObject):
    int_field1 = cross_object_field_int


def test_cross_field():
    obj1 = CrossObject1()
    obj2 = CrossObject2()
    obj3 = CrossObject3()
    obj1.int_field1 = 1
    obj2.int_field2 = 2
    obj3.int_field1 = 3
    obj4 = CrossObject1()

    assert obj1.int_field1 == 1
    assert obj2.int_field2 == 2
    assert obj3.int_field1 == 3
    assert obj4.int_field1 == 10


def test_make_box():
    box = Box(
        name='a',
        x=10, y=10,
        output_type='value',
        num_input_args=2,
        kwargs = ['input1', 'input2']
    )
    box.get_json()


if __name__ == "__main__":
    test_list_field()

