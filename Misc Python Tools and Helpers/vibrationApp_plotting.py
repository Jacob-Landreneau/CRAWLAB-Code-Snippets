#! /usr/bin/env python

###############################################################################
# vibrationApp_plotting.py
#
# script to plot data from the csvs generated by the Vibrations iOS app
#   * https://itunes.apple.com/us/app/vibration/id301097580?mt=8
#   * http://www.dld-llc.com/Diffraction_Limited_Design_LLC/Vibration.html
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 04/01/16
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
###############################################################################

import numpy as np
import matplotlib.pyplot as plt

import tkinter
from tkinter import filedialog
import csv
from scipy import signal


## Read in the text file to parse
# root = tkinter.Tk()
# 
## This line may need to be commented out in Windows
# root.withdraw()
# 
# file_name = filedialog.askopenfilename()

# file_name = '/Users/josh/Documents/Research/Cable Driven Systems/Cable Driven Systems - HiBot Direct/Feb 2016 Visit/Data/VibrationData 2016-02-07 at 10 47 52-email.csv'
# file_name = '/Users/josh/Documents/Research/Cable Driven Systems/Cable Driven Systems - HiBot Direct/Feb 2016 Visit/Data/VibrationData 2016-02-07 at 10 49 23-email.csv'
file_name = '/Users/josh/Documents/Research/Cable Driven Systems/Cable Driven Systems - HiBot Direct/Feb 2016 Visit/Data/VibrationData 2016-02-07 at 11 45 19-email.csv'
# file_name = '/Users/josh/Documents/Research/Cable Driven Systems/Cable Driven Systems - HiBot Direct/Feb 2016 Visit/Data/VibrationData 2016-02-07 at 11 48 26-email.csv'

# Let's grab the metadata the beginning of the file
with open(file_name, 'rt') as file:
    reader = csv.reader(file)
    row_number = 0
    for row in reader:
        row_number = row_number + 1
        
        # row 2 defines the source, accelerometer or gyroscopes
        if row_number == 2:
            source = row[1]
        
        if row_number == 5:
            number_of_points = int(row[0])

        if row_number == 6:
            sample_rate_Hz = float(row[0])
            sample_time = 1 / sample_rate_Hz

        if row_number == 7:
            longitude = float(row[0])

        if row_number == 8:
            latitude = float(row[0])

        # the tenth row defines what domain the frequency data is in (accel, vel, or pos)
        if row_number == 10:
            freq_data = row[1]
            
        if row_number == 11:
            break
            
            
    # Now read the actual data
    
    # Define an empty array for the time-series data
    # We know the length of this data, so define it here
    time_data = np.zeros((number_of_points, 4))
    
    # define an empty array for freq_data
    # We don't know it's length, so we'll have to append each value
    freq_data = np.empty((1,4))
    
    # The first 10 rows have already been read, so we just need to read the data
    row_number = 0
    for row in reader:
        row_number = row_number + 1
        
        if row_number <= (number_of_points):
            time_data[row_number - 1,:] = [float(item) for item in row]
        
        if row_number > number_of_points + 4:
            freq_data = np.append(freq_data, [[float(item) for item in row]], axis=0)


# Plot the time series data    
# Set the plot size - 3x2 aspect ratio is best
fig = plt.figure(figsize=(6,4))
ax = plt.gca()
plt.subplots_adjust(bottom=0.17, left=0.17, top=0.96, right=0.96)

# Change the axis units font
plt.setp(ax.get_ymajorticklabels(),fontsize=18)
plt.setp(ax.get_xmajorticklabels(),fontsize=18)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Turn on the plot grid and set appropriate linestyle and color
ax.grid(True,linestyle=':', color='0.75')
ax.set_axisbelow(True)

# Define the X and Y axis labels
plt.xlabel('Time (s)', fontsize=22, weight='bold', labelpad=5)
plt.ylabel(r'Acceleration ($m/s^2$)', fontsize=22, weight='bold', labelpad=10)
 
# plt.plot(time_data[:,0], time_data[:,1], linewidth=2, linestyle='-.', label=r'X')
# plt.plot(time_data[:,0], time_data[:,2], linewidth=2, linestyle='--', label=r'Y')
plt.plot(time_data[:,0], time_data[:,3] - 1, linewidth=2, linestyle='-', label=r'Z')

# uncomment below and set limits if needed
plt.xlim(0,20)
# plt.ylim(0,10)

# Create the legend, then fix the fontsize
# leg = plt.legend(loc='upper right', ncol = 3, fancybox=True)
# ltext  = leg.get_texts()
# plt.setp(ltext,fontsize=18)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)

# save the figure as a high-res pdf in the current folder
plt.savefig('example_accel.pdf')

# show the figure
# plt.show()


# Set the plot size - 3x2 aspect ratio is best
fig = plt.figure(figsize=(6,4))
ax = plt.gca()
plt.subplots_adjust(bottom=0.17, left=0.17, top=0.96, right=0.96)

# Change the axis units font
plt.setp(ax.get_ymajorticklabels(),fontsize=18)
plt.setp(ax.get_xmajorticklabels(),fontsize=18)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Turn on the plot grid and set appropriate linestyle and color
ax.grid(True,linestyle=':', color='0.75')
ax.set_axisbelow(True)

# Define the X and Y axis labels
plt.xlabel('Frequency (Hz)', fontsize=22, weight='bold', labelpad=5)
plt.ylabel('Acceleration (g)', fontsize=22, weight='bold', labelpad=10)
 
plt.loglog(freq_data[:,0], freq_data[:,1], linewidth=2, linestyle='-', label=r'X')
plt.loglog(freq_data[:,0], freq_data[:,2], linewidth=2, linestyle='--', label=r'Y')
plt.loglog(freq_data[:,0], freq_data[:,3], linewidth=2, linestyle='-.', label=r'Z')

# uncomment below and set limits if needed
# plt.xlim(0,5)
# plt.ylim(0,10)

# Create the legend, then fix the fontsize
leg = plt.legend(loc='upper right', ncol = 3, fancybox=True)
ltext  = leg.get_texts()
plt.setp(ltext,fontsize=18)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)

# save the figure as a high-res pdf in the current folder
plt.savefig('example_freq.pdf')

# show the figure
plt.show()


