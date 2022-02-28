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
from typing import NamedTuple

import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import data.import_data as impd
import data.process_data as pd
import data.active_channels as ac

class ImportWindow(ttk.Frame):
	def __init__(self, dataHandler, update_main_window):
		self.window = tk.Toplevel()
		self.window.title("Import Data")

		self.dataHandler = dataHandler
		self.update_main_window = update_main_window
		self.dataTypes = impd.importFunctions.keys()

		self._create_window()

	def _create_window(self) -> None:
		"""Define all elements within the import window."""
		self._create_frame_required_data()
		self._create_frame_optional_data()
		self._create_import_button()
		self._create_progressbar()

	def _create_frame_required_data(self) -> None:
		"""Define all elements within the required data frame."""
		frameRequiredData = ttk.Labelframe(self.window, text="Required Data", padding=15)
		frameRequiredData.pack(fill=X, expand=YES, anchor=N, padx=15, pady=(15, 5))

		# Data type
		rowDataType = ttk.Frame(frameRequiredData)
		rowDataType.pack(fill=X, expand=YES, pady=(0, 5))

		dataTypeLabel = ttk.Label(rowDataType, text="Data Type")
		dataTypeLabel.pack(side=LEFT, padx=(15, 0))

		self.selectedDataType = tk.StringVar(self.window, value="BAM_IBW")
		
		dropdownDataType = ttk.OptionMenu(
			rowDataType, self.selectedDataType, 
			"", *self.dataTypes
		)
		dropdownDataType.pack(side=RIGHT, padx=5)

		# Data files
		self.filePathData = tk.StringVar(self.window)

		rowDataFiles = ttk.Frame(frameRequiredData)
		rowDataFiles.pack(fill=X, expand=YES, pady=(10, 15))

		labelDataFile = ttk.Label(rowDataFiles, text="Data", width=8)
		labelDataFile.pack(side=LEFT, padx=(15, 0))

		entryData = ttk.Entry(rowDataFiles, textvariable=self.filePathData)
		entryData.pack(side=LEFT, fill=X, expand=YES, padx=5)

		buttonBrowseData = ttk.Button(
			rowDataFiles,
			text="Browse",
			command=self._browse_data
		)
		buttonBrowseData.pack(side=LEFT, padx=5)

		# Options
		self.showPoorCurves = tk.StringVar(self.window)

		rowOptions = ttk.Frame(frameRequiredData)
		rowOptions.pack(fill=X, expand=YES)

		checkButtonShowPoorCurves = ttk.Checkbutton(
			rowOptions,
			text="Show poor curves",
			variable=self.showPoorCurves,
			onvalue=True,
			offvalue=False
		)
		checkButtonShowPoorCurves.pack(side=LEFT, padx=(15, 0))

	def _create_frame_optional_data(self) -> None:
		"""Define all elements within the optional data frame."""	
		frameOptionalData = ttk.Labelframe(self.window, text="Optional Data", padding=15)
		frameOptionalData.pack(fill=X, expand=YES, anchor=N, padx=15, pady=5)

		# Image file
		self.filePathImage = tk.StringVar(self.window)

		rowImageFile = ttk.Frame(frameOptionalData)
		rowImageFile.pack(fill=X, expand=YES, pady=(0, 10))

		labelImageFile = ttk.Label(rowImageFile, text="Image", width=8)
		labelImageFile.pack(side=LEFT, padx=(15, 0))

		entryImage = ttk.Entry(rowImageFile, textvariable=self.filePathImage)
		entryImage.pack(side=LEFT, fill=X, expand=YES, padx=5)

		buttonBrowseImage = ttk.Button(
			rowImageFile,
			text="Browse",
			command=self._browse_image
		)
		buttonBrowseImage.pack(side=LEFT, padx=5)

		# Additional channel
		self.filePathChannel = tk.StringVar(self.window)

		rowChannelFile = ttk.Frame(frameOptionalData)
		rowChannelFile.pack(fill=X, expand=YES)

		labelChannelFile = ttk.Label(rowChannelFile, text="Channel", width=8)
		labelChannelFile.pack(side=LEFT, padx=(15, 0))

		entryImage = ttk.Entry(rowChannelFile, textvariable=self.filePathChannel)
		entryImage.pack(side=LEFT, fill=X, expand=YES, padx=5)

		buttonBrowseChannel = ttk.Button(
			rowChannelFile,
			text="Browse",
			command=self._browse_channel
		)
		buttonBrowseChannel.pack(side=LEFT, padx=5)

	def _create_import_button(self) -> None: 
		"""Define the import button."""
		rowImportButton = ttk.Frame(self.window)
		rowImportButton.pack(fill=X, expand=YES, pady=(20, 10))

		buttonImportData = ttk.Button(
			rowImportButton,
			text="Import Data",
			command=self._import_data
		)
		buttonImportData.pack(side=LEFT, padx=15)

	def _create_progressbar(self) -> None:
		"""Define the progressbar."""	
		rowLabelProgressbar = ttk.Frame(self.window)
		rowLabelProgressbar.pack(fill=X, expand=YES)

		self.progressbarCurrentLabel = tk.StringVar(self.window, value="")

		labelProgressbar = ttk.Label(rowLabelProgressbar, textvariable=self.progressbarCurrentLabel)
		labelProgressbar.pack(side=RIGHT, padx=15)

		self.progressbar = ttk.Progressbar(
			self.window,
			mode=DETERMINATE, 
            bootstyle=SUCCESS
		)
		self.progressbar.pack(fill=X, expand=YES, padx=15, pady=(5, 15))

	def _browse_data(self) -> None:
		"""Select the directory that contains the data."""
		filePathData = fd.askdirectory(
			title="Select directory",
			parent=self.window
		)

		if filePathData:
			self.filePathData.set(filePathData)

	def _browse_image(self):
		"""Select the image file."""
		filePathImage = fd.askopenfilename(
			title="Select File",
			parent=self.window
		)

		if filePathImage:
			self.filePathImage.set(filePathImage)

	def _browse_channel(self):
		"""Select the channel file."""
		filePathChannel = fd.askopenfilename(
			title="Select Channel",
			parent=self.window
		)

		if filePathChannel:
			self.filePathChannel.set(filePathChannel)

	def _import_data(self) -> messagebox:
		"""Import the selected data."""
		# Check if required data is selected.
		if not os.path.isdir(self.filePathData.get()):
			self._reset_import_window()
			return messagebox.showerror("Error", "A data dictionary is required!", parent=self.window)

		selectedImportParameters = self._create_selected_import_parameters()
		selected_import_function = impd.importFunctions[self.selectedDataType.get()][0]

		# Try to import selected data.
		try:
			importedData = selected_import_function(
				selectedImportParameters,
				self.update_progressbar
			)

		except Exception as e:
			self._reset_import_window()
			print(str(e))
			return messagebox.showerror("Error", str(e), parent=self.window)

		# Correct imported data.
		correctedCurveData = pd.correct_approach_curves(
			importedData["curveData"].approachCurves,
			self.update_progressbar
		)

		# Calculate channel data.
		channelData = ac.calculate_channels(
			correctedCurveData,
			importedData["curveData"].m,
			importedData["curveData"].n,
			self.update_progressbar
		)

		# Process imported data.
		combinedData = pd.combine_data(
			importedData,
			correctedCurveData,
			channelData,
			self.update_progressbar
		)

		# Hand data to the data handler
		self.dataHandler.set_imported_data(
			combinedData
		)

		self.update_main_window(
			combinedData["generalData"]["filename"]
		)

		# Display imported data
		self.dataHandler.init_mapped_indices()
		self.dataHandler.display_imported_data()

		# Close window
		self.window.destroy()

		return messagebox.showinfo("Success", "Data is imported.")

	def _create_selected_import_parameters(self) -> NamedTuple:
		"""Summarize the selected import options for easier use."""
		ImportOptions = namedtuple(
			"ImportOptions",
			[
				"filePathData",
				"filePathImage",
				"filePathChannel",
				"showPoorCurves",
			]	
		)

		return ImportOptions(
			filePathData=self.filePathData.get(),
			filePathImage=self.filePathImage.get(),
			filePathChannel=self.filePathChannel.get(),
			showPoorCurves=self.showPoorCurves.get()
		)

	def _reset_import_window(self):
		"""Reset the user input."""
		self.filePathData.set("")
		self.filePathImage.set("")
		self.filePathChannel.set("")

	def update_progressbar(self, mode="update", value=0, label=""):
		"""Update the progressbar."""
		if mode == "reset":
			self.progressbar["value"] = 0
			self.progressbarCurrentLabel.set(label)

		elif mode == "update":
			self.progressbar["value"] += value

		self.window.update_idletasks()