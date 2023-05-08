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

import data_processing.custom_exceptions as ce
import data_processing.named_tuples as nt

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
	def wrapper_check_file_size_channel(*args, **kwargs):
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
	importParameter: nt.ImportParameter,
) -> Dict:
	"""
	Import data in the .ibw file format.

	Parameters
	----------
	importParameter : nt.ImportParameter
		Contains the path to the measurement data and 
		if selected the paths to additional image or
		channel files. 

	Returns
	-------
	importedData : dict
		Combined data of all the imported data files.
	"""
	importedData = {}

	# Import required data.
	importedData["measurementData"] = import_ibw_measurement(
		importParameter.folderPathMeasurementData,
	)

	# Import optional data.
	if importParameter.filePathImage:
		importedData["imageData"] = import_ibw_image(
			importParameter.filePathImage,
			measurementData.size
		)

	if importParameter.filePathChannel:
		importedData["importedChannelData"] = import_channel(
			importParameter.filePathChannel,
			measurementData.size
		)

	return importedData

def import_ibw_measurement(
	folderPathMeasurementData: str
) -> nt.MeasurementData:
	"""
	Import measurement data in the .ibw file format.

	Parameters
	----------
	folderPathMeasurementData : str
		Path to the data folder.

	Returns
	-------
	measurementData : MeasurementData
		Cotains the name, size, approach and retract curves
		of the measurement.
	"""
	folderName = get_folder_name(
		folderPathMeasurementData
	)
	size = get_data_size(
		folderPathMeasurementData
	)
	approachCurves, retractCurves = import_ibw_measurement_curves(
		folderPathMeasurementData
	)

	return nt.MeasurementData(
		folderName,
		size,
		approachCurves,
		retractCurves
	)

