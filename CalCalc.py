"""CalCalc: Module for evaluating strings locally or via wolfram alpha"""

# homework 2, python seminar fall 2013
# Ryan Janish

import argparse 
import urllib2
import re

def is_arithmetic(target):
	"""
	Check if target string contains only numbers, whitespace, and the
	arithmetic/comparison operators +-/=()%.*><, 
	"""
	unacceptable_chars = r"[^\d\s+-/=()%.*><,]"
	return (re.search(unacceptable_chars, target) is None)

def CalCalc(target, force_wolfram=False):
	"""
	Evaluate the target string.  For security, evaluation is only done 
	locally if the target string contains only numbers and arithmetic 
	operators.  Otherwise, or if local evaluation fails, the target 
	string is evaluated with wolfram alpha.
	"""
	wolfram = force_wolfram or not is_arithmetic(target)
	if not wolfram:
		try:
			results = eval(target)
		except:
			results = 'wolfram output'
	else:
		results = 'wolfram output'
	return results

if __name__ == '__main__':
	# process cmd line args
	parser = argparse.ArgumentParser("Generate a histogram")
	parser.add_argument("to_evaluate", type=str, help="string to evaluate")
	parser.add_argument("-w", action="store_true", dest="wolfram", default=False, 
						help="force evaluation using wolfram alpha")
	results = parser.parse_args()
	# evaluate input
	print CalCalc(results.to_evaluate, force_wolfram=results.wolfram)