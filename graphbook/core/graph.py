# from util.logs import get_logger

from inspect import signature
import random
import math
import logging
from .registry import Registry, build_from_cfg
from torch.nn import Module
import types
from ..util import get_logger

logger = get_logger('graph')
REGISTRY = Registry('root')


class _InPort():
    name=None
    from_node=None
    from_node_key=None

    def __init__(self, name=None, from_node=None, from_node_key=None):
        self.name = name
        self.from_node = from_node
        self.from_node_key = from_node_key

class Node(Module):

    def __init__(self, func, default_args=None):
        super().__init__()

        self.default_args = default_args
        self.func = func

        self.argmap = {}
        self.current_id = None
        self.result = None
        # self.sig = signature(func)
        assert func is not None
        assert self.func is not None


    def _eval(self, _id=None):
        # logger.info(f'eval {self.func}')
        # logger.info(self.argmap)
        argmap = {}
        # print(self.argmap)
        if _id == self.current_id:
            return self.result
        self.current_id = _id
        if self.default_args is not None:
            for k,v in self.default_args.items():
                argmap[k] = v
        for k, v in self.argmap.items():
            tmp_result = v.from_node._eval(_id)
            if v.from_node_key == '' or v.from_node_key is None or v.from_node_key=='*':
                pass
            elif hasattr(tmp_result, '__getitem__'):
                tmp_result = tmp_result[v.from_node_key]
            elif hasattr(tmp_result, v.from_node_key):
                tmp_result = getattr(tmp_result, v.from_node_key)
            argmap[k] = tmp_result
        # parpare arguments
        nargs = -1
        for k in  argmap.keys():
            if isinstance(k, int):
                nargs = max(k, nargs)
        args=[]
        for i in range(nargs+1):
            if not i in argmap:
                raise AttributeError(f"FUCK no {i} in the fucking argmap")
            args.append(argmap[i])
        kwargs = {}
        # logger.info(argmap)
        for k, v in argmap.items():
            if not isinstance(k, int):
                if k == '*':
                    if not hasattr(v, '__getitem__'):
                        v = [v]
                    args = v
                elif k == '' or k is None:
                    # logger.info("here")
                    args = [v]
                elif k == '**':
                    kwargs.update(v)
                else:
                    kwargs[k] = v
        try:
            self.result = self.func(*args, **kwargs)
        except Exception as e:
            logger.error(self.func)
            logger.error(f'FUCKING ERROR, args are: ## {args}, ###{kwargs}', exc_info=True)
            raise e
        return self.result

    def __call__(self, name=None):
        result =  self._eval(_id=random.random())
        if name is None:
            return result
        rr = {}
        if isinstance(name, str):
            return result[name]
        for n in name:
            rr[n] = result[n]
        return rr


@REGISTRY.register_module()
def Const(value):
    return lambda : value

@REGISTRY.register_module()
def Math(func):
    return getattr(math, func)

def connect(n1, k1, n2, k2):
    # connect key1 form n1 output to key2 from n2 input
    port = _InPort(None, n1, k1)
    n2.argmap[k2] = port

def build_graph(cfg):
    nodes = {}
    for k in list(cfg.keys()):
        if not isinstance(cfg[k], dict):
            cfg.pop(k)

    for k, v in cfg.items():
        if not isinstance(v, dict):
            continue
        if 'type' not in v:
            logger.warn(f'config {k} not build, no type key')
            continue
        if v['type'] == '_wire_':
            pass
        else:
            default_args = None
            if 'default_args' in v:
                default_args = v.pop('default_args')
            _no_node=False
            if '_no_node' in v:
                _no_node = v.pop('_no_node')
            if _no_node:
                nodes[k] = build_from_cfg(v, REGISTRY)
            else:
                nodes[k] = Node(build_from_cfg(v, REGISTRY), default_args)
    for k, v in cfg.items():
        if 'type' not in v:
            continue
        if v['type'] == '_wire_':
            # logger.info(f'connecting {v}')
            if 'from_node_port' not in v:
                v['from_node_port'] = None
            if 'to_node_port' not in v:
                v['to_node_port'] = None
            connect(
                nodes[v['from_node']],
                v['from_node_port'],
                nodes[v['to_node']],
                v['to_node_port'])
    return nodes


class Graph(Module):
    def __init__(self, cfg):
        super().__init__()
        nodes = build_graph(cfg)
        for k, v in nodes.items():
            self.add_module(k, v)

    def forward(self, names):
        if isinstance(names, str):
            return getattr(self, names)()
        result = {}
        for name in names:
            result[name] = getattr(self, name)()
        return result
