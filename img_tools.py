# -*- coding: utf-8 -*-
# @Author: charliegallentine
# @Date:   2020-06-14 18:07:01
# @Last Modified by:   Charlie Gallentine
# @Last Modified time: 2020-06-19 09:51:21

import cv2
import numpy as np 

def img_threshold(img, val):
	ret,thresh1 = cv2.threshold(img,val,255,cv2.THRESH_BINARY)

	return thresh1


def img_thresholdf(file, val=128):
	img = cv2.imread(file,0)

	ret,thresh1 = cv2.threshold(img,val,255,cv2.THRESH_BINARY)

	return thresh1


def img_sobel(img):
	return cv2.Sobel(img,cv2.CV_8U,1,0,ksize=5)

def img_sobelf(file):
	img = cv2.imread(file,0)
	sobel = cv2.Sobel(img,cv2.CV_8U,1,0,ksize=5)

	return sobel

def img_sum_box2d(img, w=3):
	arr = np.array(img) 

	for i in range(w//2,len(img)-w//2):
		for j in range(w//2,len(img[0])-w//2):
			arr[i,j] = np.sum(img[i-w//2:i+w//2+1,j-w//2:j+w//2+1])

	return arr

def img_area_same_val(img,r,c,w=11):
	flatten_arr = np.ravel(img[r-w//2:r+w//2+1,c-w//2:c+w//2+1])
	return True if np.all(flatten_arr == flatten_arr[0])


# # img = np.array(img_sobelf('cell.jpg'))

# img = img_thresholdf('cell.jpg',val=170)

# cv2.imwrite('thresholded.png', img)

# kernel = np.ones((5,5),np.uint8)
# img = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

# cv2.imwrite('morphed.png', img)

# img = img_sobel(img)

# cv2.imwrite('edged.png', img)
