''' Bayesian model for batting averages '''

# homework 10, python seminar fall 2013
# Ryan Janish

# Model:
# Let N be at-bats, x be hits, and avg be the true average.
# The observed hits is modeled as p(x|avg) = Binomial(avg, N).
# Use beta distribution priors on avg, with the hyperparameters set
# to match the mean and variance of the 2010 all player batting data 

import pymc as pm 
import numpy as np
from pandas import read_table


def get_beta_params(mean, variance):
    ''' 
    returns the alpha and beta parameters of a beta 
    distribution with the given mean and variance
    '''
    mean, variance = float(mean), float(variance)
    alpha = -mean*(variance + mean**2 - mean)/variance
    beta = (mean - 1)*(variance + mean**2 - mean)/variance
    return alpha, beta

# read observed x and N for april 2011
baseball_data = read_table("laa_2011_april.txt", sep=r"\s*")
batting = baseball_data[["Player", "H", "AB"]]
x_obv = np.array(batting['H'].astype(np.float64))
N_obv = np.array(batting['AB'].astype(np.float64))

# model definition 
mean, variance = 0.255, 0.0011 # mean, variance over all players in 2010
alpha, beta = get_beta_params(mean, variance)
avg = pm.Beta('avg', alpha, beta, size=x_obv.size)
x = pm.Binomial('x', N_obv, avg, observed=True, value=x_obv)