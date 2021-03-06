###############
# Main script #
###############

print('Loading packages')
import cv2
import matplotlib.pyplot as plt
import xlwt

print('Loading self-written functions')
from correspondence import *
from statistics import *

print('Loading images')
img_01 = cv2.imread('images/scene1.row3.col1.ppm')
img_01_tsu = cv2.cvtColor(img_01,cv2.COLOR_BGR2RGB)
img_02 = cv2.imread('images/scene1.row3.col2.ppm')
img_02_tsu = cv2.cvtColor(img_02,cv2.COLOR_BGR2RGB)
truedisp_tsu = cv2.imread('images/truedisp.row3.col3.pgm', 0)

img_01_venus = cv2.imread('images/im0_venus.ppm')
img_01_venus = cv2.cvtColor(img_01_venus,cv2.COLOR_BGR2RGB)
img_02_venus = cv2.imread('images/im1_venus.ppm')
img_02_venus = cv2.cvtColor(img_02_venus,cv2.COLOR_BGR2RGB)

img_01_map = cv2.imread('images/im0_map.pgm')
img_01_map = cv2.cvtColor(img_01_map,cv2.COLOR_BGR2RGB)
img_02_map = cv2.imread('images/im1_map.pgm')
img_02_map = cv2.cvtColor(img_02_map,cv2.COLOR_BGR2RGB)

ground_venus = cv2.imread('venus/disp2.pgm', 0)

print('What image do you want to use? ')
img_title = input("-->")

book = xlwt.Workbook()

window_sizes = [7, 9,11,13,15]
outcome = ["Mean disparity error", "Mean squared error", "Standard deviation of disparity error", "Nr of large errors", "Fraction of large errors"]
margins = [3, 4,6]


if img_title == "Tsukuba":
	print(' ')
	
	for indexing, margin in enumerate(margins):
		sh = book.add_sheet("Tsukuba_%s" %margin)

		for index, each in enumerate(window_sizes):
			sh.write(0, index+1, each)

		for index, every in enumerate(outcome):
			sh.write(index+1, 0, every)
		
		for index, window_size in enumerate(window_sizes):
			
			print('Start pyramidal stereo matching - Tsukuba')
			disparity_map_tsu = run_stereo_matching(img_02_tsu, img_01_tsu, windowsize = window_size, limit=margin)
			
			print('\n -------------------------------------- \n')
			print('STATISTICS FOR WINDOW SIZE ', window_size, '=')
			vars = tester(disparity_map_tsu[3], truedisp_tsu)
			print('\n -------------------------------------- \n')

			for ind, var in enumerate(vars):
				sh.write(ind+1, index+1, var)
		
			print(' ')
			print('Scale and save Tsubuka image')
			scaling = np.max(disparity_map_tsu[3])
			image_tsu = np.multiply(disparity_map_tsu[3], scaling)
			cv2.imwrite('disparity_tsu_w%s_m%s.png' % (window_size, margin),image_tsu)
			
			for i in range(0,4):
				scaling = np.max(disparity_map_tsu[i])
				image_tsu = np.multiply(disparity_map_tsu[i], scaling)
				cv2.imwrite('disparity_tsu_w%s_m%s_layer%s.png' % (window_size, margin, i),image_tsu)
	
if img_title == "Venus":
	print(' ')
		
	for indexing, margin in enumerate(margins):
		sh = book.add_sheet("Venus_%s" %margin)

		for index, each in enumerate(window_sizes):
			sh.write(0, index+1, each)

		for index, every in enumerate(outcome):
			sh.write(index+1, 0, every)
		
		for index, window_size in enumerate(window_sizes):
			
			print('Start pyramidal stereo matching - Venus')
			disparity_map_venus = run_stereo_matching(img_02_venus, img_01_venus, windowsize = window_size, limit=margin, cv = 1)
			
			print('\n -------------------------------------- \n')
			print('STATISTICS FOR WINDOW SIZE ', window_size, '=')
			vars = tester(disparity_map_venus[3], ground_venus)
			print('\n -------------------------------------- \n')

			for ind, var in enumerate(vars):
				sh.write(ind+1, index+1, var)

			print('Scale and save Venus image')
			scaling = np.max(disparity_map_venus[3])
			image_venus = np.multiply(disparity_map_venus[3], scaling)
			cv2.imwrite('disparity_venus_w%s_m%s.png' % (window_size, margin),image_venus)
			print(' ')

if img_title == "Map":
	for indexing, margin in enumerate(margins):
		for index, window_size in enumerate(window_sizes):
			print(' ')
			print('Start pyramidal stereo matching - Map')
			disparity_map_map = run_stereo_matching(img_02_map, img_01_map, window_size, margin, cv = 1)

			print('Scale and save Map image')
			scaling = np.max(disparity_map_map[3])
			image_map = np.multiply(disparity_map_map[3], scaling)
			cv2.imwrite('disparity_map_w%s_m%s.png' % (window_size, margin),image_map)
print(' ')


book.save("stats_%s.xls" %img_title)
