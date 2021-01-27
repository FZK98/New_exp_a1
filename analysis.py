# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 15:58:32 2021

@author: maria
"""
import numpy as np
import matplotlib.pyplot as plt
#galaxyCounts=np.loadtxt('fixed_r galaxy counts.txt')
#galaxyCounts=np.loadtxt('variable_r galaxy counts.txt')
#galaxyCounts=np.loadtxt('galaxy_counts_plmv270121.txt')
galaxyCounts=np.loadtxt('variable_r galaxy counts - q = 2,5.txt')

#galaxyLocation=np.loadtxt('galaxy_locations_plmv270121.txt')

ZP=2.530E+01 #taken from header
ZP_err = 2.0E-2 #taken from header of FITS file
magnitudes = []
for i in galaxyCounts:
	tempMag = ZP-(2.5*np.log10(i))
	magnitudes.append(tempMag)
magnitudes=np.sort(magnitudes)
numberSmallerMag = []
for i in range(len(magnitudes)):
	a=np.where(magnitudes<=magnitudes[i])
	b=len(a[0])
	#print(b) #a bunch of these are zero oops
	numberSmallerMag.append(b)
	
plt.plot(magnitudes, np.log10(numberSmallerMag),'x')
plt.grid()
plt.xlabel("Magnitude", fontsize=15)
plt.ylabel("log(N)", fontsize=15)
plt.tick_params(labelsize=12)

#choose indices of linear region manually by examining plot
linearStartIndex = 8
linearEndIndex = 800

p = np.polyfit(magnitudes[linearStartIndex:linearEndIndex], np.log10(numberSmallerMag)[linearStartIndex:linearEndIndex],1)
fitPoints = []
for i in range(linearStartIndex, linearEndIndex):
    fitPoints.append(p[0]*magnitudes[i]+p[1])
	
plt.plot(magnitudes[linearStartIndex:linearEndIndex],fitPoints, label="variable r, q=2.5 , gradient = "+str(p[0]))
plt.legend()
print("the gradient of the linear part is ",p[0])

