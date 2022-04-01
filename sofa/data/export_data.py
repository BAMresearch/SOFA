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
import platform
import numpy as np
import json
import pandas as pd
from pylatex import (Document, Section, NewPage, Center, LineBreak, HFill, LargeText)
from pylatex import Figure as latexFig
from pylatex.utils import italic, bold

def export_data(
	dataHandler,
	exportParameters,
	progressbar,
	progressbarLabel
):
	"""
	"""
	progressbar.start()

	outputFolder = setup_output_folder(
		exportParameters,
		dataHandler.generalData["filename"]
	)

	if exportParameters.exportToSofa:
		export_to_sofa(dataHandler, outputFolder)
		progressbarLabel.set("Exporting to SOFA")

	if exportParameters.exportToTex:
		export_to_tex(dataHandler, outputFolder)
		progressbarLabel.set("Exporting to Tex")

	if exportParameters.exportToTxt:
		export_to_txt(dataHandler, outputFolder)
		progressbarLabel.set("Exporting to Txt")

	if exportParameters.exportToHdf5:
		export_to_hdf5(dataHandler, outputFolder)
		progressbarLabel.set("Exporting to HDF5")

	if exportParameters.exportToExcel:
		export_to_excel(dataHandler, outputFolder)
		progressbarLabel.set("Exporting to Excel")

	if exportParameters.exportPlots:
		export_plots(dataHandler, outputFolder)
		progressbarLabel.set("Exporting plots")

	progressbar.stop()

def setup_output_folder(exportParameters, filename):
	"""
	"""
	outputFolderPath = os.path.join(
		exportParameters.folderPath, 
		"SofaData", 
		exportParameters.folderName,
		filename
	)
	os.makedirs(outputFolderPath, exist_ok=True)

	return create_session_folder(outputFolderPath)
	
def create_session_folder(currentFolder):
	""".

	Parameters:
		currentFolder(string): .
	"""
	pathSessionNumberFile = os.path.join(currentFolder, ".sessionNumber")

	sessionNumber = get_session_number(pathSessionNumberFile)

	path_session_folder = os.path.join(
		currentFolder,
		"Session" + sessionNumber
	)
	os.mkdir(path_session_folder)

	return path_session_folder

def get_session_number(pathSessionNumberFile):
	"""
	"""
	if os.path.exists(pathSessionNumberFile):
		with open(pathSessionNumberFile, 'r+') as fileSessionNumber:
			sessionNumber = int(fileSessionNumber.read(3)) + 1
		with open(pathSessionNumberFile, 'r+') as fileSessionNumber:
			fileSessionNumber.write(str(sessionNumber))
	else:
		with open(pathSessionNumberFile, 'w') as fileSessionNumber:
			fileSessionNumber.write('1')
			sessionNumber = 1

		if platform.system() == "Windows":
			os.system("attrib +h " + pathSessionNumberFile)

	return str(sessionNumber)

def export_to_sofa(
	dataHandler, 
	outputFolder, 
	fileName="data.json", 
	hidden=False
):
	"""
	"""
	channelData = {}
	for channelName, channel in dataHandler.channelData.items():
		channelData[channelName]["data"] = channel["data"].tolist()
		channelData[channelName]["sourceData"] = channel["sourceData"].tolist()

	curveData = {}


	linePlotParameters = {
		"showInactive": dataHandler.linePlotParameters["showInactive"],
		"displayAverage": dataHandler.linePlotParameters["displayAverage"],
		"displayErrorbar": dataHandler.linePlotParameters["displayErrorbar"]
	}

	heatmapParameters = {
		"currentChannel": dataHandler.heatmapParameters["currentChannel"].get(),
		"selectedArea": dataHandler.heatmapParameters["selectedArea"],
		"mappedIndices": dataHandler.heatmapParameters["mappedIndices"].tolist()
	}

	histogramParameters = {
		"currentChannel": dataHandler.histogramParameters["currentChannel"].get(),
		"zoom": dataHandler.histogramParameters["zoom"].get(),
		"numberOfBins": dataHandler.histogramParameters["numberOfBins"].get()
	}

	histogramData = {}

	sofaData = {
		"inactiveDataPoints": dataHandler.inactiveDataPoints.copy(),
		"generalData": dataHandler.generalData.copy(),
		"curveData": channelData,
		"averageData": averageData,
		"channelData": curveData,
		"linePlotParameters": linePlotParameters,
		"heatmapParameters": heatmapParameters,
		"histogramParameters": histogramParameters,
		"histogramData": histogramData,
	}

	outPutFilePath = os.path.join(outputFolder, fileName)

	with open(outPutFilePath, 'w+', newline='') as outputDatafileJSON:
		json.dump(sofaData, outputDatafileJSON)

	if hidden == True and platform.system() == "Windows":
		os.system("attrib +h " + outPutFilePath)

def export_to_tex(dataHandler, outputFolder):
	"""
	"""
	pass

def export_to_txt(dataHandler, outputFolder):
	"""
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

def export_to_hdf5(dataHandler, outputFolder):
	"""
	"""
	pass

def export_to_excel(dataHandler, outputFolder):
	"""
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

def export_plots(dataHandler, outputFolder):
	"""
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

def split_corrected_curves(correctedCurves):
	""""""
	xValues = []
	yValues = []

	for curve in correctedCurves:
		xValues.append(curve[0])
		yValues.append(curve[1])

	return xValues, yValues
