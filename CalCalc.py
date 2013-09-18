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

class ReadURL(object):
	"""
	This is a wrapper class around urllib2's urlopen function that provides 
	a context manager.  On entering it gets a stream from urlopen and 
	on exiting it closes the stream """
	def __init__(self, url):
		self.url = url

	def __enter__(self):
		self.stream = urllib2.urlopen(self.url)
		return self.stream

	def __exit__(self, type, value, traceback):
		self.stream.close()

def query_wolframalpha(request):
	"""
	Send the string request to wolfram alpha, and return the first 
	string 	that wolfram displays under the "Results" heading. If 
	no plain text result is received from wolfram, returns None. 
	"""
	request = str(request)
	# strip leading and trailing whitespace, replace all other whitespace
	# with the characters %20, as is the convention in wolfram urls
	wolfram_request = re.sub(r"\s", "%20", request.strip())
	# this is the conventional form for a wolfram search url, the string 
	# UAGAWR-3X6Y8W777Q is a wolfram app id for the python seminar course
	wolfram_url = ("http://api.wolframalpha.com/v2/query?input="
				   "{}&appid=UAGAWR-3X6Y8W777Q".format(wolfram_request))
	# get wolfram results, extract all 'results pod' matches.  The 
	# formating for these comes from examining a few wolfram search results.
	results_pod_re = re.compile(r"<pod title='Result'.*?</pod>", re.DOTALL)
	with ReadURL(wolfram_url) as wolfram_search:
		full_results = wolfram_search.read()
		results_pods = results_pod_re.finditer(full_results)
	# return the first chunk of plain text in a 'results pod' 
	plaintext_re = re.compile(r"<plaintext>(.*?)</plaintext>", re.DOTALL)
	for pod_match in results_pods:
		pod_string = pod_match.group() 
		result = plaintext_re.search(pod_string)
		if result is not None:
			return result.group(1)
	# no results pods contain a plain text answer
	return None

def calculate(target, force_wolfram=False):
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
			results = query_wolframalpha(target)
	else:
		results = query_wolframalpha(target)
	if results is None:
		results = "Result could not be found"
	return results

########################################################################

if __name__ == '__main__':
	# process cmd line args
	parser = argparse.ArgumentParser("Generate a histogram")
	parser.add_argument("to_evaluate", type=str, help="string to evaluate")
	parser.add_argument("-w", action="store_true", dest="wolfram", default=False, 
						help="force evaluation using wolfram alpha")
	results = parser.parse_args()
	# evaluate input
	print calculate(results.to_evaluate, force_wolfram=results.wolfram)