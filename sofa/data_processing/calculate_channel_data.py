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
import functools

import numpy as np
from scipy.stats import linregress

import data_processing.named_tuples as nt

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

def calculate_channel_data(
	forceDistanceCurves: List[nt.ForceDistanceCurve], 
	size: Tuple[int]
) -> Dict:
	"""
	Calculate every channel defined in the active_channels dictionary.
	
	Parameters
	----------
	forceDistanceCurves : list[nt.ForceDistanceCurve] 
		Every force distance curve of the force volume.
	size : tuple[int] 
		Size of the force volume.
	
	Returns
	-------
	channelData : dict
		Contains the names and associated data of every definied 
		channel.
	"""
	channelData = {}

	for channelName, caluclate_channel in active_channels.items():
		channelData[channelName] = caluclate_channel(
			forceDistanceCurves,
			size
		)

	return channelData

@decorator_reshape_channel_data
def calculate_topography(
	forceDistanceCurves: List[nt.ForceDistanceCurve], 
	size: Tuple[int]
) -> List:
	"""
	

	Parameters
	----------
	forceDistanceCurves : list[nt.ForceDistanceCurve] 
		Every force distance curve of the force volume.
	size : tuple[int] 
		Size of the force volume.

	Returns
	-------
	topographyChannelData : list
		
	"""
	return [
		np.nan if not forceDistanceCurve.couldBeCorrected
		else forceDistanceCurve.channelMetadata.pointOfContact.piezo
		for forceDistanceCurve
		in forceDistanceCurves
	] 

@decorator_reshape_channel_data
def calculate_piezo_at_maximum_deflection(
	forceDistanceCurves: List[nt.ForceDistanceCurve],
	size: Tuple[int]
) -> List:
	"""
	

	Parameters
	----------
	forceDistanceCurves : list[nt.ForceDistanceCurve] 
		Every force distance curve of the force volume.
	size : tuple[int] 
		Size of the force volume.

	Returns
	-------
	 : list
	"""
	return [
		np.nan if not forceDistanceCurve.couldBeCorrected
		else forceDistanceCurve.dataApproachCorrected.piezo[-1]
		for forceDistanceCurve
		in forceDistanceCurves
	]

@decorator_reshape_channel_data
def calculate_stiffness(
	forceDistanceCurves: List[nt.ForceDistanceCurve],
	size: Tuple[int]
) -> List:
	"""
	

	Parameters
	----------
	forceDistanceCurves : list[nt.ForceDistanceCurve] 
		Every force distance curve of the force volume.
	size : tuple[int] 
		Size of the force volume.

	Returns
	-------
	 : list
	"""
	return [
		np.nan if not forceDistanceCurve.couldBeCorrected
		else calculate_slope_linear_fit_to_corrected_approach_curve(
			forceDistanceCurve.dataApproachCorrected
		)
		for forceDistanceCurve
		in forceDistanceCurves
	]

def calculate_slope_linear_fit_to_corrected_approach_curve(
	correctedForceDistanceCurve: nt.ForceDistanceCurve
) -> float:
	"""
	

	Parameters
	----------
	correctedForceDistanceCurve : nt.ForceDistanceCurve
		

	Returns
	-------
	slope : float
	"""
	slope, _, _, _, _ = linregress(
		correctedForceDistanceCurve.piezo,
		correctedForceDistanceCurve.deflection
	)

	return slope

@decorator_reshape_channel_data
def calculate_attractive_area(
	forceDistanceCurves: List[nt.ForceDistanceCurve],
	size: Tuple[int]
) -> List:
	"""
	

	Parameters
	----------
	forceDistanceCurves : list[nt.ForceDistanceCurve] 
		Every force distance curve of the force volume.
	size : tuple[int] 
		Size of the force volume.

	Returns
	-------
	 : list
	"""
	return [
		np.nan if not forceDistanceCurve.couldBeCorrected
		else calculate_surface_area_attractive_area(
			forceDistanceCurve.dataApproachCorrected.deflection,
			forceDistanceCurve.channelMetadata.endOfZeroline,
			forceDistanceCurve.channelMetadata.pointOfContact
		)
		for forceDistanceCurve
		in forceDistanceCurves
	]

def calculate_surface_area_attractive_area(
	deflection: np.ndarray,
	endOfZeroline: nt.ForceDistancePoint,
	pointOfContact: nt.ForceDistancePoint
) -> float:
	"""
	"""
	return np.trapz(
		deflection[endOfZeroline.index:pointOfContact.index]
	)

@decorator_reshape_channel_data
def calculate_raw_offset(
	forceDistanceCurves: List[nt.ForceDistanceCurve],
	size: Tuple[int]
) -> List:
	"""
	

	Parameters
	----------
	forceDistanceCurves : list[nt.ForceDistanceCurve] 
		Every force distance curve of the force volume.
	size : tuple[int] 
		Size of the force volume.

	Returns
	-------
	 : list
	"""
	return [
		np.nan if not forceDistanceCurve.couldBeCorrected
		else forceDistanceCurve.channelMetadata.coefficientsFitApproachCurve.intercept
		for forceDistanceCurve
		in forceDistanceCurves
	]

