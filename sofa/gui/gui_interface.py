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

import data_processing.named_tuples as nt
import data_visualization.plot_data as plt_data
from fdc_data.force_volume import ForceVolume

class GUIInterface():
	"""
	.

	Attributes
	----------
	forceVolumes : Dict[ForceVolume]

	"""
	def __init__(self):
		"""
		"""
		self.forceVolumes: Dict[ForceVolume] = []
		self.activeForceVolume: 
		self.linePlotParameters: nt.LinePlotParameters 
		self.heatmapParameters: nt.HeatmapParameters
		self.histogramParameters: nt.HistogramParameters

	def set_plot_parameters(self, plotParameters: Dict) -> None:
		"""
		"""
		self.activeForceVolume = plotParameters["activeForceVolume"]
		self.linePlotParameters = nt.LinePlotParameters(
			linked=plotParameters["linkedLinePlot"],
			holder=plotParameters["holderLinePlot"],
			showInactive=False,
			plotAverage=False,
			plotErrorbar=False
		)
		self.heatmapParameters = nt.HeatmapParameters(
			linked=plotParameters["linkedHeatmap"],
			holder=plotParameters["holderHeatmap"],
			activeChannel=plotParameters["activeChannelHeatmap"],
			selectedArea=[],
			orientationIndices=[]
		)
		self.histogramParameters = nt.HistogramParameters(
			linked=plotParameters["linkedHistogram"],
			holder=plotParameters["holderHistogram"],
			activeChannel=plotParameters["activeChannelHistogram"],
			zoom=plotParameters["zoomHistogram"],
			numberOfBins=plotParameters["numberOfBins"]
		)

	def import_force_volume(self, importedData) -> None: 
		"""
		"""
		newForceVolume = ForceVolume(importedData)
		newForceVolume.correct_force_distance_curves()
		newForceVolume.calculate_channel_data()

		self.activeForceVolume.set(newForceVolume.name)
		self.activeForceVolume[newForceVolume.name] = newForceVolume

		self._plot_force_volume()

	def _plot_force_volume(self) -> None:
		"""
		"""
		self.plot_line_plot()
		self.plot_heatmap()
		self.plot_histogram()

	def plot_line_plot(self) -> None:
		"""
		"""
		plt_data.plot_line_plot(
			self.linePlotParameters.holder, 
			activeForceVolume.get_force_distance_curves_lines()
		)

	def plot_heatmap(self) -> None: 
		"""
		"""
		activeForceVolume = self._get_active_force_volume()
		activeHeatmapChannel = self.heatmapParameters.activeChannel.get()

		plt_data.plot_heatmap(
			self.heatmapParameters.holder,
			activeForceVolume.get_heatmap_data(activeHeatmapChannel),
			self.linePlotParameters.selectedArea
		)

	def plot_histogram(self) -> None:
		"""
		"""
		activeForceVolume = self._get_active_force_volume()
		activeHistogramChannel = self.histogramParameters.activeChannel.get()

		plt.plt_data.plot_histogram(
			self.histogramParameters.holder, 
			activeForceVolume.get_histogram_data(activeHistogramChannel, active=False),
			activeForceVolume.get_histogram_data(activeHistogramChannel),
			self.histogramParameters.numberOfBins,
			self.histogramParameters.zoom
		)

	def _get_active_force_volume(self) -> ForceVolume:
		"""
		"""
		return self.forceVolumes[self.activeForceVolume.get()]