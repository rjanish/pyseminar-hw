
import numpy as np 
from matplotlib import pyplot as plt

class BrushingPlot(object):
	'''
	Produces a matplotlib figure containing a grid of pairwise scatter
	plots of n-dimensional data that allow interactive brushing 

	arguments:

	data - The data to be plotted.  Must be interpretable as an array of 
	dimension two or three.  A single n-dimensional datapoint is 
	assumed to be given by fixing all but the last array dimension.  If the 
	array dimension is less than two, all points are plotted in the same
	color.  For array dimension three, the first dimension identifies the 
	color to be used for the data along that dimension. 

	color - Either a single matplotlib color given as a string, or a list of
	colors.  If a single color is given, then all datapoints are plotted with
	that color.  For a list of colors, the sets of datapoints along the first
	dimension of the data array will be colored respectively by the colors 
	given in the list.  
	'''
	def __init__(self, data, color='blue', dimension_names=None, 
				 title="Brushing Plot"):
		self.data = np.array(data)
		self.data_shape = self.data.shape
		self.datapnt_dim = self.data_shape[-1]
		# verify data shape
		if len(self.data_shape) > 3:
			raise Exception("Invalid data shape: {}".format(self.data_shape))
		# verify and initialize colors
		elif len(self.data_shape) == 2:
			if not isinstance(color, str):
				raise Exception("Invalid color specification {} " 
								"for data shape {}".format(color, 
														   self.data_shape))
			self.colors = [color]
		elif len(self.data_shape) == 3:
			colors_needed = self.data_shape[0]
			if isinstance(color, str):
				self.colors = [color]*colors_needed
			elif len(color) >= colors_needed:
				self.colors = color[:colors_needed]
			else:
				raise Exception("Invalid color specification {} " 
								"for data shape {}".format(color, 
														   self.data_shape))
		# verify and initialize dimension names
		if dimension_names is None:
			self.dim_names = map(str, range(self.datapnt_dim))
		elif len(dimension_names) >= self.datapnt_dim:
			self.dim_names = dimension_names[:self.datapnt_dim]
		else:
			raise Exception("Invalid dimension names {} " 
							"for data shape {}".format(dimension_names, 
													   self.data_shape))
		# construct figure, start interaction
		self.title = title
		self.initialize_figure()

	def initialize_figure(self):
		self.figure = plt.figure()
		# add axes to lower left subplot grid points
		grid_size = (self.datapnt_dim, self.datapnt_dim)
		y, x = np.indices(grid_size)
		upper_left = y >= x
		self.subplot_locations = zip(y[upper_left].flatten(),
							         x[upper_left].flatten())
		for loc in self.subplot_locations:
			ax = plt.subplot2grid(grid_size, loc)
		self.figure.tight_layout()
		# plot data, title, axis labels
		for loc, ax in zip(self.subplot_locations, self.figure.axes):
			y, x = loc
			y_data = self.data[..., y]
			x_data = self.data[..., x]
			for setx, sety, color in zip(x_data, y_data, self.colors):
				ax.scatter(setx, sety, c=color, edgecolor=None)
			ax.set_xlabel(self.dim_names[x])
			ax.set_ylabel(self.dim_names[y])
		self.figure.suptitle(self.title)

def struc_to_float(struct_array, field):
	field_values = np.unique(struct_array[field])
	try:
		field_values.sort()
	except:
		pass
	new_array = []
	for fv in field_values:
		other_fields = [n for n in struct_array.dtype.names if n != field]
		trimmed = struct_array[struct_array[field] == fv][other_fields]
		print trimmed
		floating = trimmed.view((float, len(trimmed.dtype.names)))
		new_array.append(floating)
	return np.array(new_array), field_values
