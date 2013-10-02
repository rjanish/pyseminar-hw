
import os
import sys
import pickle

import numpy as np
from numpy.random import shuffle as npshuffle
from scipy.ndimage import imread
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation as cval

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

    def feature_names(self):
        return [feature_func.func_name for feature_func 
                                       in self.features_to_use]

    # begin feature calculators
    def red_fraction(self, image):
        if len(image.shape) == 3:
            return image[:,:,0].sum()/float(image.sum())
        else:
            return 0.0

    def blue_fraction(self, image):
        if len(image.shape) == 3:
            return image[:,:,1].sum()/float(image.sum())
        else:
            return 0.0

    def green_fraction(self, image):
        if len(image.shape) == 3:
            return image[:,:,2].sum()/float(image.sum())
        else:
            return 0.0


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
    print ("\nbuilt random forest classifier, "
           "saved to: {}".format(classifier_file))
    print "model accuracy: {:.3f}".format(accuracy)
    print "accuracy from random guessing: {:.3f}".format(random_guessing)
    improv_factor = (accuracy - random_guessing)/float(random_guessing)
    print ("improvement factor over random guessing: "
           "{:.1f}".format(improv_factor))
    importances = np.argsort(full_classifier.feature_importances_)
    sorted_features = feature_names[importances]
    print "three most important features:"
    for feature_name in sorted_features[:3]:
        print "\t{}".format(feature_name)
    return full_classifier, accuracy

def run_final_classifier(path, forest='trained_classifier.p', 
                         print_results=True):
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
    return

#############################################################
