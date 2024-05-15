====
SOFA
====

Description
===========
SOFA is a GUI which addresses the most common problems of AFM force spectroscopy: finding the true point of contact of any given force-distance curve and increasing signal to noise ratio of single curves by defining and averaging representative subsets of curves. By loading an array of curves (force map or force volume depending on the AFM company) into SOFA a universal algorithm corrects and plots all force distance curves into one common coordinate system (cantilever deflection δ vs piezo displacement Z). 

Subgroups of curves can be defined by either 

- choosing a section of the x,y array 
- excluding single curves (visual outliers) 
- using predefined curve characteristics (channels, i.e. stiffness, adhesion, hysteresis). 

Subsets of curves are automatically averaged and can be exported for subsequent analysis, as can the channel maps. 

Documentation
=============
For examples of how SOFA can be used and detailed information about the implementation of SOFA read the `documentation <https://bamresearch.github.io/sofa/build/html/index.html>`_.

Examples
========
Test data can be found in the test_data folder. The data is from the FTC method. For a detailed documentation on how to use the software see the tutorial section in the documentation.

Installation
============

First, get a copy of the source code. Either by cloning this repository or by downloading a snapshot ZIP package by clicking on that green button above.

Windows
-------

Install miniconda or miniforge, for example `from here <https://docs.anaconda.com/free/miniconda/miniconda-other-installer-links/>`_. Open the *Miniconda Prompt* or the *Miniforge Prompt* and type the following commands. 

First, create a new environment for *SOFA* and required packages::

    conda create -n sofa

Activate the new environment::

    conda activate sofa

Install required packages which are specified in `requirements.txt` file::

    conda -c conda-forge install --file requirements.txt

Install additional packages *SOFA* requires which not available through *conda*::

    pip install -r requirements_pip.txt

Finally, run the program::

    python sofa/sofa.py

Linux/Ubuntu
------------

Install tkinter system wide packages::

    sudo apt install python3-tk python3-pil.imagetk

Create a Python virtual environment (venv) for SOFA required modules::

    python3 -m venv --system-site-packages --symlinks ~/.py11sofa

Activate that venv::

    source ~/.py11sofa/bin/activate

Install further Python packages required by SOFA::

    cd <SOFA-directory>
    pip install -r requirements.txt -r requirements_pip.txt

Finally, run the program::

    python sofa/sofa.py

Contact
=======
To get in contact please use the following email address: sofa@bam.de

License
=======
This software is distributed under the GNU GENERAL PUBLIC LICENSE, see the COPYING file for detailed information.
