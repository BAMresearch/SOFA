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
from typing import List, Tuple, NamedTuple, Dict, Union, Callable

from matplotlib.lines import Line2D
import numpy as np
from scipy import stats
from scipy.ndimage import gaussian_filter1d

def correct_approach_curves(
	approachCurves: List,
	update_progressbar: Callable
) -> NamedTuple:
	"""Correct the approach curves by shifting the point of contact to the origin.

	Parameters:
		approachCurves(list): List of np.arrays with the x values.
		update_progressbar(function): Function to show the correction progress.

	Returns:
		correctedCurveData(NamedTuple): All the important data that is created while correcting the curves.
	"""
	update_progressbar(
		mode="reset",
		value=0,
		label="Correcting wave data"
	)
	progressValue = 100 / len(approachCurves)

	CorrectedCurveData = namedtuple(
		"CorrectedCurveData",
		[
			"correctedCurves",
			"indexeEndOfZeroline",
			"valuesRawOffset",
			"valuesRawStiffness",
			"indexePointOfContact",
			"valuesPointOfContact",
			"curvesWithArtifacts"
		]
	)

	correctedCurves = []
	indexeEndOfZeroline = []
	valuesRawOffset = []
	valuesRawStiffness = []
	indexePointOfContact = []
	valuesPointOfContact = []
	curvesWithArtifacts = []

	for index, currentCurve in enumerate(approachCurves):
		# Try to shift the curve along the y axis to 0.
		try:
			correctedYValues, indexEndOfZeroline, rawStiffness, rawOffset = shift_y_axis(
				currentCurve[0], currentCurve[1]
			)
		except ValueError:
			correctedCurves.append(
				[currentCurve[0], currentCurve[1]]
			)
			indexeEndOfZeroline.append(np.nan)
			valuesRawOffset.append(np.nan)
			valuesRawStiffness.append(np.nan)
			indexePointOfContact.append(np.nan)
			valuesPointOfContact.append(np.nan)
			curvesWithArtifacts.append(index)

			update_progressbar(
				mode="update",
				value=progressValue
			)

			continue

		# Shift the curve along the x axis to 0.
		correctedXValues, pointOfContact, indexPointOfContact = shift_x_axis(
			currentCurve[0], correctedYValues, indexEndOfZeroline
		)

		correctedCurves.append(
			[correctedXValues, correctedYValues]
		)
		indexeEndOfZeroline.append(indexEndOfZeroline)
		valuesRawOffset.append(rawOffset)
		valuesRawStiffness.append(rawStiffness)
		indexePointOfContact.append(indexPointOfContact)
		valuesPointOfContact.append(pointOfContact)

		update_progressbar(
			mode="update",
			value=progressValue
		)

	return CorrectedCurveData(
		correctedCurves=correctedCurves,
		indexeEndOfZeroline=indexeEndOfZeroline,
		valuesRawOffset=valuesRawOffset,
		valuesRawStiffness=valuesRawStiffness,
		indexePointOfContact=indexePointOfContact, 
		valuesPointOfContact=valuesPointOfContact,
		curvesWithArtifacts=curvesWithArtifacts
	)

def shift_y_axis(
	xValueApproach: np.ndarray, 
	yValueApproach: np.ndarray
) -> Tuple[np.ndarray, int]:
	"""Shift the end of the zero line along the y axis to zero.

	Parameters:
		xValueApproach(np.ndarray): X values of the current curve.
		yValueApproach(np.ndarray): Y values of the current curve.

	Returns:
		shiftedYValueApproach(np.ndarray): .
		endOfZeroLine(int): Position of the endOfZeroLine.
		rawOffset(float): .
		rawStiffness(float): . 

	Raises:
		(ValueError): .
	"""
	coefficients = np.polyfit(xValueApproach, yValueApproach, 1)
	fittedCurveFunction = np.poly1d(coefficients)

	startPoint = np.where(yValueApproach < fittedCurveFunction(xValueApproach))[0][0] 
	endPoint = np.where(yValueApproach < fittedCurveFunction(xValueApproach))[0][-1]

	difference = np.absolute(fittedCurveFunction(xValueApproach) - yValueApproach)
	differenceMaxIndex = np.where(difference[startPoint:endPoint] == np.max(difference[startPoint:endPoint]))[0][0] + startPoint
	newEndPoint = int(differenceMaxIndex + ((endPoint - differenceMaxIndex) * 0.05))
	
	try:
		endOfZeroline = calculate_end_of_zeroline(
			xValueApproach, yValueApproach, startPoint, newEndPoint
		)
	except ValueError:
		raise ValueError

	regressionData = stats.linregress(
		xValueApproach[0:endOfZeroline], 
		yValueApproach[0:endOfZeroline])
	
	fittedLine = (
		regressionData.slope 
		* xValueApproach[0:endOfZeroline] 
		+ regressionData.intercept
	)

	correctedYValues = np.concatenate(
		[
			yValueApproach[0:endOfZeroline] - fittedLine,
			yValueApproach[endOfZeroline:] - fittedLine[-1]
		]
	)

	return correctedYValues, endOfZeroline, coefficients[0], coefficients[1]

