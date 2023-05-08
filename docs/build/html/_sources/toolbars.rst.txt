.. _toolbar funcitionalities:

========
Toolbars
========

To deselect outliers or define a region of interest in on of the channels, SOFA offers two custom Matplotlib Toolbars. For more information about the implementation of these see the :ref:`codebase <toolbar implementation>` section. 

.. _lineplot toolbar:

Lineplot Toolbar
================

- **Home** - Reset the inactive data points and the zoom.
- **Zoom In** - Toggle the zoom mode, to zoom to a rectangle drawn by the mouse.
- **Zoom Out** - Undo the last zoom.
- **Reset Zoom** - Reset the zoom.
- **Select Sinlge Curve** - Toggle the curve selection mode, to disable or activate single curves by click.
- **Select Visible Curves** - Disable all curves that have a datapoint within the current view.
- **Display Average Curve** - Calculate and display the average of the currently active curves.
- **Toggle Errorbar** - Display or hide the standard deviation of the average curve.
- **Toggle Inactive Curves** - Show or hide the currently inactive curves.

.. _heatmap toolbar:

Heatmap Toolbar
===============

- **Home** - Reset the inactive data points, the orientation of the channel and any selected area.
- **Select Area** - Toggle the selection mode to select arbitrary area's with the mouse.  
- **Select Rectangle** - Toggle the selection mode to select rectangular area's with the mouse.
- **Include Area** - Disable all data points that are not within the selected area.
- **Exclude Area** - Disable all data points that are in the selected area.
- **Flip Heatmap Horizontally** - Flip the channel horizontally without changing the axes.
- **Flip Heatmap Verticaly** - Flip the channel vertically without changing the axes.
- **Rotate Heatmap** - Rotate the channel counterclockwise by 90 degrees without changing the axes.
