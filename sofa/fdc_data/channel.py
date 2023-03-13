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
from abc import ABC, abstractmethod
import functools

import numpy as np
from scipy.stats import linregress

def decorator_reshape_channel_data(function):
	"""
	Reshape the data of a channel to a 2 dimensional array.
	"""
	@functools.wraps(function)
	def wrapper_reshape_channel_data(*args, **kwargs):
		measurementSize = args[1]
		channelData = function(*args, **kwargs)
		
		return np.asarray(channelData).reshape(measurementSize)

	return wrapper_reshape_channel_data

class Channel(ABC):
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
		name: str,
		forceDistanceCurves: List,
		size: Tuple[int]
	):
		"""
		"""
		self.name: str = name
		self.rawData: np.ndarray = _calculate_channel_data(
			forceDistanceCurves,
			size
		)

	@abstractmethod
	@staticmethod
	def _calculate_channel_data(
		forceDistanceCurves: List, 
		size: Tuple[int]
	) -> np.ndarray:
		"""
		"""
		pass

	def get_active_data(
		inactiveForceDistanceCurves: List[int]
	) -> None:
		""""""
		pass

class Topography(Channel):
	"""
	"""
	@staticmethod
	@decorator_reshape_channel_data
	def _calculate_channel_data(
		forceDistanceCurves, 
		size
	) -> np.ndarray:
		"""
		"""
		return [
			np.nan if not forceDistanceCurve.couldBeCorrected
			else forceDistanceCurve.channelMetadata.pointOfContact.piezo
			for forceDistanceCurve
			in forceDistanceCurves
		]

class PiezoAtMaximumDeflection(Channel):
	"""
	"""
	@staticmethod
	@decorator_reshape_channel_data
	def _calculate_channel_data(forceDistanceCurves, size) -> np.ndarray:
		"""
		"""
		return [
			np.nan if not forceDistanceCurve.couldBeCorrected
			else forceDistanceCurve.dataApproachCorrected.piezo[-1]
			for forceDistanceCurve
			in forceDistanceCurves
		]

class Stiffness(Channel):
	"""
	"""
	@staticmethod
	@decorator_reshape_channel_data
	def _calculate_channel_data(forceDistanceCurves, size) -> np.ndarray:
		"""
		"""
		return [
			np.nan if not forceDistanceCurve.couldBeCorrected
			else _calculate_slope_linear_fit_to_corrected_approach_curve(
				forceDistanceCurve.dataApproachCorrected
			)
			for forceDistanceCurve
			in forceDistanceCurves
		]

	@staticmethod
	def _calculate_slope_linear_fit_to_corrected_approach_curve(
		correctedForceDistanceCurve: nt.ForceDistanceCurve
	) -> float:
		"""
		"""
		slope, _, _, _, _ = linregress(
			correctedForceDistanceCurve.piezo,
			correctedForceDistanceCurve.deflection
		)

		return slope

class AttractiveArea(Channel):
	"""
	"""
	@staticmethod
	@decorator_reshape_channel_data
	def _calculate_channel_data(forceDistanceCurves, size) -> np.ndarray:
		"""
		"""
		return [
			np.nan if not forceDistanceCurve.couldBeCorrected
			else _calculate_attractive_area(
				forceDistanceCurve.dataApproachCorrected.deflection,
				forceDistanceCurve.channelMetadata.endOfZeroline,
				forceDistanceCurve.channelMetadata.pointOfContact
			)
			for forceDistanceCurve
			in forceDistanceCurves
		]

	@staticmethod
	def _calculate_attractive_area(
		deflection: np.ndarray,
		endOfZeroline: nt.ForceDistancePoint,
		pointOfContact: nt.ForceDistancePoint
	) -> float:
		"""
		"""
		return np.trapz(
			deflection[endOfZeroline.index:pointOfContact.index]
		)

class AttractiveAreaLength(Channel):
	"""
	"""
	@staticmethod
	@decorator_reshape_channel_data
	def _calculate_channel_data(forceDistanceCurves, size) -> np.ndarray:
		"""
		"""
		return [
			np.nan if not forceDistanceCurve.couldBeCorrected
			else _calculate_attractive_area_length(
				forceDistanceCurve.channelMetadata.endOfZeroline,
				forceDistanceCurve.channelMetadata.pointOfContact
			)
			for forceDistanceCurve
			in forceDistanceCurves
		]

	@staticmethod
	def _calculate_attractive_area_length(
		endOfZeroline: nt.ForceDistancePoint,
		pointOfContact: nt.ForceDistancePoint
	) -> float:
		"""
		"""
		return pointOfContact.index - endOfZeroline.index

class RawSlope(Channel):
	"""
	"""
	@staticmethod
	@decorator_reshape_channel_data
	def _calculate_channel_data(forceDistanceCurves, size) -> np.ndarray:
		"""
		"""
		return [
			np.nan if not forceDistanceCurve.couldBeCorrected
			else forceDistanceCurve.channelMetadata.coefficientsFitApproachCurve.slope
			for forceDistanceCurve
			in forceDistanceCurves
		]

class RawOffset(Channel):
	"""
	"""
	@staticmethod
	@decorator_reshape_channel_data
	def _calculate_channel_data(forceDistanceCurves, size) -> np.ndarray:
		"""
		"""
		return [
			np.nan if not forceDistanceCurve.couldBeCorrected
			else forceDistanceCurve.channelMetadata.coefficientsFitApproachCurve.intercept
			for forceDistanceCurve
			in forceDistanceCurves
		]

class MaximumDeflection(Channel):
	"""
	"""
	@staticmethod
	@decorator_reshape_channel_data
	def _calculate_channel_data(forceDistanceCurves, size) -> np.ndarray:
		"""
		"""
		return [
			np.nan if not forceDistanceCurve.couldBeCorrected
			else forceDistanceCurve.dataApproachCorrected.deflection[-1]
			for forceDistanceCurve
			in forceDistanceCurves
		]

class MinimumDeflection(Channel):
	"""
	"""
	@staticmethod
	@decorator_reshape_channel_data
	def _calculate_channel_data(forceDistanceCurves, size) -> np.ndarray:
		"""
		"""
		return [
			np.nan if not forceDistanceCurve.couldBeCorrected
			else np.min(forceDistanceCurve.dataApproachCorrected.deflection)
			for forceDistanceCurve
			in forceDistanceCurves
		]

class Artifact(Channel):
	"""
	"""
	@staticmethod
	@decorator_reshape_channel_data
	def _calculate_channel_data(forceDistanceCurves, size) -> np.ndarray:
		"""
		"""
		return [
			1 if _check_for_decreasing_contact_values(
				forceDistanceCurve.dataApproachCorrected.deflection,
				forceDistanceCurve.channelMetadata.pointOfContact
			)
			else 0
			for forceDistanceCurve
			in forceDistanceCurves
		]

	@staticmethod
	def _check_for_decreasing_contact_values(
		deflection: np.ndarray,
		pointOfContact: nt.ForceDistancePoint
	) -> bool:
		"""
		"""
		return np.min(
			np.diff(deflection[pointOfContact.index:])
		) < 0