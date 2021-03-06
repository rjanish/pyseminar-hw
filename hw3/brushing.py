'''defines BrushingPlot class, used to make pairwise brushed scatter plots'''

# homework 3, python seminar fall 2013
# Ryan Janish

import argparse
import numpy as np 
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

class BrushingPlot(object):
	'''
	Produces a matplotlib figure containing a grid of pairwise scatter
	plots of n-dimensional data that allow interactive brushing 

	arguments:

	data - The data to be plotted.  Must be interpretable as an array of 
	shape (number_of_data_points, dimension_of_single_data_point).  A single 
	n-dimensional datapoint is assumed to be given by fixing the zeroth 
	dimension of the data array and allowing the first to vary.   

	color - Either a single matplotlib color given as a string, or a list of
	colors with the same length as the zeroth dimension of the data array.  
	If a single color is given, then all datapoints are plotted with
	that color.  For a list of colors, each datapoint is plotted with the 
	corresponding color from the colors list.  

	dimension_names - give the name of each dimension of the datapoints, to
	be displayed on the axis of the plots

	title - overall title of figure

	figsize - tuple that gives the size of resulting figure in inches, if 
	not specified, matplotlib's default will be used
	'''
	def __init__(self, data, color='blue', dimension_names=None, 
				 title="Brushing Plot", figsize=None):
		self.data = np.array(data)
		data_shape = self.data.shape
		# verify data shape
		if len(data_shape) != 2:
			raise Exception("Invalid data shape: {}".format(data_shape))
		self.num_datapoints, self.datapnt_dim = data_shape
		# verify and initialize colors
		if isinstance(color, str):
			self.colors = np.array([color]*self.num_datapoints)
		elif len(color) >= self.num_datapoints:
			self.colors = np.array(color[:self.num_datapoints])
		else:
			raise Exception("Invalid color specification {} for "
							"data shape {}".format(color, data_shape))
		# verify and initialize dimension names
		if dimension_names is None:
			self.dim_names = map(str, range(self.datapnt_dim))
		elif len(dimension_names) >= self.datapnt_dim:
			self.dim_names = dimension_names[:self.datapnt_dim]
		else:
			raise Exception("Invalid dimension names {} for data "
							"shape {}".format(dimension_names, data_shape))
		self.figsize = figsize
		# initialize brushing data
		self.target_axis = None
		self.rec_start = None
		self.rec = None
		# construct figure, start interaction
		self.title = title
		self.initialize_figure()
		self.connect()
		plt.show()

	def initialize_figure(self):
		'''make static figure of pairwise scatter plots'''
		if self.figsize is None:
			self.figure = plt.figure()
		else:
			self.figure = plt.figure(figsize=self.figsize)
		# add axes to lower left subplot grid points
		grid_size = (self.datapnt_dim, self.datapnt_dim)
		y, x = np.indices(grid_size)
		upper_left = y >= x
		self.subplot_locations = zip(y[upper_left].flatten(),
							         x[upper_left].flatten())
		for loc in self.subplot_locations:
			ax = plt.subplot2grid(grid_size, loc)
			ax.set_label("{}-{}".format(loc[0], loc[1]))
		self.figure.tight_layout(pad=2)
		# plot data, title, axis labels
		self.collections = []
		self.limits = []
		for loc, ax in zip(self.subplot_locations, self.figure.axes):
			grid_y, grid_x = loc
			y_data = self.data[..., grid_y]
			x_data = self.data[..., grid_x]
			new_colletcion = ax.scatter(x_data, y_data, 
									    c=self.colors, alpha=1.0)
			self.collections.append([new_colletcion])
			ax.set_xlabel(self.dim_names[grid_x], fontsize=14)
			ax.set_ylabel(self.dim_names[grid_y], fontsize=14)
			self.limits.append([ax.get_xlim(), ax.get_ylim()])
		self.figure.suptitle(self.title, fontsize=25)

	def update_plot(self):
		'''
		removes current scatter plot points, determines which points are
		currently selected by a the rectangle, and re-plots the scatter 
		plots with appropriate shading
		'''
		if self.rec is not None:
			label = self.rec.axes.get_label()
			y, x = map(int, label.split('-'))
			y_data = self.data[:,y]
			x_data = self.data[:,x] 
			xmin, ymin = self.rec.xy
			xmax, ymax = xmin + self.rec.get_width(), ymin + self.rec.get_height()
			vert = (ymin < y_data) & (y_data < ymax)
			hor  = (xmin < x_data) & (x_data < xmax)
			selected = vert & hor
			alph_bright = 1.0
			alph_dim = 0.01
		else:
			selected = np.zeros(self.num_datapoints, dtype=bool)	
			alph_bright = 0
			alph_dim = 1.0
		for ax_num, ax in enumerate(self.figure.axes):
			for collection in self.collections[ax_num]:
				collection.remove()
			grid_y, grid_x = self.subplot_locations[ax_num]
			y_data = self.data[..., grid_y]
			x_data = self.data[..., grid_x]
			bright = ax.scatter(x_data[selected], 
								y_data[selected], 
								c=self.colors[selected], alpha=alph_bright)
			dim = ax.scatter(x_data[~selected], 
								y_data[~selected], 
								c=self.colors[~selected], alpha=alph_dim)
			ax.set_xlim(self.limits[ax_num][0])
			ax.set_ylim(self.limits[ax_num][1])
			self.collections[ax_num] = [bright, dim]
			self.figure.canvas.draw()

	def on_press(self, event):
		'''initialize hollow rectangle object, update plot'''
		if self.rec is not None:
			self.rec.remove()
			self.figure.canvas.draw()
			self.rec = None
			self.update_plot()
		ax_clicked = event.inaxes
		if ax_clicked in self.figure.axes:
			self.target_axis = ax_clicked
			self.rec_start = event.xdata, event.ydata

	def on_movement(self, event):
		'''resize rectangle to match cursor position'''
		if (self.target_axis is not None) and (self.rec_start is not None):
			if event.inaxes is self.target_axis:
				if self.rec is not None:
					self.rec.remove()
					self.figure.canvas.draw()
				# update rectangle
				current_pos = event.xdata, event.ydata
				self.rec = corners_to_rec(self.rec_start, current_pos)
				self.target_axis.add_patch(self.rec)
				self.figure.canvas.draw()

	def on_release(self, event):
		'''freeze rectangle'''
		self.target_axis = None
		self.rec_start = None
		self.update_plot()

	def connect(self):
		'''connect all event handlers'''
		self.cid_press = self.figure.canvas.mpl_connect('button_press_event',
														self.on_press)
		self.cid_move = self.figure.canvas.mpl_connect('motion_notify_event',
														self.on_movement)
		self.cid_release = self.figure.canvas.mpl_connect('button_release_event',
														  self.on_release)

def corners_to_rec(c1, c2, fill=False):
	'''
	c1 and c2 are any two Cartesian coordinates, this returns the rectangle
	they span as a matplotlib rectangle patch object
	'''
	c1, c2 = np.array(c1), np.array(c2)
	min_x, min_y = np.minimum(c1, c2)
	max_x, max_y = np.maximum(c1, c2)
	lower_left = min_x, min_y
	width = max_x - min_x
	height = max_y - min_y
	rect = Rectangle(lower_left, width, height, fill=fill)
	return rect

#################################################################

if __name__ == '__main__':
	# process cmd line args
	parser = argparse.ArgumentParser("Generate a Brushing Plot")
	parser.add_argument("datafile", type=str, 
						help="datafile to plot, must be formated as whitespace delimited columns of numbers with a one-line header")
	results = parser.parse_args()
	# make plot
	print "plotting {}".format(results.datafile)
	data = np.loadtxt(results.datafile, skiprows=1)
	plot_title = results.datafile
	with open(results.datafile, 'r') as datafile:
		header = datafile.readlines()[0].split()
	if len(header) >= data.shape[1]:
		BrushingPlot(data, dimension_names=header, title=plot_title)
	else:
		BrushingPlot(data, title=plot_title)