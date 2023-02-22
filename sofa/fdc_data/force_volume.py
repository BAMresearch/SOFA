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

from fdc_data.force_distance_curve import ForceDistanceCurve
from fdc_data.average_force_distance_curve import AverageForceDistanceCurve
from fdc_data.channel import Channel

class ForceVolume():
	"""

	"""
	def __init__(self):
		"""
		"""
		self.identifier: str
		self.size: Tuple[int]
		self.forceDistanceCurves: List[ForceDistanceCurve]
		self.averageForceDistanceCurve: AverageForceDistanceCurve
		self.channels: List[Channel]
		self.inactiveForceDistanceCurves: List[int] = []

		self.guiInterface: Dict

	def import_data(self, importedData:nt.): -> None:
		"""
		"""
		self.identifier = importedData.filename
		self.size = importedData.size

		self._import_force_distance_curves(
			importedData.approachCurves
		)

	def _import_force_distance_curves(
		importedApproachCurves: List[nt.ForceDistanceCurve]
	) -> None
		"""
		"""
		for index, approachCurve in enumerate(importedApproachCurves):
			self.forceDistanceCurves.append(
				ForceDistanceCurve(
					identifier="Curve_" + Index,
					dataApproachRaw=approachCurve
				)
			)

	def correct_data(self) -> None:
		"""
		"""
		for forceDistanceCurve in self.forceDistanceCurves:
			forceDistanceCurve.correct_raw_data()

	def calculate_channel_data(self) -> None: 
		"""
		"""
		for channelName, caluclate_channel in channels.items():
			self.channels.append(
				Channel(
					identifier=channelName,
					data=
				)
			)

	def calculate_average_data(self) -> None:
		"""
		"""
		pass

	def plot_data_as_lineplot(self) -> None:
		"""
		"""
		pass

	def plot_data_as_heatmap(self) -> None:
		"""
		"""
		pass

	def plot_data_as_histogram(self) -> None:
		"""
		"""
		pass

	def export_data(self) -> None: 
		"""
		"""
		pass