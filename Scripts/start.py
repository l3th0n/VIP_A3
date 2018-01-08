
print('Loading packages')
import cv2
import matplotlib.pyplot as plt

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

print(' ')
print('Start pyramidal stereo matching - Tsukuba')
disparity_map_tsu = run_stereo_matching(img_01_tsu, img_02_tsu)
print('\n -------------------------------------- \n')
print(tester(disparity_map_tsu[3], truedisp_tsu))
print('\n -------------------------------------- \n')

print(' ')
print('Scale and save Tsubuka image')
scaling = np.max(disparity_map_tsu[3])
image_tsu = np.multiply(disparity_map_tsu[3], scaling)
cv2.imwrite('disparity_tsu.png',image_tsu)
print(' ')


print('Start pyramidal stereo matching - Venus')
disparity_map_venus = run_stereo_matching(img_01_venus, img_02_venus, cv = 1)

print('Scale and save Venus image')
scaling = np.max(disparity_map_venus[3])
image_venus = np.multiply(disparity_map_venus[3], scaling)
cv2.imwrite('disparity_venus.png',image_venus)
print(' ')

print(' ')
print('Start pyramidal stereo matching - Map')
disparity_map_map = run_stereo_matching(img_01_map, img_02_map, cv = 1)

print('Scale and save Map image')
scaling = np.max(disparity_map_map[3])
image_map = np.multiply(disparity_map_map[3], scaling)
cv2.imwrite('disparity_map.png',image_map)