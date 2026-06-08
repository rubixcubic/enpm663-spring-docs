====================================================
Week 11: Frames, Transforms, and Motion Planning
====================================================

Overview
--------

This lecture covers the motion layer of the three-layer architecture: TF2
in depth, MoveIt2 architecture, the motion planning pipeline (sampling,
collision checking, trajectory optimization), and parameterized grasps. By
the end of class, students can ask MoveIt2 to plan a pick-and-place
trajectory and understand what each stage of the pipeline contributed.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Build and reason about a TF2 frame chain for an ARIAC-style scene.
   - Describe the MoveIt2 architecture: move_group, planning scene, planners.
   - Plan a motion in MoveIt2 from Python using the MoveIt2 Python API.
   - Specify grasp poses as parameterized targets (no learned grasp model).
   - Reason about collision objects, octomaps, and execution monitoring.


Topics
------

- TF2 deep dive: static vs. dynamic transforms, frame conventions,
  troubleshooting (lookup failures, time inconsistencies).
- MoveIt2 architecture: move_group node, planning scene, planning pipeline,
  controllers.
- Sampling-based planners (RRT-Connect, PRM); when each is appropriate.
- Trajectory optimization (CHOMP, STOMP) at a high level.
- Parameterized grasps: defining a grasp pose relative to a part frame.


Hands-On Exercise
-----------------

Using a provided MoveIt2 scene (TODO: starter), plan (do not execute) a
pick motion to a part at a given pose. Inspect the resulting trajectory in
RViz; vary the planner and compare. Add a collision object and re-plan.


ARIAC Tie-in
------------

ARIAC uses MoveIt2 for the kitting robot's pick-and-place. PT4 and PT5 both
call MoveIt2 as the reactive layer beneath the LLM-driven executor. The
grasp poses for ARIAC parts are parameterized (no learned grasp prediction),
defined per part type.


References
----------

- MoveIt2 documentation: https://moveit.picknik.ai/main/
- ROS 2 TF2 tutorials: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/
- ARIAC robot configurations: TODO link into ARIAC docs.
- ARIAC GitHub: https://github.com/usnistgov/ARIAC


Next Steps
----------

- Week 12 covers recovery and robustness for AI-driven systems; Quiz #5.
- Continue PT4; due Week 13.
