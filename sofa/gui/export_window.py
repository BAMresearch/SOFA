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
import data_processing.export_data as exp_data

def decorator_check_required_folder_path(function):
	"""
	Check if the required path for the measurement
	folder is set.
	"""
	@functools.wraps(function)
	def wrapper_check_required_folder_path(self):
		if not os.path.isdir(self.folderPath.get()):
			return messagebox.showerror(
				"Error", 
				"A folder for the ouput folder is required.", 
				parent=self
			)
		else:
			function(self)

	return wrapper_check_required_folder_path

def decorator_check_required_folder_name(function):
	"""
	Check if the required path for the measurement
	folder is set.
	"""
	@functools.wraps(function)
	def wrapper_check_required_folder_name(self):
		if not self.folderName.get():
			return messagebox.showerror(
				"Error", 
				"A name for the ouput folder is required.", 
				parent=self
			)
		else:
			function(self)

	return wrapper_check_required_folder_name

class ExportWindow(ttk.Frame):
	"""
	A subwindow to export data.

	Attributes
	----------
	guiInterface : guiInterface
		Interface between the diffenrent SOFA windwos and 
		imported measurement data sets.
	progressbar : ttk.Progressbar
		Shows the user if the process of exporting 
		the data is still running.
	labelProgressbarVariable : tk.Stringvar
		Indicates the current running process.
	folderPath : tk.StringVar
		Location where folder is created to store the data.
	folderName : tk.StringVar
		Name of the folder to store the data.
	exportToCsv : tk.BooleanVar
		Indicates whether the data should be exported 
		to the .csv file format.
	exportToXlsx : tk.BooleanVar
		Indicates whether the data should be exported 
		to the .xlsx file format.
	exportPlots : tk.BooleanVar
		Indicates whether the plots should be exported.
	"""
	def __init__(
		self, 
		root, 
		guiInterface
	):
		"""
		Create a subwindow to export the data of the guiInterface.
		"""
		super().__init__(root)
		
		self.pack(fill=BOTH, expand=YES)

		self.toplevel = root
		self.guiInterface = guiInterface

		self._setup_input_variables()
		self._create_window()

	def _setup_input_variables(self) -> None: 
		"""
		Initialize all required variables for the entries,
		checkbuttons and the progressbar.
		"""
		self.folderName = tk.StringVar(self, value="")
		self.folderPath = tk.StringVar(self, value="")

		self.exportToCsv = tk.BooleanVar(self, value=0)
		self.exportToXlsx = tk.BooleanVar(self, value=0)
		self.exportPlots = tk.BooleanVar(self, value=0)

		self.progressbarCurrentLabel = tk.StringVar(self, value="")

	def _create_window(self) -> None:
		"""
		Define all elements within the export window.
		"""
		self._create_frame_data_location()
		self._create_frame_data_types()
		self._create_export_button()
		self._create_progressbar()

	def _create_frame_data_location(self) -> None:
		"""
		Define two entries in the data location frame
		to specify the location and name of the output
		folder.
		"""
		frameDataLocation = ttk.Labelframe(self, text="Data Location", padding=15)
		frameDataLocation.pack(fill=X, expand=YES, anchor=N, padx=15, pady=(15, 5))

		# Folder name
		rowFolderName = ttk.Frame(frameDataLocation)
		rowFolderName.pack(fill=X, expand=YES, pady=(10, 15))

		labelFolderName = ttk.Label(rowFolderName, text="Foldername", width=12)
		labelFolderName.pack(side=LEFT, padx=(15, 0))

		entryFolderName = ttk.Entry(rowFolderName, textvariable=self.folderName)
		entryFolderName.pack(side=LEFT, fill=X, expand=YES, padx=5)

		# Folder path
		rowFolderPath= ttk.Frame(frameDataLocation)
		rowFolderPath.pack(fill=X, expand=YES, pady=(10, 15))

		labelFolderPath = ttk.Label(rowFolderPath, text="Folderpath", width=12)
		labelFolderPath.pack(side=LEFT, padx=(15, 0))

		entryFolderPath = ttk.Entry(rowFolderPath, textvariable=self.folderPath)
		entryFolderPath.pack(side=LEFT, fill=X, expand=YES, padx=5)

		buttonBrowseFolderPath = ttk.Button(
			rowFolderPath,
			text="Browse",
			command=self._browse_folder_path
		)
		buttonBrowseFolderPath.pack(side=LEFT, padx=5)

	def _create_frame_data_types(self) -> None:
		"""
		Define a checkbutton for every available export format
		in the data types frame.
		"""
		frameDataTypes = ttk.Labelframe(self, text="Data Types", padding=15)
		frameDataTypes.pack(fill=X, expand=YES, anchor=N, padx=15, pady=5)

		self._create_checkbutton_data_type(
			frameDataTypes,
			self.exportToCsv,
			"export to csv"
		)
		self._create_checkbutton_data_type(
			frameDataTypes,
			self.exportToXlsx,
			"export to xlsx"
		)
		self._create_checkbutton_data_type(
			frameDataTypes,
			self.exportPlots,
			"export plots"
		)

	def _create_checkbutton_data_type(
		self,
		parentFrame: ttk.Labelframe,
		booleanVar: tk.BooleanVar,
		label: str
	) -> None:
		"""
		Create a single chechbutton for a file type
		to be able to select if the data should be 
		exported in this format.

		Parameters
		----------
		parentFrame : ttk.Labelframe
			Labeled frame for all data type checkbuttons.
		booleanVar : tk.BooleanVar
			Variable to store the selection.
		label : str
			Label of the checkbutton with the releated
			file type.
		"""
		rowCheckButton = ttk.Frame(parentFrame)
		rowCheckButton.pack(fill=X, expand=YES)

		checkbutton = ttk.Checkbutton(
			rowCheckButton,
			text=label,
			variable=booleanVar,
			onvalue=True,
			offvalue=False
		)
		checkbutton.pack(side=LEFT, padx=(15, 0), pady=5)

	def _create_export_button(self) -> None:
		"""
		Create the export button.
		"""
		rowExportButton = ttk.Frame(self)
		rowExportButton.pack(fill=X, expand=YES, pady=(20, 10))

		buttonExportData = ttk.Button(
			rowExportButton,
			text="Export Data",
			command=self._export_data
		)
		buttonExportData.pack(side=LEFT, padx=15)

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

	def _browse_folder_path(self) -> None:
		"""
		Select the directory in which the data will be saved.
		"""
		folderPath = fd.askdirectory(
			title="Select directory",
			parent=self
		)

		if folderPath:
			self.folderPath.set(folderPath)

	@decorator_check_required_folder_path
	@decorator_check_required_folder_name
	def _export_data(self) -> messagebox:
		"""
		Export the data of the force volume and if selected
		the plots as well to the specified location.

		Returns
		-------
		userFeedback : messagebox
			Informs the user whether the data could 
			be exported or not.
		"""
		self._update_progressbar("Exporting data...", 0)

		exportParameters = self._create_selected_export_parameters()
		outputFolder = exp_data.setup_output_folder(
			exportParameters.folderPath,
			exportParameters.folderName
		)
		activeForceVolume = self.guiInterface.get_active_force_volume()

		if exportParameters.exportToCsv:
			self._update_progressbar("Exporting to csv...", 25.0)
			exp_data.export_to_csv(activeForceVolume, outputFolder)

		if exportParameters.exportToXlsx:
			self._update_progressbar("Exporting to xlsx...", 25.0)
			exp_data.export_to_xlsx(activeForceVolume, outputFolder)

		if exportParameters.exportPlots:
			self._update_progressbar("Exporting plots...", 25.0)
			exp_data.export_plots(
				self.guiInterface.linePlotParameters.holder,
				self.guiInterface.heatmapParameters.holder,
				self.guiInterface.histogramParameters.holder,
				outputFolder
			)

		self._reset_progrressbar()

		self.toplevel.destroy()

		return messagebox.showinfo("Success", "Data is exported.")

	def _create_selected_export_parameters(self) -> nt.ExportParameter:
		"""
		Combine the selected export parameter.

		Returns
		-------
		ExportParameter : nt.ExportParameter
			Contains the path and name of the output
			folder and the selected file formats for
			the export.
		"""
		return nt.ExportParameter(
			folderPath=self.folderPath.get(),
			folderName=self.folderName.get(),
			exportToCsv=self.exportToCsv.get(),
			exportToXlsx=self.exportToXlsx.get(),
			exportPlots=self.exportPlots.get(),
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