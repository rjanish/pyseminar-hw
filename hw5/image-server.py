
from SimpleXMLRPCServer import SimpleXMLRPCServer

import numpy as np
from scipy.fftpack import fft2, ifft2, fftshift

class ImageMethods(object):
    """ A bucket of image manipulation routines """

    def invert(self, image):
        """
        Invert the brightness of an image.  For RGB images each color 
        channel is inverted separately.
        """
        image = np.array(image)
        if len(image.shape) == 3:
            maxes = np.max(np.max(image, axis=0), axis=0)
            for channel, channel_max in enumerate(maxes):
                image[..., channel] = channel_max - image[..., channel]
        elif len(image.shape) == 2:
            max_gray = np.max(image)
            image = max_gray - image
        else:
            raise Exception("Invalid image shape: {}".foramt(image.shape))
        return image.tolist()

    def frequency_space_by_channel(self, image): 
        """ 
        Compute the Fourier transform of the image, treating each color 
        channel separately if the image is in RGB form.  Output is centered 
        such that the zero frequency mode is in the center.
        """
        image = np.array(image)
        if len(image.shape) == 3:
            freq_space = np.zeros(image.shape)
            for color in [0,1,2]:
                freq_space[..., color] = fftshift(fft2(image[..., color]))
        elif len(image.shape) == 2:
            freq_space = fftshift(fft2(image))
        else:
            raise Exception("Invalid image shape: {}".foramt(image.shape))
        return freq_space.tolist()

    def colorize_by_power(self, image):
        """
        Colorize the image mode-by-mode according to the power in each mode.  
        The top third of modes are colored red, the middle third green, and 
        the lower third blue.  For RGB images, a grayscale equivalent is 
        computed and colorized. 
        """
        image = np.array(image)
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
        return colorized.tolist()

class ImageServer(object):
    __init__(self, name='localhost', port=5000, help=True):
        self.name = name
        self.port = port

    def run(self):
        server = SimpleXMLRPCServer((name, port))
        server.register_instance(ImageMethods())
        print "Starting ImageServer........"
        print "Press Control-C to exit"
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print "ImageServer exiting........."

            
if __name__ == '__main__':
    im_server = ImageServer()
    im_server.run()
