====================================================
L5: Sensing and Perception for Robotic Systems
====================================================

Overview
--------

This lecture covers classical perception for a factory cell: getting
structured information out of sensor data. In ARIAC 2025 your team chooses
and places its own sensors (break beams, distance sensors, RGB cameras,
lidar) within a budget. ARIAC requires lidar for cell inspection, so the
lecture first finds dents, scratches and bulges in lidar point clouds and
turns them into an inspection report, and measures the detector with
precision and recall. Camera images come later: the VLM in GP4 reads them
(L9), and L10 teaches the camera model that locates the Task 2 top shell. Quiz 2 (L4) is given at the start
of class. GP1 is due and GP2 is posted.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Choose sensors and their placement for an inspection task within a budget.
- Read a ``PointCloud2`` message and transform its points into a frame on the
  cell with TF2.
- Detect surface defects on a cell by comparing its points with a cylinder.
- Wrap a perception pipeline as a ROS 2 node.
- Evaluate a defect detector with precision and recall against ground truth.


.. admonition:: Materials in progress
   :class: note

   The lecture notes, quiz and references for this lecture are written with
   the slide deck and are not published yet. This page will link to them
   once they are ready. The topics below are the plan.


Planned Topics
--------------

- ARIAC 2025 sensors: break beams, distance sensors, RGB cameras and lidar;
  their cost grades, the sensor budget, and the bounding boxes lidar must sit
  in.
- Point clouds: the ``PointCloud2`` message, how many points land on a cell,
  and combining scans as the cell moves.
- Finding defects: fit the cell's cylinder and flag points that sit inside it
  (dents, scratches) or outside it (bulges).
- Inspection reports: pass or fail and the defect list, submitted before the
  cell reaches the inspection door. The voltage is a separate check at the
  tester.
- TF2 in a perception pipeline: sensor frame to world frame.
- ROS 2 perception node patterns: sensor subscriber, result publisher, latency.


ARIAC Tie-in
------------

GP2 is this lecture applied to the inspection conveyor: place lidar sensors
within the sensor budget, detect dents, scratches and bulges from the point
clouds, and submit an inspection report for each cell before it reaches the
inspection door. A failing report sends the cell into the inspection bin. The
GP1 behavior tree then reads the voltage of each cell that passes and places
or recycles it.


Starting References
-------------------

- ARIAC 2025 scenario (Step 1a, physical inspection): https://pages.nist.gov/ARIAC_docs/en/latest/pages/scenario.html
- ROS 2 TF2 tutorials: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/
- ARIAC 2025 sensors: https://pages.nist.gov/ARIAC_docs/en/latest/pages/sensors.html
- ARIAC GitHub: https://github.com/usnistgov/ARIAC


Next Steps
----------

- Quiz 2 today (L4).
- GP1 is due today. **GP2 is posted today** and is due in Week 7.
- In the next lecture, we will cover **task planning with PDDL**, the
  classical planner that consumes the representation and the perception
  output.
