=========================
Atomic Force Spectroscopy
=========================

Atomic force microscopy (AFM) is a powerful tool used to investigate surfaces at the nanoscale level. Atomic force spectroscopy (AFS) is a variation of AFM that measures the force between a small probe and the sample surface to obtain detailed information about its properties. AFS can provide valuable insights into the physical, chemical, and mechanical properties of materials, including elasticity, adhesion, and friction. It works by bringing the probe very close to the sample surface, such that the attractive or repulsive forces between them can be measured. The probe is mounted on a cantilever that can deflect in response to the forces between it and the sample surface. By monitoring the deflection of the cantilever, the force between the probe and the surface can be measured. 

During a measurement, the probe is brought into contact with the sample surface and retracts after the maximum piezo is reached. By measuring the piezo displacement and the force as the probe is moved towards and away from the surface a single :ref:`force distance curve <force distance curve>` is obtained. This measurement process is repeteated for every measurement point of the sample. Resulting in a set of m x n force distance curves, called :ref:`force volume <force volume>`. By analysing the individual force distance curves, conclusions can be drawn about the properties of the sample. If this is done for each force distnace curve in the force volume, :ref:`channels <channels>` about the different properties can be obtained. 

The interpretation of AFS data can be complex, requiring advanced modeling and analysis techniques to extract meaningful information. This is due to some :ref:`measurement errors <measurement erros>` which occur during the measurement. SOFA automatically :ref:`corrects <correction algorithm>` these errors and calculates multiple different :ref:`channels <channels>` which makes the evaluation of the data much easier. 

For more detailed information about the underlying theories, see - add link to paper.

.. note::
	The current version of SOFA (1.0) only takes the approach part of the force distance curves into consederation. Therefore the retreat part of the force distance curves is neglected in the following.

.. _force volume:

Force Volume
============

A force volume is a set of m x n force distance curves, resulting from an AFM measurement. After the force distance curves of the force volume have been corrected the different channels can be calculated.

.. _force distance curve:

Force Distance Curve
====================

.. figure:: images/force_distance_curve.svg
	:alt: image of the approach part of a force distance curve

	Approach part of a corrected force distance curve with the different sections and points of interest.

A force distance curve represents the force applied by the cantilever of the AFM probe on the sample surface as a function of the distance between the probe and the surface. 

.. _curve sections:

Curve Sections
--------------

Zero Line
~~~~~~~~~

The zeroline of a force distance curve represents the baseline level of the measured force when the AFM probe is positioned far away from the sample surface, beyond the range of any interaction forces. Therefore the measured force in this section is primarily due to noise or drift in the measurement system. 

Attractive Area
~~~~~~~~~~~~~~~

The attractive area of a force distance curve is the section where the probe and the sample are held together by van der Waals, electrostatic, or chemical interactions. In this region, the force decreases as the attractive forces become stronger as the probe is brought closer to the surface until the force reaches a minimum value. From this point on, the probe and sample are already so close that the attractive forces start to decrease again and the force thus increases.

Repulsive Regime
~~~~~~~~~~~~~~~~

The repulsive area of a force distance curve refers to the region of the curve where the probe and the sample surface are in contact and thus pushed apart by repulsive forces. They continue to approach each other until the maximum piezo value is reached. This region is characterized by an increase in the measured force, which is proportional to the strength of the repulsive forces.

.. _points of interest:

Points of Interest
------------------

End Of Zeroline
~~~~~~~~~~~~~~~

Jump To Contact
~~~~~~~~~~~~~~~

oder auch nicht test

Point Of Contact
~~~~~~~~~~~~~~~~

.. _measurement erros:

Measurement Erros
=================

During the measurement each force distance curve 

Topography Offset
-----------------

The topography offset is a shift of the force distance curve in the piezo (x) axis. This error arises because

Virtual Deflection
------------------

The virtual deflection is a shift of the force distance curve in force (y) axis. This error is caused by the fact that 