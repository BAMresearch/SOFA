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
from typing import List, Optional

#import matplotlib as mpl
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backend_bases import NavigationToolbar2
import tkinter as tk
import tkinter.font

class SofaToolbar(NavigationToolbar2Tk):
	def __init__(self, canvas_, parent_, toolItems):
		"""
		"""
		self.holder = canvas_
		self.mode: str = ""

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

		if self.mode == "select area":
			self.eventConnections.extend(
				(
					self.holder.figure.canvas.mpl_connect("button_press_event", self._select_area_on_click),
					self.holder.figure.canvas.mpl_connect("button_release_event", self._select_area_on_release)
				)
			)
		elif self.mode == "select rect":
			self.eventConnections.extend(
				(
					self.holder.figure.canvas.mpl_connect("button_press_event", self._select_rect_on_click),
					self.holder.figure.canvas.mpl_connect("button_release_event", self._select_rect_on_release)
				)
			)

	def _update_event_connections(self) -> None:
		"""
		Update event connections in dependace of the current mode.
		"""
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

	def _reset_event_connections(self) -> None:
		"""
		Disconnect and delete all event connections.
		"""
		for connection in self.eventConnections:
			self.holder.figure.canvas.mpl_disconnect(connection)

		self.eventConnections = []

	def _update_toolbar_buttons(self) -> None:
		"""
		Update the state of the toolbar buttons.
		"""
		if self.mode == "":
			inactiveButtons = [
				self._buttons["select_area"],
				self._buttons["select_rectangle"]
			]
			self._set_toolbar_button_state(inactiveButtons)
		elif self.mode == "select area":
			inactiveButtons = [self._buttons["select_rectangle"]]
			self._set_toolbar_button_state(
				inactiveButtons, self._buttons["select_area"]
			)
		elif self.mode == "select rect":
			inactiveButtons = [self._buttons["select_area"]]
			self._set_toolbar_button_state(
				inactiveButtons, self._buttons["select_rectangle"]
			)

	def _update_toolbar_buttons(self) -> None:
		"""
		Update the state of the toolbar buttons.
		"""
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

	@staticmethod
	def _set_toolbar_button_state(
		inactiveButtons: List[tk.Button], 
		activeButton: Optional[tk.Button] = None
	) -> None:
		"""
		Mark buttons as either active or inactive.

		Parameters
		----------
		inactiveButtons : list[tk.Button]
			List with the new inactive buttons. 
		activeButton : tk.Button 
			Potential new active button.
		"""
		for button in inactiveButtons:
			button.configure(bg=self.inactiveButtonColor)

		if activeButton:
			activeButton.configure(bg=self.activeButtonColor)