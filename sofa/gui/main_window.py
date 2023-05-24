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
from typing import Tuple
import functools

import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from ttkbootstrap.constants import *

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from interfaces.gui_interface import GUIInterface
from gui.export_window import ExportWindow
from gui.import_window import ImportWindow
from data_processing.calculate_channel_data import active_channels as activeChannels
from toolbars.line_plot_toolbar import LinePlotToolbar
from toolbars.heatmap_toolbar import HeatmapToolbar

def decorator_check_imported_data_set_with_feedback(function):
	"""
	Check if the required path for the measurement
	folder is set.
	"""
	@functools.wraps(function)
	def wrapper_check_imported_data_set(self, *args):
		if self.guiInterface.check_imported_data_set() == False:
			return messagebox.showinfo(
				"Error", 
				"No imported data sets.", 
				parent=self
			)
		else:
			function(self, *args)

	return wrapper_check_imported_data_set

def decorator_check_imported_data_set(function):
	"""
	Check if the required path for the measurement
	folder is set.
	"""
	@functools.wraps(function)
	def wrapper_check_imported_data_set(self, *args):
		if self.guiInterface.check_imported_data_set():
			function(self, *args)

	return wrapper_check_imported_data_set

class MainWindow(ttk.Frame):
	"""
	The main window of SOFA.

	Attributes
	----------
	guiInterface : GUIInterface

	sourceDirectory : str

	channelNames : list[str]
	"""
	def __init__(self, root):
		"""
		"""
		super().__init__(root, padding=20)

		self.pack(fill=BOTH, expand=YES)

		self.guiInterface = GUIInterface()

		self.channelNames = [
			self._camel_case_to_text(channelName)
			for channelName in activeChannels.keys()
		]

		self.colorPlot = "#e6f7f4"
		
		self._create_main_window()
		self._set_gui_parameters_in_gui_interface()

	def _create_main_window(self) -> None:
		"""
		Define all elements within the main window.
		"""
		self._create_first_row()
		self._create_second_row()

	def _create_first_row(self) -> None: 
		"""
		Define all frames in the first row, consisting of
		the data import and export, information about the 
		imported data, the control of the linked plot and 
		the control.
		"""
		frameFirstRow = ttk.Frame(self)
		frameFirstRow.pack(fill=X, expand=YES, pady=(0, 20))

		self._create_frame_files(frameFirstRow)
		self._create_frame_active_data(frameFirstRow)
		self._create_frame_linked_plots(frameFirstRow)

	def _create_second_row(self) -> None:
		"""
		Define all figures in the second row, consisting of 
		the line plot, the heamtap and histogram. 
		"""
		frameSecondRow = ttk.Frame(self)
		frameSecondRow.pack(fill=X, expand=YES)

		self._create_line_plot_frame(frameSecondRow)
		self._create_heatmap_frame(frameSecondRow)
		self._create_histogram_frame(frameSecondRow)

	def _create_frame_files(
		self, 
		frameParent: ttk.Frame
	) -> None: 
		"""
		Define a button to import and export data.

		Parameters
		----------
		frameParent : ttk.Frame
			Corresponding row of the main window.
		"""
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

	def _create_frame_active_data(
		self, 
		frameParent: ttk.Frame
	) -> None: 
		"""
		Define labels to display general information about
		the imported measurement data.

		Parameters
		----------
		frameParent : ttk.Frame
			Corresponding row of the main window.
		"""
		frameActiveData = ttk.Labelframe(frameParent, text="Active Data", padding=15)
		frameActiveData.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 15))

		self.forceVolumes = []
		self.activeForceVolume = ttk.StringVar(self, value="Force Volume")

		self.stringVarActiveData = ttk.StringVar(self, value="")
		self.stringVarActiveDataLocation = ttk.StringVar(self, value="")
		self.stringVarActiveDataSize = ttk.StringVar(self, value="")
		
		self.dropdownForceVolumes = ttk.OptionMenu(
			frameActiveData, 
			self.activeForceVolume, 
			"",
			*self.forceVolumes, 
			command=self._update_force_volume,
			bootstyle=""
		)
		self.dropdownForceVolumes.grid(row=0, column=2, padx=10, sticky=E)

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

		labelActiveDataSize = ttk.Label(
			frameActiveData, 
			text="Size:"
		)
		labelActiveDataSize.grid(row=1, column=0, padx=10, sticky=W)

		valueActiveDataSize = ttk.Label(
			frameActiveData,
			textvariable=self.stringVarActiveDataSize
		)
		valueActiveDataSize.grid(row=1, column=1, padx=10, sticky=W)

		labelActiveDataLocation = ttk.Label(
			frameActiveData, 
			text="Location:"
		)
		labelActiveDataLocation.grid(row=2, column=0, padx=10, sticky=W)

		valueActiveDataLocation = ttk.Label(
			frameActiveData,
			textvariable=self.stringVarActiveDataLocation
		)
		valueActiveDataLocation.grid(row=2, column=1, padx=10, sticky=W)

	def _create_frame_linked_plots(
		self, 
		frameParent: ttk.Frame
	) -> None:
		"""
		Define checkboxes to toggle the connection between the 
		different plots.
		
		Parameters
		----------
		frameParent : ttk.Frame
			Corresponding row of the main window.
		"""
		frameInteractivePlots = ttk.Labelframe(frameParent, text="Linked Plots", padding=15)
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
		
	def _create_line_plot_frame(
		self, 
		frameParent: ttk.Frame
	) -> None:
		"""
		Define the figure for the line plot.

		Parameters
		----------
		frameParent : ttk.Frame
			Corresponding row of the main window.
		"""
		frameLinePlot = ttk.Labelframe(frameParent, text="Line Plot", padding=10)
		frameLinePlot.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 15))

		self.displayAverage = tk.BooleanVar(self, value=False)
		checkbuttonZoom = ttk.Checkbutton(
			frameLinePlot, 
			text="Display Average", 
			variable=self.displayAverage,
			command=self._update_line_plot,
			bootstyle="round-toggle")
		checkbuttonZoom.grid(row=0, column=0, padx=5, pady=15, sticky=W)

		self.displayErrorbar = tk.BooleanVar(self, value=False)
		checkbuttonZoom = ttk.Checkbutton(
			frameLinePlot, 
			text="Display Errorbar", 
			variable=self.displayErrorbar,
			command=self._update_line_plot,
			bootstyle="round-toggle")
		checkbuttonZoom.grid(row=0, column=1, padx=5)

		self.displayInactiveCurves = tk.BooleanVar(self, value=False)
		checkbuttonZoom = ttk.Checkbutton(
			frameLinePlot, 
			text="Display Inactive Curves", 
			variable=self.displayInactiveCurves,
			command=self._update_line_plot,
			bootstyle="round-toggle")
		checkbuttonZoom.grid(row=0, column=2, padx=5, sticky=E)

		figureLineplot = Figure(figsize=(6, 4.8), facecolor=self.colorPlot)
		self.holderFigureLineplot = FigureCanvasTkAgg(figureLineplot, frameLinePlot)
		frameToolbarLineplot = ttk.Frame(frameLinePlot)
		toolbarLineplot = LinePlotToolbar(
			self.holderFigureLineplot, frameToolbarLineplot, 
			self.guiInterface
		)
		self.holderFigureLineplot.get_tk_widget().grid(row=1, column=0, columnspan=3)
		frameToolbarLineplot.grid(row=2, column=0, columnspan=3)

	def _create_heatmap_frame(
		self, 
		frameParent: ttk.Frame
	) -> None:
		"""
		Define the figure for the heatmap and a dropdown 
		menu to select the displayed channel.

		Parameters
		----------
		frameParent : ttk.Frame
			Corresponding row of the main window.
		"""
		frameHeatmap= ttk.Labelframe(frameParent, text="Heatmap", padding=10)
		frameHeatmap.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 15))

		self.heatmapChannel = tk.StringVar(self, value="Topography")
		
		dropdownHeatmapChannel = ttk.OptionMenu(
			frameHeatmap, 
			self.heatmapChannel, 
			"",
			*self.channelNames, 
			command=self._update_heatmap_channel,
			bootstyle=""
		)
		dropdownHeatmapChannel.grid(row=0, column=0, pady=10, sticky=E)

		figureHeatmap = Figure(figsize=(6, 4.8), facecolor=self.colorPlot)
		self.holderFigureHeatmap = FigureCanvasTkAgg(figureHeatmap, frameHeatmap)
		frameToolbarHeatmap = ttk.Frame(frameHeatmap)
		toolbarHeatmap = HeatmapToolbar(
			self.holderFigureHeatmap, frameToolbarHeatmap, 
			self.guiInterface
		)
		self.holderFigureHeatmap.get_tk_widget().grid(row=1, column=0)
		frameToolbarHeatmap.grid(row=2, column=0)

	def _create_histogram_frame(self, frameParent: ttk.Frame) -> None:
		"""
		Define the figure for the histogram, a dropdown 
		menu to select the displayed channel, an entry
		to set the number of bins for the histogram
		and some buttons to change the minimum and 
		maximum value of the displayed channel.

		Parameters
		----------
		frameParent : ttk.Frame
			Corresponding row of the main window.
		"""
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
			command=self._update_histogram_channel,
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

	def _set_gui_parameters_in_gui_interface(self) -> None:
		"""
		Give the GUIInterface all relevant parameters to handle the plots.
		"""
		guiParameters = {
			"keyActiveForceVolume": self.activeForceVolume,
			"holderLinePlot": self.holderFigureLineplot,
			"linkedLinePlot": self.interactiveLinePlot,
			"displayAverage": self.displayAverage,
			"displayErrorbar": self.displayErrorbar,
			"displayInactiveCurves": self.displayInactiveCurves,
			"holderHeatmap": self.holderFigureHeatmap,
			"activeChannelHeatmap": self.heatmapChannel,
			"linkedHeatmap": self.interactiveHeatmap,
			"holderHistogram": self.holderFigureHistogram,
			"activeChannelHistogram": self.histogramChannel,
			"linkedHistogram": self.interactiveHistogram,
			"zoomHistogram": self.zoomHistogram,
			"numberOfBins": self.numberOfBins
		}
		self.guiInterface.set_gui_parameters(guiParameters)

	def set_data_active_force_volume(
		self,
		name: str,
		size: Tuple[int],
		location: str
	) -> None:
		"""

		Parameters
		----------
		name : str
			
		size : tuple[int]

		location : str

		"""
		self.stringVarActiveData.set(name)
		self.stringVarActiveDataSize.set(str(size))
		self.stringVarActiveDataLocation.set(location)

		self.forceVolumes.append(name)
		self._update_dropdown_force_volumes()

	def _update_dropdown_force_volumes(self) -> None:
		"""
		Update the dropdown menu options for the
		imported force volumes.
		"""
		self.dropdownForceVolumes.set_menu("", *self.forceVolumes)

	def _create_import_window(self) -> None:
		"""
		Create a subwindow to import data.
		"""
		toplevelImport = ttk.Toplevel("Import Data")
		ImportWindow(
			toplevelImport,
			self.guiInterface, 
			self.set_data_active_force_volume
		)

	@decorator_check_imported_data_set_with_feedback
	def _create_export_window(self) -> None:
		"""
		Create a subwindow to export data.
		"""
		toplevelExport = ttk.Toplevel("Export Data")
		ExportWindow(
			toplevelExport,
			self.guiInterface
		)

	def _update_force_volume(self, _) -> None: 
		"""
		Update the active force volume.
		"""
		self.guiInterface.plot_active_force_volume()

	@decorator_check_imported_data_set_with_feedback
	def _update_plots(self) -> None:
		"""
		Update the inactive data points in every plot.
		"""
		self.guiInterface.update_active_force_volume_plots()

	@decorator_check_imported_data_set
	def _update_line_plot(self) -> None:
		"""
		Update the line plot.
		"""
		self.guiInterface.update_line_plot()

	@decorator_check_imported_data_set
	def _update_heatmap_channel(self, _) -> None:
		"""
		Update the displayed channel in the heatmap.
		"""
		self.guiInterface.plot_heatmap()

	@decorator_check_imported_data_set
	def _update_histogram_channel(self, _) -> None:
		"""
		Update the displayed channel in the histogram.
		"""
		self.guiInterface.plot_histogram()

	@decorator_check_imported_data_set_with_feedback
	def _restrict_histogram(self, direction) -> None:
		"""
		Change the minimum or maximum border for the histogram values.

		Parameters
		----------
		direction : str
			Indicates whether the minimum or maximum is 
			decreased or increased.
		"""
		self.guiInterface.restrict_histogram(direction)
		self.guiInterface.update_inactive_data_points_histogram()

	@staticmethod
	def _camel_case_to_text(inputString: str) -> str:
		"""
		Converts string from lower CamelCase to a title format.

		Parameters
		----------
		inputString : str
			String in lower CamelCase.

		Returns
		-------
		outputString : str
			String as title text.
		"""
		return ''.join(
			[
				' ' + character.lower() 
				if character.isupper() 
				else character 
				for character in inputString
			]
		).title()