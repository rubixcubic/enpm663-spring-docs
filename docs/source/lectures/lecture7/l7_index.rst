====================================================
L7: Plan Execution Patterns with Behavior Trees
====================================================

Overview
--------

This lecture returns to behavior trees from L4. Now that you have PDDL plans
(L6), it shows how to turn a plan made outside the tree into a tree that runs
it: the plan-to-BT factory, decorators for retry and timeout, and triggers
that abandon a plan and ask for a new one. A short tour of
``BehaviorTree.CPP``, the C++ library used in industry, shows you how to read
industry code. Quiz 3 (L5 and L6) is given at the start of class. GP2 is due
and GP3 is posted.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Translate a PDDL plan (a list of actions) into a BT with one subtree per
  action.
- Apply retry and timeout decorators to tolerate actions that fail once.
- Design replanning triggers: when the tree should stop and ask for a new
  plan.
- Read ``BehaviorTree.CPP`` code and map it back to ``py_trees_ros``.


.. admonition:: Materials in progress
   :class: note

   The lecture notes, quiz and references for this lecture are written with
   the slide deck and are not published yet. This page will link to them
   once they are ready. The topics below are the plan.


Planned Topics
--------------

- The plan-to-BT factory: build one subtree per action from its name and
  arguments.
- Retry and timeout decorators.
- Replanning triggers: failures that need a new plan and failures that need a
  retry.
- ``BehaviorTree.CPP``: XML tree descriptions, ports as typed arguments.
- Debugging a BT: visualization (Groot), logging, tick traces.


ARIAC Tie-in
------------

GP3's executor is this lecture. The factory pattern lets the same executor
run a plan whether it came from PDDL (GP3) or from an LLM agent (GP4). GP3
uses replanning triggers for cells that fail inspection: detect the failure,
stop the current plan, and plan again from the updated state.


Starting References
-------------------

- ``py_trees_ros`` documentation: TODO link.
- ``BehaviorTree.CPP``: https://www.behaviortree.dev/
- Groot BT visualizer: TODO link.
- ARIAC GitHub: https://github.com/usnistgov/ARIAC


Next Steps
----------

- Quiz 3 today (L5 and L6).
- GP2 is due today. **GP3 is posted today** and is due in Week 10.
- Week 8 is spring break: no class.
- In the next lecture, we will start **LLM agents for task planning**.
