================================================================
L12: Evaluation and Measurement Science for AI-Augmented Systems
================================================================

Overview
--------

This lecture covers how to measure an agentic robot system. AI components
add failure modes that the usual metrics (cycle time, success rate) only
partly capture: a plan can be valid and still wrong, and perception can be
confident and mistaken. The lecture draws on NIST measurement science to
define metrics for plan validity, grounding accuracy, execution success and
end-to-end task performance, and covers the experiment design needed to
compare two systems fairly. GP4 is due.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Define plan-level metrics: validity, length, cost.
- Define perception-level metrics: precision and recall of defect detection,
  position error.
- Define execution-level metrics: action success rate, recovery rate, task
  completion.
- Design a controlled comparison: change one variable, hold the rest, repeat
  enough runs.
- Read the ARIAC 2025 scoring formula and explain what each term rewards or
  penalizes.


.. admonition:: Materials in progress
   :class: note

   The lecture notes, quiz and references for this lecture are written with
   the slide deck and are not published yet. This page will link to them
   once they are ready. The topics below are the plan.


Planned Topics
--------------

- Measurement science: what "good" means for an agentic system.
- Plan validity and plan quality: a valid plan may not be the best one.
- Grounding accuracy: precision and recall of the VLM on defects and cell
  types.
- End-to-end metrics: kits and modules completed, time, recoveries, correct
  handling of each challenge.
- How many runs: sample size, variation between runs, confidence intervals.
- ARIAC 2025 scoring as a worked example: base score for kits and modules,
  bonuses for time, inspection speed, priority orders and sensor cost, and
  penalties for drops and collisions.


ARIAC Tie-in
------------

ARIAC scores every trial with a published formula, and the final demo is
scored the same way on an unseen trial. This lecture is how you measure your
own system before that day.


Starting References
-------------------

- ARIAC 2025 scoring: https://pages.nist.gov/ARIAC_docs/en/latest/pages/scoring.html
- NIST measurement science publications: TODO links.
- ARIAC GitHub: https://github.com/usnistgov/ARIAC
- ARIAC documentation: https://pages.nist.gov/ARIAC_docs/en/latest/index.html


Next Steps
----------

- GP4 is due today.
- In the next lecture, we will survey **the physical AI frontier**: the
  learned models this course did not build.
