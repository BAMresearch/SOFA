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

from window.export_window import ExportWindow
from window.import_window import ImportWindow
from window.info_window import InfoWindow

from data.data_handler import DataHandler
from data.active_channels import channels as activeChannels
from data.import_data import restore_sofa_data
from data.export_data import export_to_sofa

from toolbar.line_plot_toolbar import LinePlotToolbar
from toolbar.heatmap_toolbar import HeatmapToolbar

class MainWindow(ttk.Frame):
	"""The main window of SOFA."""
	def __init__(self, root):
		self.root = root
		# Set tkinter dialog language to english.
		self.root.tk.eval('::msgcat::mclocale en')
		self.versionNumber = "1.0"
		self.root.title("SOFA " + self.versionNumber)
		self.sourceDirectory = os.path.abspath(os.path.dirname(__file__))
		self.iconPath = os.path.join(self.sourceDirectory, "icons", "sofa_icon_50.png")
		self.dataHandler = DataHandler()

		self.channelNames = [
			self._camel_case_to_text(channelName)
			for channelName in activeChannels.keys()
		]
		
		self.root.protocol(
			"WM_DELETE_WINDOW", 
			self._close_main_window
		)
		
		self._create_main_window()
		self._set_plot_parameters_in_data_handler()
		self._specify_data_import()

	def _create_main_window(self) -> None:
		"""Define all elements within the main window."""
		self._create_interactive_plots_frame()
		self._create_control_frame()

		# Diagram frame
		self.frameDiagrams = ttk.Labelframe(self.root, text="", padding=10, relief=RIDGE)
		self.frameDiagrams.grid(row=1, column=0, columnspan=2, padx=15, pady=15)

		self._create_line_plot_frame(self.frameDiagrams)
		self._create_heatmap_frame(self.frameDiagrams)
		self._create_histogram_frame(self.frameDiagrams)

		self.root.grid_columnconfigure(0, weight=1)
		self.root.grid_columnconfigure(1, weight=3)

		self.root.grid_rowconfigure(0, weight=1)
		self.root.grid_rowconfigure(1, weight=1)

	def _create_interactive_plots_frame(self) -> None:
		"""Define all elements within the interactive plots frame."""
		frameInteractivePlots = ttk.Labelframe(self.root, text="Interactive Plots", padding=15)
		frameInteractivePlots.grid(row=0, column=0, padx=15, pady=15, sticky=NSEW)

		self.interactiveLinePlot = tk.BooleanVar(self.root, value=False)
		checkbuttonInteractiveLinePlot = ttk.Checkbutton(
			frameInteractivePlots, 
			text="Line Plot", 
			variable=self.interactiveLinePlot,
			bootstyle="round-toggle"
		)
		checkbuttonInteractiveLinePlot.grid(row=0, column=0, padx=10, sticky=W)

		self.interactiveHeatmap = tk.BooleanVar(self.root, value=False)
		checkbuttonInteractiveHeatmap = ttk.Checkbutton(
			frameInteractivePlots, 
			text="Heatmap", 
			variable=self.interactiveHeatmap,
			bootstyle="round-toggle"
		)
		checkbuttonInteractiveHeatmap.grid(row=1, column=0, padx=10, sticky=W)

		self.interactiveHistogram = tk.BooleanVar(self.root, value=False)
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

	def _create_control_frame(self) -> None:
		"""Define all the elements within the control frame."""
		frameControl = ttk.Labelframe(self.root, text="Control", padding=15)
		frameControl.grid(row=0, column=1, columnspan=2, padx=15, pady=15, sticky=NSEW)

		buttonImport = ttk.Button(
			frameControl, text="Import Data", 
			bootstyle="", command=self._create_import_window
		)
		buttonImport.grid(row=0, column=0, padx=10, sticky=W)

		self.progressbarCurrentLabel = tk.StringVar(self.root, value="")

		progressbarLabel = ttk.Label(frameControl, textvariable=self.progressbarCurrentLabel)
		progressbarLabel.grid(row=0, column=1, padx=10)

		buttonInfo = ttk.Button(
			frameControl, text="Info", 
			bootstyle="", command=self._create_info_window
		)
		buttonInfo.grid(row=0, column=2, padx=10, sticky=E)

		buttonExport = ttk.Button(
			frameControl, text="Export Data",
			bootstyle="", command=self._create_export_window
		)
		buttonExport.grid(row=1, column=0, padx=10, pady=10, sticky=W)

		self.progressbar = ttk.Progressbar(
			frameControl,
			mode=INDETERMINATE,
            bootstyle=SUCCESS
		)
		self.progressbar.grid(row=1, column=1, padx=10)

		frameControl.columnconfigure(0, weight=1)
		frameControl.columnconfigure(1, weight=1)

		frameControl.rowconfigure(0, weight=1)
		frameControl.rowconfigure(1, weight=1)

	def _create_line_plot_frame(self, parentFrame) -> None:
		"""Define all the elements within the line plot frame."""
		frameLinePlot = ttk.Labelframe(parentFrame, text="Line Plot", padding=10)
		frameLinePlot.grid(row=0, column=0, padx=10, pady=15, sticky=N)

		labelEmpty = ttk.Label(frameLinePlot, text="")
		labelEmpty.grid(row=0, column=0, pady=15)

		figureLineplot = Figure(figsize=(6, 4.8), facecolor=("#d3d3d3"))
		self.holderFigureLineplot = FigureCanvasTkAgg(figureLineplot, frameLinePlot)
		frameToolbarLineplot = ttk.Frame(frameLinePlot)
		toolbarLineplot = LinePlotToolbar(
			self.holderFigureLineplot, frameToolbarLineplot, 
			self.dataHandler
		)
		self.holderFigureLineplot.get_tk_widget().grid(row=1, column=0)
		frameToolbarLineplot.grid(row=2, column=0)

	def _create_heatmap_frame(self, parentFrame) -> None:
		"""Define all the elements within the heatmap frame."""
		frameHeatmap= ttk.Labelframe(parentFrame, text="Heatmap", padding=10)
		frameHeatmap.grid(row=0, column=1, padx=10, pady=15, sticky=N)

		self.heatmapChannel = tk.StringVar(self.root, value="Topography")
		
		dropdownHeatmapChannel = ttk.OptionMenu(
			frameHeatmap, 
			self.heatmapChannel, 
			"",
			*self.channelNames, 
			command=self._update_heatmap,
			bootstyle=""
		)
		dropdownHeatmapChannel.grid(row=0, column=0, pady=10, sticky=E)

		figureHeatmap = Figure(figsize=(6, 4.8), facecolor=("#d3d3d3"))
		self.holderFigureHeatmap = FigureCanvasTkAgg(figureHeatmap, frameHeatmap)
		frameToolbarHeatmap = ttk.Frame(frameHeatmap)
		toolbarHeatmap = HeatmapToolbar(
			self.holderFigureHeatmap, frameToolbarHeatmap, 
			self.dataHandler
		)
		self.holderFigureHeatmap.get_tk_widget().grid(row=1, column=0)
		frameToolbarHeatmap.grid(row=2, column=0)

	def _create_histogram_frame(self, parentFrame) -> None:
		"""Define all the elements within the histogram frame."""
		frameHistogram = ttk.Labelframe(parentFrame, text="Histogram", padding=10)
		frameHistogram.grid(row=0, column=2, padx=10, pady=15)

		self.zoomHistogram = tk.BooleanVar(self.root, value=False)
		checkbuttonZoom = ttk.Checkbutton(
			frameHistogram, 
			text="Zoom", 
			variable=self.zoomHistogram,
			bootstyle="round-toggle")
		checkbuttonZoom.grid(row=0, column=0, padx=10, sticky=W)

		self.histogramChannel = tk.StringVar(self.root, value="Topography")
		
		dropdownHistogramChannel = ttk.OptionMenu(
			frameHistogram, 
			self.histogramChannel, 
			"",
			*self.channelNames, 
			command=self._update_histogram,
			bootstyle=""
		)
		dropdownHistogramChannel.grid(row=0, column=0, columnspan=4, pady=10, sticky=E)

		figureHistogram = Figure(figsize=(3.5, 4.8), facecolor=("#d3d3d3"))
		self.holderFigureHistogram = FigureCanvasTkAgg(figureHistogram, frameHistogram)
		self.holderFigureHistogram.get_tk_widget().grid(row=1, column=0, columnspan=4)

		labelNumberOfBins = ttk.Label(frameHistogram, text="Number of bins:")
		labelNumberOfBins.grid(row=2, column=0, padx=10, sticky=SW)

		self.numberOfBins = tk.IntVar(self.root, value=100)

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
		ImportWindow(self.dataHandler, self.set_filename)

	def set_filename(self, filename) -> None:
		"""Display the name of the current data files."""
		self.frameDiagrams.configure(text=filename)

	def _create_export_window(self) -> None:
		"""Open the window to export data."""
		ExportWindow(self.dataHandler)

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

		self.root.update_idletasks()

	def stop_progressbar(self) -> None:
		"""Stop the progressbar."""
		self.progressbar.stop()
		self.progressbarCurrentLabel.set("")

		self.root.update_idletasks()

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

		self.root.quit()
		self.root.destroy()

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