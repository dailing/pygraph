from ..core import REGISTRY

from torch.utils.data import Dataset
import numpy as np
from os.path import join as pjoin


@REGISTRY.register_module()
class Mnist(Dataset):
    def __init__(self, split=None, root=None, uniform_noise_ratio=0.1):
        if root is None:
            root = '../data/mnist'
        if split is None:
            split = 'train'
        files = dict(
            test=('t10k-images.idx3-ubyte', 't10k-labels.idx1-ubyte'),
            train=('train-images.idx3-ubyte', 'train-labels.idx1-ubyte'))
        self.split = split
        self.root = root
        image_file_name, label_file_name = files[split]
        self.images = np.frombuffer(
            open(pjoin(root, image_file_name), 'rb').read()[16:],
            dtype=np.uint8).reshape(-1, 28, 28)
        self.labels = np.frombuffer(
            open(pjoin(root, label_file_name), 'rb').read()[8:],
            dtype=np.uint8).astype(np.int)
        rstate = np.random.RandomState(341325)
        noise = rstate.randint(0, 9, self.images.shape[0]) + 1
        selection = rstate.choice(
            self.images.shape[0],
            int(self.images.shape[0] * uniform_noise_ratio),
            replace=False)
        noise_label = self.labels.copy()
        noise_label[selection] = \
            (noise_label[selection] + noise[selection]) % 10
        self.uniform_noise_label = noise_label

    def __getitem__(self, index):
        if index > self.images.shape[0]:
            raise IndexError()
        return dict(
            image=self.images[index, :, :],
            label=self.labels[index],
            uniform_noise=self.uniform_noise_label[index])

    def __len__(self):
        return self.images.shape[0]

# if __name__ == "__main__":
#     import matplotlib.pyplot as plt
#     import dataset.mnist
#     mnist = dataset.mnist.Mnist()
#     img, label = mnist[0]
#     print(label)
#     plt.imshow(img)

