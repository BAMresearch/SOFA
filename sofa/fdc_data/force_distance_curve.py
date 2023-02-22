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
from typing import List, Dict, Tuple, NamedTuple

import numpy as np
from matplotlib.lines import Line2D

from data_processing.correct_data import correct_approach_curves
import data_visualization.plot_data as plt_data

class ForceDistanceCurve():
	"""
	

	Attributes
	----------
	identifier : str
		
	dataApproachRaw : namedTuple
		
	dataApproachCorrected : namedTuple
		
	couldBeCorrected : bool
		
	channelMetadata : namedtuple
		
	lineRepresentationRawData : mpl.lines.Line2D
		
	lineRepresentationCorrectedData : mpl.lines.Line2D
		
	"""
	def __init__(self, identifier: str, dataApproachRaw: NamedTuple):
		"""
		
		Parameters
		----------
		identifier : str

		dataApproachRaw : np.ndarray

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
		
		"""
		try:
			self.dataApproachCorrected, self.channelMetadata = correct_approach_curve(
				self.dataApproachRaw
			)
			self.couldBeCorrected = True

		except CorrectionError:
			self.couldBeCorrected = False 

	def create_line_representation_raw_data(self) -> None:
		"""

		"""
		self.lineRepresentationRawData = plt_data.create_raw_line(
			self.identifier
			self.dataApproachRaw
		)

	def create_line_representation_corrected_data(self) -> None:
		"""
		
		"""
		self.lineRepresentationCorrectedData = plt_data.create_corrected_line(
			self.identifier
			self.dataApproachCorrected
		)