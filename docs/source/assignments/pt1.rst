====================================================
PT1: Behavior Tree for a Simple Kitting Workflow
====================================================

.. list-table::
   :widths: 25 25 25 25
   :class: compact-table

   * - **Hand out:** Week 2
     - **Due:** Week 5
     - **Weight:** 10%
     - **Library:** ``py_trees_ros``

Goal
----

Build a runnable ``py_trees_ros`` behavior tree that executes a fixed,
single-order kitting sequence with hard-coded part poses. The focus is BT
structure (sequences, selectors, decorators, blackboards) and ROS 2
action-client leaves that call ARIAC's pick and place skills as opaque actions.
No perception or planner integration yet; this PT is the "I understand behavior
trees" gate.

ARIAC Tie-in
------------

The BT you build here is the skeleton of the later projects. It calls ARIAC's
pick and place actions directly and drives a single, known kitting order. PT2
will replace the hard-coded part poses with perception output, and PT3 will
replace the hard-coded sequence with a generated plan, executed by the same BT
pattern.

Deliverable
-----------

- A ROS 2 package with a launchable behavior tree.
- A short write-up (1 to 2 pages) including the BT diagram and the rationale for
  the composite choices (why a sequence here, a selector there, which
  decorators and why).

Relevant Lectures
-----------------

- Week 4: Behavior Trees for Task Execution.
