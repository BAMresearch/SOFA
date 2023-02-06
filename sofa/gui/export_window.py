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

import data_processing.export_data as exp_data

class ExportWindow(ttk.Frame):
	"""A subwindow to handle the data export."""
	def __init__(self, root, dataHandler):
		super().__init__(root)
		
		self.pack(fill=BOTH, expand=YES)

		self.dataHandler = dataHandler

		self._create_window()

	def _create_window(self) -> None:
		"""Define all elements within the export window."""
		self._create_frame_data_location()
		self._create_frame_data_types()
		self._create_export_button()
		self._create_progressbar()

	def _create_frame_data_location(self) -> None:
		"""Define all elements within the data location frame."""
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
		"""Define all elements within the data types frame."""
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
		"""Define the export button."""
		rowExportButton = ttk.Frame(self)
		rowExportButton.pack(fill=X, expand=YES, pady=(20, 10))

		buttonExportData = ttk.Button(
			rowExportButton,
			text="Export Data",
			command=self._export_data
		)
		buttonExportData.pack(side=LEFT, padx=15)

	def _create_progressbar(self) -> None:
		"""Define the progressbar."""	
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
		"""Select the directory in which the data will be saved."""
		folderPath = fd.askdirectory(
			title="Select directory",
			parent=self
		)

		if folderPath:
			self.folderPath.set(folderPath)

	def _export_data(self) -> messagebox:
		"""Export the current state of the data with the selected options.

		Returns:
			userFeedback(messagebox): Informs the user whether the data could be saved or not.
		"""
		# Check if a folder name is selected.
		if not self.folderName.get():
			return messagebox.showerror(
				"Error", 
				"Please specify a name for the ouput folder.", 
				parent=self
			)

		# Check if a output folder is selected.
		if not os.path.isdir(self.folderPath.get()):
			return messagebox.showerror(
				"Error", 
				"Please specify a location to save your data.", 
				parent=self
			)

		selectedExportParameters = self._create_selected_export_parameters()

		exp_data.export_data(
			self.dataHandler,
			selectedExportParameters,
			self.progressbar,
			self.progressbarCurrentLabel
		)
		# Close window
		self.destroy()

		return messagebox.showinfo("Success", "Data is saved.")

	def _create_selected_export_parameters(self) -> NamedTuple:
		"""Summarize the selected export options for easier use.

		Returns:
			ExportOptions(namedtuple): Contains the selected export opotions.
		"""
		ExportOptions = namedtuple(
			"ExportOptions",
			[
				"folderName",
				"folderPath",
				"exportToSofa",
				"exportToTex",
				"exportToTxt",
				"exportToHdf5",
				"exportToExcel",
				"exportPlots",
			]	
		)

		return ExportOptions(
			folderName=self.folderName.get(),
			folderPath=self.folderPath.get(),
			exportToSofa=self.exportToSofa.get(),
			exportToTex=self.exportToTex.get(),
			exportToTxt=self.exportToTxt.get(),
			exportToHdf5=self.exportToHdf5.get(),
			exportToExcel=self.exportToExcel.get(),
			exportPlots=self.exportPlots.get(),
		)