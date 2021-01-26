# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 16:14:24 2021

@author: maria
"""
no_objects = 20 #how many galaxies
#no_object_half = 10
object_loc = []

image_size = 500
import numpy as np
import matplotlib.pyplot as plt
popt = np.loadtxt('image_parameters.txt')

basearray = np.zeros((image_size,image_size*2)) #test image, asymmetrical to check indices
#masktest = np.zeros((image_size,image_size*2)) #mask image for test

initialRadius = 6
secondaryRadius = 9

#make background with gaussian distribution same as real image
for i in range(image_size):
	for j in range(image_size*2):
		basearray[i][j] = np.random.normal(popt[1],popt[2]) 
		
#assign location to galaxies, but ensuring they're not too close to edges
for i in range(no_objects):
	object_loc.append(((np.random.randint(secondaryRadius,image_size-secondaryRadius)),(np.random.randint(secondaryRadius,image_size*2-secondaryRadius))))
	i += 1
	
def gaussian2d(a, mux, muy, sigma,x, y):
	gauss = a*np.exp(-((x-mux)**2/(2*sigma**2))-((y-muy)**2/(2*sigma**2)))
	return gauss

def sersicIntensity(amplitude, radius, b):
	#logIntensity = np.log10(amplitude) - k*(radius**0.25)
	intensity = amplitude*np.exp(-b*(radius**0.25))
	return intensity
#make half of the galaxies have amplitude of 4000
#for i in range(no_object_half):
#	loctemp=object_loc[i]
#	x_centre=loctemp[0]
#	y_centre=loctemp[1]
#	for j in range(x_centre-6,x_centre+6): #6 is the radius, arbitrary can be changed
#		for k in range(y_centre-6,y_centre+6):
#			basearray[j,k] = gaussian2d(4000,x_centre, y_centre, 13, j, k) #makes the objects gaussian blobs, arbitrary amplitude and sigma, can be changed
for i in range(no_objects):
	loctemp=object_loc[i]
	x_centre=loctemp[0]
	y_centre=loctemp[1]
	radius1 = np.random.randint(3,15)
	for j in range(x_centre-radius1,x_centre+radius1): #6 is the radius, arbitrary can be changed
		for k in range(y_centre-radius1,y_centre+radius1):
			radius2 = np.sqrt((j-x_centre)**2+(k-y_centre)**2)
			basearray[j,k] = sersicIntensity(4000, radius2, 0.01) #makes the objects gaussian blobs, arbitrary amplitude and sigma, can be changed

#make other half of the galaxies have amplitude 10000			
#for i in range(no_object_half):
#	loctemp=object_loc[-i]
#	x_centre=loctemp[0]
#	y_centre=loctemp[1]
#	for j in range(x_centre-8,x_centre+8): #8 is the radius, arbitrary can be changed
#		for k in range(y_centre-8,y_centre+8):
#			basearray[j,k] = gaussian2d(10000,x_centre, y_centre, 13, j, k) #makes the objects gaussian blobs, arbitrary amplitude and sigma, can be changed


plt.figure()
plt.imshow(basearray)

#plt.savetxt('simulatedimage.txt', basearray)

#
#base1d = basearray.ravel() #make test image 1D array
#base1d_sorted = sorted(base1d) #sort values in test image in ascending order
#
##sums values of pixels inside 1st aperture, pixels of galaxy
#def galaxyPhotons(x_centre,y_centre, radius):
#	photon_vals=[];
#	for i in range(x_centre-radius,x_centre+radius):
#		for j in range(y_centre-radius,y_centre+radius):
#			if i<(image_size) and i>=0 and j<(image_size*2) and j>=0 and masktest[i,j]==0: #only consider pixels within the image
#				d=np.sqrt((i-x_centre)**2+(j-y_centre)**2)
#				if d<radius: 
#					photon_vals.append(basearray[i,j])
#				
#	return(np.sum(photon_vals))
#	
#
#
##averages values of pixels between 1st and 2nd aperture, local bakcground mean
#def localBackground(x_centre,y_centre, initialRadius, secondaryRadius):
#	bg_photon_vals=[];
#	for i in range(x_centre-secondaryRadius,x_centre+secondaryRadius):#outer x
#		for j in range(y_centre-secondaryRadius,y_centre+secondaryRadius):#outer y
#			if i<(image_size) and i>=0 and j<(image_size*2) and j>=0 and masktest[i,j]==0: #only consider pixels within the image!
#				d2=np.sqrt((i-x_centre)**2+(j-y_centre)**2)
#				if d2<secondaryRadius and d2>initialRadius: #only consider pixels between the two apertures
#					bg_photon_vals.append(basearray[i,j])
#				masktest[i,j]=1
#	return(np.sum(bg_photon_vals)/len(bg_photon_vals))
#
#def pixelPos(data, value):
#	indices = np.where(basearray==value) #gives tuples of coordinates
#	listIndices= list(zip(indices[1], indices[0])) # gives pairs of coordinates in form (x,y)
#	return listIndices
#
#	
#initialRadius = 6
#secondaryRadius = 9
#galaxyCounts = []
#for i in range(len(base1d_sorted)): 
#	tempPixVal = base1d_sorted[-(1+i)] #find highest pixel value
#	if tempPixVal > popt[1]+5*popt[2]:
#		tempPixPos = pixelPos(basearray, tempPixVal) #find position of highest pixel value
#		for j in range(len(tempPixPos)): #potentially multiple locations with same pixel value
#			loc = tempPixPos[j]
#			if masktest[loc[1],loc[0]] == 0: #if pixel is available to use 
#				galaxyBrightness=galaxyPhotons(loc[1],loc[0],initialRadius)
#				galaxyBackground = localBackground(loc[1],loc[0],initialRadius, secondaryRadius)
#				galaxyCounts.append(galaxyBrightness-galaxyBackground)
#				print(tempPixVal)
#plt.figure()
#plt.imshow(masktest)			
