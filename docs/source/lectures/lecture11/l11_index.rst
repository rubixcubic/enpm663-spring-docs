=====================================================================
L11: Recovery, Robustness, and Failure Handling for AI-Driven Systems
=====================================================================

Overview
--------

This lecture is about what happens when things go wrong. Agentic systems
fail in their own ways: LLMs invent objects, VLMs misread a defect, plans run
on a stale world state, and factory equipment breaks. The lecture collects
the patterns at the behavior tree, planner and execution levels for catching
these failures, classifying them and recovering. Quiz 5 (L9 and L10) is given
at the start of class. The final demo specification is posted.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Design BT recovery structures: fallback chains, retry with backoff, parallel
  monitors.
- Detect LLM output failures: output that breaks the schema, plans that call
  missing tools, invented objects.
- Detect VLM grounding failures: a missed defect, a wrong cell type, a wrong
  position.
- Handle equipment that stops reporting: cached state with a timeout, partial
  replanning.
- Decide between local recovery (retry) and global recovery (replan).


.. admonition:: Materials in progress
   :class: note

   The lecture notes, quiz and references for this lecture are written with
   the slide deck and are not published yet. This page will link to them
   once they are ready. The topics below are the plan.


Planned Topics
--------------

- A failure taxonomy: action failure, sensor failure, plan failure, world
  drift.
- BT recovery structures: fallback (selector), retry with backoff, parallel
  monitors that stop the active branch.
- LLM output validation as a recovery checkpoint; re-prompting with the
  validation error.
- VLM cross-checking: ask twice and compare, or compare with the classical
  detector; flag disagreement.
- Equipment that stops reporting: cached state with a time limit, degraded
  operation.
- ARIAC 2025 challenges as failure scenarios: conveyor malfunction, voltage
  tester malfunction, vacuum tool malfunction, high-priority orders; defective
  cells.


ARIAC Tie-in
------------

The final demo runs an unseen trial that can include any of the ARIAC 2025
challenges. Each one needs an explicit recovery pattern, and this lecture is
the toolkit.


Starting References
-------------------

- ``py_trees_ros`` decorators: TODO link.
- BehaviorTree.CPP: https://www.behaviortree.dev/
- Papers on detecting LLM hallucinations: TODO links.
- ARIAC 2025 challenges: https://pages.nist.gov/ARIAC_docs/en/latest/pages/challenges.html
- ARIAC GitHub: https://github.com/usnistgov/ARIAC


Next Steps
----------

- Quiz 5 today (L9 and L10).
- **The final demo specification is posted today.** The demo is in Week 15.
- GP4 is due in Week 13.
- In the next lecture, we will cover **evaluation**: how to measure an agentic
  system.
