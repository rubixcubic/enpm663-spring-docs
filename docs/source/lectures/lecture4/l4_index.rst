====================================================
L4: Behavior Trees for Task Execution
====================================================

Overview
--------

This lecture introduces behavior trees (BTs) as the executive layer of an
agentic robot system. It covers the BT language (sequence, selector, parallel,
decorators), how a tree executes (ticks and status), blackboards for shared
state, and the ``py_trees_ros`` library that GP1 uses. Quiz 1 (L1 to L3) is
given at the start of class.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain why behavior trees replaced finite state machines for robot task
  execution.
- Use the BT primitives: sequence, selector, parallel and the standard
  decorators.
- Implement a BT in ``py_trees_ros`` whose leaves call ROS 2 actions.
- Use blackboards to share state between BT nodes.
- Reason about BT failure modes: an action that fails, a tick that is
  interrupted.


.. admonition:: Materials in progress
   :class: note

   The lecture notes, quiz and references for this lecture are written with
   the slide deck and are not published yet. This page will link to them
   once they are ready. The topics below are the plan.


Planned Topics
--------------

- BTs and FSMs: composition instead of enumerating states; why industry
  adopted BTs.
- BT primitives: sequence, selector, parallel; decorators (inverter, retry,
  timeout).
- Execution: tick propagation, SUCCESS, FAILURE and RUNNING, reactive and
  memory variants.
- Blackboards: shared state, read and write conventions, pitfalls.
- ``py_trees_ros``: ROS 2 integration, action-client leaves.


ARIAC Tie-in
------------

GP1 is a BT that builds one kit: it feeds cells, reads their voltages,
recycles the ones out of range, places four cells on an AGV tray, sends the
AGV to shipping and submits the kit. Its leaves call the course skills
package and the ARIAC services.


Starting References
-------------------

- ``py_trees_ros`` documentation: TODO link.
- BehaviorTree.CPP (shown in L7): https://www.behaviortree.dev/
- ARIAC GitHub: https://github.com/usnistgov/ARIAC
- ARIAC documentation: https://pages.nist.gov/ARIAC_docs/en/latest/index.html


Next Steps
----------

- Quiz 1 today (L1 to L3).
- GP1 is due in Week 5.
- In the next lecture, we will cover **perception**: inspecting battery cells
  from camera images.
