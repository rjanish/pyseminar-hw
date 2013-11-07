
import numpy as np
from numpy.random import random

def count_hits(n):
	''' 
	Simulate n dart throws into the first quadrant of [-1,1]x[-1,1] 
	and count the number of throws inside the unit circle
	'''
	hits = 0
	for throw in xrange(int(n)):
		x, y = random(), random()
		if x**2 + y**2 <= 1.0:	  
			hits += 1 
	return hits			  

def compute_pi_pythonloop(n):
	'''
	Approximate pi using a monte-carlo dartboard, implemented using
	pure python loops.  n is the number of darts simulated.
	'''
	hits = 0
	pi_approx = 4*count_hits(n)/float(n)
	return pi_approx

def compute_pi_numpy(n):
	'''
	Approximate pi using a monte-carlo dartboard, implemented with 
	numpy vectorization.  n is the number of darts simulated.
	'''
	x, y = random(n), random(n) # n points in quadrant I of [-1,1]x[-1,1]
	rsq = x**2 + y**2
	hits = np.sum(rsq <= 1)		# count number of points inside unit circle
	pi_approx = 4*hits/float(n)
	return pi_approx
