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

import numpy as np
import pandas as pd

def setup_output_folder(
	folderPath: str,
	folderName: str
) -> str:
	"""
	Set up a folder to store the data.
	
	Parameters
	----------
	folderPath : str
		.
	folderName : str

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

	Parameters
	----------
	forceVolume : ForceVolume
	pathOutputFolder : str
	"""
	pass

def export_to_xlsx(
	forceVolume, 
	pathOutputFolder: str
) -> None:
	"""

	Parameters
	----------
	forceVolume : ForceVolume
	pathOutputFolder : str
	"""
	generalDataFrame = pd.DataFrame(
		dataHandler.generalData.copy(),
		index=[0]
	)

	curveXValues, curveYValues = split_corrected_curves(dataHandler.curveData["correctedCurves"])
	curveXValuesDataframe = pd.DataFrame(
		data=curveXValues,
		index=np.arange(curveXValues.shape[0]).tolist(),
		columns=np.arange(curveXValues.shape[1]).tolist()
	)
	curveYValuesDataframe = pd.DataFrame(
		data=curveYValues,
		index=np.arange(curveYValues.shape[0]).tolist(),
		columns=np.arange(curveYValues.shape[1]).tolist()
	)

	averageDataFrames = {}
	for name, data in dataHandler.averageData.items():
		averageDataFrames[name] = pd.DataFrame(
			data=data,
			index=[i for i in range(len(data))]
		)

	channelDataFrames = {} 
	for channelName, channelData in dataHandler.channelData.items():
		channelDataFrames[channelName] = pd.DataFrame(
			data= channelData["sourceData"],
			index= np.arange(channelData["sourceData"].shape[0]).tolist(),
			columns= np.arange(channelData["sourceData"].shape[1]).tolist()
		)

	outPutFilePath = os.path.join(outputFolder, "data.xlsx")
	with pd.ExcelWriter(outPutFilePath) as writer:  
		generalDataFrame.to_excel(writer, sheet_name='General Data')

		curveXValuesDataframe.to_excel(writer, sheet_name='Curves X Values')
		curveYValuesDataframe.to_excel(writer, sheet_name='Curves Y Values')

		for name, data in channelDataFrames.items():
			data.to_excel(writer, sheet_name=name)
		
		for channelDataFrameName, channelDataFrame in channelDataFrames.items():
			channelDataFrame.to_excel(writer, sheet_name=channelDataFrameName)

def export_to_txt(
	forceVolume, 
	pathOutputFolder: str
) -> None:
	"""

	Parameters
	----------
	forceVolume : ForceVolume
	pathOutputFolder : str
	"""
	outPutFilePath = os.path.join(outputFolder, "data.txt")
	with open(outPutFilePath, 'w', newline='') as outputDatafileTxt:
		# Save general data.
		outputDatafileTxt.write("General data: \n")
		for name, data in dataHandler.generalData.items():
			outputDatafileTxt.write(name + str(data) + "\n")

		# Save channel data.
		outputDatafileTxt.write("Channel data: \n")
		for name, data in dataHandler.channelData.items():
			outputDatafileTxt.write(name + ": \n")
			np.savetxt(outputDatafileTxt, data, fmt="%1.8e")
			outputDatafileTxt.write("\n")	

		# Save curve data.
		outputDatafileTxt.write("Curve data: \n")
		for curve in dataHandler.curveData["correctedCurves"]:
			np.savetxt(
				outputDatafileTxt,
				np.asarray(curve),
				fmt="%1.8e"
			)

		# Save average data.
		outputDatafileTxt.write("Channel data: \n")
		for name, data in dataHandler.averageData.items():
			outputDatafileTxt.write(name + ": \n")
			np.savetxt(outputDatafileTxt, data, fmt="%1.8e")
			outputDatafileTxt.write("\n")	

def export_plots(
	forceVolume, 
	pathOutputFolder: str
) -> None:
	"""

	Parameters
	----------
	forceVolume : ForceVolume
	pathOutputFolder : str
	"""

	linePlotFilePath = os.path.join(outputFolder, "lineplot")
	dataHandler.linePlotParameters["holder"].figure.savefig(
		linePlotFilePath, dpi=300
	)

	heatmapFilePath = os.path.join(outputFolder, "heatmap")
	dataHandler.heatmapParameters["holder"].figure.savefig(
		heatmapFilePath, dpi=300
	)

	histogramFilePath = os.path.join(outputFolder, "histogram")
	dataHandler.histogramParameters["holder"].figure.savefig(
		histogramFilePath, dpi=300
	)

# Defines all available file types to export.
importFunctions = {
	"csv": export_to_csv,
	"xlsx": export_to_xlsx,
	"txt": export_to_txt
}