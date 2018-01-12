import cv2
import numpy as np
import matplotlib.pyplot as plt
import ps_utils as ps


(I, mask, S) = ps.read_data_file("Beethoven.mat")
imgs_be = [I[:,:,i] for i in range(3)]
# print(I.shape, mask.shape, S.shape)

# (I, mask, S) = ps.read_data_file("Buddha.mat")
# imgs_bu = [I[:,:,i] for i in range(10)]
# print(I.shape, mask.shape, S.shape)

# Plot images function - plot_images(imgs, x, y, figsize)
# Call example - plot_images([img1, img2, img3], 3, 1, (30, 30))

def plot_images(imgs_input, i, j, figsize=(15,15)):
    imgs = imgs_input[:]
    ax = [["ax"+str(ii)+str(jj) for jj in range(j)] for ii in range(i)] 
    # [[ax1, ax2, ax3], [ax4, ax5, ax6]] Fx. with y = 2, x = 3
    fig, ax = plt.subplots(i, j, figsize=figsize)
    ax = np.array(ax).flatten()
    if not len(ax) == len(imgs): print('Not matching dimensions! \nNumber of images: '+str(len(imgs))+\
                                       '\nNumber of plots: '+str(len(ax))) 
    for axis in ax:
        axis.imshow(imgs.pop(0), "gray")
    plt.show()
    
def plot_image(img, figsize=(20,20)):
    plt.imshow(img)
    plt.rcParams["figure.figsize"] = figsize
    plt.show()
    
    

i_s, j_s = np.where(mask == 1)
resized_mask = mask[min(i_s):max(i_s), min(j_s):max(j_s)]
print(resized_mask.shape)
resized_images = [img[min(i_s):max(i_s), min(j_s):max(j_s)] for img in imgs_be]
print(len(resized_images))
imgs_and_mask = np.vstack((resized_mask, resized_images))
#imgs_and_mask = resized_images.append(resized_mask)
print(imgs_and_mask)
#plot_images([fig for fig in imgs_and_mask], 2, 2)

#d_map = ps.unbiased_integrate(imgs_and_mask[0], imgs_and_mask[1], imgs_and_mask[2], imgs_and_mask[3])

#print(d_map)
# d_map = ps.simchony_integrate(imgs_be[0], imgs_be[1], imgs_be[2], mask)
# test = np.where(d_map == np.nan)
# print(test.shape)
#ps.display_depth(d_map)