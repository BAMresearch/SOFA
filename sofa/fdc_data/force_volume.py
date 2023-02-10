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
from typing import List, Dict, Tuple, Type

import numpy as np

from fdc_data.force_distance_curve import ForceDistanceCurve
from fdc_data.average_force_distance_curve import AverageForceDistanceCurve
from fdc_data.channel import Channel

class ForceVolume():
	""""""
	def __init__(self):
		self.identifier: str
		self.size: List[int]
		self.forceDistanceCurves: List[Type[ForceDistanceCurve]]
		self.averageForceDistanceCurve: Type[AverageForceDistanceCurve]
		self.channels: List[Type[Channel]]
		self.inactiveForceDistanceCurves: List[int] = []

		self.guiInterface: Dict

	def import_data(self, importOptions) -> None:
		""""""
		pass 

	def correct_data(self) -> None:
		""""""
		for forceDistanceCurve in self.forceDistanceCurves:
			forceDistanceCurve.correct_raw_data()

	def calculate_channel_data(self) -> None: 
		""""""
		pass

	def calculate_average_data(self) -> None:
		""""""
		pass

	def plot_data(self) -> None:
		""""""
		pass

	def ploat_data_as_lineplot(self) -> None:
		""""""
		pass

	def plot_data_as_heatmap(self) -> None:
		""""""
		pass

	def plot_data_as_histogram(self) -> None:
		""""""
		pass

	def export_data(self) -> None: 
		""""""
		pass