====================================================
PT3: PDDL Planner + BT Executor (Classical Baseline)
====================================================

.. list-table::
   :widths: 25 25 25 25
   :class: compact-table

   * - **Hand out:** Week 7
     - **Due:** Week 10
     - **Weight:** 10%
     - **Planner:** Fast Downward or UP

Goal
----

Replace PT1's hard-coded action sequence with a PDDL planner that generates
plans from a goal; execute those plans through a behavior tree that translates
each PDDL action into a BT subtree. This is the classical baseline that PT4's
LLM agent will be compared against. This project spans Spring Break (Week 8).

ARIAC Tie-in
------------

Multi-part kitting orders with varying contents are read from ARIAC's order
interface, including at least one scenario with a faulty part that triggers
re-planning. The plan-to-BT factory you build here is reused unchanged in PT4,
where the plan comes from an LLM agent instead of a PDDL planner.

Deliverable
-----------

- PDDL domain and problem files.
- Planner integration (Fast Downward or the Unified Planning Framework).
- A BT executor that consumes plans via a plan-to-BT factory.
- A demo on 2 to 3 ARIAC kitting scenarios, one of which triggers a re-plan.
- A brief reflection on what PDDL captures well vs. where it strains.

Relevant Lectures
-----------------

- Week 6: Task-Level Planning with PDDL.
- Week 7: Plan Execution Patterns with Behavior Trees.
