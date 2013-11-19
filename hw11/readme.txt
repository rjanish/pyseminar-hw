'batting_averages.py'

This script computes a Bayesian and MLE estimate of the 2011 batting averages of 13 players using their April 2011 average.  To run this, call:
	$ python batting_averages.py
This script requires that current directory contain the two datafiles "laa_2011_april.txt" and "laa_2011_full.txt" and the Bayesian model file "batting_model.py".  

The Bayesian model assumes that the number of hits in April 2011 is a binomial distributed random variable with average given by the true 2011 batting average.  These batting averages are given priors of a beta distribution with mean and variance matching the mean and variance of batting averages of all player in 2010.  This model is defined in the script "batting_model.py".  Distributions for the full 2011 averages are generated using MCMC sampling. 

Outputs:
The Bayesian estimates and 95% confidence intervals will be printed to the screen, as will the actual averages.  The number of players for which the actual averages are not in the predicted confidence intervals is also printed.  Plots of the MCMC sampling for each player are saved in the current directory to verify convergence and are given the names "trace-PLAYER.png".  A plot of the Bayesian estimate, MLE, and the true averages are saved in the current directory as "batting_averages.png".