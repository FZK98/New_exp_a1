# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 15:58:32 2021

@author: maria
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.optimize import curve_fit
galaxyCounts=np.loadtxt('./q = 2.5, min r = 3, global BG correction/variable_r galaxy counts - q = 2,5.txt')
#galaxyRadii = np.loadtxt('./full scan q = 2, r min = 2, local BG corrected/galaxy_radii_plmv270121.txt')
#galaxyLocation=np.loadtxt('galaxy_locations_plmv270121.txt')

ZP=2.530E+01 #taken from header
ZP_err = 2.0E-2 #taken from header of FITS file
magnitudes = []
for i in galaxyCounts:
	if i >0:
	    tempMag = ZP-(2.5*np.log10(i))
	    magnitudes.append(tempMag)
magnitudes=np.sort(magnitudes)

bins1=np.arange(np.min(magnitudes), np.max(magnitudes), 0.2)

#numberSmallerMag = []
#for i in range(len(magnitudes)):
#	a=np.where(magnitudes<=magnitudes[i])
#	b=len(a[0])
#	#print(b) #a bunch of these are zero oops
#	numberSmallerMag.append(b)
	
numberSmallerMag2 = []
for i in range(len(bins1)):
	a=np.where(magnitudes<=bins1[i])
	b=len(a[0])
	#print(b) #a bunch of these are zero oops
	numberSmallerMag2.append(b)
	
#plt.plot(magnitudes, np.log10(numberSmallerMag),'x')
#plt.errorbar(magnitudes, np.log10(numberSmallerMag), 0.434/np.sqrt(numberSmallerMag), marker='x', fmt=' ')
plt.errorbar(bins1, np.log10(numberSmallerMag2), 0.434/np.sqrt(numberSmallerMag2), marker='x', fmt=' ')
plt.grid()
plt.xlabel("Magnitude", fontsize=15)
plt.ylabel("log(N)", fontsize=15)
plt.tick_params(labelsize=12)

def linear(x, m , c):
	return((m*x)+c)

#choose indices of linear region manually by examining plot
linearStartIndex = 11
linearEndIndex = 33

#p = np.polyfit(magnitudes[linearStartIndex:linearEndIndex], np.log10(numberSmallerMag)[linearStartIndex:linearEndIndex],1)
fitPoints = []
p,q=sp.optimize.curve_fit(linear, bins1[linearStartIndex:linearEndIndex], np.log10(numberSmallerMag2[linearStartIndex:linearEndIndex]), sigma=0.434/np.sqrt(numberSmallerMag2)[linearStartIndex:linearEndIndex])
#p,q=np.polyfit(bins1[linearStartIndex:linearEndIndex], np.log10(numberSmallerMag2[linearStartIndex:linearEndIndex]), 1,w=1/(0.434/np.sqrt(numberSmallerMag2)[linearStartIndex:linearEndIndex]))

for i in range(linearStartIndex, linearEndIndex):
    fitPoints.append(p[0]*bins1[i]+p[1])
	
plt.plot(bins1[linearStartIndex:linearEndIndex],fitPoints, label="variable r, q=2.5, minr=3 , gradient = "+str(p[0]))
plt.legend()
print("the gradient of the linear part is ",p[0], "+/-",np.sqrt(q[0,0]))

