import numpy as np

import sofa.data.process_data as pd

def test_shift_x_axis_valid():
	""""""
	xData = np.array([1,2,3,4,5,6,7,8,9,10])
	yData = np.array([1,0,1,-1,-2,-1,1,2,3,6])
	endOfZeroline = 2

	results = pd.shift_x_axis(xData, yData, endOfZeroline)
	
	np.testing.assert_array_equal(xData - 6.5, results[0])
	assert 6.5 == results[1]
	assert 5 == results[2]