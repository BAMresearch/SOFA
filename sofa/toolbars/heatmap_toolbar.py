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
import functools
from typing import List, Tuple, Optional

import matplotlib as mpl
import numpy as np 

from toolbars.sofa_toolbar import SofaToolbar

def decorator_check_selected_rectangle(function):
	"""
	
	"""
	@functools.wraps(function)
	def wrapper_check_selected_rectangle(self, *args):
		event = args[0]
		if self.xStart and self.yStart and event.xdata and event.ydata:
			function(self, *args)

	return wrapper_check_selected_rectangle

def decorator_check_selected_area(function):
	"""
	Check if an area is selected.
	"""
	@functools.wraps(function)
	def wrapper_check_selected_area(self):
		if len(self.selectedArea) != 0:
			function(self)

	return wrapper_check_selected_area

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
		"""
		"""
		# Set path for toolbar icons.
		iconPath = os.path.join(
			os.path.abspath(os.path.dirname(__file__)), 
			"icons", 
			"heatmap_toolbar"
		)
		toolItems = (
			("reset", "", os.path.join(iconPath, "reset.gif"), "_reset_heatmap"),
			("select_area", "", os.path.join(iconPath, "select_area.gif"), "_toggle_select_arbitrary_area"),
			("select_rectangle", "", os.path.join(iconPath, "select_rectangle.gif"), "_toggle_select_rectangular_area"),
			("include_area", "", os.path.join(iconPath, "include.gif"), "_include_area"),
			("exclude_area", "", os.path.join(iconPath, "exclude.gif"), "_exclude_area"),
			("flip_h", "", os.path.join(iconPath, "flip_h.gif"), "_flip_heatmap_horizontal"),
			("flip_v", "", os.path.join(iconPath, "flip_v.gif"), "_flip_heatmap_vertical"),
			("rotate", "", os.path.join(iconPath, "rotate.gif"), "_rotate_heatmap")
		)	
		self.guiInterface = guiInterface
		self.selectedArea = []
		self.selectedAreaOutlines = []

		super().__init__(canvas_, parent_, toolItems)

	def _reset_heatmap(self) -> None:
		"""
		Reset the selected area, the orientation 
		and the inactive data points.
		"""
		self.selectedArea = []
		self._delete_selected_area_outlines()

		self.guiInterface.reset_inactive_data_points()
		self.guiInterface.reset_heatmap_orientation()
		self.guiInterface.reset_heatmap_orientation_matrix()

		self.guiInterface.update_inactive_data_points_heatmap()
		
	def _toggle_select_arbitrary_area(self) -> None:
		"""
		Toggle the selector to select an arbitrary area.
		"""
		self._update_toolbar_mode("select arbitrary area")
		self._update_event_connections()
		self._update_toolbar_buttons()

	def _select_arbitrary_area_on_click(self, event) -> None:
		"""
		Prepare to capture and chache the mouse motion
		while a mouse button is clicked.
		"""
		self.selectedArea = []
	   
		self._add_motion_capture_event()

	def _add_motion_capture_event(self) -> None:
		"""
		Add a motion_notify_event to capture the mouse
		movement.
		"""
		self.eventConnections.append(
			self.holder.figure.canvas.mpl_connect(
				"motion_notify_event", 
				self._select_arbitrary_area_motion
			)
		)

	def _select_arbitrary_area_motion(self, event) -> None:
		"""
		Cache the mouse movement while the mouse 
		is within the heatmap.
		"""
		if event.xdata and event.ydata:
			self.selectedArea.append(
				(
					int(np.trunc(event.xdata)), 
					int(np.trunc(event.ydata))
				)
			)

	def _select_arbitrary_area_on_release(self, event) -> None:
		"""
		Select the arbitrary area over which the mouse has moved
		while a button was pressed and outline it in the heatmap.
		"""
		self._remove_motion_capture_event()
		self._delete_selected_area_outlines()		
		self._remove_double_values_from_selected_area()
		self._outline_area()

	def _remove_motion_capture_event(self) -> None: 
		"""
		Stop caching mouse movement.
		"""
		self.holder.figure.canvas.mpl_disconnect(
			self.eventConnections[-1]
		)
		del self.eventConnections[-1]

	def _delete_selected_area_outlines(self) -> None:
		"""
		Delete the old outlines.
		"""
		for outline in self.selectedAreaOutlines:
			outline.remove()
		self.selectedAreaOutlines = []

	def _remove_double_values_from_selected_area(self) -> None: 
		"""
		Remove potential duplicates in the selected area.
		"""
		self.selectedArea = [
			list(entry) 
			for entry 
			in set(self.selectedArea)
		]

	def _outline_area(self) -> None: 
		"""
		Outline an arbitrary area in the heatmap.
		"""
		for section in self.selectedArea:
			self._outline_section(section)
		
		self._delete_equal_outlines()
	
		self.holder.draw()

	def _outline_section(
		self, 
		section: Tuple[int, int]
	) -> None:
		"""
		Outline a section/single point in the heatmap.

		Parameters
		----------
		section : tuple[int]
			X and y coordinates of the data point 
			to be outlined.
		"""
		# Plot left line.
		self._plot_outline(
			(section[0], section[0]), 
			(section[1], section[1]+1)
		)
		# Plot right line.
		self._plot_outline(
			(section[0]+1, section[0]+1), 
			(section[1], section[1]+1)
		)
		# Plot top line.
		self._plot_outline(
			(section[0], section[0]+1), 
			(section[1], section[1])
		)
		# Plot bottom line.
		self._plot_outline(
			(section[0], section[0]+1), 
			(section[1]+1, section[1]+1)
		)

	def _delete_equal_outlines(self) -> None:
		"""
		Find all outlines that exist more than once and delete them.
		"""
		outlineData = [
			outline.get_xydata() 
			for outline 
			in self.selectedAreaOutlines
		]
		uniqueValues, count = np.unique(
			outlineData, 
			axis=0, 
			return_counts=True
		)
		doubledValues = uniqueValues[np.where(count > 1)]
		
		doubledIndices = []

		for index, outline in enumerate(self.selectedAreaOutlines):
			for doubledValue in doubledValues:
				if np.array_equal(outline.get_xydata(), doubledValue):
					outline.remove()
					doubledIndices.append(index)

		self.selectedAreaOutlines = [
			outline
			for index, outline in enumerate(self.selectedAreaOutlines) 
			if index not in doubledIndices
		]

	def _toggle_select_rectangular_area(self) -> None:
		"""
		Toggle the selector to select a rectangular area.
		"""
		self._update_toolbar_mode("select rectangular area")
		self._update_event_connections()
		self._update_toolbar_buttons()

	def _select_rectangular_area_on_click(self, event) -> None:
		"""
		Cache startingpoint of the rectangular area,
		if it is within the heatmap.
		"""
		self.selectedArea = []
		self.xStart = self.yStart = 0
	   
		if event.xdata and event.ydata:
			self.xStart = event.xdata
			self.yStart = event.ydata

	@decorator_check_selected_rectangle
	def _select_rectangular_area_on_release(self, event) -> None:
		"""
		Select all data points in the rectangular area
		and outline the area in the heatmap.
		"""
		self._delete_selected_area_outlines()
		
		xStart, xEnd = self._standardize_value_pair(self.xStart, event.xdata)
		yStart, yEnd = self._standardize_value_pair(self.yStart, event.ydata)
		
		xStart = int(np.trunc(xStart))
		xEnd = int(np.ceil(xEnd))
		yStart = int(np.trunc(yStart))
		yEnd = int(np.ceil(yEnd))

		self.selectedArea = self._get_data_points_in_rectangular_area(
			xStart, xEnd, yStart, yEnd
		)
		
		self._plot_outline((xStart, xStart), (yStart, yEnd))
		self._plot_outline((xStart, xEnd), (yStart, yStart))
		self._plot_outline((xEnd, xEnd), (yStart, yEnd))
		self._plot_outline((xEnd, xStart), (yEnd, yEnd))

		self.holder.draw()

	@staticmethod
	def _get_data_points_in_rectangular_area(
		xStart: int, 
		xEnd: int, 
		yStart: int, 
		yEnd: int
	) -> List[List[int]]:
		"""
		. 

		Parameters
		----------
		xStart : int 
			X value of one corner of the rectangular area.
		xEnd : int
			X value of the opposite corner of the rectangular area.
		yStart : int
			Y value of one corner of the rectangular area.
		yEnd : int
			Y value of the opposite corner of the rectangular area.

		Returns
		-------
		selectedArea : list
			A list of all points within the rectangular area.
		"""
		return [
			[i, j] 
			for i in range(xStart, xEnd) 
			for j in range(yStart, yEnd)
		]

	@decorator_check_selected_area
	def _include_area(self) -> None:
		"""
		Add everything except the selected area to the inactive data points.
		"""
		m, n = self.guiInterface._get_active_force_volume().size
		# Map new inactive points in a two dimensional array to their corresponding points in a one dimensional array.
		newInactiveDataPoints = [
			i 
			for i in range(m * n) 
			if i not in [dataPoint[1] * n + dataPoint[0] 
			for dataPoint in self.selectedArea]
		]

		self.selectedArea = []
		self._delete_selected_area_outlines()	
		
		self.guiInterface.add_inactive_data_points(newInactiveDataPoints)

		self.guiInterface.update_inactive_data_points_heatmap()

	@decorator_check_selected_area
	def _exclude_area(self) -> None:
		"""
		Add the selected area to the inactive data points.
		"""
		m, n = self.guiInterface._get_active_force_volume().size 
		# Map new inactive points in a two dimensional array to their corresponding points in a one dimensional array.
		newInactiveDataPoints = [dataPoint[1] * n + dataPoint[0] for dataPoint in self.selectedArea]
	
		self.selectedArea = []
		self._delete_selected_area_outlines()	
		
		self.guiInterface.add_inactive_data_points(newInactiveDataPoints)

		self.guiInterface.update_inactive_data_points_heatmap()

	def _flip_heatmap_horizontal(self) -> None:
		"""
		Flip the heatmap horizontal.
		"""
		self._flip_selected_area_horizontal()
		self._flip_selected_area_outlines_horizontal()
		
		self.guiInterface.flip_heatmap_orientation_matrix_horizontal()
		self.guiInterface.flip_channel_horizontal()

		self.guiInterface.plot_heatmap()

	def _flip_selected_area_horizontal(self) -> None:
		"""
		Flip the selected area horizontal.
		"""
		m, n = self.guiInterface._get_active_force_volume().size

		for i in range(len(self.selectedArea)):
			self.selectedArea[i][1] = m - self.selectedArea[i][1] - 1

	def _flip_selected_area_outlines_horizontal(self) -> None: 
		"""
		Flip the outlines of the selected area horizontal.
		"""
		for outline in self.selectedAreaOutlines:
			self._flip_outline_horizontal(outline)

	def _flip_outline_horizontal(
		self, 
		outline: mpl.lines.Line2D
	) -> None:
		"""
		Flip a single outline horizontal.

		Parameters
		----------
		outline : mpl.lines.Line2D
			The outline to be flipped.
		"""
		m, n = self.guiInterface._get_active_force_volume().size
		flippedLine = outline.get_xydata().copy()

		flippedLine[0][1] = m - flippedLine[0][1]
		flippedLine[1][1] = m - flippedLine[1][1]

		outline.set_data(
			[flippedLine[0][0], flippedLine[1][0]], 
			[flippedLine[0][1], flippedLine[1][1]]
		)

	def _flip_heatmap_vertical(self) -> None: 
		"""
		Flip the heatmap vertical.
		"""
		self._flip_selected_area_vertical()
		self._flip_selected_area_outlines_vertical()

		self.guiInterface.flip_heatmap_orientation_matrix_vertical()
		self.guiInterface.flip_channel_vertical()

		self.guiInterface.plot_heatmap()

	def _flip_selected_area_vertical(self) -> None:
		"""
		Flip the selected area vertical.
		"""
		m, n = self.guiInterface._get_active_force_volume().size

		for i in range(len(self.selectedArea)):
			self.selectedArea[i][0] = n - self.selectedArea[i][0] - 1 

	def _flip_selected_area_outlines_vertical(self) -> None: 
		"""
		Flip the outlines of the selected area vertical.
		"""
		for outline in self.selectedAreaOutlines:
			self._flip_outline_vertical(outline)

	def _flip_outline_vertical(
		self, 
		outline: mpl.lines.Line2D
	) -> None:
		"""
		Flip a single outline vertical.

		Parameters
		----------
		outline : mpl.lines.Line2D
			The outline to be flipped.
		"""
		m, n = self.guiInterface._get_active_force_volume().size
		flippedLine = outline.get_xydata().copy()

		flippedLine[0][0] = n - flippedLine[0][0]
		flippedLine[1][0] = n - flippedLine[1][0]

		outline.set_data(
			[flippedLine[0][0], flippedLine[1][0]], 
			[flippedLine[0][1], flippedLine[1][1]]
		)

	def _rotate_heatmap(self) -> None:
		"""
		Rotate the heatmap by 90 degrees to the left.
		"""	
		self._rotate_selected_area()
		self._rotate_selected_area_outlines()

		self.guiInterface.rotate_heatmap_orientation_matrix()
		self.guiInterface.rotate_channel()
		
		self.guiInterface.plot_heatmap()

	def _rotate_selected_area(self) -> None:
		"""
		Rotate an area by 90 degrees.
		"""
		m, n = self.guiInterface._get_active_force_volume().size

		for i in range(len(self.selectedArea)):
			temp1, temp2 = self.selectedArea[i][1], n-self.selectedArea[i][0]-1
			self.selectedArea[i][0] = temp1
			self.selectedArea[i][1] = temp2

	def _rotate_selected_area_outlines(self) -> None: 
		"""
		Rotate the outlines of the selected area.
		"""
		for outline in self.selectedAreaOutlines:
			self._rotate_outline(outline)

	def _rotate_outline(
		self, 
		outline: mpl.lines.Line2D
	) -> None:
		"""
		Rotate a single outline by 90 degrees.

		Parameters
		----------
		outline : mpl.lines.Line2D
			The outline to be rotated.
		"""
		m, n = self.guiInterface._get_active_force_volume().size
		rotatedLine = outline.get_xydata().copy()
		
		rotatedLine[0] = [rotatedLine[0][1], n-rotatedLine[0][0]]
		rotatedLine[1] = [rotatedLine[1][1], n-rotatedLine[1][0]]

		outline.set_data(
			[rotatedLine[0][0], rotatedLine[1][0]], 
			[rotatedLine[0][1], rotatedLine[1][1]]
		)

	def _plot_outline(
		self, 
		xValues: Tuple[int, int], 
		yValues: Tuple[int, int]
	) -> None:
		"""
		
		Parameters: 
			xValues(tuple):
			yValues(tuple):
		"""
		self.selectedAreaOutlines.append(
			self.holder.figure.get_axes()[0].plot(
				xValues, 
				yValues, 
				color="r", 
				linestyle="-", 
				linewidth=2
			)[0]
		)