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
from typing import Dict, List, Tuple
import functools

import data_processing.mutate_histogram_data as mhd 
import data_processing.named_tuples as nt
import data_visualization.plot_data as plt_data
from force_spectroscopy_data.force_volume import ForceVolume
from interfaces.plot_interface import PlotInterface

def decorator_get_active_data_set(function):
	"""
	Get the force volume and plot interface of the 
	current selected data set.
	"""
	@functools.wraps(function)
	def wrapper_get_active_data_set(self, *args, **kwargs):
		activeForceVolume = self.get_active_force_volume()
		activePlotInterface = self.get_active_plot_interface()
		function(self, activeForceVolume, activePlotInterface, *args, **kwargs)

	return wrapper_get_active_data_set

def decorator_get_active_force_volume(function):
	"""
	Get current selected force volume.
	"""
	@functools.wraps(function)
	def wrapper_get_active_force_volume(self, *args, **kwargs):
		activeForceVolume = self.get_active_force_volume()
		function(self, activeForceVolume, *args, **kwargs)

	return wrapper_get_active_force_volume

def decorator_get_active_plot_interface(function):
	"""
	Get current selected plot interface.
	"""
	@functools.wraps(function)
	def wrapper_get_active_plot_interface(self, *args, **kwargs):
		activePlotInterface = self.get_active_plot_interface()
		function(self, activePlotInterface, *args, **kwargs)

	return wrapper_get_active_plot_interface

def decorator_get_active_heatmap_channel(function):
	"""
	Get name of current selected channel of heatmap.
	"""
	@functools.wraps(function)
	def wrapper_get_active_force_volume(self, *args, **kwargs):
		keyActiveHeatmapChannel = self._text_to_camel_case(
			self.heatmapParameters.activeChannel.get()
		)
		function(self, keyActiveHeatmapChannel, *args, **kwargs)

	return wrapper_get_active_force_volume

def decorator_get_active_histogram_channel(function):
	"""
	Get name of current selected channel of histogram.
	"""
	@functools.wraps(function)
	def wrapper_get_active_force_volume(self, *args, **kwargs):
		keyActiveHistogramChannel = self._text_to_camel_case(
			self.histogramParameters.activeChannel.get()
		)
		function(self, keyActiveHistogramChannel, *args, **kwargs)

	return wrapper_get_active_force_volume

