SOFA Workflow
=============

SOFA GUI
--------

The GUI is divided in different sections, as indicated by the orange dashed rectangles in Figure 1. 
Add text

.. _selection process:

Selection Process
-----------------

After importing FSD to SOFA, subgroups of Force Curves can be created. This is done to get averaged Force Curves with high signal-to-noise ratio for comparison and analysis. Subgroups of Force Curves are created by selecting and rejecting single curves due to their spatial position in a parameter map (Parameter maps), due to an untypical shape (Outliers) and value ranges in histograms of channels (Histogram). These selection steps can be combined in any particular order, but we recommend to follow the order, in which these steps are presented here.

.. note::
	
	By *update plots* any made selection in either plot is adopted by the other plots. To keep all plots synchronized automatically *Interactive Elements* must be activated by ticking *Heatmap* (for the parameter maps), *Lineplot* (for the center plot) and/or *Histogram*. Be aware that this can slow down the responds time significantly.

Excluded Curves appear gray instead of red in the center plot. The histogram of the ROI is plotted in red and in front of the histogram of the whole channel map, which is plotted in blue. Any selection step can reselect curves, which were rejected before.

.. _parameter maps:

Parameter maps
~~~~~~~~~~~~~~

Parameter maps corresponding to Channels are automatically created when FSD is imported to SOFA. Maps can be viewed on the middle bottom section of the SOFA GUI, together with any raw parameter map, which was created during the experiment.

In these maps the topography and spatial distribution of parameters can be used as a filter criterion for subgroups. In order to define a ROI SOFA provides a custom :ref:`heatmap toolbar`.

By drawing a rectangle mask and using the *ROI inside mask button*, the following selection was done via parameter map.

In case *Interactive Elements* are not ticked, all plots are synchronizing by *update plots*. Deselected data appears grey in curve plot and blue in the hoistogram.

.. _outliers:

Outliers
~~~~~~~~

One of the advantages of SOFA is that all force curves are plotted in one graph and therefore can be compared directly. In this plot it also becomes evident that in some cases either the experimental curve is not ideal and/or SOFA’s algorithm did not succeed to correct the curve as expected. Those curves are clearly visible as outliers. If these outliers might change significantly and unnecessarily the outcome of average curves and their standard deviation, as explained in detail in :ref:`averaged subgroups of force curves`. To deselect such outliers, SOFA has a custom :ref:`lineplot toolbar`.

Force Curves are expected to have a certain typical shape in order to interpret the contact between probe and sample according to theories and physical models. In case a curve shows any deviation from F = 0 for Z < 0 beyond certain noise (areas are shown by horizontal yellow markings), the point of contact can not be identified conclusively. These curves need to be discarded. Also, in case curves show extensive non-monotonous behavior (zigzag) for Z > 0 (area also shown yellow marking), the contact between probe and sample may have been unstable and therefore these curves must be discarded as well. By using update plots, Maps on the left and histogram on the right adopt the selection.

In case *Interactive Elements* are not ticked, all plots can be synchronizing by *update plots*.

.. _histogram:

Histogram
~~~~~~~~~

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