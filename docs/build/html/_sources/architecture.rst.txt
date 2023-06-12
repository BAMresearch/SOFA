=====================
Software Architecture
=====================

SOFA is a graphical user interface to process experimental force spectroscopy data. As such, it must provide various functionalities, from the GUI itself to the import, processing and display of the measurement data and other. To make it easier to maintain and extend SOFA the architecture is divded into the different functionalities. This results in the following folder structure of SOFA.

.. figure:: images/sofa_folder_structure.svg
	:alt: image of the sofa folder structure

	SOFA folder structure with the different packages and their modules.

SOFA Packages
=============

data_processing
---------------

This package is responsible for everything that has to do with the processing of the force spectroscopy data. This includes the import and correction of the measurement data, the calulation of the different channels and an average force distance curve, modifying the data from the histogram and the export of the data from SOFA. These modules use a **procedural** approach. In addition this package also contains the named_tuples and custom_exceptions modules.

import_data
~~~~~~~~~~~

This is a subpackage responsible for importing the measurement data in different file formats. For every new import format a new module should be added in the :code:`import_formats` folder and integrated in the :code:`import_data` module. The function to import a certain data type get's the selected import options of the import window as a :code:`nt.ImportParameter` and is expected to return a dictionary with at least the required measurement data in form of a :code:`nt.MeasurementData`. This includes the name of the measurement, the size and data of the approach and retract curves of the measurement. An image or additional channel data can optionally be added to the dictionary.

calculate_average
~~~~~~~~~~~~~~~~~

This module contains the functions to calculate an average force distance curve from the currently active force distance curves of a force volume. To be able to calculate the average the measurement points of the active force distance curves need to be aligned. Currently this is done every time the average needs to be calculated. To speed up the processing time, this could probably be done once instead, after the curves have been corrected. 

.. _calculate channel data architecture:

calculate_channel_data
~~~~~~~~~~~~~~~~~~~~~~

This module contains the functions to calculate all the different channels defined in SOFA. If the number of channels will increase in the future it might be better to split this module into two, where one is responsible for channels based on parameters and the other is responsible for channels based on physical values. Each function to calculate a channels get's a list of the :code:`ForceDistanceCurve` objects from a force volume. These contain the corrected piezo (x), corrected deflection (y) values and the data created during the correction process. Function to calculate a channel should return Python list, which can be reshaped into a two dimensional numpy array by the :code:`decorator_reshape_channel_data` decorator.

correct_data
~~~~~~~~~~~~

This module is responsible for correcting a single force distance curve. See the :ref:`correction algorithm <correction algorithm>` section for detialed information about the process.

export_data
~~~~~~~~~~~

This module is responsible for the export of the data from a :code:`ForceVolume`. Functions to export the data get the currently selected force volume and the selected export options from the export window as :code:`nt.ExportParameter`.

mutate_histogram_data
~~~~~~~~~~~~~~~~~~~~~

This module contains the functionalities to modify the data of channel by the histogram. Currently this only includes the restriction of the minimum or maximum borders of the histogram. 

custom_exceptions
~~~~~~~~~~~~~~~~~

This is a small helper module which contains custom exceptions, which are used in the import and correction process of the measurement data. Each type of exception has a general and further specific exceptions. This structure allows to catch a general type of exception with a descriptive name that should make it easier to understand the problem.

named_tuples
~~~~~~~~~~~~

Another small helper module which contains the definition of every :code:`NamedTuple` used by SOFA. Named tuples can make it easier to read the code and this module itself uses type hints to further increase the readability.

data_visualization
------------------

This package is responsible for everything related to the representation of the data. The modules use a **procedural** approach.

plot_data
~~~~~~~~~

This module contains functions to display the force spectroscopy data in a line plot, heatmap or histogram. This module could perhaps be divided into three modules, one responsible for each of the different display options.

force_spectroscopy_data
-----------------------

This package is responsible for caching the imported and processed measurement data. The modules use a **object orientated** approach.

.. figure:: images/class_diagram_force_volume.svg
	:alt: image of a class diagram of the force spectroscopy data classes 

	Class diagram of the force spectroscopy data classes.

force_volume
~~~~~~~~~~~~

The :code:`ForceVolume` class serves as a container for the imported measurment data and the data created by SOFA. The data is organized like in a real experiment. Each :code:`ForceVolume` as a list of n x m :ref:`force distance curves <force distance curve architecture>` and a dictionary with the different :ref:`channels <channel architecture>`. The different methods of the class allow other components of SOFA to access the various data.

.. _force distance curve architecture:

force_distance_curve
~~~~~~~~~~~~~~~~~~~~

The :code:`ForceDistanceCurve` class represents a single force distance curve, with their associated data and methods. This class could be extended to include the retract part of the measurement curves in a further version of SOFA.

