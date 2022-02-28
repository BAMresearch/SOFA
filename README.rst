============
SOFA
============

Description
===========
SOFA is an intuitive open-source GUI program which addresses the most common problems of AFM force spectroscopy: finding the true point of contact of any given force-distance curve and increasing signal to noise ratio of single curves by defining and averaging representative subsets of curves. By loading an array of curves (force map or force volume depending on the AFM company) into SOFA a universal algorithm corrects and plots all force distance curves (either approach or retract) into one common coordinate system (cantilever deflection δ vs piezo displacement Z). Subgroups of curves can be defined by either i) choosing a section of the x,y array or ii) excluding single curves (visual outliers) or iii) using predefined curve characteristics (channels, i.e. stiffness, adhesion, hysteresis). Subsets of curves are automatically averaged and can be exported for subsequent analysis, as can the channel maps. 

Examples
========
Test data can be found in the sofa/test_data folder. There is data for both the IM and FTC methods. For a detailed documentation on how to use the software check out the tutorial in the documentation.

Installation
============
To install the software either clone the git repository, install the requirements and execute the sofa.py file or use the executable file.

Contact
============
To get in contact please use the following email address: sofa@bam.de

License
=======
This software is distributed under the GNU GENERAL PUBLIC LICENSE, see the COPYING file for detailed information.