.. _correction algorithm:

====================
Correction Algorithm
====================

To be able to analyze the imported measurement data statistically, for example average a subgroup of force curves, the data needs to be corrected. Due to the experiment setup each force curve is exposed to a topography offset and a virtual deflection, shifting the curve in the x and y direction. SOFA automatically tries to shift the point of contact of each force curve to zero, so they all align. To be able to do that, SOFA relies on the fact that Force Curves are expected to have a certain typical shape in order to interpret the contact between probe and sample according to theories and physical models. When the quality of the force curves decreases SOFA might not be able to correct them anymore. Below are some cases are listed, for which SOFA can not correct the data. 

- In case a curve shows any deviation from F = 0 for Z < 0 beyond certain noise, the point of contact can not be identified conclusively. 
- **WELCHE ANDEREN FÄLLE GIBT ES NOCH**. 

Force curves which can not be corrected are discarded by SOFA. For more detailed information about the edge cases SOFA can't currently handle, see the :ref:`Tests <tests implementation>` section. To shift the point of contact of a single force curve to zero, first its force values and then the pizeo values are corrected.

Correction of the force
=======================



Calculate the end of the zero line
----------------------------------

Narrow search area
~~~~~~~~~~~~~~~~~~

Fitt the zero line
------------------

Shift the force values
----------------------

Correction of the piezo displacement
====================================

Calculate the zero crossing
---------------------------

Interpolate point of contact
----------------------------

Shift piezo displacement values
-------------------------------