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
from typing import List, Dict

import numpy as np
import matplotlib

class DataHandler():
	"""."""
	def __init__(self):
		
		self.heatmapParameters = {}
		self.linePlotParameters = {}
		self.histogramParameters = {}

		self.generalData = {}
		self.curveData = {}
		self.averageData = {}
		self.channelData = {}
		self.histogramData = {}

		self.inactiveDataPoints = []

	def set_imported_data(
		self,
		combinedData: Dict
	) -> None:
		""".

		"""
		self.generalData = combinedData["generalData"]
		self.curveData = combinedData["curveData"]
		self.channelData = combinedData["channelData"]

		self.averageData["leftCurve"] = None
		self.averageData["rightCurve"] = None

	def set_plot_parameters(
		self,
		guiComponents: Dict
	):
		"""
		
		"""
		self.linePlotParameters["interactive"] = guiComponents["interactiveLinePlot"]
		self.linePlotParameters["holder"] = guiComponents["holderLinePlot"]
		self.linePlotParameters["showInactive"] = False
		self.linePlotParameters["displayAverage"] = False
		self.linePlotParameters["displayErrorbar"] = False

		self.heatmapParameters["interactive"] = guiComponents["interactiveHeatmap"]
		self.heatmapParameters["holder"] = guiComponents["holderHeatmap"]
		self.heatmapParameters["currentChannel"] = guiComponents["currentChannelHeatmap"]
		self.heatmapParameters["selectedArea"] = []
		self.heatmapParameters["mappedIndices"] = []

		self.histogramParameters["interactive"] = guiComponents["interactiveHistogram"]
		self.histogramParameters["holder"] = guiComponents["holderHistogram"]
		self.histogramParameters["currentChannel"] = guiComponents["currentChannelHistogram"]
		self.histogramParameters["zoom"] = guiComponents["zoomHistogram"]
		self.histogramParameters["numberOfBins"] = guiComponents["numberOfBins"]

	def init_mapped_indices(self) -> None:
		"""Create a two dimensional array of indices 
		   to map the datapoints to their original orientation."""	
		m = int(self.generalData["m"])
		n = int(self.generalData["n"])

		self.heatmapParameters["mappedIndices"] = np.arange(
			m * n
		).reshape((m, n))

	def reset_channel_data(self):
		"""Reset the data of every channel."""
		for channel in self.channelData.values():
			channel["data"] = channel["sourceData"].copy()

	def display_imported_data(self):
		"""Display the data as line plot heatmap and histogram."""
		self.plot_lines()
		self.plot_heatmap()
		self.plot_histogram()

	def plot_heatmap(self) -> None:
		"""Plot two dimensional data as a heatmap."""
		data = self._get_current_heatmap_data()
		m, n = np.shape(data)

		# Make data displayable, if there are no valid values
		if np.isnan(data).all():
			data = np.zeros((m, n))

		ax = self.get_axes(self.heatmapParameters["holder"])
		ax.cla()
		#ax.set_title(self.filename)
		ax.imshow(data, cmap="gray", extent=[0, n, m, 0])
		# Simplify mouse hover by removing currenet x and y coordinates.
		ax.format_coord = lambda x, y: ""

		# Plot potentional marking lines.
		for line in self.heatmapParameters["selectedArea"]:
			ax.add_line(line)

		self.heatmapParameters["holder"].draw()

	def plot_lines(self) -> None:
		"""Plot a set of curves as line plot."""
		ax = self.get_axes(self.linePlotParameters["holder"])
		ax.cla()
		#ax.set_title("Curves of " + self.filename)
		ax.ticklabel_format(axis="both", style="sci", scilimits=(0,0))
		# Simplify mouse hover by removing currenet x and y coordinates.
		ax.format_coord = lambda x, y: ""

		# Add lines to axis.
		for line in self.curveData["displayedLines"]:
			ax.add_line(line)

		# Set view limits.
		ax.autoscale_view()

		self.linePlotParameters["holder"].draw()

	@staticmethod
	def get_axes(holder):
		"""Create or get axis of the given holder.

		Parameters:
			holder(canvasTkAgg): Given holder that requires an axes.

		Returns:
			axes(axes): New or existing axes of the given holder.
		"""
		try:
			return holder.figure.get_axes()[0]
		except IndexError:
			return holder.figure.add_subplot(111)

	def update_lines(self) -> None:
		"""Update the state of all lines. """
		for index, line in enumerate(self.curveData["displayedLines"]):
			if index in self.inactiveDataPoints and self.linePlotParameters["showInactive"]:
				self.update_state_of_line(line, "gray", -1)
			elif index in self.inactiveDataPoints and not self.linePlotParameters["showInactive"]:
				self.update_state_of_line(line, "white", -1)
			else:
				self.update_state_of_line(line, "red", 1)

		self.linePlotParameters["holder"].draw()

	@staticmethod
	def update_state_of_line(line, color, zorder):
		"""Update the state of a line.
		
		Parameters:
			line(line2d): 2D Line from matplotlib.
			color(str): New color of the line.
			zorder(int): New z order of the line.
		"""
		line.set_color(color)
		line.zorder = zorder

	def _calculate_average(self):
		"""Calculate the average of the active data points."""
		# Return if all datapoints are inactive.
		if len(self.inactiveDataPoints) == int(self.generalData["m"]) * int(self.generalData["n"]):
			return

		activeCurves, xMin, yMax = self._get_active_curve_data()
		
		NormedCurves = self._interpolate_normed_curves(activeCurves, xMin, yMax)

		# Average the points along the x/y axis.
		averagedYValuesLeft = [
			np.nanmean(nthValues) for nthValues in zip(*NormedCurves.yValuesLeft)
		]
		averagedYValuesRight = [
			np.nanmean(nthValues) for nthValues in zip(*NormedCurves.yValuesRight)
		]

		# Calculate the standard deviation for the left/right side.
		standardDeviationLeft = [
			np.nanstd(nthValues) for nthValues in zip(*NormedCurves.yValuesLeft)
		]
		standardDeviationRight = [
			np.nanstd(nthValues) for nthValues in zip(*NormedCurves.yValuesRight)
		]

		self.averageData["leftXValues"] = np.asarray(NormedCurves.xValuesLeft)
		self.averageData["leftYValues"] = np.asarray(averagedYValuesLeft)
		self.averageData["rightXValues"] = np.asarray(NormedCurves.xValuesRight)
		self.averageData["rightYValues"] = np.asarray(averagedYValuesRight)
		self.averageData["standardDeviationLeft"] = np.asarray(standardDeviationLeft)
		self.averageData["standardDeviationRight"] = np.asarray(standardDeviationRight)

	def _get_active_curve_data(self):
		""""""
		activeCurves = []
		xMinValues = []
		yMaxValues = []

		for index, curve in enumerate(self.curveData["correctedCurves"]):
			if index not in self.inactiveDataPoints:
				activeCurves.append(curve)
				xMinValues.append(min(curve[0]))
				yMaxValues.append(max(curve[1]))

		return activeCurves, min(xMinValues), max(yMaxValues)
	
	@staticmethod
	def _interpolate_normed_curves(activeCurves, xMin, yMax):
		"""Normalize lines in preparation of averraging them.

		Parameter:
			activeXValues(np.ndarray): 2 dim array containing the x values of the curves.
			activeYValues(np.ndarray): 2 dim array containing the y values of the curves.

		Returns: 
			NormedCurves(namedtuple): Tuple with a normed line for the left and right part.
		"""
		numberOfDataPoints = 2000

		normedXValuesLeft = np.linspace(xMin, 0, numberOfDataPoints)
		normedYValuesLeft = []
		normedXValuesRight = np.linspace(0, yMax, numberOfDataPoints)
		normedYValuesRight = []
		
		# Interpolate y values for the left and right part.
		for curve in activeCurves:
			# Split left and right part by the last zero crossing/point of contact.
			lastZeroCrossing = np.where(curve[0] < 0)[0][-1]

			normedYValuesLeft.append(
				np.interp(
					normedXValuesLeft, 
					curve[0][:lastZeroCrossing], 
					curve[1][:lastZeroCrossing]
				)
			)
			normedYValuesRight.append(
				np.interp(
					normedXValuesRight, 
					curve[1][lastZeroCrossing:], 
					curve[0][lastZeroCrossing:]
				)
			)

		NormedCurves = namedtuple(
			"NormedCurves", 
			[
				"xValuesLeft",
				"yValuesLeft",
				"xValuesRight",
				"yValuesRight"
			]
		)
		return NormedCurves(
			normedXValuesLeft, 
			normedYValuesLeft, 
			normedXValuesRight, 
			normedYValuesRight
		)

	def plot_average_curve(self):
		""" Plot the average as normal curve or as an errorbar with the standard deviation."""
		self._calculate_average()

		if self.averageData["leftCurve"] and self.averageData["rightCurve"]:
			self.remove_average_curve()

		# Plot the average as errorbar with with the standard deviation.
		if self.linePlotParameters["displayErrorbar"]:
			self.averageData["leftCurve"] = self.linePlotParameters["holder"].figure.get_axes()[0].errorbar(
				self.averageData["leftXValues"], 
				self.averageData["leftYValues"], 
				yerr=self.averageData["standardDeviationLeft"], 
				color="black", ecolor="black", zorder=6
			)
			self.averageData["rightCurve"] = self.linePlotParameters["holder"].figure.get_axes()[0].errorbar(
				self.averageData["rightYValues"], 
				self.averageData["rightXValues"], 
				xerr=self.averageData["standardDeviationRight"], 
				color="black", ecolor="black", zorder=6
			)
		# Plot the average as normal curve.
		else:
			self.averageData["leftCurve"] = self.linePlotParameters["holder"].figure.get_axes()[0].plot(
				self.averageData["leftXValues"], 
				self.averageData["leftYValues"], 
				color="black", zorder=6
			)[0]
			self.averageData["rightCurve"] = self.linePlotParameters["holder"].figure.get_axes()[0].plot(
				self.averageData["rightYValues"], 
				self.averageData["rightXValues"],
				color="black", zorder=6
			)[0]

		self.linePlotParameters["holder"].draw()

	def remove_average_curve(self):
		"""Remove the average curve."""
		self.averageData["leftCurve"].remove()
		self.averageData["leftCurve"] = None

		self.averageData["rightCurve"].remove()
		self.averageData["rightCurve"] = None

	def plot_histogram(self):
		"""Display the data and active data as a histogram."""
		data = self._get_current_histogram_data()
		activeData = self._get_active_histogram_data(data)

		ax = self.get_axes(self.histogramParameters["holder"])

		# Clear the axes 
		ax.cla()
		ax.ticklabel_format(axis="y", style="sci", scilimits=(0,0))

		# Plot the entire data.
		nValues, binValues, patchValues = ax.hist(
			data, 
			bins=int(self.histogramParameters["numberOfBins"].get()), 
			range=(np.min(data), np.max(data)),
			alpha=1, orientation="horizontal", color='b'
		)
		
		# Plot active part of the data.
		ax.hist(
			activeData,  
			bins=int(self.histogramParameters["numberOfBins"].get()), 
			range=(np.min(data), np.max(data)),
			alpha=1, orientation="horizontal", color='r'
		)
		
		self.histogramData["binValues"] = binValues
		# Find the current lower and upper bounds of the bin values.
		self.histogramData["indexOfMinValue"] = np.where(binValues <= np.min(activeData))[0][-1]
		self.histogramData["indexOfMaxValue"] = np.where(binValues >= np.max(activeData))[0][0]

		if self.histogramParameters["zoom"].get():
			ax.set_ylim(
				binValues[self.histogramData["indexOfMinValue"]],
				binValues[self.histogramData["indexOfMaxValue"]]
			)
			ax.set_xlim(auto=True)
		
		self.histogramParameters["holder"].draw()

	def restrict_histogram(self, direction):
		"""Restrict the histogram data by setting new borders for the min and max of the data.

		Parameters:
			direction(str): 
		"""
		minIndex = self.histogramData["indexOfMinValue"]
		maxIndex = self.histogramData["indexOfMaxValue"]
		data = self.histogramData["data"].flatten()
		sourceData = self.histogramData["sourceData"].flatten()
		binsAll = self.histogramData["binValues"]

		# Increase the min border if it is still smaller then the current max border.
		if direction == "minUp" and minIndex < maxIndex - 1:
			minIndex += 1
			newMin = binsAll[minIndex]
			self.inactiveDataPoints.extend(np.where(data < newMin)[0])

		# Decrease the min border if it is still bigger then the lowest border.
		elif direction == "minDown" and minIndex > 0:
			# Continue to decrease the min border until there are datapoints within the new border.
			while (True):
				minIndex -= 1
				newMin = binsAll[minIndex]
				activeIndex = np.where(
					np.logical_and(sourceData >= newMin, sourceData < binsAll[minIndex + 1])
				)[0]
				if len(activeIndex) > 0:
					break

			for point in activeIndex:
				 self.inactiveDataPoints.remove(point)

		# Increase the max border if it is still smaller then the highest border.
		elif direction == "maxUp" and maxIndex < int(self.histogramData["numberOfBins"].get()):
			# Continue to increase the max border until there are datapoints within the new border.
			while (True):
				maxIndex += 1
				newMax = binsAll[maxIndex]
				activeIndex = np.where(
					np.logical_and(sourceData <= newMax, sourceData > binsAll[maxIndex - 1])
				)[0]
				if len(activeIndex) > 0:
					break

			for point in activeIndex:
				 self.inactiveDataPoints.remove(point)

		# Decrease the max border if it is still bigger then the current min border.
		elif direction == "maxDown" and maxIndex > minIndex + 1:
			maxIndex -= 1
			newMax = binsAll[maxIndex]
			self.inactiveDataPoints.extend(np.where(data > newMax)[0])

		# Remove duplicates.
		self.inactiveDataPoints = list(set(self.inactiveDataPoints))

	def _get_current_heatmap_data(self) -> np.ndarray:
		""""""
		channelKey = self._text_to_camel_case(
			self.heatmapParameters["currentChannel"].get()
		)
		heatmapData = self.channelData[channelKey]["data"]

		activeHeatmapData =  self._get_active_heatmap_data(heatmapData)

		return activeHeatmapData

	def _get_current_histogram_data(self) -> np.ndarray:
		""""""
		channelName = self._text_to_camel_case(
			self.histogramParameters["currentChannel"].get()
		)
		histogramData = self.channelData[channelName]["data"]

		return histogramData[np.isfinite(histogramData)].flatten()

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

	def _get_active_heatmap_data(self, data):
		"""Remove inactive data points from the given data in the dependence of its current alignment.
		
		Parameters:
			data(np.ndarray): 2 dim data array.

		Returns:
			mappedActiveData(np.ndarray): 2 dim data array with nan values at inactive data points.
		"""
		m, n = np.shape(data)

		data = data.flatten()
		mappedIndices = self.heatmapParameters["mappedIndices"].flatten()

		# Map inactive data points to the current alignment.
		mappedInactiveDataPoints = [
			np.where(point == mappedIndices)[0][0] for point in self.inactiveDataPoints
		]

		np.put(data, mappedInactiveDataPoints, np.nan)

		return np.reshape(data, (m, n))

	def _get_active_histogram_data(self, data):
		"""Set inactive data points to nan.
		
		Parameters:
			data(np.ndarray): 1 dim data array.

		Returns:
			activeData(np.ndarray): 2 dim data array with nan values at inactive data points.
		"""
		activeData = data.copy()
		np.put(activeData, self.inactiveDataPoints, np.nan)

		return activeData[np.isfinite(activeData)]

	def add_inactive_data_points(self, newPoints):
		"""Add data points to the inactive data points in 
		   dependence of the current alignment of the data.
		
		Parameters:
			newPoints(np.ndarray): Array with the new inactive data points.
		"""
		flattenMappedIndicies = self.heatmapParameters["mappedIndices"].flatten()

		# Map new data points to the current alignment.
		for point in newPoints:
			self.inactiveDataPoints.append(self.heatmapParameters["mappedIndices"].flatten()[point])
		
		# Remove duplicates.
		self.inactiveDataPoints = list(set(self.inactiveDataPoints))
	
	def remove_inactive_data_points(self, newPoints):
		"""Remove data points from the inactive data 
		   points in dependence of the current alignment of the data.
		
		Parameters:
			newPoints(np.ndarray): Array with the new active data ponits.
		"""
		flattenMappedIndicies = self.heatmapParameters["mappedIndices"].flatten()

		for point in newPoints:
			self.inactiveDataPoints.remove(self.heatmapParameters["mappedIndices"].flatten()[point])

	def update_plots(self):
		"""Update every plot."""
		self.update_line_plot()
		self.update_histogram()
		self.update_heatmap()

	def update_line_plot(self):
		"""Update the line plot."""
		self.update_lines()

		if self.linePlotParameters["displayAverage"]:
			self.plot_average_curve()

	def update_heatmap(self):
		"""Update every active channel."""
		self.plot_heatmap()

	def update_histogram(self):
		"""Update the histogram."""
		self.plot_histogram()