def calculate_end_of_zeroline(
	xValues: np.ndarray, 
	yValues: np.ndarray, 
	leftBorder: int, 
	rightBorder: int
) -> int:
	"""Calculate the end of the zero line as the last point with positive slope before the jump to contact.

	Parameters:
		xValues(np.ndarray): X values of the curve.
		yValues(np.ndarray): Y values of the curve.
		leftBorder(int): Left limit to search within.
		rightBorder(int): Right limit to search within.

	Returns:
		endOfZeroline(int): The index of the end of the zeroline.

	Raises:
		(ValueError): .
	"""
	smoothedDerivation = gaussian_filter1d(
		(np.diff(yValues) / np.diff(xValues)), 
		sigma=10
	)
	
	try:
		endOfZeroline = np.where(smoothedDerivation[leftBorder:rightBorder] < 0)[0][-1]
	except IndexError:
		raise ValueError

	return endOfZeroline + leftBorder

def shift_x_axis(
	xValueApproach, 
	yValueApproach, 
	endOfZeroline
):
	"""Shift the point of contact along the x axis to zero.

	Parameters:
		xValueApproach(np.ndarray): X values of the current curve.
		yValueApproach(np.ndarray): Y values of the current curve.

	Returns:
		().
	"""
	try:
		zeroCrossing = np.where(yValueApproach[endOfZeroline:] <= 0)[0][-1] + endOfZeroline
	except IndexError:
		zeroCrossing = endOfZeroline
		
	pointOfContact = np.interp(
		0, 
		yValueApproach[zeroCrossing-2:zeroCrossing+2], 
		xValueApproach[zeroCrossing-2:zeroCrossing+2]
	)

	return xValueApproach - pointOfContact, pointOfContact, zeroCrossing

def combine_data(
	importedData, 
	correctedCurveData, 
	channelData,
	update_progressbar
):
	"""
	"""
	processedGeneralData, additionalChannelData = prepare_general_data(importedData)

	if additionalChannelData:
		merge_dictionaries(channelData, additionalChannelData)

	displayedLines = prepare_line_plot(correctedCurveData.correctedCurves, update_progressbar)
	processedCurveData = {
		"displayedLines": displayedLines,
		"correctedCurves": correctedCurveData.correctedCurves
	}

	processedChannelData = prepare_channel_data(
		channelData
	)

	return {
		"generalData": processedGeneralData,
		"curveData": processedCurveData, 
		"channelData": processedChannelData
	}

def prepare_general_data(
	importedData
):
	"""
	"""
	generalData = {
		"filename": importedData["curveData"].filename,
		"m": importedData["curveData"].m,
		"n": importedData["curveData"].n
	}
	additionalChannelData = {}

	if "imageData" in generalData:
		additionalChannelData["height"] = importedData["imageData"].height
		additionalChannelData["adhesion"] = importedData["imageData"].adhesion

		generalData = importedData["imageData"]._asdict()
		del generalData["height"]
		del generalData["adhesion"]

	if "channelData" in generalData:
		pass

	return generalData, additionalChannelData

def prepare_line_plot(
	correctedCurves,
	update_progressbar
):
	"""

	Parameters:
		.
	"""
	update_progressbar(
		mode="reset",
		value=0,
		label="Processing wave data"
	)
	progressValue = 100 / len(correctedCurves)

	displayedLines = []

	for index, curve in enumerate(correctedCurves):
		displayedLines.append(
			create_line(curve, index)
		)
		update_progressbar(
			mode="update",
			value=progressValue
		)
	return displayedLines

def create_line(curve, index):
	""""""
	return Line2D(
		curve[0], curve[1], c="red", label=str(index),
		linewidth=0.5, picker=True, pickradius=1.0, zorder=5
	)

def prepare_channel_data(
	channelData
):
	""""""
	processedChannelData = {}

	for channelName, channelData in channelData.items():
		processedChannelData[channelName] = {
			"data": channelData.copy(),
			"sourceData": channelData.copy()
		}

	return processedChannelData

def merge_dictionaries(mainDict, additionalDict):
	""""""
	for key, value in additionalDict.items():
		mainDict[key] = value