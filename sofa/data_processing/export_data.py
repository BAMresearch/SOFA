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
import os
from typing import List, Tuple, Dict
import functools

import numpy as np
import pandas as pd

import data_processing.named_tuples as nt

def decorator_check_average(function):
	"""Check if average data exists."""
	@functools.wraps(function)
	def wrapper_check_average(*args, **kwargs):
		forceVolume = args[0]
		if hasattr(forceVolume, "average"):
			return function(*args, **kwargs)
		else: 
			return create_data_frame_empty_average_data()

	return wrapper_check_average

def setup_output_folder(
	folderPath: str,
	folderName: str
) -> str:
	"""
	Set up a folder to store the data in the
	desired location.
	
	Parameters
	----------
	folderPath : str
		.Specified location where the folder is created.
	folderName : str
		Specified name of the output folder.

	Returns
	-------
	pathOutputFolder : str
		Path of the output folder.
	"""
	outputFolderPath = os.path.join(
		folderPath, 
		folderName
	)
	os.makedirs(outputFolderPath, exist_ok=True)

	return outputFolderPath

def export_to_csv(
	forceVolume, 
	pathOutputFolder: str, 
) -> None:
	"""
	Export the processed data of the imported 
	force volume to the .csv file format.

	Parameters
	----------
	forceVolume : ForceVolume
		Contains the raw and calculated data from the 
		imported measurement.
	pathOutputFolder : str
		Path to the folder in which the data will be stored.
	"""
	dataFramesForceVolume = get_force_volume_data(forceVolume)
	dataFrameCombinedCurveData = combine_data_frames(
		[
			dataFramesForceVolume.rawCurves,
			dataFramesForceVolume.correctedCurves,
			dataFramesForceVolume.averageData,
		]
	)

	write_csv_file(
		dataFramesForceVolume.metaData,
		os.path.join(pathOutputFolder, "meta_data.csv")
	)
	write_csv_file(
		dataFrameCombinedCurveData,
		os.path.join(pathOutputFolder, "curve_data.csv")
	)
	write_csv_file(
		dataFramesForceVolume.channelData,
		os.path.join(pathOutputFolder, "channel_data.csv")
	)

def export_to_xlsx(
	forceVolume, 
	pathOutputFolder: str
) -> None:
	"""
	Export the processed data of the imported 
	force volume to the .xlsx file format.

	Parameters
	----------
	forceVolume : ForceVolume
		Contains the raw and calculated data from the 
		imported measurement.
	pathOutputFolder : str
		Path to the folder in which the data will be stored.
	"""
	dataFramesForceVolume = get_force_volume_data(forceVolume)
	outPutFilePath = os.path.join(pathOutputFolder, "data.xlsx")
	
	with pd.ExcelWriter(outPutFilePath) as writer:  
		dataFramesForceVolume.metaData.to_excel(writer, sheet_name='Meta Data')
		dataFramesForceVolume.rawCurves.to_excel(writer, sheet_name='Raw Curves')
		dataFramesForceVolume.correctedCurves.to_excel(writer, sheet_name='Corrected Curves')
		dataFramesForceVolume.averageData.to_excel(writer, sheet_name='Average Data')
		dataFramesForceVolume.channelData.to_excel(writer, sheet_name='Channel Data')

def export_plots(
	holderLinePlot,
	holderHeatmap,
	holderHistogram,
	pathOutputFolder: str
) -> None:
	"""
	Export the plots of the imported force volume.

	Parameters
	----------
	plotHolders : dict
		Contains the holders of every figure in the main window
		of SOFA.
	pathOutputFolder : str
		Path to the folder in which the plots will be stored.
	"""
	save_figure(
		holderLinePlot,
		os.path.join(pathOutputFolder, "lineplot")
	)
	save_figure(
		holderHeatmap,
		os.path.join(pathOutputFolder, "heatmap")
	)
	save_figure(
		holderHistogram,
		os.path.join(pathOutputFolder, "histogram")
	)

def get_force_volume_data(
	forceVolume
) -> nt.DataFramesForceVolume:
	"""
	Convert the data of a force volume to panda dataframes
	to simpliy the export of the data.

	Parameters
	----------
	forceVolume : ForceVolume
		Contains the raw and calculated data from the 
		imported measurement.

	Returns
	-------
	dataFramesForceVolume : nt.DataFramesForceVolume
		Data of the force volume cached in different
		distinct panda data frames.
	"""
	dataFrameMetaData = create_data_frame_metadata(forceVolume)
	dataFramerawCurves = create_data_frame_raw_curves(forceVolume.forceDistanceCurves)
	dataFrameCorrectedCurves = create_data_frame_corrected_curves(forceVolume.forceDistanceCurves)
	dataFrameAverageData = create_data_frame_average_data(forceVolume)
	dataFrameChannelData = create_data_frame_channel_data(forceVolume.channels)

	return nt.DataFramesForceVolume(
		metaData=dataFrameMetaData,
		rawCurves=dataFramerawCurves,
		correctedCurves=dataFrameCorrectedCurves,
		averageData=dataFrameAverageData,
		channelData=dataFrameChannelData
	)

def create_data_frame_metadata(
	forceVolume
) -> pd.DataFrame:
	"""
	Cache the general data and if imported additional
	data from an image in a pandas dataframe.

	Parameters
	----------
	forceVolume : ForceVolume
		Contains the raw and calculated data from the 
		imported measurement.

	Returns
	-------
	dataFrameMetaData : pd.Dataframe
		Contains the name, size and additional data from 
		the measurement, if an image was imported
	"""
	metaData = {
		"name": forceVolume.name,
		"size": forceVolume.size
	} 

	if forceVolume.imageData:
		metaData["fss"] = forceVolume.imageData["fss"]
		metaData["sss"] = forceVolume.imageData["sss"]
		metaData["xOffset"] = forceVolume.imageData["xOffset"]
		metaData["yOffset"] = forceVolume.imageData["yOffset"]
		metaData["springConstant"] = forceVolume.imageData["springConstant"]

	return pd.DataFrame.from_dict(metaData)

