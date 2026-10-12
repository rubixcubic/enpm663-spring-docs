====================================================
L6: Task-Level Planning with PDDL
====================================================

Overview
--------

This lecture introduces classical task planning with PDDL (Planning Domain
Definition Language). A PDDL domain lists predicates and actions; a problem
gives the initial state and the goal; a planner such as Fast Downward or the
Unified Planning Framework finds the sequence of actions. PDDL is also a
knowledge representation (L3), and it is the classical baseline that GP4's
LLM agent is compared against.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Write a PDDL domain with types, predicates and parameterized actions with
  preconditions and effects.
- Write a PDDL problem with an initial state and a goal.
- Run a planner (Fast Downward or the Unified Planning Framework) from Python.
- Inspect a plan and check that it is valid.
- Recognize what PDDL captures well (logical structure) and where it strains
  (numbers, partial observability).


.. admonition:: Materials in progress
   :class: note

   The lecture notes, quiz and references for this lecture are written with
   the slide deck and are not published yet. This page will link to them
   once they are ready. The topics below are the plan.


Planned Topics
--------------

- PDDL syntax: domain, problem, types, predicates, parameterized actions,
  preconditions and effects.
- Planners: Fast Downward and the Unified Planning Framework.
- Running a planner from Python; reading the plan.
- PDDL as a knowledge representation: how it relates to frames and ontologies
  (L3).
- Where PDDL strains: numeric state (a kit's total voltage), partial
  observability, large numbers of objects.


ARIAC Tie-in
------------

GP3 writes a PDDL domain for Task 1: cells, the inspection robots, the
voltage testers, kit trays on the AGVs, and the shipping station. Choosing
four cells whose voltages meet the kit tolerance is a numeric problem, so GP3
solves it in a separate selection step and gives PDDL the result.


Starting References
-------------------

- Fast Downward: https://www.fast-downward.org/
- Unified Planning Framework: https://unified-planning.readthedocs.io/
- ARIAC GitHub: https://github.com/usnistgov/ARIAC
- ARIAC documentation: https://pages.nist.gov/ARIAC_docs/en/latest/index.html


Next Steps
----------

- Read the PDDL Primer pre-read before this class (see :doc:`Pre-Read
  </preread/index>`).
- GP2 is due in Week 7.
- In the next lecture, we will cover **plan execution with behavior trees**:
  running today's plans and replanning on failure.
