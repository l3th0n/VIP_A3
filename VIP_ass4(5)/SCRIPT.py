#####################################################################################################################################
# VISION AND IMAGE PROCESSING - ASSIGNMENT 5																						#																
#																																	#											
# by Bo Arlet (tsl967), Viktor Hargitai (lzm222) and Maud Ottenheijm (cqw485)						 								#
# 																																	#
# This code performs photometric stereo on two datasets to create a 3-dimensional representation of the input.						#
# It uses the following steps/algorithms:																							#
# - loading data, slicing mask and input images to exclude excessive zero-masking 													#		
# - obtain albedo modulated normal field M by multiplying with the (pseudo-) inverse of lighting S									#		
# - extract and display albedo within mask																							#	
# - extract components of the normal fields after normalizing M																		#
# - unbiased_integrate function for computing depth within mask																		#
# - visualise results from 4 different viewpoints																					#
#																																	#
# The code calls on the following libraries:																						#
# - matplotlib (https://matplotlib.org/index.html)																					#	
# - numpy (http://www.numpy.org/)																									#	
# - scipy (https://www.scipy.org/)																									#
#																																	#		
# The code calls on the following python scripts:																					#
# - ps_utils.py, provided by Francois Lauze, University of Copenhagen																#
#																																	#		
#####################################################################################################################################


# load libraries and prewritten functions
from ps_utils import *
import numpy as np
import numpy.linalg as lin
import matplotlib.pyplot as plt
import scipy.io as sio


## MAIN FUNCTION: 
# takes filename for MAT file as input, performs photometric stereo to return a 3D representation of the input
def get_3Dirty(filename):
	# load file, save content in globals
	all_images = sio.loadmat(filename)
	global images
	images = all_images['I']
	global mask
	mask = all_images['mask']
	global S
	S = all_images['S']    
	global shape
	
	# reshape data to dimensions [nr of images, x, y], apply mask
	images = np.stack([images[:,:,i] for i in range(images.shape[2])], axis=0)
	images, mask = mask_that_boy()

	# save new shape
	shape = images.shape

	# flatten images to 1D array
	images = np.reshape(images, (images.shape[0],images.shape[1]*images.shape[2]))

	# take inverse of light vectors S, pseudo-inverse for sets with more than 3 images
	if shape[0] > 3:
		Sinv = lin.pinv(S)
	else:
		Sinv = lin.inv(S)

	# obtain albedo normal field, calculate albedo within mask
	dot_pd = np.dot(Sinv, images)
	p = lin.norm(dot_pd, axis=0)
	N = dot_pd / p

	# reshape to image dimensions
	N = np.reshape(N, (3,shape[1],shape[2]))

	# display albedo image with mask applied
	p = p.reshape(shape[1],shape[2])
	plt.imshow(p * mask, 'gray')
	plt.axis('off')
	plt.show()

	## SIMCHONY FUNCTION DOES NOT FUNCTION! Uncomment next two code lines to perform Simchony

	# perform Simchony for sets larger than 3 images, return 3D representation
	#if shape[0] > 3:
	#    Dirty3 = simchony_integrate(N[0], N[1], N[2], mask)

	# perform Direct Poisson Solver for sets of 3 images, return 3D representation
	Dirty3 = unbiased_integrate(N[0], N[1], N[2], mask, order=2)
	# display 4 different rotations of Dirty3 in 2D
	rotations = [Dirty3]

	for i in range(3):
		Dirty3 = np.rot90(Dirty3)
		rotations.append(Dirty3)

	# uncomment next line to display 2D representations of Dirty3
	#prints = [display_depth_matplotlib(img) for img in rotations]
	return rotations



# reshapes images and mask to exclude any rows/columns that are 0 masked
def mask_that_boy():
    i_s, j_s = np.where(mask == 1)
    resized_mask = mask[min(i_s):max(i_s), min(j_s):max(j_s)]
    resized_images = images[:, min(i_s):max(i_s), min(j_s):max(j_s)]
    return resized_images, resized_mask

# call main function
DirtyRotations_BBOY = get_3Dirty('Beethoven.mat')
DirtyRotations_BBUD = get_3Dirty('Buddha.mat')

