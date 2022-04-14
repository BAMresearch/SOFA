import pytest
import numpy as np

import sofa.data.process_data as pd

def test_correct_approach_curves_curves_can_be_corrected_simple_data():
	"""Successfully correct a set of simple curves by shifting 
	   the point of contcat of each curve to the origin."""
	pass

def test_correct_approach_curves_curves_can_not_be_corrected_simple_data():
	"""Fail to correct a set of simple curves by not being able 
	   to shift the point of contact of each curve to the origin."""
	pass

def test_shift_y_axis_y_axis_can_be_corrected_simple_data():
	"""Successfully correct the y axis by shifting it to zero."""
	pass

def test_shift_y_axis_y_axis_can_not_be_corrected_simple_data():
	"""Fail to correct the y axis since the end of the zero line 
	   could not be calculated."""
	pass

def test_calculate_end_of_zeroline_eoz_can_be_calculated_simple_data():
	"""Successfully calculate the end of the zeroline by finding the 
	   last point with a positive slope within the borders."""
	pass

def test_calculate_end_of_zeroline_eoz_can_not_be_calculated_simple_data():
	"""Fail to calculate the end of the zeroline since the curve has
	   no points with a positive slope within the borders."""
	xData = np.array([1,2,3,4,5,6,7,8,9,10])
	yData = np.array([1,0,1,-1,-2,-1,1,2,3,6])  
	leftBorder = 0
	rightBorder = 1
	   
	with pytest.raises(ValueError):
		pd.calculate_end_of_zeroline(
			xData, 
			yData, 
			leftBorder,
			rightBorder
		)

def test_shift_x_axis_x_axis_can_be_corrected_simple_data():
	"""Successfully correct the x axis by shifting it to zero."""
	xData = np.array([1,2,3,4,5,6,7,8,9,10])
	yData = np.array([1,0,1,-1,-2,-1,1,2,3,6])
	endOfZeroline = 2

	results = pd.shift_x_axis(xData, yData, endOfZeroline)
	
	np.testing.assert_array_equal(xData - 6.5, results[0])
	assert 6.5 == results[1]
	assert 5 == results[2]

def test_shift_x_axis_x_axis_can_not_be_corrected_simple_data():
	"""Fail to correct the x axis since the curve has no 
	   more negative values after the end of the zero line."""
	xData = np.array([1,2,3,4,5,6,7,8,9,10])
	yData = np.array([1,-1,-2,1,-2,1,2,2,4,5])
	endOfZeroline = 6

	results = pd.shift_x_axis(xData, yData, endOfZeroline)
	
	np.testing.assert_array_equal(xData, results[0])
	assert 6.5 == results[1]
	assert 5 == results[2]

def test_prepare_channel_data():
	""""""
	pass

def test_merge_dictionaries():
	""""""
	pass 