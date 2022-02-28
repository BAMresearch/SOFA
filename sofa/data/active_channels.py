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
from typing import List, Tuple, NamedTuple, Dict, Union

import numpy as np

def calculate_channels(
	correctedCurveData, 
	m, 
	n, 
	update_progressbar
) -> Dict:
	"""
	"""
	update_progressbar(
		mode="reset",
		value=0,
		label="Calculating channel data"
	)
	progressValue = 100 / len(channels)

	channelData = {}

	for channel, caluclate_channel in channels.items():
		currentChannelData = caluclate_channel(
			correctedCurveData
		)
		channelData[channel] = np.asarray(currentChannelData).reshape((int(m), int(n))).astype(float)

		update_progressbar(
			mode="update",
			value=progressValue
		)

	return channelData

def calculate_topography(correctedCurveData):
	"""

	Parameters:
		curveData(namedtuple): .

	Returns:
		topography(np.ndarray): .
	"""

	return [
		pointOfContact
		for pointOfContact
		in correctedCurveData.valuesPointOfContact
	]

def calculate_force_distance_topography(correctedCurveData):
	""".
	
	Parameters:
		().

	Returns:
		(float).
	"""
	return [
		pointOfContact
		for pointOfContact
		in correctedCurveData.valuesPointOfContact
	]

def calculate_z_piezo_at_maximum_deflection(correctedCurveData):
	""".
	
	Parameters:
		(np.ndarray).

	Returns:
		(float).
	"""
	return [
		correctedCurve[0][-1]
		for correctedCurve
		in correctedCurveData.correctedCurves
	]

def calculate_stiffness(correctedCurveData):
	"""Calculate the stiffness of a curve as the slope of it's linear fit.

	Parameters:
		xData(np.ndarray):
		yData(np.ndarray):

	Returns:
		().
	"""
	stiffness = []

	for correctedCurve in correctedCurveData.correctedCurves:
		a = np.vstack([correctedCurve[0], np.zeros(len(correctedCurve[0]))]).T 

		m, _ = np.linalg.lstsq(a, correctedCurve[1], rcond=None)[0]

		stiffness.append(m)

	return stiffness

def calculate_attractive_area(correctedCurveData):
	""".
	
	Parameters:
		().

	Returns:
		().
	"""
	attractiveArea = []

	for correctedCurve, indexPointOfContact in zip (correctedCurveData.correctedCurves, correctedCurveData.indexePointOfContact):
		indexAttractiveStart, indexAttractiveEnd = locate_attractive_area(
			correctedCurve[1], 
			indexPointOfContact
		)
		attractiveArea.append(
			np.trapz(correctedCurve[1][indexAttractiveStart:indexAttractiveEnd])
		)

	return attractiveArea

def calculate_raw_offset(correctedCurveData):
	""""""
	return [
		rawOffset
		for rawOffset
		in correctedCurveData.valuesRawOffset
	]

def calculate_raw_stiffness(correctedCurveData):
	""""""
	return [
		rawStiffness
		for rawStiffness
		in correctedCurveData.valuesRawStiffness
	]

def calculate_max_deflection(correctedCurveData):
	""".
	
	Parameters:
		(np.ndarray).

	Returns:
		(float).
	"""
	return [
		correctedCurve[1][-1]
		for correctedCurve
		in correctedCurveData.correctedCurves
	]

def calculate_z_attractive(correctedCurveData):
	""".

	Parameters:
		().

	Returns:
		().
	"""
	zAttractive = []

	for curve, indexPointOfContact in zip (correctedCurveData.correctedCurves, correctedCurveData.indexePointOfContact):
		indexAttractiveStart, indexAttractiveEnd = locate_attractive_area(
			curve[1], 
			indexPointOfContact
		)
		zAttractive.append(
			indexAttractiveEnd - indexAttractiveStart
		)

	return zAttractive

def calculate_deflection_attractive(correctedCurveData):
	""".
	
	Parameters:
		().

	Returns:
		().
	"""
	return [
		np.nanmin(correctedCurve[1])
		for correctedCurve
		in correctedCurveData.correctedCurves
	]

def calculate_curves_with_artifacts(correctedCurveData):
	"""Check whether the curve is valid or not.
	
	Parameters:
		yData(np.ndarray): 1 dim data array with the contact part of the curve.

	Returns:
		datapoint(int): 0 if the contact part is not monotonously increasing else 1. 
	"""
	return [
		1 if np.min(np.diff(correctedCurve[1])) < 0
		else 0
		for correctedCurve
		in correctedCurveData.correctedCurves
	]

def locate_attractive_area(yValues, indexPointOfContact):
	"""Locate the start and endpoint of the curves attractive part.

	Parameters:
		yValues(np.ndarray):
		indexPointOfContact(int):

	Returns:
		().
	"""
	# Take a first positiv value before the jtc as startpoint
	flippedIndexAttractiveStart = np.where(np.flip(yValues[:indexPointOfContact]) > 0)[0][0]
	indexAttractiveStart = len(yValues[:indexPointOfContact]) - 1 - flippedIndexAttractiveStart
	indexAttractiveEnd = indexPointOfContact

	return indexAttractiveStart, indexAttractiveEnd

'''
def calculate_custom_channel(correctedCurveData):
	"""
	
	Parameters:

	Returns:
	"""

'''

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
	#"customChannel": calculate_custom_channel,
}