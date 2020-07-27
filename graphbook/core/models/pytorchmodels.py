from torch import optim
from ..graph import REGISTRY

from torch import nn
from torch import optim


for name in dir(nn):
    if 'A' <= name[0] <= 'Z':
        REGISTRY._register_module(getattr(nn, name))

for name in dir(optim):
    if 'A' <= name[0] <= 'Z':
        REGISTRY._register_module(getattr(optim, name))

