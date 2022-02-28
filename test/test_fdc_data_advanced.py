import unittest
import numpy as np
import sys
import os
sys.path.append(os.path.join("..", "sofa"))

from fdc_data import FdcData

class TestFdcData(unittest.TestCase):
	""""""	
	def test_correct_approach_curves_good_data_quality(self):
		"""The function should be able to correct every curve in the data set along the x and y axis."""
		pass

	def test_correct_approach_curves_poor_data_quality(self):
		"""The function should not be able to correct every curve in the data set along the x and y axis.
		   As a result, some curves remain unchanged. """
		pass

if __name__ == '__main__':
    unittest.main()