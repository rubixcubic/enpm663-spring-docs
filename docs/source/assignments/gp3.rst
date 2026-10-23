====================================================
GP3: PDDL Planner and BT Executor
====================================================

.. card:: GP3: At a Glance
   :class-card: sd-shadow-sm

   .. list-table::
      :widths: 30 70
      :class: compact-table

      * - **Duration**
        - 3 weeks (Week 7 to Week 10, over spring break), posted 03/10, due 03/31
      * - **Weight**
        - 10% of the course grade
      * - **Lectures**
        - L6 and L7
      * - **Team Size**
        - 3 students
      * - **Submission**
        - Canvas + GitHub repository link


.. admonition:: Specification draft
   :class: note

   This page is the specification draft for GP3. The provided code (the
   course skills package, as in GP1 and GP2) and the GP3 trial
   configurations are released with the project, on the day GP3 is posted.


.. admonition:: AI tools
   :class: warning

   You may use AI tools to clarify concepts or look up syntax. Your team is
   responsible for every line you submit, and any member may be asked to
   explain any part of it. Read :ref:`ai-disclosure` for the full rules.


Overview
--------

GP3 replaces the fixed order of the GP1 tree with a plan. **PDDL**
(Planning Domain Definition Language) describes a task as predicates and
actions. A **predicate** is a fact that is true or false, such as "AGV 1 is
at the inspection station". Each action has preconditions (facts that must
hold before it) and effects (facts it makes true or false). A planner, such
as Fast Downward, finds a sequence of actions that reaches the goal. The
Unified Planning Framework (UPF) is a Python library that calls planners
such as Fast Downward (L6).

Your team writes a PDDL domain for ARIAC Task 1, with the two inspection
robots, the voltage testers, the tray slots on the AGVs and the shipping
station. Your code builds the PDDL problem from the trial's current state,
runs the planner, and turns the plan into a behavior tree with one subtree
per action. This **plan-to-BT executor** is the part that carries over: in
GP4 it runs the LLM agent's decisions.

Why a separate selection step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Choosing four cells whose total voltage lands within the kit limit is a
numeric problem. Classical PDDL, the form L6 teaches, describes facts that
are true or false, not sums of numbers. So a separate selection step in
Python makes that choice, and its result goes into the PDDL problem as
facts.

When a queued cell fails inspection, or the world no longer matches the plan, the
executor stops and asks for a new plan from the updated state. GP3 spans
spring break (Week 8). Lectures L6 and L7 cover what GP3 needs.


Learning Objectives
-------------------

After completing GP3, you will be able to:

- Write a PDDL domain and problem for ARIAC Task 1.
- Generate the PDDL problem from the trial state at run time.
- Write a cell selection step that meets the kit voltage limit.
- Run a planner from Python and check the plan before running it.
- Build a plan-to-BT executor with retry, timeout and replanning triggers.
- Explain what PDDL modeled well in Task 1 and what was hard to model.


Provided Resources
------------------

.. list-table::
   :widths: 32 68
   :header-rows: 1
   :class: compact-table

   * - Resource
     - What it gives you
   * - Your team's GP2 package
     - The tree, the perception node and the per-cell records.
   * - A planner
     - Fast Downward, run directly or through the Unified Planning
       Framework. Your team chooses.
   * - Course skills package and ARIAC 2025 Task 1 interfaces
     - As in GP1 and GP2.
   * - GP3 trial configurations
     - Trials with defective cells.

GP3 does not model the ARIAC challenges in PDDL. GP4 handles them with an
LLM agent.


Tasks
-----

.. dropdown:: Task 1: Write the domain
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** a PDDL domain that describes Task 1.

   **Requirements:**

   - **Types:** cell, robot, tester, AGV, slot, station.
   - **Predicates:** where each cell is, what each robot holds, which slots
     are empty, where each AGV is, which cells passed inspection and which
     have a voltage in range.
   - **Actions:** for both inspection robots, the AGV moves and the kit
     submission. Each action's preconditions and effects match what the
     robot or the ARIAC service does.

.. dropdown:: Task 2: Generate the problem from the trial state
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** a PDDL problem that matches the factory at the moment you plan.

   **Requirements:**

   - Write a generator that builds the problem from the trial state: the
     cells known so far, the testers, the AGV stations and the empty slots.
   - Write each problem to a file, so the grader can read it.

.. dropdown:: Task 3: Write the selection step
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** four cells whose total lands inside the kit limit.

   **Requirements:**

   - From the averaged voltages, choose cells so that the four-cell total
     is within 4 × nominal ± 0.15 V. For Li-Ion (3.6 V nominal) that is
     4 × 3.6 = 14.4 V, so 14.25 V to 14.55 V.
   - Give the choice to the problem as facts.
   - Test the selection step on its own, with voltages you choose.

.. dropdown:: Task 4: Run the planner and check the plan
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** run only plans you have checked.

   **Requirements:**

   - Run the planner from Python.
   - Check the plan before you run it. For example, apply each action's
     effects to the state in order, and confirm the goal holds at the end.
   - Log each plan and the result of its check.

.. dropdown:: Task 5: Build the plan-to-BT executor
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** a behavior tree built from the plan, one subtree per action.

   **Requirements:**

   - Look up each plan action's subtree by the action's name, and pass the
     action's arguments as its inputs.
   - Put retry and timeout decorators around each skill.
   - Print the tree built for one plan, for the write-up and the grader.