def get_folder_name(folderPathMeasurementData: str) -> str:
	"""
	Get the name of a folder from it's path.

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
	Get the size of the measurement grid.

	Parameters
	----------
	folderPathMeasurementData : str
		Path to the data folder.

	Returns
	-------
	size : tuple
		The number of data points as the width (fast scan size) 
		and height (slow scan size) of the measurement grid.
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

def import_ibw_measurement_curves(
	folderPathMeasurementData: str
) -> Tuple[List[nt.ForceDistanceCurve]]:
	"""
	Import all measurement curves from a given folder.

	Parameters
	----------
	folderPathMeasurementData : str
		Path to the data folder.

	Returns
	-------
	approachCurves : list[nt.ForceDistanceCurve]
		The approach curve of every imported measurement
		curve.
	retractCurves : list[nt.ForceDistanceCurve]
		The retract curve of every imported measurement
		curve.
	"""
	dataFilePathsPiezo = get_data_file_paths_in_folder(
		folderPathMeasurementData,
		"**/*ZSnsr.ibw"
	)
	dataFilePathsDeflection = get_data_file_paths_in_folder(
		folderPathMeasurementData,
		"**/*Defl.ibw"
	)

	approachCurves = []
	retractCurves = []

	for dataFilePathPiezo, dataFilePathDeflection in zip(dataFilePathsPiezo, dataFilePathsDeflection):
		approachCurve, retractCurve = import_ibw_measurement_curve(
			dataFilePathPiezo,
			dataFilePathDeflection
		)
		
		approachCurves.append(approachCurve)
		retractCurves.append(retractCurve)

	return approachCurves, retractCurves

def get_data_file_paths_in_folder(
	folderPath: str,
	fileType: str
) -> List[str]:
	"""
	Get the file paths of all files in a directory with the 
	specified file type and sort them alphabetically.

	Parameters
	----------
	folderPath : str
		Path to the data folder.
	fileType : str
		Name and extension of the wanted file type.

	Returns
	-------
	dataFilePaths : list[str]
		Sorted file paths of all data files in the given folder
		that matched the file type.
	"""
	return sorted(
		glob.glob(
			os.path.join(folderPath, fileType)
		)
	)

def import_ibw_measurement_curve(
	dataFilePathPiezo: str,
	dataFilePathDeflection: str
) -> Tuple[nt.ForceDistanceCurve]:
	"""
	Import a single measurement curve, remove invalid values
	and split it into an approach and retract part.

	Parameters
	----------
	dataFilePathPiezo : str
		Path to the piezo data file.
	dataFilePathDeflection : str
		Path to the deflection data file.

	Returns
	-------
	approachCurve : nt.ForceDistanceCurve
		Approach curve of the measurement curve with
		piezo (x) and deflection (y) values.
	retractCurve : nt.ForceDistanceCurve
		Retract curve of the measurement curve with
		piezo (x) and deflection (y) values.
	"""
	piezo = load_ibw_measurement_curve_file(
		dataFilePathPiezo
	)
	deflection = load_ibw_measurement_curve_file(
		dataFilePathDeflection
	)

	validPiezo = remove_invalid_values(piezo)
	validDeflection = remove_invalid_values(deflection)

	approachCurve, retractCurve = split_curve(
		validPiezo, 
		validDeflection
	)

	return approachCurve, retractCurve

def load_ibw_measurement_curve_file(
	filePathCurveData: str
) -> np.ndarray:
	"""
	Load the data from a .ibw measurement file.
	
	Parameters
	----------
	filePathCurveData : str
		Path to the data file.

	Returns
	-------
	curveData : np.ndarray
		Piezo (x) or deflection (y) values of a
		measurement curve.

	Raises
	------
	ce.UnableToReadMeasurementFileError : ce.ImportError
		If the measurement file structure is different 
		and the expected keys are missing.
	"""
	try:
		curveData = loadibw(filePathCurveData)["wave"]["wData"]
	except ValueError as e: 
		raise ce.UnableToReadMeasurementFileError(
			"Unable to read measurement file. Expected "
			"'wave|wData' key does not exist. For further "
			"information see the docs or "
			"data_processing/import_data.py."
		) from e
	else:
		return np.asarray(curveData)

def remove_invalid_values(
	curveData: np.ndarray
) -> np.ndarray:
	"""
	Remove potential nan values from raw measurement data.

	Parameters
	----------
	curveData : np.ndarry
		Raw measurement data which might contain nan values.

	Returns
	-------
	validCurveData : np.ndarry
		Cleaned data without nan values.
	"""
	return curveData[~np.isnan(curveData)]

def split_curve(
	piezo: np.ndarray, 
	deflection: np.ndarray
) -> Tuple[nt.ForceDistanceCurve]:
	"""
	Split a measurement curve into it's approach and retract part.

	Parameters
	----------
	piezo : np.ndarray
		X values of the measurement curve.
	deflection : np.ndarray
		Y values of the measuremnet curve.

	Returns
	-------
	approachCurve : ForceDistanceCurve
		Approach part of the measurement curve from 
		the start point to the maximum piezo value.
	retractCurve : ForceDistanceCurve
		Retract part of the measurement curve from 
		the maximum piezo value back to the start point.
	"""
	indexMaximumPiezo = np.argmax(piezo)
	
	approachPiezo = piezo[:indexMaximumPiezo]
	approachDeflection = deflection[:indexMaximumPiezo]
	
	retractPiezo = np.flip(piezo[indexMaximumPiezo :], 0)
	retractDeflection = np.flip(deflection[indexMaximumPiezo :], 0)

	approachCurve = nt.ForceDistanceCurve(
		approachPiezo, 
		approachDeflection
	)
	retractCurve = nt.ForceDistanceCurve(
		retractPiezo, 
		retractDeflection
	)

	return approachCurve, retractCurve

@decorator_check_file_size_image
def import_ibw_image(
	filePathImage: str,
	measurementDataSize: Tuple[int]
) -> nt.ImageData:
	"""
	Import an optional image file in the .ibw file format.
	
	Parameters
	----------
	filePathImage : str
		Path to the image file.
	measurementDataSize : tuple
		Grid size of the imported measurement data.

	Returns
	-------
	ImageData : ImageData
		Contains meta data from the measurement and
		two pre processed channels.
	"""
	imageData = loadibw(importParameters.filePathImage)

	imageSize = get_image_size(imageData)
	imageDataNote = get_image_data_note(imageData)
	imageChannelData = get_image_channel_data(imageData)
	adjustedImageChannelData = adjust_image_channel_data(imageChannelData)

	return nt.ImageData(
		size=imageSize,
		fss=imageDataNote[imageDataNote.index("FastScanSize")+1],
		sss=imageDataNote[imageDataNote.index("SlowScanSize")+1],
		xOffset=imageDataNote[imageDataNote.index("XOffset")+1],
		yOffset=imageDataNote[imageDataNote.index("YOffset")+1],
		springConstant=imageDataNote[imageDataNote.index("SpringConstant")+1],
		channelHeight=adjustedImageChannelData[:, :, 0],
		channelAdhesion=adjustedImageChannelData[:, :, 1]
	)

def get_image_size(
	imageData: Dict
) -> Tuple[int]:
	"""
	Get the size of the image to see if it fits 
	the size of the imported measurement data.

	Parameters
	----------
	imageData : dict
		Data of the image file.

	Returns
	-------
	imageSize : tuple(int)
		Width and height of the measurement data grid.

	Raises
	------
	ce.UnableToReadImageFileError : ce.ImportError
		If the image file structure is different 
		and the expected keys are missing.
	"""
	try:
		imageSize = (
			imageData['wave']['wave_header']['nDim'][1],
			imageData['wave']['wave_header']['nDim'][0]
		)
	except ValueError as e:
		raise UnableToReadImageFileError(
			"Can't read image data size. Unable to find " 
			"'wave|wave_header' key in the image file. "
			"For further information see the docs or "
			"data_processing/import_data.py."
		) from e
	else:
		return imageSize

def get_image_data_note(
	imageData: Dict
) -> List[str]:
	"""
	Decode the meta data from the image, from binary
	to string.

	Parameters
	----------
	imageData : dict
		Data of the image file.

	Returns
	-------
	imageDataNote : list(str)
		List of meta data entries with their 
		identifiers and data.		

	Raises
	------
	ce.UnableToReadImageFileError : ce.ImportError
		If the image file structure is different 
		and the expected keys are missing.
	"""
	try:
		imageDataNote = re.split(
			r'[\r:]', 
			imageData['wave']['note'].decode("utf-8", errors="replace")
		)
	except ValueError as e:
		raise UnableToReadImageFileError(
			"Can't read image data note. Unable to find " 
			"'wave|note' key in the image file. "
			"For further information see the docs or "
			"data_processing/import_data.py."
		) from e
	else:
		return imageDataNote

def get_image_channel_data(
	imageData: Dict
) -> np.ndarray:
	"""
	Import the pre processed channel data.

	Parameters
	----------
	imageData : dict
		Data of the image file.

	Returns
	-------
	imageChannelData : np.ndarray
		Pre processed height and adhesion
		channel.

	Raises
	------
	ce.UnableToReadImageFileError : ce.ImportError
		If the image file structure is different 
		and the expected keys are missing.
	"""
	try:
		imageChannelData = np.asarray(imageData["wave"]["wData"])
	except ValueError as e:
		raise UnableToReadImageFileError(
			"Can't read image channel data. Unable to find " 
			"'wave|wData' key in the image file. "
			"For further information see the docs or "
			"data_processing/import_data.py."
		) from e
	else:
		return imageChannelData

def adjust_image_channel_data(
	imageChannelData: np.ndarray
) -> np.ndarray:
	"""
	Adjust the orientation of the pre processed image
	channel to match the orientation of the channels
	calculated from the measurement data.

	Parameters
	----------
	imageChannelData : np.ndarray
		Pre processed height and adhesion
		channel.

	Returns
	-------
	adjustedImageChannelData : np.ndarray
		Pre processed height and adhesion
		channel with adjusted orientation.
	"""
	return np.flip(
		np.rot90(
			imageChannelData, 
			3
		), 
		1
	)

@decorator_check_file_size_channel
def import_channel(
	filePathChannel: str,
	measurementDataSize: Tuple[int]
) -> nt.ImportedChannelData: 
	"""
	Import an additional pre processed channel.

	Parameters
	----------
	filePathChannel : str
		Path to the channel file

	measurementDataSize : tuple[int]
		Grid size of the imported measurement data.

	Returns
	-------
	channelData : nt.ImportedChannelData
		Name, size and data of the imported channel.
	"""
	pass


# Defines all available import options.
importFunctions = {
	".ibw": (import_ibw_data, "*.ibw"),
}