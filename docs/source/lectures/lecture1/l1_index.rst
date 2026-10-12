====================================================
L1: Course Overview and ROS 2 Refresher
====================================================

Overview
--------

This lecture introduces ENPM663 and what this course means by agentic
physical AI: an AI agent decides what a robot cell does next, and classical
robot skills carry it out. It walks through the ARIAC 2025 testbed, a
simulated EV battery factory, and how a trial is scored. The second half
refreshes the ROS 2 topics the course uses most: lifecycle nodes, TF2, QoS
profiles and executors. An ungraded diagnostic quiz at the start of class
shows you, and the instructor, where your ROS 2 background stands.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Describe the course structure, the group projects that build up to the final
  demo, and the grading policies.
- Explain what physical AI and agentic AI mean, and which part of an agentic
  robot system this course builds.
- Describe the ARIAC 2025 factory: its two tasks, its robots and sensors, and
  how a trial is scored.
- Recall the ROS 2 Python APIs for publishers, subscribers, services and
  actions.
- Use lifecycle nodes, TF2, QoS profiles and executors in Python.
- Identify gaps in your own ROS 2 background with the diagnostic quiz.


.. admonition:: Materials in progress
   :class: note

   The lecture notes, quiz and references for this lecture are written with
   the slide deck and are not published yet. This page will link to them
   once they are ready. The topics below are the plan.


Planned Topics
--------------

- Course logistics: the syllabus, team formation in L2, the four group
  projects and the final demo.
- Physical AI and agents: what the terms mean, and the modular stack this
  course builds.
- ARIAC 2025: Task 1 (inspection and kit building) and Task 2 (module
  construction); the inspection robots, assembly robots, gantry welder and
  AGVs; sensors bought from a budget; the challenges; how a trial is scored.
- ROS 2 refresher: lifecycle nodes, TF2 transforms, QoS profiles, executors.
- Diagnostic quiz (ungraded): the ROS 2 prerequisites.


ARIAC Tie-in
------------

Trace one battery cell through the factory: the inspection conveyor feeds
it, a voltage tester reads it, your node submits an inspection report, a robot
places it in a kit on an AGV tray, and the AGV takes the kit to shipping. Each
step is a ROS 2 topic, service or action in the ARIAC API.


Starting References
-------------------

- ROS 2 Jazzy documentation: https://docs.ros.org/en/jazzy/
- ARIAC GitHub: https://github.com/usnistgov/ARIAC
- ARIAC documentation: https://pages.nist.gov/ARIAC_docs/en/latest/index.html
- NVIDIA glossary, physical AI: https://www.nvidia.com/en-us/glossary/generative-physical-ai/


Next Steps
----------

- Read the ROS 2 Refresher pre-read before this class (see :doc:`Pre-Read
  </preread/index>`).
- Install Ubuntu 24.04, ROS 2 Jazzy and ARIAC 2025 with the :doc:`ARIAC
  Testbed </ariac/ariac>` pages. You need them for GP1, posted in L2.
- Find two teammates: teams are formed in L2.
- In the next lecture, we will cover **system architectures**: where AI
  components plug into a classical robot stack.
