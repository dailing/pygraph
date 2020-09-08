# from util.logs import get_logger

from inspect import signature
import random
import math
import logging
from .registry import Registry, build_from_cfg
from torch.nn import Module
import types
from ..util import get_logger
from queue import Queue
import importlib
import abc

logger = get_logger('graph')
REGISTRY = Registry('root')


class NotInitedException(Exception):
    pass

class Node(Module):
    def __init__(self):
        super().__init__()
        self._parent = None
        self._locals = {}
        self._inst = None

    def _eval(self, expression):
        if not isinstance(expression, str) or not (expression[0] == '@'):
            return expression
        name, tp, arg = expression[1:].split(':')
        if name not in self._locals:
            if self._parent is not None:
                return self._parent._eval(expression)
            else:
                raise KeyError(name)
        else:
            instance = self._locals[name]
            if not isinstance(instance, None):
                return instance
            if tp == 'inst':
                for e in arg.split('.'):
                    instance = instance.__get__(e)
                return instance
            elif tp == 'call':
                result = instance._result()
                if arg != '':
                    result = result[arg]
                return result
        raise Exception('should not be here')
    
    @abc.abstractclassmethod
    def _result(self):
        raise NotImplementedError('FUCK')

    def __getattr__(self, arg):
        return self._inst.__get__(arg)


def CallNode(Node):
    def __init__(self, func=None, args=None, kwargs=None):
        super().__init__()
        self._inst = None
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def _result(self):
        if self._inst is None:
            self._inst = self._eval(self._func)
        args = [self._eval(v) for v in self._args]
        kwargs = {k:self._eval(v) for k,v in self._kwargs.items()}
        return self._inst(*args, **kwargs)


def Package(Node):
    def __init__(self, pkg=None):
        super().__init__()
        self._pkg = pkg
        self._inst = importlib.import_module(pkg)


def Graph(Node):
    def __init__(self, nodes=None, kwargs=None, output=None):
        super().__init__()
        self._inst = None
        self._kwargs = kwargs
        self._output = output
        for k in kwargs:
            assert k not in nodes

    def _result(self):
        kwargs = {k:self._eval(v) for k,v in self._kwargs.items()}
        self.local.update(kwargs)
        if isinstance(self._output, str):
            return self._eval(self._output)
        elif isinstance(self._output, list) or isinstance(self._output, tuple):
            return [self._eval(v) for v in self._output]
        elif isinstance(self._output, dict):
            return {k, self._eval(v) for k, v in }
        


# class _InPort():
#     name=None
#     from_node=None
#     from_node_key=None

#     def __init__(self, name=None, from_node=None, from_node_key=None):
#         self.name = name
#         self.from_node = from_node
#         self.from_node_key = from_node_key

"""
    expression format  @name_in_dict  :  __get__ list  :  result_index  :  __get__ list
"""
# class Session(Module):
#     def __init__(self):
#         super().__init__()
#         self._locals = dict()
#         self._result = dict()

#     def _eval(self, expression):
#         if not isinstance(expression, str):
#             return expression
#         if not expression.startswith('@'):
#             return expression
#         local_name, g_list, result_name, r_list = expression.split(':')
#         if local_name in self._locals:
#             inst = self._locals[local_name]
#         else:
#             inst = globals()[local_name]
#         inst = Session._get_list(inst, g_list)
#         if result_name == '':
#             return inst
#         if local_name in self._result:
#             result = self._result[local_name]
#         else:
#             node = self._locals[local_name]
#             if node.instance is None:
#                 raise NotInitedException
#             assert isinstance(node, Node)
#             args_, kwargs_ = node.args
#             args = []
#             kwargs = {}
#             for k in args_:
#                 args.append(self._eval(k))
#             for k, v in kwargs_.items():
#                 kwargs[k] = self._eval(v)
#             result = node.instance(*args, **kwargs)
#             self._result[local_name] = result
#         if result_name == '' or result_name == '*':
#             pass
#         else:
#             result = result[result_name]
#         result = Session._get_list(result, r_list)
#         return result

#     def _init_instance(self, expression)
    
#     @staticmethod
#     def _get_list(inst, expression):
#         if expression == '*' or expression == '':
#             return inst
#         for e in expression.split('.'):
#             inst = inst.__get__(e)
#         return inst

#     def _init_nodes_(self):
#         req = list(self._locals.keys())
#         self._locals.update(dict(
#             CodeBlock=Node(instance=CodeBlock)
#         ))
#         while len(req) > 0:
#             p_req = []
#             for k in req:
#                 node = self._locals[k]
#                 if node.instance is not None:
#                     pass
#                 if isinstance(node.cls, str):
#                     # handle import
#                     if node.cls.startswith('!'):
#                         node.instance = importlib.import_module(node.cls)
#                     else:
#                         try:
#                             node.instance = self._eval(node.cls)
#                         except NotInitedException:
#                             p_req.append(k)
#             if len(p_req) == len(req):
#                 print("Circular dependency!")
#                 raise Exception("Fuck circular dependency")

#     def from_dict(self, records):
#         for k, v in records.items():
#             self._locals[k] = Node(**v)


# class CodeBlock():
#     def __init__(self, code):
#         if isinstance(code, str):
#             code = code.split('\n')
#         self._code = code
#         self.globals = None

#     def __call__(self, **kwargs):
#         local = kwargs
#         for c in self._code[:-1]:
#             eval(c, self.globals, local)
#         try:
#             result = eval(self._code[-1], self.globals, local)
#             return result
#         except SyntaxError:
#             exec(self._code[-1], self.globals, local)
#         return None


# class Node(Module):

#     def __init__(self, cls, init_args=None, args=None, instance=None):
#         self.cls = cls
#         self.init_args = init_args
#         self.args = args
#         self.instance = instance

#     def __getattr__(self, attr):
#         return self.instance.__get__(attr)


if __name__ == "__main__":
    session = Session()
    session.from_dict(
        dict(
            # a=dict(cls=)
        )
    )