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
	

	Attributes
	----------
	name : str
		Name of the channel.
	rawData : np.ndarray
		Unmodified data of the channel used to restore
		data and orientation.
	data : np.ndarray
		Data of the channel with the current orientation,
		can be flipped or rotated.
	"""
	def __init__(
		self,
		name: str,
		size: Tuple[int],
		data: np.ndarray
	):
		"""
		"""
		self.name: str = name
		self.size: Tuple = size
		self.rawData: np.ndarray = data.copy()
		self.data: np.ndarray = data.copy()

	def reset_data(self) -> None:
		"""
		"""
		self.data = self.rawData.copy()

	def get_active_heatmap_data(
		self,
		inactiveDataPoints: List[int]
	) -> np.ndarray:
		""""""
		pass

	def get_histogram_data(
		self
	) -> np.ndarray:
		"""
		"""
		return self.rawData.flatten().copy()

	def get_active_histogram_data(
		self,
		inactiveDataPoints: List[int]
	) -> np.ndarray:
		""""""
		histogramData = self.rawData.flatten().copy()
		activeHistogramData = np.delete(histogramData, inactiveDataPoints)

		return activeHistogramData