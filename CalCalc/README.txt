CalCalc, v1.0
This is a module for evaluating strings either locally in python or by sending the string to wolfram alpha.  

Installation:
Download the source tarball from CalcCalc/dist, extract, and from the extraction directory run:
	$ python setup.py install
This will install the python module CalCalc

The primary module script CalCalc.py also implements the command line functionality.  This script will be placed into some packages directory depending on your python installation, likely something/lib/python2.7/site-packages/.  This directory needs to be added to your shell search path in order to use CalcCal.py from the command line. 

Tests are implemented in the module script CalCalc.py.  To run tests use:
	$ nosetests CalCalc.py 

Usage:
Evaluation is implemented in the calculate function in CalCalc.  To use from python:
	> from CalCalc import calculate
	> calculate("string to evaluate")
or from the command line:
	$ python CalCalc.py "string to evaluate"
For more details and options, see the calculate docstring or from the command line:
	$ python CalCalc.py --help
