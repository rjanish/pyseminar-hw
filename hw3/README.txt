stocks-plot.py
This script generates a plot of Yahoo! and Google stock prices and New York temperatures.  Usage is:
	$ python stocks-plot.py
This script assumes that it is run from a directory containing a subdirectory "hw_3_data/", which contains the data files "google_data.txt", "ny_temps.txt", and "yahoo_data.txt".  The plot will be written to "stocks-temperatures.png".


efficiency-purity-plot.py
This script generates a annotated plot of efficiency and purity of high-z grb follow up observations.  Usage is:
	$ python efficiency-purity-plot.py
This script assumes that it is run from a directory containing a subdirectory "hw_3_data/", which contains the data files "Efficiency.txt" and "Purity.txt".  The plot will be written to "efficiency-purity.png".


brushing.py
This defines the BrushingPlot class.  For class usage see the docstring of BrushingPlot.  A subset of BrushingPlot's functionality is accessible via the command line from "brushing.py", for usage see:
	$ python brushing.py --help
This class implements brushing of a pairwise n-dimensional scatter plot, with a few caveats:  
- Brushing is rather slow
- Brushing only updates after the rectangle has been drawn, it does not update in real time
To select data, simply click and drag on a plot to make a selection rectangle, and then release to see the brushed data.  Clicking anywhere on the figure will remove the rectangle and allow you to draw a new one.


brushing_example.py
An example of using BrushingPlot on the Anderson Iris data, for usage see the scripts docstring.