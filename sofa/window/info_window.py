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
import os

import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class InfoWindow(ttk.Frame):
	"""A subwindow that contains some informations about SOFA."""
	def __init__(self, versionNumber):
		self.window = tk.Toplevel()
		self.window.title("About")

		self.versionNumber = versionNumber
		self.contactEmail = "sofa@bam.de"
		self.license = "GNU GENERAL PUBLIC LICENSE"
		self.textGeneralInfo = (
			"SOFA offers universal and robust algorithms for correcting topography \n"
			"in AFM force spectroscopy data and for postprocessing of AFM force \n"
			"spectroscopy arrays. SOFA was developed by researchers of BAM and is \n"
			"shared with the scientific community for the benefit of non-commercial \n"
			"research."
		)
		self.textLicense = (
			"SOFA is distributed under the " + self.license + "."
		)
		self.textContact = (
			"To get in contact please use: " + self.contactEmail + "."
		)
		self.font = "10"

		self._create_window()

	def _create_window(self) -> None:
		"""Define all elements within the info window."""
		frameInformation = ttk.Frame(self.window, padding=10)
		frameInformation.pack(fill=X, expand=YES, padx=10, pady=10)

		rowGeneralInfo = ttk.Frame(frameInformation)
		rowGeneralInfo.pack(fill=X, expand=YES)
		
		labelGeneralInfo = ttk.Label(
			rowGeneralInfo, 
			text=self.textGeneralInfo, 
		)
		labelGeneralInfo.pack(side = LEFT, pady=(0, 10))

		rowLicense = ttk.Frame(frameInformation)
		rowLicense.pack(fill=X, expand=YES)

		labelLicense = ttk.Label(
			rowLicense, 
			text=self.textLicense, 
		)
		labelLicense.pack(side = LEFT, pady=10)

		rowContact = ttk.Frame(frameInformation)
		rowContact.pack(fill=X, expand=YES)

		labelContact = ttk.Label(
			rowContact, 
			text=self.textContact, 
		)
		labelContact.pack(side = LEFT)