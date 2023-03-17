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

import data_processing.custom_exceptions as ce
import data_processing.named_tuples as nt

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
) -> Tuple[np.ndarray, nt.ForceDistancePoint, nt.CoefficientsFitApproachCurve]:
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
	fitZeroline = calculate_linear_fit_to_zeroline(
		approachCurve,
		endOfZeroline
	)
	correctedDeflectionValues = shif_deflection_values(
		approachCurve,
		endOfZeroline,
		fitZeroline
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
) -> Tuple[nt.ForceDistanceCurve, nt.CoefficientsFitApproachCurve]:
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
	coefficientsFitApproachCurve : nt.CoefficientsFitApproachCurve
		Slope (raw stiffness) and intercept (raw offset) of the fitted
		line.
	"""
	slope, intercept, _, _, _ = linregress(
		approachCurve.piezo,
		approachCurve.deflection
	)
	linearDeflectionValues = np.array(
		intercept + slope*approachCurve.piezo
	)

	fitApproachCurve = nt.ForceDistanceCurve(
		piezo=approachCurve.piezo,
		deflection=linearDeflectionValues
	)
	coefficientsFitApproachCurve = nt.CoefficientsFitApproachCurve(
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
	approachCurve : nt.ForceDistanceCurve
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
	approachCurve : nt.ForceDistanceCurve
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
) -> Tuple[int, int, nt.CoefficientsFitApproachCurve]:
	"""
	Calculates borders to restrict the area in which the 
	end of the zero line is searched for.
	
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
	indexMaxDeflectionDifference: int
		Index of the point with the maximum deflection difference
		within in area between the two intersections, slighty 
		shifted to the right.
	"""
	indexFirstIntersection, indexLastIntersection = calculate_curve_intersections(
		approachCurve, 
		fitApproachCurve
	)
	indexMaxDeflectionDifference = calculate_maximum_deflection_difference(
		approachCurve, 
		fitApproachCurve,
		indexFirstIntersection,
		indexLastIntersection
	)

	return indexFirstIntersection, indexMaxDeflectionDifference

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

def calculate_maximum_deflection_difference(
	approachCurve: nt.ForceDistanceCurve,
	fitApproachCurve: nt.ForceDistanceCurve,
	indexFirstIntersection: int,
	indexLastIntersection: int
) -> int:
	"""
	Calculate the point with the maximum deflection difference
	within the area between the two intersections and shift it
	lightly to the right.

	Parameters
	----------
	approachCurves : namedTuple
		Raw approach curve with piezo (x) and deflection (y) values.
	fitApproachCurve : nt.ForceDistanceCurve
		Linear curve fit to the approach curve with the same 
		piezo (x) values and adjusted deflection (y) values.
	indexFirstIntersection : int
		Index of the first intersection point of the approach curve
		and it's linear fit.
	indexLastIntersection : int
		Index of the last intersection point of the approach curve
		and it's linear fit.

	Returns
	-------
	adjustedIndexMaxDeflectionDifference : int
		Index of the point with the maximum deflection difference
		within in area between the two intersections, slighty 
		shifted to the right.
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
	Locate the end of the zero line as the first point with 
	a negative slope before the jump to contact.

	Parameters
	----------
	approachCurve : nt.ForceDistanceCurve
		Raw approach curve with piezo (x) and deflection (y) values.
	smoothedDerivationDeflection : np.ndarray
		Smoothed first derivation of the deflection (y) values
		of the approach curve.
	indexLeftBorder : int
		Index of the first intersection point of the approach curve
		and it's linear fit.
	indexRightBorder : int
		Index of the point with the maximum deflection difference
		in the attractive area.

	Returns
	-------
	endOfZeroline : nt.ForceDistancePoint
		Index, piezo and deflection value of the end of the 
		zero line.

	Raises
	------
	ce.UnableToLocateEndOfZerolineError : CorrectionError
		If there are no points with a negative slope within 
		the area of the left and right border.
	"""
	pointsWithDecreasingDeflection = np.where(
		smoothedDerivationDeflection[indexLeftBorder:indexRightBorder] < 0
	)

	try:
		indexEndOfZeroline = pointsWithDecreasingDeflection[0] + indexLeftBorder
	except IndexError as e:
		raise ce.UnableToLocateEndOfZerolineError from e
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
	Calculate linear regression curve to the zeroline of the raw
	approach curve.

	Parameters
	----------
	approachCurve : nt.ForceDistanceCurve
		Raw approach curve with piezo (x) and deflection (y) values.
	endOfZeroline : nt.ForceDistancePoint
		Index, piezo and deflection value of the end of the 
		zero line.

	Returns
	-------
	fitApproachCurve : nt.ForceDistanceCurve
		Linear regression curve to the zero line, with raw 
		piezo (x) values and fitted deflection (y) values.
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
	fitZeroline: nt.ForceDistanceCurve
) -> np.ndarray:
	"""
	Shift the deflection values along the zero line to zero.
	Values to the end of the zero line are smoothed.

	Parameters
	----------
	approachCurve : nt.ForceDistanceCurve
		Raw approach curve with piezo (x) and deflection (y) values.
	endOfZeroline : nt.ForceDistancePoint
		Index, piezo and deflection value of the end of the 
		zero line.
	fitZeroline : nt.ForceDistanceCurve
		Linear regression curve to the zero line, with raw 
		piezo (x) values and fitted deflection (y) values.

	Returns
	-------
	correctedDeflectionValues : np.ndarray
		Deflection values shifted to zero along the zero line.
	"""
	return np.concatenate(
		[
			approachCurve.deflection[0:endOfZeroline.index] - fitZeroline.deflection,
			approachCurve.deflection[endOfZeroline.index:] - fitZeroline.deflection[-1]
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
	indexZeroCrossing = locate_index_zero_crossing(
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

def locate_index_zero_crossing(
	correctedDeflectionValues: np.ndarray,
	endOfZeroline: nt.ForceDistancePoint
) -> int:
	"""
	Locate the first zero crossing after the end of the zeroline.

	Parameters
	----------
	correctedDeflectionValues : np.ndarray
		Already corrected deflection values shifted to zero 
		along the end of the zero line.
	endOfZeroline : nt.ForceDistancePoint
		Index, piezo and deflection value of the end of the 
		zero line.

	Returns
	-------
	indexZeroCrossing : int
		Index of the last point after the end of the zeroline
		with a deflection value samller or equal to zero.

	Raises
	------
	ce.UnableToLocateZeroCrossingAfterEozlError : CorrectionError
		If no negative values exist after the end of the zeroline.
	"""
	deflectionAttractionPart = np.where(
		correctedDeflectionValues[endOfZeroline.index:] <= 0
	)[0]

	try: 
		indexZeroCrossing = deflectionAttractionPart[-1] + endOfZeroline.index
	except IndexError as e:
		raise ce.UnableToLocateZeroCrossingAfterEozlError from e
	else:
		return indexZeroCrossing

def interpolate_unshifted_point_of_contact(
	approachCurve: nt.ForceDistanceCurve,
	indexZeroCrossing: int
) -> nt.ForceDistancePoint:
	"""
	Interpolate the exact piezo value at which the zero crossing occurs.

	Parameters
	----------
	approachCurve : nt.ForceDistanceCurve
		Raw approach curve with piezo (x) and deflection (y) values.
	indexZeroCrossing : int
		Index of the last point after the end of the zeroline
		with a deflection value samller or equal to zero.

	Returns
	-------
	unshiftedPointOfContact : nt.ForceDistancePoint
		Index, piezo and deflection value of the point of contact
		before the correction of the piezo values.
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
	Shift the piezo values along the point of contact to zero.

	Parameters
	----------
	approachCurve : nt.ForceDistanceCurve
		Raw approach curve with piezo (x) and deflection (y) values.
	unshiftedPointOfContact : nt.ForceDistancePoint
		Index, piezo and deflection value of the point of contact
		before the correction of the piezo values.

	Returns
	-------
	correctedPiezoValues : np.ndarray
		Piezo values shifted to zero along the point of contact.
	"""
	return (
		approachCurve.piezo - unshiftedPointOfContact.piezo
	)
