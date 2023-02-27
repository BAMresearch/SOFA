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
	correctedDeflectionValues, endOfZeroline, linearCoefficients = correct_deflection_values(
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
		linearCoefficients=linearCoefficients
	)

	return correctedDataApproach, channelMetadata

def correct_deflection_values(
	approachCurve: nt.ForceDistanceCurve,
) -> Tuple[np.ndarray, nt.ForceDistancePoint, nt.LinearCoefficients]:
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
	linearCoefficients : nt.LinearCoefficients
		Slope and intercept value of a lineare fit to the raw data.
	"""
	smoothedDerivation = calculate_smoothed_derivation(
		approachCurve
	)
	linearCurveFit, linearCoefficients = calculate_linear_fit_to_approach_curve(
		approachCurve
	)
	indexLeftBorder, indexRightBorder = restrict_deflection_values(
		approachCurve,
		linearCurveFit
	)
	endOfZeroline = locate_end_of_zeroline(
		smoothedDerivation,
		indexLeftBorder,
		indexRightBorder
	)
	fittedLine = calculate_linear_fit_to_zeroline(
		approachCurve,
		endOfZeroline
	)
	correctedDeflectionValues = shif_deflection_values(
		approachCurve,
		endOfZeroline,
		fittedLine
	)

	return correctedDeflectionValues, endOfZeroline, linearCoefficients

def calculate_smoothed_derivation(
	approachCurve: nt.ForceDistanceCurve,
) -> np.ndarray:
	"""
	"""
	derivation = derivate_curve(approachCurve)
	smoothedDerivation = smooth_derivation(derivation)

	return smoothedDerivation

def derivate_curve(
	approachCurve: nt.ForceDistanceCurve,
) -> np.ndarray:
	"""

	
	Parameters
	----------
	

	Returns
	-------


	"""
	return (
		np.diff(approachCurve.deflection) / np.diff(approachCurve.piezo)
	)

def smooth_derivation(
	derivationApproachCurve: np.ndarray,
	smoothFactor: int = 10
) -> np.ndarray:
	"""

	
	Parameters
	----------
	

	Returns
	-------


	"""
	return gaussian_filter1d(
		derivationApproachCurve,
		sigma=smoothFactor
	)

def calculate_linear_fit_to_approach_curve(
	approachCurve: nt.ForceDistanceCurve
) -> Tuple[nt.ForceDistanceCurve, nt.LinearCoefficients]:
	"""


	Parameters
	----------
	approachCurves : nt.ForceDistanceCurve
		Raw approach curve with piezo (x) and deflection (y) values.

	Returns
	-------
	linearCurveFit : nt.ForceDistanceCurve

	linearCoefficients : nt.LinearCoefficients
		Slope (raw stiffness) and intercept (raw offset) 
	"""
	slope, intercept, _, _, _ = linregress(
		approachCurve.piezo,
		approachCurve.deflection
	)
	linearDeflectionValues = np.array(
		[intercept + slope*approachCurve.piezo]
	)

	linearCurveFit = nt.ForceDistanceCurve(
		piezo=approachCurve.piezo,
		deflection=linearDeflectionValues
	)
	linearCoefficients = nt.LinearCoefficients(
		slope=slope,
		intercept=intercept
	)

	return linearCurveFit, linearCoefficients

def restrict_deflection_values(
	approachCurve: nt.ForceDistanceCurve,
	linearCurveFit: nt.ForceDistanceCurve
) -> Tuple[int, int, nt.LinearCoefficients]:
	"""


	Parameters
	----------
	approachCurves : namedTuple
		Raw approach curve with piezo (x) and deflection (y) values.
	linearCurveFit : nt.ForceDistanceCurve
	
	Returns
	-------
	indexLeftBorder : int

	adjustedIndexRightBorder: int

	linearCoefficients: nt.LinearCoefficients
		Slope (raw stiffness) and intercept (raw offset) 
	"""
	indexLeftBorder, indexRightBorder = calculate_curve_intersections(
		approachCurve, 
		linearCurveFit
	)
	adjustedIndexRightBorder = adjust_intersection_border(
		approachCurve, 
		linearCurveFit,
		indexLeftBorder,
		indexRightBorder
	)

	return indexLeftBorder, adjustedIndexRightBorder, linearCoefficients

def calculate_curve_intersections(
	approachCurve: nt.ForceDistanceCurve,
	linearCurveFit: nt.ForceDistanceCurve
) -> Tuple[int]:
	"""


	Parameters
	----------
	approachCurve : nt.ForceDistanceCurve
		
	linearCurveFit : nt.ForceDistanceCurve
		

	Returns
	-------
	indexLeftBorder : int 
		
	indexRightBorder : int


	Raises
	------
	LinearFitIntersectionError : ce.CorrectionError

	"""
	temp = np.where(
		approachCurve.deflection < linearCurveFit.deflection
	)[0]

	try:
		indexLeftBorder = temp[0]
		indexRightBorder = temp[-1]
	except IndexError as e:
		raise ce.LinearFitIntersectionError from e
	else:
		return indexLeftBorder, indexRightBorder

def adjust_intersection_border(
	approachCurve: nt.ForceDistanceCurve,
	linearCurveFit: nt.ForceDistanceCurve,
	indexLeftBorder: int,
	indexRightBorder: int
) -> int:
	"""


	Parameters
	----------
	approachCurve : nt.ForceDistanceCurve
	
	linearCurveFit : nt.ForceDistanceCurve
	
	indexLeftBorder : int

	indexRightBorder : int


	Returns
	-------
	adjustedIndexRightBorder : int

	"""
	deflectionDifferences = np.absolute(
		linearCurveFit.deflection - approachCurve.deflection
	)
	indexMaxDeflectionDifference = np.argmax(
		deflectionDifferences[indexLeftBorder:indexRightBorder]
	) + indexLeftBorder
	adjustedIndexRightBorder = int(
		indexMaxDeflectionDifference 
		+ ((indexRightBorder - indexMaxDeflectionDifference) * 0.05)
	)

	return adjustedIndexRightBorder

def locate_end_of_zeroline(
	smoothedDerivationApproachCurve: np.ndarray,
	indexLeftBorder: int,
	indexRightBorder: int
) -> nt.ForceDistancePoint: 
	"""
	

	Parameters
	----------
	smoothedDerivationApproachCurve : np.ndarray

	indexLeftBorder : int
		
	indexRightBorder : int


	Returns
	-------
	endOfZeroline : nt.ForceDistancePoint
	

	Raises
	------
	: CorrectionError

	"""
	endOfZeroline = np.where(
		smoothedDerivationApproachCurve[indexLeftBorder:indexRightBorder] < 0
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
):
	"""
	"""
	slope, intercept, _, _, _ = linregress(
		approachCurve.piezo[0:endOfZeroline.index],
		approachCurve.deflection[0:endOfZeroline.index]
	)

	linearZerolineDeflectionValues = np.array(
		[intercept + slope*approachCurve.piezo[0:endOfZeroline.index]]
	)

	linearCurveFit = nt.ForceDistanceCurve(
		piezo=approachCurve.piezo[0:endOfZeroline.index],
		deflection=linearDeflectionValues
	)

	return linearCurveFit

def shif_deflection_values(
	approachCurve: nt.ForceDistanceCurve,
	endOfZeroline: nt.ForceDistancePoint,
	fittedLine: nt.ForceDistanceCurve
) -> np.ndarray:
	"""
	"""
	return np.concatenate(
		[
			approachCurve.deflection[0:endOfZeroline.index] - fittedLine.deflection,
			approachCurve.deflection[endOfZeroline.index:] - fittedLine.deflection[-1]
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
		Deflection values shifted to zero along the zero line.
	endOfZeroline : nt.ForceDistancePoint
		Index, piezo and deflection value from the last point 
		of the zero line.

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
	"""
	return (
		approachCurve.piezo - unshiftedPointOfContact.piezo
	)
