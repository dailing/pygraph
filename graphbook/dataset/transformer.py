from ..core import REGISTRY
import numpy as np
from ..util import get_logger

logger = get_logger('transformer')


@REGISTRY.register_module()
class ImgToTensor():
    key = 'image'

    def __call__(self, data):
        if self.key not in data:
            logger.info(f'key not exist {list(data.keys())}')
            return data
        img = data.pop(self.key)
        # logger.info('data')
        assert isinstance(img, np.ndarray)
        if len(img.shape) == 2:
            img = img[np.newaxis, :,:]
        elif len(img.shape) == 3:
            img = img.transpose(2,0,1)
        data[self.key] = img
        return data

