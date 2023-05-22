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
from typing import Dict, List
import functools

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
		activeForceVolume = self._get_active_force_volume()
		activePlotInterface = self._get_active_plot_interface()
		function(self, activeForceVolume, activePlotInterface, *args, **kwargs)

	return wrapper_get_active_data_set

def decorator_get_active_force_volume(function):
	"""
	Get current selected force volume.
	"""
	@functools.wraps(function)
	def wrapper_get_active_force_volume(self, *args, **kwargs):
		activeForceVolume = self._get_active_force_volume()
		function(self, activeForceVolume, *args, **kwargs)

	return wrapper_get_active_force_volume

def decorator_get_active_plot_interface(function):
	"""
	Get current selected force volume.
	"""
	@functools.wraps(function)
	def wrapper_get_active_plot_interface(self, *args, **kwargs):
		activePlotInterface = self._get_active_plot_interface()
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
	forceVolumes : Dict[ForceVolume]
		Set of every imported force volume.
	keyActiveForceVolume : ttk.StringVar
		Variable that stores the name of active force volume.
	linePlotParameters : nt.LinePlotParameters
		
	heatmapParameters : nt.HeatmapParameters

	histogramParameters : nt.HistogramParameters

	"""
	def __init__(self) -> None:
		"""
		Initialize a blank interface. The attributes can only be 
		set after 
		"""
		self.importedDataSets: Dict = {}
		self.keyActiveForceVolume: ttk.StringVar
		self.linePlotParameters: nt.LinePlotParameters 
		self.heatmapParameters: nt.HeatmapParameters
		self.histogramParameters: nt.HistogramParameters

	def set_gui_parameters(self, guiParameters: Dict) -> None:
		"""

		
		Parameters
		----------
		guiParameters : dict

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


		Parameters
		----------
		importedData : Dict
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
		
		"""
		plt_data.plot_line_plot(
			self.linePlotParameters.holder, 
			activePlotInterface.linePlotForceDistanceLines
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
		"""
		plt_data.plot_heatmap(
			self.heatmapParameters.holder,
			activeForceVolume.get_active_heatmap_data(
				keyActiveHeatmapChannel,
				activePlotInterface.inactiveDataPoints,
				activePlotInterface.heatmapOrientationMatrix
			),
			activePlotInterface.heatmapSelectedAreaBorders
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
		"""
		plt_data.plot_histogram(
			self.histogramParameters.holder, 
			activeForceVolume.get_histogram_data(keyActiveHistogramChannel),
			activeForceVolume.get_active_histogram_data(
				keyActiveHistogramChannel,
				activePlotInterface.inactiveDataPoints
			),
			self.histogramParameters.numberOfBins.get(),
			self.histogramParameters.zoom.get()
		)

	def update_active_force_volume_plots(self) -> None: 
		"""
		"""
		self.update_line_plot()
		self.plot_heatmap()
		self.plot_histogram()

	def update_inactive_data_points_line_plot(self) -> None:
		"""
		"""
		if self.linePlotParameters.linked.get():
			self.update_active_force_volume_plots()
		else:
			self.update_line_plot()

	def update_inactive_data_points_heatmap(self) -> None:
		"""
		"""
		if self.heatmapParameters.linked.get():
			self.update_active_force_volume_plots()
		else:
			self.plot_heatmap()

	def update_inactive_data_points_histogram(self) -> None:
		"""
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
		"""
		plt_data.update_line_plot(
			self.linePlotParameters.holder,
			activePlotInterface.linePlotForceDistanceLines,
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

	def _get_active_force_volume(self) -> ForceVolume:
		"""


		Returns
		-------
		activeForceVolume : ForceVolume

		"""
		return self.importedDataSets[self.keyActiveForceVolume.get()]["forceVolume"]

	def _get_active_plot_interface(self) -> ForceVolume:
		"""


		Returns
		-------
		activeForceVolume : ForceVolume

		"""
		return self.importedDataSets[self.keyActiveForceVolume.get()]["plotInterface"]

	@staticmethod
	def _text_to_camel_case(inputString: str) -> str:
		"""Converts text string to a lower CamelCase format.

		Parameters:
			inputString(str): Text string.

		Returns:
			outputString(str): String in lower CamelCase.
		"""
		inputString = inputString.replace(" ", "")
		inputString = inputString[0].lower() + inputString[1:]

		return inputString

	def check_imported_data_set(self) -> bool: 
		"""
		"""
		if self.importedDataSets:
			return True
			
		return False

	@decorator_get_active_plot_interface
	def reset_inactive_data_points(
		self,
		activePlotInterface: PlotInterface
	) -> None:
		"""
		"""
		activePlotInterface.reset_inactive_data_points()

	@decorator_get_active_plot_interface
	def reset_heatmap_orientation_matrix(
		self,
		activePlotInterface: PlotInterface
	) -> None:
		"""
		"""
		activePlotInterface._create_heatmap_orientation_matrix()

	@decorator_get_active_plot_interface
	def add_inactive_data_point(
		self,
		activePlotInterface: PlotInterface,
		inactiveDataPoint: int
	) -> None:
		"""
		"""
		activePlotInterface.add_inactive_data_point(inactiveDataPoint)

	@decorator_get_active_plot_interface
	def remove_inactive_data_point(
		self,
		activePlotInterface: PlotInterface,
		inactiveDataPoint: int
	) -> None:
		"""
		"""
		activePlotInterface.remove_inactive_data_point(inactiveDataPoint)

	@decorator_get_active_plot_interface
	def add_inactive_data_points(
		self,
		activePlotInterface: PlotInterface,
		inactiveDataPoints: List[int]
	) -> None:
		"""
		"""
		activePlotInterface.add_inactive_data_points(inactiveDataPoints)

	@decorator_get_active_plot_interface
	def flip_heatmap_orientation_matrix_horizontal(
		self,
		activePlotInterface: PlotInterface,
	) -> None:
		"""
		"""
		activePlotInterface.flip_heatmap_orientation_matrix_horizontal()

	@decorator_get_active_plot_interface
	def flip_heatmap_orientation_matrix_vertical(
		self,
		activePlotInterface: PlotInterface,
	) -> None:
		"""
		"""
		activePlotInterface.flip_heatmap_orientation_matrix_vertical()

	@decorator_get_active_plot_interface
	def rotate_heatmap_orientation_matrix(
		self,
		activePlotInterface: PlotInterface,
	) -> None:
		"""
		"""
		activePlotInterface.rotate_heatmap_orientation_matrix()

	@decorator_get_active_force_volume
	def flip_channel_horizontal(
		self,
		activeForceVolume: ForceVolume
	) -> None:
		"""
		"""
		activeForceVolume.flip_channel_horizontal()

	@decorator_get_active_force_volume
	def flip_channel_vertical(
		self,
		activeForceVolume: ForceVolume
	) -> None:
		"""
		"""
		activeForceVolume.flip_channel_vertical()

	@decorator_get_active_force_volume
	def rotate_channel(
		self,
		activeForceVolume: ForceVolume
	) -> None:
		"""
		"""
		activeForceVolume.rotate_channel()