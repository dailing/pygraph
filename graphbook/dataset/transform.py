import numpy as np
from torchvision.transforms import Compose, Resize as _resize, ToTensor as _totensor \
    , RandomRotation as _random_rotation
from PIL import Image
import os
import cv2

class Resize():
    def __init__(self, size, ignore_key=None):
        if ignore_key is None:
            ignore_key = []

        self.ignore_key = set(ignore_key)
        self.transform = _resize(size)
    
    def __call__(self, inputs:dict):
        inputs = inputs.copy()
        # if 'image' in inputs:
        #     if isinstance(input['image'], np.ndarray):
        #         input['image'] = Image.fromarray(input['image'])
        # else:
        #     return inputs
        for k in list(inputs.keys()):
            v = inputs[k]
            if k in self.ignore_key:
                continue
            if isinstance(v, np.ndarray):
                v = Image.fromarray(v)
            if not isinstance(v, Image.Image):
                continue
            ishape = v.size
            img = self.transform(v)
            oshape= img.size
            ratio = [oshape[1] / ishape[1], oshape[0] / ishape[0]]
            if 'ratio' in inputs:
                if ratio != inputs['ratio']:
                    print(f"change ration from {inputs['ratio']} to {ratio}")
            inputs['ratio'] = ratio
            inputs[k] = img

        return inputs

class CenterCrop():
    def __init__(self, ignore_key=None):
        pass

    def __call__(self, inputs:dict):
        inputs = inputs.copy()
        # if 'image' in inputs:
        #     if isinstance(input['image'], np.ndarray):
        #         input['image'] = Image.fromarray(input['image'])
        # else:
        #     return inputs
        for k in list(inputs.keys()):
            v = inputs[k]
            if isinstance(v, np.ndarray):
                v = Image.fromarray(v)
            if not isinstance(v, Image.Image):
                continue
            
            if '_crop_' in inputs:
                crop = inputs['_crop_']
            else:
                w, h = v.size
                if  w > h:
                    crop = ((w-h)//2, 0, h + (w-h)//2 , h)
                else:
                    crop = (0, (h-w)//2, w, (h-w)//2+w)
                inputs['_crop_'] = crop
            img = v.crop(crop)
            inputs[k] = img
        return inputs
    
class LoadImg():
    def __init__(self, root = ''):
        self.root = root
        
    def __call__(self, inputs:dict):
        inputs = inputs.copy()
        for k,v in inputs.items():
            if not isinstance(v, str):
                continue
            v = os.path.join(self.root, v)
            # print(f'loading {v}')
            if not os.path.exists(v):
                print(f'NOT EXIST {v}')
                continue
            if v.split('.')[-1] in ('png', 'jpg'):
                try:
                    v = Image.open(v)
                    inputs[k] = v
                except Exception as e:
                    continue
        return inputs


class Generate_mask():
    def __call__(self, inputs):
        shape = inputs['image'].size
        fx, fy = inputs['fx'], inputs['fy']
        x, y = np.meshgrid(range(shape[0]), range(shape[1]))
        label = (x-fx)**2 + (y-fy)**2
        label = label / ((np.array(shape)**2).sum())
        label = np.exp(-label * 100)
        inputs['mask'] = label.astype(np.float32)
        return inputs


class ToTensor():
    def __init__(self):
        self._transform = _totensor()
    
    def __call__(self, inputs):
        inputs = inputs.copy()
        for k,v in inputs.items():
            if not isinstance(v, Image.Image):
                continue
            inputs[k] = self._transform(v)
        return inputs


def convert_color_factory(src, dst):

    code = getattr(cv2, f'COLOR_{src.upper()}2{dst.upper()}')

    def convert_color(img):
        out_img = cv2.cvtColor(img, code)
        return out_img

    convert_color.__doc__ = f"""Convert a {src.upper()} image to {dst.upper()}
        image.

    Args:
        img (ndarray or str): The input image.

    Returns:
        ndarray: The converted {dst.upper()} image.
    """

    return convert_color

bgr2rgb = convert_color_factory('bgr', 'rgb')
rgb2bgr = convert_color_factory('rgb', 'bgr')
bgr2hsv = convert_color_factory('bgr', 'hsv')
hsv2bgr = convert_color_factory('hsv', 'bgr')
bgr2hls = convert_color_factory('bgr', 'hls')
hls2bgr = convert_color_factory('hls', 'bgr')


    
class PhotoMetricDistortion(object):
    """Apply photometric distortion to image sequentially, every transformation
    is applied with a probability of 0.5. The position of random contrast is in
    second or second to last.

    1. random brightness
    2. random contrast (mode 0)
    3. convert color from BGR to HSV
    4. random saturation
    5. random hue
    6. convert color from HSV to BGR
    7. random contrast (mode 1)
    8. randomly swap channels

    Args:
        brightness_delta (int): delta of brightness.
        contrast_range (tuple): range of contrast.
        saturation_range (tuple): range of saturation.
        hue_delta (int): delta of hue.
    """

    def __init__(self,
                 brightness_delta=32,
                 contrast_range=(0.5, 1.5),
                 saturation_range=(0.5, 1.5),
                 hue_delta=18):
        self.brightness_delta = brightness_delta
        self.contrast_lower, self.contrast_upper = contrast_range
        self.saturation_lower, self.saturation_upper = saturation_range
        self.hue_delta = hue_delta

    def __call__(self, results):
        """Call function to perform photometric distortion on images.

        Args:
            results (dict): Result dict from loading pipeline.

        Returns:
            dict: Result dict with images distorted.
        """
        img = results['image']
        img = np.array(img).astype(np.float32)
        assert img.max() > 0.2
        assert img.dtype == np.float32, \
            'PhotoMetricDistortion needs the input image of dtype np.float32,'\
            ' please set "to_float32=True" in "LoadImageFromFile" pipeline'
        # random brightness
        if random.randint(2):
            delta = random.uniform(-self.brightness_delta,
                                   self.brightness_delta)
            img += delta

        # mode == 0 --> do random contrast first
        # mode == 1 --> do random contrast last
        mode = random.randint(2)
        if mode == 1:
            if random.randint(2):
                alpha = random.uniform(self.contrast_lower,
                                       self.contrast_upper)
                img *= alpha

        # convert color from BGR to HSV
        img = bgr2hsv(img)

        # random saturation
        if random.randint(2):
            img[..., 1] *= random.uniform(self.saturation_lower,
                                          self.saturation_upper)

        # random hue
        if random.randint(2):
            img[..., 0] += random.uniform(-self.hue_delta, self.hue_delta)
            img[..., 0][img[..., 0] > 360] -= 360
            img[..., 0][img[..., 0] < 0] += 360

        # convert color from HSV to BGR
        img = hsv2bgr(img)

        # random contrast
        if mode == 0:
            if random.randint(2):
                alpha = random.uniform(self.contrast_lower,
                                       self.contrast_upper)
                img *= alpha

        # randomly swap channels
        if random.randint(2):
            img = img[..., random.permutation(3)]
        
        img[img>255]=255
        img[img<0] = 0
        img = (img).astype(np.uint8)
        img = Image.fromarray(img)
        results['image'] = img
        return results
