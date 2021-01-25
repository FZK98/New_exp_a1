# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 15:58:32 2021

@author: maria
"""
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.optimize import curve_fit
galaxyCounts=np.loadtxt('galaxycounts.txt') #some of these are negative rip
galaxyLocation=np.loadtxt('galaxylocations.txt')

ZP=2.530E+01 #taken from header

magnitudes = []
for i in galaxyCounts:
	tempMag = ZP-(2.5*np.log10(i))
	magnitudes.append(tempMag)
	
yerr = []
for i in range(len(galaxyCounts)):
	yerr.append(np.sqrt(galaxyCounts[i]))
#need some error propagation
	
numberSmallerMag = []
for i in range(len(magnitudes)):
	a=np.where(magnitudes<=magnitudes[i])
	b=len(a[0])
	#print(b) #a bunch of these are zero oops
	numberSmallerMag.append(b)
	
#plt.errorbar(magnitudes, np.log10(numberSmallerMag), yerr, 'x')
plt.plot(magnitudes, np.log10(numberSmallerMag),'x')

#then can do a fit of the linear part of the line

