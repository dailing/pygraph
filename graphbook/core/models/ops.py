from ...core import REGISTRY

def FUNCREG(func):
    def wrapper():
        return func
    return wrapper

@REGISTRY.register_module()

class Flaten():
    def __call__(self, x):
        x=x.view(x.size(0), -1)
        return x