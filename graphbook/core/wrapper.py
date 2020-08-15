from .graph import build_from_cfg, build_graph, Node, REGISTRY
import typing
import random
from multiprocessing import Queue, Process
from .graph import connect
from ..util import get_logger
import queue
import numpy as np
import torch


logger = get_logger('wrapper')


_prime_number_list = [
    900000000013, 900000000017, 900000000049, 900000000199, 900000000253,
    900000000269, 900000000281, 900000000373, 900000000461, 900000000587,
    900000000643, 900000000671, 900000000673, 900000000737, 900000000743,
    900000000773, 900000000787, 900000000803, 900000000859, 900000000869,
    900000000941, 900000000943, 900000000967, 900000000971, 900000000979,
    900000001057, 900000001091, 900000001111, 900000001151, 900000001183,
    900000001207, 900000001237, 900000001301, 900000001309, 900000001321,
    900000001339, 900000001393, 900000001457, 900000001471, 900000001487,
    900000001513, 900000001531, 900000001553, 900000001559, 900000001633,
    900000001697, 900000001739, 900000001783, 900000001811, 900000001847,
    900000001853, 900000001889, 900000001921, 900000001969, 900000001993,
    900000002029, 900000002051, 900000002063, 900000002071, 900000002087,
    900000002107, 900000002113, 900000002119, 900000002159, 900000002203,
    900000002221, 900000002381, 900000002431, 900000002437, 900000002441,
    900000002471, 900000002507, 900000002543, 900000002549, 900000002599,
    900000002623, 900000002639, 900000002641, 900000002653, 900000002683,
    900000002711, 900000002779, 900000002873, 900000002879, 900000002959,
    900000002977, 900000002983, 900000003017, 900000003029, 900000003079,
    900000003107, 900000003109, 900000003163, 900000003173, 900000003187,
    900000003197, 900000003263, 900000003269, 900000003283, 900000003293,
    900000003349, 900000003403, 900000003443, 900000003457, 900000003547,
    900000003583, 900000003601, 900000003613, 900000003733, 900000003751,
    900000003787, 900000003829, 900000003901, 900000003923, 900000003937,
    900000003941, 900000003943, 900000003979, 900000004049, 900000004147,
    900000004151, 900000004157, 900000004159, 900000004177, 900000004217,
    900000004219, 900000004259, 900000004261, 900000004271, 900000004307,
    900000004381, 900000004399, 900000004411, 900000004441, 900000004457,
    900000004469, 900000004481, 900000004499, 900000004511, 900000004513,
    900000004531, 900000004577, 900000004601, 900000004691, 900000004741,
    900000004751, 900000004759, 900000004763, 900000004823, 900000004829,
    900000004859, 900000004867, 900000004873, 900000004879, 900000004933,
    900000004951, 900000004961, 900000004991, 900000004993, 900000005053,
    900000005083, 900000005087, 900000005101, 900000005123, 900000005143,
    900000005167, 900000005171, 900000005263, 900000005269, 900000005293,
    900000005297, 900000005309, 900000005341, 900000005351, 900000005393,
    900000005407, 900000005417, 900000005453, 900000005473, 900000005491,
    900000005503, 900000005519, 900000005573, 900000005587, 900000005683,
    900000005687, 900000005803, 900000005831, 900000005881, 900000005893,
    900000005909, 900000005939, 900000005977, 900000005987, 900000006007,
    900000006023, 900000006041, 900000006047, 900000006079, 900000006119,
]


@REGISTRY.register_module()
class IndexSelecter(object):
    def __init__(self, cfg):
        super().__init__()
        self.obj = build_from_cfg(cfg, REGISTRY)
    
    def __call__(self, key):
        assert type(key) in (str, int)
        # logger.info(f'key is {key}')
        return dict(index=key, data=self.obj[key])


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

