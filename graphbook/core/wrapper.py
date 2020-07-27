from .graph import build_from_cfg, REGISTRY
import typing
# from torch.nn import Module

@REGISTRY.register_module()
class IndexSelecter(object):
    def __init__(self, cfg):
        super().__init__()
        self.obj = build_from_cfg(cfg, REGISTRY)
    
    def __call__(self, key):
        return self.obj[key]


@REGISTRY.register_module()
class IndexProjector(object):
    def __init__(self, key, cfg):
        super().__init__()
        self.obj = build_from_cfg(cfg, REGISTRY)
        self.key = key

    def __call__(self):
        return self.obj[self.key]


@REGISTRY.register_module()
class AttrbuteProjector(object):
    def __init__(self, keys, cfg):
        super().__init__()
        self.obj = build_from_cfg(cfg, REGISTRY)
        self.keys = keys

    def __call__(self):
        if isinstance(self.keys, str):
            return getattr(self.obj, self.keys)
        return {k:getattr(self.obj, k) for k in self.keys}