.. dropdown:: Task 6: Add replanning triggers
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** a new plan when the world no longer matches the old one.

   **Requirements:**

   - Trigger a new plan on: a queued cell fails inspection, a voltage outside
     the cell range, or a skill that still fails after its retries.
   - On a trigger: stop the plan, update the state, and plan again.
   - Log the trigger and the new plan.

.. dropdown:: Task 7: Run two or three trials
   :icon: gear
   :class-container: sd-border-primary

   **Goal:** evidence that the system works on more than one trial.

   **Requirements:**

   - Run two or three trials, one of which triggers a replan.
   - Keep each trial configuration, a screen recording or log of each run,
     and the ARIAC run results.


Suggested Schedule
------------------

GP3 runs from 03/10 to 03/31, and Week 8 (03/17) is spring break. A team
that does not start before the break has about one working week after it.

.. list-table::
   :widths: 22 78
   :header-rows: 1
   :class: compact-table

   * - Week
     - Work
   * - Week 7 (from 03/10)
     - Tasks 1 to 3: the domain, the problem generator and the selection
       step, tested without the simulator.
   * - Week 8 (spring break)
     - Your team decides. Agree on it before the break.
   * - Week 9 (from 03/24)
     - Tasks 4 to 6: the planner, the executor and the replanning triggers,
       on ARIAC trials.
   * - Week 10 (03/31)
     - Task 7, the reflection, final check.


Deliverables
------------

1. The PDDL domain file, the problem generator, the planner integration and
   the executor in your team's repository. Submit the link on Canvas.
2. A demonstration on two or three trials, one of which triggers a replan:
   the trial configurations, a screen recording or log of each run, and the
   ARIAC run results.
3. A short reflection (1 to 2 pages) on what PDDL modeled well in Task 1 and
   what was hard to model.
4. The honor pledge, signed by every team member.


Submission Checklist
--------------------

.. admonition:: Before submitting, check every item
   :class: tip

   - [ ] The planner runs on the domain and on each problem file you
         submit.
   - [ ] The log shows each plan and the result of its check before it ran.
   - [ ] Every submitted kit total is inside 14.25 V to 14.55 V.
   - [ ] The printed tree has one subtree per plan action, with retry and
         timeout around each skill.
   - [ ] One run shows a trigger, the new plan, and an accepted kit after
         it.
   - [ ] The reflection names at least two things PDDL modeled well and
         two things that were hard to model, each with a Task 1 example.
   - [ ] Every team member signed the honor pledge.
   - [ ] Each member fills in the peer-review form after the deadline (see
         :ref:`peer-evaluation`).


Grading Rubric (Draft)
----------------------

.. admonition:: Draft rubric
   :class: note

   This rubric is a draft. It may change before GP3 is posted. The total is
   100 points, scaled to 10% of the course grade.

.. list-table::
   :widths: 26 10 64
   :header-rows: 1
   :class: compact-table

   * - Criterion
     - Points
     - How the grader checks it
   * - PDDL domain
     - 20
     - The grader runs the team's planner on the domain and the team's
       problem files, and reads the domain: both inspection robots, the
       testers, the slots, the AGV moves and the submission are modeled,
       and each action's preconditions and effects match what the robot
       does.
   * - Problem generation
     - 10
     - The grader runs the generator during a grader trial and reads the
       problem file it writes: objects and initial facts match the trial.
   * - Cell selection step
     - 10
     - The grader reads the selection code and its tests, and checks in the
       run results that every submitted kit total is inside
       4 × nominal ± 0.15 V.
   * - Planner integration and plan check
     - 10
     - The log shows each plan and the result of the check before
       execution; the grader reads the check code.
   * - Plan-to-BT executor
     - 15
     - The grader reads the executor and the printed tree for one plan: one
       subtree per action, built from the action name and arguments, with
       retry and timeout around each skill.
   * - Replanning
     - 15
     - The grader runs a trial with defective cells: the log shows the
       trigger, the new plan, and the kit submitted and accepted afterwards.
   * - Demonstration on two or three trials
     - 10
     - The grader reads the submitted trial configurations, logs and ARIAC
       run results; one run shows a replan.
   * - Reflection
     - 10
     - The grader reads the reflection: at least two things PDDL modeled
       well and two things that were hard to model, each tied to a Task 1
       example.

The points add up to 20 + 10 + 10 + 10 + 15 + 15 + 10 + 10 = 100.


Common Mistakes
---------------

.. danger::

   - **Voltages inside the PDDL problem as numbers.** Classical PDDL works
     with true or false facts. Choose the cells in Python and pass the
     choice as facts.
   - **Running an unchecked plan.** A plan that does not reach the goal
     moves robots for nothing. Check it first.
   - **One executor per plan.** Build the subtrees from the action name and
     arguments, so any plan (and in GP4, any agent decision) runs through
     the same code.
   - **Replanning from the old state.** Update the state from the factory
     before you plan again.


Tips for Success
----------------

.. tip::

   **Design the action names once.** The GP4 agent emits the same action
   names and arguments, and the same executor runs them. A clear action
   vocabulary in Task 1 saves work in GP4.

.. tip::

   **Test the domain without the simulator.** Write a problem by hand and
   run the planner on it before you connect the generator to ARIAC.
