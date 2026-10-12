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


.. admonition:: Specification in progress
   :class: note

   This page is the plan for GP3. The full specification (provided code,
   folder structure, submission checklist and grading rubric) is added
   before it is posted.


.. admonition:: AI tools
   :class: warning

   You may use AI tools to clarify concepts or look up syntax. Your team is
   responsible for every line you submit, and any member may be asked to
   explain any part of it. Read :ref:`ai-disclosure` for the full rules.


Overview
--------

GP3 replaces the fixed order of GP1 with a plan. Your team writes a PDDL
domain for Task 1, with the two inspection robots and the AGVs, and runs its
plans through a behavior tree built from the plan. When a cell fails
inspection, the executor stops and asks for a new plan. Choosing four cells
that meet the kit voltage tolerance is a numeric problem, so it is a separate
selection step whose result goes into the PDDL problem.


Learning Objectives
-------------------

- Write a PDDL domain and problem for a factory task.
- Run a planner from Python and check the plan.
- Build a plan-to-BT executor with retry and replanning triggers.
- Explain what PDDL captures well and where it strains.


Provided Resources
------------------

- Your team's GP2 package.
- The Unified Planning Framework or Fast Downward.


Tasks
-----

- Write the domain and generate the problem from the trial state.
- Select cells that meet the kit voltage tolerance.
- Execute plans through the plan-to-BT executor.
- Replan when a cell fails inspection, and show it on at least one trial.


Deliverables
------------

- The PDDL files, the planner integration and the executor.
- A demo on two or three trials, one of which triggers a replan.
- A short reflection on what PDDL captured well and where it strained.
