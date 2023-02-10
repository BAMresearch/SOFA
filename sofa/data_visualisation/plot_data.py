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

import numpy as np
import matplotlib as mpl

def create_raw_line(
	identifier: str, 
	xData: np.ndarray,
	yData: np.ndarray
) -> mpl.lines.Line2D:
	""""""
	return mpl.lines.Line2D(
		xData, 
		yData, 
		c="darkred", 
		label=identifier + "_raw",
		linewidth=0.5, 
		picker=True, 
		pickradius=1.0, 
		zorder=5
	)

def create_corrected_line(
	identifier: str, 
	xData: np.ndarray,
	yData: np.ndarray
) -> mpl.lines.Line2D:
	""""""
	return mpl.lines.Line2D(
		xData, 
		yData, 
		c="red", 
		label=identifier + "_corrected",
		linewidth=0.5, 
		picker=True, 
		pickradius=1.0, 
		zorder=5
	)

def get_axes(holder) -> mpl.axes:
	"""Create or get axis of a given holder.

	Parameters:
		holder(canvasTkAgg): Holder which requires an axes.

	Returns:
		axes(mpl.axes): New or existing axes of the given holder.
	"""
	try:
		return holder.figure.get_axes()[0]
	except IndexError:
		return holder.figure.add_subplot(111)

def plot_line_plot(
	holder,
	lines: List[mpl.lines.Line2D]
) -> None: 
	""""""
	ax = get_axes(holder)
	ax.cla()

	ax.ticklabel_format(axis="both", style="sci", scilimits=(0,0))
	# Simplify mouse hover by removing currenet x and y coordinates.
	ax.format_coord = lambda x, y: ""

	# Add lines to axes.
	for line in lines:
		ax.add_line(line)

	# Set view limits.
	ax.autoscale_view()

	holder.draw()

def plot_heatmap(
	holder, 
	data: np.ndarray,
	markingLines: List[mpl.lines.Line2D]
) -> None:
	""""""
	m, n = np.shape(data)

	ax = get_axes(holder)
	ax.cla()
	ax.imshow(data, cmap="gray", extent=[0, n, m, 0])
	# Simplify mouse hover by removing currenet x and y coordinates.
	ax.format_coord = lambda x, y: ""

	# Plot potentional marking lines.
	for line in markingLines:
		ax.add_line(line)

	holder.draw()

def plot_histogram(
	holder,
	data: np.ndarray,
	activeData: np.ndarray,
	numberOfBins: int,
	zoom: bool
) -> None:
	""""""
	ax = get_axes(holder)

	ax.cla()
	ax.ticklabel_format(axis="y", style="sci", scilimits=(0,0))

	_, binValues, _ =ax.hist(
		data, 
		bins=numberOfBins, 
		range=(np.min(data), np.max(data)),
		alpha=1, 
		orientation="horizontal", 
		color="blue"
	)

	ax.hist(
		activeData, 
		bins=numberOfBins, 
		range=(np.min(data), np.max(data)),
		alpha=1, 
		orientation="horizontal", 
		color="red"
	)

	if zoom:
		ax.set_ylim(
			binValues[np.where(binValues <= np.min(activeData))[0][-1]],
			binValues[np.where(binValues >= np.max(activeData))[0][0]]
		)
		ax.set_xlim(auto=True)

	holder.draw()

def update_line(
	line: mpl.lines.Line2D, 
	color: str, 
	zorder: int
) -> None:
	""""""
	line.set_color(color)
	line.zorder = zorder

def add_average_curve_to_line_plot() -> None: 
	""""""
	pass 

def remove_average_curve_from_line_plot() -> None:
	""""""
	pass

def update_line_plot(
	holder,
	lines: List[mpl.lines.Line2D],
	inactiveForceDistanceCurves: List[int],
	showInactive: bool
) -> None:
	""""""
	for index, line in enumerate(lines):
		if index in inactiveForceDistanceCurves and showInactive:
			self.update_line(line, "gray", -1)
		elif index in inactiveForceDistanceCurves and not showInactive:
			self.update_line(line, "white", -1)
		else:
			self.update_line(line, "red", 1)
	
	holder.draw()