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
        self._master = None
        self._locals = {}
        # self._inst = None

    def _eval(self, expression):
        if not isinstance(expression, str) or not expression.startswith('@'):
            return expression
        logger.info(f'eval {expression}')
        name, tp, arg = expression[1:].split(':')
        if name not in self._locals:
            logger.info('searching parent node {name}')
            if self._master is not None:
                return self._master._eval(expression)
            elif hasattr(__builtins__, name):
                return getattr(__builtins__, name)
            else:
                raise KeyError(name)
        else:
            instance = self._locals[name]
            if not isinstance(instance, Node):
                return instance
            if tp == 'inst':
                instance = instance._inst
                for e in arg.split('.'):
                    if e == '':
                        continue
                    instance = getattr(instance, e)
                return instance
            elif tp == 'call':
                result = instance._result()
                if arg != '' and arg != '*':
                    result = result[arg]
                return result
        raise Exception('should not be here')

    def __getattr__(self, name):
        if '_parameters' in self.__dict__:
            _parameters = self.__dict__['_parameters']
            if name in _parameters:
                return _parameters[name]
        if '_buffers' in self.__dict__:
            _buffers = self.__dict__['_buffers']
            if name in _buffers:
                return _buffers[name]
        if '_modules' in self.__dict__:
            modules = self.__dict__['_modules']
            if name in modules:
                return modules[name]
        if '_locals' in self.__dict__:
            if name in self._locals:
                return self._locals[name]
        if self._inst is not None:
            return getattr(self._inst, name)
        raise AttributeError("'{}' object has no attribute '{}'".format(
            type(self).__name__, name))

    @abc.abstractclassmethod
    def _result(self):
        raise NotImplementedError('FUCK')


@REGISTRY.register_module()
class CallNode(Node):
    def __init__(self, func=None, args=None, kwargs=None):
        super().__init__()
        self.__inst = None
        self._func = func
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        self._args = args
        self._kwargs = kwargs

    @property
    def _inst(self):
        if self.__inst is None:
            self.__inst = self._eval(self._func)
        return self.__inst

    def _result(self):
        # if self._inst is None:
        #     self._inst = self._eval(self._func)
        args = [self._eval(v) for v in self._args]
        kwargs = {k:self._eval(v) for k, v in self._kwargs.items()}
        return self._inst(*args, **kwargs)


@REGISTRY.register_module()
class CodeNode(Node):
    def __init__(self, code):
        super().__init__()
        self._code = code.split('\n')
        self._eval_line = None
        self._global = dict()
        if len(self._code) == 1 or not self._code[-1].startswith(' '):
            self._eval_line = self._code[-1]
            self._code = '\n'.join(self._code[1:])

    def _result(self):
        # TODO calculate local map and global map here
        # TODO calculate args
        global_vars= dict()
        local_vars = dict()
        if self._code != '':
            exec(self._code, global_vars, local_vars)
        if self._eval_line is not None:
            result = eval(self._eval, global_vars, local_vars)
            return result
        return None


@REGISTRY.register_module()
class Package(Node):
    def __init__(self, pkg=None):
        super().__init__()
        self._pkg = pkg
        self._inst = importlib.import_module(pkg)


@REGISTRY.register_module()
class Graph(Node):
    def __init__(self, nodes=None, kwargs=None, output=None):
        super().__init__()
        if kwargs is None:
            kwargs = {}
        if nodes is None:
            nodes = {}
        self._kwargs = kwargs
        self._output = output
        for k in kwargs:
            assert k not in nodes
        for k, v in nodes.items():
            if isinstance(v, dict):
                v = build_from_cfg(v, REGISTRY)
            v.__dict__['_master'] =  self
            self._locals[k] = v
            setattr(self, k, v)

    def _result(self):
        kwargs = {k:self._eval(v) for k,v in self._kwargs.items()}
        self._locals.update(kwargs)
        if isinstance(self._output, str):
            return self._eval(self._output)
        elif isinstance(self._output, list) or isinstance(self._output, tuple):
            return [self._eval(v) for v in self._output]
        elif isinstance(self._output, dict):
            return {k: self._eval(v) for k, v in self._output.items()}


def build_graph(g):
    return build_from_cfg(g, REGISTRY)