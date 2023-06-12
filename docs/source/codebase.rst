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

The general aim of SOFA was to write code which is simple to read and easy to extend. The implementation followed the principle of separation of concerns. Therefore functions are keept short and only take responsibility for one single functionality. To increase the readability of the code, SOFA tries to implement the following PEP's:

- `PEP 8 <https://peps.python.org/pep-0008/>`_ - The Style Guide for Python Code
- `PEP 257 <https://peps.python.org/pep-0257/>`_ - Docstring Conventions
- `PEP 484 <https://peps.python.org/pep-0484/>`_ - Type Hints

The implementation uses a mixture of object oriented and procedural programming, depending on which is more suitable for the different requirements at hand.

Packages Peculiarities
======================

GUI
---

The GUI of SOFA is written in Tkinter and uses the ttkbootstrap theme extension, to give it a modern look. To embed the different plots in the :code:`MainWindow` SOFA uses the :code:`FigureCanvasTkAgg` from the Matplotlib tkinter backend. If an error occurs during the import or export process the user is informed via a message box. Both the Import and Export Window contain a progressbar to show the current progress. The :code:`indeterminate` mode of the Tkinter toolbar did not work therefore they run as a very simple :code:`determinate` version. In the :code:`ImportWindow` this was probadly due to the fact how SOFA handles exceptions during the import process.

Toolbar
-------

The :code:`SofaToolbar` base class for the different toolbars of SOFA is inhereted from the Matplotlib :code:`NavigationToolbar2Tk`. 

Line Plot Toolbar
~~~~~~~~~~~~~~~~~

When zooming in or out of the plot it felt inefficient to always cache the basic view limits. Therefore when zooming into the plot, the old view limits are cached and not the new ones. Making it easier to revert a single step or to reset the zoom as a whole. The selection mode of single force distance curves uses the Matplotlib :code:`pick_event` in combination with the :code:`pickradius` attribute of the :code:`Line2D` objects. While this mode is active mouse clicks which are close enough to a curve will toggle their state. The function to select multiple force distance curves uses the current view limits and tries to disable all curves within the current view. However, the current implementation only disables all curves that actually have a data point within the current view. This neglects all cases where curves only intersect the current view limits. An older version of SOFA calculated whether a curve intersects the boundaries of the current view if it has no data points in the boundaries. However, this increases the computational effort considerably, which is especially problematic for large force volumes with a lot of force distance curves. Therefore, the faster but somewhat less precise solution was chosen in the end.

Heatmap Toolbar
~~~~~~~~~~~~~~~

The two different modes to select an area of the heatmap both use the :code:`button_press_event` and :code:`button_release_event` of matplotlib to capture the movement of the mouse while the mouse button is pressed. To select a rectangular area, a rectangle is drawn between the start and end points of the mouse movement. Start and end point are defined by clicking and releasing the mouse button. To indicate the selected area, red lines are drawn around the resulting rectangle. The other mode allows to select any area. To do this, a tuple with the x and y indices of every data point of the heatmap over which the mouse moves while the button is pressed are cached. Indicating such a created area by outlining it with red lines is difficult. To achieve this, each point of the selected area is first outlined with red lines. This already results in the the outline of the area, but there are also unwanted red lines within the area. To delete the unwanted marking lines every line which exists exactly twice, is deleted. After an area is selected, either all points in or outside the area can be disabled. 

Data Processing
---------------

To import data files in the ibw file format SOFA uses `Igor <https://github.com/wking/igor>`_.

Docs
====

The SOFA documentation is written using Sphinx, uses the Furo theme and is hosted with Gihub Pages. It is located in the :code:`gh-pages` branch of the SOFA repository.