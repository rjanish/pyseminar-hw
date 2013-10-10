
import numpy as np
from scipy.fftpack import fft2, ifft2, fftshift

class ImageServer(object):
    
    def invert(self, image):
        if len(image.shape) == 3:
            maxes = np.max(np.max(image, axis=0), axis=0)
            for channel, channel_max in enumerate(maxes):
                image[..., channel] = channel_max - image[..., channel]
        elif len(image.shape) == 2:
            max_gray = np.max(image)
            image = max_gray - image
        else:
            raise Exception("Invalid image shape: {}".foramt(image.shape))
        return image

    def frequency_space_by_channel(self, image): 
        if len(image.shape) == 3:
            freq_space = np.zeros(image.shape)
            for color in [0,1,2]:
                freq_space[..., color] = fftshift(fft2(image[..., color]))
        elif len(image.shape) == 2:
            freq_space = fftshift(fft2(image))
        else:
            raise Exception("Invalid image shape: {}".foramt(image.shape))
        return freq_space

    def colorize_by_power(self, image):
        if len(image.shape) == 3:
            power = fft2(np.sum(image, axis=2))**2
        elif len(image.shape) == 2:
            power = fft2(image)**2
        else:
            raise Exception("Invalid image shape: {}".foramt(image.shape))
        thirds = (power.max() - power.min())/3.0
        third_cut = power.min() + thirds
        twothird_cut = third_cut + thirds
        lower = power < third_cut
        upper = power > twothird_cut
        middle = ~(lower | upper)
        colorized = np.zeros((power.shape[0], power.shape[1], 3), 
                             dtype=np.uint8)
        for color, region in enumerate([upper, middle, lower]):
            new_channel = ifft2(np.where(region, power, 0.0))
            shifted = (new_channel - new_channel.min())
            scaled = 255.0*shifted/shifted.max()
            colorized[..., color] = ifft2(np.where(region, power, 0.0))
        return colorized

        