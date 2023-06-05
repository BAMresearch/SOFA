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
	Interface between a force volume and the presentation
	of the force volume in the different plots.

	Attributes
	----------
	size : tuple[int]
		Size of the associated force volume.
	inactiveDataPoints : list[int]
		Inactive force distance curve/data points
		of the force volume.
	forceDistanceLines : list[mpl.lines.Line2D]
		Displayable line representation of every
		force distance curve of the associated force
		volume.
	averageLines : list[mpl.lines.Line2D]
		Displayable line representation of the
		average curve of the associated force volume.
	zoomHistory : list[nt.ViewLimits]
		Contains the x and y axis limits of the different
		zoom settings.
	orientationMatrix : np.ndarray
		Contains the original position of the data points
		in the current orientation of the channel.
	selectedArea : list[tuple[int]]
		X and y coordinates of the data points
		within the selected area of the heatmap. 
	selectedAreaOutlines : list[mpl.lines.Line2D]
		Outlines of the selected area in the 
		heatmap.
	binValues : list[float]
		Values of the bins from the general channel data
		displayed in the histogram.
	"""
	def __init__(
		self, 
		size,
		forceDistanceCurves
	) -> None:
		"""
		Initialize a plot interface, create a line
		representation for every force distance curve
		and initialize the orientation matrix.
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
	) -> None:
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

	def delete_average_lines(self) -> None: 
		"""
		Delete the line representations of 
		the average force distance curve.
		"""
		for line in self.averageLines:
			line.remove()
		self.averageLines = []

	def check_active_data_points(self) -> bool:
		"""
		Checks if any data points are still active

		Returns
		-------
		hasActiveDataPoints : bool
			True if any data point is still active
			false otherwise
		"""
		numberOfDataPoints = self.size[0] * self.size[1]
		if len(self.inactiveDataPoints) == numberOfDataPoints:
			return False 
		return True

	def init_orientation_matrix(self) -> None:
		"""
		Initialize the orientation matrix with the default
		orientation of the channels.
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
		Add a new data point to the inactive
		data points if he is not already inactive (no 
		mapping is required as the points only come 
		from the line plot).

		Parameters
		----------
		inactiveDataPoint : int
			New inactive data point.
		"""
		if inactiveDataPoint not in self.inactiveDataPoints:
			self.inactiveDataPoints.append(inactiveDataPoint)

	def remove_inactive_data_point(
		self,
		inactiveDataPoint: int
	) -> None: 
		"""
		Remove a data point from the inactive data 
		points if he is inactive (no mapping is required 
		as the points only come from the line plot).

		Parameters
		----------
		inactiveDataPoint : int
			Data point who becomes active again.
		"""
		if inactiveDataPoint in self.inactiveDataPoints:
			self.inactiveDataPoints.remove(inactiveDataPoint)

	def add_inactive_data_points(
		self, 
		inactiveDataPoints: List[int]
	) -> None: 
		"""
		Add new data points to the inactive data points 
		by mapping them to the orientation matrix.

		Parameters
		----------
		inactiveDataPoints : list[int]
			Contains all data points which are added
			to the inactive data points.
		"""
		flatOrientationMatrix = self.orientationMatrix.flatten()

		# Map new data points to the current alignment.
		for inactiveDataPoint in inactiveDataPoints:
			self.inactiveDataPoints.append(flatOrientationMatrix[inactiveDataPoint])
		
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