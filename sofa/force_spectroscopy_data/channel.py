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

import data_processing.named_tuples as nt

class Channel():
	"""
	A two dimensional parameter map of a force volume.

	Attributes
	----------
	name : str
		Name of the channel.
	size : tuple[int]
		Height and width of the channel corresponding to number 
		of force distance curves.
	rawData : np.ndarray
		Unmodified data of the channel used to restore
		data and orientation.
	data : np.ndarray
		Data of the channel with the current orientation -
		can be flipped or rotated by the toolbar.
	"""
	def __init__(
		self,
		name: str,
		size: Tuple[int],
		data: np.ndarray
	):
		"""
		Initialize a channel by setting its name, size and parameter data.

		Parameters
		----------
		name : str
			Name of the new channel
		size : tuple[int]
			Size of the force volume corresponding to the height
			and width of the channel.
		data : np.ndarray
			Parameter values calculated from the meta data 
			resulting from the correction of the force 
			distance curves of the force volume. 
		"""
		self.name: str = name
		self.size: Tuple = size
		self.rawData: np.ndarray = data.copy()
		self.data: np.ndarray = data.copy()

	def reset_data(self) -> None:
		"""
		Reset the orientation of the data.
		"""
		self.data = self.rawData.copy()

	def get_active_heatmap_data(
		self,
		inactiveDataPoints: List[int],
		heatmapOrientationMatrix: np.ndarray
	) -> np.ndarray:
		"""
		Get the active data of the channel displayable as heatmap.

		Parameters
		----------
		inactiveDataPoints : list[int]
			Indices of the currently inactive force distance curves.
		heatmapOrientationMatrix: np.ndarray
			Matrix showing the position of the force distance curves 
			in the channel with the current orientation.

		Returns
		-------
		activeHeatmapData : np.ndarray
			Channel data of the currently active force distance 
			curves.
		"""
		flatHeatmapData = self.data.copy().flatten()
		mappedInactiveDataPoints = self._map_heatmap_orientation_to_inactive_datapoints(
			inactiveDataPoints,
			heatmapOrientationMatrix.flatten()
		)
		np.put(
			flatHeatmapData, 
			mappedInactiveDataPoints,
			np.nan
		)
		activeHeatmapData = flatHeatmapData.reshape(self.size)

		return activeHeatmapData

	@staticmethod
	def _map_heatmap_orientation_to_inactive_datapoints(
		inactiveDataPoints: List[int],
		heatmapOrientationMatrix: np.ndarray
	) -> List[int]:
		"""
		Map the indices of the currently inactive force distance curves
		to the orientation of the heatmap. This is necessary because a 
		rotation or shift of the heatmap does not change the axis.

		Parameters
		----------
		inactiveDataPoints : list[int]
			Indices of the currently inactive force distance curves
		heatmapOrientationMatrix: np.ndarray
			Matrix showing the position of the force distance curves 
			in the channel with the current orientation.

		Returns
		-------
		mappedInactiveDataPoints : list[int]
			Indices of the currently inactive force distance curves
			taking into account the orientation of the heatmap. 
		"""
		return [
			np.where(dataPoint == heatmapOrientationMatrix)[0][0]
			for dataPoint in inactiveDataPoints
		]

	def get_histogram_data(
		self
	) -> np.ndarray:
		"""
		Get the data of the channel displayable as histogram.

		Returns
		-------
		validHistogramData : np.ndarray
			One dimensional channel data without potential nan values.
		"""
		histogramData = self.rawData.copy().flatten()
		validHistogramData = self._remove_nan_values(histogramData)

		return validHistogramData

	def get_active_histogram_data(
		self,
		inactiveDataPoints: List[int]
	) -> np.ndarray:
		"""
		Get the active data of the channel displayable as histogram.

		Parameters
		----------
		inactiveDataPoints : np.ndarray
			Indices of the currently inactive force distance curves

		Returns
		-------
		validActiveHistogramData : np.ndarray
			One dimensional channel data of the currently active 
			force distance curves without potential nan values.
		"""
		histogramData = self.rawData.copy().flatten()
		activeHistogramData = np.delete(histogramData, inactiveDataPoints)
		validActiveHistogramData = self._remove_nan_values(activeHistogramData)

		return validActiveHistogramData

	@staticmethod
	def _remove_nan_values(channelData: np.ndarray) -> np.ndarray:
		"""
		Remove potential nan values from the channel data, to 
		ensure the data is displayable as a histogram.

		Parameters
		----------
		channelData : np.ndarray
			Channel values which might contain nan values if a 
			force curve could not be corrected.

		Returns
		-------
		validChannelData : np.ndarray
			Channel values with no nan values.
		"""
		return channelData[np.isfinite(channelData)]

	def flip_channel_horizontal(self) -> None: 
		"""
		"""
		self.data = np.flip(self.data, 0)

	def flip_channel_vertical(self) -> None: 
		"""
		"""
		self.data = np.flip(self.data, 1)

	def rotate_channel(self) -> None: 
		"""
		"""
		self.data = np.rot90(self.data)