def create_data_frame_raw_curves(
	forceDistanceCurves: List
) -> pd.DataFrame:
	"""
	Cache the raw imported measurment data in a 
	pandas dataframe.

	Parameters
	----------
	forceDistanceCurves : list[ForceDistanceCurve]
		All force distance curves in the force volume.

	Returns
	-------
	dataFrameRawCurves : pd.Dataframe
		Contains the data of the imported
		measuremnt curves.
	"""
	rawPiezo = [
		forceDistanceCurve.dataApproachRaw.piezo
		for forceDistanceCurve
		in forceDistanceCurves
	]
	rawDeflection = [
		forceDistanceCurve.dataApproachRaw.deflection
		for forceDistanceCurve
		in forceDistanceCurves
	]
	rawData = np.array([rawPiezo, rawDeflection], dtype=object).transpose()

	return pd.DataFrame(
		rawData,
		columns=["raw piezo", "raw deflection"]
	)

def create_data_frame_corrected_curves(
	forceDistanceCurves: List
) -> pd.DataFrame:
	"""
	Cache the corrected measurment data in a 
	pandas dataframe.

	Parameters
	----------
	forceDistanceCurves : list[ForceDistanceCurve]
		All force distance curves in the force volume.

	Returns
	-------
	dataFrameCorrectedCurves : pd.Dataframe
		Contains the data of the corrected 
		measurement curves.
	"""
	correctedPiezo = [
		forceDistanceCurve.dataApproachCorrected.piezo
		for forceDistanceCurve
		in forceDistanceCurves
		if forceDistanceCurve.couldBeCorrected
	]
	correctedDeflection = [
		forceDistanceCurve.dataApproachCorrected.deflection
		for forceDistanceCurve
		in forceDistanceCurves
		if forceDistanceCurve.couldBeCorrected
	]
	correctedData = np.array([correctedPiezo, correctedDeflection], dtype=object).transpose()

	return pd.DataFrame(
		correctedData,
		columns=["corrected piezo", "corrected deflection"]
	)

@decorator_check_average
def create_data_frame_average_data(
	forceVolume
) -> pd.DataFrame:
	"""
	Cache the the calculated average data in a 
	pandas dataframe.

	Parameters
	----------
	averageForceDistanceCurve : AverageForceDistanceCurve
		Average of the active force distance curve with
		the standard deviation if selected.

	Returns
	-------
	dataFrameAverageData : pd.Dataframe
		Contains the data of the calculated average
		curve.
	"""
	return pd.DataFrame(
		average.averageData.piezo,
		average.averageData.deflection,
		average.standardDeviation,
		columns=[
			"average piezo", 
			"average deflection", 
			"standard deviation"
		]
	) 

def create_data_frame_empty_average_data() -> pd.DataFrame:
	"""
	Create an empty data frame to indicate that 
	no average data as been calculated.

	Returns
	-------
	dataFrameEmptyAverageData : pd.Dataframe
		Empty dataframe with a note that no 
		average data has been calculated.
	"""
	return pd.DataFrame(
		["average data has not been calculated"],
		index=["note"]
	)

def create_data_frame_channel_data(
	channels: List
) -> pd.DataFrame:
	"""
	Cache the flattended data of the calculated 
	channels in a pandas dataframe.

	Parameters
	----------
	channels : list[Channel]
		All channels calculated from the corrected data. 

	Returns
	-------
	dataFrameChannelData : pd.Dataframe
		Contains the data of every calculated channel.
	"""
	channelData = {}

	for channel in channels.values():
		channelData[channel.name] = channel.rawData.flatten()

	return pd.DataFrame.from_dict(channelData)

def combine_data_frames(
	dataFrames: List[pd.DataFrame]
) -> pd.DataFrame:
	"""
	Combine a list of data frames with the same
	shape to a single dataframe, to reduce the 
	number of files created when exporting to 
	.csv file format.

	Parameters
	----------
	dataFrames : list[pd.DataFrame]
		List of data frames with similar shape
		which are combined into one data frame.
	
	Returns
	-------
	comninedDataFrame : pd.DataFrame
		Contains the combined data of the 
		data frames.
	"""
	return pd.concat(
		dataFrames
	)

def write_csv_file(
	dataFrame: pd.DataFrame,
	filePathOutput: str
) -> None:
	"""
	Export the data of a pandas dataframe 
	to the .csv file format.

	Parameters
	----------
	dataFrame : pd.DataFrame
		Data frame which is to be exported.
	filePathOutput : str
		File path where the file is to be saved.
	"""
	dataFrame.to_csv(
		filePathOutput
	)

def save_figure(
	holder,
	filePath: str
) -> None: 
	"""
	Export a single matplotlib figure to the given location.

	Parameters
	----------
	holder : matplotlib.backends.backend_tkagg.FigureCanvasTkAgg
		Interface of a matplotlib figure and a tkinter window.
	filePath : str
		Path in which the figure will be saved.
	"""
	holder.figure.savefig(
		filePath, 
		dpi=300
	)

# Defines all available file types to which the data can be exported.
exportFormats = {
	"csv": export_to_csv,
	"xlsx": export_to_xlsx
}