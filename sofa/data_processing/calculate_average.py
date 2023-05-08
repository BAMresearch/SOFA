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
	"""
	normedCurves = _interpolate_normed_curves(
		activeForceDistanceCurves
	)
	
	averagedDeflectionApproach = [
		np.mean(nthValues) 
		for nthValues 
		in zip(*NormedCurves.deflectionApproach)
	]
	averagedDeflectionContact = [
		np.mean(nthValues) 
		for nthValues 
		in zip(*NormedCurves.deflectionContact)
	]

	standardDeviationApproach = [
		np.std(nthValues) for nthValues in zip(*NormedCurves.deflectionApproach)
	]
	standardDeviationContact = [
		np.std(nthValues) for nthValues in zip(*NormedCurves.deflectionContact)
	]

	averageForceDistanceCurve = nt.ForceDistanceCurve(
		piezo=np.concatenate(normedCurves.piezoApproach , normedCurves.piezoContact),
		deflection=np.concatenate(averagedDeflectionApproach, averagedDeflectionContact)
	)
	standardDeviation = standardDeviationApproach + standardDeviationContact

	return nt.AverageForceDistanceCurve(
		
	)

def _interpolate_normed_curves(
	activeForceDistanceCurves
) -> None:
	"""
	"""
	numberOfDataPoints = 2000

	minimumPizeo = _get_minimum_piezo(activeForceDistanceCurves)
	maximumDeflection = _get_maximum_deflection(activeForceDistanceCurves)

	normedPiezoApproach = np.linspace(minimumPizeo, 0, numberOfDataPoints)
	normedDeflectionApproach = []
	normedDeflectionContact = np.linspace(0, maximumDeflection, numberOfDataPoints)
	normedPiezoContact = []

	# Interpolate y values for the left and right part.
	for forceDistanceCurve in activeForceDistanceCurves:
		indexZeroCrossing = forceDistanceCurve.channelMetadata.pointOfContact.index

		normedDeflectionApproach.append(
			np.interp(
				normedPiezoApproach, 
				forceDistanceCurve.dataApproachCorrected.piezo[:indexZeroCrossing], 
				forceDistanceCurve.dataApproachCorrected.deflection[:indexZeroCrossing]
			)
		)
		normedPiezoContact.append(
			np.interp(
				normedDeflectionContact, 
				forceDistanceCurve.dataApproachCorrected.deflection[indexZeroCrossing:], 
				forceDistanceCurve.dataApproachCorrected.piezo[indexZeroCrossing:]
			)
		)

	return nt.NormedCurves(
		normedPiezoApproach, 
		np.asarray(normedDeflectionApproach), 
		normedDeflectionContact, 
		np.asarray(normedPiezoContact)
	)

def _get_minimum_piezo(
	activeForceDistanceCurves
) -> float:
	"""
	"""
	piezoValues = [
		forceDistanceCurve.dataApproachCorrected.piezo
		for forceDistanceCurve
		in activeForceDistanceCurves
	]

	return np.min(piezoValues)

def _get_maximum_deflection(
	activeForceDistanceCurves
) -> float:
	"""
	"""
	deflectionValues = [
		forceDistanceCurve.dataApproachCorrected.deflection
		for forceDistanceCurve
		in activeForceDistanceCurves
	]

	return np.max(deflectionValues)