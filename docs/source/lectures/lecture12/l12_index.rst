====================================================
Week 12: Recovery, Robustness, and Failure Handling for AI-Driven Systems
====================================================

Overview
--------

This lecture is about what happens when things go wrong. AI-driven systems
fail in distinctive ways: LLMs hallucinate, VLMs misidentify, plans run on
stale world state, sensors drop out, parts arrive faulty. This lecture
collects the BT-level, planner-level, and execution-level patterns for
catching, classifying, and recovering from these failures. Quiz #5
(covering W10 LLM II and W11 Motion) is administered at the start of class.
PT5 (capstone) is handed out today.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Design BT recovery composites: fallback chains, retry with backoff,
     parallel monitors.
   - Detect LLM output failures: schema-invalid output, plan calling missing
     tools, hallucinated objects.
   - Detect VLM grounding failures: missing parts, wrong colors, position
     drift.
   - Handle sensor blackouts: cached state with timeout, partial replanning.
   - Decide between local recovery (retry) and global recovery (re-plan).


Topics
------

- Failure taxonomy: action failure, sensor failure, plan failure, world
  drift.
- BT recovery composites: fallback (selector), retry-with-backoff,
  parallel monitors that abort the active branch.
- LLM output validation as a recovery checkpoint; re-prompt with the
  validation error.
- VLM cross-checking: ask twice, compare; flag disagreement.
- Sensor blackout handling: cached state with TTL, degraded operation,
  ask-for-help signal.
- ARIAC challenges as failure scenarios: faulty parts, faulty grippers,
  sensor blackouts, kit rearrangement, high-priority orders.


Hands-On Exercise
-----------------

Extend a provided BT (TODO: starter) by wrapping a flaky action node with a
retry decorator (N=3, backoff 1s) and a parallel monitor that watches a
"part-faulty" topic and triggers a fallback subtree on detection.


ARIAC Tie-in
------------

This lecture's content IS the PT5 capstone deliverable's robustness layer.
The ARIAC challenges that PT5 is graded on (faulty parts, sensor blackouts,
high-priority orders) all need explicit recovery patterns; today's lecture
is the toolkit.


References
----------

- ``py_trees_ros`` decorators: TODO link.
- BehaviorTree.CPP recovery patterns: TODO link.
- Papers on LLM hallucination detection: TODO links.
- ARIAC challenge scenarios: TODO link into ARIAC docs.
- ARIAC GitHub: https://github.com/usnistgov/ARIAC


Next Steps
----------

- Quiz #5 today (W10 LLM II, W11 Motion).
- PT5 (Integrated Capstone) handed out today; due Week 15.
- PT4 due Week 13.
- Week 13 covers evaluation and measurement science.
