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
from typing import List, Dict, Tuple

import numpy as np

import data_visualization.plot_data as plt_data

class PlotInterface():
	"""


	Attributes
	----------
	inactiveDataPoints : List[int]

	heatmapOrientationMatrix : np.ndarray

	heatmapSelectedArea : List[]

	histogramBins : 
	"""
	def __init__(
		self, 
		size,
		forceDistanceCurves
	) -> None:
		"""
		"""
		self.size: Tuple[int] = size
		self.inactiveDataPoints: List = []

		self.forceDistanceLines: List = []
		self.averageLines: List = []
		self.zoomHistory: List = []

		self.orientationMatrix: np.ndarray
		self.selectedArea: List = []
		self.selectedAreaOutlines: List = []  

		self.binValues: List = []

		self._create_force_distance_lines(
			forceDistanceCurves
		)
		self.init_orientation_matrix()

	def _create_force_distance_lines(
		self, 
		forceDistanceCurves
	) -> List:
		"""
		"""
		for index, forceDistanceCurve in enumerate(forceDistanceCurves):
			self.forceDistanceLines.append(
				plt_data.create_corrected_line(
					str(index),
					forceDistanceCurve
				)
			)

	def init_orientation_matrix(self) -> np.ndarray:
		"""
		"""
		self.orientationMatrix = np.arange(
			self.size[0] * self.size[1]
		).reshape(self.size)

	def reset_inactive_data_points(self) -> None: 
		"""
		"""
		self.inactiveDataPoints = []

	def add_inactive_data_point(
		self, 
		inactiveDataPoint: int
	) -> None: 
		"""
		"""
		if inactiveDataPoint not in self.inactiveDataPoints:
			self.inactiveDataPoints.append(inactiveDataPoint)

	def remove_inactive_data_point(
		self,
		inactiveDataPoint: int
	) -> None: 
		"""
		"""
		if inactiveDataPoint in self.inactiveDataPoints:
			self.inactiveDataPoints.remove(inactiveDataPoint)

	def add_inactive_data_points(
		self, 
		inactiveDataPoints: List[int]
	) -> None: 
		"""
		"""
		flatHeatmapOrientationMatrix = self.orientationMatrix.flatten()

		# Map new data points to the current alignment.
		for inactiveDataPoint in inactiveDataPoints:
			self.inactiveDataPoints.append(flatHeatmapOrientationMatrix[inactiveDataPoint])
		
		# Remove duplicates.
		self.inactiveDataPoints = list(set(self.inactiveDataPoints))

	def flip_orientation_matrix_horizontal(self) -> None: 
		"""
		"""
		self.orientationMatrix = np.flip(self.orientationMatrix, 0)

	def flip_orientation_matrix_vertical(self) -> None: 
		"""
		"""
		self.orientationMatrix = np.flip(self.orientationMatrix, 1)

	def rotate_orientation_matrix(self) -> None: 
		"""
		"""
		self.orientationMatrix = np.rot90(self.orientationMatrix)