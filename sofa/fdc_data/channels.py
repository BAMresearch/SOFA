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
from typing import List, Tuple, NamedTuple, Dict, Union, Callable

import numpy as np

def calculate_channels(
	correctedCurveData: NamedTuple, 
	m: int, 
	n: int, 
) -> Dict:
	"""Calculate every channel defined in the channels dictionary.

	Parameters:
		correctedCurveData(namedtuple): Data created while correcting the curves.
		m(int): The number of rows.
		n(int): The number of columns.

	Returns:
		channelData(dict): Contains the data of every calculated channel.
	"""

	channelData = {}

	for channelName, caluclate_channel in channels.items():
		currentChannelData = caluclate_channel(
			correctedCurveData
		)
		# Reshape the channel data to a 2 dimensional numpy array.
		channelData[channelName] = np.asarray(currentChannelData).reshape((int(m), int(n))).astype(float)
		
	return channelData

def calculate_topography(correctedCurveData) -> List:
	"""Calculate the topography channel as the y value 
	   of the point of conatact for every corrected curve.

	Parameters:
		correctedCurveData(namedtuple): Data created while correcting the curves.

	Returns:
		channelTopography(list): The calculated topography values.
	"""

	return [
		np.nan if index in correctedCurveData.curvesWithArtifacts
		else pointOfContact
		for index, pointOfContact
		in enumerate(correctedCurveData.valuesPointOfContact)
	]

def calculate_force_distance_topography(correctedCurveData) -> List:
	"""Calculate the force distance topography channel as the y value 
	   of the point of conatact for every corrected curve.
	
	Parameters:
		correctedCurveData(namedtuple): Data created while correcting the curves.

	Returns:
		channelForceDistanceTopography(list): The calculated force distance topography values.
	"""
	return [
		pointOfContact
		for pointOfContact
		in correctedCurveData.valuesPointOfContact
	]

def calculate_z_piezo_at_maximum_deflection(correctedCurveData) -> List:
	"""Calculate the z piezo at maximum deflection channel as 
	   the last x value for every corrected curve.
	
	Parameters:
		correctedCurveData(namedtuple): Data created while correcting the curves.

	Returns:
		channelZPiezoAtMaximumDeflection(list) The calculated z piezo at maximum deflection values.
	"""
	return [
		np.nan if index in correctedCurveData.curvesWithArtifacts
		else correctedCurve[0][-1]
		for index, correctedCurve
		in enumerate(correctedCurveData.correctedCurves)
	]

def calculate_stiffness(correctedCurveData) -> List:
	"""Calculate the stiffness channel as the slope of a linear
	   fit for every corrected curve.

	Parameters:
		correctedCurveData(namedtuple): Data created while correcting the curves.

	Returns:
		channelStiffness(list) The calculated stiffness values.
	"""
	stiffness = []

	for index, correctedCurve in enumerate(correctedCurveData.correctedCurves):
		if index in correctedCurveData.curvesWithArtifacts:
			stiffness.append(np.nan)
		else:
			a = np.vstack([correctedCurve[0], np.zeros(len(correctedCurve[0]))]).T 

			m, _ = np.linalg.lstsq(a, correctedCurve[1], rcond=None)[0]

			stiffness.append(m)

	return stiffness

def calculate_attractive_area(correctedCurveData) -> List:
	"""Calculate the attractive area channel as the value of 
	   the integral over the attractive area for every corrected curve.
	
	Parameters:
		correctedCurveData(namedtuple): Data created while correcting the curves.

	Returns:
		channelAttractiveArea(list): The calculated values for the attractive areas.
	"""
	attractiveArea = []

	for index, (correctedCurve, indexPointOfContact) in enumerate(
		zip(
			correctedCurveData.correctedCurves, 
			correctedCurveData.indexePointOfContact
		)
	):
		if index in correctedCurveData.curvesWithArtifacts:
			attractiveArea.append(np.nan)
		else:
			indexAttractiveStart, indexAttractiveEnd = locate_attractive_area(
				correctedCurve[1], 
				indexPointOfContact
			)
			attractiveArea.append(
				np.trapz(correctedCurve[1][indexAttractiveStart:indexAttractiveEnd])
			)

	return attractiveArea

def calculate_raw_offset(correctedCurveData) -> List:
	"""Calculate the raw offset channel as the intersection value
	   .
	
	Parameters:
		correctedCurveData(namedtuple): Data created while correcting the curves.

	Returns:
		(list): .
	"""
	return [
		np.nan if index in correctedCurveData.curvesWithArtifacts
		else rawOffset
		for index, rawOffset
		in enumerate(correctedCurveData.valuesRawOffset)
	]

