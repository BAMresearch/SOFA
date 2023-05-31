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
from typing import Optional, Tuple
import functools

from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backend_bases import NavigationToolbar2
import tkinter as tk
import tkinter.font

class SofaToolbar(NavigationToolbar2Tk):
	"""
	Base class for the line plot and heatmap toolbar, which 
	contains their shared attributes and functionalities.
	
	Attributes
	----------
	holder : mpl.backends.backend_tkagg.FigureCanvasTkAgg
		Interface between the matplotlib figure of the line 
		plot/heatmap and the main window of SOFA.
	guiInterface : GUIInterface
		Interface between the diffenrent SOFA windwos and 
		imported measurement data sets.
	mode : str
		Identifier of the currently active toolbar mode.
	eventConnectionIds : list
		Contains all active matplotlib event connections ids. 
	activeButtonColor : str
		Color for the active toolbar buttons.
	inactiveButtonColor : str
		Color for the inactive toolbar buttons.
	"""
	def decorator_get_active_data_set(function):
		"""
		Get the active force volume and plot interface.
		"""
		@functools.wraps(function)
		def wrapper_get_active_data_set(self, *args, **kwargs):
			activeForceVolume = self.guiInterface.get_active_force_volume()
			activePlotInterface = self.guiInterface.get_active_plot_interface()
			function(self, activeForceVolume, activePlotInterface, *args, **kwargs)

		return wrapper_get_active_data_set

	def decorator_get_active_force_volume(function):
		"""
		Get the active force volume.
		"""
		@functools.wraps(function)
		def wrapper_get_active_force_volume(self, *args, **kwargs):
			activeForceVolume = self.guiInterface.get_active_force_volume()
			function(self, activeForceVolume, *args, **kwargs)

		return wrapper_get_active_force_volume

	def decorator_get_active_plot_interface(function):
		"""
		Get the active plot interface.
		"""
		@functools.wraps(function)
		def wrapper_get_active_plot_interface(self, *args, **kwargs):
			activePlotInterface = self.guiInterface.get_active_plot_interface()
			function(self, activePlotInterface, *args, **kwargs)

		return wrapper_get_active_plot_interface

	def __init__(self, canvas_, parent_, toolItems, guiInterface):
		"""
		Initialise a toolbar with custom tool items and icons
		and adjust the button color of the toolbar to match 
		the background color of the main window of SOFA.
		"""
		self.holder = canvas_
		self.guiInterface = guiInterface
		self.mode: str = ""
		self.eventConnectionIds = []

		self.activeButtonColor: str = "#999999"
		self.inactiveButtonColor: str = "#ffffff"

		self._init_navigation_toolbar_2Tk(canvas_, parent_, toolItems)
		self._adjust_button_color()

	def _init_navigation_toolbar_2Tk(
		self, 
		canvas_, 
		parent_, 
		toolitems
	) -> None: 
		"""
		Overwrite the NavigationToolbar2Tk __init__ to be
		able to load the toolbar icons from a custom location.
		"""
		self.window = parent_
		
		tk.Frame.__init__(
			self, master=parent_, borderwidth=2,
			width=int(canvas_.figure.bbox.width), height=50
		)

		self._buttons = {}
		# Changed file path to load SOFA toolbar icons. 
		for text, tooltip_text, image_file, callback in toolitems:
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

	def _adjust_button_color(self) -> None:
		"""
		Adjust the color of the toolbar buttons to the
		background color of the main window.
		"""
		for button in self._buttons.values():
			button.configure(bg=self.inactiveButtonColor)

	@staticmethod
	def _standardize_value_pair(
		firstValue: float, 
		secondValue: float
	) -> Tuple[float]:
		"""
		Standardize two values by ensuring that the first
		one ist smaller than the second one.

		Parameters
		----------
		firstValue : float
			The first value of the value pair.
		secondValue : float
			The second value of the value pair.

		Returns
		-------
		firstValue : float
			The smaller value of the value pair.
		secondValue : float
			The bigger value of the value pair.
		"""
		if firstValue > secondValue:
			return secondValue, firstValue

		return firstValue, secondValue

	def _update_toolbar_mode(self, newMode: str) -> None:
		"""
		Update the mode of the toolbar.

		Parameters
		----------
		newMode : str
			The new active toolbar mode.
		"""
		if self.mode == newMode:
			self.mode = ""
		else:
			self.mode = newMode

	def _update_event_connections(self) -> None:
		"""
		Update event connections in dependace of the current mode.
		"""
		self._reset_event_connections()

		# Line plot toolbar modes
		if self.mode == "zoom in":
			self.eventConnectionIds.extend(
				(
					self.holder.figure.canvas.mpl_connect("button_press_event", self._start_zoom_motion),
				 	self.holder.figure.canvas.mpl_connect("button_release_event", self._end_zoom_motion)
				)
			)
		elif self.mode == "pick single line":
			self.eventConnectionIds.append(
				self.holder.figure.canvas.mpl_connect("pick_event", self._pick_single_line),
			)
		# Heatmap toolbar modes
		elif self.mode == "select arbitrary area":
			self.eventConnectionIds.extend(
				(
					self.holder.figure.canvas.mpl_connect("button_press_event", self._select_arbitrary_area_on_click),
					self.holder.figure.canvas.mpl_connect("button_release_event", self._select_arbitrary_area_on_release)
				)
			)
		elif self.mode == "select rectangular area":
			self.eventConnectionIds.extend(
				(
					self.holder.figure.canvas.mpl_connect("button_press_event", self._select_rectangular_area_on_click),
					self.holder.figure.canvas.mpl_connect("button_release_event", self._select_rectangular_area_on_release)
				)
			)

	def _reset_event_connections(self) -> None:
		"""
		Disconnect and delete all event connections.
		"""
		for connection in self.eventConnectionIds:
			self.holder.figure.canvas.mpl_disconnect(connection)

		self.eventConnectionIds = []

	def _update_toolbar_buttons(self) -> None:
		"""
		Update the state of the toolbar buttons.
		"""
		if self.mode == "":
			self._set_toolbar_button_state()
		# Line plot toolbar modes
		elif self.mode == "zoom in":
			self._set_toolbar_button_state(
				self._buttons["zoom_in"]
			)
		elif self.mode == "pick single line":
			self._set_toolbar_button_state(
				self._buttons["pick_single"]
			)
		# Heatmap toolbar modes
		elif self.mode == "select area":
			self._set_toolbar_button_state(
				self._buttons["select_area"]
			)
		elif self.mode == "select rect":
			self._set_toolbar_button_state(
				self._buttons["select_rectangle"]
			)

	def _set_toolbar_button_state(
		self,
		activeButton: Optional[tk.Button] = None
	) -> None:
		"""
		Mark buttons as either active or inactive.

		Parameters
		----------
		activeButton : tk.Button 
			Potential new active button.
		"""
		for button in self._buttons.values():
			button.configure(bg=self.inactiveButtonColor)

		if activeButton:
			activeButton.configure(bg=self.activeButtonColor)