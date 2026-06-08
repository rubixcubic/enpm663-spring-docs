====================================================
Week 5: Sensing and Perception for Robotic Systems
====================================================

Overview
--------

This lecture covers classical perception for robotic systems: extracting
structured information (part identities and 3D poses) from camera images.
We use OpenCV for color segmentation, contour detection, and bounding-box
extraction, then convert pixel coordinates to robot-frame 3D poses via
camera intrinsics, extrinsics, and TF2. Quiz #2 (covering Week 4 BTs) is
administered at the start of class. PT1 is due today; PT2 is handed out.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Use OpenCV to segment colored objects and extract bounding boxes and
     centroids.
   - Convert pixel coordinates to camera-frame 3D coordinates using camera
     intrinsics and depth.
   - Transform camera-frame poses to a world frame using TF2.
   - Wrap a perception pipeline as a ROS 2 node with publish/subscribe.
   - Evaluate perception output against ground-truth poses.


Topics
------

- Image preprocessing: color spaces (BGR, HSV), thresholding, morphological
  operations.
- Contour detection and bounding-box extraction; centroid estimation.
- Camera model: intrinsics, extrinsics, depth, pixel-to-3D conversion.
- TF2 in perception pipelines: camera frame to world frame.
- ROS 2 perception node patterns: image subscriber, pose publisher, latency.


Hands-On Exercise
-----------------

Given a static ARIAC scene image (TODO: provide), detect parts by color and
output their image-frame centroids. Then add TF2 to convert one detection
into a world-frame pose using a published camera transform. (TODO: starter
package.)


ARIAC Tie-in
------------

ARIAC's overhead RGB-D cameras above the supply bins are the input to PT2's
perception pipeline. The four part colors (red, green, blue, purple) and
four part types (battery, sensor, regulator, pump) define the detection
classes.


References
----------

- OpenCV documentation: https://docs.opencv.org/4.x/
- ROS 2 TF2 tutorials: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/
- ARIAC sensor configuration: TODO link into ARIAC docs.
- ARIAC GitHub: https://github.com/usnistgov/ARIAC


Next Steps
----------

- Quiz #2 today (Week 4 BTs).
- PT1 due today; PT2 (Perception Pipeline) is handed out and due Week 7.
- Week 6 covers PDDL, the classical task-level planner that consumes the KR
  and perception output.
