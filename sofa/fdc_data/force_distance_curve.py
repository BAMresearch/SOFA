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
from typing import List, Dict, Tuple

import numpy as np
from matplotlib.lines import Line2D

from data_processing.correct_data import correct_approach_curve
import data_visualization.plot_data as plt_data

import data_processing.named_tuples as nt

class ForceDistanceCurve():
	"""
	A single force distance curve.

	Attributes
	----------
	identifier : str
		Name of the force distance curve.
	dataApproachRaw : namedTuple
		Raw imported approach data with piezo (x) and
		deflection (y) values.
	dataApproachCorrected : namedTuple
		Corrected approach data with shifted piezo (x) 
		and deflection (y) values.
	couldBeCorrected : bool
		Indicates whether the curve could be corrected.
	channelMetadata : namedtuple
		Data created while correcting the curve used
		to calculate the different channels.
	lineRepresentationRawData : mpl.lines.Line2D
		Line of the raw data used to represent the 
		curve in a plot. 
	lineRepresentationCorrectedData : mpl.lines.Line2D
		Line of the corrected data used to represent 
		the curve in a plot.
	"""
	def __init__(self, identifier: str, dataApproachRaw: nt.ForceDistanceCurve):
		"""
		Initialize a force distance curve by setting it's identifier 
		and raw data. 

		Parameters
		----------
		identifier : str
			Name of the force distance curve.
		dataApproachRaw : namedTuple
			Raw imported approach data with piezo (x) and
			deflection (y) values.
		"""
		self.identifier: str = identifier
		
		self.dataApproachRaw: NamedTuple = dataApproachRaw
		self.dataApproachCorrected: NamedTuple
		self.couldBeCorrected: bool
		self.channelMetadata: NamedTuple

		self.lineRepresentationRawData: matplotlib.lines.Line2D
		self.lineRepresentationCorrectedData: matplotlib.lines.Line2D

	def correct_raw_data(self) -> None:
		"""
		Correct the raw data of the approach curve.
		"""
		try:
			self.dataApproachCorrected, self.channelMetadata = correct_approach_curve(
				self.dataApproachRaw
			)
		except CorrectionError:
			self.couldBeCorrected = False
		else:
			self.couldBeCorrected = True 

	def create_line_representation_raw_data(self) -> None:
		"""
		Create a displayable line from the raw data of the force
		distance curve.
		"""
		self.lineRepresentationRawData = plt_data.create_raw_line(
			self.identifier,
			self.dataApproachRaw
		)

	def create_line_representation_corrected_data(self) -> None:
		"""
		Create a displayable line from the corrected data of 
		the force distance curve.
		"""
		self.lineRepresentationCorrectedData = plt_data.create_corrected_line(
			self.identifier,
			self.dataApproachCorrected
		)