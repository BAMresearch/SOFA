.. _correction algorithm:

====================
Correction Algorithm
====================

To be able to analyze the imported measurement data statistically, for example average a subgroup of force curves, the data needs to be corrected. Due to the experiment setup each force curve is exposed to a topography offset and a virtual deflection, shifting the curve in the x and y direction. SOFA automatically tries to shift the point of contact of each force curve to zero, correcting the errors and alignig all curves. SOFA relies on the fact that Force Curves are expected to have a certain typical shape in order to interpret the contact between probe and sample according to theories and physical models. When the quality of the force curves decreases SOFA might not be able to correct them anymore. Below some cases are listed, for which SOFA can not correct the data. 

- In case a curve shows any deviation from F = 0 for Z < 0 beyond certain noise, the point of contact can not be identified conclusively. 
- **WELCHE ANDEREN FÄLLE GIBT ES NOCH**. 

Force curves which can not be corrected are discarded by SOFA. For more detailed information about the edge cases SOFA can't currently handle, see the :ref:`Tests <tests implementation>` section. To shift the point of contact of a single force curve to zero, first its :ref:`force values <correction force>` and then the :ref:`pizeo values <correction piezo>` are corrected.

.. note::

	Up to version 1.0 SOFA processes only the approach part of every imported force distance curve.

.. _correction force:

Correction of the force
=======================

vlt Bild von Kurve vorher nachher einfügen

To correct the virtual deflection the force distance curve is shifted to zero along the deflection (y) axis using the end of the zeroline. Additionally the noise in the deflection values before the point of contact is smoothed. For this, the :ref:`end of the zero line <calculate end of zero line>` must first be found. With the end of the zero line a :ref:`fit of the zero line <fit zero line>` can be calculated. Using this fit the deflection values are :ref:`shifted along the deflection (y) axis <fit zero line>`. 

.. _calculate end of zero line:

Calculate the end of the zero line
----------------------------------

The end of the zeroline is the last measurement point before attractive forces start to appear between the probe and sample. In other words it is the last measurement point with a positive slope before the jump to contact. 

Narrow search area
~~~~~~~~~~~~~~~~~~

.. _fit zero line:

Fit the zero line
-----------------

.. _shift force values:

Shift the force values
----------------------

.. _correction piezo:

Correction of the piezo displacement
====================================

vlt Bild von Kurve vorher nachher einfügen

.. _calculate zero crossing:

Calculate the zero crossing
---------------------------

.. _interpolate point of contact:

Interpolate point of contact
----------------------------

.. _shift piezo values:

Shift the piezo values
----------------------