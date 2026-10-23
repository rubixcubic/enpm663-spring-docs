================================================================
L12: Evaluation and Measurement Science for Agentic Systems
================================================================

Overview
--------

Every team has just compared its GP4 agent with its GP3 planner. This lecture is about
the measurement behind that comparison. A claim about a system needs three
things: a **defined metric**, a **source of truth** to compare against, and
enough runs to know how far the number moves by chance.

The lecture sorts the metrics of an agentic robot system into **four
levels**, from narrow to broad. **Plan level:** is the plan valid, short and
cheap, and for an LLM planner, does the reply pass the schema, name only
objects that exist, and come back fast and cheaply? **Perception level:**
**precision** and **recall** of the defect detector, worked from 20 labeled
cells, and the **position error** of the top shell estimate over 8 spawns.
**Execution level:** action success rate, recovery rate, challenge handling
and collisions. **End to end:** kits and modules completed, times, and the
ARIAC run score.

The middle of the lecture asks how many runs a claim needs. A success rate
measured over a few runs moves by chance. Its **standard error** is the
spread of one estimate: about how far one measured rate lands from the true
rate. Two independent sets of runs differ from each other by about √2 times
that: at 20 runs and a true rate of 0.80, 0.089 for one set and 0.126 for a
difference. A worked example (GP3 completes 17 of 20 runs, GP4 15 of 20)
shows that a gap of 0.10 is smaller than one standard error of the
difference, so those runs do not show that GP4 is worse. A simulation shows
how far chance moves a success rate for 5 to 100 runs. Two cases then put a
number on it: 126 runs per system to resolve a 0.10 gap, and what a 20-run
batch with a bar of 19 of 20 can and cannot show. A **controlled
comparison** then changes one variable and holds the rest, so a difference
has only one cause.

The last part reads the **ARIAC 2025 scoring formula** term by term, with the
weights from the ARIAC source, and works two runs of the same trial. A
run that misses one kit loses 3201.25 points: its share of the base score and
every bonus, because ARIAC pays bonuses only when every order is complete.
The lecture ends with what a final demo test plan contains.

.. important::

   **ARIAC tie-in.** NIST runs ARIAC as a common test with a common score,
   and the final demo is scored the same way, on a trial no team has seen.
   The scoring section uses ``scoring_weights.yaml`` and ``scoring.py`` from
   the ARIAC source (branch ariac2025, commit 0c3e722), and the worked
   example is checked with a calculator that follows ``scoring.py``.

.. important::

   **Group project.** GP4 is due this Friday, April 23, at 11:59 pm: submit
   it on ELMS-Canvas with the repository link. After the deadline, fill in the GP4 peer-review form.
   There is no quiz today. Use this lecture's rules for the GP4 comparison
   with GP3 and for the final demo test plan.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Define plan-level metrics (validity, length, cost) and the extra measures
  an LLM planner needs (schema-valid rate, invented objects, tokens and
  latency per decision).
- Compute precision and recall for defect detection from a confusion count,
  and explain which error costs more in ARIAC.
- Define execution-level metrics: action success rate, recovery rate and
  challenge handling.
- Design a controlled comparison that changes one variable, and estimate
  whether a difference in success rate is larger than chance.
- Compute an ARIAC 2025 run score from the scoring formula and the published
  weights, and explain how each term raises or lowers the score.
- Evaluate a test plan for the final demo against these metrics.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l12_lecture
   l12_code
   l12_exercises
   l12_quiz
   l12_references


Next Steps
----------

- In the next lecture we cover **L13: The Physical AI Frontier** (Wednesday,
  April 28):

  - VLAs, robot foundation models and world models.
  - Final demo questions are answered at the end of class.

- **Before next class:**

  - Write your team's final demo test plan: trial configurations, runs per
    configuration, and the metrics recorded per run.
  - Recompute Run 1 of the worked example with your own measurements and
    sensor list.
  - Run ``run_all.sh`` (see :doc:`l12_code`) and compare the outputs with
    the ones in the notes.
  - Work through the :doc:`L12 exercises <l12_exercises>` and take the
    :doc:`self-check quiz <l12_quiz>` (ungraded).
