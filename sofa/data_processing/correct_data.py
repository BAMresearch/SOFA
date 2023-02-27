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
from typing import Tuple

import numpy as np
from scipy.stats import linregress
from scipy.ndimage import gaussian_filter1d

import exceptions.custom_exceptions as ce
import named_tuples.named_tuples_correct_data as nt_cd

def correct_approach_curve(
	approachCurve: nt.ForceDistanceCurve,
) -> Tuple[nt.ForceDistanceCurve, nt.ChannelMetadata]:
	"""
	Correct an approach curve by shifting it's point of contact to the origin.

	Parameters
	----------
	approachCurves : nt.ForceDistanceCurve
		Raw approach curve with piezo (x) and deflection (y) values.

	Returns
	-------
	correctedCurveData : nt.ForceDistanceCurve 
		Corrected approach curve with shifted piezo (x) and deflection (y) values.
	channelMetadata : nt.ChannelMetadata
		Metadata generated during the correction of the curve, which is used for 
		calculating the different channels.
	"""
	correctedDeflectionValues, endOfZeroline, coefficientsFitApproachCurve = correct_deflection_values(
		approachCurve
	)
	correctedPiezoValues, pointOfContact = correct_piezo_values(
		approachCurve, 
		correctedDeflectionValues,
		endOfZeroline
	)

	correctedDataApproach = nt.ForceDistanceCurve(
		piezo=correctedPiezoValues,
		deflection=correctedDeflectionValues
	)
	channelMetadata = nt.ChannelMetadata(
		endOfZeroline=endOfZeroline,
		pointOfContact=pointOfContact,
		coefficientsFitApproachCurve=coefficientsFitApproachCurve
	)

	return correctedDataApproach, channelMetadata

def correct_deflection_values(
	approachCurve: nt.ForceDistanceCurve,
) -> Tuple[np.ndarray, nt.ForceDistancePoint, nt.coefficientsFitApproachCurve]:
	"""
	Correct the deflection values of an approach curve by removing the 
	virtual deflection.

	Parameters
	----------
	approachCurves : nt.ForceDistanceCurve
		Raw approach curve with piezo (x) and deflection (y) values.
	
	Returns
	-------
	correctedDeflectionValues : np.ndarray
		Deflection values shifted to zero along the zero line.
	endOfZeroline : nt.ForceDistancePoint
		Index, piezo and deflection value from the last point 
		of the zero line.
	coefficientsFitApproachCurve : nt.coefficientsFitApproachCurve
		Slope and intercept value of a lineare fit to the raw data.
	"""
	endOfZeroline, coefficientsFitApproachCurve = calculate_end_of_zeroline(
		approachCurve
	)
	fitEndOfZeroline = calculate_linear_fit_to_zeroline(
		approachCurve,
		endOfZeroline
	)
	correctedDeflectionValues = shif_deflection_values(
		approachCurve,
		endOfZeroline,
		fitEndOfZeroline
	)

	return correctedDeflectionValues, endOfZeroline, coefficientsFitApproachCurve

def calculate_end_of_zeroline(
	approachCurve: nt.ForceDistanceCurve,
) -> nt.ForceDistancePoint: 
	"""
	Calculate the end of the zero line as the last measurement point
	with a positive slope before the jump to contact.

	Parameters
	----------
	approachCurve : nt.ForceDistanceCurve
		Raw approach curve with piezo (x) and deflection (y) values.

	Returns
	-------
	endOfZeroline : nt.ForceDistancePoint
		Index, piezo and deflection value from the last point 
		of the zero line.
	coefficientsFitApproachCurve : nt.coefficientsFitApproachCurve
		Slope and intercept value of a lineare fit to the raw data.
		
	"""
	fitApproachCurve, coefficientsFitApproachCurve = calculate_linear_fit_to_approach_curve(
		approachCurve
	)
	smoothedDerivationDeflection = calculate_smoothed_derivation(
		approachCurve
	)
	indexLeftBorder, indexRightBorder = calculate_deflection_borders(
		approachCurve,
		fitApproachCurve
	)
	endOfZeroline = locate_end_of_zeroline(
		approachCurve,
		smoothedDerivationDeflection,
		indexLeftBorder,
		indexRightBorder
	)

	return endOfZeroline, coefficientsFitApproachCurve

