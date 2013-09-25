"""Script to generate plot of google and yahoo! stocks and ny temps"""

# homework 3, python seminar fall 2013
# Ryan Janish

import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

# load data 
data_dir = "hw_3_data/"
google = np.loadtxt(data_dir + "google_data.txt", skiprows=1)
temperature = np.loadtxt(data_dir + "ny_temps.txt", skiprows=1)
yahoo = np.loadtxt(data_dir + "yahoo_data.txt", skiprows=1)

# make plots
fig, ax_stock = plt.subplots()
ax_temp = plt.twinx(ax=ax_stock) # add right yaxis
ax_stock.plot(*google.T, color='blue', 
			  label="Google Stock Value")
ax_stock.plot(*yahoo.T, color='purple', 
			  label="Yahoo! Stock Value")
ax_temp.plot(*temperature.T, color='red', 
			 linestyle='--', label="NY Mon. High Temp")
ax_stock.plot([], [], color='red', linestyle='-', 
			  label="NY Mon. High Temp") # add placeholder plot for legend 

# limits and tick marks
ax_temp.set_ylim(-150, 100)
ax_stock.set_ylim(0, 800)
ax_stock.set_xlim(48800, 55600)
ax_stock.yaxis.set_ticks_position("left")
ax_stock.yaxis.set_minor_locator(AutoMinorLocator(5))
ax_stock.xaxis.set_ticks_position("bottom")
ax_stock.xaxis.set_minor_locator(AutoMinorLocator(5))
ax_temp.yaxis.set_ticks_position("right")
ax_temp.yaxis.set_minor_locator(AutoMinorLocator(5))

# labels, legend, and title
ax_temp.set_ylabel(r"Temperature ($^{o}$F)", fontsize=12)
ax_stock.set_ylabel("Value (Dollars)", fontsize=12)
ax_stock.set_xlabel("Date (MJD)", fontsize=12)
ax_stock.legend(loc="center left", frameon=False, fontsize=10)
ax_stock.set_title("New York Temperature, Google, and Yahoo!",
				   fontsize=20)

fig.savefig("stocks-temperatures.png")