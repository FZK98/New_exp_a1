# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 15:58:32 2021

@author: maria
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.optimize import curve_fit
from scipy import stats
# =============================================================================
# import necessary data
# =============================================================================
galaxyCounts=np.loadtxt('./full scan q = 2, r min = 2, local BG corrected/variable_r galaxy counts.txt')
magnitudeError=np.loadtxt('./full scan q = 2, r min = 2, local BG corrected/Variable_r galaxy magnitude errors.txt')

ZP=2.530E+01 #taken from header
ZP_err = 2.0E-2 #taken from header of FITS file

magnitudes = []
magnitudeError2 = [] #errors corresponding to positive fluxes

for i in range(len(galaxyCounts)):
	if galaxyCounts[i]>0:
		tempMag=ZP-2.5*np.log10(galaxyCounts[i])
		magnitudes.append(tempMag)
		magnitudeError2.append(magnitudeError[i])

bins1=list(np.arange(np.min(magnitudes), np.max(magnitudes), 0.2)) #bins for placing the magnitudes into
magnitudesZip = list(zip(magnitudes, magnitudeError2)) #keeping the magnitudes and their errors together
magnitudesSorted = sorted(magnitudesZip) #sorted according to magnitude
magValSorted=sorted(magnitudes) #sorted magnitudes, without associated error
	
numberSmallerMag2 = [] #cumulative number of objects with a given magnitude or lower (N)
binError = []
for i in range(len(bins1)):
	a=np.where(magValSorted<=bins1[i])
	b=len(a[0])
	numberSmallerMag2.append(b)
	
poissonError = [] #sqrt(N) error associated with counting pixels
for i in range(len(numberSmallerMag2)):
	poissonError.append(0.434/np.sqrt(numberSmallerMag2[i]))
	
# =============================================================================
# 	finding the error on the bin population using probability and magnitude error
# =============================================================================
binsProbabilityError=[] #the error on each bin count associated with the magnitude error
for j in range(len(bins1)-1):
	magnitudePdf=[] #the probability density for each magnitude point being in its correct bin 
	for i in range(len(magnitudesSorted)):
		if magnitudesSorted[i][0] >= bins1[j] and magnitudesSorted[i][0] < bins1[j+1]: #if the magnitude is placed in this bin
			lower=stats.norm(magnitudesSorted[i][0], magnitudesSorted[i][1]).cdf(bins1[j]) #pdf of upper bin bound (gaussian)
			upper=stats.norm(magnitudesSorted[i][0], magnitudesSorted[i][1]).cdf(bins1[j+1]) #pdf of lower bin bound (gaussian)
			magnitudePdf.append(upper-lower) #probability of being inside the bin bounds
	magnitudeProbability = [] #sqrt(p*(1-p)) for each magnitude point gives std
	for k in magnitudePdf:
		magnitudeProbability.append(np.sqrt(k*(1-k)))
	binsProbabilityError.append(0.434/np.sum(magnitudeProbability))	
binsProbabilityError.append(binsProbabilityError[-1]) #add another point to make the array the right size

# =============================================================================
# plotting the data
# =============================================================================

#3rd argument can be binsProbabilityError or poissonError (ensure it mateches with line 80)
plt.errorbar(bins1, np.log10(numberSmallerMag2), (binsProbabilityError), marker='x', fmt=' ') #plotting binned data with errorbars
plt.grid()
plt.xlabel("Magnitude", fontsize=15)
plt.ylabel("log(N)", fontsize=15)
plt.tick_params(labelsize=12)

# =============================================================================
# linear function for fitting
# =============================================================================
def linear(x, m, c):
	return((m*x)+c)
 
#choose indices of linear region manually by examining plot
linearStartIndex = 11
linearEndIndex = 33

#sigma can be binsProbabilityError or poissonError (ensure it matches with line 61)
p,q=sp.optimize.curve_fit(linear, bins1[linearStartIndex:linearEndIndex], np.log10(numberSmallerMag2[linearStartIndex:linearEndIndex]), sigma=binsProbabilityError[linearStartIndex:linearEndIndex])  #perform a linear fit

fitPoints = [] #y values for the linear fit plot
for i in range(linearStartIndex, linearEndIndex):
    fitPoints.append(p[0]*bins1[i]+p[1])
	
plt.plot(bins1[linearStartIndex:linearEndIndex],fitPoints, label="variable r, q=2.5, minr=3 , gradient = "+str(p[0])) #plot the linear fit on top of data
plt.legend()
print("the gradient of the linear part is ",p[0], "+/-",np.sqrt(q[0,0]))