def calculate_linear_fit_to_approach_curve(
	approachCurve: nt.ForceDistanceCurve
) -> Tuple[nt.ForceDistanceCurve, nt.coefficientsFitApproachCurve]:
	"""
	Calculate linear regression curve to a raw approach curve.

	Parameters
	----------
	approachCurves : nt.ForceDistanceCurve
		Raw approach curve with piezo (x) and deflection (y) values.

	Returns
	-------
	fitApproachCurve : nt.ForceDistanceCurve
		Linear regression curve with the same piezo (x) values and
		new calculated deflection (y) values.
	coefficientsFitApproachCurve : nt.coefficientsFitApproachCurve
		Slope (raw stiffness) and intercept (raw offset) of the fitted
		line.
	"""
	slope, intercept, _, _, _ = linregress(
		approachCurve.piezo,
		approachCurve.deflection
	)
	linearDeflectionValues = np.array(
		[intercept + slope*approachCurve.piezo]
	)

	fitApproachCurve = nt.ForceDistanceCurve(
		piezo=approachCurve.piezo,
		deflection=linearDeflectionValues
	)
	coefficientsFitApproachCurve = nt.coefficientsFitApproachCurve(
		slope=slope,
		intercept=intercept
	)

	return fitApproachCurve, coefficientsFitApproachCurve

def calculate_smoothed_derivation(
	approachCurve: nt.ForceDistanceCurve,
) -> np.ndarray:
	"""
	Calculate the first derivation of the raw measurement curve and 
	smooth it.

	Parameters
	----------
	approachCurves : namedTuple
		Raw approach curve with piezo (x) and deflection (y) values.

	Returns
	-------
	smoothedDerivationDeflection : np.ndarray
		Smoothed first derivation of the deflection (y) values.
	"""
	derivationDeflection = derivate_curve(approachCurve)
	smoothedDerivationDeflection = smooth_derivation(derivationDeflection)

	return smoothedDerivationDeflection

def derivate_curve(
	approachCurve: nt.ForceDistanceCurve,
) -> np.ndarray:
	"""
	Calculate the first derivation of the deflection (y) values
	of the approach curve.
	
	Parameters
	----------
	approachCurves : namedTuple
		Raw approach curve with piezo (x) and deflection (y) values.

	Returns
	-------
	derivationDeflection : np.ndarray
		First derivate of the deflection (y) values.
	"""
	return (
		np.diff(approachCurve.deflection) / np.diff(approachCurve.piezo)
	)

def smooth_derivation(
	derivationDeflection: np.ndarray,
	smoothFactor: int = 10
) -> np.ndarray:
	"""
	Smooth the first derivation of the deflection (y) values
	of the approach curve.
	
	Parameters
	----------
	derivationDeflection : np.ndarray
		First derivate of the deflection (y) values.
	smoothFactor : int


	Returns
	-------
	smoothedDerivationDeflection : np.ndarray
		Smoothed first derivation of the deflection (y) values.
	"""
	return gaussian_filter1d(
		derivationApproachCurve,
		sigma=smoothFactor
	)

def calculate_deflection_borders(
	approachCurve: nt.ForceDistanceCurve,
	fitApproachCurve: nt.ForceDistanceCurve
) -> Tuple[int, int, nt.coefficientsFitApproachCurve]:
	"""
	
	
	Parameters
	----------
	approachCurves : namedTuple
		Raw approach curve with piezo (x) and deflection (y) values.
	fitApproachCurve : nt.ForceDistanceCurve
		Linear curve fit to the approach curve with the same 
		piezo (x) values and adjusted deflection (y) values.

	Returns
	-------
	indexLeftBorder : int
		Index of the first intersection point between the approach curve
		and it's linear fit.
	indexRightBorder: int
		.
	"""
	indexFirstIntersection, indexLastIntersection = calculate_curve_intersections(
		approachCurve, 
		fitApproachCurve
	)
	indexRightBorder = adjust_intersection_border(
		approachCurve, 
		fitApproachCurve,
		indexFirstIntersection,
		indexLastIntersection
	)

	return indexFirstIntersection, indexRightBorder

