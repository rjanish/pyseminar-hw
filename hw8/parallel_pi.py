
from numpy.random import random

def compute_pi_pythonloop(n):
	'''
	Approximate pi using a monte-carlo dartboard, implemented using
	pure python loops.  n is the number of darts simulated.
	'''
	hits = 0
	for throw in xrange(int(n)):
		x, y = random(), random() # get point in quadrant I of [-1,1]x[-1,1]
		if x**2 + y**2 <= 1.0:	  
			hits += 1 			  # count if point is inside unit circle
	pi_approx = 4*hits/float(n)
	return pi_approx