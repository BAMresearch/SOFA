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

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from gui.export_window import ExportWindow
from gui.import_window import ImportWindow

from data_processing.data_handler import DataHandler
from data_processing.active_channels import channels as activeChannels
from data_processing.import_data import restore_sofa_data
from data_processing.export_data import export_to_sofa

from toolbar.line_plot_toolbar import LinePlotToolbar
from toolbar.heatmap_toolbar import HeatmapToolbar

class MainWindow(ttk.Frame):
	"""The main window of SOFA."""
	def __init__(self, root):
		super().__init__(root, padding=20)

		self.pack(fill=BOTH, expand=YES)

		# Set tkinter dialog language to english.
		self.tk.eval('::msgcat::mclocale en')
		self.sourceDirectory = os.path.abspath(os.path.dirname(__file__))
		self.dataHandler = DataHandler()

		self.channelNames = [
			self._camel_case_to_text(channelName)
			for channelName in activeChannels.keys()
		]

		self.colorPlot = "#e6f7f4"
		'''
		root.protocol(
			"WM_DELETE_WINDOW", 
			self._close_main_window
		)
		'''
		
		self._create_main_window()
		self._set_plot_parameters_in_data_handler()

	def _create_main_window(self) -> None:
		"""Define all elements within the main window."""
		self._create_first_row()
		self._create_second_row()

	def _create_first_row(self) -> None: 
		""""""
		frameFirstRow = ttk.Frame(self)
		frameFirstRow.pack(fill=X, expand=YES, pady=(0, 20))

		self._create_frame_files(frameFirstRow)
		self._create_frame_active_data(frameFirstRow)
		self._create_frame_interactive_plots(frameFirstRow)
		self._create_frame_control(frameFirstRow)

	def _create_second_row(self) -> None:
		""""""
		frameSecondRow = ttk.Frame(self)
		frameSecondRow.pack(fill=X, expand=YES)

		self._create_line_plot_frame(frameSecondRow)
		self._create_heatmap_frame(frameSecondRow)
		self._create_histogram_frame(frameSecondRow)

	def _create_frame_files(self, frameParent) -> None: 
		"""Define all elements within the files frame."""
		frameFiles = ttk.Labelframe(frameParent, text="Files", padding=15)
		frameFiles.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 15))

		buttonImport = ttk.Button(
			frameFiles, text="Import Data", 
			bootstyle="", command=self._create_import_window
		)
		buttonImport.grid(row=0, column=0, padx=10, sticky=W)

		buttonExport = ttk.Button(
			frameFiles, text="Export Data",
			bootstyle="", command=self._create_export_window
		)
		buttonExport.grid(row=1, column=0, padx=10, pady=10, sticky=W)

	def _create_frame_active_data(self, frameParent) -> None: 
		""""""
		frameActiveData = ttk.Labelframe(frameParent, text="Active Data", padding=15)
		frameActiveData.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 15))

		self.stringVarActiveData = ttk.StringVar(self, value="")
		self.stringVarActiveDataLocation = ttk.StringVar(self, value="")
		self.stringVarActiveDataSize = ttk.StringVar(self, value="")

		labelActiveData = ttk.Label(
			frameActiveData, 
			text="Name:"
		)
		labelActiveData.grid(row=0, column=0, padx=10, sticky=W)

		valueActiveData = ttk.Label(
			frameActiveData,
			textvariable=self.stringVarActiveData
		)
		valueActiveData.grid(row=0, column=1, padx=10, sticky=W)

		labelActiveDataLocation = ttk.Label(
			frameActiveData, 
			text="Location:"
		)
		labelActiveDataLocation.grid(row=1, column=0, padx=10, sticky=W)

		valueActiveDataLocation = ttk.Label(
			frameActiveData,
			textvariable=self.stringVarActiveDataLocation
		)
		valueActiveDataLocation.grid(row=1, column=1, padx=10, sticky=W)

		labelActiveDataSize = ttk.Label(
			frameActiveData, 
			text="Size:"
		)
		labelActiveDataSize.grid(row=2, column=0, padx=10, sticky=W)

		valueActiveDataSize = ttk.Label(
			frameActiveData,
			textvariable=self.stringVarActiveDataSize
		)
		valueActiveDataSize.grid(row=2, column=1, padx=10, sticky=W)

	def _create_frame_interactive_plots(self, frameParent) -> None:
		"""Define all elements within the interactive plots frame."""
		frameInteractivePlots = ttk.Labelframe(frameParent, text="Interactive Plots", padding=15)
		frameInteractivePlots.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 15))

		self.interactiveLinePlot = tk.BooleanVar(self, value=False)
		checkbuttonInteractiveLinePlot = ttk.Checkbutton(
			frameInteractivePlots, 
			text="Line Plot", 
			variable=self.interactiveLinePlot,
			bootstyle="round-toggle"
		)
		checkbuttonInteractiveLinePlot.grid(row=0, column=0, padx=10, sticky=W)

		self.interactiveHeatmap = tk.BooleanVar(self, value=False)
		checkbuttonInteractiveHeatmap = ttk.Checkbutton(
			frameInteractivePlots, 
			text="Heatmap", 
			variable=self.interactiveHeatmap,
			bootstyle="round-toggle"
		)
		checkbuttonInteractiveHeatmap.grid(row=1, column=0, padx=10, sticky=W)

		self.interactiveHistogram = tk.BooleanVar(self, value=False)
		checkbuttonInteractiveHistogram = ttk.Checkbutton(
			frameInteractivePlots, 
			text="Histogram", 
			variable=self.interactiveHistogram,
			bootstyle="round-toggle"
		)
		checkbuttonInteractiveHistogram.grid(row=2, column=0, padx=10, sticky=W)

		buttonUpdatePlots = ttk.Button(
			frameInteractivePlots, 
			text="Update Plots", 
			command=self._update_plots,
			bootstyle=""
		)
		buttonUpdatePlots.grid(row=1, column=2, padx=10, sticky=E)

		frameInteractivePlots.columnconfigure(0, weight=1)
		frameInteractivePlots.columnconfigure(1, weight=1)
		frameInteractivePlots.columnconfigure(2, weight=1)

	def _create_frame_control(self, frameParent) -> None:
		"""Define all the elements within the control frame."""
		frameControl = ttk.Labelframe(frameParent, text="Control", padding=15)
		frameControl.pack(side=LEFT, fill=BOTH, expand=YES)

		self.progressbarCurrentLabel = tk.StringVar(self, value="Test")

		progressbarLabel = ttk.Label(frameControl, textvariable=self.progressbarCurrentLabel)
		progressbarLabel.grid(row=0, column=0, padx=10)

		self.progressbar = ttk.Progressbar(
			frameControl,
			mode=INDETERMINATE,
            bootstyle=SUCCESS
		)
		self.progressbar.grid(row=1, column=0, padx=10)
		
	def _create_line_plot_frame(self, frameParent) -> None:
		"""Define all the elements within the line plot frame."""
		frameLinePlot = ttk.Labelframe(frameParent, text="Line Plot", padding=10)
		frameLinePlot.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 15))

		labelEmpty = ttk.Label(frameLinePlot, text="")
		labelEmpty.grid(row=0, column=0, pady=15)

		figureLineplot = Figure(figsize=(6, 4.8), facecolor=self.colorPlot)
		self.holderFigureLineplot = FigureCanvasTkAgg(figureLineplot, frameLinePlot)
		frameToolbarLineplot = ttk.Frame(frameLinePlot)
		toolbarLineplot = LinePlotToolbar(
			self.holderFigureLineplot, frameToolbarLineplot, 
			self.dataHandler
		)
		self.holderFigureLineplot.get_tk_widget().grid(row=1, column=0)
		frameToolbarLineplot.grid(row=2, column=0)

	def _create_heatmap_frame(self, frameParent) -> None:
		"""Define all the elements within the heatmap frame."""
		frameHeatmap= ttk.Labelframe(frameParent, text="Heatmap", padding=10)
		frameHeatmap.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 15))

		self.heatmapChannel = tk.StringVar(self, value="Topography")
		
		dropdownHeatmapChannel = ttk.OptionMenu(
			frameHeatmap, 
			self.heatmapChannel, 
			"",
			*self.channelNames, 
			command=self._update_heatmap,
			bootstyle=""
		)
		dropdownHeatmapChannel.grid(row=0, column=0, pady=10, sticky=E)

		figureHeatmap = Figure(figsize=(6, 4.8), facecolor=self.colorPlot)
		self.holderFigureHeatmap = FigureCanvasTkAgg(figureHeatmap, frameHeatmap)
		frameToolbarHeatmap = ttk.Frame(frameHeatmap)
		toolbarHeatmap = HeatmapToolbar(
			self.holderFigureHeatmap, frameToolbarHeatmap, 
			self.dataHandler
		)
		self.holderFigureHeatmap.get_tk_widget().grid(row=1, column=0)
		frameToolbarHeatmap.grid(row=2, column=0)

	def _create_histogram_frame(self, frameParent) -> None:
		"""Define all the elements within the histogram frame."""
		frameHistogram = ttk.Labelframe(frameParent, text="Histogram", padding=10)
		frameHistogram.pack(side=LEFT, fill=BOTH, expand=YES)

		self.zoomHistogram = tk.BooleanVar(self, value=False)
		checkbuttonZoom = ttk.Checkbutton(
			frameHistogram, 
			text="Zoom", 
			variable=self.zoomHistogram,
			bootstyle="round-toggle")
		checkbuttonZoom.grid(row=0, column=0, padx=10, sticky=W)

		self.histogramChannel = tk.StringVar(self, value="Topography")
		
		dropdownHistogramChannel = ttk.OptionMenu(
			frameHistogram, 
			self.histogramChannel, 
			"",
			*self.channelNames, 
			command=self._update_histogram,
			bootstyle=""
		)
		dropdownHistogramChannel.grid(row=0, column=0, columnspan=4, pady=10, sticky=E)

		figureHistogram = Figure(figsize=(3.5, 4.8), facecolor=self.colorPlot)
		self.holderFigureHistogram = FigureCanvasTkAgg(figureHistogram, frameHistogram)
		self.holderFigureHistogram.get_tk_widget().grid(row=1, column=0, columnspan=4)

		labelNumberOfBins = ttk.Label(frameHistogram, text="Number of bins:")
		labelNumberOfBins.grid(row=2, column=0, padx=10, sticky=SW)

		self.numberOfBins = tk.IntVar(self, value=100)

		entryBins = ttk.Entry(frameHistogram, textvariable=self.numberOfBins)
		entryBins.grid(row=3, column=0, padx=10, sticky=NW)

		buttonReduceMin = ttk.Button(
			frameHistogram, 
			text="-", 
			command=lambda: self._restrict_histogram("min down"),
			bootstyle=""
		)
		buttonReduceMin.grid(row=2, column=1, pady=5, sticky=E)

		labelMin = ttk.Label(frameHistogram, text="Min")
		labelMin.grid(row=2, column=2, pady=5, sticky=E)

		buttonIncreaseMin = ttk.Button(
			frameHistogram, 
			text="+",
			command=lambda: self._restrict_histogram("min up"), 
			bootstyle=""
		)
		buttonIncreaseMin.grid(row=2, column=3, pady=5, sticky=E)

		buttonReduceMax = ttk.Button(
			frameHistogram, 
			text="-", 
			command=lambda: self._restrict_histogram("max down"),
			bootstyle=""
		)
		buttonReduceMax.grid(row=3, column=1, pady=5, sticky=E)

		labelMax = ttk.Label(frameHistogram, text="Max")
		labelMax.grid(row=3, column=2, pady=5, sticky=E)

		buttonIncreaseMax = ttk.Button(
			frameHistogram, 
			text="+",
			command=lambda: self._restrict_histogram("max up"), 
			bootstyle=""
		)
		buttonIncreaseMax.grid(row=3, column=3, pady=5, sticky=E)

		frameHistogram.columnconfigure(0, weight=1)
		frameHistogram.columnconfigure(1, weight=1)
		frameHistogram.columnconfigure(2, weight=1)
		frameHistogram.columnconfigure(3, weight=1)

	def _set_plot_parameters_in_data_handler(self) -> None:
		"""Give the datahandler all relevant parameters to handle the plots."""
		plotParameters = {
			"holderLinePlot": self.holderFigureLineplot,
			"holderHeatmap": self.holderFigureHeatmap,
			"holderHistogram": self.holderFigureHistogram,
			"currentChannelHeatmap": self.heatmapChannel,
			"currentChannelHistogram": self.histogramChannel,
			"interactiveLinePlot": self.interactiveLinePlot,
			"interactiveHeatmap": self.interactiveHeatmap,
			"interactiveHistogram": self.interactiveHistogram,
			"zoomHistogram": self.zoomHistogram,
			"numberOfBins": self.numberOfBins
		}

		self.dataHandler.set_plot_parameters(plotParameters)

	def _create_import_window(self) -> None:
		"""Open the window to import data."""
		toplevelImport = ttk.Toplevel("Import Data")
		ImportWindow(
			toplevelImport,
			self.dataHandler, 
			self.set_filename
		)

	def set_filename(self, filename) -> None:
		"""Display the name of the current data files."""
		self.frameDiagrams.configure(text=filename)

	def _create_export_window(self) -> None:
		"""Open the window to export data."""
		toplevelExport = ttk.Toplevel("Export Data")
		ExportWindow(
			toplevelExport,
			self.dataHandler
		)

	def _create_info_window(self) -> None:
		"""Open the info window."""
		InfoWindow(self.versionNumber)

	def _update_plots(self) -> None:
		"""Update the inactive data points in every plot."""
		# use decorator with args to start/end progressbar
		self.start_progressbar()
		self.dataHandler.update_plots()
		self.stop_progressbar()

	def _update_heatmap(self, newHeatmapChannel) -> None:
		"""Update the displayed channel in the heatmap.

		Parameters:
			newHeatmapChannel(str): Name of the new channel.
		"""
		self.dataHandler.update_heatmap()

	def _update_histogram(self, newHistogramChannel) -> None:
		"""Update the displayed channel in the histogram.

		Parameters:
			newHeatmapChannel(str): Name of the new channel.
		"""
		self.dataHandler.update_histogram()

	def _restrict_histogram(self, direction) -> None:
		"""Change the minimum or maximum border for the histogram values.

		Parameters:
			direction(str): .
		"""
		self.start_progressbar()
		self.dataHandler.restrict_histogram(direction)

		if self.interactiveHistogram.get():
			self.dataHandler.update_plots()
		else:
			self.dataHandler.update_histogram()

		self.stop_progressbar()

	def start_progressbar(self) -> None:
		"""Start the progressbar."""
		self.progressbarCurrentLabel.set("Updating data")
		self.progressbar.start()

		self.update_idletasks()

	def stop_progressbar(self) -> None:
		"""Stop the progressbar."""
		self.progressbar.stop()
		self.progressbarCurrentLabel.set("")

		self.update_idletasks()

	@staticmethod
	def _camel_case_to_text(inputString: str) -> str:
		"""Converts string from lower CamelCase to a title format.

		Parameters:
			inputString(str): String in lower CamelCase.

		Returns:
			outputString(str): String as title text.
		"""
		return ''.join(
			[
				' ' + character.lower() 
				if character.isupper() 
				else character 
				for character in inputString
			]
		).title()

	def _close_main_window(self) -> None:
		"""Ask the user if he wants to save the session before closing sofa."""
		saveSession = messagebox.askyesno(
			"Save session", 
			"Do you want to save the current session before closing SOFA?"
		)
		
		if saveSession:
			export_to_sofa(
				self.dataHandler, 
				self.sourceDirectory,
				".sofaSession",
				hidden=True
			)

		self.quit()
		self.destroy()

	def _specify_data_import(self) -> None:
		"""Ask the user if he wants to restore the last session or import new data."""
		loadLastSession = messagebox.askyesno(
			"Load last session", 
			"Do you want to load the last session?"
		)
		
		if loadLastSession:
			self._restore_session()
		else:
			self._create_import_window()

	def _restore_session(self) -> None:
		"""Try to restore the last session."""
		try:
			filePath = os.path.join(
				self.sourceDirectory,
				".sofaSessionBackup"
			)
			backupData = restore_sofa_data(filePath)
			self.set_filename_in_labeled_frame(backupData["generalData"]["filename"])
			self.dataHandler.restore_session_data(backupData)
			self.dataHandler.display_imported_data()
		except FileNotFoundError:
			messagebox.showerror(
				"Error", 
				"Could not find a session file. Please import data."
			)
			self._create_import_window()