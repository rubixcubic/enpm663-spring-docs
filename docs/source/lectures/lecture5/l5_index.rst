====================================================
L5: Sensing and Perception for Robotic Systems
====================================================

Overview
--------

This lecture covers classical perception for a factory cell: getting
structured information out of camera images and sensor topics. In ARIAC 2025
your team chooses and places its own sensors (RGB cameras, break beams,
distance sensors, lidar) within a budget. The lecture uses OpenCV to find
cells and their surface defects (dents, scratches, bulges), combines them
with the voltage readings, and converts image positions to robot-frame
positions with the camera model and TF2. Quiz 2 (L4) is given at the start of
class. GP1 is due and GP2 is posted.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Choose sensors and their placement for an inspection task within a budget.
- Use OpenCV to segment objects and extract features from an RGB image.
- Convert image coordinates to camera-frame and world-frame positions with the
  camera model, known geometry and TF2.
- Wrap a perception pipeline as a ROS 2 node.
- Evaluate a defect detector with precision and recall against ground truth.


.. admonition:: Materials in progress
   :class: note

   The lecture notes, quiz and references for this lecture are written with
   the slide deck and are not published yet. This page will link to them
   once they are ready. The topics below are the plan.


Planned Topics
--------------

- ARIAC 2025 sensors: RGB cameras, break beams, distance sensors and lidar;
  their cost grades and the sensor budget.
- Image preprocessing: color spaces, thresholding, morphological operations.
- Finding cells and surface defects: contours, regions, simple features.
- Camera model: intrinsics and extrinsics; locating an object on a known plane
  (the conveyor) without a depth camera.
- TF2 in a perception pipeline: camera frame to world frame.
- ROS 2 perception node patterns: image subscriber, result publisher, latency.
- Inspection reports: pass or fail, the defect list, and the voltage readings.


ARIAC Tie-in
------------

GP2 is this lecture applied to the inspection conveyor: place cameras within
the sensor budget, detect dents, scratches and bulges, combine them with the
voltage readings, and submit an inspection report for each cell. The GP1
behavior tree then recycles the cells that fail.


Starting References
-------------------

- OpenCV documentation: https://docs.opencv.org/4.x/
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
