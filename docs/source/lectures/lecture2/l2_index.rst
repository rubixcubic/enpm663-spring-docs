====================================================
L2: System Architectures for Agentic Robotics
====================================================

Overview
--------

A robot's **architecture** says how its software is split into parts, and
how the parts pass decisions and data to each other. This lecture gives you
the architecture vocabulary that the rest of the course uses.

It starts with four classical architectures: **sense-plan-act**,
**reactive**, **subsumption** and the **three-layer architecture**. Each one
strikes a different balance between planning and reacting. The three-layer
architecture is the frame for the whole semester: a **deliberative** layer
plans, an **executive** layer runs the plan step by step and checks every
result, and a **reactive** layer controls the hardware.

A toy factory, written in plain Python, then runs one short Task 1 run under
three architectures while a voltage tester malfunctions. A fixed plan
recycles good cells and ships a kit whose total voltage is too high. Pure
reaction ships a kit that is also too high. Only the three layers ship a kit
inside the window, and a sweep over 1000 runs shows that this is not luck.
The same run is then told step by step: which layer sees the malfunction,
which layer handles it, and what moves up.

The lecture then finds the same pattern in real robot software (Nav2 and
MoveIt), shows where an **LLM agent** and a **VLM** plug into the stack, and
maps ARIAC 2025, the course skills package and every group project onto the
three layers. It closes with the end-to-end alternative,
**vision-language-action (VLA)** models, with multi-robot coordination, and
with GP1 and team formation.

.. important::

   **ARIAC tie-in.** ARIAC 2025 gives you the reactive layer: each robot's
   joint trajectory and gripper actions, the AGV move actions, the conveyor
   and feed services, the sensors and the submission services. The course
   skills package turns the arm interfaces into skills such as picking a
   cell. Your team builds the executive (the GP1 behavior tree) and the
   deliberative layer (the GP3 planner, then the GP4 agent).

.. important::

   **Group project.** GP1, a ``py_trees_ros`` behavior tree that builds one
   kit, is posted in this lecture and is due on 02/24. The behavior tree is
   the executive layer of your stack. Teams form today.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Compare the classical robot architectures by how they trade planning
  against reaction time.
- Describe the three-layer architecture and the goals and status that flow
  between its layers.
- Explain, from a toy factory run, why a fixed plan or pure reaction alone
  does not finish a Task 1 kit.
- Trace one voltage tester malfunction through the three layers: which layer
  sees it, which handles it, and what moves up.
- Recognize the three-layer pattern in real robot software (Nav2 and MoveIt).
- Identify where an LLM agent and a VLM plug into a robot architecture, and
  which parts stay classical.
- Map the ARIAC 2025 interfaces, the course skills package and each group
  project onto the three layers.
- Explain the end-to-end VLA alternative and weigh its tradeoffs against the
  modular stack.
- Describe the GP1 task, its deliverables and the team rules.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l2_lecture
   l2_code
   l2_exercises
   l2_quiz
   l2_references


Next Steps
----------

- In the next lecture we cover **L3: Knowledge Representation for
  Agentic Robotics** (Wednesday, February 10):

  - Frames and an ontology for ARIAC cells, kits, modules and AGVs.
  - A world model at each layer, and status that moves up (two ideas from
    4D/RCS).
  - One kit written three ways: PDDL facts, a JSON record checked by a JSON
    schema, and text.

- **Before next class:**

  - Form your team, submit the roster on Canvas, and post the team charter
    on ELMS.
  - Get the starter package and the skills package running in the ARIAC
    trial.
  - Try the toy factory at home (optional, not graded). The commands are on
    the :doc:`code page <l2_code>`.
  - Work through the :doc:`L2 exercises <l2_exercises>` and the
    :doc:`self-check quiz <l2_quiz>`.
