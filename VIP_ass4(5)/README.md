# VIP_A5

VISION AND IMAGE PROCESSING - ASSIGNMENT 5																																						
by Bo Arlet (tsl967), Viktor Hargitai (lzm222) and Maud Ottenheijm (cqw485)	

This is the README for assignment 5.					 								
																																
The code in this folder performs photometric stereo on two datasets to create a 3-dimensional representation of the input.						
It uses the following steps/algorithms:																							
- loading data, slicing mask and input images to exclude excessive zero-masking 															
- obtain albedo modulated normal field M by multiplying with the (pseudo-) inverse of lighting S											
- extract and display albedo within mask																								
- extract components of the normal fields after normalizing M																		
- unbiased_integrate function for computing depth within mask																		
- visualise results from 4 different viewpoints																					

Input files are .mat files and are included in the main directory.
Output files are .png files and can be found in the subfolder Images.																												

The code calls on the following libraries:																						
- matplotlib (https://matplotlib.org/index.html)																						
- numpy (http://www.numpy.org/)																										
- scipy (https://www.scipy.org/)																									
																																		
The code calls on the following python scripts (included in the main directory):																					
- ps_utils.py, provided by Francois Lauze, University of Copenhagen		

