# -*- coding: utf-8 -*-
# @Author: Charlie Gallentine
# @Date:   2020-06-19 11:23:59
# @Last Modified by:   Charlie Gallentine
# @Last Modified time: 2020-06-19 12:26:52

import numpy as np 

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




arr = np.array([1,1,1,1,1,1,1,1,1,1])

print(contiguous_black_pixels(arr,minimum=4))