.. _channel architecture:

channel
~~~~~~~

The :code:`Channel` class represents any channel defined in :ref:`calculate_channel_data <calculate channel data architecture>` module. Through its methods, the class can manipulate the data and for example, return the active data of the channel.

gui
---

This package contains every window of SOFA. Every module in this package uses an **object orientated** approach.

main_window
~~~~~~~~~~~

This module contains the main window of SOFA, which is divided into different sections/frames. Since the histogram does not have its own toolbar the :code:`MainWindow` also contains widgets to manipulte the data displayed in the histogram.

import_window
~~~~~~~~~~~~~

The :code:`ImportWindow` class is a subwindow that handles the import of measurement data.

export_window
~~~~~~~~~~~~~

The :code:`ExportWindow` class is a subwindow that handles the export of the data of a force volume.

interfaces
----------

This package contains the different interfaces of SOFA, which handle the interaction between the different components. All of them use an **object orientated** approach.

gui_interface
~~~~~~~~~~~~~

The :code:`GUIInterface` class is the interface between the different windows of SOFA, for example the main or import window, the toolbars and the imported measurment data respectively the resulting force volumes. This allows the different components of SOFA to access the same data and everything else they need.

.. _plot interface architecture:

plot_interface
~~~~~~~~~~~~~~

The :code:`PlotInterface` class contains the descriptive data to a force volume used by the different plots. These include for example the :ref:`inactive data points <inactive data points architecture>` or the :code:`selectedArea` used by the :ref:`heatmap toolbar <heatmap toolbar architecture>`. Each force volume has it's own :code:`PlotInterface`. 

toolbars
--------

The toolbars package contains the custom toolbars for the different plots of the measurement data, used to select a subsset of force distance curves. Every toolbar is a separate class, thus this package uses an **object orientated** approach.

sofa_toolbar
~~~~~~~~~~~~

This class contains the shared functionalities of each SOFA toolbar. With Matplotlib version 3.5.1 it is no longer possible to load toolbar icons from a custom location. Therefore, the toolbar has to overwrite a part of the NavigationToolbar2Tk :code:`__init__` function. Additionally it adjusts the background color of the toolbar icons to the background color of the main window. Furthermore the functions to switch between the different modes of the toolbar are defined here. The active mode is displayed next to the toolbar icons and the button of the active mode is highlighted. 

line_plot_toolbar
~~~~~~~~~~~~~~~~~

The :code:`LinePlotToolbar` inherits from the :code:`SofaToolbar` and allows the selection of single or multiple force distance curves. In addition it is possible to zoom in and out of the line plot or reset the made selections.

.. _heatmap toolbar architecture:

heatmap_toolbar
~~~~~~~~~~~~~~~

The :code:`HeatmapToolbar` inherits from the :code:`SofaToolbar`. With the heatmap toolbar a certain section of the heatmap can be selected and the heatmap can be rotated or flipped without changing the axis.

Connected Plots
===============

In SOFA the different plots of the measurement data are connected with each other. Selecting a curve in the line plot or a section in the heatmap will effect the other plots aswell. To make this possible the :ref:`Plot Interface <plot interface architecture>` has an attribute called :code:`inactiveDataPoints`.

.. _inactive data points architecture:

Inactive Data Points
--------------------

The :code:`inactiveDataPoints` is a list which stores the indices of the currently inactive force distance cuves or data points in a channel. The first curve imported from the measurement data corresponds to first force distance curve and so on. Any selection made from one of the different plots only changes the :code:`inactiveDataPoints` and not the corresponding data itself. But when the different plots are updated the only display the currently active data, by removing the :code:`inactiveDataPoints`. The flowchart below shows exemplary how the different components of SOFA interact with each other to first update the inactive data points and then update the representation of the data.

.. figure:: images/flowchart_restrict_histogram.svg
	:alt: image of a flow chart showing the process of restricting the histogram data 

	Flow chart showing the restriction of the histogram.

Heapmap Orientation
~~~~~~~~~~~~~~~~~~~

The heatmap can be flipped or rotated changing the axis aswell. This can cause problems with the :code:`inactiveDataPoints`. After a rotation, for example, the point at poistion (0, 0) of the heatmap no longer corresponds to the first data point. To get around this problem the :ref:`Plot Interface <plot interface architecture>` has an attribute called :code:`heatmapOrientationMatrix` which is a two dimensional NumPy array with the same size as the heatmap that stores the positon of the data points in current orientation. When the heatmap is rotated or flipped the same transformation is performed on the NumPy array. And if new inactive data points are added from the heatmap or some datapoints in the heatmap needs to be disabled the points of the heatmap can be mapped to their actual datapoints with the help of the :code:`heatmapOrientationMatrix` array.