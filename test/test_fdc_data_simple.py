import unittest
import numpy as np
import sys
import os
sys.path.append(os.path.join("..", "sofa"))

from fdc_data import FdcData

class TestFdcData(unittest.TestCase):
	""""""
	def test_calculate_end_of_zeroline_valid(self):
		""""""
		pass

	def test_calculate_end_of_zeroline_invalid(self):
		""""""
		pass

	def test_shift_y_axis_valid(self):
		"""was sollte wie passieren (erfolgreich/ fehlerhaft mit ergebnis x)"""
		xData = np.array([1,2,3,4,5,6,7,8,9,10])
		yData = np.array([6,5,6,4,3,4,6,7,8,11])

		results = FdcData.shift_y_axis(self, xData, yData)

		np.testing.assert_array_equal(yData - 6, results[0])
		assert 6 == results[1]

	def test_shift_y_axis_invalid(self):
		""""""
		pass

	def test_shift_x_axis_valid(self):
		""""""
		xData = np.array([1,2,3,4,5,6,7,8,9,10])
		yData = np.array([1,0,1,-1,-2,-1,1,2,3,6])
		endOfZeroline = 2

		results = FdcData.shift_x_axis(self, xData, yData, endOfZeroline)
		
		np.testing.assert_array_equal(xData - 6.5, results[0])
		assert 6.5 == results[1]
		assert 5 == results[2]

	def test_shift_x_axis_invalid_no_poc(self):
		""""""
		xData = np.array([1,2,3,4,5,6,7,8,9,10])
		yData = np.array([1,0,1,-1,-2,-1,-1,-2,-3,-4])
		endOfZeroline = 2

		results = FdcData.shift_x_axis(self, xData, yData, endOfZeroline)
	
		np.testing.assert_array_equal(xData, results[0])
		np.testing.assert_equal(np.nan, results[1])
		np.testing.assert_equal(np.nan, results[2])
	
	def test_locate_attractive_area(self):
		""""""
		data = np.array([2,1,-1,-2,-1,0,2,4,6,8])
		pointOfContact = 5

		assert (1,5) == FdcData.locate_attractive_area(data, pointOfContact)

	def test_calculate_z_piezo_at_maximum_deflection(self):
		""""""
		pass

	def test_calculate_max_deflection(self):
		""""""
		pass

	def test_calculate_force_distance_topography(self):
		""""""
		pass

	def test_calculate_attractive_area(self):
		""""""
		pass

	def test_calculate_deflection_attractive(self):
		""""""
		pass

	def test_calculate_z_attractive(self):
		""""""
		pass

	def test_calculate_stiffness_stiffness(self):
		""""""
		xData = np.array([1,2,3,4])
		yData = np.array([1,2,3,4])

		np.testing.assert_almost_equal(
			1, 
			FdcData.calculate_stiffness(xData, yData)
		)

	def test_calculate_curves_with_artifacts_no_artifact(self):
		"""was sollte wie passieren (erfolgreich/ fehlerhaft mit ergebnis x)"""
		data = np.array([1,2,3,4])

		assert 0 == FdcData.calculate_curves_with_artifacts(data)

	def test_calculate_curves_with_artifacts_with_artifact(self):
		""""""
		data = np.array([1,2,1,3,4])
		
		assert 1 == FdcData.calculate_curves_with_artifacts(data)

	def test_align_ibw_curve_length(self):
		""""""
		pass


if __name__ == '__main__':
    unittest.main()