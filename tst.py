# -*- coding: utf-8 -*-
# @Author: Charlie Gallentine
# @Date:   2020-06-19 11:23:59
# @Last Modified by:   Charlie Gallentine
# @Last Modified time: 2020-06-21 17:15:34

import numpy as np 
import cv2

def contiguous_black_pixels(arr,minimum=50):
	left = 0
	right = 0

	arr1 = arr.copy()

	indices = [i for i in range(len(arr1))]
	
	arr_indexed = np.vstack((arr1,indices))

	arr_threshold = [i for i in np.split(arr_indexed, np.where(arr_indexed[0] != 0)[0],axis=1) if len(i[0]) >= minimum]
	try:
		left = arr_threshold[0][1][0]
		right = arr_threshold[-1][1][-1]
	except:
		left = 0
		right = 0

	return left,right

def img_thresholdf(file, val=128):
	img = cv2.imread(file,0)

	ret,thresh1 = cv2.threshold(img.copy(),val,255,cv2.THRESH_BINARY)

	return thresh1
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



# arr = np.array([
# 	[255,0,0,0,255,0,0,0,255,0,0,0,255],
# 	[255,0,255,0,255,0,255,0,255,0,255,0,255],
# 	[255,255,0,0,0,0,255,0,255,0,0,255,255],
# 	[255,0,0,0,0,0,0,0,0,0,0,0,255],
# 	[255,255,255,255,255,255,255,255,255,255,255,255,255],
# 	[255,255,255,0,0,0,255,0,255,0,0,255,255],
# 	[0,0,0,0,0,0,0,0,0,0,0,0,0],
# 	])

arr = img_thresholdf('cell.jpg', val=128)

print(arr.shape)

print(cont_row(arr,minimum=5))
# print(contiguous_black_pixels(arr,minimum=4))



















