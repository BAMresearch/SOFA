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
from collections import namedtuple
from typing import List, Dict, Tuple

import numpy as np

from collections import namedtuple
from typing import List, Dict, Tuple

import numpy as np
from matplotlib.lines import Line2D

class ForceDistanceCurve():
	""""""
	def __init__(self):
		self.identifier: str
		self.rawDataApproach: np.ndarray
		self.couldBeCorrected: bool
		self.correctedDataApproach: np.ndarray
		self.correctionMetaData: Dict 	# needs better name
		self.lineRepresentationRawData: matplotlib.lines.Line2D
		self.lineRepresentationCorrectedData: matplotlib.lines.Line2D

	def import_raw_data(
		self, 
		identifier: str, 
		rawDataApproach: np.ndarray
	) -> None:
		""""""
		self.identifier = identifier
		self.rawDataApproach = rawDataApproach

	def correct_raw_data(self) -> None:
		""""""
		try:
			self.correctedDataApproach, self.correctionMetaData = correct_approach_curve(
				self.rawDataApproach
			)
			self.couldBeCorrected = True

		except ValueError:
			self.couldBeCorrected = False 

	def create_line_representation_raw_data(self) -> None:
		""""""
		self.lineRepresentationRawData = create_raw_line(
			self.identifier
			self.rawDataApproach[0], 
			self.rawDataApproach[1],
		)

	def create_line_representation_corrected_data(self) -> None:
		""""""
		self.lineRepresentationCorrectedData = create_corrected_line(
			self.identifier
			self.correctedDataApproach[0], 
			self.correctedDataApproach[1],
		)