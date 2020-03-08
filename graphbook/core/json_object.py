import json
from abc import ABC, abstractmethod
import uuid
from graphbook.util.logs import get_logger


logger = get_logger('jsonobject')


class JsonObject():
    # TODO: add __get__, __set__ function, to make it suitable 
    # to be used as a single field
    def __init__(self, **kwargs):
        storage = {}
        for k, v in self.__class__.__dict__.items():
            if isinstance(v, Field):
                v.name = k
                if callable(v.default):
                    storage[k] = v.default()
                else:
                    storage[k]=v.default
        self.__storage__ = storage
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def get_json(self):
        json_dict = {}
        for k, v in self.__class__.__dict__.items():
            if isinstance(v, Field) or isinstance(v, JsonObject):
                json_dict[k] = v.get_json(self)
        return json_dict

    def from_json(self, data, strict=False):
        assert isinstance(data, dict)
        for k, v in data.items():
            if not k in self.__storage__:
                if strict:
                    raise Exception(f"Not Match! key {k} not found")
                continue
            self.__class__.__dict__[k].from_json(self, v)


class Field(ABC):
    def __init__(self, default=None, dtype=None, verify=None):
        self.name = None
        self.default = default
        self.dtype = dtype
        if not hasattr(self, '_verify'):
            self._verify = verify

    def __set__(self, instance, value):
        '''
        Make sure that write a json serializable value to 
        __storage__
        '''
        value = self._from(value)
        # print('set')
        if self._verify is not None and not self._verify(value):
            raise Exception('input data not correct!')
        instance.__storage__[self.name] = value
    
    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        return self._to(instance.__storage__[self.name])

    def get_json(self, instance):
        return self.__get__(instance)

    def from_json(self, instance, obj):
        self.__set__(instance, obj)

    def _from(self, obj):
        return self.dtype(obj)

    def _to(self, obj):
        return self.dtype(obj)

class IntField(Field):
    def __init__(self, default=0):
        super().__init__(default=default, dtype=int)


class FloatField(Field):
    def __init__(self, default=0.):
        super().__init__(default=default, dtype=float)


class StringField(Field):
    def __init__(self, default=''):
        super().__init__(default=default, dtype=str)


class StringOptionField(Field):
    def __init__(self, default=None, value_list=[]):
        assert len(value_list) > 0
        if default is None:
            default = value_list[0]
        super().__init__(default=default, dtype=str)
        self.value_list = value_list
    
    def _verify(self, data):
        return data in self.value_list


class UUIDField(Field):
    @staticmethod
    def get_uuid():
        return str(uuid.uuid4())

    def __init__(self):
        super().__init__(default=UUIDField.get_uuid, dtype=str)


class _ListFieldStorage(JsonObject):
    def __init__(self, dtype):
        # self._dtype = dtype
        self._dtype_instance = dtype()
        self._storage = []
        super().__init__()

    def __setitem__(self, index, value):
        self._storage[index] = self._dtype_instance._from(value)

    def __getitem__(self, index):
        return self._dtype_instance._to(self._storage[index])

    def append(self, value):
        self._storage.append(self._dtype_instance._from(value))

    def __len__(self):
        return self._storage.__len__()

    def get_json(self):
        return [self._dtype_instance._to(i) for i in self._storage]

    def from_json(self, obj):
        assert isinstance(obj, list)
        for i in obj:
            self.append(i)
    # TODO: add more list api here


class ListField(Field):
    class _default_value():
        def __get__(self, instance, cls=None):
            # print('default__get__')
            return _ListFieldStorage(instance.dtype)
    
    default=_default_value()

    def __init__(self, dtype, **kwargs):
        super().__init__()
        self.dtype = dtype
        self.initial_args = kwargs
        del self.__dict__['default']

    def _from(self, obj):
        storage = _ListFieldStorage(self.dtype)
        storage.from_json(obj)
        return storage

    def _to(self, obj):
        return obj

    def get_json(self, instance):
        return self.__get__(instance).get_json()

    def from_json(self, instance, obj):
        self.__get__(instance).from_json(obj)
