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
from typing import List, Tuple, Optional

import numpy as np 

from toolbars.sofa_toolbar import SofaToolbar

class HeatmapToolbar(SofaToolbar):
	"""
	A custom toolbar to process data, displayed as a heatmap.
	
	Attributes
	----------
	guiInterface : GUIInterface

	holder : 

	mode : 

	eventConnections : list[]

	"""
	def __init__(self, canvas_, parent_, guiInterface):
		# Set path for toolbar icons.
		iconPath = os.path.join(
			os.path.abspath(os.path.dirname(__file__)), 
			"icons", 
			"heatmap_toolbar"
		)
		toolItems = (
			("reset", "", os.path.join(iconPath, "reset.gif"), "_reset_heatmap"),
			("select_area", "", os.path.join(iconPath, "select_area.gif"), "_toggle_select_area"),
			("select_rectangle", "", os.path.join(iconPath, "select_rectangle.gif"), "_toggle_select_rect"),
			("include_area", "", os.path.join(iconPath, "include.gif"), "_include_area"),
			("exclude_area", "", os.path.join(iconPath, "exclude.gif"), "_exclude_area"),
			("flip_h", "", os.path.join(iconPath, "flip_h.gif"), "_flip_heatmap_h"),
			("flip_v", "", os.path.join(iconPath, "flip_v.gif"), "_flip_heatmap_v"),
			("rotate", "", os.path.join(iconPath, "rotate.gif"), "_rotate_heatmap")
		)	
		self.guiInterface = guiInterface
		self.selectedArea = []

		super().__init__(canvas_, parent_, toolItems)

	def _reset_heatmap(self) -> None:
		"""Reset the selected area, the orientation 
		   and the inactive data points."""
		self.selectedArea = []
		self._delete_selected_area_lines()

		self.dataHandler.init_mapped_indices()
		self.dataHandler.reset_channel_data()

		self.dataHandler.inactiveDataPoints = []

		self._check_interactive_plot()
		
	def _toggle_select_area(self) -> None:
		"""Toggle the selector to select an area."""
		self._update_toolbar_mode("select area")
		self._update_event_connections()
		self._update_toolbar_buttons()

	def _select_area_on_click(self, event) -> None:
		"""Prepare to capture the mouse motion."""
		self.selectedArea = []
	   
		self.eventConnections.append(
			self.holder.figure.canvas.mpl_connect(
				"motion_notify_event", 
				self._select_area_motion
			)
		)

	def _select_area_motion(self, event) -> None:
		"""Capture and store the data of the mouse, 
		   while moving over the heatmap."""
		if event.xdata and event.ydata:
			self.selectedArea.append(
				(
					int(np.trunc(event.xdata)), 
					int(np.trunc(event.ydata))
				)
			)

	def _select_area_on_release(self, event) -> None:
		"""Mark the selected area in the heatmap."""
		# Stop capaturing mouse movement.
		self.holder.figure.canvas.mpl_disconnect(
			self.eventConnections[-1]
		)
		del self.eventConnections[-1]
		
		self._delete_selected_area_lines()
		
		# Delete recurring values in the marked area.
		self.selectedArea = [
			list(entry) 
			for entry 
			in set(self.selectedArea)
		]
		
		# Mark selected Area.
		for i, section in enumerate(self.selectedArea):
			self._orbit_area(section, i)
		
		self._delete_equal_lines(
			self.dataHandler.heatmapParameters["selectedArea"]
		)
	
		self.holder.draw()

	def _delete_equal_lines(self, selectedAreaLines: List) -> None:
		"""Find all lines that exist more than once and delete them."""
		lineData = [line.get_xydata() for line in selectedAreaLines]
		
		uniqueValues, count = np.unique(
			lineData, axis=0, return_counts=True
		)
		doubledValues = uniqueValues[np.where(count > 1)]
		doubledIndices = []

		for i, line in enumerate(selectedAreaLines):
			for value in doubledValues:
				if np.array_equal(line.get_xydata(), value):
					line.remove()
					doubledIndices.append(i)

		self.dataHandler.heatmapParameters["selectedArea"] = [
			line
			for index, line in enumerate(selectedAreaLines) 
			if index not in doubledIndices
		]

	def _toggle_select_rect(self) -> None:
		"""Toggle the selector to select a rectangle."""
		self._update_toolbar_mode("select rect")
		self._update_event_connections()
		self._update_toolbar_buttons()

	def _select_rect_on_click(self, event) -> None:
		"""Store startingpoint of the rectangle, if existing."""
		self.selectedArea = []
		self.xStart = self.yStart = np.nan
	   
		if event.xdata:
			self.xStart = event.xdata
			self.yStart = event.ydata

	def _select_rect_on_release(self, event) -> None:
		"""Mark the selected rectangle in the heatmap."""
		if np.isfinite(self.xStart) and event.xdata:
			self._delete_selected_area_lines()
			
			# Standardize data.
			if self.xStart > event.xdata:
				self.xStart, event.xdata = event.xdata, self.xStart
			if self.yStart > event.ydata:
				self.yStart, event.ydata = event.ydata, self.yStart
			
			xStart = int(np.trunc(self.xStart))
			xEnd = int(np.ceil(event.xdata))
			yStart = int(np.trunc(self.yStart))
			yEnd = int(np.ceil(event.ydata))

			self.selectedArea = self._create_selected_area(
				xStart, xEnd, yStart, yEnd
			)
			
			self._plot_marking_line((xStart, xStart), (yStart, yEnd))
			self._plot_marking_line((xStart, xEnd), (yStart, yStart))
			self._plot_marking_line((xEnd, xEnd), (yStart, yEnd))
			self._plot_marking_line((xEnd, xStart), (yEnd, yEnd))

			self.holder.draw()

	@staticmethod
	def _create_selected_area(
		xStart: int, 
		xEnd: int, 
		yStart: int, 
		yEnd: int
	) -> List[List[int]]:
		"""Spans a rectangle between a start and end point. 

		Parameters:
			xStart(int): X value of the start point.
			xEnd(int): X value of the end point.
			yStart(int): Y value of the start point.
			yEnd(int): Y value of the end point.

		Returns: 
			selectedArea(list): A list of all points within the rectangle.
		"""
		return [
			[i, j] 
			for i in range(xStart, xEnd) 
			for j in range(yStart, yEnd)
		]

	def _include_area(self) -> None:
		"""Add everything except the selected area to the inactive data points."""
		if len(self.selectedArea) == 0:
			return

		m, n = np.shape(self.dataHandler._get_heatmap_data())
		# Map new inactive points in a two dimensional array to their corresponding points in a one dimensional array.
		newInactiveDataPoints = [
			i 
			for i in range(m * n) 
			if i not in [dataPoint[1] * n + dataPoint[0] 
			for dataPoint in self.selectedArea]
		]

		self.selectedArea = []
		self._delete_selected_area_lines()	
		
		self.dataHandler.add_inactive_data_points(newInactiveDataPoints)

		self._check_interactive_plot()

	def _exclude_area(self) -> None:
		"""Add the selected area to the inactive data points."""
		if len(self.selectedArea) == 0:
			return

		m, n = np.shape(self.dataHandler._get_heatmap_data()) 
		# Map new inactive points in a two dimensional array to their corresponding points in a one dimensional array.
		newInactiveDataPoints = [dataPoint[1] * n + dataPoint[0] for dataPoint in self.selectedArea]
	
		self.selectedArea = []
		self._delete_selected_area_lines()	
		
		self.dataHandler.add_inactive_data_points(newInactiveDataPoints)

		self._check_interactive_plot()

	def _flip_heatmap_h(self) -> None:
		"""Flip every heatmap horizontal."""
		for line in self.dataHandler.heatmapParameters["selectedArea"]:
			self._flip_line_h(line)

		self._flip_area_h()
		self.dataHandler.heatmapParameters["mappedIndices"] = np.flip(self.dataHandler.heatmapParameters["mappedIndices"], 0)
		
		for channel in self.dataHandler.channelData.values():
			channel["data"] = np.flip(
				channel["data"], 0
			)
		self.dataHandler.plot_heatmap()

	def _flip_heatmap_v(self) -> None: 
		"""Flip every heatmap vertical."""
		for line in self.dataHandler.heatmapParameters["selectedArea"]:
			self._flip_line_v(line)

		self._flip_area_v()
		self.dataHandler.heatmapParameters["mappedIndices"] = np.flip(self.dataHandler.heatmapParameters["mappedIndices"], 1)

		for channel in self.dataHandler.channelData.values():
			channel["data"] = np.flip(
				channel["data"], 1
			)
		self.dataHandler.plot_heatmap()
	
	def _rotate_heatmap(self) -> None:
		"""Rotate every heatmap by 90 degrees to the left."""	
		for line in self.dataHandler.heatmapParameters["selectedArea"]:
			self._rotate_line(line)

		self._rotate_area()
		self.dataHandler.heatmapParameters["mappedIndices"] = np.rot90(self.dataHandler.heatmapParameters["mappedIndices"])

		for channel in self.dataHandler.channelData.values():
			channel["data"] = np.rot90(
				channel["data"]
			)
		self.dataHandler.plot_heatmap()

	def _flip_line_h(self, line) -> None:
		"""Flip a single line horizontal.

		Parameters:
			line(Line2D): The line to be flipped.
		"""
		m, n = np.shape(self.dataHandler._get_heatmap_data())
		flippedLine = line.get_xydata().copy()

		flippedLine[0][1] = m - flippedLine[0][1]
		flippedLine[1][1] = m - flippedLine[1][1]

		line.set_data(
			[flippedLine[0][0], flippedLine[1][0]], 
			[flippedLine[0][1], flippedLine[1][1]]
		)

	def _flip_area_h(self) -> None:
		"""Flip an area horizontal."""
		m, n = np.shape(self.dataHandler._get_heatmap_data())

		for i in range(len(self.selectedArea)):
			self.selectedArea[i][1] = m - self.selectedArea[i][1] - 1

	def _flip_line_v(self, line) -> None:
		"""Flip a single line vertical.

		Parameters:
			line(Line2D): The line to be flipped.
		"""
		m, n = np.shape(self.dataHandler._get_heatmap_data())
		flippedLine = line.get_xydata().copy()

		flippedLine[0][0] = n - flippedLine[0][0]
		flippedLine[1][0] = n - flippedLine[1][0]

		line.set_data(
			[flippedLine[0][0], flippedLine[1][0]], 
			[flippedLine[0][1], flippedLine[1][1]]
		)

	def _flip_area_v(self) -> None:
		"""Flip an area vertical."""
		m, n = np.shape(self.dataHandler._get_heatmap_data())

		for i in range(len(self.selectedArea)):
			self.selectedArea[i][0] = n - self.selectedArea[i][0] - 1 

	def _rotate_line(self, line) -> None:
		"""Rotate a single line by 90 degrees.

		Parameters:
			line(Line2D): The line to be rotated.
		"""
		m, n = np.shape(self.dataHandler._get_heatmap_data())
		rotatedLine = line.get_xydata().copy()
		
		rotatedLine[0] = [rotatedLine[0][1], n-rotatedLine[0][0]]
		rotatedLine[1] = [rotatedLine[1][1], n-rotatedLine[1][0]]

		line.set_data(
			[rotatedLine[0][0], rotatedLine[1][0]], 
			[rotatedLine[0][1], rotatedLine[1][1]]
		)

	def _rotate_area(self) -> None:
		"""Rotate an area by 90 degrees."""
		m, n = np.shape(self.dataHandler._get_heatmap_data())

		for i in range(len(self.selectedArea)):
			temp1, temp2 = self.selectedArea[i][1], n-self.selectedArea[i][0]-1
			self.selectedArea[i][0] = temp1
			self.selectedArea[i][1] = temp2

	def _orbit_area(self, area: Tuple[int, int], index: int) -> None:
		"""Orbit an area in the heatmap.

		Parameters:
			area(tuple): The entry to frame.
			index(int): An index to distinguish the different lines.
		"""
		# Plot left line.
		self._plot_marking_line((area[0], area[0]), (area[1], area[1]+1))
		# Plot right line.
		self._plot_marking_line((area[0]+1, area[0]+1), (area[1], area[1]+1))
		# Plot top line.
		self._plot_marking_line((area[0], area[0]+1), (area[1], area[1]))
		# Plot bottom line.
		self._plot_marking_line((area[0], area[0]+1), (area[1]+1, area[1]+1))

	def _plot_marking_line(
		self, 
		xValues: Tuple[int, int], 
		yValues: Tuple[int, int]
	) -> None:
		"""
		
		Parameters: 
			xValues(tuple):
			yValues(tuple):
		"""
		self.dataHandler.heatmapParameters["selectedArea"].append(
			self.holder.figure.get_axes()[0].plot(
				xValues, yValues, 
				color='r', linestyle='-', linewidth=2
			)[0]
		)

	def _delete_selected_area_lines(self) -> None:
		"""Delete existing marks."""
		for line in self.dataHandler.heatmapParameters["selectedArea"]:
			line.remove()
		self.dataHandler.heatmapParameters["selectedArea"] = []