def calculate_curve_intersections(
	approachCurve: nt.ForceDistanceCurve,
	fitApproachCurve: nt.ForceDistanceCurve
) -> Tuple[int]:
	"""
	Calculate intersections of the approach curve and it's linear 
	fit.

	Parameters
	----------
	approachCurves : namedTuple
		Raw approach curve with piezo (x) and deflection (y) values.
	fitApproachCurve : nt.ForceDistanceCurve
		Linear curve fit to the approach curve with the same 
		piezo (x) values and adjusted deflection (y) values.
		
	Returns
	-------
	indexFirstIntersection : int 
		Index of the first intersection point.
	indexLastIntersection : int
		Index of the last intersection point.
	"""
	innerIntersection = np.where(
		approachCurve.deflection < fitApproachCurve.deflection
	)[0]

	indexFirstIntersection = innerIntersection[0]
	indexLastIntersection = innerIntersection[-1]
	
	return indexFirstIntersection, indexLastIntersection

def adjust_intersection_border(
	approachCurve: nt.ForceDistanceCurve,
	fitApproachCurve: nt.ForceDistanceCurve,
	indexFirstIntersection: int,
	indexLastIntersection: int
) -> int:
	"""
	

	Parameters
	----------
	approachCurves : namedTuple
		Raw approach curve with piezo (x) and deflection (y) values.
	fitApproachCurve : nt.ForceDistanceCurve
	
	indexFirstIntersection : int

	indexLastIntersection : int


	Returns
	-------
	adjustedIndexMaxDeflectionDifference : int

	"""
	deflectionDifferences = np.absolute(
		fitApproachCurve.deflection - approachCurve.deflection
	)

	indexMaxDeflectionDifference = np.argmax(
		deflectionDifferences[indexFirstIntersection:indexLastIntersection]
	) + indexFirstIntersection
	adjustedIndexMaxDeflectionDifference = int(
		indexMaxDeflectionDifference 
		+ ((indexLastIntersection - indexMaxDeflectionDifference) * 0.05)
	)

	return adjustedIndexMaxDeflectionDifference

def locate_end_of_zeroline(
	approachCurve: nt.ForceDistanceCurve,
	smoothedDerivationDeflection: np.ndarray,
	indexLeftBorder: int, 
	indexRightBorder: int
) -> nt.ForceDistancePoint:
	"""

	Parameters
	----------
	approachCurves : namedTuple
		Raw approach curve with piezo (x) and deflection (y) values.

	Returns
	-------

	Raises
	------
	"""
	endOfZeroline = np.where(
		smoothedDerivationDeflection[indexLeftBorder:indexRightBorder] < 0
	)

	try:
		indexEndOfZeroline = endOfZeroline[-1] + indexLeftBorder
	except IndexError as e:
		raise ce. from e
	else:
		return nt.ForceDistancePoint(
			index=indexEndOfZeroline,
			piezo=approachCurve.piezo[indexEndOfZeroline],
			deflection=approachCurve.deflection[indexEndOfZeroline]
		)

def calculate_linear_fit_to_zeroline(
	approachCurve: nt.ForceDistanceCurve,
	endOfZeroline: nt.ForceDistancePoint
) -> nt.ForceDistanceCurve:
	"""

	Parameters
	----------
	approachCurves : namedTuple
		Raw approach curve with piezo (x) and deflection (y) values.

	Returns
	-------
	

	"""
	slope, intercept, _, _, _ = linregress(
		approachCurve.piezo[0:endOfZeroline.index],
		approachCurve.deflection[0:endOfZeroline.index]
	)

	linearZerolineDeflectionValues = np.array(
		[intercept + slope*approachCurve.piezo[0:endOfZeroline.index]]
	)

	fitApproachCurve = nt.ForceDistanceCurve(
		piezo=approachCurve.piezo[0:endOfZeroline.index],
		deflection=linearDeflectionValues
	)

	return fitApproachCurve

