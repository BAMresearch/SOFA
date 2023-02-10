"""
This file is part of SOFA.
SOFA is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SOFA is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SOFA.  If not, see <http://www.gnu.org/licenses/>.
"""
from collections import namedtuple
from typing import List, Dict, Tuple

import numpy as np

class AverageForceDistanceCurve():
	def __init__(self):
		self.DataApproach: np.ndarray 	# need better name
		self.DataContact: np.ndarray 	# need better name
		self.averageDataApproach: np.ndarray
		self.averageDataContact: np.ndarray
		self.standardDeviationApproach: np.ndarray
		self.standardDeviationContact: np.ndarray
		self.lineRepresentation: matplotlib.lines.Line2D

	def calculate_(self) -> None:
		""""""
		pass

	def calculate_average(self) -> None:
		""""""
		self.averageDataApproach = 
		self.averageDataContact = 

	def calculate_standard_deviation(self) -> None:
		""""""
		self.standardDeviationApproach = np.asarray(
			[np.nanstd(nthValues) for nthValues in zip(*NormedCurves.yValuesLeft)]
		)
		self.standardDeviationContact = np.asarray(
			[np.nanstd(nthValues) for nthValues in zip(*NormedCurves.yValuesRight)]
		)

	def create_line_representation(self) -> None: 
		""""""
		self.lineRepresentation =  

	def create_line_representation_as_errorbar(self) -> None:
		""""""
		self.lineRepresentation =  

	def add_line_representation_to_plot(self) -> None:
		""""""
		pass 

	def remove_line_representation_from_plot(self) -> None:
		""""""
		pass