def calculate_raw_stiffness(correctedCurveData) -> List:
	""".
	
	Parameters:
		correctedCurveData(namedtuple): Data created while correcting the curves.

	Returns:
		(list): .
	"""
	return [
		np.nan if index in correctedCurveData.curvesWithArtifacts
		else rawStiffness
		for index, rawStiffness
		in enumerate(correctedCurveData.valuesRawStiffness)
	]

def calculate_max_deflection(correctedCurveData) -> List:
	""".
	
	Parameters:
		correctedCurveData(namedtuple): Data created while correcting the curves.

	Returns:
		(list): .
	"""
	return [
		np.nan if index in correctedCurveData.curvesWithArtifacts
		else correctedCurve[1][-1]
		for index, correctedCurve
		in enumerate(correctedCurveData.correctedCurves)
	]

def calculate_z_attractive(correctedCurveData) -> List:
	""".

	Parameters:
		correctedCurveData(namedtuple): Data created while correcting the curves.

	Returns:
		(list): .
	"""
	zAttractive = []

	for index, (curve, indexPointOfContact) in enumerate(
		zip(
			correctedCurveData.correctedCurves, 
			correctedCurveData.indexePointOfContact
		)
	):
		if index in correctedCurveData.curvesWithArtifacts:
			zAttractive.append(np.nan)
		else:
			indexAttractiveStart, indexAttractiveEnd = locate_attractive_area(
				curve[1], 
				indexPointOfContact
			)
			zAttractive.append(
				indexAttractiveEnd - indexAttractiveStart
			)

	return zAttractive

def calculate_deflection_attractive(correctedCurveData) -> List:
	""".
	
	Parameters:
		correctedCurveData(namedtuple): Data created while correcting the curves.

	Returns:
		(list): .
	"""
	return [
		np.nan if index in correctedCurveData.curvesWithArtifacts
		else np.nanmin(correctedCurve[1])
		for index, correctedCurve
		in enumerate(correctedCurveData.correctedCurves)
	]

def calculate_curves_with_artifacts(correctedCurveData) -> List:
	"""Check whether the corrected curves are valid or not. If 
	
	Parameters:
		correctedCurveData(namedtuple): Data created while correcting the curves.

	Returns:
		curvesWithArtifacts(list): 0 if the contact part is not monotonously increasing else 1. 
	"""
	return [
		1 if np.min(np.diff(correctedCurve[1])) < 0
		else 0
		for correctedCurve
		in correctedCurveData.correctedCurves
	]

def locate_attractive_area(yValues, indexPointOfContact) -> Tuple[int, int]:
	"""Locate the start and endpoint of the attractive area of a curve.

	Parameters:
		yValues(np.ndarray): Y Values of the curve.
		indexPointOfContact(int): Index of the point of contact.

	Returns:
		indexAttractiveStart(int): The index where the attractive area beginns.
		indexAttractiveEnd(int): The index where the attractive area ends.
	"""
	# Take a first positiv value before the jtc as startpoint
	flippedIndexAttractiveStart = np.where(np.flip(yValues[:indexPointOfContact]) > 0)[0][0]
	indexAttractiveStart = len(yValues[:indexPointOfContact]) - 1 - flippedIndexAttractiveStart
	indexAttractiveEnd = indexPointOfContact

	return indexAttractiveStart, indexAttractiveEnd

# Template to calculate a custom channel.
'''
def calculate_custom_channel(correctedCurveData):
	""".
	
	Parameters:
		correctedCurveData(namedtuple): .

	Returns:
		customChannelData(list): .
	"""
	pass
'''

# Defines all available channels and how they are calculated.
channels = {
	"topography": calculate_topography,
	"forceDistanceTopography": calculate_force_distance_topography,
	"zPiezoAtMaximumDeflection": calculate_z_piezo_at_maximum_deflection,
	"stiffness": calculate_stiffness,
	"attractiveArea": calculate_attractive_area,
	"rawOffset": calculate_raw_offset,
	"rawStiffness": calculate_raw_stiffness,
	"maxDeflection": calculate_max_deflection,		
	"zAttractive": calculate_z_attractive,
	"deflectionAttractive": calculate_deflection_attractive,
	"curvesWithArtifacts": calculate_curves_with_artifacts,
	#"customChannelName": calculate_custom_channel,
}