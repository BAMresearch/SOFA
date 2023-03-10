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
	forceVolume : ForceVolume
	"""
	def __init__(
		self, 
		root, 
		forceVolume
	):
		"""
		"""
		super().__init__(root)
		
		self.pack(fill=BOTH, expand=YES)

		self.forceVolume = forceVolume

		self._create_window()

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
		Define all elements within the data location frame.
		"""
		frameDataLocation = ttk.Labelframe(self, text="Data Location", padding=15)
		frameDataLocation.pack(fill=X, expand=YES, anchor=N, padx=15, pady=(15, 5))

		self.folderName = tk.StringVar(self, value="")
		self.folderPath = tk.StringVar(self, value="")

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
		Define all elements within the data types frame.
		"""
		frameDataTypes = ttk.Labelframe(self, text="Data Types", padding=15)
		frameDataTypes.pack(fill=X, expand=YES, anchor=N, padx=15, pady=5)

		self.exportToSofa = tk.BooleanVar(self, value=0)
		self.exportToTex = tk.BooleanVar(self, value=0)
		self.exportToTxt = tk.BooleanVar(self, value=0)
		self.exportToHdf5 = tk.BooleanVar(self, value=0)
		self.exportToExcel = tk.BooleanVar(self, value=0)
		self.exportPlots = tk.BooleanVar(self, value=0)

		# Export to sofa
		rowExportToSofa = ttk.Frame(frameDataTypes)
		rowExportToSofa.pack(fill=X, expand=YES)

		checkbuttonExportToSofa = ttk.Checkbutton(
			rowExportToSofa,
			text="export to sofa",
			variable=self.exportToSofa,
			onvalue=True,
			offvalue=False
		)
		checkbuttonExportToSofa.pack(side=LEFT, padx=(15, 0), pady=5)

		# Export to tex
		rowExportToTex = ttk.Frame(frameDataTypes)
		rowExportToTex.pack(fill=X, expand=YES)

		checkbuttonExportToTex = ttk.Checkbutton(
			rowExportToTex,
			text="export to tex",
			variable=self.exportToTex,
			onvalue=True,
			offvalue=False
		)
		checkbuttonExportToTex.pack(side=LEFT, padx=(15, 0), pady=5)

		# Export to txt
		rowExportToTxt = ttk.Frame(frameDataTypes)
		rowExportToTxt.pack(fill=X, expand=YES)

		checkbuttonExportToTxt = ttk.Checkbutton(
			rowExportToTxt,
			text="export to txt",
			variable=self.exportToTxt,
			onvalue=True,
			offvalue=False
		)
		checkbuttonExportToTxt.pack(side=LEFT, padx=(15, 0), pady=5)

		# Export to hdf5
		rowExportToHdf5 = ttk.Frame(frameDataTypes)
		rowExportToHdf5.pack(fill=X, expand=YES)

		checkbuttonExportToHdf5 = ttk.Checkbutton(
			rowExportToHdf5,
			text="export to hdf5",
			variable=self.exportToHdf5,
			onvalue=True,
			offvalue=False
		)
		checkbuttonExportToHdf5.pack(side=LEFT, padx=(15, 0), pady=5)

		# Export to excel
		rowExportToExcel = ttk.Frame(frameDataTypes)
		rowExportToExcel.pack(fill=X, expand=YES)

		checkbuttonExportToExcel = ttk.Checkbutton(
			rowExportToExcel,
			text="export to excel",
			variable=self.exportToExcel,
			onvalue=True,
			offvalue=False
		)
		checkbuttonExportToExcel.pack(side=LEFT, padx=(15, 0), pady=5)

		# Export plots
		rowExportPlots = ttk.Frame(frameDataTypes)
		rowExportPlots.pack(fill=X, expand=YES)

		checkbuttonExportPlots = ttk.Checkbutton(
			rowExportPlots,
			text="export plots",
			variable=self.exportPlots,
			onvalue=True,
			offvalue=False
		)
		checkbuttonExportPlots.pack(side=LEFT, padx=(15, 0), pady=5)

	def _create_export_button(self) -> None:
		"""
		Define the export button.
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
		the plots as well.

		Returns
		-------
		userFeedback : messagebox
			Informs the user whether the data could 
			be exported or not.
		"""
		self._update_progressbar_label("Exporting data...")
		self._start_progressbar()

		exportParameters = self._create_selected_export_parameters()

		outputFolder = exp_data.setup_output_folder(
			exportParameters.folderPath,
			exportParameters.folderName
		)

		if exportParameters.exportToTxt:
			self._update_progressbar_label("Exporting to txt...")
			exp_data.export_to_txt(self.forceVolume, outputFolder)

		if exportParameters.exportToCsv:
			self._update_progressbar_label("Exporting to csv...")
			exp_data.export_to_csv(self.forceVolume, outputFolder)

		if exportParameters.exportToXlsx:
			self._update_progressbar_label("Exporting to xlsx...")
			exp_data.export_to_xlsx(self.forceVolume, outputFolder)

		if exportParameters.exportPlots:
			self._update_progressbar_label("Exporting plots...")
			exp_data.export_plots(self.forceVolume, outputFolder)

		self._stop_progressbar()

		self.destroy()

		return messagebox.showinfo("Success", "Data is exported.")

	def _create_selected_export_parameters(self) -> nt.ExportParameter:
		"""
		Summarize the selected export parameter.

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
			exportToTxt=self.exportToTxt.get(),
			exportToCsv=self.exportToCsv.get(),
			exportToXlsx=self.exportToXlsx.get(),
			exportPlots=self.exportPlots.get(),
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