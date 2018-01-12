
# coding: utf-8

# In[56]:


from ps_utils import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio


beethoven = read_data_file('Beethoven.mat')
buddha = sio.loadmat('Buddha.mat')


matrix = beethoven[0]
matrix.shape

new_matrix = np.stack(matrix, axis=2)
new_matrix = np.stack(new_matrix, axis=2)

output = unbiased_integrate(new_matrix[0], new_matrix[1], new_matrix[2], beethoven[1], order=2)
    
display_depth_matplotlib(output)

