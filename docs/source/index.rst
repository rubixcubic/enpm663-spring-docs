ENPM663: Building AI-Augmented Robotic Systems
==============================================

Course Description
------------------
ENPM663 is a graduate, hands-on course on how modern AI techniques, including
large language models (LLMs) and vision-language models (VLMs), are integrated
into ROS 2 based robotic systems. Students enter with working ROS 2 knowledge
and extend classical task and motion planning with AI-augmented counterparts at
the task-planning layer: LLM agents for task planning (the observe-act-observe
loop, tool use, and structured output), VLM grounding for scene understanding,
and closed-loop replanning. Motion planning, grasp execution, and control remain
classical (MoveIt2); the end-to-end vision-language-action (VLA) frontier is
surveyed for context but not built.

The course is structured around the Agile Robotics for Industrial Automation
Competition (ARIAC) 2025 as a unifying testbed, but the concepts and engineering
patterns taught are general to autonomous robotic systems.

Software Stack
--------------
- Ubuntu 24.04 LTS (Noble Numbat)
- ROS 2 Jazzy Jalisco
- Gazebo Harmonic
- ARIAC 2025 (https://pages.nist.gov/ARIAC_docs/en/latest/)
- Primary language: Python (with selected C++ where it is the industry standard)

Prerequisites
-------------
Working knowledge of ROS 2 (publishers and subscribers, services, actions,
parameters, launch files). Week 1 provides a refresher on the ROS 2 topics most
directly used in the course (lifecycle nodes, TF2, QoS, executors).

Learning Outcomes
-----------------
After successfully completing this course, you will be able to:

- Design system architectures that integrate classical robotic components
  (perception, planning, control) with AI-based components (LLMs, VLMs).
- Apply knowledge-representation techniques (frames, ontologies, hierarchical
  task and world models) consumable by both classical and AI planners.
- Implement behavior trees in ``py_trees_ros`` for robust task execution.
- Apply classical task-level planning using PDDL.
- Build LLM agents for task planning that reason in an observe-act-observe loop
  and invoke robot actions through tool/function calling (MCP).
- Use vision-language models to ground robotic plans in observed scenes.
- Design robust execution patterns (failure handling, recovery, replanning) for
  AI-driven systems where LLM and VLM outputs may be incorrect.
- Plan and execute robot motion using MoveIt2.
- Evaluate AI-augmented robotic systems using quantitative metrics.

All course work is team-based; there are no individual assignments.

.. toctree::
   :hidden:
   :maxdepth: 3
   :titlesonly:

   syllabus/syllabus
   setup/setup
   lectures/index
   assignments/index
   glossary/glossary
   reading_material/index
   changelog/changelog
