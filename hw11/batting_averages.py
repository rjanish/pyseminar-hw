''' This script computes a bayesian estimate of batting averages '''

# homework 10, python seminar fall 2013
# Ryan Janish

import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import pymc as pm

# read stats for 2011 
april_data = pd.read_table("laa_2011_april.txt", sep=r"\s*")
april_batting = april_data[["Player", "H", "AB"]]
for column in ["H", "AB"]:
    april_batting[column] = april_batting[column].astype(np.float64)
full = pd.read_table("laa_2011_full.txt", sep=r"\s*")
full_batting = full[["Player", "H", "AB"]]
for column in ["H", "AB"]:
    full_batting[column] = full_batting[column].astype(np.float64)
full_averages = np.array(full_batting["H"]/full_batting["AB"])

# maximum likelihood estimate; avg = hits/at-bats
mle_averages = np.array(april_batting["H"]/april_batting["AB"])

# bayesian estimate
import batting_model
M = pm.MCMC(batting_model)
print "generating posterior distributions:"
M.sample(iter=10000, burn=1000, thin=2)
print ''
post_samples = M.trace('avg')[:]
players = np.array(april_data.Player)
# save traces
for player_num, player in enumerate(players):
    fig, ax = plt.subplots(1,1)
    ax.plot(post_samples[:, player_num])
    ax.set_title("MCMC trace for {}".format(player))
    fig.savefig("trace-{}.png".format(player))
# get mean, confidence intervals 
summary = M.stats()['avg']
low = summary['quantiles'][2.5]
high = summary['quantiles'][97.5]
means = summary['mean']
print "\npredicted mean batting average:"
for player_num, player in enumerate(players):
    print "{}\t\t{:.3f}".format(player, means[player_num])
print "\npredicted 95% confidence interval batting average:"
for player_num, player in enumerate(players):
    print "{}\t\t{:.3f}, {:.3f}".format(player, low[player_num], 
                                        high[player_num])
# check for real averages outside CI
print "\nactual 2011 batting average:"
for player_num, player in enumerate(players):
    print "{}\t\t{:.3f}".format(player, full_averages[player_num])

fails = (full_averages < low) | (high < full_averages)
print ("\nnumber of actual averages outside the estimated"
       " confidence interval: {}/{}".format(np.sum(fails), len(fails)))
# plot mle and bayesian estimates vs true values
fig, ax = plt.subplots(1,1)
ax.plot(full_averages, full_averages, '-r', alpha=0.7, 
        label="Full 2011 AVG")
ax.plot(full_averages, mle_averages, 'og', alpha=0.7,
        label="Maximum Likelihood Estimate of AVG")
ax.errorbar(full_averages, means, yerr=[means - low, high - means], 
            alpha=0.7, marker='o', linestyle='', 
            label="Bayesian Estimate of AVG")
ax.set_title("Estimates of full 2011 AVG from April 2011 stats")
ax.set_xlabel("Full 2011 AVG")
ax.set_ylabel("Batting Averages")
ax.legend(loc='lower right', fontsize=12)
fig.savefig("batting_averages.png")
