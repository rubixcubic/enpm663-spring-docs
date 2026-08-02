====================================================================================
Week 13: Evaluation and Measurement Science for AI-Augmented Systems
====================================================================================

Overview
--------

This lecture covers how to evaluate AI-augmented robotic systems
quantitatively. AI components introduce new failure modes that traditional
metrics (cycle time, success rate) only partially capture: plans can be
valid but wrong; perception can be confident but mistaken. We borrow from
NIST measurement science to define metrics that capture plan validity,
grounding accuracy, execution success, and end-to-end task performance, and
discuss the experimental design needed to compare systems fairly. PT4 is
due today.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Define plan-level metrics: plan validity, plan length, plan cost.
   - Define perception-level metrics: precision/recall on part detection,
     pose error distribution.
   - Define execution-level metrics: action success rate, recovery rate,
     end-to-end task completion.
   - Design controlled experiments: hold one variable constant, vary
     another, repeat for statistical power.
   - Reason about what PT5's grading rubric likely measures (forward-looking).


Topics
------

- Measurement science: what does "good" mean for an AI-augmented system?
- Plan validity vs. plan optimality: a valid plan may not be the best.
- Grounding accuracy: VLM precision/recall on part identity; pose error
  decomposition (position vs. orientation).
- End-to-end task metrics: completion rate, time to completion, recovery
  count, fault-handling correctness.
- Statistical methods: sample sizes, significance, confidence intervals.
- ARIAC scoring criteria as a worked example (forward-looking to PT5).


Hands-On Exercise
-----------------

In teams, design an evaluation protocol for PT4 (your LLM + VLM planner):
which metrics, how many runs, what counts as a fair comparison to a PDDL
baseline. Share protocols; instructor critiques.


ARIAC Tie-in
------------

ARIAC has its own scoring criteria for the competition; PT5 will be graded
on a similar protocol (live demo on an unseen scenario). Today's lecture is
how you measure your own system before that day.


References
----------

- NIST measurement science publications: TODO links.
- ARIAC scoring documentation: TODO link.
- ARIAC GitHub: https://github.com/usnistgov/ARIAC
- ARIAC Documentation: https://pages.nist.gov/ARIAC_docs/en/latest/index.html


Next Steps
----------

- PT4 due today; PT5 hand-out was last week (Week 12); PT5 due Week 15.
- Week 14 is a PT5 lab session.
- Week 15 is the PT5 live demo.
