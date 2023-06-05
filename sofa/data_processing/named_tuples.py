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

from typing import NamedTuple, Tuple, List
from numpy import ndarray
from pandas import DataFrame
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import ttkbootstrap as ttk

# GUI interface
class LinePlotParameters(NamedTuple):
	linked: tk.BooleanVar
	holder: FigureCanvasTkAgg
	plotInactive: bool 
	plotAverage: bool
	plotErrorbar: bool

class HeatmapParameters(NamedTuple): 
	linked: tk.BooleanVar
	holder: FigureCanvasTkAgg
	activeChannel: tk.StringVar

class HistogramParameters(NamedTuple):  
	linked: tk.BooleanVar
	holder: FigureCanvasTkAgg
	activeChannel: tk.StringVar
	zoom: tk.BooleanVar
	numberOfBins: ttk.Entry

class HistogramRestrictionParameters(NamedTuple):
	data: ndarray
	activeData: ndarray
	binValues: List
	indexMinBinValue: int
	indexMaxBinValue: int

# FDC data
class ForceDistanceCurve(NamedTuple): 
	piezo: ndarray
	deflection: ndarray

class ForceDistancePoint(NamedTuple):
	index: int
	piezo: float
	deflection: float

class CoefficientsFitApproachCurve(NamedTuple):
	slope: float
	intercept: float

class ChannelMetadata(NamedTuple):
	endOfZeroline: ForceDistancePoint
	pointOfContact: ForceDistancePoint
	coefficientsFitApproachCurve: CoefficientsFitApproachCurve

class AverageForceDistanceCurve(NamedTuple):
	piezoNonContact: ndarray
	deflectionNonContact: ndarray
	piezoContact: ndarray
	deflectionContact: ndarray
	standardDeviationNonContact: ndarray
	standardDeviationContact: ndarray

class NormedCurves(NamedTuple):
	piezoNonContact: ndarray
	deflectionNonContact: ndarray
	piezoContact: ndarray
	deflectionContact: ndarray

# Data import
class ImportParameter(NamedTuple):
	dataFormat: str
	filePathData: str 
	filePathImage: str 
	filePathChannel: str 
	showPoorCurves: bool

class MeasurementData(NamedTuple):
	folderName: str
	size: Tuple[int]
	approachCurves: List[ForceDistanceCurve]
	retractCurves: List[ForceDistanceCurve]

class ImageData(NamedTuple):
	size: Tuple[int]
	fss: float 
	sss: float
	xOffset: float
	yOffset: float
	springConstant: float
	channelHeight: ndarray
	channelAdhesion: ndarray

class ImportedChannelData(NamedTuple):
	name: str
	size: Tuple[int]
	data: ndarray

# Data export
class ExportParameter(NamedTuple):
	folderPath: str
	folderName: str
	exportToCsv: bool
	exportToXlsx: bool
	exportPlots: bool

class DataFramesForceVolume(NamedTuple):
	metaData: DataFrame
	rawCurves: DataFrame
	correctedCurves: DataFrame
	averageData: DataFrame
	channelData: DataFrame

# Lineplot toolbar
class ViewLimits(NamedTuple):
	xMin: int
	xMax: int
	yMin: int
	yMax: int