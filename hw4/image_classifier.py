
import os
import sys
import pickle
import time

import numpy as np
from numpy.random import shuffle as npshuffle
from scipy.ndimage import imread
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation as cval
from skimage.feature import peak_local_max, corner_subpix
from skimage.filter import vsobel, hsobel

class ImageFeaturizer(object):
    '''
    Class for computing features of images for machine classification.  This 
    is basically a bucket for storing the definition of all features to be 
    used.

    Images to be featureized can either be passed during initialization of
    the class, or added later with the "compute_features" method.  The
    resulting features can be retrieved with the "get_features" method.

    Features should be written as methods of the class which return a list 
    of numbers, so that each method may compute more than one feature when 
    called if more efficient.  The name of these methods should be of the 
    form: "feature_1__feature_2__feature_3()", where the double underscore
    will be used to compute a list of individual feature names. 

    Arguments:
    ---------------
    images - list of image filenames to featureize 
    '''

    def __init__(self, images=[]):
        DEFAULT_FEATURES_RGB = [self.red_frac__green_frac__blue_frac,
                                self.red_std__green_std__blue_std,
                                self.rgb_theta__rgb_phi]
        DEFAULT_FEATURES_GRAY = [self.frac_peaks,
                                 self.frac_valleys,
                                 self.frac_hedges__frac_vedges,
                                 self.im_std,
                                 self.g11__g12__g13__g14__g21__g22__g23__g34__g31__g32__g33__g34__g41__g42__g34__g44]
        self.rgb_features_to_use = DEFAULT_FEATURES_RGB
        self.gray_features_to_use = DEFAULT_FEATURES_GRAY
        self.features_to_use = DEFAULT_FEATURES_RGB + DEFAULT_FEATURES_GRAY
        self.features = []
        self.compute_features(images)

    def compute_features(self, images):
        ''' 
        Read each image in the passed list of image filename, and compute 
        each feature in self.features_to_use for each image.  Results are 
        stored in 2d list self.features
        '''
        for im_filename in images:
            im = imread(im_filename).astype(float)
            im_features = []
            for feature_func in self.rgb_features_to_use:
                im_features += feature_func(im)
            if len(im.shape) == 3:
              gray = im.sum(axis=2)
            for feature_func in self.gray_features_to_use:
                im_features += feature_func(gray)
            self.features.append(im_features)

    def get_features(self):
        return np.array(self.features)

    def feature_names(self):
        name = []
        for feature_func in self.features_to_use:
            name += feature_func.func_name.split("__")
        return name

    # begin rgb feature calculators
    def red_frac__green_frac__blue_frac(self, image):
        '''fraction of luminosity that is red, green and blue'''
        if len(image.shape) == 3:
            total = float(image.sum())
            rgb = np.array([image[:,:,n].sum() for n in range(3)])
            return list(rgb/total)
        else:
            return [0.0]*3

    def red_std__green_std__blue_std(self, image):
        '''standard deviation of red, green and blue subframes'''
        if len(image.shape) == 3:
            std_devs = np.array([np.std(image[:,:,n]) for n in range(3)])
            return list(std_devs)
        else:
            return [0.0]*3

    def rgb_theta__rgb_phi(self, image):
        ''' 
        represent the image as a point in R^3, with each coordinate given by 
        the sum over a rgb color channel, and then return the spherical 
        coordinate angles of the image in rgb-space
        '''
        if len(image.shape) == 3:
            x,y,z = [image[:,:,n].sum() for n in range(3)]
            r = np.sqrt(x**2 + y**2 + x**2)
            try:
                theta = np.arccos(z/r)
                phi = np.arctan2(y, x)
            except:
                theta, phi = 0.0, 0.0
            if (0 <= theta <= np.pi) and (-np.pi <= phi <= np.pi):
                return [theta, phi]
            else:
                return [0.0, 0.0]
        else:
            return [0.0, 0.0]

    # begin grayscale feature calculators
    def frac_peaks(self, image):
        '''fraction of all grayscale pixels that are local maxima'''
        peaks = peak_local_max(image)
        return [peaks.shape[0]/float(image.size)]

    def frac_valleys(self, image):
        '''fraction of all grayscale pixels that are local minima'''
        valleys = peak_local_max(np.max(image)-image)
        return [valleys.shape[0]/float(image.size)]

    def im_std(self, image):
        '''standard deviation of grayscale image'''
        return [np.std(image)]

    def frac_hedges__frac_vedges(self, image):
        '''
        fraction of all grayscale pixels that lie on vertical and
        horizontal edges in the image interior
        '''
        v = vsobel(image)
        h = hsobel(image)
        return [v.mean(), h.mean()]

    def g11__g12__g13__g14__g21__g22__g23__g34__g31__g32__g33__g34__g41__g42__g34__g44(self, image):
        '''
        divide image into a 4x4 grid of sub pixels, compute the fraction of 
        total grayscale luminosity located in each subimage 
        '''
        y, x = image.shape
        total = image.sum()
        block_weights = []
        x_divisions = np.linspace(0, x, 5).astype(int)
        y_divisions = np.linspace(0, y, 5).astype(int)
        for xi, xf in zip(x_divisions[:-1], x_divisions[1:]):
            for yi, yf in zip(y_divisions[:-1], y_divisions[1:]):
                block_weights.append(image[yi:yf, xi:xf].sum()/total)
        return block_weights


