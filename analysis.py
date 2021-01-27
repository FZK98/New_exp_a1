# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 15:58:32 2021

@author: maria
"""
import numpy as np
import matplotlib.pyplot as plt
galaxyCounts=np.loadtxt('fixed_r galaxy counts.txt')
#galaxyCounts=np.loadtxt('variable_r galaxy counts.txt')
#galaxyCounts=np.loadtxt('galaxy_counts_plmv270121.txt')
galaxyLocation=np.loadtxt('galaxy_locations_plmv270121.txt')

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
	
#plt.errorbar(magnitudes, np.log10(numberSmallerMag), yerr, 'x')
plt.plot(magnitudes, np.log10(numberSmallerMag),'x')

#choose indices of linear region manually by examining plot
p = np.polyfit(magnitudes[12:1005], np.log10(numberSmallerMag)[12:1005],1)
fitPoints = []
for i in range(len(magnitudes)):
    fitPoints.append(p[0]*magnitudes[i]+p[1])
	
plt.plot(magnitudes,fitPoints)
print("the gradient of the linear part is ",p[0])

