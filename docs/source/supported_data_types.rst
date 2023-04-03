====================
Supported Data Types
====================

Please make sure that the raw FSD can be exported from your AFM device. SOFA 1.0 can only import directly \*.ibw (igor binary wave, supported by oxford instrument Asylum AFM) and \*.hdf5.

.. note::

	We intend to make data import possible for most common FSD formats. If you wish to use SOFA for analyzing your experimental data, please contact sofa@bam.de and provide us with a small data set of exemplary FSD (2x2 curves are sufficient), model and maker of your AFM and the maker and version of the used software.

In case your FSD format is accepted by SOFA, please make also sure that the data is organized as a Force Volume (FV), i.e. each FS curve is assigned to a x,y-coordinate in a spatial grid, as described in detail in :ref:`force spectroscopy data structure`. SOFA 1.0 can only handle FV with a square grid i.e., number of curves in x and y direction is identical.

.. _force spectroscopy data structure:

Force Spectroscopy data structure
=================================

FSD contains single Force Curves (aka Force-Distance curves, FDC) which consist of two data sets of equal dimensions, the controlled variable **piezo displacement Z** and the measured variable **force F**.

.. note:: 

	For simplicity’s sake we refer in this manual to the raw data as piezo displacement Z and force F, although individual AFM set-ups export cantilever deflection δ [nm] or t-b-signal [V] instead of force F [N]. These observables can be treated as equal since they are proportional to each other. Deflection δ and t-b signal are connected through their proportionality factor sensitivity Ω [nm/V], provided by calibration procedure of the AFM set-up (δ = (t-b)\*Ω). Cantilever deflection δ is proportional to the force F since the AFM cantilever is assumed to be an elastic spring with the proportionality factor or spring constant kc [N/nm], as provided by Hooke’s law (F = kc\*δ). Usage of different observables is only of consequence when absolute values are calculated, which is addressed in :ref:`channels based on physical values`.

Force curves can be differently stored, depending on the software used in AFM set-ups. Approach and retract part of the curve can be merged in one data set, or already split in two separate data sets. As of version 1.0, SOFA’s algorithm expects a merged data set and provides a step to split the approach part from the retract part. All subsequent steps of SOFA ignore the retract part and analyze the approach part. Incorporation of the retract part in the analysis will be provided in future versions of SOFA.

Also, storage of a FV can differ significantly, depending on the software used in the AFM set-up. The two most common forms are depicted in a schematic drawing in Figure 1.

.. figure:: images/data_organization_of_fsd_sets.jpg
	:alt: drawing of typical data organization of FSD sets

	Figure 1 schematic drawing of typical data organization of FSD sets force and distance. A) 3D in n x n matrices, with n being the number of lines and rows of the measurement grid. B) 2D in a (n*n) linear data set.
	

Besides the most common ways of storing FSD in a compact form as shown above, single curves can be stored in a hierarchical folder system.

Most exported FSD formats also include notes or headers which describe the experimental set-up, i.e. time, date, temperature, calibration data, measurement rate, maximum force, dimension of FV in points, lines, x and y-range. In case this additional data is available, SOFA will import information, which is necessary for further analysis, such as the spring constant kc or the sensitivity Ω.

Also included in the exported FSD are raw parameter maps, which can be also uploaded and used for further analysis in SOFA, as shown in Parameter maps.

.. _import formats:

Import Formats
==============

add text

.. _export formats:

Export Formats
==============

add text