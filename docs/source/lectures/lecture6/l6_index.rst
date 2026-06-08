====================================================
Week 6: Task-Level Planning with PDDL
====================================================

Overview
--------

This lecture introduces classical task-level planning using PDDL (Planning
Domain Definition Language). PDDL is the durable, decades-old formalism for
describing planning problems symbolically: a domain (predicates and actions)
and a problem (initial state and goal). We run plans through Fast Downward
or the Unified Planning Framework and inspect the resulting action
sequences. PDDL is also a knowledge-representation formalism (see W3), the
classical baseline that PT4's LLM planner will be compared against.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Write a PDDL domain with typed objects, predicates, and parameterized
     actions including preconditions and effects.
   - Write a PDDL problem with an initial state and a goal.
   - Run a planner (Fast Downward or Unified Planning Framework) from Python.
   - Inspect a plan and reason about its validity.
   - Recognize what PDDL captures well (logical structure) vs. where it
     strains (numerical reasoning, partial observability).


Topics
------

- PDDL syntax: domain, problem, types, predicates, parameterized actions,
  precondition/effect.
- Planner backends: Fast Downward (research-grade), Unified Planning
  Framework (Python-first).
- Running a planner from Python; parsing the plan output.
- PDDL as KR: relationship to frames and ontologies (W3).
- Where PDDL strains: numerical state, partial observability, large object
  sets.


Hands-On Exercise
-----------------

Write a 4-line PDDL domain for a 3-block stacking world (predicates: on,
clear, holding; actions: pickup, putdown, stack, unstack). Write a problem
that requires a 3-step plan. Run the planner in class and inspect the output.


ARIAC Tie-in
------------

PT3 (next two weeks) extends today's toy domain to a multi-part ARIAC
kitting domain: parts in bins, slots in kits, place-part actions with
preconditions on slot availability. ARIAC's order interface produces the
goal.


References
----------

- Fast Downward: https://www.fast-downward.org/
- Unified Planning Framework: https://unified-planning.readthedocs.io/
- PDDL primer: TODO link.
- ARIAC GitHub: https://github.com/usnistgov/ARIAC
- ARIAC Documentation: https://pages.nist.gov/ARIAC_docs/en/latest/index.html


Next Steps
----------

- Week 7 covers plan execution patterns: how to take today's PDDL plans and
  execute them via a BT, with re-planning on failure.
- PT2 due Week 7; continue your perception pipeline.
