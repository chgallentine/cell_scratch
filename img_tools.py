# -*- coding: utf-8 -*-
# @Author: charliegallentine
# @Date:   2020-06-14 18:07:01
# @Last Modified by:   Charlie Gallentine
# @Last Modified time: 2020-06-21 17:50:40

import cv2
import numpy as np 

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


