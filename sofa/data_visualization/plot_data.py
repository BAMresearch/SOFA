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
		label=identifier,
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
		label=identifier,
		linewidth=0.5, 
		picker=True, 
		pickradius=1.0, 
		zorder=5
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
		Number of data bins into which the data is divided.
	zoom : bool
		If true adjust the view limits to the current 
		minimum and maximum values.

	Returns
	-------
	binValues : list
		Values of the bins from the general channel data.
	"""
	ax = get_axes(holder)

	ax.cla()
	ax.ticklabel_format(axis="y", style="sci", scilimits=(0,0))

	_, binValues, _ = ax.hist(
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

	return binValues

def plot_average(
	holder: mpl.backends.backend_tkagg.FigureCanvasTkAgg,
	averageData: nt.AverageForceDistanceCurve
) -> List[mpl.lines.Line2D]:
	"""
	Plot the average force distance curve consisting of the
	non contact and contact part.

	Parameters
	----------
	holder : mpl.backends.backend_tkagg.FigureCanvasTkAgg
		Interface between the matplotlib figure and the 
		main window in which the plot is located.
	averageData : nt.AverageForceDistanceCurve
		Contains the piezo(x) and deflection (y) values
		of the average curve and the standard deviation.

	Returns
	-------
	averageLineNonContact : mpl.lines.Line2D
		Line representation of the non contact part
		of the average force distance curve.
	averageLineContact : mpl.lines.Line2D
		Line representation of the contact part
		of the average force distance curve.
	"""
	axes = get_axes(holder)
	averageLineNonContact = plot_average_line(
		axes,
		averageData.piezoNonContact,
		averageData.deflectionNonContact
	)
	# Swap piezo and deflection values to plot the part correctly.
	averageLineContact = plot_average_line(
		axes,
		averageData.deflectionContact,
		averageData.piezoContact
	)
	holder.draw()

	return averageLineNonContact, averageLineContact

def plot_average_line(
	axes: mpl.axes,
	piezoValues: np.ndarray,
	deflectionValues: np.ndarray
) -> mpl.lines.Line2D: 
	"""
	Plot a part of the average force distance
	curve.

	Parameters
	----------
	axes : mpl.axes
		Contains all elements of the line plot figure.
	piezoValues : np.ndarray
		Piezo (x) values of the part of the 
		force distance curve.
	deflectionValues : np.ndarray
		Deflection (y) values of the part of the 
		force distance curve.

	Returns
	-------
	averageLine : mpl.lines.Line2D
		Line representation of one part of
		the average force distance curve.
	"""
	return axes.plot(
		piezoValues,
		deflectionValues,
		c="black", 
		label="average_data",
		zorder=6
	)[0]

def plot_errorbar(
	holder: mpl.backends.backend_tkagg.FigureCanvasTkAgg,
	averageData: nt.AverageForceDistanceCurve
) -> List[mpl.lines.Line2D]:
	"""
	Plot the average force distance curve consisting of the
	non contact and contact part with the standard deviation
	as an errorbar.

	Parameters
	----------
	holder : mpl.backends.backend_tkagg.FigureCanvasTkAgg
		Interface between the matplotlib figure and the 
		main window in which the plot is located.
	averageData : nt.AverageForceDistanceCurve
		Contains the piezo(x) and deflection (y) values
		of the average curve and the standard deviation.

	Returns
	-------
	averageErrorbarNonContact : mpl.container.ErrorbarContainer
		Errorbar representation of the non contact part
		of the average force distance curve.
	averageErrorbarContact : mpl.container.ErrorbarContainer
		Errorbar representation of the contact part
		of the average force distance curve.
	"""
	axes = get_axes(holder)
	averageErrorbarNonContact = plot_average_errorbar_non_contact(
		axes,
		averageData.piezoNonContact,
		averageData.deflectionNonContact,
		averageData.standardDeviationNonContact
	)
	averageErrorbarContact = plot_average_errorbar_contact(
		axes,
		averageData.deflectionContact,
		averageData.piezoContact,
		averageData.standardDeviationContact
	)
	holder.draw()

	return averageErrorbarNonContact, averageErrorbarContact

def plot_average_errorbar_non_contact(
	axes: mpl.axes,
	piezoValues: np.ndarray,
	deflectionValues: np.ndarray,
	standardDeviation: np.ndarray
) -> mpl.container.ErrorbarContainer: 
	"""
	Plot the non contact part of the average force
	distance curve as an errorbar with the standard
	devitation of the deflection values as y error.

	Parameters
	----------
	axes : mpl.axes
		Contains all elements of the line plot figure.
	piezoValues : np.ndarray
		Piezo (x) values of the non contact part of the 
		force distance curve.
	deflectionValues : np.ndarray
		Deflection (y) values of the non contact part 
		of the force distance curve.
	standardDeviation : np.ndarray
		Standard deviation of the deflection values 
		of the non contact part of the average force
		distance curve.

	Returns
	-------
	averageErrorbarNonContact : mpl.container.ErrorbarContainer
		Errorbar representation of the non contact 
		part of the average force distance curve.
	"""
	return axes.errorbar(
		piezoValues,
		deflectionValues,
		yerr=standardDeviation,
		c="black",
		ecolor="black",
		label="average_data_with_std",
		zorder=6
	)

def plot_average_errorbar_contact(
	axes: mpl.axes,
	piezoValues: np.ndarray,
	deflectionValues: np.ndarray,
	standardDeviation: np.ndarray
) -> mpl.container.ErrorbarContainer: 
	"""
	Plot the contact part of the average force
	distance curve as an errorbar with the standard
	devitation of the piezo values as x error.

	Parameters
	----------
	axes : mpl.axes
		Contains all elements of the line plot figure.
	piezoValues : np.ndarray
		Piezo (x) values of the contact part of the 
		force distance curve.
	deflectionValues : np.ndarray
		Deflection (y) values of the contact part of the 
		force distance curve.
	standardDeviation : np.ndarray
		Standard deviation of the piezo values 
		of the contact part of the average force
		distance curve.

	Returns
	-------
	averageErrorbarContact : mpl.container.ErrorbarContainer
		Errorbar representation of the contact 
		part of the average force distance curve.
	"""
	return axes.errorbar(
		piezoValues,
		deflectionValues,
		xerr=standardDeviation,
		c="black",
		ecolor="black",
		label="average_data_with_std",
		zorder=6
	)

def update_line_plot(
	holder: mpl.backends.backend_tkagg.FigureCanvasTkAgg,
	forceDistanceCurves: List[mpl.lines.Line2D],
	inactiveDataPoints: List[int],
	showInactive: bool
) -> None:
	"""
	Update the state of every force distance curve
	displayed in the line plot.

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
			deactivate_line(
				forceDistanceCurve, 
			)
		elif index in inactiveDataPoints and not showInactive:
			hide_line(
				forceDistanceCurve, 
			)
		else:
			activate_line(
				forceDistanceCurve, 
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