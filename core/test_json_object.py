from core.json_object import JsonObject, IntField, ListField


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


if __name__ == "__main__":
    test_list_field()

