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
from typing import Dict, Tuple, List

import h5py
import numpy as np

import data_processing.named_tuples as nt

def import_hdf5_data(
	importParameter: nt.ImportParameter,
) -> Dict:
	"""
	Import data in the .hdf5 file format.

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
	importedData["measurementData"] = import_hdf5_measurement(
		importParameter.filePathData,
	)

	# Import optional data.
	if importParameter.filePathImage:
		pass

	if importParameter.filePathChannel:
		pass

	return importedData

def import_hdf5_measurement(
	filePathData: str
) -> nt.MeasurementData:
	"""
	Import measurement data in the .hdf5 file format.

	Parameters
	----------
	filePathData : str
		Path to the data folder.

	Returns
	-------
	measurementData : MeasurementData
		Cotains the name, size, approach and retract curves
		of the measurement.
	"""
	measurementData = import_hdf5_file(
		filePathData
	)
	fileName = get_file_name(
		filePathData
	)
	size = get_data_size(
		measurementData
	)
	approachCurves, retractCurves = arrange_force_distance_curves(
		measurementData
	)

	return nt.MeasurementData(
		fileName,
		size,
		approachCurves,
		retractCurves
	)
	
def import_hdf5_file(filePathData: str) -> np.array:
	"""
	Load the data of a single hdf5 file.

	Parameters
	----------
	filePathData : str
		Path to the measurement file

	Returns
	-------
	measurementData : np.ndarray
		Data of the imported measurement.
	"""
	dataFile = h5py.File(filePathData, 'r')
	measurementData = np.array(dataFile["data"]).transpose(1, 0)
	measurementData = np.array(measurementData.tolist())

	return measurementData

def get_file_name(filePathData: str) -> str: 
	"""
	Get the name of a data file from the 
	associated file path.

	Parameters
	----------
	filePathData : str
		Path to the measurement file

	Returns
	-------
	fileName : str
		Name of the measurement file without extension.
	"""
	return filePathData.rsplit("/",1)[1].split(".", 1)[0]

def get_data_size(measurementData: np.ndarray) -> Tuple[int]:
	"""
	Get the size of measurment grid of the imported
	data.

	Parameters
	----------
	measurementData : np.ndarray
		The imported measurement data.

	Returns
	-------
	measurementSize : tuple[int]
		Size of the measurement grid.
	"""

	measurementSize = int(np.sqrt(measurementData.shape[0]))
	
	return measurementSize, measurementSize

def arrange_force_distance_curves(
	measurementData: np.ndarray
) -> Tuple[List[nt.ForceDistanceCurve]]:
	"""
	Arrange the measurement data into the format
	SOFA needs.

	Parameters
	----------
	measurementData : np.ndarray
		The imported measurement data.

	Returns
	-------
	approachCurves : list[nt.ForceDistanceCurve]
		The approach curves of the imported measurement.
	retractCurves : list[nt.ForceDistanceCurve]
		The retract curves of the imported measurement.
	"""
	signFactor = 1e-09
	piezoValuesApproach = np.flip(measurementData[:,:,0], 1) * signFactor
	deflectionValuesApproach = measurementData[:,:,1] * signFactor

	approachCurves = [
		nt.ForceDistanceCurve(
			approachPiezo, 
			approachDeflection
		)
		for approachPiezo, approachDeflection
		in zip(piezoValuesApproach, deflectionValuesApproach)
	]
	retractCurves = []

	return approachCurves, retractCurves