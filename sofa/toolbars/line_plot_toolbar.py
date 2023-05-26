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
import data_processing.named_tuples as nt

def decorator_check_zoom_history_empty(function):
	"""
	Check if the zoom history is not empty.
	"""
	@functools.wraps(function)
	def wrapper_check_zoom_history_empty(self, *args):
		activePlotInterface = args[0]
		if activePlotInterface.zoomHistory:
			function(self, *args)

	return wrapper_check_zoom_history_empty

def decorator_check_zoom_inside_axes(function):
	"""
	Check if the zoom motion starts and ends within
	the axes.
	"""
	@functools.wraps(function)
	def wrapper_check_zoom_inside_axes(self, *args):
		event = args[1]
		if self.zoomXStart and self.zoomYStart and event.xdata and event.ydata:
			function(self, *args)

	return wrapper_check_zoom_inside_axes

def decorator_check_zoom_valid(function):
	"""
	.
	"""
	@functools.wraps(function)
	def wrapper_check_zoom_valid(self, *args):
		event = args[1]
		if self.zoomXStart != event.xdata and self.zoomYStart != event.ydata:
			function(self, *args)

	return wrapper_check_zoom_valid

class LinePlotToolbar(SofaToolbar):
	"""
	A custom toolbar to process data, displayed in a line plot.

	Attributes
	----------
	guiInterface : GUIInterface
		 Handles the state and different display options of the data.
	holder : 
	
	mode : str

	eventConnections : list[]

	"""
	def __init__(self, canvas_, parent_, guiInterface):
		# Set path for toolbar icons.
		iconPath = os.path.join(
			os.path.abspath(os.path.dirname(__file__)), 
			"icons", 
			"line_plot_toolbar"
		)
		toolItems = (
			("reset", "", os.path.join(iconPath, "reset.gif"), "_reset_line_plot"),
			("zoom_in", "", os.path.join(iconPath, "zoom.gif"), "_toggle_zoom_in"),
			("zoom_out", "", os.path.join(iconPath, "zoom_out.gif"), "_zoom_out"),
			("reset_zoom", "", os.path.join(iconPath, "zoom_reset.gif"), "_reset_zoom"),
			("pick_single", "", os.path.join(iconPath, "pick_one.gif"), "_toggle_pick_single_line"),
			("pick_multiple", "", os.path.join(iconPath, "pick_all.gif"), "_pick_multiple_lines")
		)
		super().__init__(canvas_, parent_, toolItems, guiInterface)

	@SofaToolbar.decorator_get_active_plot_interface
	def _reset_line_plot(
		self,
		activePlotInterface
	) -> None:
		"""
		Reset zoom and the inactive data points.

		Parameters
		----------
		activePlotInterface : PlotInterface

		"""
		self._reset_zoom()

		activePlotInterface.reset_inactive_data_points()
		self.guiInterface.update_inactive_data_points_line_plot()
	
	@SofaToolbar.decorator_get_active_plot_interface
	@decorator_check_zoom_history_empty
	def _reset_zoom(
		self, 
		activePlotInterface
	) -> None:
		"""
		Reset zoom.

		Parameters
		----------
		activePlotInterface : PlotInterface
		"""
		self._set_zoom(
			activePlotInterface.zoomHistory[0]
		)		
		activePlotInterface.zoomHistory = []

		self.holder.draw()

	@SofaToolbar.decorator_get_active_plot_interface
	@decorator_check_zoom_history_empty
	def _zoom_out(
		self, 
		activePlotInterface
	) -> None:
		"""
		Set zoom to the previous one.

		Parameters
		----------
		activePlotInterface : PlotInterface

		"""
		self._set_zoom(
			activePlotInterface.zoomHistory[-1]
		)
		del activePlotInterface.zoomHistory[-1:]
		
		self.holder.draw()

	def _toggle_zoom_in(self) -> None:
		"""
		Toggle the selector to zoom.
		"""
		self._update_toolbar_mode("zoom in")
		self._update_event_connections()
		self._update_toolbar_buttons()

	def _start_zoom_motion(
		self, 
		event: mpl.backend_bases.MouseEvent
	) -> None:
		"""
		Buffer the starting point for zooming, if it 
		exists.

		Parameters
		----------
		event : mpl.backend_bases.MouseEvent
			button_press_event triggers when the 
			mouse button is pressed.
		"""
		self.zoomXStart = self.zoomYStart = 0

		if event.xdata and event.ydata:
			self.zoomXStart = event.xdata
			self.zoomYStart = event.ydata

	@SofaToolbar.decorator_get_active_plot_interface
	@decorator_check_zoom_inside_axes
	@decorator_check_zoom_valid
	def _end_zoom_motion(
		self,
		activePlotInterface,
		event: mpl.backend_bases.MouseEvent
	) -> None:
		"""
		Zoom to the spanned rectangle, if it is
		within the axes.

		Parameters
		----------
		activePlotInterface : PlotInterface

		event : mpl.backend_bases.MouseEvent
			button_release_event triggers when the 
			mouse button is released.
		"""
		# Save current view limits.
		currentViewLimits = self._get_view_limits()
		activePlotInterface.zoomHistory.append(currentViewLimits)

		standardizedViewLimits = self._get_standardized_view_limits(
			self.zoomXStart,
			event.xdata,
			self.zoomYStart,
			event.ydata
		)
		
		self._set_zoom(standardizedViewLimits)
		
		self.holder.draw()

	def _get_view_limits(self) -> nt.ViewLimits:
		"""
		

		Returns
		-------
		currentViewLimits : nt.ViewLimits

		"""
		axes = self.holder.figure.get_axes()[0]

		viewXMin, vieXMax = axes.get_xlim()
		viewYMin, viewYMax = axes.get_ylim()

		return nt.ViewLimits(
			viewXMin,
			vieXMax,
			viewYMin,
			viewYMax
		)

	def _get_standardized_view_limits(
		self,
		zoomXStart: int,
		zoomXEnd: int,
		zoomYStart: int,
		zoomYEnd: int
	) -> nt.ViewLimits:
		"""
		"""
		zoomXStart, zoomXEnd = self._standardize_value_pair(
			zoomXStart, 
			zoomXEnd
		)
		zoomYStart, zoomYEnd = self._standardize_value_pair(
			zoomYStart, 
			zoomYEnd
		)

		return nt.ViewLimits(
			zoomXStart,
			zoomXEnd,
			zoomYStart,
			zoomYEnd
		)

	def _set_zoom(
		self, 
		viewLimits: nt.ViewLimits
	) -> None: 
		"""


		Parameters
		----------
		viewLimits : nt.ViewLimits
		"""
		axes = self.holder.figure.get_axes()[0]

		axes.set_xlim(viewLimits.xMin, viewLimits.xMax)
		axes.set_ylim(viewLimits.yMin, viewLimits.yMax)

	def _toggle_pick_single_line(self) -> None:
		"""Toggle the selctor to pick a single curve."""
		self._update_toolbar_mode("pick single line")
		self._update_event_connections()
		self._update_toolbar_buttons()
	
	def _pick_single_line(
		self, 
		event: mpl.backend_bases.PickEvent
	) -> None:
		"""
		Click a curve to toggle it's state.

		Parameters
		----------
		event : mpl.backend_bases.PickEvent
			pick_event triggers when a line is
			selected.
		"""
		self._toggle_line(event.artist)
		self.guiInterface.update_inactive_data_points_line_plot()

	def _pick_multiple_lines(self) -> None:
		"""
		Select all currently visiable curves that 
		have a datapoint within the current view limits.
		"""
		currentViewLimits = self._get_view_limits()
		
		for line in self.holder.figure.get_axes()[0].get_lines():
			hasIntersection = self._check_line_intersection(
				line, 
				currentViewLimits
			)
			
			if hasIntersection:
				self._deactivate_line(line)
		
		self.guiInterface.update_inactive_data_points_line_plot()

	def _check_line_intersection(
		self,
		line: mpl.lines.Line2D, 
		currentViewLimits: nt.ViewLimits
	) -> bool:
		"""
		Check whether a line lies within the current view limits.
		
		Paramters
		---------
		line : matplotlib.lines.Line2D
			Line to be checked.
		currentViewLimits : nt.ViewLimits
			Contains the current x and y view limits.

		Returns
		-------
		hasIntersection : bool
			True if the line has a data point within the current
			view limits, otherwise false.
		"""
		validLineXData, validLineYData = self._get_valid_line_data(line)

		xIntersections = self._get_value_intersections(
			validLineXData,
			currentViewLimits.xMin,
			currentViewLimits.xMax
		)
		yIntersections = self._get_value_intersections(
			validLineYData,
			currentViewLimits.yMin,
			currentViewLimits.yMax
		)
		# If there is a x and y intersection at the same time, the line lies within the view.
		if np.any(np.isin(xIntersections, yIntersections)):
			return True

		return False

	@staticmethod
	def _get_valid_line_data(
		line: mpl.lines.Line2D
	) -> Tuple[np.ndarray]:
		"""


		Parameters
		----------
		line : matplotlib.lines.Line2D


		Returns
		-------
		validLineXData : np.ndarray

		validLineYData : np.ndarray
		"""
		lineData = line.get_xydata()
		
		lineXData = lineData[:,0]
		lineYData = lineData[:,1]
		validLineXData = lineXData[~np.isnan(lineXData)]
		validLineYData = lineYData[~np.isnan(lineYData)]

		return validLineXData, validLineYData

	@staticmethod
	def _get_value_intersections(
		validLineData: np.ndarray,
		minimumBorder: float,
		maximumBorder: float
	) -> np.ndarray:
		"""
		"""
		return np.where(
			np.logical_and(validLineData >= minimumBorder, validLineData <= maximumBorder)
		)

	@SofaToolbar.decorator_get_active_plot_interface
	def _toggle_line(
		self,
		activePlotInterface,
		line: mpl.lines.Line2D
	) -> None:
		"""
		Toggle the state of a curve.

		Paramerters
		-----------
		activePlotInterface : PlotInterface

		line : matplotlib.lines.Line2D
			Line representation of the curve that is toggled.
		"""
		if line.get_color() == "gray":
			activePlotInterface.remove_inactive_data_point(int(line._label))
		elif line.get_color() == "red":
			activePlotInterface.add_inactive_data_point(int(line._label))

	@SofaToolbar.decorator_get_active_plot_interface
	def _deactivate_line(
		self,
		activePlotInterface,
		line: mpl.lines.Line2D
	) -> None:
		"""
		Deactivate a curve.

		Paramerters
		-----------
		activePlotInterface : PlotInterface

		line : matplotlib.lines.Line2D
			Line representation of the curve that is deactivated.
		"""
		if line.get_color() == "red":
			activePlotInterface.add_inactive_data_point(int(line._label))