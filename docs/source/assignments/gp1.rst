====================================================
GP1: Behavior Tree for One Kit
====================================================

.. card:: GP1: At a Glance
   :class-card: sd-shadow-sm

   .. list-table::
      :widths: 30 70
      :class: compact-table

      * - **Duration**
        - 3 weeks (Week 2 to Week 5), posted 02/03, due 02/24
      * - **Weight**
        - 10% of the course grade
      * - **Lectures**
        - L1 to L4
      * - **Team Size**
        - 3 students
      * - **Submission**
        - Canvas + GitHub repository link


.. admonition:: Specification in progress
   :class: note

   This page is the plan for GP1. The full specification (provided code,
   folder structure, submission checklist and grading rubric) is added
   before it is posted.


.. admonition:: AI tools
   :class: warning

   You may use AI tools to clarify concepts or look up syntax. Your team is
   responsible for every line you submit, and any member may be asked to
   explain any part of it. Read :ref:`ai-disclosure` for the full rules.


Overview
--------

GP1 builds the behavior tree that every later project extends. Your tree
builds one kit in the ARIAC 2025 factory: it feeds cells onto the inspection
conveyor, submits a passing inspection report for each cell, reads their
voltages, recycles the cells outside the voltage range, places four cells on
an AGV tray, moves the AGV to shipping and submits the kit. No defect
detection yet: GP2 adds it.

.. important::

   A cell reaches the inspection robot only if your team has submitted a
   passing inspection report for it. A cell with no report is pushed into the
   inspection bin. In GP1, with no defect detection, every report says the
   cell passed.

GP1 comes with a starter tree. Spend Weeks 2 and 3 on setup, the skills
package and the ARIAC services; write the tree after L4 (Week 4).


Learning Objectives
-------------------

- Structure a behavior tree with sequences, selectors and decorators, and justify each choice.
- Write ``py_trees_ros`` leaves that call ROS 2 actions and services.
- Share state between leaves through the blackboard.
- Run an ARIAC 2025 trial and submit a kit.


Provided Resources
------------------

- The course skills package (pick and place for the robot arms), built on MoveIt 2.
- A starter ROS 2 package with a launch file for the trial, and a starter
  ``py_trees_ros`` tree that you extend after L4.
- The ARIAC 2025 example team configuration.


Tasks
-----

- Submit a passing inspection report for each cell before it reaches the inspection door.
- Read the voltage of each fed cell and decide whether it can go in a kit.
- Place four acceptable cells on an AGV tray with the skills package.
- Move the AGV to shipping with ARIAC's AGV move action and submit the kit.
- Handle a skill that fails once (retry) and one that keeps failing (stop cleanly).


Deliverables
------------

- A ROS 2 package with a launchable behavior tree.
- A short write-up (1 to 2 pages) with the tree diagram and the reason for each composite choice.
