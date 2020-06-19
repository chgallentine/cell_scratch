# -*- coding: utf-8 -*-
# @Author: Charlie Gallentine
# @Date:   2020-06-19 09:34:03
# @Last Modified by:   Charlie Gallentine
# @Last Modified time: 2020-06-19 09:52:19

from img_tools import *

import cv2

alpha_slider_max = 255
title_window = 'Threshold Value'

def on_trackbar_threshold(val):
    dst = img_threshold(src,val)

    kernel = np.ones((5,5),np.uint8)
    dst = cv2.morphologyEx(dst, cv2.MORPH_GRADIENT, kernel)

    dst = cv2.resize(dst, (960, 540))   
    cv2.imshow(title_window, dst)


src = cv2.imread('cell.jpg',0)

cv2.namedWindow(title_window)

trackbar_name = 'Alpha x %d' % alpha_slider_max
cv2.createTrackbar(trackbar_name, title_window , 0, alpha_slider_max, on_trackbar_threshold)
# Show some stuff
on_trackbar(0)
# Wait until user press some key
cv2.waitKey()