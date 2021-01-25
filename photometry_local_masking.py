# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 04:03:04 2021

@author: User
"""

from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.optimize import curve_fit

#read data from the file
hdulist = fits.open("Mosaic.fits/mosaic.fits")#plt.imshow(data, cmap='gray')
hdr=hdulist[0].header #meta data 
data=hdulist[0].data #astro image data
background_data=[] #empty list - store the relevant background data
hdulist.close()

# data = data[1500:1650,1900:2000] #[y,x]
#datatest=hdulist[0].data
#show the test image taken 
plt.figure()
plt.imshow(np.log10(data))
plt.show()
#dimensions of the image 
testimagey = np.shape(data)[0]
testimagex = np.shape(data)[1]
#load in image parameters and the premade mask 
popt = np.loadtxt('image_parameters.txt')
mask = np.loadtxt('mask.txt')
#this is the sample of the mask that corresponds to the image
# mask =  mask[1500:1650,1900:2000] #[y,x]
#displays the mask sample to show is corresponds to the image
plt.figure()
plt.imshow(mask)
plt.show()

# datatest = datatest*masktest
# plt.figure()
# plt.imshow(np.log10(datatest))
# plt.show()


#reduce the data set to valid unmasked values - remove test suffix for the real thing
masked_data = mask*data 
masked_data_1d = masked_data.ravel()
masked_data_sorted = sorted(masked_data_1d)
masked_data_sorted = list(filter(lambda a: a!=0, masked_data_sorted ))
plt.figure()
plt.imshow(masked_data)
plt.show()

#make a local mask around the object with a given radius
def inner_mask(mask, inner_mask,x, y,r1):
    inner_mask[y-r1:y+r1 , x-r1:x+r1] = 1
    mask[y-r1:y+r1 , x-r1:x+r1] = 0
    return inner_mask
def annulus_mask(mask , annulus_mask, x, y, r2):
    annulus_mask[y-r2:y+r2 , x-r2:x+r2] = 1
    mask[y-r2:y+r2 , x-r2:x+r2] = 0
    return annulus_mask

r1 =6
r2 =15
galaxy_counts = []
galaxy_locations = []
for i in range(len(masked_data_sorted)): 
    # if masked_data_sorted[i]
    #make empty masks that are the same size as the image and full of zeros
    mask_1 = np.zeros((testimagey, testimagex))
    mask_2 = np.zeros((testimagey, testimagex))

    tempPixVal = masked_data_sorted[-(1+i)] #find highest pixel value
    tempPixPos = np.where(masked_data == tempPixVal) #find position of pixel in masked image
    if any(tempPixPos[0]):
    
        #extract co-ordinates for simplicity
        y = tempPixPos[0][0]
        x = tempPixPos[1][0] 

        innermask = inner_mask(masked_data,mask_1, x, y, r1)
        outermask = annulus_mask(masked_data,mask_2, x, y, r2)
        
        apeture_flux = np.sum(innermask*data)
        annulus_flux = np.sum(outermask*data) - apeture_flux
        local_background = annulus_flux/ (r2**2 - r1**2)
        
        print(len(masked_data_sorted) - i)
        galaxy_counts.append(apeture_flux - (r1**2)*local_background)
        coordxy = [x,y]
        galaxy_locations.append(coordxy)
    
    
plt.figure()
plt.imshow(np.log10(data), cmap='jet')
for i in galaxy_locations:
    mycircle = plt.Circle(i, r1, color= 'k',fill=False)
    plt.gca().add_artist(mycircle)
    # mycircle2 = plt.Circle(i, r2, color= 'k',fill=False)
    # plt.gca().add_artist(mycircle2)
plt.show()

plt.figure()
plt.imshow(masked_data)
plt.show()

#ZP=2.530E+01
#def calculateMagnitude(data_points, ZP):
#	magnitudes = []
#	for i in data_points:
#		tempMag = ZP-(2.5*np.log10(i))
#		magnitudes.append(tempMag)
#	return magnitudes

#plt.figure()
#plt.hist(calculateMagnitude(galaxyCounts, ZP))