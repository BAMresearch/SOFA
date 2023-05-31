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
	size : tuple[int]

	inactiveDataPoints : list[int]

	forceDistanceLines : list[mpl.lines.Line2D]

	averageLines : list[mpl.lines.Line2D]
	
	zoomHistory : list[nt.ViewLimits]

	orientationMatrix : np.ndarray

	selectedArea : list[tuple[int]]

	selectedAreaOutlines : list[mpl.lines.Line2D]

	binValues : list[float]
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
		forceDistanceCurves: List
	) -> List:
		"""
		Create a displayable line representation of every 
		corrected force distance curve of a force volume.

		Parameters
		----------
		forceDistanceCurves : list[nt.ForceDistanceCurve]
			Piezo(x) and deflection (y) values of every
			corrected fore distance curve of a force volume.
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
		Reset the inactive data points.
		"""
		self.inactiveDataPoints = []

	def add_inactive_data_point(
		self, 
		inactiveDataPoint: int
	) -> None: 
		"""

		Parameters
		----------
		inactiveDataPoint : int
		"""
		if inactiveDataPoint not in self.inactiveDataPoints:
			self.inactiveDataPoints.append(inactiveDataPoint)

	def remove_inactive_data_point(
		self,
		inactiveDataPoint: int
	) -> None: 
		"""

		Parameters
		----------
		inactiveDataPoint : int
		"""
		if inactiveDataPoint in self.inactiveDataPoints:
			self.inactiveDataPoints.remove(inactiveDataPoint)

	def add_inactive_data_points(
		self, 
		inactiveDataPoints: List[int]
	) -> None: 
		"""

		Parameters
		----------
		inactiveDataPoints : list[int]

		"""
		flatHeatmapOrientationMatrix = self.orientationMatrix.flatten()

		# Map new data points to the current alignment.
		for inactiveDataPoint in inactiveDataPoints:
			self.inactiveDataPoints.append(flatHeatmapOrientationMatrix[inactiveDataPoint])
		
		# Remove duplicates.
		self.inactiveDataPoints = list(set(self.inactiveDataPoints))

	def flip_orientation_matrix_horizontal(self) -> None: 
		"""
		Flip the orientation matrix of the heatmap horizontally.
		"""
		self.orientationMatrix = np.flip(self.orientationMatrix, 0)

	def flip_orientation_matrix_vertical(self) -> None: 
		"""
		Flip the orientation matrix of the heatmap vertically.
		"""
		self.orientationMatrix = np.flip(self.orientationMatrix, 1)

	def rotate_orientation_matrix(self) -> None: 
		"""
		Rotate the orientation matrix of the heatmap by 90 degrees.
		"""
		self.orientationMatrix = np.rot90(self.orientationMatrix)