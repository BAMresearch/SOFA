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
from typing import List, Tuple, Dict
import glob
import os
import re
import functools

import numpy as np

from igor.binarywave import load as loadibw

def decorator_check_file_size_image(function):
	"""

	"""
	@functools.wraps(function)
	def wrapper_check_file_size_image(*args, **kwargs):
		imagedData = function(*args, **kwargs)
		measurementDataSize = args[1]
		if measurementDataSize != imagedData.size:
			raise WrongImageSizeError()
		else:
			return imagedData

	return wrapper_check_file_size_image

def decorator_check_file_size_channel(function):
	"""

	"""
	@functools.wraps(function)
	def wrapper_check_file_size_image(*args, **kwargs):
		channelData = function(*args, **kwargs)
		measurementDataSize = args[1]
		if measurementDataSize != channelData.size:
			raise WrongChannelSizeError()
		else:
			return channelData

	return wrapper_check_file_size_channel

def import_ibw_data(
	importParameter: ImportParameter,
) -> :
	"""

	"""
	# Import required data.
	measurementData = import_ibw_measurement(
		importParameter.folderPathMeasurementData,
	)
	# Import optional data.
	imageData = import_ibw_image(
		importParameter.filePathImage,
		measurementData.size
	)
	channelData = import_channel(
		importParameter.filePathChannel,
		measurementData.size
	)

	return ImportedData(
		measurementData,
		imageData,
		channelData
	)

def import_ibw_measurement(
	folderPathMeasurementData: str
) -> MeasurementData:
	"""
	"""
	folderName = get_folder_name(
		folderPathMeasurementData
	)
	size = get_data_size(
		folderPathMeasurementData
	)
	approachCurves, retractCurves = import_ibw_curves(
		folderPathMeasurementData
	)

	return MeasurementData(
		folderName,
		size,
		approachCurves,
		retractCurves
	)

def get_folder_name(folderPathMeasurementData: str) -> str:
	"""

	Parameters
	----------
	folderPathMeasurementData : str
		Filepath to the data dictionary.

	Returns
	-------
	folderName : str

	"""
	return os.path.basename(folderPathMeasurementData)

def get_data_size(folderPathMeasurementData: str) -> Tuple[int, int]:
	"""

	Parameters
	----------
	folderPathMeasurementData : str

	Returns
	-------
	size : tuple

	"""
	numberOfLines = len(
		os.listdir(folderPathMeasurementData)
	)
	folderPathFirstLine = os.path.join(
		folderPathMeasurementData, 
		os.listdir(folderPathMeasurementData)[0]
	)
	numberOfPoints = len(
		os.listdir(folderPathFirstLine)
	) / 2

	return numberOfLines, numberOfPoints

def import_ibw_curves(
	folderPathMeasurementData: str
) -> Tuple[List[ForceDistanceCurve]]:
	"""
	"""
	ibwDataFiles = get_data_file_paths_in_folder(
		folderPathMeasurementData,
		"**/*.ibw"
	)

	approachCurves = []
	retractCurves = []

	for i in range(0, len(dataFiles), 2):
		piezo = load_ibw_curve_data(dataFiles[i+1])
		deflection = load_ibw_curve_data(dataFiles[i])

		piezo = remove_invalid_values(piezo)
		deflection = remove_invalid_values(deflection)

		approachCurve, retractCurve = split_curve(
			piezo, 
			deflection
		)
		
		approachCurves.append(approachCurve)
		retractCurves.append(retractCurve)

	return approachCurves, retractCurves

def get_data_file_paths_in_folder(
	folderPath: str,
	fileExtension: str
) -> List[str]:
	"""
	"""
	return sorted(
		glob.glob(
			os.path.join(folderPath, fileExtension)
		)
	)

def load_ibw_curve_data(
	filePathCurveData: str
) -> np.ndarray:
	"""

	"""
	try:
		curveData = loadibw(filePathCurveData)["wave"]["wData"]
	except ValueError as e: 
		raise UnableToReadMeasurementFileError("") from e
	else:
		return np.asarray(curveData)

def remove_invalid_values(
	curveData: np.ndarray
) -> np.ndarray:
	"""
	"""
	return curveData[~np.isnan(curveData)]

def split_curve(
	piezo: np.ndarray, 
	deflection: np.ndarray
) -> Tuple[ForceDistanceCurve, ForceDistanceCurve]:
	"""
	Split measurement curve into an approach and retract part.

	Parameters
	----------
	piezo : np.ndarray
		X values of the current curve.
	deflection : np.ndarray
		Y values of the current curve.

	Returns
	-------
	approachCurve : ForceDistanceCurve

	retractCurve : ForceDistanceCurve

	"""
	indexMaximumPiezo = np.argmax(piezo)
	
	approachPiezo = piezo[:indexMaximumPiezo]
	approachDeflection = deflection[:indexMaximumPiezo]
	
	retractPiezo = np.flip(piezo[indexMaximumPiezo :], 0)
	retractDeflection = np.flip(deflection[indexMaximumPiezo :], 0)

	approachCurve = ForceDistanceCurve(
		approachPiezo, 
		approachDeflection
	)
	retractCurve = ForceDistanceCurve(
		retractPiezo, 
		retractDeflection
	)

	return approachCurve, retractCurve

def import_ibw_image(
	filePathImage: str,
	measurementDataSize: Tuple[int]
) -> ImageData:
	"""
	Import an optional image file.
	
	Parameters
	----------
	filePathImage : str
		Contains the selected import parameters and options.
	measurementDataSize : tuple
		Function to show the import progress.

	Returns
	-------
	ImageData : ImageData
		Contains the image data.

	Raises
	------

	"""
	try:
		imageData = loadibw(importParameters.filePathImage)
		imageDataNote = re.split(r'[\r:]', imageData['wave']['note'].decode("utf-8", errors="replace"))
		imageChannelData = np.flip(np.rot90(np.asarray(imageData["wave"]["wData"]), 3), 1)
	except ValueError as e:
		raise UnableToReadImageFileError("Cant read image data!") from e
	else:
		imageSize = (
			imageData['wave']['wave_header']['nDim'][1],
			imageData['wave']['wave_header']['nDim'][0]
		)
		
		return ImageData(
			size=imageSize,
			fss=imageDataNote[imageDataNote.index("FastScanSize")+1],
			sss=imageDataNote[imageDataNote.index("SlowScanSize")+1],
			xOffset=imageDataNote[imageDataNote.index("XOffset")+1],
			yOffset=imageDataNote[imageDataNote.index("YOffset")+1],
			springConstant=imageDataNote[imageDataNote.index("SpringConstant")+1],
			channelHeight=imageChannelData[:, :, 0],
			channelAdhesion=imageChannelData[:, :, 1]
		)