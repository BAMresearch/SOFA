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
from data_processing.calculate_average import calculate_average
from force_spectroscopy_data.force_distance_curve import ForceDistanceCurve
from force_spectroscopy_data.channel import Channel

class ForceVolume():
	"""
	A set of force distance curves, their related channels and 
	average curve.

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
		Every force distance curve of the force volume.
	channels : dict[Channel]
		All calculated and possibly imported channels.
	average : nt.
		The average data of the currently active force 
		distance curves.
	"""
	def __init__(self, importedData: Dict) -> None:
		"""
		Initialize a force volume by setting its name, size and if
		imported an additonal image and channel. Create a ForceDistanceCurve
		for every imported measurement curve, correct the measurement 
		data and calculate the channels.

		Parameters
		----------
		importedData : Dict 
			Data of all imported measurement files.
		"""
		self.name: str = importedData["measurementData"].filename
		self.size: Tuple[int] = importedData["measurementData"].size

		self.imageData: Dict = {}
		self.forceDistanceCurves: List[ForceDistanceCurve] = []
		self.channels: Dict[Channel] = {}
		self.average: nt.AverageForceDistanceCurve

		# Set optional data if imported.
		if "imageData" in importedData:
			self._set_image_data(importedData["imageData"])
		if "importedChannelData" in importedData:
			self._set_channel_data(importedData["importedChannelData"])
		# Create a list of force distance curves from the imported data.
		self._create_force_distance_curves(
			importedData["measurementData"].approachCurves
		)
		# Correct the measurement data.
		self._correct_force_distance_curves()
		# Calculate every defined channel.
		self._calculate_channel_data()

	def _set_image_data(self, imageData: nt.ImageData) -> None: 
		"""
		Set the meta data of the image and add the channels
		to the calculated channel.

		Parameters
		----------
		imageData : nt.ImageData
			Contains meta data of the measurement and two 
			additional channels, height and adhesion.
		"""
		# Set the meta data.
		self.imageData = {
			"size": imageData.size,
			"fss": imageData.fss,
			"sss": imageData.sss,
			"xOffset": imageData.xOffset,
			"yOffset": imageData.yOffset,
			"springConstant": imageData.springConstant
		}
		# Add the two additional channels
		self.channels["height"] = Channel(
			name="height",
			size=self.size,
			data=imageData.channelHeight
		)
		self.channels["adhesion"] = Channel(
			name="adhesion",
			size=self.size,
			data=imageData.channelAdhesion
		)

	def _set_channel_data(self, importedChannelData: nt.ImportedChannelData) -> None: 
		"""
		Add the channel to the calculated channels.

		Parameters
		----------
		importedChannelData : nt.ImportedChannelData
			Contains name, size and data of an imported 
			additional channel.
		""" 
		self.channels[importedChannelData.name] = Channel(
			name=importedChannelData.name,
			size=self.size,
			data=importedChannelData.data
		)

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
			self.channels[channelName] = Channel(
				name=channelName,
				size=self.size,
				data=channelData
			)

	def calculate_average(
		self,
		inactiveDataPoints: List[int]
	) -> None:
		"""
		Calculate the average from the currently active 
		force distance curves.
		"""
		activeForceDistanceCurves = self.get_active_force_distance_curves_data(
			inactiveDataPoints
		)

		self.average = calculate_average(
			activeForceDistanceCurves
		)

	def get_force_distance_curves_data(
		self
	) -> List:
		"""
		Get the 

		Returns
		-------
		 : list
		"""
		return [
			forceDistanceCurve.dataApproachCorrected
			for forceDistanceCurve
			in self.forceDistanceCurves
			if forceDistanceCurve.couldBeCorrected
		]

	def get_active_force_distance_curves_data(
		self,
		inactiveDataPoints: List[int]
	) -> List:
		"""
		"""
		return [
			forceDistanceCurve.dataApproachCorrected
			for index, forceDistanceCurve
			in enumerate(self.forceDistanceCurves)
			if (
				forceDistanceCurve.couldBeCorrected and
				index not in inactiveDataPoints
			)
		]

	def get_active_heatmap_data(
		self,
		activeChannel: str,
		inactiveDataPoints: List[int],
		heatmapOrientationMatrix: np.ndarray
	) -> np.ndarray:
		"""
		"""
		return self.channels[activeChannel].get_active_heatmap_data(
			inactiveDataPoints,
			heatmapOrientationMatrix
		)

	def get_histogram_data(
		self,
		activeChannel: str,
	) -> np.ndarray:
		"""
		"""
		return self.channels[activeChannel].get_histogram_data()

	def get_active_histogram_data(
		self,
		activeChannel: str,
		inactiveDataPoints: List[int]
	) -> np.ndarray:
		"""
		"""
		return self.channels[activeChannel].get_active_histogram_data(
			inactiveDataPoints
		)