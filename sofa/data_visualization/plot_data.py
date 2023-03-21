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

import numpy as np
import matplotlib as mpl

import data_processing.named_tuples as nt

def create_raw_line(
	identifier: str, 
	dataRaw: nt.ForceDistanceCurve
) -> mpl.lines.Line2D:
	"""

	
	Parameters
	----------
	identifier : str
	dataRaw : nt.ForceDistanceCurve

	Returns
	-------
	rawLine : mpl.lines.Line2D

	"""
	return mpl.lines.Line2D(
		dataRaw.piezo, 
		dataRaw.deflection, 
		c="darkred", 
		label=identifier + "_raw",
		linewidth=0.5, 
		picker=True, 
		pickradius=1.0, 
		zorder=5
	)

def create_corrected_line(
	identifier: str, 
	dataCorrected: nt.ForceDistanceCurve
) -> mpl.lines.Line2D:
	"""

	
	Parameters
	----------
	identifier : str
	dataRaw : nt.ForceDistanceCurve

	Returns
	-------
	rawLine : mpl.lines.Line2D
	
	"""
	return mpl.lines.Line2D(
		dataCorrected.piezo, 
		dataCorrected.deflection, 
		c="red", 
		label=identifier + "_corrected",
		linewidth=0.5, 
		picker=True, 
		pickradius=1.0, 
		zorder=5
	)

def create_average_line(
	averageData: np.ndarray
) -> mpl.lines.Line2D:
	"""
	"""
	return mpl.lines.Line2D(
		averageData.piezo, 
		averageData.deflection, 
		c="black", 
		label="average_data",
		zorder=6
	)

def create_average_errorbar(
	averageData: np.ndarray,
	standardDeviation: np.ndarray
) -> mpl.container.ErrorbarContainer:
	"""
	"""
	return mpl.container.ErrorbarContainer(
		averageData.piezo, 
		averageData.deflection, 
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
		New or existing axes of the given holder.
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
	

	Parameters
	----------
	holder : mpl.backends.backend_tkagg.FigureCanvasTkAgg

	lines : list

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
	data: np.ndarray,
	markingLines: List[mpl.lines.Line2D]
) -> None:
	"""


	Parameters
	----------
	holder : mpl.backends.backend_tkagg.FigureCanvasTkAgg

	data : np.ndarray

	markingLines : list

	"""
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
	holder: mpl.backends.backend_tkagg.FigureCanvasTkAgg,
	data: np.ndarray,
	activeData: np.ndarray,
	numberOfBins: int,
	zoom: bool
) -> None:
	"""

	
	Parameters
	----------
	holder : mpl.backends.backend_tkagg.FigureCanvasTkAgg

	data : np.ndarray

	activeData : np.ndarray

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

def update_line(
	line: mpl.lines.Line2D, 
	color: str, 
	zorder: int
) -> None:
	"""


	Parameters
	----------
	line : mpl.lines.Line2D
	
	color : str

	zorder : int

	"""
	line.set_color(color)
	line.zorder = zorder

def add_average_curve_to_line_plot() -> None: 
	"""
	"""
	pass 

def add_errorbar_to_line_plot() -> None: 
	"""
	"""
	pass 

def remove_average_curve_from_line_plot() -> None:
	"""
	"""
	pass

def remove_errorbar_from_line_plot() -> None:
	"""
	"""
	pass

def update_line_plot(
	holder: mpl.backends.backend_tkagg.FigureCanvasTkAgg,
	forceDistanceCurves: List,
	showInactive: bool
) -> None:
	"""

	Parameters
	----------
	holder : mpl.backends.backend_tkagg.FigureCanvasTkAgg,
	
	forceDistanceCurves : list
	
	showInactive : bool
	
	"""
	for forceDistanceCurve in forceDistanceCurves:
		if not forceDistanceCurve.isActive and showInactive:
			self.update_line(
				forceDistanceCurve.lineRepresentationCorrectedData, 
				"gray", 
				-1
			)
		elif not forceDistanceCurve.isActive and not showInactive:
			self.update_line(
				forceDistanceCurve.lineRepresentationCorrectedData, 
				"white", 
				-1
			)
		else:
			self.update_line(
				forceDistanceCurve.lineRepresentationCorrectedData, 
				"red", 
				1
			)
	
	holder.draw()