@REGISTRY.register_module()
class RandomSequenceGenerator():
    def __init__(self, n):
        self.n = n
        self.current_index=0
        self.prime = random.choice(_prime_number_list)
        self.counter = 0

    def __call__(self):
        if self.counter >= self.n:
            self.counter = 0
            self.prime = random.choice(_prime_number_list)
        self.counter += 1
        return ((self.counter) * self.prime) % self.n


@REGISTRY.register_module()
class SequenceGenerator():
    def __init__(self, n):
        self.n = n
        self.current = 0
    
    def __call__(self):
        if self.current >= self.n:
            self.current = 0
        self.current += 1
        return self.current


class _QueueExtractor():
    def __init__(self, queue):
        self.queue = queue

    def __call__(self):
        res = self.queue.get()
        # logger.info(f'get {res}')
        return res


@REGISTRY.register_module()
class Collector():
    def __init__(self):
        pass

    def _element_type(self, a):
        while type(a) in (list, tuple):
            a = a[0]
        return type(a)
            

    def __call__(self, data):
        if isinstance(data, list) or isinstance(data, tuple):
            if isinstance(data[0], dict):
                keys = list(data[0].keys())
                result = {k:[d[k] for d in data] for k in keys}
                for k,v in result.items():
                    eletype = self._element_type(v)
                    if eletype in (int, np.int64):
                        result[k] = torch.LongTensor(v)
                    elif eletype == float or eletype==np.ndarray:
                        result[k] = torch.FloatTensor(v)
                    elif issubclass(eletype, torch.Tensor):
                        result[k] = torch.stack(v)
                    else:
                        logger.info(f'cannot convert type {eletype}')
                return result
        logger.warning(f'not implemented for type: {type(data)}')
        return data


class Connector():
    def __call__(self, **kwargs):
        # logger.info(f'got {list(kwargs.keys())}')
        return kwargs


class _Transformer():
    def __init__(self, cfg):
        self.transforms = [build_from_cfg(c, REGISTRY) for c in cfg]
        # logger.info(self.transforms)

    def __call__(self, data):
        # logger.info(data)
        for t in self.transforms:
            data = t(data)
        return data


@REGISTRY.register_module()
class AsyncLoader():
    @staticmethod
    def _worker(cfg, transform, req_queue:Queue, result_queue:Queue):
        # data = build_from_cfg(cfg, REGISTRY)
        qex = Node(_QueueExtractor(req_queue))
        data = Node(IndexSelecter(cfg))
        transformer = Node(_Transformer(transform))
        conn = Node(Connector())
        connect(qex, None, data, None)
        connect(data, 'data', transformer, 'data')
        connect(data, 'index', conn, 'index')
        connect(transformer, '*', conn, 'data')
        # logger.info(transforms)
        while True:
            d = conn()
            # logger.info(d)
            # logger.info(f'finish work')
            result_queue.put((d['index'], d['data']))
            # logger.info(f'result queue size {result_queue.qsize()}, req queue: {req_queue.qsize()}')
    
    def __init__(self, n, seq, data, transform=[], workers=12):
        self.seq = build_from_cfg(seq, REGISTRY)
        self.data = data
        self.req_queue = Queue(1024)
        self.result_queue = Queue(1024)
        self.n = n
        self.task_queue = queue.Queue(0)
        self.result_buffer = {}
        self.workers = [
            Process(
                target=AsyncLoader._worker,
                daemon=True,
                args=(data, transform, self.req_queue, self.result_queue)) for _ in range(workers)]

        for p in self.workers:
            p.start()
        self._preload(self.n * 2)

    def _preload(self, n=1):
        for _ in range(self.n):
            res = self.seq()
            self.req_queue.put(res)
            self.task_queue.put(res)

    def __call__(self):
        self._preload(self.n)
        res = []
        for _ in range(self.n):
            t = self.task_queue.get()
            while t not in self.result_buffer:
                idx, result = self.result_queue.get()
                self.result_buffer[idx] = result
            res.append(self.result_buffer.pop(t))
        return res
