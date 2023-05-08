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
from typing import List
import functools

import numpy as np
import matplotlib as mpl

import data_processing.named_tuples as nt

def decorator_update_plot(function):
	"""Get axes and redraw the holder of a plot."""
	@functools.wraps(function)
	def wrapper_update_plot(*args, **kwargs):
		holder = args[0]
		axes = get_axes(holder)
		function(axes, *args, **kwargs)
		holder.draw()

	return wrapper_update_plot

def create_raw_line(
	identifier: str, 
	rawMeasurementCurve: nt.ForceDistanceCurve
) -> mpl.lines.Line2D:
	"""
	Construct a displayable matplotlib line from a raw
	measurement curve.
	
	Parameters
	----------
	identifier : str
		Name matching the corresponding force distance curve.
	rawMeasurementCurve : nt.ForceDistanceCurve
		Raw piezo (x) and deflection (y) values of the 
		corresponding force distance curve.

	Returns
	-------
	rawLine : mpl.lines.Line2D
		Line representation of a raw force 
		distance curve.
	"""
	return mpl.lines.Line2D(
		rawMeasurementCurve.piezo, 
		rawMeasurementCurve.deflection, 
		c="darkred", 
		label=identifier + "_raw",
		linewidth=0.5, 
		picker=True, 
		pickradius=1.0, 
		zorder=5
	)

def create_corrected_line(
	identifier: str, 
	correctedMeasurementCurve: nt.ForceDistanceCurve
) -> mpl.lines.Line2D:
	"""
	Construct a displayable matplotlib line from a
	corrected measurement curve.
	
	Parameters
	----------
	identifier : str
		Name matching the corresponding force distance curve.
	correctedMeasurementCurve : nt.ForceDistanceCurve
		Corrected piezo (x) and deflection (y) values of the 
		corresponding force distance curve.

	Returns
	-------
	rawLine : mpl.lines.Line2D
		Line representation of a corrected 
		force distance curve.
	"""
	return mpl.lines.Line2D(
		correctedMeasurementCurve.piezo, 
		correctedMeasurementCurve.deflection, 
		c="red", 
		label=identifier + "_corrected",
		linewidth=0.5, 
		picker=True, 
		pickradius=1.0, 
		zorder=5
	)

def create_average_line(
	averageCurve: np.ndarray
) -> mpl.lines.Line2D:
	"""
	Construct a displayable matplotlib line for
	the calculated average values.

	Parameters
	----------
	averageCurve : nt.ForceDistanceCurve
		Average Piezo (x) and deflection (y) values
		of all active force distance curves.

	Returns
	-------
	averageLine : mpl.lines.Line2D
		Line representation of the average of 
		the active force distance curves.
	"""
	return mpl.lines.Line2D(
		averageCurve.piezo, 
		averageCurve.deflection, 
		c="black", 
		label="average_data",
		zorder=6
	)

def create_average_errorbar(
	averageCurve: np.ndarray,
	standardDeviation: np.ndarray
) -> mpl.container.ErrorbarContainer:
	"""
	Construct a displayable matplotlib object for
	the calculated average values and the 
	corresponding standard deviation.

	Parameters
	----------
	averageCurve : nt.ForceDistanceCurve
		Average Piezo (x) and deflection (y) values
		of all active force distance curves.
	standardDeviation : np.ndarray
		Standard deviation of the calculated average
		values.

	Returns
	-------
	averageErrorbar : mpl.container.ErrorbarContainer
		Line representation of the average of 
		the active force distance curves with
		the standard deviation as errorbars.
	"""
	return mpl.container.ErrorbarContainer(
		averageCurve.piezo, 
		averageCurve.deflection, 
		yerr=standardDeviation,
		c="black",
		ecolor="black",
		label="average_data_with_std",
		zorder=6
	)

def get_axes(
	holder: mpl.backends.backend_tkagg.FigureCanvasTkAgg
) -> mpl.axes:
	"""
	Create or get axis of a given holder.

	Parameters
	----------
	holder : mpl.backends.backend_tkagg.FigureCanvasTkAgg
		Holder which requires an axes.

	Returns
	-------
	axes : mpl.axes
		New or existing axes of the figure of
		the given holder.
	"""
	try:
		return holder.figure.get_axes()[0]
	except IndexError:
		return holder.figure.add_subplot(111)

