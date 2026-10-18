====================================================
L7: Plan Execution Patterns with Behavior Trees
====================================================

Overview
--------

**L6 gave you a plan. This lecture runs it.**

A PDDL plan is a list of **ground actions**: an action name and its
arguments, such as ``(pick-from-tester inspection_robot_2 c3 tester1)``. The
planner does not move a robot. A behavior tree does, and in GP3 the tree is no
longer written by hand: your code builds it from each new plan. The question of
the lecture is how a behavior tree runs a plan that it did not write, and what
it does when the plan stops matching the factory.

The lecture starts with the **plan-to-BT factory**: a **registry** that maps
each action name to a **builder**, a function that returns one subtree for one
plan step. Every subtree follows the same pattern, **guard, act, verify,
update**: check the preconditions on the blackboard, send the goal, check that
the effect happened, then write the effects. A five-step plan becomes a tree,
and its tick trace shows each step handing over to the next.

Next come two decorators. **Retry** runs a step again after it fails, so it
tolerates a failed attempt; **Timeout** fails a step that runs too long, so it
turns a stalled attempt into a failure. Each one has an
ARIAC 2025 case (the vacuum tool malfunction and the voltage tester
malfunction), and a measured demo shows that the order in which you nest them
changes how long a step can take.

The lecture then sorts failures into four responses (**retry, wait, replan,
stop**) and walks through the **replanning loop**: detect a trigger, stop at a
safe point, write a new problem, plan again and swap in the new tree. A traced
replan recycles a cell whose voltage is out of range and still ships a kit
inside the voltage window.

The last two sections show how to read **BehaviorTree.CPP**, the C++ behavior
tree library used in industry (Nav2 builds on it), next to the same tree in
``py_trees``, and how to debug a running tree from its tick trace.

.. important::

   **ARIAC tie-in.** Every example uses Task 1: inspection robot 2 picks
   tested cells from the voltage testers, places them in the slots of AGV 1,
   and the AGV goes to shipping. The failure cases are the ARIAC 2025
   challenges and Task 1 events: a cell that fails inspection, a voltage out
   of range, a kit window that closes, a tester that malfunctions and a
   high-priority order.

.. important::

   **Group project.** GP3 (PDDL Planner and BT Executor) is posted today and
   is due in Week 10, on March 31. It combines L6 and L7: a PDDL domain for
   Task 1, a problem generator, a selection step for the kit voltages, and a
   plan-to-BT executor with retry and timeout decorators around each skill,
   and replanning triggers. GP3 spans spring break.

.. admonition:: This week
   :class: warning

   - **Quiz 3** (L5 and L6) opens the class.
   - **GP2 is due** today. Rate each teammate in the GP2 peer review on
     ELMS-Canvas.
   - **GP3 is posted** today.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Implement a plan-to-BT factory that builds one ``py_trees`` subtree per
  plan action from the action's name and arguments.
- Explain the guard, act, verify pattern for a plan step and how it keeps the
  blackboard consistent with the factory.
- Apply Retry to tolerate a failed attempt and Timeout to turn a stalled
  attempt into a failure, and explain how their nesting order changes their
  behavior.
- Classify an execution failure as retry, wait, replan or stop, using the
  ARIAC 2025 challenges and Task 1 events as cases.
- Describe the replanning loop: detect a trigger, stop at a safe point, write
  a new problem, plan again and swap in the new tree.
- Read a BehaviorTree.CPP XML tree and a C++ node, and map each element to its
  ``py_trees`` counterpart.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l7_lecture
   l7_code
   l7_exercises
   l7_quiz
   l7_references


Next Steps
----------

- **Spring break** is March 14 to 21. There is no class on March 17.
- In the next lecture we cover **L8: LLM Agents I: Agent Loops, Tool Use, and
  Structured Output** (Wednesday, March 24):

  - An LLM agent replaces the planner and calls the same executor.
  - The executor you write for GP3 carries over unchanged.

- **Before next class:**

  - Rate each teammate in the GP2 peer review on ELMS-Canvas.
  - Read the LLM Prompting and Structured Output pre-read and the Model
    Context Protocol (MCP) pre-read.
  - Run ``lecture7/code/run_all.sh`` (see :doc:`l7_code`) and compare your
    outputs with the ones in the notes. The timing numbers differ a little
    from run to run.
  - Work through the :doc:`L7 exercises <l7_exercises>` and the
    :doc:`self-check quiz <l7_quiz>`.
  - Start GP3 before the break. A team that does not start before the break
    has about one working week after it.
