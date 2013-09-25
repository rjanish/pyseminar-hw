"""Script to generate plot of efficiency and purity of grb follow ups"""

# homework 3, python seminar fall 2013
# Ryan Janish

import numpy as np 
import matplotlib.pyplot as plt

# load data 
data_dir = "hw_3_data/"
effciency = np.loadtxt(data_dir + "Efficiency.txt", skiprows=2)
purity = np.loadtxt(data_dir + "Purity.txt", skiprows=2)

# make plots
closest_02 = []
fig, [ax_left, ax_right] = plt.subplots(1, 2)
fig.tight_layout(pad=3)
for ax, data in zip([ax_left, ax_right], [effciency, purity]):
	ax.set_aspect("equal")
	# full data
	ax.plot(data[:,0], data[:,1], color='black', linestyle='-',)
	ax.fill_between(data[:,0], data[:,1] - data[:,2], data[:,1] + data[:,2],
					facecolor='gray', alpha=0.4)
	# 0.2 line
	closest = data[np.argmin(np.abs(data[:,0] - 0.2)), 1]
	closest_02.append(closest)
	ax.axvline(0.2, ymin=0.05, ymax=closest,
			   color='black', linestyle=':', linewidth=2)
# result for random guessing
ax_left.plot([0,1], [0,1], color='black', linestyle='-')
purity_guessing_level = 18.0/135.0
ax_right.axhline(purity_guessing_level, xmin=0.05, xmax=0.95, 
				 color='black', linestyle='-')

# limits and tick marks
for ax in [ax_left, ax_right]:
	ax.set_aspect("equal")
	ax.set_ylim(-0.05, 1.05)
	ax.set_xlim(-0.05, 1.05)
	ax.tick_params("both", direction="out", labelsize='8',
				   top=False, right=False)

# annotations 
ax_left.annotate("Random\nguessing", xy=(0.8, 0.8),
				 xytext=(0.7, 0.5), fontsize=10,
				 arrowprops=dict(facecolor='black', shrink=0.1, 
								 width=1, headwidth=5))
ax_left.annotate("Follow 20% of bursts\nto capture ~50%\nof high-z events", 
				 xy=(0.2, closest_02[0]), xytext=(0.4, 0.1), fontsize=10, 
				 arrowprops=dict(facecolor='black', shrink=0.05, 
				 	    		 width=1, headwidth=5))
ax_right.annotate("Random\nguessing", xy=(0.7, purity_guessing_level),
				 xytext=(0.6 ,0.4), fontsize=10,
				 arrowprops=dict(facecolor='black', shrink=0.05, 
								 width=1, headwidth=5))
ax_right.annotate("If 20% of events are\nfollowed up, ~40% of\nthem will be high-z", 
				 xy=(0.2, closest_02[1]), xytext=(0.05, 0.8), fontsize=10, 
				 arrowprops=dict(facecolor='black', shrink=0.05, 
				 	    		 width=1, headwidth=5))
# labels and title
ax_left.set_ylabel("Fraction of z > 4 GRBs Observed", fontsize=10)
ax_left.set_xlabel("Fraction of GRBs Followed Up", fontsize=10)
ax_left.set_title("Efficiency", fontsize=20, weight='medium')
ax_right.set_ylabel("Percent of Observed GRBs with z > 4", fontsize=10)
ax_right.set_xlabel("Fraction of GRBs Followed Up", fontsize=10)
ax_right.set_title("Purity", fontsize=20, weight='medium')

fig.savefig("efficiency-purity.png")