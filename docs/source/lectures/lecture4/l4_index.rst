====================================================
Week 4: Behavior Trees for Task Execution
====================================================

Overview
--------

This lecture introduces behavior trees (BTs) as the executive layer of an
AI-augmented robotic system. We cover the BT language (sequence, selector,
parallel, decorators), execution semantics (ticking, status propagation),
blackboards for shared state, and the ``py_trees_ros`` library that PT1
requires. Quiz #1 (covering Weeks 1 to 3) is administered at the start of
class.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Explain why BTs replaced finite state machines for robot task execution.
   - Identify and use the BT primitives: sequence, selector, parallel, and
     standard decorators.
   - Implement a BT in ``py_trees_ros`` with action-client leaves.
   - Use blackboards to share state between BT nodes.
   - Reason about BT failure modes (action failure, mid-tick interruption).


Topics
------

- BT vs. FSM: composition over enumeration; why industry adopted BTs.
- BT primitives: sequence, selector, parallel; standard decorators (inverter,
  retry, timeout, success-is-failure).
- Execution semantics: tick propagation, status (SUCCESS/FAILURE/RUNNING),
  reactive vs. memory variants.
- Blackboards: shared state, read/write conventions, pitfalls.
- ``py_trees_ros``: ROS 2 integration, action-client leaves, lifecycle.


Hands-On Exercise
-----------------

Build a minimal ``py_trees_ros`` tree with a single sequence node that ticks
two action-client leaves wrapping ARIAC's pick and place actions. Verify
SUCCESS, FAILURE, and RUNNING propagation. (TODO: starter package with stub
action servers.)


ARIAC Tie-in
------------

The BT you build here is the skeleton of PT1: a fixed-order, hard-coded
kitting sequence. PT2 (next module) will replace the hard-coded part poses
with perception output; PT3 will replace the hard-coded sequence with a
PDDL plan, executed by the same BT pattern.


References
----------

- ``py_trees_ros`` documentation: TODO link.
- BehaviorTree.CPP (industry, will be shown in W7): TODO link.
- ARIAC GitHub: https://github.com/usnistgov/ARIAC
- ARIAC Documentation: https://pages.nist.gov/ARIAC_docs/en/latest/index.html


Next Steps
----------

- Quiz #1 administered today (Weeks 1 to 3).
- PT1 due Week 5; finish your BT and write-up.
- Week 5 covers perception, which will feed real poses into a PT1-style BT.
