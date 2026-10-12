====================================================
L10: Frames, Transforms, and Motion Planning
====================================================

Overview
--------

Since GP1 you have moved the ARIAC robots by calling the course skills
package. This lecture opens that layer: how a skill goal becomes a robot
motion, and how each step can fail.

It starts with **TF2**, the ROS 2 library that tracks coordinate frames. The
transform from an AGV to its tray slot never changes, while the transform from
the world to the AGV changes every time the AGV drives. A skill must look up a
slot when its goal arrives: a pose cached at the inspection station is
4.229 m off once the AGV is at the assembly station. Three short scripts show
the lookup, and the three ways a lookup fails.

Next comes the **pinhole camera model**, which turns a camera pixel into a
point on a known plane. In Task 2 the top shell lands at a random pose on the
assembly table, and your camera must find it. A worked example takes one pixel
of a 720p camera 1.0 m above the table to a point 0.10 m from the spot under
the camera, by hand and then with TF2.

The second half covers **MoveIt 2**: its parts, its planning pipeline, and the
configurations the ARIAC example team ships. It compares the sampling-based
planners (RRT-Connect, PRM, RRTstar) with the **Pilz industrial motion
planner**, using a small RRT-Connect toy that finds five different paths for
the same start and goal. It then defines a **parameterized grasp** and works
out where a cell on the moving inspection conveyor will be when the arm
arrives. It ends inside the course skills package: one goal traced from call
to result, the failure results, and why a skill reports a failure instead of
retrying.

.. important::

   **ARIAC tie-in.** ARIAC 2025 gives each robot a joint trajectory action and
   a gripper action, plus vacuum tool services on assembly robot 2. It has no
   pick, place or move-to-pose service, and it publishes no frame for a cell or
   a shell. The course skills package fills the first gap; your sensors fill
   the second. Task 2 motion (placing cells, placing the top shell, the six
   welds) appears here for the first time, ahead of the final demo.

.. important::

   **Group project.** GP4 (LLM agent with VLM grounding) is in progress and is
   due in Week 13. Its agent calls the skills as tools, so its tool
   descriptions should name each skill's preconditions and failure results.
   This lecture lists both.

.. admonition:: This week
   :class: warning

   - No quiz and no deliverable.
   - **Quiz 5**, at the start of next class, covers L9 and L10.

.. note::

   **The course skills package is still being built.** These pages describe it
   by role, from its design: what it is planned to do, not released code. Its
   action names and fields will be on its documentation page when it is
   published.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Build a TF2 frame chain from the world frame to an AGV tray slot, and
  explain which transforms are static and which change as the AGV moves.
- Compute the world position of an image pixel on a known plane with the
  pinhole camera model, the camera intrinsics and TF2, and explain how it
  becomes a robot target.
- Describe the MoveIt 2 architecture: ``move_group``, the planning scene, the
  planning pipeline and the trajectory controllers, and where MoveItPy fits.
- Compare RRT-Connect, PRM and the Pilz industrial motion planner, and choose
  one for a given ARIAC motion.
- Compute a grasp target as a fixed offset from a part frame, including the
  predicted position of a cell on the moving inspection conveyor.
- Explain how the course skills package turns a skill goal into a trajectory
  and a gripper command, and why it reports failures instead of retrying
  them.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l10_lecture
   l10_code
   l10_exercises
   l10_quiz
   l10_references


Next Steps
----------

- In the next lecture we cover **L11: Recovery, Robustness, and Failure
  Handling for AI-Driven Systems**: what your tree and your agent do with
  today's failure results. The final demo specification is posted.

- **Quiz 5** (Wednesday, April 14, start of class) covers L9 and L10. From
  L10: static and moving frames; the pinhole model and the pixel-to-table
  steps; the MoveIt 2 parts; RRT-Connect, PRM and Pilz; the conveyor example;
  the skill failure results.

- **Before next class:**

  - GP4 (due Week 13): write tool descriptions that list each skill's
    preconditions and failure results.
  - Read the course skills package documentation page when it is published.
  - Run the L10 scripts (see :doc:`l10_code`) and compare your outputs with
    the ones in the notes. Optional: the example team's Move Robots demo.
  - Work through the :doc:`L10 exercises <l10_exercises>` and the
    :doc:`self-check quiz <l10_quiz>`.
