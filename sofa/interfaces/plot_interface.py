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

		self.linePlotForceDistanceLines: List = []
		self.linePlotAverageLines: List = []
		self.linePlotZoomHistory: List = []

		self.heatmapOrientationMatrix: np.ndarray
		self.heatmapSelectedAreaBorders: List = []  

		self.histogramBins: List = []

		self._create_line_plot_force_distance_lines(
			forceDistanceCurves
		)
		self._create_heatmap_orientation_matrix()

	def _create_line_plot_force_distance_lines(
		self, 
		forceDistanceCurves
	) -> List:
		"""
		"""
		for index, forceDistanceCurve in enumerate(forceDistanceCurves):
			self.linePlotForceDistanceLines.append(
				plt_data.create_corrected_line(
					str(index),
					forceDistanceCurve
				)
			)

	def _create_heatmap_orientation_matrix(self) -> np.ndarray:
		"""
		"""
		self.heatmapOrientationMatrix = np.arange(
			self.size[0] * self.size[1]
		).reshape(self.size)

	def reset_inactive_data_points(self) -> None: 
		"""
		"""
		self.inactiveDataPoints = []

	def add_inactive_data_point(
		self, 
		inactiveDataPoints: int
	) -> None: 
		"""
		"""
		self.inactiveDataPoints.append(inactiveDataPoints)

	def remove_inactive_data_point(
		self,
		inactiveDataPoints: int
	) -> None: 
		"""
		"""
		self.inactiveDataPoints.remove(inactiveDataPoints)