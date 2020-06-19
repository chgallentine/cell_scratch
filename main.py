# -*- coding: utf-8 -*-
# @Author: Charlie Gallentine
# @Date:   2020-06-19 09:34:03
# @Last Modified by:   Charlie Gallentine
# @Last Modified time: 2020-06-19 15:23:18

from img_tools import *

import cv2

which_display=0
mindist_slider_val = 0
threshold_slider_val = 0
threshold_slider_max = 255
mindist_slider_max = 800
title_window = 'Threshold Value'

def on_trackbar_threshold(val):
	global threshold_slider_val

	threshold_slider_val = val 
	set_images(val)

def on_trackbar_mindist(val):
	global mindist_slider_val

	mindist_slider_val = val 
	set_images(val)

def set_images(val):
	global mindist_slider_val

	dst = img_threshold(src,val)
	src_cpy = src.copy()

	kernel = np.ones((11,11),np.uint8)
	dst = cv2.morphologyEx(dst, cv2.MORPH_GRADIENT, kernel)

	# for i,row in enumerate(dst):
	for i in range(1,len(dst),3):
		left,right = contiguous_black_pixels(dst[i],minimum=mindist_slider_val)
		src_cpy[i,left:right] = 0

	# flooded_mask = fill_holes(dst)
	# flooded_mask = img_sum_box2d(dst,w=21)

	dst_rgb = np.stack((dst,)*3, axis=-1)
	src_rgb = np.stack((src_cpy,)*3, axis=-1)

	image_to_display = np.vstack((src_rgb,dst_rgb)) 

	# if which_display == 0:
	# 	print("Thresholded Image")
	# 	image_to_display = dst
	# else:
	# 	print("Source Image")
	# 	image_to_display = src_cpy

	resized = cv2.resize(image_to_display, (960, 540,),interpolation = cv2.INTER_AREA)
	cv2.moveWindow(title_window, 40,30)
	cv2.imshow(title_window, resized)




src = np.array(cv2.imread('cell.jpg',0))

cv2.namedWindow(title_window)

trackbar_name = 'Threshold Value'
cv2.createTrackbar(trackbar_name, title_window , 0, threshold_slider_max, on_trackbar_threshold)
trackbar_name = 'Min Gap Width'
cv2.createTrackbar(trackbar_name, title_window , 0, mindist_slider_max, on_trackbar_mindist)

# Show some stuff
on_trackbar_threshold(0)
on_trackbar_mindist(0)

# Wait until user press some key
while(1):
	k = cv2.waitKey(33)
	if k==27:    # Esc key to stop
		break
	elif k==ord('t'):
		print('Toggle Display')
		which_display = (which_display + 1) % 2
		set_images(threshold_slider_val)




















