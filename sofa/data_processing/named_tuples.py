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

# Named tuples for the data import
class ImportParameter(NamedTuple):
	folderPathMeasurementData: str 
	filePathImage: str 
	filePathChannel: str 
	showPoorCurves: bool

class ExportParameter(NamedTuple):
	folderName: str
	folderPath: str 
	exportToTex: bool
	exportToTxt: bool
	exportToHdf5: bool
	exportToExcel: bool
	exportPlots: bool

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
	exportToTxt: bool
	exportToCsv: bool
	exportToXlsx: bool
	exportPlots: bool