def plot_line_plot(
	holder: mpl.backends.backend_tkagg.FigureCanvasTkAgg,
	lines: List[mpl.lines.Line2D]
) -> None: 
	"""
	Plot every force distance curve of a force volume 
	as a line plot.

	Parameters
	----------
	holder : mpl.backends.backend_tkagg.FigureCanvasTkAgg
		Interface between the matplotlib figure and the 
		main window in which the plot is located.
	lines : list[mpl.lines.Line2D]
		Line representations of all force distance curves
		in a force volume.
	"""
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
	holder: mpl.backends.backend_tkagg.FigureCanvasTkAgg, 
	activeData: np.ndarray,
	linesSelectedArea: List[mpl.lines.Line2D]
) -> None:
	"""
	Plot the active data of a channel as a grayscale heatmap.

	Parameters
	----------
	holder : mpl.backends.backend_tkagg.FigureCanvasTkAgg
		Interface between the matplotlib figure and the 
		main window in which the plot is located.
	activeData : np.ndarray
		Two dimensional data of the active data points
		of the channel.
	linesSelectedArea : list[mpl.lines.Line2D]
		Lines enclosing the selected area. 
	"""
	m, n = np.shape(activeData)

	ax = get_axes(holder)
	ax.cla()
	ax.imshow(activeData, cmap="gray", extent=[0, n, m, 0])
	# Simplify mouse hover by removing currenet x and y coordinates.
	ax.format_coord = lambda x, y: ""

	# Plot potentional marking lines.
	for line in linesSelectedArea:
		ax.add_line(line)

	holder.draw()

def plot_histogram(
	holder: mpl.backends.backend_tkagg.FigureCanvasTkAgg,
	data: np.ndarray,
	activeData: np.ndarray,
	numberOfBins: int,
	zoom: bool
) -> None:
	"""
	Plot the data versus the data of the active data 
	points of a channel as a histogram.
	
	Parameters
	----------
	holder : mpl.backends.backend_tkagg.FigureCanvasTkAgg
		Interface between the matplotlib figure and the 
		main window in which the plot is located.
	data : np.ndarray
		One dimensional data of the channel.
	activeData : np.ndarray
		One dimensional data of the active data points
		of the channel.
	numberOfBins : int
		
	zoom : bool
		
	"""
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

def add_average_to_line_plot(
	holder: mpl.backends.backend_tkagg.FigureCanvasTkAgg,
	averageLine: mpl.lines.Line2D
) -> None: 
	"""
	"""
	ax = get_axes(holder)

	ax.add_line(averageLine)

	holder.draw() 

def add_errorbar_to_line_plot(
	holder: mpl.backends.backend_tkagg.FigureCanvasTkAgg,
	errorbar: mpl.container.ErrorbarContainer
) -> None: 
	"""
	"""
	ax = get_axes(holder)

	ax.add_container(errorbar)

	holder.draw()

def remove_average_curve_from_line_plot(
	averageLine: mpl.lines.Line2D
) -> None:
	"""
	"""
	averageLine.remove()

def remove_errorbar_from_line_plot(
	errorbar: mpl.container.ErrorbarContainer
) -> None:
	"""
	"""
	errorbar.remove()

def update_line_plot(
	holder: mpl.backends.backend_tkagg.FigureCanvasTkAgg,
	forceDistanceCurves: List[mpl.lines.Line2D],
	inactiveDataPoints: List[int],
	showInactive: bool
) -> None:
	"""
	

	Parameters
	----------
	holder : mpl.backends.backend_tkagg.FigureCanvasTkAgg
		Interface between the matplotlib figure and the 
		main window in which the plot is located.
	forceDistanceCurves : list[mpl.lines.Line2D]
		Line representations of all force distance curves
		in a force volume.
	inactiveDataPoints : list[int]
		Indicis of the inactive data points/force distance
		curves.
	showInactive : bool
		Specifies whether inactice force distance curves
		should be displayed as grey or hidden.
	"""
	for index, forceDistanceCurve in enumerate(forceDistanceCurves):
		if index in inactiveDataPoints and showInactive:
			self.deactivate_line(
				forceDistanceCurve.lineRepresentationCorrectedData, 
			)
		elif index in inactiveDataPoints and not showInactive:
			self.hide_line(
				forceDistanceCurve.lineRepresentationCorrectedData, 
			)
		else:
			self.activate_line(
				forceDistanceCurve.lineRepresentationCorrectedData, 
			)
	
	holder.draw()

def deactivate_line(line: mpl.lines.Line2D) -> None: 
	"""
	Deactivate the line representation of a inactive
	force distance curve by setting the line color to 
	gray and adjusting the z order so it appears
	behind active force distance curves.

	Parameters
	----------
	line : mpl.lines.Line2D
		Line representation of a force distance curve.
	"""
	line.set_color("gray")
	line.zorder = -1

def hide_line(line: mpl.lines.Line2D) -> None: 
	"""
	Hide the line representation of a inactive
	force distance curve by setting the line color to 
	white and adjusting the z order so it appears
	behind active force distance curves.

	Parameters
	----------
	line : mpl.lines.Line2D
		Line representation of a force distance curve.
	"""
	line.set_color("white")
	line.zorder = -1

def activate_line(line: mpl.lines.Line2D) -> None: 
	"""
	Activate the line representation of an active
	force distance curve by setting the line color to 
	red and adjusting the z order so it appears
	before inactive force distance curves.

	Parameters
	----------
	line : mpl.lines.Line2D
		Line representation of a force distance curve.
	"""
	line.set_color("red")
	line.zorder = 1