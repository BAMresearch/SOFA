========
Codebase
========

SOFA is written in Python (should require Python 3.6.1 at minimum) and uses the following external modules and libraries:

- **NumPy** - for basic mathematical computations (tested with NumPy version 1.22.1)
- **SciPy** - for some specific mathematical computations (tested with SciPy version 1.8.0)
- **Matplotlib** - to plot the data and create the custom toolbars (tested with Matplotlib version 3.5.1)
- **pandas** - to export the data to the different ouput file formats (tested with pandas version 1.4.1)
- **igor** - to read files in the .ibw (igor binary wave) file format (tested with igor version 0.3)
- **ttkbootstrap** - to give the Tkinter GUI a modern look (tested with ttkbootstrap version 1.5.1)

SOFA Packages
=============

The general aim of SOFA was to write code which is simple to read and easy to extend. The implementation followed the principle of separation of concerns. Therefore SOFA is comprised of multiple distinct packages. On the code level functions are keept short and only take responsibility for one single functionality. To increase the readability of the code, SOFA tries to implement the following PEP's:

- `PEP 8 <https://peps.python.org/pep-0008/>`_ - The Style Guide for Python Code
- `PEP 257 <https://peps.python.org/pep-0257/>`_ - Docstring Conventions
- `PEP 484 <https://peps.python.org/pep-0484/>`_ - Type Hints

The implementation uses a mixture of object oriented and procedural programming, depending on which is more suitable for the different requirements at hand.

.. _gui implementation:

GUI
---

The GUI of SOFA is written in Tkinter and uses the ttkbootstrap theme extension, to give it a modern look. It consists of of three windows, the main window and two subwindows for the data import and export. All of them are written in an object oriented approach.

.. _main window implementation:

Main Window  `source <https://github.com/2Puck/sofa/tree/development>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The main window of SOFA allows the user to import, process and export experimental force spectroscopy data. To improve the clarity of the window it is divided into smaller frames. The different plots are embedded into the GUI using the :code:`FigureCanvasTkAgg` from the Matplotlib tkinter backend. To arrange the different widgets the pack geometry manager is prefered over grid. 

To interact with the different imported force volumes the main window creates a :ref:`GUI Interface <gui interface implementation>` object. This object is passed to the line plot and heatmap :ref:`toolbars <toolbar implementation>` and to the :ref:`import <import window implementation>` and :ref:`export <export window implementation>` window when they are opened. After all widgets have been created the interactive parameters for the different plots, like the variables behind the checkboxes from the Line Plot or Linked Plots frame, are set in the GUI Interface. This way the various data plots can all be connected with each other.

.. _import window implementation:

Import Window
~~~~~~~~~~~~~

The import window is a small subwindow to handle the import of measurement data. Like in the main window the different widgets are arranged in rows using only the pack geometry manager. It contains a indeterminate progressbar to show if the import process is still runing and which process is currently being executed. The decorator :code:`decorator_check_required_folder_path` checks if a required measurement folder is selected before the import process starts.

During the import process the selected measurement files are first imported and combined into one data dictionary with the selected import function of the :ref:`Import Data <import data implementation>` module. Afterwards the data dictionary is passed to the :ref:`GUI Interface <gui interface implementation>`, where a new force volume will be created. Finally the foldername, size and folderpath of the imported measurement data are set in the Active Data frame of the :ref:`Main Window <main window implementation>`.

If an error occurs during the import process the user is informed via a message box and the import process is terminated. If the data could sucessfully be imported the window closes it self and informs the user via a message box.

.. _export window implementation:

Export Window
~~~~~~~~~~~~~

The export window is a small subwindow to handle the export of the imported force volumes. Like in the main window the different widgets are arranged in rows using only the pack geometry manager. It contains a indeterminate progressbar to show if the import process is still runing.
The decorator :code:`decorator_check_required_folder_path` and :code:`decorator_check_required_folder_name` check if the required folder path and folder name for the ouput folder are selected before the export process starts.

In the export process the data of the selected force volume can be exported to the selected :ref:`export formats <export formats>`. The :ref:`Export Data <export data implementation>` module creates an output folder for data with the selected location and name. After this the data of the selected force volume is exported to the different formats.

Window Settings
~~~~~~~~~~~~~~~

This file should contain all of the general window settings, sutch as spacing parameters between widgets or background colors for the different GUI elements, making it easier to adjust the different windows of the GUI. 

.. _toolbar implementation:

Toolbar
-------

The toolbar package contains the line plot and heatmap toolbars to select a certain subgroup of force curves and inspect the data more closely. Since they share some similarities they both inheret from the SOFA Toolbar which in turn is inhereted from the Matplotlib :code:`NavigationToolbar2Tk`. 

SOFA Toolbar
~~~~~~~~~~~~

With Matplotlib version 3.5.1 it is no longer possible to load toolbar icons from a custom location. Therefore, the toolbar has to overwrite a part of the NavigationToolbar2Tk :code:`__init__` function. Additionally it adjusts the background color of the toolbar icons to the background color of the main window. Furthermore the functions to switch between the different modes of the toolbar are defined here. The active mode is displayed next to the toolbar icons and the button of the active mode is highlighted.

Line Plot Toolbar
~~~~~~~~~~~~~~~~~

The line plot toolbar allows the selection of single or multiple force distance curves. In addition it is possible to zoom in and out of the line plot or reset the made selections. Always having to cache the basic view limits felt inefficient. Therefore when zooming into the plot, the old view limits are cached and not the new ones. Making it easier to revert a single step or to reset the zoom as a whole. The selection mode of single force distance curves uses the Matplotlib :code:`pick_event` in combination with the :code:`pickradius` attribute of the :code:`Line2D` objects. While this mode is active mouse clicks which are close enough to a curve will toggle their state. The function to select multiple force distance curves uses the current view limits and tries to disable all curves within the current view. However, the current implementation only disables all curves that actually have a data point within the current view. This neglects all cases where curves only intersect the current view limits. An older version of SOFA calculated whether a curve intersects the boundaries of the current view if it has no data points in the boundaries. However, this increases the computational effort considerably, which is especially problematic for large force volumes with a lot of force distance curves. Therefore, the faster but somewhat less precise solution was chosen in the end.

Heatmap Toolbar
~~~~~~~~~~~~~~~

With the heatmap toolbar a certain section of the heatmap can be selected and disabled and the heatmap can be rotated or flipped without changing the axis. There are two different modes to select an area of the heatmap and both use the :code:`button_press_event` and :code:`button_release_event` of matplotlib to capture the movement of the mouse while the mouse button is pressed. To select a rectangular area, a rectangle is drawn between the start and end points of the mouse movement. Start and end point are defined by clicking and releasing the mouse button. To indicate the selected area, red lines are drawn around the resulting rectangle. The other mode allows to select any area. To do this, a tuple with the x and y indices of every data point of the heatmap over which the mouse moves while the button is pressed are cached. Indicating such a created area by outlining it with red lines is difficult. To achieve this, each point of the selected area is first outlined with red lines. This already results in the the outline of the area, but there are also unwanted red lines within the area. To delete the unwanted marking lines every line which exists exactly twice, is deleted. After an area is selected, either all points in or outside the area can be disabled. When the heatmap is flipped or rotated the selected area and the marking lines indicating it are flipped/rotated as well. Because the axis are not rotated/flipped, problems can occur. After a rotation, for example, the point at poistion (0, 0) of the heatmap no longer corresponds to the first data point. To get around this problem the :ref:`Plot Interface <plot interface implementation>` has an attribute called :code:`heatmapOrientationMatrix` which is a two dimensional NumPy array with the same size as the heatmap that stores the positon of the data points in current orientation. When the heatmap is rotated or flipped the same transformation is performed on the NumPy array. And if new inactive data points are added from the heatmap or some datapoints in the heatmap needs to be disabled the points of the heatmap can be mapped to their actual datapoints with the help of the :code:`heatmapOrientationMatrix` array.

Interfaces
----------

.. _gui interface implementation:

GUI Interface
~~~~~~~~~~~~~

.. _plot interface implementation:

Plot Interface
~~~~~~~~~~~~~~



Force Spectroscopy Data
-----------------------



Force Volume
~~~~~~~~~~~~



Force Distance Curve
~~~~~~~~~~~~~~~~~~~~



Channel
~~~~~~~



Data Processing
---------------

This package is responsible for the processing of the force spectroscopy data. This includes the import and correction of the measurement data, the calulation of the different channels and an average force distance curve and the export of the data from SOFA. These modules use a procedural approach.  

.. _import data implementation:

Import Data
~~~~~~~~~~~

The Import Data module is responsible for the import of measurement data. It contains functions to import all currently supported file formats. In addition to the required measurement data, other optional files like an image file or data for additional channels can be imported as well. At first the required measurement data are imported. All data files in the folder are collected and seperated into the piezo and deflection data. Afterwards the piezo and deflection data files are loaded using the `Igor <https://github.com/wking/igor>`_. Then invalid values are removed and the curve is splitted into it's approach and retract part. After this process is finished, the optional data is imported. The decorators :code:`decorator_check_file_size_image` and :code:`decorator_check_file_size_channel` check whether all data matches in size.

