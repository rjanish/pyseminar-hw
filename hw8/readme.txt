
This script compares various serial and parallel implementations of a monte carlo dart board simulation to approximate pi.  There are four methods tested: a serial implementation and a parallel implementation using multiprocessing, and for each a these a method using pure python loops and one using vectorized numpy arrays. 

monte-carlo-comparison.pdf contains a plot of the output as run on my machine, giving the execution time, simulation rate, and accuracy as a function of the number of simulation realizations.  To reproduce this, simply run the script:
	$ python parallel_pi.py
which will regenerate the plot. Note that the cpu info displayed in the plot title is hard-coded and will not probably not be accurate when run on a different machine.  

The two parallel methods are slower until about N > 10**5, due to the overhead of setting up the parallel computations.  