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
	Check that the size of the measurement data 
	matches that of the image.
	"""
	@functools.wraps(function)
	def wrapper_check_file_size_image(*args, **kwargs):
		imagedData = function(*args, **kwargs)
		measurementDataSize = args[1]
		if measurementDataSize != imagedData.size:
			raise WrongImageSizeError(
				"The image size does not match the " 
				"size of the measurement data."
			)
		else:
			return imagedData

	return wrapper_check_file_size_image

def decorator_check_file_size_channel(function):
	"""
	Check that the size of the measurement data 
	matches that of the channel.
	"""
	@functools.wraps(function)
	def wrapper_check_file_size_image(*args, **kwargs):
		channelData = function(*args, **kwargs)
		measurementDataSize = args[1]
		if measurementDataSize != channelData.size:
			raise WrongChannelSizeError(
				"The channel size does not match the "
				"size of the measurement data."
			)
		else:
			return channelData

	return wrapper_check_file_size_channel

def import_ibw_data(
	importParameter: ImportParameter,
) -> ImportedData:
	"""
	Import measurement data in the .ibw file format.

	Parameters
	----------
	importParameter : ImportParameter
		

	Returns
	-------
	importedData : ImportedData

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
		Path to the data folder.

	Returns
	-------
	folderName : str
		Basename of the folder path.
	"""
	return os.path.basename(folderPathMeasurementData)

def get_data_size(folderPathMeasurementData: str) -> Tuple[int, int]:
	"""


	Parameters
	----------
	folderPathMeasurementData : str
		Path to the data folder.

	Returns
	-------
	size : tuple
		The number of data points as the width and height 
		of the measurement grid.
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
	------

	"""
	imageData = loadibw(importParameters.filePathImage)

	imageSize = get_image_size(imageData)
	imageDataNote = get_image_data_note(imageData)
	imageChannelData = get_image_channel_data(imageData)

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

def get_image_size(
	imageData
) -> Tuple[int]:
	"""
	"""
	try:
		imageSize = (
			imageData['wave']['wave_header']['nDim'][1],
			imageData['wave']['wave_header']['nDim'][0]
		)
	except ValueError as e:
		raise UnableToReadImageFileError(
			"Can't read image data size. Unable to find" 
			"'wave|wave_header' key in the image file."
		) from e
	else:
		return imageSize

def get_image_data_note(
	imageData
) -> None:
	"""
	"""
	try:
		imageDataNote = re.split(
			r'[\r:]', imageData['wave']['note'].decode("utf-8", errors="replace")
		)
	except ValueError as e:
		raise UnableToReadImageFileError(
			"Can't read image data note. Unable to find" 
			"'wave|note' key in the image file."
		) from e
	else:
		return imageDataNote

def get_image_channel_data(
	imageData
) -> None:
	"""
	"""
	try:
		imageChannelData = np.flip(
			np.rot90(
				np.asarray(imageData["wave"]["wData"]), 
				3
			), 
			1
		)
	except ValueError as e:
		raise UnableToReadImageFileError(
			"Can't read image channel data. Unable to find" 
			"'wave|wData' key in the image file."
		) from e
	else:
		return imageChannelData

def import_ibw_channel(

) -> None: 
	"""
	"""
	pass