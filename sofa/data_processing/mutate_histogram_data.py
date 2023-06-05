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
from typing import List
import functools

import numpy as np

def get_index_of_minimum_bin_value(
	binValues: List,
	activeData: np.ndarray
) -> int:
	"""
	Get the index of the of the bin value
	which limits the active data from below.

	Parameters
	----------
	binValues : List
		Values of the bins from the data of
		a channel.
	activeData : np.ndarray
		Active data of a channel.

	Returns
	-------
	indexMinBinValue : int
		Index of the lower limit of the
		active data.
	"""
	return np.where(binValues <= np.nanmin(activeData))[0][-1]

def get_index_of_maximum_bin_value(
	binValues: List,
	activeData: np.ndarray
) -> int:
	"""
	Get the index of the of the bin value
	which limits the active data from above.

	Parameters
	----------
	binValues : List
		Values of the bins from the data of
		a channel.
	activeData : np.ndarray
		Active data of a channel.
	
	Returns
	-------
	indexMinBinValue : int
		Index of the upper limit of the
		active data.
	"""
	return np.where(binValues >= np.nanmax(activeData))[0][0]

def restrict_histogram_min_up(
	indexMinBinValue: int,
	indexMaxBinValue: int,
	binValues: List,
	data: np.ndarray
) -> np.ndarray: 
	"""
	Restrict the histogram by increasing 
	the border for the minimum value.

	Parameters
	----------
	indexMinBinValue : int
		Index of the lower limit of the
		active data.
	indexMaxBinValue : int
		Index of the upper limit of the
		active data.
	binValues : List
		Values of the bins from the data of
		a channel.
	data : np.ndarray
		Data of a channel.
	
	Returns
	-------
	inactiveDataPoints : np.ndarray
		Data point which are below the new 
		minimum treshold.
	"""
	if indexMinBinValue >= indexMaxBinValue - 1:
		return np.array([])

	minimumTreshold = binValues[indexMinBinValue + 1]
	inactiveDataPoints = np.where(
		data < minimumTreshold
	)[0]

	return inactiveDataPoints

def restrict_histogram_min_down(
	indexMinBinValue: int,
	indexMaxBinValue: int,
	binValues: List,
	data: np.ndarray
) -> np.ndarray: 
	"""
	Restrict the histogram by decreasing 
	the border for the minimum value.

	Parameters
	----------
	indexMinBinValue : int
		Index of the lower limit of the
		active data.
	indexMaxBinValue : int
		Index of the upper limit of the
		active data.
	binValues : List
		Values of the bins from the data of
		a channel.
	data : np.ndarray
		Data of a channel.

	Returns
	-------
	reactivatedDataPoints : np.ndarray
		Data point which are within the
		old and new minimum treshold.
	"""
	
	if indexMinBinValue <= 0:
		return np.array([])

	while True:
		oldMinBinValue = binValues[indexMinBinValue]
		indexMinBinValue -= 1
		newMinBinValue = binValues[indexMinBinValue]

		reactivatedDataPoints = np.where(
			np.logical_and(
				data >= newMinBinValue, 
				data < oldMinBinValue
			)
		)[0]

		if len(reactivatedDataPoints) > 0 or indexMinBinValue == 0:
			break

	return reactivatedDataPoints

def restrict_histogram_max_up(
	indexMinBinValue: int,
	indexMaxBinValue: int,
	binValues: List,
	numberOfBins: int,
	data: np.ndarray
) -> np.ndarray: 
	"""
	Restrict the histogram by increasing 
	the border for the maximum value.

	Parameters
	----------
	indexMinBinValue : int
		Index of the lower limit of the
		active data.
	indexMaxBinValue : int
		Index of the upper limit of the
		active data.
	binValues : List
		Values of the bins from the data of
		a channel.
	numberOfBins : int
		Number of bins specified in the 
		main window of SOFA.
	data : np.ndarray
		Data of a channel.

	Returns
	-------
	reactivatedDataPoints : np.ndarray
		Data point which are within the
		old and new maximum treshold.
	"""
	if indexMaxBinValue >= numberOfBins:
		return np.array([]) 

	while True:
		oldMaxBinValue = binValues[indexMaxBinValue]
		indexMaxBinValue += 1
		newMaxBinValue = binValues[indexMaxBinValue]

		reactivatedDataPoints = np.where(
			np.logical_and(
				data <= newMaxBinValue, 
				data > oldMaxBinValue
			)
		)[0]

		if len(reactivatedDataPoints) > 0 or indexMaxBinValue == numberOfBins:
			break

	return reactivatedDataPoints

def restrict_histogram_max_down(
	indexMinBinValue: int,
	indexMaxBinValue: int,
	binValues: List,
	data: np.ndarray
) -> np.ndarray: 
	"""
	Restrict the histogram by decreasing 
	the border for the maximum value.

	Parameters
	----------
	indexMinBinValue : int
		Index of the lower limit of the
		active data.
	indexMaxBinValue : int
		Index of the upper limit of the
		active data.
	binValues : List
		Values of the bins from the data of
		a channel.
	data : np.ndarray
		Data of a channel.

	Returns
	-------
	inactiveDataPoints : np.ndarray
		Data point which are above the new 
		maximum treshold.
	"""
	if indexMaxBinValue <= indexMinBinValue + 1:
		return np.array([])

	maximumTreshold = binValues[indexMaxBinValue - 1]
	inactiveDataPoints = np.where(
		data > maximumTreshold
	)[0]

	return inactiveDataPoints 