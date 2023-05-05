=========================
Atomic Force Spectroscopy
=========================

Atomic force microscopy (AFM) is a powerful tool used to investigate surfaces at the nanoscale level. Atomic force spectroscopy (AFS) is a variation of AFM that measures the force between a small probe and the sample surface to obtain detailed information about its properties. AFS can provide valuable insights into the physical, chemical, and mechanical properties of materials, including elasticity, adhesion, and friction. It works by bringing the probe very close to the sample surface, such that the attractive or repulsive forces between them can be measured. The probe is mounted on a cantilever that can deflect in response to the forces between it and the sample surface. By monitoring the deflection of the cantilever, the force between the probe and the surface can be measured. 

During a measurement, the probe is brought into contact with the sample surface and retracts after the maximum piezo is reached. By measuring the piezo displacement and the force as the probe is moved towards and away from the surface a single :ref:`force distance curve <force distance curve>` is obtained. This measurement process is repeteated for every measurement point of the sample. Resulting in a set of m x n force distance curves, called :ref:`force volume <force volume>`. The analysis of each force distance curve can result in different physical properties of the measurement point of the material. When this is done for every force distance curve in the force volume statements can be made about the general properties of the sample.

.. note::
	The current version of SOFA (version 1.0) only takes the approach part of the force distance curves into consederation. During the import process of the measurement data every curve is splitted into an approach and retract part using the maximum piezo.

The interpretation of AFS data can be complex, requiring advanced modeling and analysis techniques to extract meaningful information. This is due to some :ref:`measurement errors <measurement erros>` which occur during the measurement. SOFA automatically :ref:`corrects <correction algorithm>` these errors and calculates multiple different :ref:`channels <channels>` which makes the evaluation of the data much easier. 

For more detailed information about the underlying theories, see - add link to paper.

.. _force volume:

Force Volume
============

zusammenhang zwischen curve und channel erklären

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

The approach part of a force distance curve can be devided into three different parts 

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

Point Of Contact
~~~~~~~~~~~~~~~~

.. _measurement erros:

Measurement Erros
=================

Topography Offset
-----------------

Virtual Deflection
------------------