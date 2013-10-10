
import xmlrpclib
import os

from scipy.ndimage import imread 

# read rgb and gray images, convert to list form 
examples_dir = "example-images"
image_filenames = os.listdir(examples_dir)
half = int(len(image_filenames)/2)
rgb_images = [imread("{}/{}".format(examples_dir, image)).tolist() 
					for image in image_filenames]
gray_images = [imread("{}/{}".format(examples_dir, image), flatten=True).tolist() 
					for image in image_filenames]

# connect to server
host, port = "localhost", 5009
server = xmlrpclib.ServerProxy("http://%s:%d" % (host, port))

# process an rgb and gray image with each available method
im1 = server.colorize_by_power(gray_images[0])
im2 = server.colorize_by_power(rgb_images[0])
im3 = server.invert(gray_images[1])
im4 = server.invert(rgb_images[1])
im5 = server.frequency_space_by_channel(gray_images[2])
im6 = server.frequency_space_by_channel(rgb_images[2])