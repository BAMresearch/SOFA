==========
Using SOFA
==========

Include image of the SOFA GUI after importing some test data

.. _import data:

Import Data
===========

To start working with SOFA, measurement data needs to be imported. When SOFA is started a subwindow to import data will automatically appear. To import new data, the :guilabel:`Import Data` button opens this subwindow as well. In this window the data type of the measurement data and the location of the different data files can be specified. If the :guilabel:`Show poor curves` checkbox is selected, SOFA will also plot every lines, which could not be corrected. In addition to the measurement data an optional image file, or extra channels can be imported as well. 

If SOFA can not read any of the selected files the import process is cancelled and a notification appears. Please see :ref:`import formats <import formats>` for further informations about the currently supported data types. SOFA will also check if the selected files match in size. If this is not the case, the import process is also aborted.

During the import process SOFA will import the data, correct the measurement curves (add link), calculate the different channels (add link) and plot the data in a line plot, a heatmap and a histogram. An indeterminate progress bar will run during the import process. After the data was sucessfully imported the import window will close it self and a notification will appear. The name, size and location of the imported data will be displayed in the Imported Data frame of the main window.


.. _selection process:

Selection Process
=================

After importing force spectroscopy data to SOFA, subgroups of Force Curves can be created. This is done to get averaged Force Curves with high signal-to-noise ratio for comparison and analysis. Subgroups of Force Curves are created by selecting and rejecting single curves due to their spatial position in a :ref:`parameter map <parameter maps>`, due to an untypical :ref:`shape <outliers>` and value ranges in :ref:`histograms <histogram>` of channel. These selection steps can be combined in any particular order, but we recommend to follow the order, in which these steps are presented here.

The Interactive Plots frame contains a checkbox for the line plot, heatmap and histogram. If they are active, changes in their associated plot will automatically appear in every other plot as well. Automatically updating large measurement data with every change can slow down the responds time significantly. In this case it is recommended to use the :guilabel:`Update Plots` button instead. This will snychronize the changes in every plot.

.. _parameter maps:

Parameter maps
--------------

Parameter maps corresponding to Channels are automatically created when force spectroscopy data is imported to SOFA. These maps are displayed in the Heatmap frame of the SOFA GUI. Any additionl imported channel will be displayed here as well. The different channels can be selected by using the dropdown menu.

In these maps the topography and spatial distribution of parameters can be used as a filter criterion for subgroups. In order to define a region of interest SOFA provides a custom :ref:`heatmap toolbar`.

By drawing a rectangle mask and using the *ROI inside mask button*, the following selection was done via parameter map.

Deselected data appears grey in curve plot and blue in the hoistogram.

.. _outliers:

Outliers
--------

One of the advantages of SOFA is that all force curves are plotted in one graph and therefore can be compared directly. In this plot it also becomes evident that in some cases either the experimental curve is not ideal and/or SOFA’s algorithm did not succeed to correct the curve as expected. Those curves are clearly visible as outliers. If these outliers might change significantly and unnecessarily the outcome of average curves and their standard deviation, as explained in detail in :ref:`averaged subgroups of force curves`. To deselect such outliers, SOFA has a custom :ref:`lineplot toolbar`.

Force Curves are expected to have a certain typical shape in order to interpret the contact between probe and sample according to theories and physical models. In case a curve shows any deviation from F = 0 for Z < 0 beyond certain noise (areas are shown by horizontal yellow markings), the point of contact can not be identified conclusively. These curves need to be discarded. Also, in case curves show extensive non-monotonous behavior (zigzag) for Z > 0 (area also shown yellow marking), the contact between probe and sample may have been unstable and therefore these curves must be discarded as well. By using update plots, Maps on the left and histogram on the right adopt the selection.

In case *Interactive Elements* are not ticked, all plots can be synchronizing by *update plots*.

.. _histogram:

Histogram
---------

Every Channel can be either displayed as a map (containing the spatial information) or as a histogram (containing the statistical information). By choosing the channel of interest in the pull-down menu and confirming by Histogram, the histogram is plotted, giving the numbers of bins (by default 100) and the maximum and minimum value of the chosen channel, with the bin width = (max-min)/100. In order to select a certain value range please use the up and down buttons for the maximum and minimum value.

To avoid a histogram, that is distorted by extreme outliers, one can use a zoom function, which can be activated by ticking *zoom*. Please be aware, that the zoomed range equals the selected range.

In case *Interactive Elements* are not ticked, all plots can be synchronizing by *update plots*.

.. _averaged subgroups of force curves:

Averaged Subgroups of Force Curves
----------------------------------

After selecting a subgroup of curves an average curve can be calculated using the :ref:`lineplot toolbar`. The average curve is then plotted on top of the active Force Curves.

.. note::
	
	The average curve is on purpose divided into two parts. The contact part (Z > 0 & F > 0) is averaged in respect to the force F (y- axis) and the non-contact part of the curve (Z ≤ 0) is averaged in respect to the piezo displacement Z (x-axis).

Error bars representing the standard deviation can be added by using the :ref:`lineplot toolbar`. Please note that due to the density of points, single error bars can only be made out when zooming into the plot.

Please note again the change of direction of the error bars at Z = 0. As pointed out above the average is calculated differently for the non-contact part and the contact part.

.. note::

	Average Curve and its error are always recalculated when the Force Curve plot is updated. Force Curves can be further deselected and reselected, while the average curve is already plotted. But this might slow down the responds time of SOFA.

Export Data
===========

Once a subgroup has been defined and the selected curves have been averaged the analysis cycle of SOFA has been completed. Before selecting another subset of curves or analyzing another measurement the results can be exported.

.. note::

   As of version 1.0 SOFA has no capacities to remember previous selected subsets of Force Curves or previous averaged curves. Results have to be exported to be stored.

The :guilabel:`Export Data` button opens a subwindow to export the data. SOFA will create a new folder to store the data. A name for the folder and the path where the folder will be created, are required for this. Furthermore, the desired export formats can be specified. An indeterminate progress bar will run during the export process. After the data is saved the export winwow will close itself and a notification will appear.  