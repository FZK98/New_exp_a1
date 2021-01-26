# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 16:14:24 2021

@author: maria
"""
no_objects = 10 #how many galaxies
#no_object_half = 10
object_loc = []

image_size = 500
import numpy as np
import matplotlib.pyplot as plt
popt = np.loadtxt('image_parameters.txt')

basearray = np.zeros((image_size,image_size*2)) #test image, asymmetrical to check indices
#make background with gaussian distribution same as real image
for i in range(image_size):
	for j in range(image_size*2):
		basearray[i][j] = np.random.normal(popt[1],popt[2]) 
		
#assign location to galaxies, but ensuring they're not too close to edges
for i in range(no_objects):
	object_loc.append(((np.random.randint(15,image_size-15)),(np.random.randint(15,image_size*2-15))))
	i += 1
	
def gaussian2d(a, mux, muy, sigma,x, y):
	gauss = a*np.exp(-((x-mux)**2/(2*sigma**2))-((y-muy)**2/(2*sigma**2)))
	return gauss

def vaucouleurIntensity(amplitude, radius, b):
	intensity = amplitude*np.exp(-b*(radius**0.25))
	return intensity

for i in range(no_objects):
	loctemp=object_loc[i]
	x_centre=loctemp[0]
	y_centre=loctemp[1]
	maxAmp = np.random.randint(5000,6000)
	b = 0.1
	radius1 = (-1*(1/b)*np.log10((popt[1]+4*popt[2])/maxAmp))**4
	radius1 = int(radius1)
	for j in range(x_centre-radius1,x_centre+radius1): #6 is the radius, arbitrary can be changed
		for k in range(y_centre-radius1,y_centre+radius1):
			radius2 = np.sqrt((j-x_centre)**2+(k-y_centre)**2)
			basearray[j,k] = vaucouleurIntensity(maxAmp, radius2, b) #makes the objects gaussian blobs, arbitrary amplitude and sigma, can be changed

plt.figure()
plt.imshow(basearray)

#plt.savetxt('simulatedimage.txt', basearray)

