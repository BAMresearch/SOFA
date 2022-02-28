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
from collections import namedtuple
from typing import List, Tuple, Optional, NamedTuple

import numpy as np 
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backend_bases import NavigationToolbar2
from matplotlib.lines import Line2D
import tkinter as tk
import tkinter.font

class LinePlotToolbar(NavigationToolbar2Tk):
	'''
	A custom toolbar to process data, displayed as a lineplot.

	Paramters:
		dataHandler(object): Handles the state and different display options of the data.
	'''
	def __init__(self, canvas_, parent_, dataHandler):
		# Set path for toolbar icons.
		iconPath = os.path.join(
			os.path.abspath(os.path.dirname(__file__)), 
			"icons", "curves_toolbar"
		)
		self.toolitems = (
			("reset", "", os.path.join(iconPath, "reset.gif"), "_reset_line_plot"),
			("zoom_in", "", os.path.join(iconPath, "zoom.gif"), "_toggle_zoom_in"),
			("zoom_out", "", os.path.join(iconPath, "zoom_out.gif"), "_zoom_out"),
			("reset_zoom", "", os.path.join(iconPath, "zoom_reset.gif"), "_reset_zoom"),
			("pick_single", "", os.path.join(iconPath, "pick_one.gif"), "_toggle_pick_single_line"),
			("pick_multiple", "", os.path.join(iconPath, "pick_all.gif"), "_pick_multiple_lines"),
			("show_inactive", "", os.path.join(iconPath, "pick_all.gif"), "_show_inactive"),
			("display_average", "", os.path.join(iconPath, "average.gif"), "_display_average"),
			("display_errorbar", "", os.path.join(iconPath, "errorbar.gif"), "_display_as_errorbar")
		)

		self.dataHandler = dataHandler
		self.holder = canvas_
		self.eventConnections = []
		self.zoomHist = []

		self.activeButtonColor = "#999999"
		self.inactiveButtonColor = "#ffffff"

		ViewLimits = namedtuple("ViewLimits", "xMin xMax yMin yMax")

		# Overwrite Matplotlib NavigationToolbar2Tk init to load toolbar icons from a custom location.
		self.window = parent_
		
		tk.Frame.__init__(
			self, master=parent_, borderwidth=2,
			width=int(canvas_.figure.bbox.width), height=50
		)

		self._buttons = {}
		# Changed file path to load SOFA toolbar icons. 
		for text, tooltip_text, image_file, callback in self.toolitems:
			self._buttons[text] = super()._Button(
				text, 
				image_file,
				toggle=False, 
				command=getattr(self, callback)
			)

		self._label_font = tk.font.Font(root=parent_, size=10)

		label = tk.Label(
			master=self, font=self._label_font,
			text='\N{NO-BREAK SPACE}\n\N{NO-BREAK SPACE}'
		)
		label.pack(side=tk.RIGHT)

		self.message = tk.StringVar(master=self)
		self._message_label = tk.Label(
			master=self, font=self._label_font,
			textvariable=self.message
		)
		self._message_label.pack(side=tk.RIGHT)

		NavigationToolbar2.__init__(self, canvas_)
		
		self.pack(side=tk.BOTTOM, fill=tk.X)

		for button in self._buttons.values():
			button.configure(bg="#ffffff")

	def _reset_line_plot(self) -> None:
		"""Reset zoom and the inactive data points."""
		self._reset_zoom()

		self.dataHandler.inactiveDataPoints = []

		self._check_interactive_plot()
	
	def _reset_zoom(self) -> None:
		"""Reset zoom."""
		try:
			self.holder.figure.get_axes()[0].set_xlim(self.zoomHist[0])
			self.holder.figure.get_axes()[0].set_ylim(self.zoomHist[1])
		except IndexError:
			return
			
		self.zoomHist = []

		self.holder.draw()

	def _zoom_out(self) -> None:
		"""Set zoom to the previous one."""
		try:
			self.holder.figure.get_axes()[0].set_xlim(self.zoomHist[-2])
			self.holder.figure.get_axes()[0].set_ylim(self.zoomHist[-1])
		except IndexError:
			return

		del self.zoomHist[-2:]
		
		self.holder.draw()

	def _toggle_zoom_in(self) -> None:
		"""Toggle the selector to zoom."""
		self._update_mode("zoom in")
		self._update_event_connections()
		self._update_toolbar_buttons()

	def _start_zoom_motion(self, event) -> None:
		"""Buffer the starting point for zooming, if existing."""
		self.xStart = self.yStart = 0

		if event.xdata:
			self.xStart = event.xdata
			self.yStart = event.ydata

	def _end_zoom_motion(self, event) -> None:
		"""Zoom to the marked rectangle, if it's located in the axis'"""
		# Return if zooming starts or ends outside of the lineplot.
		if not self.xStart or not event.xdata or not event.ydata:
			return

		# Return if the area was is to small.
		if self.xStart == event.xdata or self.yStart == event.ydata:
			return 

		# Save old view limits.
		self.zoomHist.extend(
			[
				self.holder.figure.get_axes()[0].get_xlim(), 
				self.holder.figure.get_axes()[0].get_ylim()
			]
		)

		# Standardize zoom data.
		if self.xStart > event.xdata:
			self.xStart, event.xdata = event.xdata, self.xStart
		if self.yStart > event.ydata:
			self.yStart, event.ydata = event.ydata, self.yStart
		
		# Set zoom.
		self.holder.figure.get_axes()[0].axis(
			(self.xStart, event.xdata, self.yStart, event.ydata)
		)
		
		self.holder.draw()

	def _toggle_pick_single_line(self) -> None:
		"""Toggle the selctor to pick a single curve."""
		self._update_mode("pick single line")
		self._update_event_connections()
		self._update_toolbar_buttons()
	
	def _pick_single_line(self, event) -> None:
		"""Click curve to toggle it's state.

		Parameters:
			event(event): Current click event.
		"""
		self._toggle_line(event.artist)

		self._check_interactive_plot()

	def _pick_multiple_lines(self) -> None:
		"""Select all currently visiable curves that 
		   have a datapoint within the current view limits."""
		ViewLimits = namedtuple(
			"ViewLimits",
			[
				"xMin",
				"xMax",
				"yMin",
				"yMax",
			]
		)

		xMin, xMax = self.holder.figure.get_axes()[0].get_xlim()
		yMin, yMax = self.holder.figure.get_axes()[0].get_ylim()

		currentViewLimits = ViewLimits(xMin, xMax, yMin, yMax)
		
		for line in self.holder.figure.get_axes()[0].get_lines():
			hasIntersection = self._check_line_intersection(line, currentViewLimits)
			
			if hasIntersection:
				self._deactivate_line(line)
		
		self._check_interactive_plot()

	@staticmethod
	def _check_line_intersection(line, currentViewLimits: NamedTuple) -> bool:
		"""Check whether a line lies within the current view limits.
		
		Paramters:
			line(Line2D): Current line.
			currentViewLimits(namedtuple): Tuple that contains the current view limits

		Returns: 
			hasIntersection(bool): True if a data point of the line lies within the current
								   view limits, otherwise false.
		"""
		# Get valid line data.
		lineXData = np.asarray(line.get_xdata())
		lineXData = lineXData[~np.isnan(lineXData)]
		lineYData = np.asarray(line.get_ydata())
		lineYData = lineYData[~np.isnan(lineYData)]
		# Check  whether the line has x/y values within the the view limits.
		xIntersections = np.where(
			np.logical_and(lineXData >= currentViewLimits.xMin, lineXData <= currentViewLimits.xMax)
		)
		yIntersections = np.where(
			np.logical_and(lineYData >= currentViewLimits.yMin, lineYData <= currentViewLimits.yMax)
		)
		# If there is a x and y intersection at the same time, the line lies within the view.
		if np.any(np.isin(xIntersections, yIntersections)):
			return True

		return False

	def _toggle_line(self, line) -> None:
		"""Toggle line state.

		Paramerters:
			line(Line2D): Clicked line.
		"""
		if line.get_color() == "gray":
			self.dataHandler.inactiveDataPoints.remove(int(line._label))
		elif line.get_color() == "red":
			self.dataHandler.inactiveDataPoints.append(int(line._label))

	def _deactivate_line(self, line) -> None:
		"""Deactivate a line.

		Paramerters:
			line(Line2D): Line to deactivate.
		"""
		if line.get_color() == "red":
			self.dataHandler.inactiveDataPoints.append(int(line._label))

	def _show_inactive(self) -> None:
		"""Toggle the option to show only active lines."""
		self.dataHandler.linePlotParameters["showInactive"] = not self.dataHandler.linePlotParameters["showInactive"]

		self.dataHandler.update_lines()

	def _display_average(self) -> None:
		"""Toggle the average line."""
		if self.dataHandler.linePlotParameters["displayAverage"]:
			self.dataHandler.remove_average_curve()
			self.dataHandler.linePlotParameters["holder"].draw()
		else:
			self.dataHandler.calculate_average()
			
		self.dataHandler.linePlotParameters["displayAverage"] = not self.dataHandler.linePlotParameters["displayAverage"]

	def _display_as_errorbar(self) -> None:
		"""Toggle the errorbar."""
		if self.dataHandler.linePlotParameters["displayAverage"] is False:
			return

		self.dataHandler.linePlotParameters["displayErrorbar"] = not self.dataHandler.linePlotParameters["displayErrorbar"]

		self.dataHandler.calculate_average()

	def _update_mode(self, newMode: str) -> None:
		"""Update the mode of the toolbar.

		Parameters:
			newMode(str): The new active toolbar mode.
		"""
		if self.mode == newMode:
			self.mode = ""
		else:
			self.mode = newMode

	def _update_event_connections(self) -> None:
		"""Update event connections in dependace of the current mode."""
		self._delete_all_event_connections()

		if self.mode == "zoom in":
			self.eventConnections.extend(
				(
					self.holder.figure.canvas.mpl_connect("button_press_event", self._start_zoom_motion),
				 	self.holder.figure.canvas.mpl_connect("button_release_event", self._end_zoom_motion)
				)
			)
		elif self.mode == "pick single line":
			self.eventConnections.append(
				self.holder.figure.canvas.mpl_connect("pick_event", self._pick_single_line),
			)

	def _delete_all_event_connections(self) -> None:
		"""Disconnect and delete all event connections."""
		for connection in self.eventConnections:
			self.holder.figure.canvas.mpl_disconnect(connection)

		self.eventConnections = []

	def _update_toolbar_buttons(self) -> None:
		"""Update the state of the toolbar buttons."""
		if self.mode == "":
			inactiveButtons = [
				self._buttons["zoom_in"],
				self._buttons["pick_single"]
			]
			self._set_toolbar_button_state(inactiveButtons)
		elif self.mode == "zoom in":
			inactiveButtons = [self._buttons["pick_single"]]
			self._set_toolbar_button_state(
				inactiveButtons, self._buttons["zoom_in"]
			)
		elif self.mode == "pick single line":
			inactiveButtons = [self._buttons["zoom_in"]]
			self._set_toolbar_button_state(
				inactiveButtons, self._buttons["pick_single"]
			)

	def _set_toolbar_button_state(
		self, 
		inactiveButtons: List[tk.Button], 
		activeButton: Optional[tk.Button] = None
	) -> None:
		"""Mark buttons as either active or inactive.

		Parameters:
			inactiveButtons(list): List with the new inactive buttons. 
			activeButton(tk.Button): Potential new active button.
		"""
		for button in inactiveButtons:
			button.configure(bg=self.inactiveButtonColor)

		if activeButton:
			activeButton.configure(bg=self.activeButtonColor)

	def _check_interactive_plot(self) -> None:
		"""Check if all plots or only the line plot are updated."""
		if self.dataHandler.linePlotParameters["interactive"].get():
			self.dataHandler.update_plots()
		else:
			self.dataHandler.update_line_plot()