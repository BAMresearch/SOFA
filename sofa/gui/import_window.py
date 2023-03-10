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
import functools

import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import data_processing.named_tuples as nt
import data_processing.import_data as imp_data

def decorator_check_required_folder_path(function):
	"""
	Check if the required path for the measurement
	folder is set.
	"""
	@functools.wraps(function)
	def wrapper_check_required_folder_path(self):
		if not os.path.isdir(self.filePathData.get()):
			return messagebox.showerror(
				"Error", 
				"A data dictionary is required!", 
				parent=self
			)
		else:
			function(self)

	return wrapper_check_required_folder_path

class ImportWindow(ttk.Frame):
	"""
	A subwindow to import data.

	Attributes
	----------
	forceVolume : ForceVolume

	"""
	def __init__(self, root, forceVolume, set_filename):
		"""
		"""
		super().__init__(root, padding=10)
		
		self.pack(fill=BOTH, expand=YES)

		self.forceVolume = forceVolume
		self.set_filename = set_filename
		self.dataTypes = imp_data.importFunctions.keys()

		self._create_window()

	def _create_window(self) -> None:
		"""Define all elements within the import window."""
		self._create_frame_required_data()
		self._create_frame_optional_data()
		self._create_import_button()
		self._create_progressbar()

	def _create_frame_required_data(self) -> None:
		"""Define all elements within the required data frame."""
		frameRequiredData = ttk.Labelframe(self, text="Required Data", padding=15)
		frameRequiredData.pack(fill=X, expand=YES, anchor=N, padx=15, pady=(15, 5))

		# Data type
		rowDataType = ttk.Frame(frameRequiredData)
		rowDataType.pack(fill=X, expand=YES, pady=(0, 5))

		dataTypeLabel = ttk.Label(rowDataType, text="Data Type")
		dataTypeLabel.pack(side=LEFT, padx=(15, 0))

		self.selectedDataType = tk.StringVar(self, value="BAM_IBW")
		
		dropdownDataType = ttk.OptionMenu(
			rowDataType, self.selectedDataType, 
			"", *self.dataTypes
		)
		dropdownDataType.pack(side=RIGHT, padx=5)

		# Data files
		self.filePathData = tk.StringVar(self)

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
		self.showPoorCurves = tk.StringVar(self)

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
		frameOptionalData = ttk.Labelframe(self, text="Optional Data", padding=15)
		frameOptionalData.pack(fill=X, expand=YES, anchor=N, padx=15, pady=5)

		# Image file
		self.filePathImage = tk.StringVar(self)

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
		self.filePathChannel = tk.StringVar(self)

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
		"""
		Define the import button.
		"""
		rowImportButton = ttk.Frame(self)
		rowImportButton.pack(fill=X, expand=YES, pady=(20, 10))

		buttonImportData = ttk.Button(
			rowImportButton,
			text="Import Data",
			command=self._import_data
		)
		buttonImportData.pack(side=LEFT, padx=15)

	def _create_progressbar(self) -> None:
		"""
		Define the progressbar.
		"""	
		rowLabelProgressbar = ttk.Frame(self)
		rowLabelProgressbar.pack(fill=X, expand=YES)

		self.progressbarCurrentLabel = tk.StringVar(self, value="")

		labelProgressbar = ttk.Label(rowLabelProgressbar, textvariable=self.progressbarCurrentLabel)
		labelProgressbar.pack(side=RIGHT, padx=15)

		self.progressbar = ttk.Progressbar(
			self,
			mode=INDETERMINATE, 
            bootstyle=SUCCESS
		)
		self.progressbar.pack(fill=X, expand=YES, padx=15, pady=(5, 15))

	def _browse_data(self) -> None:
		"""
		Select the required folder that contains the 
		measurement data.
		"""
		filePathData = fd.askdirectory(
			title="Select directory",
			parent=self
		)

		if filePathData:
			self.filePathData.set(filePathData)

	def _browse_image(self):
		"""
		Select an additional image file.
		"""
		filePathImage = fd.askopenfilename(
			title="Select File",
			parent=self
		)

		if filePathImage:
			self.filePathImage.set(filePathImage)

	def _browse_channel(self):
		"""
		Select an additional channel file.
		"""
		filePathChannel = fd.askopenfilename(
			title="Select Channel",
			parent=self
		)

		if filePathChannel:
			self.filePathChannel.set(filePathChannel)

	@decorator_check_required_folder_path
	def _import_data(self) -> messagebox:
		"""
		Import, process and display the selected data files.

		Returns
		-------
		userFeedback : messagebox
			Informs the user whether the data could be imported or not.
		"""
		self._update_progressbar_label("Importing data...")
		self._start_progressbar()

		selected_import_function = imp_data.importFunctions[self.selectedDataType.get()][0]
		selectedImportParameters = self._create_selected_import_parameters()

		try:
			importedData = selected_import_function(
				selectedImportParameters,
			)
		except ce.ImportError as e:
			self._stop_progressbar()
			return messagebox.showerror("Error", str(e), parent=self)
		else:
			self.forceVolume.import_data(importedData)

		self._update_progressbar_label("Correcting data...")
		self.forceVolume.correct_data()

		self._update_progressbar_label("Calculating channel data...")
		self.forceVolume.calculate_channel_data()

		self._update_progressbar_label("Preparing to plot data...")
		self.forceVolume.display_imported_data()

		# Set the name, size and location of the imported data in the main window.
		self.set

		self._stop_progressbar()

		self.destroy()

		return messagebox.showinfo("Success", "Data was successfully imported.")

	def _create_selected_import_parameters(self) -> nt.ImportParameter:
		"""
		Summarize the selected import parameters.

		Returns
		-------
		importParameter : nt.ImportParameter
			Contains the selected import parameters and opotions.
		"""
		return nt.ImportParameter(
			filePathData=self.filePathData.get(),
			filePathImage=self.filePathImage.get(),
			filePathChannel=self.filePathChannel.get(),
			showPoorCurves=self.showPoorCurves.get()
		)

	def _start_progressbar(self) -> None:
		"""

		"""
		self.progressbar.start()

	def _stop_progressbar(self) -> None:
		"""

		"""
		self.progressbar.stop()
		self.progressbarCurrentLabel.set("")

	def _update_progressbar_label(
		self, 
		label=""
	) -> None:
		"""
		.

		Parameters
		----------
		label : str
			Describes the current action.
		"""
		self.progressbarCurrentLabel.set(label)