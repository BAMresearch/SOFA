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
from typing import Callable

import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import data_processing.named_tuples as nt
import data_processing.custom_exceptions as ce
import data_processing.import_data.import_data as imp_data

def decorator_check_required_folder_path(function):
	"""
	Check if the required path for the measurement
	data is set.
	"""
	@functools.wraps(function)
	def wrapper_check_required_folder_path(self):
		if (not os.path.isdir(self.filePathData.get()) and 
			not os.path.isfile(self.filePathData.get())):
			return messagebox.showerror(
				"Error", 
				"Measurement data is required!", 
				parent=self
			)
		else:
			function(self)

	return wrapper_check_required_folder_path

class ImportWindow(ttk.Frame):
	"""
	A subwindow to import measurement data.

	Attributes
	----------
	guiInterface : GUIInterface
		Interface between the diffenrent SOFA windwos and 
		imported measurement data sets.
	progressbar : ttk.Progressbar
		Shows the user if the process of importing 
		the data is still running. 
	labelProgressbarVariable : tk.Stringvar
		Indicates the current running process.
	dataTypes : dict_keys
		Every available import format of SOFA.
	filePathData : tk.StringVar
		File path to the required measurement data.
	filePathImage : tk.StringVar
		File path to an optional image file.
	filePathChannel : tk.StringVar
		File path to a file with optional channel data.
	showPoorCurves : tk.BooleanVar
		Specifies whether curves that cannot be corrected 
		are to be displayed in the line plot. 
	"""
	def __init__(
		self, 
		root, 
		guiInterface, 
	) -> None:
		"""
		Create a subwindow to import measurement data.
		"""
		super().__init__(root, padding=10)
		
		self.pack(fill=BOTH, expand=YES)

		self.toplevel = root
		self.guiInterface = guiInterface
		self.dataTypes = imp_data.importFunctions.keys()

		self._setup_input_variables()
		self._create_window()

	def _setup_input_variables(self) -> None: 
		"""
		Initialize all required variables for the entries,
		checkbuttons and the progressbar.
		"""
		self.selectedDataType = tk.StringVar(self, value=".ibw")
		self.showPoorCurves = tk.BooleanVar(self)

		self.filePathData = tk.StringVar(self)

		self.filePathImage = tk.StringVar(self)
		self.filePathChannel = tk.StringVar(self)

		self.progressbarCurrentLabel = tk.StringVar(self, value="")

	def _create_window(self) -> None:
		"""
		Define all elements within the import window.
		"""
		self._create_frame_import_options()
		self._create_frame_required_data()
		self._create_frame_optional_data()
		self._create_import_button()
		self._create_progressbar()

	def _create_frame_import_options(self) -> None:
		"""
		Define a drop down menu to select the data type
		of the measurement data and checkbuttons to
		specify the import options.
		"""
		frameImportOptions = ttk.Labelframe(self, text="Import Options", padding=15)
		frameImportOptions.pack(fill=X, expand=YES, anchor=N, padx=15, pady=(15, 5))

		# Data type
		rowDataType = ttk.Frame(frameImportOptions)
		rowDataType.pack(fill=X, expand=YES, pady=(0, 15))

		dataTypeLabel = ttk.Label(rowDataType, text="Data Type")
		dataTypeLabel.pack(side=LEFT, padx=(15, 0))
		
		dropdownDataType = ttk.OptionMenu(
			rowDataType, 
			self.selectedDataType, 
			"", 
			*self.dataTypes
		)
		dropdownDataType.pack(side=RIGHT, padx=5)

		# Show poor curves
		rowShowPoorCurves = ttk.Frame(frameImportOptions)
		rowShowPoorCurves.pack(fill=X, expand=YES)

		checkButtonShowPoorCurves = ttk.Checkbutton(
			rowShowPoorCurves,
			text="Show poor curves",
			variable=self.showPoorCurves,
			onvalue=True,
			offvalue=False
		)
		checkButtonShowPoorCurves.pack(side=LEFT, padx=(15, 0))

	def _create_frame_required_data(self) -> None:
		"""
		Define an entry to specify the location of the 
		measurement data.
		"""
		frameRequiredData = ttk.Labelframe(self, text="Required Data", padding=15)
		frameRequiredData.pack(fill=X, expand=YES, anchor=N, padx=15, pady=(15, 5))

		# Measurement data files
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

	def _create_frame_optional_data(self) -> None:
		"""
		Define two entries to specify the location of an 
		optional image and channel file.
		"""	
		frameOptionalData = ttk.Labelframe(self, text="Optional Data", padding=15)
		frameOptionalData.pack(fill=X, expand=YES, anchor=N, padx=15, pady=5)

		# Image file.
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

		# Additional channel.
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
		Create the import button.
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
		Create an indeterminate progressbar.
		"""	
		rowLabelProgressbar = ttk.Frame(self)
		rowLabelProgressbar.pack(fill=X, expand=YES)

		labelProgressbar = ttk.Label(rowLabelProgressbar, textvariable=self.progressbarCurrentLabel)
		labelProgressbar.pack(side=RIGHT, padx=15)

		self.progressbar = ttk.Progressbar(
			self,
			mode=DETERMINATE, 
            bootstyle=SUCCESS
		)
		self.progressbar.pack(fill=X, expand=YES, padx=15, pady=(5, 15))

	def _browse_data(self) -> None:
		"""
		Select the required folder or file that contains 
		the measurement data.
		"""
		filedialog = self._map_data_type_to_file_dialog()
		filePathData = filedialog()

		if filePathData:
			self.filePathData.set(filePathData)

	def _map_data_type_to_file_dialog(self) -> Callable:
		"""
		Map the selected data type of the measurement
		data to the associated file structure (file or
		folder).

		Returns
		-------
		browse_files : function
			Function to either select a single file
			or directory.
		"""
		if self.selectedDataType.get() == ".ibw":
			return self._browse_data_directory

		return self._browse_data_file

	def _browse_data_file(self) -> str:
		"""
		Select the required file that contains the 
		measurement data.

		Returns
		-------
		filePathDatafile : str
			File path to the measurement file
		"""
		return fd.askopenfilename(
			title="Select file",
			parent=self
		)

	def _browse_data_directory(self) -> str:
		"""
		Select the required folder that contains the 
		measurement data.

		Returns
		-------
		filePathDirectory : str
			File path to the measurement folder.
		"""
		return fd.askdirectory(
			title="Select directory",
			parent=self
		)

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
		self._update_progressbar("Importing data...", 0.0)
		
		selected_import_function = imp_data.importFunctions[self.selectedDataType.get()][0]
		selectedImportParameters = self._create_selected_import_parameters()
		
		try:
			importedData = selected_import_function(
				selectedImportParameters
			)
		except ce.ImportError as e:
			self._stop_progressbar()
			return messagebox.showerror("Error", str(e), parent=self)
		else:
			self._update_progressbar("Processing data...", 50.0)
			self.guiInterface.create_force_volume(
				importedData,
				selectedImportParameters.filePathData
			)
		self._reset_progrressbar()

		self.toplevel.destroy()

		return messagebox.showinfo("Success", "Data was successfully imported.")
		
	def _create_selected_import_parameters(self) -> nt.ImportParameter:
		"""
		Combine the selected import parameters.

		Returns
		-------
		importParameter : nt.ImportParameter
			Bundels the selected import parameters and opotions.
		"""
		return nt.ImportParameter(
			dataFormat=self.selectedDataType.get(),
			filePathData=self.filePathData.get(),
			filePathImage=self.filePathImage.get(),
			filePathChannel=self.filePathChannel.get(),
			showPoorCurves=self.showPoorCurves.get()
		)

	def _update_progressbar(
		self, 
		label: str,
		progressValue: float
	) -> None:
		"""
		Update the value and label of procressbar to 
		show the current process.

		Parameters
		----------
		label : str
			Description of the current process.
		progressValue : float.
			Indicates current progress made.
		"""
		self.progressbar["value"] += progressValue
		self.progressbarCurrentLabel.set(label)
		self.update_idletasks()

	def _reset_progrressbar(self) -> None: 
		"""
		Reset the value and label of the progressbar.
		"""
		self.progressbar["value"] = 0
		self.progressbarCurrentLabel.set("")
		self.update_idletasks()