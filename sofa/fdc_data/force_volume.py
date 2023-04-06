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
from data_processing.calculate_channel_data import calculate_channel_data
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
	imageData : dict
		Optional image data.
	forceDistanceCurves : list[ForceDistanceCurve]
		
	averageForceDistanceCurve : AverageForceDistanceCurve
		The average of the currently active force distance
		curves.
	channels : list[Channel]

	"""
	def __init__(self):
		"""
		Initialize an empty force volume.
		"""
		self.name: str
		self.size: Tuple[int]
		self.imageData: Dict
		self.forceDistanceCurves: List[ForceDistanceCurve]
		self.averageForceDistanceCurve: AverageForceDistanceCurve
		self.channels: List[Channel]

	def set_imported_data(self, importedData: Dict) -> None:
		"""
		

		Parameters
		----------
		importedData : dict
			Data from the imported measurement.
		"""
		# Set mandatory data.
		self.name = importedData["measurementData"].filename
		self.size = importedData["measurementData"].size

		self._create_force_distance_curves(
			importedData["measurementData"].approachCurves
		)
		# Set optional data if imported.
		if "imageData" in importedData:
			self.imageData = importedData["imageData"]
		if "channelData" in importedData:
			pass

	def _create_force_distance_curves(
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

	def correct_force_distance_curves(self) -> None:
		"""
		Correct the raw data of all force distance 
		curves in the force volume.
		"""
		for forceDistanceCurve in self.forceDistanceCurves:
			forceDistanceCurve.correct_raw_data()

	def calculate_channel_data(self) -> None: 
		"""
		
		"""
		channels = calculate_channel_data(
			self.forceDistanceCurves,
			self.size
		)

		for channelName, channelData in channels.items():
			self.channels.append(
				Channel(
					name=channelName,
					size=self.size,
					data=channelData
				)
			)

	def calculate_average_data(self) -> None:
		"""
		Calculate the average from the currently active 
		force distance curves.
		"""
		pass

	def get_force_distance_curves_lines(
		self
	) -> List:
		"""
		"""
		return [
			forceDistanceCurve.lineRepresentationCorrectedData
			for forceDistanceCurve
			in self.forceDistanceCurves
		]

	def get_heatmap_data(
		self,
		activeChannel: str
	) -> np.ndarray:
		"""
		"""
		return self.channels[activeChannel].get_active_heatmap_data(
			self.inactiveDataPoints
		)

	def get_histogram_data(
		self,
		activeChannel: str,
		active: bool = True
	) -> np.ndarray:
		"""
		"""
		if active:
			return self.channels[activeChannel].get_active_histogram_data(
				self.inactiveDataPoints
			)
		else:
			return self.channels[activeChannel].get_histogram_data()