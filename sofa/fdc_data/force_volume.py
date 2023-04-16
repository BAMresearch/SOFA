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
	inactiveDataPoints : List[int]

	heatmapOrientaionMatrix : np.ndarray

	imageData : dict
		Optional image data.
	forceDistanceCurves : list[ForceDistanceCurve]
		
	channels : list[Channel]

	averageForceDistanceCurve : AverageForceDistanceCurve
		The average of the currently active force distance
		curves.
	"""
	def __init__(self, importedData: Dict) -> None:
		"""
		.

		Parameters
		----------
		importedData : Dict 

		"""
		self.name: str = importedData["measurementData"].filename
		self.size: Tuple[int] = importedData["measurementData"].size

		self.inactiveDataPoints: List = []
		self.heatmapOrientaionMatrix: np.ndarray = self._create_heatmap_orientation_matrix()

		self.imageData: Dict
		self.forceDistanceCurves: List[ForceDistanceCurve]
		self.channels: List[Channel]
		self.averageForceDistanceCurve: AverageForceDistanceCurve

		# Set optional data if imported.
		if "imageData" in importedData:
			self._set_image_data(importedData["imageData"])
		if "channelData" in importedData:
			self._set_channel_data(importedData["channelData"])
		# 
		self._create_force_distance_curves(
			importedData["measurementData"].approachCurves
		)
		# 
		self._correct_force_distance_curves()
		# 
		self._calculate_channel_data()

	def _create_heatmap_orientation_matrix(self) -> np.ndarray:
		"""
		"""
		return np.arange(self.size[0] * self.size[1]).reshape(self.size)

	def _set_image_data(self, imageData) -> None: 
		"""
		"""
		pass 

	def _set_channel_data(self, channelData) -> None: 
		"""
		"""
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

	def _correct_force_distance_curves(self) -> None:
		"""
		Correct the raw data of all force distance 
		curves in the force volume.
		"""
		for forceDistanceCurve in self.forceDistanceCurves:
			forceDistanceCurve.correct_raw_data()

	def _calculate_channel_data(self) -> None: 
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
			self.inactiveDataPoints,
			self.heatmapOrientaionMatrix
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