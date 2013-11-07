'''script comparing various serial and parallel implementations'''

# homework 8, python seminar fall 2013
# Ryan Janish

from multiprocessing import Pool, cpu_count
from subprocess import call
from functools import partial
from time import time

import numpy as np
from numpy.random import random
from IPython import parallel

def count_hits_loop(n):
	''' 
	Simulate n dart throws into the first quadrant of [-1,1]x[-1,1] 
	and count the number of throws inside the unit circle. 
	Implemented with a pure python loop.
	'''
	hits = 0
	for throw in xrange(int(n)):
		x, y = random(), random()
		if x**2 + y**2 <= 1.0:	  
			hits += 1
	return hits			  

def count_hits_numpy(n):
	''' 
	Simulate n dart throws into the first quadrant of [-1,1]x[-1,1] 
	and count the number of throws inside the unit circle. 
	Implemented with a numpy vectorized array
	'''
	rsq = random(n)**2 + random(n)**2
	hits = np.sum(rsq <= 1)
	return hits		

def compute_pi_serial(n, style='numpy'):
	'''
	Approximate pi using a monte-carlo dartboard, implemented using	
	either 	python loops or numpy, depending on the value of 'style'.  
	n is the number of darts simulated. Execution is timed. 
	'''
	if style == 'numpy':
		counter = count_hits_numpy
	else:
		counter = count_hits_loop
	start = time()
	hits = counter(n)
	exec_time = time() - start
	return 4*hits/float(n), exec_time

def compute_pi_multiprocessing(n, cores=None, style='numpy'):
	'''
	Approximate pi using a monte-carlo dartboard, implemented using
	pure python loops parallelized over the passed number of cores. 
	Parallelization is done using the multiprocessing module. If 
	cores=None then the default number of cores detected by multiprocessing
	will be used. n is the number of darts simulated. Execution is timed. 
	'''
	if cores is None:
		cores = cpu_count()
	else:
		cores = int(cores)
	if style == 'numpy':
		counter = count_hits_numpy
	else:
		counter = count_hits_loop
	start = time()
	workers = Pool(cores)
	hits_parallel = workers.map(counter, [n/cores]*cores)
	hits = sum(hits_parallel)
	exec_time = time() - start
	return 4*hits/float(n), exec_time

def compute_pi_ipythoncluster(n, cores=4):
	'''
	Approximate pi using a monte-carlo dartboard, implemented using
	pure python loops parallelized over the passed number of cores. 
	Parallelization is done with an ipython cluster. n is the number 
	of darts simulated.
	'''
	call(['ipcluster', 'start',  '-n',  '4'])
	rc = parallel.Client()
	dview = rc[:]
	dview.apply(count_hits, n/int(cores))

	call(['ipcluster', 'stop'])

if __name__ == '__main__':
	# run each serial/parallel method with both loops and numpy 
	# for 10 log-spaced samples between 10 and 10**8
	calculators = {'serial':compute_pi_serial, 
				   'multiprocessing':compute_pi_multiprocessing}
	results = {'Error':{}, 'Execution Time':{}, 'Simulation Rate':{}}
	dart_number = np.int64(np.logspace(1, 8, num=10))
	for style in ['loop', 'numpy']:
		for calc_type in calculators:
			label = "{}-{}".format(calc_type, style)
			for result in results:
				results[result][label] = []
			for n in dart_number:
				pi_approx, t = calculators[calc_type](n, style=style)
				frac_error = np.absolute(np.pi-pi_approx)/np.pi
				results["Error"][label].append(frac_error)
				results["Execution Time"][label].append(t)
				results["Simulation Rate"][label].append(n/t)
	# plot results			
	from matplotlib import pyplot as plt
	fig, axs = plt.subplots(3, 1)
	for ax, parameter in zip(axs, results.keys()):
		for run in results[parameter]:
			ax.loglog(dart_number, results[parameter][run], label=run)
			ax.set_title(parameter, fontsize=12)
	plt.legend(fontsize=10, loc='lower left')
	plt.suptitle("Monte Carlo Comparison - Linux Laptop, "
				 "4-Core 2.8 GHz Intel i7", fontsize=14)
	plt.show()


