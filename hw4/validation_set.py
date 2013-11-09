'''
This script will test the image classifier built in 'image_classifier.py'
and saved to 'trained_classifier.p' on the provided set of validation images.
This classifier was previously trained on the images provided with the
original homework.  
'''
from os import listdir

from matplotlib import pyplot as plt 
from sklearn.metrics import accuracy_score, confusion_matrix

from image_classifier import run_final_classifier as predict

# calculate actual and predicted subject of each validation image
actual, predicted, imnames = [], [], []
validation_dir = "validation_images"
for subject in listdir(validation_dir):
	if subject[0] != '.':
		images, classes = predict("{}/{}/".format(validation_dir, subject))
		predicted += list(classes)
		imnames += [filename.split('/')[-1] for filename in images]
		actual += [subject]*len(classes)

# compute accuracy, confusion matrix
score = accuracy_score(actual, predicted)
print score
con_matrix = confusion_matrix(actual, predicted)
plt.imshow(con_matrix, interpolation="nearest", origin="upper")
plt.savefig("confusion_matrix.pdf")
plt.close("all")

# write results
results_file = file("results.txt", "w")
results_file.write("Predicted image classes for Ryan Janish's classifier\n")
results_file.write("Accuracy score: {}\n\n".format(score))
results_file.write("filename\t\tpredicted_class\n")
results_file.write("-----------------------------------------\n")
for filename, prediction in zip(imnames, predicted):
    results_file.write("{}\t{}\n".format(filename, prediction))
results_file.close()