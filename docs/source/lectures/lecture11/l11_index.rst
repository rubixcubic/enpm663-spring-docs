=====================================================================
L11: Recovery, Robustness, and Failure Handling for AI-Driven Systems
=====================================================================

Overview
--------

**What does the system do when something goes wrong, and which layer
handles it?** This lecture answers that question for the system you build
from GP1 to GP4.

The lecture sorts failures into four types: an **action failure** (a skill
does not do what it was asked), a **sensor failure** (a device gives no data
or wrong data), a **plan failure** (the plan is invalid) and **world drift**
(the world changed, and no single action failed). Each type has a signal
that detects it in the ARIAC 2025 interfaces, and the type decides where
recovery starts. AI components add two new sources of failure: LLM output,
which shows up as plan failures, and VLM output, which shows up as sensor
failures.

The recovery tools come next, at three levels:

- **The behavior tree.** A selector falls back to another branch, Retry runs
  a failed skill again, Timeout turns a hang into a failure, and a guard
  stops a running branch when a device breaks. A demonstration in
  ``py_trees`` 2.6.0 injects failures into a tree that places a cell on a
  voltage tester, with no simulator.
- **Checks on AI output.** Five layers of checks stop a bad LLM reply before
  it reaches a robot, cheapest first. A VLM error passes a schema check, so
  it needs a second source instead.
- **Equipment.** The ARIAC docs say a malfunctioning voltage tester stops
  publishing. The ARIAC code keeps publishing voltage -1 with status
  ``MALFUNCTIONING``. A watcher with four rules handles both.

The lecture then treats each ARIAC 2025 challenge as a failure scenario and
ends with the rule for choosing **local recovery** (retry in the tree) or
**global recovery** (a new plan from the planner or agent), worked on three
examples.

.. important::

   **ARIAC tie-in.** The final demo runs an ARIAC trial that no team has
   seen, and any of the four challenges can occur in it: the conveyor
   malfunction, the voltage tester malfunction, the vacuum tool malfunction
   and high-priority orders. Defective cells are in every trial. You cannot
   tune your system for a known order of challenges, so detection and
   recovery must work for any order.

.. important::

   **Group project.** GP4 (LLM agent with VLM grounding) is due on
   Wednesday, April 21. Add the checks and the challenge handling from this
   lecture, and log every detection and recovery. GP4 tests the conveyor
   malfunction, the voltage tester malfunction and high-priority orders. The
   vacuum tool malfunction happens only in Task 2, so the final demo is the
   first place your system meets it.

.. admonition:: This week
   :class: warning

   - **Quiz 5** (L9 and L10, 20 minutes, closed notes) opens the class. It
     is the last quiz of the course.
   - **The final demo specification is posted** on ELMS-Canvas and the
     course site. The demo is in Week 15 (05/05) and is 20% of the course
     grade. The grading rubric, the code-freeze date and the
     embodied-reasoning model are to be announced.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Classify a failure as an action failure, a sensor failure, a plan failure
  or world drift, and name the signal that detects it in the ARIAC 2025
  interfaces.
- Build behavior tree recovery with ``py_trees``: selectors, the Retry and
  Timeout decorators, and guards that stop the active branch.
- Check LLM output before it reaches a robot: the schema, tools that do not
  exist, and objects that are not in the world state.
- Cross-check VLM output against a second source.
- Handle equipment that stops giving valid readings with status checks,
  value checks, a time limit and degraded operation.
- Choose local or global recovery for each ARIAC 2025 challenge, and give
  the reason.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l11_lecture
   l11_code
   l11_exercises
   l11_quiz
   l11_references


Next Steps
----------

- In the next lecture we cover **L12: Evaluation and Measurement Science
  for AI-Augmented Systems**:

  - How to measure an agentic system with the ARIAC scoring formula.
  - Recovery rate, challenge handling, and how the ARIAC score rewards or
    penalizes each recovery choice.

- **GP4 is due Wednesday, April 21.** Add the checks and the challenge
  handling from today, and log every detection and recovery.

- **Before L12:**

  - Read the final demo specification as a team, and list your questions
    for L13.
  - Start your **challenge test matrix**: each challenge, alone and
    combined, on several trial configurations, each run more than once.
  - Run the four L11 scripts (see :doc:`l11_code`) and compare your outputs
    with the ones in the notes.
  - Work through the :doc:`L11 exercises <l11_exercises>` and the
    :doc:`self-check quiz <l11_quiz>` (ungraded).