def prepare_training_set(training_dir):
    '''
    Gather filenames and category names from a training set, assigns each
    category a label and returns a list of training image filenames and
    a corresponding list of the category labels of each image.

    Arguments:
    training_dir - directory that holds training set.  The structure is 
    assumed to be:
        training_dir
            - category1
                - image_in_category1_1
                - image_in_category1_2
                ...
            - category2
                - image_in_category2_1
                - image_in_category2_2
                ...
            ...
    The names of categories will be taken from the name of their 
    subdirectory, and all images in that subdir are assigned to the 
    corresponding category.  

    Output:
    a tuple (image_files, categories)
    image_files - list of all training image filenames
    categories - list of the category of each training image, respectively
    '''
    if training_dir[-1] == '/':
        training_dir = training_dir[:-1]
    cat_names = [d for d in os.listdir(training_dir)
                    if os.path.isdir(training_dir + '/' + d)]
    cat_dirs = [training_dir + '/' + catagory for catagory in cat_names]
    categories = []
    image_files = []
    for cat_name, cat_dir in zip(cat_names, cat_dirs):
        images = [cat_dir + '/' + f for f in os.listdir(cat_dir) 
                                    if (os.path.isfile(cat_dir + '/' + f) and
                                        f[0] != '.')]
        categories += [cat_name]*len(images)
        image_files += images
    return image_files, np.array(categories)

def construct_classifier(training_dir, folds=20, 
                         classifier_file='trained_classifier.p'):
    '''
    Construct a random forest image classifier from the training data in 
    the passed directory.  The directory must be formated as described 
    in the function "prepare_training_set".  The final classifier will be 
    pickled as well as returned.

    Arguments:
    training_dir - directory of training data, for formating specifications
    see "prepare_training_set"
    folds - number of folds of cross_validation to preform, default is 20
    classifier_file - file destination for pickled final classifier, default
    is 'trained_classifier.p'

    Output:
    tuple (clf, accuracy)
    clf - final classifier object
    accuracy - median accuracy of classifier via cross validation
    '''
    initial_time = time.time()
    # get data, compute features
    image_files, categories = prepare_training_set(training_dir)
    featurizer = ImageFeaturizer(images=image_files)
    features = featurizer.get_features()
    feature_names = np.array(featurizer.feature_names())
    # shuffle and estimate accuracy with cross validation
    shuffle_index = np.arange(features.shape[0])
    npshuffle(shuffle_index)
    features = features[shuffle_index, :]
    categories = categories[shuffle_index, :]
    cv_splits = cval.KFold(len(categories), folds, shuffle=True)
    cv_scores = cval.cross_val_score(RandomForestClassifier(), features, 
                                     categories, cv=cv_splits, n_jobs=-1)
    accuracy = np.median(cv_scores)
    random_guessing = 1.0/len(np.unique(categories))
    # build classifier on full training set
    full_classifier = RandomForestClassifier(n_estimators=50, n_jobs=-1, 
                                             compute_importances=True)
    full_classifier.fit(features, categories)
    # output stats and save full classifier
    pickle.dump(full_classifier, open(classifier_file,'w'))
    final_time = time.time()
    print ("\nbuilt random forest classifier in {:.1f} sec, "
           "saved to: {}".format(final_time - initial_time, classifier_file))
    print "model accuracy: {:.3f}".format(accuracy)
    print "accuracy from random guessing: {:.3f}".format(random_guessing)
    improv_factor = (accuracy - random_guessing)/float(random_guessing)
    print ("improvement factor over random guessing: "
           "{:.1f}".format(improv_factor))
    importances = np.argsort(full_classifier.feature_importances_)[::-1]
    sorted_features = feature_names[importances]
    sorted_importances = full_classifier.feature_importances_[importances]
    sorted_importances = sorted_importances/np.max(sorted_importances)
    print "features by importance:"
    for n, (feature_name, importance) in \
                        enumerate(zip(sorted_features, sorted_importances)):
        print "{}\t{}\t{:.3f}".format(n+1 ,feature_name, importance)
    return full_classifier, accuracy

def run_final_classifier(path, forest='trained_classifier.p', 
                         print_results=True):
    '''
    Use classifier saved in the file forest to identify each in in the 
    directory path, results are printed to screen if print_results is True
    '''
    clf = pickle.load(open(forest, "rb"))
    if path[-1] == '/':
        path = path[:-1]
    images = [path + '/' + f for f in os.listdir(path) 
                             if (os.path.isfile(path + '/' + f) and
                                 f[0] != '.')]
    featurizer = ImageFeaturizer(images=images)
    features = featurizer.get_features()
    feature_names = np.array(featurizer.feature_names())
    results = clf.predict(features)
    print "filename\t\t\tcategory"
    print "------------------------------------------"
    for im, cat in zip(images, results):
        print "{}\t\t{}".format(im, cat)
    return images, results

#############################################################
