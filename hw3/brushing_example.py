'''
example script illustrating the usage of brushing.py, here Anderson's 
iris data is plotted in a brush plot colored by species 

usage:
 	$ python brushing_example.py
requies that brushing.py be in the current directory and the datafile 
"flowers.csv" be located in a subdirectory "hw_3_data/"
'''

# homework 3, python seminar fall 2013
# Ryan Janish

import numpy as np
import brushing

def remove_string_field(struct_array, field):
	'''
	takes a structured array containing exactly one string field and 
	returns a float array with the string field removed and a 
	corresponding string array containing the old string fields
	'''
	field_values = np.unique(struct_array[field])
	try:
		field_values.sort()
	except:
		pass
	new_array = []
	removed_section = []
	for fv in field_values:
		other_fields = [n for n in struct_array.dtype.names if n != field]
		trimmed = struct_array[struct_array[field] == fv][other_fields]
		removed = struct_array[struct_array[field] == fv][field]
		floating = trimmed.view((float, len(trimmed.dtype.names)))
		new_array.append(floating)
		removed_section.append(removed)
	return np.vstack(new_array), np.hstack(removed_section)

################################################################	

# read data
flowers = np.loadtxt("hw_3_data/flowers.csv", 
					 dtype=[('sepal length',float), 
					 		('sepal width',float), 
					 		('petal length',float), 
					 		('petal width',float), 
					 		('species', 'S10')], skiprows=1, delimiter=',')

# extract species names as a seperate array
data, species = remove_string_field(flowers, 'species')
# map species to colors
colors = species.copy()
species_names = ['virginica', 'setosa', 'versicolor']
clrs_to_use = ['blue', 'green', 'red']
for spec, clr in zip(species_names, clrs_to_use):
	colors[colors==spec] = clr
# get names for dimensions
names = flowers.dtype.names[:-1]
# make brush plot
brushing.BrushingPlot(data, color=colors, dimension_names=names, 
				      title="Iris Flowers", figsize=(13,9))