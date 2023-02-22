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
from typing import List, Tuple, NamedTuple

import numpy as np
from scipy.stats import linregress
from scipy.ndimage import gaussian_filter1d

import exceptions.custom_exceptions as ce
import data_processing.named_tuples as nt

def correct_approach_curve(
	approachCurve: NamedTuple,
) -> Tuple[NamedTuple]:
	"""
	Correct an approach curve by shifting it's point of contact to the origin.

	Parameters
	----------
	approachCurves : NamedTuple
		Raw approach curve with piezo (x) and deflection (y) values.

	Returns
	-------
	correctedCurveData : NamedTuple 
		Corrected approach curve with shifted piezo (x) and deflection (y) values.
	correctionMetaData : NamedTuple
		Metadata generated during the correction of the curve, which is used for 
		calculating the different channels.
	"""
	correctedDeflectionValues, endOfZeroline, coefficients = correct_deflection_values(
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
	correctionMetaData = nt.correctionMetaData(
		endOfZeroline=endOfZeroline,
		pointOfContact=pointOfContact,
		rawStiffness=coefficients[0],
		rawOffset=coefficients[1],
	)

	return correctedDataApproach, correctionMetaData

def correct_deflection_values(
	approachCurve: NamedTuple,
) -> Tuple:
	"""
	Correct the deflection values of an approach curve by removing the 
	virtual deflection.

	Parameters
	----------
	approachCurves : NamedTuple
		Raw approach curve with piezo (x) and deflection (y) values.
	
	Returns
	-------
	correctedDeflectionValues : np.ndarray
	
	endOfZeroline : NamedTuple

	coefficients : Tuple
	"""
	indexLeftBorder, indexRightBorder, coefficients = restrict_deflection_values(
		approachCurve
	)
	endOfZeroline = locate_end_of_zeroline(
		approachCurve,
		indexLeftBorder,
		indexRightBorder
	)
	correctedDeflectionValues = smooth_zeroline()

	return correctedDeflectionValues, endOfZeroline, coefficients

def correct_piezo_values(
	approachCurve: NamedTuple, 
	correctedDeflectionValues: np.ndarray, 
	endOfZeroline: NamedTuple
) -> Tuple:
	"""
	Correct the piezo values of an approach curve by removing the 
	virtual topography offset.

	Parameters
	----------
	approachCurve : NamedTuple

	correctedDeflectionValues : np.ndarray

	endOfZeroline : NamedTuple

	Returns
	-------
	correctedPiezoValues : np.ndarray

	pointOfContact : NamedTuple
	"""
	pointOfContact = 
	correctedPiezoValues = approachCurve.piezo - pointOfContact.piezo

	return correctedPiezoValues, pointOfContact

def restrict_deflection_values(
	approachCurve: NamedTuple
) -> Tuple:
	"""

	Parameters
	----------
	approachCurves : NamedTuple
		Raw approach curve with piezo (x) and deflection (y) values.

	Returns
	-------

	"""
	linearCurveFit, coefficients = calculate_linear_fit(
		approachCurve
	)
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

	return indexLeftBorder, adjustedIndexRightBorder, coefficients

def calculate_linear_fit(
	approachCurve: NamedTuple
) -> Tuple:
	"""

	Parameters
	----------
	approachCurves : NamedTuple
		Raw approach curve with piezo (x) and deflection (y) values.

	Returns
	-------

	"""
	slope, intercept, _, _, _ = linregress(
		approachCurve.piezo,
		approachCurve.deflection
	)
	linearDeflectionValues = np.array([
		approachCurve.piezo,
		intercept + slope*approachCurve.piezo
	])
	linearCurveFit = ForceDistanceCurve(
		piezo=approachCurve.piezo,
		deflection=linearDeflectionValues
	)

	return linearCurveFit, (slope, intercept)

def calculate_curve_intersections(
	approachCurve: NamedTuple,
	linearCurveFit: NamedTuple
) -> Tuple[int]:
	"""

	Parameters
	----------

	Returns
	-------

	Raises
	------
	"""
	temp = np.where(
		approachCurve.deflection < linearCurveFit.deflection
	)[0]

	try:
		indexLeftBorder = temp[0]
		indexRightBorder = temp[-1]
	except IndexError as e:
		raise from e
	else:
		return indexLeftBorder, indexRightBorder

def adjust_intersection_border(
	approachCurve: NamedTuple,
	linearCurveFit: NamedTuple,
	indexLeftBorder: int,
	indexRightBorder: int
) -> int:
	"""
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
	approachCurve: NamedTuple,
	indexLeftBorder: int,
	indexRightBorder: int
) -> int: 
	"""
	

	Parameters
	----------
	approachCurve : NamedTuple

	indexLeftBorder : int
		
	indexRightBorder : int


	Returns
	-------
	indexEndOfZeroline : int
	

	Raises
	------

	"""
	endOfZeroline = np.where(
		smoothedDerivation[indexLeftBorder:indexRightBorder] < 0
	)

	try:

	except IndexError:

	else:
		return 

def smooth_zeroline(

) -> None:
	"""
	"""


def locate_zero_crossing(
	deflection: np.ndarray,
	indexEndOfZeroline: int
) -> int:
	"""


	Parameters
	----------
	deflection : np.ndarray

	indexEndOfZeroline : int
		

	Returns
	-------
	indexZeroCrossing : int
	

	Raises
	------

	"""
	deflectionAttractionPart = np.where(
		deflection[indexEndOfZeroline:] <= 0
	)[0]

	try: 
		indexZeroCrossing = deflectionAttractionPart[-1] + indexEndOfZeroline
	except IndexError as e:
		raise NeedsNameError("") from e
	else:
		return indexZeroCrossing

def interpolate_point_of_contact() -> Tuple:
	"""
	"""