def shif_deflection_values(
	approachCurve: nt.ForceDistanceCurve,
	endOfZeroline: nt.ForceDistancePoint,
	fitEndOfZeroline: nt.ForceDistanceCurve
) -> np.ndarray:
	"""
	Shift the deflection values a long the zero line to zero.
	Values to the end of the zero line are smoothed.

	Parameters
	----------
	approachCurves : namedTuple
		Raw approach curve with piezo (x) and deflection (y) values.
	endOfZeroline : nt.ForceDistancePoint
		
	fitEndOfZeroline : nt.ForceDistanceCurve
		

	Returns
	-------
	correctedDeflectionValues : np.ndarray
		
	"""
	return np.concatenate(
		[
			approachCurve.deflection[0:endOfZeroline.index] - fitEndOfZeroline.deflection,
			approachCurve.deflection[endOfZeroline.index:] - fitEndOfZeroline.deflection[-1]
		]
	)

def correct_piezo_values(
	approachCurve: nt.ForceDistanceCurve, 
	correctedDeflectionValues: np.ndarray, 
	endOfZeroline: nt.ForceDistancePoint
) -> Tuple[np.ndarray, nt.ForceDistancePoint]:
	"""
	Correct the piezo values of an approach curve by removing the 
	virtual topography offset.

	Parameters
	----------
	approachCurve : nt.ForceDistanceCurve
		Raw approach curve with piezo (x) and deflection (y) values.
	correctedDeflectionValues : np.ndarray
		Deflection (y) values shifted to zero along the zero line.
	endOfZeroline : nt.ForceDistancePoint
		Index, piezo (x) and deflection (y) value from the last 
		point of the zero line.

	Returns
	-------
	correctedPiezoValues : np.ndarray
		Piezo values shifted to zero with the unshifted point of contact.
	unshiftedPointOfContact : nt.ForceDistancePoint
		Index, piezo and deflection value from the point of contact
		before the shift along the x axis.
	"""
	indexZeroCrossing = locate_zero_crossing(
		correctedDeflectionValues,
		endOfZeroline
	)
	unshiftedPointOfContact = interpolate_unshifted_point_of_contact(
		approachCurve,
		indexZeroCrossing
	)
	correctedPiezoValues = shif_piezo_values(
		approachCurve,
		unshiftedPointOfContact
	)

	return correctedPiezoValues, unshiftedPointOfContact

def locate_zero_crossing(
	correctedDeflectionValues: np.ndarray,
	endOfZeroline: nt.ForceDistancePoint
) -> int:
	"""


	Parameters
	----------
	correctedDeflectionValues : np.ndarray

	endOfZeroline : nt.ForceDistancePoint
		

	Returns
	-------
	indexZeroCrossing : int
	

	Raises
	------

	"""
	deflectionAttractionPart = np.where(
		correctedDeflectionValues[endOfZeroline.index:] <= 0
	)[0]

	try: 
		indexZeroCrossing = deflectionAttractionPart[-1] + endOfZeroline.index
	except IndexError as e:
		raise NeedsNameError("") from e
	else:
		return indexZeroCrossing

def interpolate_unshifted_point_of_contact(
	approachCurve: nt.ForceDistanceCurve,
	indexZeroCrossing: int
) -> nt.ForceDistancePoint:
	"""

	Parameters
	----------

	Returns
	-------
	

	"""
	piezoUnshiftedPointOfContact = np.interp(
		0, 
		approachCurve.deflection[indexZeroCrossing-2:indexZeroCrossing+2], 
		approachCurve.piezo[indexZeroCrossing-2:indexZeroCrossing+2]
	)

	return nt.ForceDistancePoint(
		index=indexZeroCrossing,
		piezo=piezoUnshiftedPointOfContact,
		deflection=0
	)

def shif_piezo_values(
	approachCurve: nt.ForceDistanceCurve,
	unshiftedPointOfContact: nt.ForceDistancePoint
) -> np.ndarray:
	"""

	Parameters
	----------

	Returns
	-------
	

	"""
	return (
		approachCurve.piezo - unshiftedPointOfContact.piezo
	)
