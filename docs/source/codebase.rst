========
Codebase
========

SOFA is written in Python (should require Python 3.6.1 at minimum) and uses the following external modules and libraries:

- **NumPy** - for basic mathematical computations
- **SciPy** - for some specific mathematical computations
- **Matplotlib** - to plot the data and create the custom toolbars
- **pandas** - to export the data to the different ouput file formats 
- **igor** - to read files in the .ibw (igor binary wave) file format
- **ttkbootstrap** - to give the Tkinter GUI a modern look

SOFA Modules
============

The general aim of SOFA was to write code which is simple to read and easy to extend. The implementation followed the principle of separation of concerns. Therefore SOFA is comprised of multiple distinct modules. On the code level functions are keept short and only take responsibility for one single functionality. To increase the readability of the code, SOFA tries to implement the following PEP's:

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

The main window of SOFA contains ... . The widgets . The main window uses mostly the pack geometry manager. Only for complexer layouts like in the in ... frame the grid manager is used.  

einzelne frames erklären
wie sind plots in tkinter eingebunden
gui interface ansprechen warum nachher attribute setzen
interaktionsmöglichkeiten toolbars histogram buttons
import and export window ansprechen

Import Window
~~~~~~~~~~~~~

The import window is a small subwindow to handle the import of measurement data. Like in the main window the different widgets are arranged in rows using only the pack geometry manager. It contains a indeterminate progressbar to show if the import process is still runing and which process is currently being executed. The decorator *decorator_check_required_folder_path* checks if a required measurement folder is selected before the import process starts.

During the import process the selected measurement files are first imported and combined into one data dictionary with the selected import function of the :ref:`Import Data <import data implementation>` module. Afterwards the data dictionary is passed to the :ref:`GUI Interface <gui interface implementation>`, where a new force volume will be created. Finally the foldername, size and folderpath of the imported measurement data are set in the Active Data frame of the :ref:`Main Window <main window implementation>`.

If an error occurs during the import process the user is informed via a message box and the import process is terminated. If the data could sucessfully be imported the window closes it self and informs the user via a message box.

Export Window
~~~~~~~~~~~~~

The export window is a small subwindow to handle the export of the imported force volumes. Like in the main window the different widgets are arranged in rows using only the pack geometry manager. It contains a indeterminate progressbar to show if the import process is still runing.
The decorator *decorator_check_required_folder_path* and *decorator_check_required_folder_name* check if the required folder path and folder name for the ouput folder are selected before the export process starts.

In the export process the data of the selected force volume can be exported to the selected :ref:`export formats <export formats>`. The :ref:`Export Data <export data implementation>` module creates an output folder for data with the selected location and name. After this the data of the selected force volume is exported to the different formats.


Window Settings
~~~~~~~~~~~~~~~

Interfaces
----------

.. _gui interface implementation:

GUI Interface
~~~~~~~~~~~~~

Plot Interface
~~~~~~~~~~~~~~

.. _toolbar implementation:

Toolbar
-------

Lineplot Toolbar
~~~~~~~~~~~~~~~~



Heatmap Toolbar
~~~~~~~~~~~~~~~



FDC Data
--------

Force Volume
~~~~~~~~~~~~



Force Distance Curve
~~~~~~~~~~~~~~~~~~~~



Channel
~~~~~~~



Average Force Distance Curve
~~~~~~~~~~~~~~~~~~~~~~~~~~~~



Data Processing
---------------

.. _import data implementation:

Import Data
~~~~~~~~~~~



Correct Data
~~~~~~~~~~~~



.. _calculate channel data implementation:

Calculate Channel Data
~~~~~~~~~~~~~~~~~~~~~~

.. _export data implementation:

Export Data
~~~~~~~~~~~

Named Tuples
~~~~~~~~~~~~

To increase the readability of the code SOFA uses NamedTuple. These are all defined in this file. - Type hints und Aufteilung ansprechen - 

Custom Exceptions
~~~~~~~~~~~~~~~~~

- warum eigene exceptions - for the import and correction process. Both cases have a general exception - *ImportError* and *CorrectionError* and further specific exceptions to - erklären warum die struktur gewählt wurde -

Data Visualization
------------------

Plot Data
~~~~~~~~~



.. _tests implementation:

Tests
=====



Docs
====

The SOFA documentation is written using Sphinx, uses the Furo theme and is hosted with Gihub Pages.