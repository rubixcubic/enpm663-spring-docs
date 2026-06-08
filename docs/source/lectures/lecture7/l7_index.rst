====================================================
Week 7: Plan Execution Patterns with Behavior Trees
====================================================

Overview
--------

This lecture is the revisit of behavior trees promised in Week 4. Now that
students have seen PDDL plans (Week 6), we look at how to translate an
externally-produced plan into a BT for execution. We cover the plan-to-BT
factory pattern, decorators for retry and timeout, re-planning triggers on
action failure, and a short tour of ``BehaviorTree.CPP`` (industry standard
in C++) so students can read industry codebases. Quiz #3 (covering W5-W6) is
administered at the start of class. PT2 is due today; PT3 is handed out.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Translate a PDDL plan (list of actions) into a sequence-of-subtrees BT.
   - Apply retry and timeout decorators to make a BT tolerant of transient
     action failures.
   - Design re-plan triggers: when should the BT bail out and ask for a new
     plan?
   - Read ``BehaviorTree.CPP`` source (C++) and map concepts back to
     ``py_trees_ros`` (Python).


Topics
------

- The plan-to-BT factory: given a list of action names + arguments, build a
  BT subtree per action.
- Retry and timeout decorators; success-is-failure inversion.
- Re-planning triggers: action failure types that warrant a new plan vs.
  those that warrant a retry.
- ``BehaviorTree.CPP`` walkthrough: XML BT description, ports as typed
  arguments.
- BT debugging: visualization (Groot), logging, tick traces.


Hands-On Exercise
-----------------

Given a 3-step PDDL plan output from Week 6's domain, build a BT factory in
``py_trees_ros`` that constructs an executable subtree per action. Add a
retry decorator with N=3 to handle transient failure of one action. (TODO:
starter package with stub actions.)


ARIAC Tie-in
------------

PT3's BT executor IS this lecture. The factory pattern lets the same
executor work whether the plan came from PDDL (PT3) or an LLM (PT4). Re-plan
triggers will be used in PT3 to handle faulty parts: detect the fault, abort
the current plan, re-plan with updated state.


References
----------

- ``py_trees_ros`` documentation: TODO link.
- ``BehaviorTree.CPP`` (industry, C++): https://www.behaviortree.dev/
- Groot BT visualizer: TODO link.
- ARIAC GitHub: https://github.com/usnistgov/ARIAC


Next Steps
----------

- Quiz #3 today (W5 Perception, W6 PDDL).
- PT2 due today; PT3 (PDDL Planner + BT Executor) is handed out and due Week 10.
- Week 8 is Spring Break (no class).
- Week 9 begins LLM-based task planning.
