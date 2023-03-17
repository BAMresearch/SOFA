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
from fdc_data.force_distance_curve import ForceDistanceCurve
from fdc_data.average_force_distance_curve import AverageForceDistanceCurve
from fdc_data.channel import Channel

class ForceVolume():
	"""
	A set of force distance curves and 

	Attributes
	----------
	name : str
		Name of the measurement data.
	size : tuple[int]
		Number of force distance curves as the width and height 
		of the measurement grid.
	metadata : dict
		
	forceDistanceCurves : list[ForceDistanceCurve]
		
	averageForceDistanceCurve : AverageForceDistanceCurve
		The average of the currently active force distance
		curves.
	channels : list[Channel]
		
	inactiveForceDistanceCurves : list[int]
		
	guiInterface : dict

	"""
	def __init__(self):
		"""
		Initialize an empty force volume.
		"""
		self.name: str
		self.size: Tuple[int]
		self.metadata: Dict
		self.forceDistanceCurves: List[ForceDistanceCurve]
		self.averageForceDistanceCurve: AverageForceDistanceCurve
		self.channels: List[Channel]
		self.inactiveForceDistanceCurves: List[int] = []

		self.guiInterface: Dict

	def import_data(self, importedData: Dict) -> None:
		"""


		Parameters
		----------
		importedData : dict

		"""
		self.name = importedData["measurementData"].filename
		self.size = importedData["measurementData"].size

		self._import_force_distance_curves(
			importedData["measurementData"].approachCurves
		)

	def _import_force_distance_curves(
		importedApproachCurves: List[nt.ForceDistanceCurve]
	) -> None:
		"""
		Create a ForceDistanceCurve object for every imported
		approach measurement curve.
		
		Parameters
		----------
		importedApproachCurves : List[nt.ForceDistanceCurve]
			Contains every imported approach curve of the 
			measurement.
		"""
		for index, approachCurve in enumerate(importedApproachCurves):
			self.forceDistanceCurves.append(
				ForceDistanceCurve(
					name="Curve_" + Index,
					dataApproachRaw=approachCurve
				)
			)

	def correct_data(self) -> None:
		"""
		Correct the data of all force distance curves in the
		force volume.
		"""
		for forceDistanceCurve in self.forceDistanceCurves:
			forceDistanceCurve.correct_raw_data()

	def calculate_channel_data(self) -> None: 
		"""
		
		"""
		for channelName, caluclate_channel in channels.items():
			"""
			self.channels.append(
				Channel(
					name=channelName,
					data=
				)
			)
			"""
			pass

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