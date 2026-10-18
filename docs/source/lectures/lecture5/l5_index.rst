====================================================
L5: Sensing and Perception for Robotic Systems
====================================================

Overview
--------

**Your GP1 tree submits an inspection report for every cell, and every report
says the cell passed. This lecture answers the next question: how does the
system find out that a cell is defective, and how sure can it be?**

**Perception** turns sensor data into facts the rest of the system can use,
such as "this cell has a dent at :math:`\theta` = 0.3 rad, :math:`z` = 14 mm".
ARIAC 2025 publishes no pose topics and no TF frames for cells or shells, so a
team learns where things are, and whether a cell is good, only from the
sensors it places.

The lecture starts with the ARIAC sensors: how a team declares them, what each
grade costs, the three boxes a lidar must sit in, and how the sensor cost
bonus is computed against the $9600 budget. It then reads a lidar's
``PointCloud2`` message into NumPy and moves its points to the world frame with
TF2, and computes how far apart lidar points land on a cell. The main part
builds a **cylinder-fit defect detector** in eight steps (crop, separate cells,
undo the belt's motion, fit the axis, measure each point's distance from the
fitted cylinder, threshold, cluster, classify) and runs it on synthetic cells.
A measurement of ARIAC's own training meshes shows that their defects are 0.84
to 2.49 mm deep, while the ARIAC documentation says every defect is at least
2 mm from the surface. The lecture ends with the inspection report and its two
bonuses, the voltage readings, and how to score a detector with **precision**
and **recall**, including what each kind of error costs in ARIAC.

.. important::

   **ARIAC tie-in.** Every example is the inspection step of Task 1: lidars in
   the boxes around the inspection conveyor, a report for each cell before it
   reaches the inspection door at :math:`x` = 1.0 m, and the voltage check
   that comes later at a tester.

.. important::

   **Group project.** **GP2 (Cell Inspection)** is posted today and is due in
   Week 7 (03/10). It uses everything in this lecture: place lidars within the
   boxes and the budget, detect defects from the point clouds, report every
   cell, average the voltage readings, and measure precision and recall.

.. warning::

   **The demo data is synthetic.** Every point cloud and every voltage
   reading in the lecture's demos is made in NumPy by the lecture's scripts,
   not by ARIAC. The one exception is the defect depth measurement, which
   reads ARIAC's own mesh files.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Choose sensor types, grades and placements for the ARIAC inspection task,
  and compute their total cost and sensor cost bonus against the $9600 budget.
- Describe the structure of a ROS 2 ``PointCloud2`` message and transform its
  points from the sensor frame to the world frame with TF2.
- Compute the spacing between lidar points on a cell from the sample count,
  the angular range and the distance to the cell.
- Explain the steps of a point cloud defect detector: crop, stack the scans of
  a moving cell, fit a cylinder, and flag points that lie inside or outside it
  by more than a threshold.
- Compute a defect's location (:math:`\theta` and :math:`z`) in the form the
  ARIAC inspection report uses.
- Evaluate a defect detector with precision and recall, and compare the score
  cost of a missed defect with the cost of a false alarm.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l5_lecture
   l5_code
   l5_exercises
   l5_quiz
   l5_references


Next Steps
----------

- **Next class, Wednesday, March 3:** L6, Task-Level Planning with PDDL:
  domains and problems, typed predicates, and running a planner from Python.
- **Before next class:**

  - Read the PDDL Primer pre-read on the course site.
  - Install the Unified Planning Framework with Fast Downward in a virtual
    environment: ``python3 -m venv ~/venvs/planning``, then
    ``~/venvs/planning/bin/pip install unified-planning up-fast-downward``.
  - Run the L5 scripts (see :doc:`l5_code`) and compare your outputs with the
    notes.
  - Work through the :doc:`L5 exercises <l5_exercises>` and the
    :doc:`self-check quiz <l5_quiz>`.

- **Quiz 3**, at the start of Week 7, covers L5 and L6.
- **GP2** is due in Week 7 (03/10).
