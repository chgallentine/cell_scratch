# -*- coding: utf-8 -*-
# @Author: Charlie Gallentine
# @Date:   2020-06-19 09:34:03
# @Last Modified by:   Charlie Gallentine
# @Last Modified time: 2020-06-21 18:09:22

import cv2
import numpy as np 
import os

# =============================================================================
# =============================================================================
# BEGIN GLOBAL VARIABLE DECLARATIONS
# =============================================================================
# =============================================================================
average_width = 0
total_area = 0

which_display=0
display_stats=False

mindist_slider_val = 0
threshold_slider_val = 0
threshold_slider_max = 255
mindist_slider_max = 800

title_window = 'Threshold Value'
src = None
src_original = None

# =============================================================================
# =============================================================================
# END GLOBAL VARIABLE DECLARATIONS
# =============================================================================
# =============================================================================

# =============================================================================
# =============================================================================
# BEGIN FUNCTION DEFINITIONS
# =============================================================================
# =============================================================================
def on_trackbar_threshold(val):
	global threshold_slider_val

	threshold_slider_val = val 
	set_images(val)

def on_trackbar_mindist(val):
	global mindist_slider_val

	mindist_slider_val = val 
	set_images(val)

def overlay_info(img):
	img[0:700,0:1300] = 255

	img = cv2.putText(
		img, 
		'Average Width (Pixels)', 
		(150,150), 
		cv2.FONT_HERSHEY_SIMPLEX, 
		3, 
		(0,0,255), 
		10, 
		cv2.LINE_AA) 

	img = cv2.putText(
		img, 
		str(int(average_width)), 
		(150,300), 
		cv2.FONT_HERSHEY_SIMPLEX, 
		3, 
		(0,0,255), 
		10, 
		cv2.LINE_AA) 

	img = cv2.putText(
		img, 
		'Total Area (Pixels)', 
		(150,450), 
		cv2.FONT_HERSHEY_SIMPLEX, 
		3, 
		(0,0,255), 
		10, 
		cv2.LINE_AA) 

	img = cv2.putText(
		img, 
		str(int(total_area)), 
		(150,600), 
		cv2.FONT_HERSHEY_SIMPLEX, 
		3, 
		(0,0,255), 
		10, 
		cv2.LINE_AA)

	return img

def set_images(val):
	global mindist_slider_val
	global threshold_slider_val
	global total_area
	global average_width

	dst = img_threshold(src,threshold_slider_val)
	src_cpy = src.copy()
	src_original_copy = src_original.copy()

	kernel = np.ones((11,11),np.uint8)
	dst = cv2.morphologyEx(dst, cv2.MORPH_GRADIENT, kernel)

	gap_data = cont_row(dst,minimum=mindist_slider_val)

	for row in gap_data:
		src_original_copy[row[0],row[1][0]:row[1][1],:] = 0
	
	row,gap = zip(*gap_data)
	gap = np.array(gap)
	gap_widths = np.diff(gap)
	average_width = np.average(gap_widths)
	total_area = np.sum(gap_widths)

	dst_rgb = np.stack((dst,)*3, axis=-1)
	# src_rgb = np.stack((src_cpy,)*3, axis=-1)

	image_to_display = None
	if which_display == 0:
		image_to_display = dst_rgb
	else:
		image_to_display = src_original_copy

	if display_stats:
		image_to_display = overlay_info(image_to_display)

	resized = cv2.resize(image_to_display, (960, 540,),interpolation = cv2.INTER_AREA)
	cv2.moveWindow(title_window, 40,30)
	cv2.imshow(title_window, resized)

def img_threshold(img, val):
	ret,thresh1 = cv2.threshold(img.copy(),val,255,cv2.THRESH_BINARY)

	return thresh1


def img_thresholdf(file, val=128):
	img = cv2.imread(file,0)

	ret,thresh1 = cv2.threshold(img.copy(),val,255,cv2.THRESH_BINARY)

	return thresh1

def img_sobel(img):
	return cv2.Sobel(img,cv2.CV_8U,1,0,ksize=5)

def img_sobelf(file):
	img = cv2.imread(file,0)
	sobel = cv2.Sobel(img.copy(),cv2.CV_8U,1,0,ksize=5)

	return sobel

def cont_row(arr,minimum=50):
	arr[:,0] = 255
	arr[:,-1] = 255

	arr = arr.astype('int16')

	dA = np.diff(arr)

	start = np.where(dA < 0)
	end = np.where(dA > 0)

	runs = end[1] - start[1]

	gt_min = np.where(runs >= minimum)

	start_row_indices = np.split(start[0][tuple(gt_min)], np.where(np.diff(start[0][tuple(gt_min)]))[0] + 1)
	start_col_indices = np.split(start[1][tuple(gt_min)], np.where(np.diff(start[0][tuple(gt_min)]))[0] + 1)

	end_row_indices = np.split(end[0][tuple(gt_min)], np.where(np.diff(end[0][tuple(gt_min)]))[0] + 1)
	end_col_indices = np.split(end[1][tuple(gt_min)], np.where(np.diff(end[0][tuple(gt_min)]))[0] + 1)

	end_rows = [i[-1] for i in end_row_indices]
	end_cols = [i[-1] for i in end_col_indices]

	start_rows = np.array((list(zip(*start_row_indices))[0]))
	start_cols = np.array((list(zip(*start_col_indices))[0]))

	return np.array(list(zip(start_rows,np.array(list(zip(start_cols,end_cols))))))

# =============================================================================
# =============================================================================
# END FUNCTION DEFINITIONS
# =============================================================================
# =============================================================================

# =============================================================================
# =============================================================================
# BEGIN SCRIPT EXECUTION
# =============================================================================
# =============================================================================
src = np.array(cv2.imread('cell.jpg',0))
src_original = np.array(cv2.imread('cell.jpg',1))

# Set up display functions/keyboard interactivity
cv2.namedWindow(title_window)

# Create Trackbars to control image thresholds
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
	elif k==ord('t'): # Toggle between src overlay/threshold image
		print('Toggle Display')
		which_display = (which_display + 1) % 2
		set_images(threshold_slider_val)
	elif k==ord('d'): # Toggle stats visibility
		print('Toggle Display Stats')
		display_stats = not display_stats
		set_images(threshold_slider_val)



















