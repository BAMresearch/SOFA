========
Codebase
========

SOFA is written in Python (should require Python 3.6.1 at minimum) and uses the following external modules and libraries:

- **NumPy** - for basic mathematical computations
- **SciPy** - 
- **Matplotlib** - to plot the data and create the custom toolbars
- **pandas** - to export the data to the different ouput file formats 
- **igor** - to read files in the .ibw (igor binary wave) file format
- **ttkbootstrap** - to give the Tkinter GUI a modern look

SOFA Modules
============

The general aim of SOFA was to write code which is simple to read and easy to extend. The implementation followed the principle of separation of concerns. Therefore SOFA is comprised of multiple distinct modules and on the code level, functions are keept short and only take responsibility for one single functionality. To increase the readability of the code, SOFA tries to implement the following PEP's:

- `PEP 8 <https://peps.python.org/pep-0008/>`_ - The Style Guide for Python Code
- `PEP 257 <https://peps.python.org/pep-0257/>`_ - Docstring Conventions
- `PEP 484 <https://peps.python.org/pep-0484/>`_ - Type Hints

The implementation uses a mixture of object oriented and procedural programming, depending on which is more suitable for the different requirements at hand.

.. _gui implementation:

GUI
---

The GUI of SOFA is written in Tkinter and uses the ttkbootstrap theme extension, to give it a modern look. It consists of of three windows, the main window and two subwindows for the data import and export. All of them are written in an object oriented approach.

Main Window  `source <https://github.com/2Puck/sofa/tree/development>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wie sind plots in tkinter eingebunden
interaktionsmöglichkeiten

Import Window
~~~~~~~~~~~~~

Export Window
~~~~~~~~~~~~~

Window Settings
~~~~~~~~~~~~~~~

GUI Interface
~~~~~~~~~~~~~

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

Custom Exceptions
~~~~~~~~~~~~~~~~~

Data Visualization
------------------

Plot Data
~~~~~~~~~

Tests
=====



Docs
====

The SOFA documentation is written using Sphinx, uses the Furo theme and is hosted with Gihub Pages.