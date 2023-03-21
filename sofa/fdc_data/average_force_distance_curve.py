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

class AverageForceDistanceCurve():
	"""
	

	Attributes
	----------
	averageData : np.ndarray

	standardDeviation : np.ndarray

	lineRepresentation : matplotlib.lines.Line2D

	errorbarBar : mpl.container.ErrorbarContainer

	"""
	def __init__(self):
		"""
		"""
		self.averageData: np.ndarray
		self.standardDeviation: np.ndarray
		self.lineRepresentation: matplotlib.lines.Line2D
		self.errorbarBar: mpl.container.ErrorbarContainer

	def calculate_average(
		self,
		forceDistanceCurves: List,
	) -> None:
		"""
		"""
		activeForceDistanceCurves = _get_active_force_distance_curves(
			forceDistanceCurves,
		)
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

		self.averageData = nt.ForceDistanceCurve(
			piezo=np.concatenate(normedCurves.piezoApproach , normedCurves.piezoContact),
			deflection=np.concatenate(averagedDeflectionApproach, averagedDeflectionContact)
		)

		self.standardDeviation = standardDeviationApproach + standardDeviationContact

	@staticmethod
	def _get_active_force_distance_curves(
		forceDistanceCurves: List,
	) -> List:
		"""
		"""
		return [
			forceDistanceCurve
			for forceDistanceCurve
			in forceDistanceCurves
			if forceDistanceCurve.isActive
		]

	@staticmethod
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

	@staticmethod
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

	@staticmethod
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

	def create_line_representation(self) -> None: 
		"""
		"""
		self.lineRepresentation = plt_data.create_average_line(
			self.averageData
		)

	def create_line_representation_as_errorbar(self) -> None:
		"""
		"""
		self.errorbarBar = plt_data.create_average_errorbar(
			self.averageData,
			self.standardDeviation
		) 