class GUIInterface():
	"""
	The interface between the GUI of SOFA and the imported force volumes.
	Handles the user input, from the GUI or the toolbars.

	Attributes
	----------
	importedDataSets : Dict
		Contains the imported force volumes and their associated
		PlotInterfaces.
	keyActiveForceVolume : ttk.StringVar
		Variable that stores the name of active force volume.
	linePlotParameters : nt.LinePlotParameters
		Contains all GUI elements of the main window
		which are related to the line plot.
	heatmapParameters : nt.HeatmapParameters
		Contains all GUI elements of the main window
		which are related to the heatmap.
	histogramParameters : nt.HistogramParameters
		Contains all GUI elements of the main window
		which are related to the histogram.
	"""
	def __init__(self) -> None:
		"""
		Initialize a blank gui interface. 
		"""
		self.importedDataSets: Dict = {}
		self.keyActiveForceVolume: ttk.StringVar
		self.linePlotParameters: nt.LinePlotParameters 
		self.heatmapParameters: nt.HeatmapParameters
		self.histogramParameters: nt.HistogramParameters

	def set_gui_parameters(self, guiParameters: Dict) -> None:
		"""
		Set the plot parameters of the main window of SOFA
		in the gui interface.
		
		Parameters
		----------
		guiParameters : dict
			Contains the relevant parameters of every plot
			in the main window of SOFA.
		"""
		self.keyActiveForceVolume = guiParameters["keyActiveForceVolume"]

		self.linePlotParameters = nt.LinePlotParameters(
			linked=guiParameters["linkedLinePlot"],
			holder=guiParameters["holderLinePlot"],
			plotInactive=guiParameters["displayInactiveCurves"],
			plotAverage=guiParameters["displayAverage"],
			plotErrorbar=guiParameters["displayErrorbar"]
		)
		self.heatmapParameters = nt.HeatmapParameters(
			linked=guiParameters["linkedHeatmap"],
			holder=guiParameters["holderHeatmap"],
			activeChannel=guiParameters["activeChannelHeatmap"]
		)
		self.histogramParameters = nt.HistogramParameters(
			linked=guiParameters["linkedHistogram"],
			holder=guiParameters["holderHistogram"],
			activeChannel=guiParameters["activeChannelHistogram"],
			zoom=guiParameters["zoomHistogram"],
			numberOfBins=guiParameters["numberOfBins"]
		)

	def create_force_volume(self, importedData: Dict) -> None: 
		"""
		Create a force volume from the imported measurement
		data, initialize it's associated plot interface and
		display the force volume in the main window of SOFA.

		Parameters
		----------
		importedData : Dict
			Contains the data of the imported 
			measurement files.
		"""
		forceVolume = ForceVolume(importedData)
		plotInterface = PlotInterface(
			forceVolume.size,
			forceVolume.get_force_distance_curves_data()
		)

		self.importedDataSets[forceVolume.name] = {
			"forceVolume": forceVolume,
			"plotInterface": plotInterface
		}
		self.keyActiveForceVolume.set(forceVolume.name)

		self.plot_active_force_volume()

	def plot_active_force_volume(self) -> None:
		"""
		Plot the processed data of a newly imported force volume
		as a line plot, heatmap and histogram.
		"""
		self._plot_line_plot()
		self.plot_heatmap()
		self.plot_histogram()
	
	@decorator_get_active_data_set
	def _plot_line_plot(
		self, 
		activeForceVolume: ForceVolume,
		activePlotInterface: PlotInterface
	) -> None:
		"""
		Display the force distance curves of
		a force volume in a line plot.

		Parameters
		----------
		activeForceVolume : ForceVolume
			Contains the imported and corrected
			measurement data.
		activePlotInterface: PlotInterface
			Interface between a force volume and 
			the different plots.
		"""
		plt_data.plot_line_plot(
			self.linePlotParameters.holder, 
			activePlotInterface.forceDistanceLines
		)

	@decorator_get_active_heatmap_channel
	@decorator_get_active_data_set
	def plot_heatmap(
		self, 
		activeForceVolume: ForceVolume,
		activePlotInterface: PlotInterface,
		keyActiveHeatmapChannel: str
	) -> None: 
		"""
		Display a channel of a force volume as 
		a heatmap.

		Parameters
		----------
		activeForceVolume : ForceVolume
			Contains the imported and corrected
			measurement data.
		activePlotInterface : PlotInterface
			Interface between a force volume and 
			the different plots.
		keyActiveHeatmapChannel : str
			Name of currently active channel
			displayed in the heatmap.
		"""
		plt_data.plot_heatmap(
			self.heatmapParameters.holder,
			activeForceVolume.get_active_heatmap_data(
				keyActiveHeatmapChannel,
				activePlotInterface.inactiveDataPoints,
				activePlotInterface.orientationMatrix
			),
			activePlotInterface.selectedAreaOutlines
		)

	@decorator_get_active_histogram_channel
	@decorator_get_active_data_set
	def plot_histogram(
		self, 
		activeForceVolume: ForceVolume,
		activePlotInterface: PlotInterface,
		keyActiveHistogramChannel: str
	) -> None:
		"""
		Display a channel of a force volume as 
		a histogram.

		Parameters
		----------
		activeForceVolume : ForceVolume
			Contains the imported and corrected
			measurement data.
		activePlotInterface : PlotInterface
			Interface between a force volume and 
			the different plots.
		keyActiveHeatmapChannel : str
			Name of currently active channel
			displayed in the histogram.
		"""
		activePlotInterface.binValues = plt_data.plot_histogram(
			self.histogramParameters.holder, 
			activeForceVolume.get_histogram_data(keyActiveHistogramChannel),
			activeForceVolume.get_active_histogram_data(
				keyActiveHistogramChannel,
				activePlotInterface.inactiveDataPoints
			),
			self.histogramParameters.numberOfBins.get(),
			self.histogramParameters.zoom.get()
		)

	@decorator_get_active_histogram_channel
	@decorator_get_active_data_set
	def restrict_histogram_min_up(
		self,
		activeForceVolume: ForceVolume,
		activePlotInterface: PlotInterface,
		keyActiveHistogramChannel: str
	) -> None: 
		"""
		Restrict the histogram by increasing the
		border for the minimum value.

		Parameters
		----------
		activeForceVolume : ForceVolume
			Contains the imported and corrected
			measurement data.
		activePlotInterface : PlotInterface
			Interface between a force volume and 
			the different plots.
		keyActiveHistogramChannel : str
			Name of currently active channel
			displayed in the histogram.
		"""
		restrictionParameters = self._get_histogram_restriction_parameters(
			activeForceVolume,
			activePlotInterface,
			keyActiveHistogramChannel
		)
		inactiveDataPoints = mhd.restrict_histogram_min_up(
			restrictionParameters.indexMinBinValue,
			restrictionParameters.indexMaxBinValue,
			restrictionParameters.binValues,
			restrictionParameters.data
		)
		for dataPoint in inactiveDataPoints:
			activePlotInterface.add_inactive_data_point(dataPoint)

	@decorator_get_active_histogram_channel
	@decorator_get_active_data_set
	def restrict_histogram_min_down(
		self,
		activeForceVolume: ForceVolume,
		activePlotInterface: PlotInterface,
		keyActiveHistogramChannel: str
	) -> None: 
		"""
		Restrict the histogram by decreasing the
		border for the minimum value.

		Parameters
		----------
		activeForceVolume : ForceVolume
			Contains the imported and corrected
			measurement data.
		activePlotInterface : PlotInterface
			Interface between a force volume and 
			the different plots.
		keyActiveHistogramChannel : str
			Name of currently active channel
			displayed in the histogram.		"""
		restrictionParameters = self._get_histogram_restriction_parameters(
			activeForceVolume,
			activePlotInterface,
			keyActiveHistogramChannel
		)
		reactivatedDataPoints = mhd.restrict_histogram_min_down(
			restrictionParameters.indexMinBinValue,
			restrictionParameters.indexMaxBinValue,
			restrictionParameters.binValues,
			restrictionParameters.data
		)
		for dataPoint in reactivatedDataPoints:
			activePlotInterface.remove_inactive_data_point(dataPoint)

	@decorator_get_active_histogram_channel
	@decorator_get_active_data_set
	def restrict_histogram_max_up(
		self,
		activeForceVolume: ForceVolume,
		activePlotInterface: PlotInterface,
		keyActiveHistogramChannel: str
	) -> None: 
		"""
		Restrict the histogram by increasing the
		border for the maximum value.

		Parameters
		----------
		activeForceVolume : ForceVolume
			Contains the imported and corrected
			measurement data.
		activePlotInterface : PlotInterface
			Interface between a force volume and 
			the different plots.
		keyActiveHistogramChannel : str
			Name of currently active channel
			displayed in the histogram.
		"""
		restrictionParameters = self._get_histogram_restriction_parameters(
			activeForceVolume,
			activePlotInterface,
			keyActiveHistogramChannel
		)
		reactivatedDataPoints = mhd.restrict_histogram_max_up(
			restrictionParameters.indexMinBinValue,
			restrictionParameters.indexMaxBinValue,
			restrictionParameters.binValues,
			int(self.histogramParameters.numberOfBins.get()),
			restrictionParameters.data
		)
		for dataPoint in reactivatedDataPoints:
			activePlotInterface.remove_inactive_data_point(dataPoint)

	@decorator_get_active_histogram_channel
	@decorator_get_active_data_set
	def restrict_histogram_max_down(
		self,
		activeForceVolume: ForceVolume,
		activePlotInterface: PlotInterface,
		keyActiveHistogramChannel: str
	) -> None: 
		"""
		Restrict the histogram by decreasing the
		border for the maximum value.

		Parameters
		----------
		activeForceVolume : ForceVolume
			Contains the imported and corrected
			measurement data.
		activePlotInterface : PlotInterface
			Interface between a force volume and 
			the different plots.
		keyActiveHistogramChannel : str
			Name of currently active channel
			displayed in the histogram.
		"""
		restrictionParameters = self._get_histogram_restriction_parameters(
			activeForceVolume,
			activePlotInterface,
			keyActiveHistogramChannel
		)
		inactiveDataPoints = mhd.restrict_histogram_max_down(
			restrictionParameters.indexMinBinValue,
			restrictionParameters.indexMaxBinValue,
			restrictionParameters.binValues,
			restrictionParameters.data
		)
		for dataPoint in inactiveDataPoints:
			activePlotInterface.add_inactive_data_point(dataPoint)

	def _get_histogram_restriction_parameters(
		self,
		activeForceVolume: ForceVolume,
		activePlotInterface: PlotInterface,
		keyActiveHistogramChannel: str
	) -> nt.HistogramRestrictionParameters:
		"""
		Get all parameters needed to restrict the
		borders of the histogram.

		Parameters
		----------
		activeForceVolume : ForceVolume
			Contains the imported and corrected
			measurement data.
		activePlotInterface : PlotInterface
			Interface between a force volume and 
			the different plots.
		keyActiveHistogramChannel : str
			Name of currently active channel
			displayed in the histogram.

		Returns
		-------
		restrictionParameters : nt.HistogramRestrictionParameters
			Contains all parameters needed to restrict
			the histogram.
		"""
		data = activeForceVolume.get_histogram_data(
			keyActiveHistogramChannel
		)
		activeData = activeForceVolume.get_active_histogram_data(
			keyActiveHistogramChannel,
			activePlotInterface.inactiveDataPoints
		)
		binValues = activePlotInterface.binValues
		indexMinBinValue = mhd.get_index_of_minimum_bin_value(
			binValues,
			activeData
		)
		indexMaxBinValue = mhd.get_index_of_maximum_bin_value(
			binValues,
			activeData
		)
		return nt.HistogramRestrictionParameters(
			data,
			activeData,
			binValues,
			indexMinBinValue,
			indexMaxBinValue
		)

	def update_active_force_volume_plots(self) -> None: 
		"""
		Update the inactive data points in every plot.
		"""
		self.update_line_plot()
		self.plot_heatmap()
		self.plot_histogram()

	def update_inactive_data_points_line_plot(self) -> None:
		"""
		Check if a change to the inactive data points
		from the line plot, updates only the line plot
		or all plots.
		"""
		if self.linePlotParameters.linked.get():
			self.update_active_force_volume_plots()
		else:
			self.update_line_plot()

	def update_inactive_data_points_heatmap(self) -> None:
		"""
		Check if a change to the inactive data points
		from the heatmap, updates only the heatmap
		or all plots.
		"""
		if self.heatmapParameters.linked.get():
			self.update_active_force_volume_plots()
		else:
			self.plot_heatmap()

	def update_inactive_data_points_histogram(self) -> None:
		"""
		Check if a change to the inactive data points
		from the histogram, updates only the histogram
		or all plots.
		"""
		if self.histogramParameters.linked.get():
			self.update_active_force_volume_plots()
		else:
			self.plot_histogram()

	@decorator_get_active_data_set
	def update_line_plot(
		self,
		activeForceVolume: ForceVolume,
		activePlotInterface: PlotInterface
	) -> None:
		"""
		Update the state of every force distance
		curve displayed in the line plot and if
		selected the average to.

		Parameters
		----------
		activeForceVolume : ForceVolume
			Contains the imported and corrected
			measurement data.
		activePlotInterface : PlotInterface
			Interface between a force volume and 
			the different plots.
		"""
		plt_data.update_line_plot(
			self.linePlotParameters.holder,
			activePlotInterface.forceDistanceLines,
			activePlotInterface.inactiveDataPoints,
			self.linePlotParameters.plotInactive.get()
		)

		if self.linePlotParameters.plotAverage.get():
			self.update_line_plot_average()

	@decorator_get_active_force_volume
	def update_line_plot_average(
		self,
		activeForceVolume: ForceVolume
	) -> None: 
		"""
		"""
		# Remove old average
		# Check if any points are still active
		# Calculate average

		if self.linePlotParameters.plotErrorbar.get():
			plt_data.add_errorbar_to_line_plot(

			)
		else:
			plt_data.add_average_to_line_plot(

			)

	def check_imported_data_set(self) -> bool: 
		"""
		Checks whether measurement data has 
		already been imported.
		"""
		if self.importedDataSets:
			return True
			
		return False

	def get_active_force_volume(self) -> ForceVolume:
		"""
		Get the currently selected force volume.

		Returns
		-------
		activeForceVolume : ForceVolume
			Active force volume.
		"""
		return self.importedDataSets[self.keyActiveForceVolume.get()]["forceVolume"]

	def get_active_plot_interface(self) -> ForceVolume:
		"""
		Get the associated plot interface of the currently
		selected force volume.

		Returns
		-------
		activeForceVolume : ForceVolume
			Plot interface of the active force volume.
		"""
		return self.importedDataSets[self.keyActiveForceVolume.get()]["plotInterface"]

	@staticmethod
	def _text_to_camel_case(inputString: str) -> str:
		"""
		Converts text string to a lower CamelCase format.

		Parameters
		----------
		inputString : str
			Text string.

		Returns
		-------
		outputString : str
			String in lower CamelCase.
		"""
		inputString = inputString.replace(" ", "")
		inputString = inputString[0].lower() + inputString[1:]

		return inputString