To add new import formats the dictionary :code:`importFunctions` .  

Import Formats
~~~~~~~~~~~~~~

Import Ibw Data
"""""""""""""""

Correct Data
~~~~~~~~~~~~

corrects the approch part of a single force distance curve
wie wird mit möglichen fehlern error umgegangen
vorgehen verweiß correction algorithm
verweiß zu test

.. _calculate channel data implementation:

Calculate Channel Data
~~~~~~~~~~~~~~~~~~~~~~

enthält funktionen um die einzelnen channel zu berechen
weitere channel braucht funktion die bestimmte argumente bekommt und folgendes zurück liefert
erweiterung in *active_channels*
decorator konvertiert daten in two dimensional np array
verweiß zu test

.. _calculate average implementation:

Calculate Average
~~~~~~~~~~~~~~~~~

.. _export data implementation:

Export Data
~~~~~~~~~~~

exportiert daten eines force volumes aus SOFA 
erstellt dafür ordner
konvertiert dann daten zunächst in pandas dataframes - einfacher zu exportieren
*exportFormats* enthält alle verfügbaren export formate mit dazugehörigen export funktionen
warum die beiden

Named Tuples
~~~~~~~~~~~~

To increase the readability of the code SOFA uses NamedTuple, which are all defined in this file. They are divided into different categories and use type hints, to make it easier to understand the code.

Custom Exceptions
~~~~~~~~~~~~~~~~~

To better undestand possible errors when importing and correcting the measurement data, SOFA uses some custom exceptions. Both cases have a general exception :code:`ImportError` and :code:`CorrectionError` and further specific exceptions. This structure allows to catch a general type of exception with a descriptive name that should make it easier to understand the problem.

Data Visualization
------------------

Plot Data
~~~~~~~~~



.. _tests implementation:

Tests
=====

Data Correction
---------------

Channel Calculation
-------------------

Average
-------

Using SyFoS Data
----------------

Docs
====

The SOFA documentation is written using Sphinx, uses the Furo theme and is hosted with Gihub Pages. It is located in the :code:`gh-pages` branch of the SOFA repository.