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

def calculate_average(
	activeForceDistanceCurves: List,
) -> nt.AverageForceDistanceCurve:
	"""
	Calculate the average and standard deviation
	of the active force distance curves.

	Parameters
	----------
	activeForceDistanceCurves : list[ForceDistanceCurve]
		Piezo(x) and deflection (y) values of the
		active force distance curves.
	
	Returns
	-------
	averageForceDistanceCurve : nt.AverageForceDistanceCurve
		Contains the piezo(x) and deflection (y) values
		of the average curve and the standard deviation.
	"""
	normedCurves = interpolate_normed_curves(
		activeForceDistanceCurves
	)
	averagedDeflectionNonContact = [
		np.mean(nthValues) 
		for nthValues 
		in zip(*normedCurves.deflectionNonContact)
	]
	averagedDeflectionContact = [
		np.mean(nthValues) 
		for nthValues 
		in zip(*normedCurves.deflectionContact)
	]
	standardDeviationNonContact = [
		np.std(nthValues) for nthValues in zip(*normedCurves.deflectionNonContact)
	]
	standardDeviationContact = [
		np.std(nthValues) for nthValues in zip(*normedCurves.deflectionContact)
	]
	return nt.AverageForceDistanceCurve(
		piezoNonContact=normedCurves.piezoNonContact,
		deflectionNonContact=averagedDeflectionNonContact,
		piezoContact=normedCurves.piezoContact,
		deflectionContact=averagedDeflectionContact,
		standardDeviationNonContact=standardDeviationNonContact,
		standardDeviationContact=standardDeviationContact
	)

def interpolate_normed_curves(
	activeForceDistanceCurves
) -> None:
	"""
	

	Parameters
	----------
	activeForceDistanceCurves : list[nt.ForceDistanceCurve]
		Piezo(x) and deflection (y) values of the
		active force distance curves.
	
	Returns
	-------
	normedCurves : nt.NormedCurves
		
	"""
	numberOfDataPoints = 2000
	minimumPizeo = get_minimum_piezo(activeForceDistanceCurves)
	maximumDeflection = get_maximum_deflection(activeForceDistanceCurves)

	normedPiezoNonContact, normedDeflectionNonContact = interpolate_non_contact_part(
		activeForceDistanceCurves,
		minimumPizeo,
		numberOfDataPoints
	)
	normedPiezoContact, normedDeflectionContact = interpolate_contact_part(
		activeForceDistanceCurves,
		maximumDeflection,
		numberOfDataPoints
	)

	return nt.NormedCurves(
		piezoNonContact=normedPiezoNonContact, 
		deflectionNonContact=normedDeflectionNonContact, 
		piezoContact=normedPiezoContact, 
		deflectionContact=normedDeflectionContact
	)

def get_minimum_piezo(
	activeForceDistanceCurves: List
) -> float:
	"""
	Find the minimum piezo value of all
	active force distance curves.

	Parameters
	----------
	activeForceDistanceCurves : list[ForceDistanceCurve]
		Piezo(x) and deflection (y) values of the
		active force distance curves.

	Returns
	-------
	minimumPiezoValue : float
		The smallest piezo value of all active
		force distance curves.
	"""
	minimumPiezoValues = [
		np.min(forceDistanceCurve.dataApproachCorrected.piezo)
		for forceDistanceCurve
		in activeForceDistanceCurves
	]
	return np.min(minimumPiezoValues)

def get_maximum_deflection(
	activeForceDistanceCurves: List
) -> float:
	"""
	Find the maximum deflection value of all
	active force distance curves.

	Parameters
	----------
	activeForceDistanceCurves : list[nt.ForceDistanceCurve]
		Piezo(x) and deflection (y) values of the
		active force distance curves.

	Returns
	-------
	maximumDeflectionValue : float
		The biggest deflection value of all 
		active force distance curves.
	"""
	maximumDeflectionValues = [
		np.max(forceDistanceCurve.dataApproachCorrected.deflection)
		for forceDistanceCurve
		in activeForceDistanceCurves
	]
	return np.max(maximumDeflectionValues)

def interpolate_non_contact_part(
	activeForceDistanceCurves: List,
	minimumPizeo: float,
	numberOfDataPoints: int
) -> Tuple[np.ndarray]:
	"""
	"""
	normedPiezoNonContact = np.linspace(minimumPizeo, 0, numberOfDataPoints)
	normedDeflectionNonContact = []

	for forceDistanceCurve in activeForceDistanceCurves:
		indexZeroCrossing = forceDistanceCurve.channelMetadata.pointOfContact.index
		normedDeflectionNonContact.append(
			np.interp(
				normedPiezoNonContact, 
				forceDistanceCurve.dataApproachCorrected.piezo[:indexZeroCrossing], 
				forceDistanceCurve.dataApproachCorrected.deflection[:indexZeroCrossing]
			)
		)
	normedDeflectionNonContact = np.asarray(normedDeflectionNonContact)

	return normedPiezoNonContact, normedDeflectionNonContact

def interpolate_contact_part(
	activeForceDistanceCurves: List,
	maximumDeflection: float,
	numberOfDataPoints: int
) -> Tuple[np.ndarray]:
	"""


	Parameters
	----------
	activeForceDistanceCurves : list[nt.ForceDistanceCurve]
		Piezo(x) and deflection (y) values of the
		active force distance curves.
	maximumDeflection : float
		
	numberOfDataPoints : int
		

	Returns
	-------
	normedPiezoContact : np.ndarray

	normedDeflectionContact : np.ndarray
	"""
	normedPiezoContact = np.linspace(0, maximumDeflection, numberOfDataPoints)
	normedDeflectionContact = []

	for forceDistanceCurve in activeForceDistanceCurves:
		indexZeroCrossing = forceDistanceCurve.channelMetadata.pointOfContact.index
		normedDeflectionContact.append(
			np.interp(
				normedPiezoContact, 
				forceDistanceCurve.dataApproachCorrected.deflection[indexZeroCrossing:], 
				forceDistanceCurve.dataApproachCorrected.piezo[indexZeroCrossing:]
			)
		)
	normedDeflectionContact = np.asarray(normedDeflectionContact)

	return normedPiezoContact, normedDeflectionContact