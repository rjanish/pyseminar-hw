
import os

import numpy as np
from scipy.ndimage import imread

class ImageFeaturizer(object):
    '''
    Class for computing features of images for machine classification.  This 
    is basically a bucket for storing the definition of all features to be 
    used.

    Images to be featureized can either be passed during initialization of
    the class, or added later with the "compute_features" method.  The
    resulting features can be retrieved with the "get_features" method.

    Arguments:
    ---------------
    images - list of image filenames to featureize
    feature_list - list of functions to use to compute features, by default
    it uses all of the feature methods defined in the class  
    '''

    def __init__(self, images=[], feature_list='all'):
        DEFAULT_FEATURES = [self.red_fraction,
                            self.blue_fraction,
                            self.green_fraction]
        if feature_list == 'all':
            self.features_to_use = DEFAULT_FEATURES
        else:
            self.features_to_use = feature_list
        self.features = []
        self.compute_features(images)

    def compute_features(self, images):
        ''' 
        Read each image in the passed list of image filename, and compute 
        each feature in self.features_to_use for each image.  Results are 
        stored in 2d list self.features
        '''
        for im_filename in images:
            im = imread(im_filename)
            f = [feature_func(im) for feature_func in self.features_to_use]
            self.features.append(f)

    def get_features(self):
        return np.array(self.features)

    # begin feature calculators
    def red_fraction(self, image):
        return image[:,:,0].sum()/float(image.sum())

    def blue_fraction(self, image):
        return image[:,:,1].sum()/float(image.sum())

    def green_fraction(self, image):
        return image[:,:,2].sum()/float(image.sum())


def prepare_training_set(training_dir):
    cat_names = [d for d in os.listdir(training_dir)
                    if os.path.isdir(training_dir + '/' + d)]
    cat_dirs = [training_dir + '/' + catagory for catagory in cat_names]
    catagories = []
    image_files = []
    for cat_num, (cat, cat_dir) in enumerate(zip(cat_names, cat_dirs)):
        images = [cat_dir + '/' + f for f in os.listdir(cat_dir) 
                                    if (os.path.isfile(cat_dir + '/' + f) and
                                        f[0] != '.')]
        catagories += [cat_num]*len(images)
        image_files += images
    return image_files, catagories, cat_names

