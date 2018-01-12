

# load packages


from ps_utils import *
import numpy as np
import numpy.linalg as lin
import matplotlib.pyplot as plt
import scipy.io as sio


# load images


beethoven = sio.loadmat('Beethoven.mat')
buddha = sio.loadmat('Buddha.mat')



# define borders of image based on mask
# and reshape images and mask accordingly
mask = beethoven["mask"][8:247,49:202]
beetm = beethoven["I"][8:247,49:202,:]

# reshape to 3x256x256
bboy = np.stack([beetm[:,:,0],beetm[:,:,1],beetm[:,:,2]], axis=0)


# Take illumination vectors
S = beethoven['S']

# take inverse of S
S_this = lin.inv(S[0])

# save image shape
image_shape = beetm.shape

# flatten S to 1-dimensional array 
# (this may seem unnescessary, but it was the only way
# to make the 3x1 array to do dotproduct with)
S_flat = np.reshape(S_this, (9,1))

output = []

# for each image
for x in range(3):

	# take the 3x1 S for that image
	S = S_flat[x*3:(x+1)*3]
	# take image
	J_this = bboy[x]

	# flatten image to 1 dimension
	J_this = np.reshape(J_this, (1,J_this.size))

	# dotproduct of S and image
	dotpd = np.dot(S, J_this)

	# divide dotproduct by the norm(dotproduct)
	N = dotpd / lin.norm(dotpd)

	# reshape N back to image shape
	# this includes the 3 values per pixel that it now has
	# we dont know how we get 3 values per pixel though
	N = np.reshape(N, (3,image_shape[0],image_shape[1]))

	output.append(N)
    


# In[305]:


output_out = unbiased_integrate(output[0][0], output[0][1], output[0][2], mask, order=2)
#display_depth_matplotlib(output_out)

