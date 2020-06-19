# -*- coding: utf-8 -*-
# @Author: charliegallentine
# @Date:   2020-06-14 18:07:01
# @Last Modified by:   Charlie Gallentine
# @Last Modified time: 2020-06-19 12:29:09

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

def img_sum_box2d(img, w=3):
	arr = [[np.sum(img[r,c-w//2:c+w//2+1]) for c in range(len(img[0]))] for r in range(w//2,len(img)-w//2)]

	padded_arr = np.pad(arr,(w//2,w//2),'maximum')
	return padded_arr

def img_area_same_val(img,r,c,w=11):
	flatten_arr = np.ravel(img[r-w//2:r+w//2+1,c-w//2:c+w//2+1])
	return True if np.all(flatten_arr == flatten_arr[0]) else False

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



def fill_holes(img):
	im_th = img.copy()

	# Copy the thresholded image.
	im_floodfill = im_th.copy()

	# Mask used to flood filling.
	# Notice the size needs to be 2 pixels than the image.
	h, w = im_th.shape[:2]
	mask = np.zeros((h+2, w+2), np.uint8)

	cv2.floodFill(im_floodfill, mask, (171,83), 255);

	# Invert floodfilled image
	im_floodfill_inv = cv2.bitwise_not(im_floodfill)

	return im_floodfill_inv 


