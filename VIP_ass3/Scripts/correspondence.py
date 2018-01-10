import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

def run_stereo_matching(img1, img2, windowsize = 11, cv = 0):
	if cv == 1:		
		pyramid_images_img1 = gaussian_pyramid_images_cv(img1)
		pyramid_images_img2 = gaussian_pyramid_images_cv(img2)
	else:
		pyramid_images_img1 = gaussian_pyramid_images(img1)
		pyramid_images_img2 = gaussian_pyramid_images(img2)

	disparity_map = correspondence(pyramid_images_img1[3], pyramid_images_img2[3], windowsize, limit = 8)[1]

	imgs = []
	imgs.append(disparity_map)
	
	for i in np.arange(3):
		disparity_map = cv2.pyrUp(disparity_map)
		disparity_map = np.multiply(disparity_map, 2)
		disparity_map = correspondence_upscaled(pyramid_images_img1[2-i], pyramid_images_img2[2-i], disparity_map, windowsize)[1]
		imgs.append(disparity_map)
	
	return np.array(imgs)

def pextract(img, y):
	patch = np.empty_like(patch0)
	patches = np.empty_like(patches0)
	for x in range(0, ish[1]):
		a = img[y:y+windowsize,x:x+windowsize,:]
		a=((a[:,:,0]+a[:,:,1]+a[:,:,2])/3).reshape(length)
		patch = (a - np.mean(a)) / np.std(a)
		patches[x] = patch
	return patches

def pextract_lum(img, y):
    patch = np.empty_like(patch0)
    patches = np.empty_like(patches0)
    for x in range(0, ish[1]):
        a = img[y:y+windowsize,x:x+windowsize,:]
        a=(a[:,:,0]*0.3+a[:,:,1]*0.6+a[:,:,2]*0.1).reshape(length)
        patch = (a - np.mean(a)) / np.std(a)
        patches[x] = patch
    return patches

def hpatches(img1, img2, y, mode='intensity'):
    padded1= cv2.copyMakeBorder(img1,pad,pad,pad,pad,cv2.BORDER_CONSTANT)
    padded2= cv2.copyMakeBorder(img2,pad,pad,pad,pad,cv2.BORDER_CONSTANT)
    
    if mode == 'intensity':
        patches1 = pextract(padded1, y)
        patches2 = pextract(padded2, y)
    elif mode == 'luminance':
        patches1 = pextract_lum(padded1, y)
        patches2 = pextract_lum(padded2, y)
    
    return patches1, patches2

def correspondence(img1,img2, wsize = 5, limit = 25, mode='intensity'):
	start = time.clock() 
	global windowsize
	windowsize = wsize
	global pad
	pad = (windowsize-1)//2
	global length
	length = windowsize**2
	global ish
	ish = img1.shape
	global psh
	psh = (img1.shape[0]+2*pad,img1.shape[1]+2*pad)
	global patch0
	patch0 = np.empty((windowsize,windowsize))
	global patches0
	patches0 = np.empty((psh[1]-windowsize+1, length))
	result = np.zeros((ish[0], ish[1]))
	result_nonsqrd = np.zeros((ish[0], ish[1]))
	for y in range(ish[0]):
		patches1, patches2 = hpatches(img1, img2, y, mode)
		for x in range(ish[1]):
			#normalized cross-correlation
			best = -999
			besth = -999

			r = [0, patches2.shape[0]]
			rr = ish[1]//limit #limits search range
			if x - rr > 0:
				r[0] = x - rr
			if x + rr < ish[1]:
				r[1] = x + rr
			for h in range(r[0],r[1]):
				ncc = np.correlate(patches1[x]/length, patches2[h]) 
				if ncc > best:
					best = ncc
					besth =h
			result[y,x]=(x-besth)**2
			result_nonsqrd[y,x]=abs(x-besth)
	elapsed = time.clock()
	elapsed = elapsed - start
	print ("Done. Time spent executing correspondence: ", elapsed)
	return result, result_nonsqrd


# In[109]:


def correspondence_upscaled(image1, image2, disparity, wsize, mode='intensity'):
	global windowsize
	windowsize = wsize
	global pad
	pad = (windowsize-1)//2
	global length
	length = windowsize**2
	global ish
	ish = image1.shape
	global psh
	psh = (image1.shape[0]+2*pad,image1.shape[1]+2*pad)
	global patch0
	patch0 = np.empty((windowsize,windowsize))
	global patches0
	patches0 = np.empty((psh[1]-windowsize+1, length))

	result = np.zeros((ish[0], ish[1]))
	result_nonsqrd = np.zeros((ish[0], ish[1]))

	results = []
	results_nonsqrd = []

	disp_map = disparity

		
	start = time.clock() 

	for y in range(ish[0]):
		patches1, patches2 = hpatches(image1, image2, y, mode)

		for x in range(ish[1]):
			#normalized cross-correlation
			best = -999
			besth = -999

			r = [0, patches2.shape[0]]
			
			rr = int(abs(disp_map[y,x]))+1 #limits search range
			
			if x - rr > 0:
				r[0] = x - rr
			if x + rr < ish[1]:
				r[1] = x + rr
				
			for h in range(r[0],r[1]):
				ncc = np.correlate(patches1[x]/length, patches2[h]) 

				if ncc > best:
					best = ncc
					besth =h

			result[y,x]=(x-besth)**2
			result_nonsqrd[y,x]=abs(x-besth)

	results.append(result)
	results_nonsqrd.append(result_nonsqrd)

	disp_map = result

	elapsed = time.clock()
	elapsed = elapsed - start
	print ("Done. Time spent executing correspondence: ", elapsed)
	return result, result_nonsqrd

# OpenCV's own implementation

def gaussian_pyramid_images_cv(img):
	p_imgs = [img]
	for i in np.arange(3):
		img = cv2.pyrDown(img)
		p_imgs.append(img)
	return p_imgs

# Selfimplemented Gaussian Pyramid function.
# Convolves with a Gaussian kernel and then removes all even rows and columns.
# Output is four images at a higher pyramid level and therefore lower resolution. 

def gaussian_pyramid_images(img):
	p_imgs = [img]

	for i in np.arange(3):
		img = cv2.GaussianBlur(img, (5,5), 2)
		img_new = []
		for i in np.arange(1,img.shape[0],2):
			img_row = []
			for j in np.arange(1,img.shape[1],2):
				img_row.append(img[i][j])
			img_new.append(img_row)
			
		img = np.array(img_new)
		p_imgs.append(img)
		
	return p_imgs


def gaussian_pyramid_images_cv_up(images):
	p_imgs = []
	for i in np.arange(images.shape[0]):
		img = images[i]
		for j in np.arange(i):
			img = cv2.pyrUp(img)
		
		print(img.shape)
		p_imgs.append(img)
	return np.array(p_imgs)


def plot_images(imgs):
	i, j = len(imgs)//2, len(imgs)//2
	fig, ax = plt.subplots(i, j, figsize=(15,15))
	ii, jj = np.meshgrid(np.arange(i), np.arange(j), indexing='ij')
	axes = [axis for axis in zip(ii.ravel(), jj.ravel())]
	for idx, axis in enumerate(axes):
		ax[axis].imshow(imgs[idx], "gray")
	plt.show()