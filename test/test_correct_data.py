import pytest
import numpy as np

import sys
sys.path.append('./sofa')

import data_processing.correct_data as cd
import data_processing.named_tuples as nt

def test_calculate_linear_fit_to_approach_curve_simple():
	"""
	"""
	simpleCurve = nt.ForceDistanceCurve(
		piezo=np.array([1, 2, 3, 4, 5]),
		deflection=np.array([1, -1, 0, -1, 1])
	)
	expectedDeflectionValues = np.array([0, 0, 0, 0, 0])

	fittedCurve, _ = cd.calculate_linear_fit_to_approach_curve(
		simpleCurve
	)

	np.testing.assert_array_equal(
		fittedCurve.deflection,
		expectedDeflectionValues
	)

def test_derivate_curve_simple():
	"""
	"""
	simpleCurve = nt.ForceDistanceCurve(
		piezo=np.array([1, 2, 3, 4, 5]),
		deflection=np.array([1, 1, 0, 4, 8])
	)
	expectedDerivation = np.array([0, -1, 4, 4])

	derivation = cd.derivate_curve(simpleCurve)

	np.testing.assert_array_equal(
		derivation,
		expectedDerivation
	)

def test_calculate_curve_intersections_simple():
	"""
	"""
	simpleCurve = nt.ForceDistanceCurve(
		piezo=np.array([1, 2, 3, 4, 5, 6]),
		deflection=np.array([1, 1, -1, -0.5, 2, 6])
	)
	simpleFittedCurve = nt.ForceDistanceCurve(
		piezo=np.array([1, 2, 3, 4, 5, 6]),
		deflection=np.array([-1, 0, 1, 2, 3, 4])
	)
	expectedFirstIntersection = 2
	expectedLastIntersection = 4

	firstIntersection, lastIntersection = cd.calculate_curve_intersections(
		simpleCurve,
		simpleFittedCurve
	)

	np.testing.assert_array_equal(
		[firstIntersection, lastIntersection],
		[expectedFirstIntersection, expectedLastIntersection]
	)

def test_calculate_maximum_deflection_difference_simple():
	"""
	"""
	simpleCurve = nt.ForceDistanceCurve(
		piezo=np.array([1, 2, 3, 4, 5, 6]),
		deflection=np.array([1, 1, -1, -0.5, 2, 6])
	)
	simpleFittedCurve = nt.ForceDistanceCurve(
		piezo=np.array([1, 2, 3, 4, 5, 6]),
		deflection=np.array([-1, 0, 1, 2, 3, 4])
	)
	firstIntersection = 2
	lastIntersection = 4
	expectedMaxDeflectionDifference = 3

	maxDeflectionDifference = cd.calculate_maximum_deflection_difference(
		simpleCurve,
		simpleFittedCurve,
		firstIntersection,
		lastIntersection
	)

	assert maxDeflectionDifference == expectedMaxDeflectionDifference