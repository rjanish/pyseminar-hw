
from multiprocessing import Pool, cpu_count
from subprocess import call
from functools import partial
import time

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
	x, y = random(n), random(n) 
	rsq = x**2 + y**2
	hits = np.sum(rsq <= 1)
	return hits		

def compute_pi_serial(n, style='numpy'):
	'''
	Approximate pi using a monte-carlo dartboard, implemented using	
	either 	python loops or numpy, depending on the value of 'style'.  
	n is the number of darts simulated.
	'''
	if style == 'numpy':
		hits = count_hits_numpy(n)
	else:
		hits = count_hits_loop(n)
	return 4*hits/float(n)

def compute_pi_multiprocessing(n, cores=None, style='numpy'):
	'''
	Approximate pi using a monte-carlo dartboard, implemented using
	pure python loops parallelized over the passed number of cores. 
	Parallelization is done using the multiprocessing module. If 
	cores=None then the default number of cores detected by multiprocessing
	will be used. n is the number of darts simulated.
	'''
	if cores is None:
		cores = cpu_count()
	else:
		cores = int(cores)
	workers = Pool(cores)
	hits_parallel = workers.map(count_hits, [n/cores]*cores)
	hits = sum(hits_parallel)
	return 4*hits/float(n)

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

