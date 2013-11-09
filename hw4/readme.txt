
image_classifier.py
This module contains functions for easily building and using a random forest classifier for image sorting.


Usage:
----------------------------
Building a classifier:
The classifier constructor needs a directory of training images sorted into subdirectories by image category.  If this directory is called "training_dir", then it must have the structure:
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
The names 'category1', 'category2', etc., will be used as labels for the categories in the classifier.  Building the classifier requires the function call:
    > clf, accuracy = construct_classifier('training_dir')
This will return the classifier object and its median accuracy as determined by a 20-fold cross-validation, in addition the classifier object will be pickeled to "trained_classifier.p".  It will also print to stdout the run time, accuracy statistics, and feature importance.  For optional arguments see the doc string.

Using a classifier:
The function run_final_classifier can be used to apply a classifier stored on disk to a directory of images.  For a directory called 'path', which contains image files, and a file 'clf_pickle' which contains a pickeled classifier
object, the images in 'path' can be sorted with the function call:
    > images, results = run_final_classifier('path', forest='clf_pickel')
This will return a list of image filename and a corresponding list of the 
image categories, as well as print to stdout the predicted category of each image.
By default, this will use the filename "trained_classifier.p" for the forest argument, but no default is specified for the path argument.  For details see the doc sting.  

features
--------------
image_classifier.py makes use of the following 29 features:

COLOR_frac - fraction of total luminosity in the COLOR, where COLOR takes values of red, green and blue.

COLOR_std - standard deviation of COLO luminosities, where COLOR takes values of red, green and blue.

im_std - standard deviation of grayscale image

rgb_theta and rgb_phi - The image is represented by a point in R^3, with the three coordinates given by the total luminosities of the red, green, and blue color channels.  The spherical coordinate angles theta and phi of this point in rgb-space are computed. 

frac_peaks - fraction of all grayscale pixels that are local maxima

frac_valleys = fraction of all grayscale pixels that are local minima

frac_hedges and frac_vedges - fraction of all grayscale pixels that lie on sharp vertical and horizontal edges in the image interior

gXY - The image is divided into 16 subimages via a rectangular 4x4 grid. gXY is the fraction of total grayscale luminosity located in the subimage with grid coordinates (x,y).


50_categories example
----------------------------
To build a classifier on the 50_categories.zip dataset, unpack this to some directory '50_categories/', so that '50_categories/' has the format described above.
From the directory containing '50_categories/', call the following from an ipython interpreter:
    > run image_classifier.py
    > construct_classifier('50_categories')
To use the classifier on new images, place those images in some directory, call it 'unclassified', and call from the directory where the above calls were made:
    > run_final_classifier("unclassified")
This will output the predicted category of the new images.  
Note that it's important to remain in the same directory for all of these commands, as construct_classifier will write the random forest model to the file "trained_classifier.p" in the current directory, and run_final_classifier will look for it in the current directory. 

50_categories performance
------------------------------
On the 50_categories dataset, construct_classifier takes about 4 minutes to build a model on my machine.  The classifier has the following score: 
    model accuracy (fraction correct): 0.226
    accuracy from random guessing (fraction correct): 0.020
    improvement factor over random guessing: 10.3
    rank    feature         relative importance
    ----------------------------------------------
    1       frac_hedges     1.000
    2       frac_peaks      0.902
    3       frac_vedges     0.820
    4       frac_valleys    0.732
    5       green_frac      0.681
    6       rgb_theta       0.617
    7       g41             0.612
    8       blue_frac       0.604
    9       g23             0.591
    10      red_frac        0.590
    11      blue_std        0.589
    12      g22             0.585
    13      g33             0.580
    14      g14             0.575
    15      g44             0.574
    16      green_std       0.569
    17      g32             0.568
    18      red_std         0.566
    19      rgb_phi         0.565
    20      g34             0.553
    21      g12             0.549
    22      g11             0.549
    23      g21             0.545
    24      g34             0.537
    25      g42             0.535
    26      g13             0.534
    27      im_std          0.529
    28      g34             0.526
    29      g31             0.523

validation 
---------------
The script 'validation_set.py' will run the previously trained model 'trained_classifier.p' on the provided validation images.  This has been done, and the results are summarized in 'results.txt' and 'confusion_matrix.pdf'