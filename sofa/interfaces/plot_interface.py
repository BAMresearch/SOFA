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

class PlotInterface():
	"""


	Attributes
	----------
	inactiveDataPoints : List[int]

	heatmapOrientationMatrix : np.ndarray

	heatmapSelectedArea : List[]

	histogramBins : 
	"""
	def __init__(self) -> None:
		"""
		"""
		self.size = 
		self.inactiveDataPoints: List = []

		self.linePlotForceDistanceLines: List = []
		self.linePlotAverageLines: List = []

		self.heatmapOrientationMatrix: np.ndarray = self._create_heatmap_orientation_matrix()
		self.heatmapSelectedArea: List = []  

		self.histogramBins: 

	def _create_heatmap_orientation_matrix(self) -> np.ndarray:
		"""
		"""
		return np.arange(self.size[0] * self.size[1]).reshape(self.size)

	def 

