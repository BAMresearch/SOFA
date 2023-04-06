====================
Supported Data Types
====================

Please make sure that the raw FSD can be exported from your AFM device. SOFA 1.0 can only import .ibw (igor binary wave) files, supported by :ref:`oxford instrument Asylum AFM <ibw oxford instrument asylum afm>`. In case your FSD format is accepted by SOFA, please make also sure that the data is organized as a Force Volume (FV), i.e. each FS curve is assigned to a x,y-coordinate in a spatial grid, as described in detail in :ref:`force spectroscopy data structure`. SOFA 1.0 can only handle FV with a square grid i.e., number of curves in x and y direction is identical.

.. note::

	We intend to make data import possible for most common FSD formats. If you wish to use SOFA for analyzing your experimental data, please contact sofa@bam.de and provide us with a small data set of exemplary FSD (2x2 curves are sufficient), model and maker of your AFM and the maker and version of the used software.

.. _force spectroscopy data structure:

Force Spectroscopy data structure
=================================

FSD contains single Force Curves (aka Force-Distance curves, FDC) which consist of two data sets of equal dimensions, the controlled variable **piezo displacement Z** and the measured variable **force F**.

.. note:: 

	For simplicity’s sake we refer in this manual to the raw data as piezo displacement Z and force F, although individual AFM set-ups export cantilever deflection δ [nm] or t-b-signal [V] instead of force F [N]. These observables can be treated as equal since they are proportional to each other. Deflection δ and t-b signal are connected through their proportionality factor sensitivity Ω [nm/V], provided by calibration procedure of the AFM set-up (δ = (t-b)\*Ω). Cantilever deflection δ is proportional to the force F since the AFM cantilever is assumed to be an elastic spring with the proportionality factor or spring constant kc [N/nm], as provided by Hooke’s law (F = kc\*δ). Usage of different observables is only of consequence when absolute values are calculated, which is addressed in :ref:`channels based on physical values`.

Force curves can be differently stored, depending on the software used in AFM set-ups. Approach and retract part of the curve can be merged in one data set, or already split in two separate data sets. As of version 1.0, SOFA’s algorithm expects a merged data set and provides a function to split the approach part from the retract part. All subsequent steps of SOFA ignore the retract part and analyze the approach part. Incorporation of the retract part in the analysis will be provided in future versions of SOFA.

Also, storage of a FV can differ significantly, depending on the software used in the AFM set-up. The two most common forms are depicted in a schematic drawing in Figure 1.

.. figure:: images/data_organization_of_fsd_sets.jpg
	:alt: drawing of typical data organization of FSD sets

	Figure 1 schematic drawing of typical data organization of FSD sets force and distance. A) 3D in n x n matrices, with n being the number of lines and rows of the measurement grid. B) 2D in a (n*n) linear data set.
	

Besides the most common ways of storing FSD in a compact form as shown above, single curves can be stored in a hierarchical folder system.

Most exported FSD formats also include notes or headers which describe the experimental set-up, i.e. time, date, temperature, calibration data, measurement rate, maximum force, dimension of FV in points, lines, x and y-range. In case this additional data is available, SOFA can import information, which is necessary for further analysis, such as the spring constant kc or the sensitivity Ω.

Also included in the exported FSD are raw parameter maps, which can be also uploaded and used for further analysis in SOFA, as shown in Parameter maps.

.. _import formats:

Import Formats
==============

SOFA requires the data to be in a spefic format to be able to read it. Below are all currently supported import formats listet. The `test_data <https://github.com/2Puck/sofa/tree/development/test_data>`_ folder of the SOFA repository includes some files in the ibw oxford instrument asylum afm format, that SOFA can import.

.. _ibw oxford instrument asylum afm:

ibw oxford instrument Asylum AFM 
--------------------------------

Measurement Data
~~~~~~~~~~~~~~~~

In order for SOFA to import measurement data the data needs to be organized as lines and points per line within a folder. The single data files for the piezo displacement and force need to end with **ZSnsr.ibw** and **Defl.ibw**. Within the files, SOFA expects to find the key **wave** and and therein the key **wData**.

Image
~~~~~

To be able to read an image file, SOFA expects the **wave** key and therein the following keys **wave_header**, **note** and **wData** in the file. SOFA imports the following informations from them:

- **wave_header** - size of the measurement grid
- **note** - fast scan size, slow scan size, x offset, y offset and spring constant
- **wData** - height and adhesion channel 

Parameter Maps
~~~~~~~~~~~~~~

Work in progress

.. _export formats:

Export Formats
==============

SOFA allows to export the plots of the line plot, heatmap and histogram of the active channel and the data created during the analysis cycle. The exported data consists of the name, size, if available data from an image, raw measurement data, corrected measurement data, average data and the data of every channel flatten into one dimesion. The plots are saved as png file. Below are all currently supported export formats for the data listed:

- .csv
- .xlsx

Adding custom Import or Export formats
======================================

As mentioned above you can contact us under sofa@bam.de or extend the SOFA code. See :ref:`Import Data <import data implementation>` or :ref:`Export Data <export data implementation>` for further information about the implementation of the import and export functionality.