@decorator_reshape_channel_data
def calculate_raw_stiffness(
	forceDistanceCurves: List[nt.ForceDistanceCurve],
	size: Tuple[int]
) -> List:
	"""
	

	Parameters
	----------
	forceDistanceCurves : list[nt.ForceDistanceCurve] 
		Every force distance curve of the force volume.
	size : tuple[int] 
		Size of the force volume.

	Returns
	-------
	 : list
	"""
	return [
		np.nan if not forceDistanceCurve.couldBeCorrected
		else forceDistanceCurve.channelMetadata.coefficientsFitApproachCurve.slope
		for forceDistanceCurve
		in forceDistanceCurves
	]

@decorator_reshape_channel_data
def calculate_max_deflection(
	forceDistanceCurves: List[nt.ForceDistanceCurve],
	size: Tuple[int]
) -> List:
	"""
	

	Parameters
	----------
	forceDistanceCurves : list[nt.ForceDistanceCurve] 
		Every force distance curve of the force volume.
	size : tuple[int] 
		Size of the force volume.

	Returns
	-------
	 : list
	"""
	return [
		np.nan if not forceDistanceCurve.couldBeCorrected
		else forceDistanceCurve.dataApproachCorrected.deflection[-1]
		for forceDistanceCurve
		in forceDistanceCurves
	]

@decorator_reshape_channel_data
def calculate_z_attractive(
	forceDistanceCurves: List[nt.ForceDistanceCurve],
	size: Tuple[int]
) -> List:
	"""
	

	Parameters
	----------
	forceDistanceCurves : list[nt.ForceDistanceCurve] 
		Every force distance curve of the force volume.
	size : tuple[int] 
		Size of the force volume.

	Returns
	-------
	 : list
	"""
	return [
		np.nan if not forceDistanceCurve.couldBeCorrected
		else calculate_attractive_area_length(
			forceDistanceCurve.channelMetadata.endOfZeroline,
			forceDistanceCurve.channelMetadata.pointOfContact
		)
		for forceDistanceCurve
		in forceDistanceCurves
	]

def calculate_attractive_area_length(
	endOfZeroline: nt.ForceDistancePoint,
	pointOfContact: nt.ForceDistancePoint
) -> float:
	"""
	"""
	return pointOfContact.index - endOfZeroline.index

@decorator_reshape_channel_data
def calculate_deflection_attractive(
	forceDistanceCurves: List[nt.ForceDistanceCurve],
	size: Tuple[int]
) -> List:
	"""
	

	Parameters
	----------
	forceDistanceCurves : list[nt.ForceDistanceCurve] 
		Every force distance curve of the force volume.
	size : tuple[int] 
		Size of the force volume.

	Returns
	-------
	 : list
	"""
	return [
		np.nan if not forceDistanceCurve.couldBeCorrected
		else np.min(forceDistanceCurve.dataApproachCorrected.deflection)
		for forceDistanceCurve
		in forceDistanceCurves
	]

@decorator_reshape_channel_data
def calculate_curves_with_artifacts(
	forceDistanceCurves: List[nt.ForceDistanceCurve],
	size: Tuple[int]
) -> List:
	"""
	

	Parameters
	----------
	forceDistanceCurves : list[nt.ForceDistanceCurve] 
		Every force distance curve of the force volume.
	size : tuple[int] 
		Size of the force volume.

	Returns
	-------
	 : list
	"""
	return [
		1 if forceDistanceCurve.couldBeCorrected and check_for_decreasing_contact_values(
			forceDistanceCurve.dataApproachCorrected.deflection,
			forceDistanceCurve.channelMetadata.pointOfContact
		)
		else 0
		for forceDistanceCurve
		in forceDistanceCurves
	]

def check_for_decreasing_contact_values(
	deflection: np.ndarray,
	pointOfContact: nt.ForceDistancePoint
) -> bool:
	"""
	"""
	return np.min(
		np.diff(deflection[pointOfContact.index:])
	) < 0

# Defines all available channels.
active_channels = {
	"topography": calculate_topography,
	"piezoAtMaximumDeflection": calculate_piezo_at_maximum_deflection,
	"stiffness": calculate_stiffness,
	"attractiveArea": calculate_attractive_area,
	"rawOffset": calculate_raw_offset,
	"rawStiffness": calculate_raw_stiffness,
	"maxDeflection": calculate_max_deflection,		
	"zAttractive": calculate_z_attractive,
	"deflectionAttractive": calculate_deflection_attractive,
	"curvesWithArtifacts": calculate_curves_with_artifacts,
}