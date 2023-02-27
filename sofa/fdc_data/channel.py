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

class Channel():
	"""
	

	Attributes
	----------
	identifier : str
		Name of the channel.
	rawData : np.ndarray
		Unmodified data of the channel used to restore
		data and orientation.
	data : np.ndarray
		Data of the channel with the current orientation,
		can be flipped or rotated.
	activeData : np.ndarray
		Active data of the channel with the current orientation.
	"""
	def __init__(
		self, 
		identifier: str, 
		data: np.ndarray
	):
		"""
		"""
		self.identifier: str = identifier
		self.rawData: np.ndarray = data.copy()
		self.data: np.ndarray = data.copy()
		self.activeData: np.ndarray = data.copy()

	def get_active_data(
		inactiveForceDistanceCurves: List[int]
	) -> None:
		""""""
		pass