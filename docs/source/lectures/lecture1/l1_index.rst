====================================================
Week 1: Course Overview and ROS 2 Refresher
====================================================

Overview
--------

This lecture introduces ENPM663 and refreshes the ROS 2 topics most directly
used throughout the course. We begin with a quick walkthrough of the syllabus,
team structure, and the ARIAC 2025 testbed, then move into a calibration
refresher on lifecycle nodes, TF2, QoS profiles, and ROS 2 executors. The
ungraded diagnostic quiz at the start of class helps both the cohort and the
instructor see where ROS 2 fluency stands.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Describe the structure, expectations, and grading of ENPM663.
   - Explain what ARIAC is and why it serves as the course testbed.
   - Recall ROS 2 publishers/subscribers, services, and actions APIs.
   - Use lifecycle nodes, TF2, QoS profiles, and ROS 2 executors in Python.
   - Identify gaps in your own ROS 2 background using the diagnostic quiz.


Topics
------

- Course logistics: syllabus walkthrough, team-formation timeline, PT1 hand-out.
- ARIAC 2025 overview: kitting and assembly stations, robots, sensors, orders.
- ROS 2 refresher: lifecycle nodes, TF2 transforms, QoS profiles, executors.
- Diagnostic quiz (ungraded): ROS 2 basics from the prerequisite list.


Hands-On Exercise
-----------------

Build and run a minimal ROS 2 Python node that publishes a TF transform and
subscribes to its own publication with a different QoS profile. Verify the
behavior in ``ros2 topic echo``. (TODO: provide starter package.)


ARIAC Tie-in
------------

Open the ARIAC documentation in class and trace one example through the ARIAC
node graph (orders, sensors, robot controllers). The exercise shows how a
small ROS 2 system maps to ARIAC's much larger one.


References
----------

- ROS 2 Jazzy documentation: https://docs.ros.org/en/jazzy/
- ARIAC GitHub: https://github.com/usnistgov/ARIAC
- ARIAC Documentation: https://pages.nist.gov/ARIAC_docs/en/latest/index.html
- TODO: prerequisite ROS 2 reading list.


Next Steps
----------

- PT1 (Behavior Tree for a Simple Kitting Workflow) is handed out today; due Week 5.
- Form your team of 3 before Week 3 (teams are formed in W3 KR lecture).
- Read the assigned ARIAC architecture overview before Week 2.
