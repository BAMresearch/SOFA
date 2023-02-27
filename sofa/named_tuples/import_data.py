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

from typing import NamedTuple
from numpy import ndarray

class ImportParameter(NamedTuple):
	folderPathMeasurementData: str 
	filePathImage: str 
	filePathChannel: str 
	showPoorCurves: bool

class ImportedData(NamedTuple):
	measurementData: MeasurementData
	imageData: ImageData
	channelData: ChannelData

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
	channelHeight: np.ndarray
	channelAdhesion: np.ndarray

class ChannelData(NamedTuple):
	name: str
	size: Tuple[int]
	channelData: np.ndarray