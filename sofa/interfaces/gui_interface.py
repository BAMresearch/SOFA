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
from typing import Dict
import functools

import data_processing.named_tuples as nt
import data_visualization.plot_data as plt_data
from fdc_data.force_volume import ForceVolume

def decorator_get_active_force_volume(function):
	"""Get current selected force volume."""
	@functools.wraps(function)
	def wrapper_get_active_force_volume(self, *args, **kwargs):
		activeForceVolume = self._get_active_force_volume()
		function(activeForceVolume, *args, **kwargs)

	return wrapper_get_active_force_volume

def decorator_get_active_heatmap_channel(function):
	"""Get name of current selected channel of heatmap."""
	@functools.wraps(function)
	def wrapper_get_active_force_volume(self, *args, **kwargs):
		keyActiveHeatmapChannel = self.heatmapParameters.activeChannel.get()
		function(keyActiveHeatmapChannel, *args, **kwargs)

	return wrapper_get_active_force_volume

def decorator_get_active_histogram_channel(function):
	"""Get name of current selected channel of histogram."""
	@functools.wraps(function)
	def wrapper_get_active_force_volume(self, *args, **kwargs):
		keyActiveHistogramChannel = self.histogramParameters.activeChannel.get()
		function(keyActiveHistogramChannel, *args, **kwargs)

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
		Name of active force volume.
	linePlotParameters : nt.LinePlotParameters
		
	heatmapParameters : nt.HeatmapParameters

	histogramParameters : nt.HistogramParameters

	"""
	def __init__(self) -> None:
		"""
		Initialize a blank interface. The attributes can only be 
		set after 
		"""
		self.forceVolumes: Dict[ForceVolume] = {}
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
			showInactive=False,
			plotAverage=False,
			plotErrorbar=False
		)
		self.heatmapParameters = nt.HeatmapParameters(
			linked=guiParameters["linkedHeatmap"],
			holder=guiParameters["holderHeatmap"],
			activeChannel=guiParameters["activeChannelHeatmap"],
			selectedArea=[],
			orientationIndices=[]
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

		self.keyActiveForceVolume.set(forceVolume.name)
		self.forceVolumes[forceVolume.name] = forceVolume

		self.plot_active_force_volume()

	def plot_active_force_volume(self) -> None:
		"""
		Plot the processed data of a newly imported force volume
		as a line plot, heatmap and histogram.
		"""
		self._plot_line_plot()
		self.plot_heatmap()
		self.plot_histogram()

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
		
	@decorator_get_active_force_volume
	def _plot_line_plot(
		self, 
		activeForceVolume: ForceVolume
	) -> None:
		"""
		
		"""
		plt_data.plot_line_plot(
			self.linePlotParameters.holder, 
			activeForceVolume.get_force_distance_curves_lines()
		)

	@decorator_get_active_force_volume
	@decorator_get_active_heatmap_channel
	def plot_heatmap(
		self, 
		activeForceVolume: ForceVolume,
		keyActiveHeatmapChannel: str
	) -> None: 
		"""
		"""
		plt_data.plot_heatmap(
			self.heatmapParameters.holder,
			activeForceVolume.get_heatmap_data(
				keyActiveHeatmapChannel
			),
			self.heatmapParameters.selectedArea
		)

	@decorator_get_active_force_volume
	@decorator_get_active_histogram_channel
	def plot_histogram(
		self, 
		activeForceVolume: ForceVolume,
		keyActiveHistogramChannel: str
	) -> None:
		"""
		"""
		plt_data.plot_histogram(
			self.histogramParameters.holder, 
			activeForceVolume.get_histogram_data(keyActiveHistogramChannel, active=False),
			activeForceVolume.get_histogram_data(keyActiveHistogramChannel),
			self.histogramParameters.numberOfBins,
			self.histogramParameters.zoom
		)

	@decorator_get_active_force_volume
	def update_line_plot(
		self,
		activeForceVolume: ForceVolume
	) -> None:
		"""
		"""
		plt.update_line_plot(
			self.linePlotParameters.holder,
			activeForceVolume.get_force_distance_curves_lines(),
			activeForceVolume.inactiveDataPoints,
			self.linePlotParameters.showInactive
		)

		if self.linePlotParameters.plotAverage:
			self.update_line_plot_average(
				activeForceVolume
			)

	def update_line_plot_average(
		self,
		activeForceVolume: ForceVolume
	) -> None: 
		"""
		"""
		# Remove old average
		# Check if any points are still active
		# Calculate average

		if self.linePlotParameters.plotErrorbar:
			plt.add_errorbar_to_line_plot(

			)
		else:
			plt.add_average_to_line_plot(

			)

	def _get_active_force_volume(self) -> ForceVolume:
		"""


		Returns
		-------
		activeForceVolume : ForceVolume

		"""
		return self.forceVolumes[self.keyActiveForceVolume.get()]