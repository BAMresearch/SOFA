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

# Named tuples for 
class LinePlotParameters(NamedTuple):
	linked: tk.BooleanVar
	holder: FigureCanvasTkAgg
	showInactive: bool 
	plotAverage: bool
	plotErrorbar: bool

class HeatmapParameters(NamedTuple): 
	linked: tk.BooleanVar
	holder: FigureCanvasTkAgg
	activeChannel: tk.StringVar
	selectedArea: List[mpl.lines.Line2D]
	orientationIndices: List[int]

class HistogramParameters(NamedTuple):  
	linked: tk.BooleanVar
	holder: FigureCanvasTkAgg
	activeChannel: tk.StringVar
	zoom: tk.BooleanVar
	numberOfBins: ttk.Entry

# Named tuples for FDC data
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

class NormedCurves(NamedTuple):
	piezoApproach: ndarray
	deflectionApproach: ndarray
	piezoContact: ndarray
	deflectionContact: ndarray

# Named tuples for the data import
class ImportParameter(NamedTuple):
	folderPathMeasurementData: str 
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

class ChannelData(NamedTuple):
	name: str
	size: Tuple[int]
	channelData: ndarray

# Named tuples for the data export
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