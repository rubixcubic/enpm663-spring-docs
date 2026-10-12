====================================================
Lecture
====================================================

.. note::

   These notes follow the L12 slides shown in class, in the same order and
   with the same sections, so you can read them at home. Every program
   output below comes from running the L12 scripts (Python 3.12.3, numpy
   1.26.4, PyYAML 6.0.1). The scripts and how to run them are on the
   :doc:`code page <l12_code>`.

.. admonition:: Class logistics for this week
   :class: warning

   - **GP4 is due today.** Submit it on Canvas with the repository link, and
     fill in the GP4 peer-review form.
   - **There is no quiz today.**


.. _l12-recap:

Recap
-----

From L11
~~~~~~~~

- Failures sorted into types, each with a signal that detects it.
- Recovery at three levels: the robot skill, the behavior tree, the planner
  or agent.
- A challenge test matrix: each challenge alone and combined, each run more
  than once.

Today's Question
~~~~~~~~~~~~~~~~

How do you know your system works, and how sure can you be? A claim needs a
metric, a source of truth and enough runs. This lecture builds each of the
three.


.. _l12-what-good-means:

What Good Means
---------------

A Claim Is Only as Good as Its Measurement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Measurement science** is the work of making a number trustworthy: saying
what was measured, against what, and how much the number can move. Every
measurement in this lecture needs three things:

1. **A defined metric:** what is counted, and from which log or topic.
2. **A source of truth** to compare against: the true defects, the true
   pose, the orders wanted.
3. **A known run-to-run variation:** how far the number moves when nothing
   in the system changes.

.. admonition:: ARIAC is a measurement
   :class: note

   NIST runs ARIAC as a common test with a common score. The ARIAC
   documentation says its results guide "standards efforts in robot
   agility".

.. admonition:: Opening discussion
   :class: hint

   Every team just compared its GP4 agent with its GP3 planner. How many runs
   did you use, and how sure are you that the difference you reported is
   real? Keep your answer in mind: the section :ref:`l12-how-many-runs` gives
   you the arithmetic to check it.


.. _l12-four-levels:

Four Levels of Metrics, from Narrow to Broad
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The figure is the course stack. The planner or LLM agent sends decisions to
the behavior tree and skills, which act on the ARIAC factory in Gazebo.
Perception (lidar, camera, VLM) reads the factory and feeds both the planner
and the behavior tree. The factory reports the ARIAC score table.

.. image:: /_static/images/l12/metric_levels.svg
   :alt: A block diagram of the course stack. A box "Planner or LLM agent" at
         the top, tag 1, has an arrow down to "Behavior tree and skills", tag
         3, which has an arrow down to "ARIAC factory in Gazebo". An arrow goes
         from the factory to a box on the right, "Perception: lidar, camera,
         VLM", tag 2, which has arrows to the planner and to the behavior
         tree. An arrow goes from the factory to a box on the left, "ARIAC
         score table", tag 4.
   :width: 90%
   :align: center

Each tag is one level of metrics:

1. **Plan level:** is the plan correct and efficient before it runs?
2. **Perception level:** does the system see the factory correctly?
3. **Execution level:** do the actions and the recoveries work?
4. **End to end:** how much of the order was done, how fast, at what cost,
   with what penalties? The ARIAC score sits here.


Why Measure Below the Score
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- The ARIAC score says **how** a run went. The three lower levels say
  **why**.
- When the score drops, the lower levels show where: a longer plan, a
  detector that missed defects, or a skill that failed more often.
- A good score next to poor lower-level metrics means the trial did not test
  the weak part. Example: a trial with few defective cells hides a detector
  that misses defects.

.. tip::

   Log the metrics of every level on every run. Then you can explain a
   score, not only report it.


.. _l12-plan-metrics:

Plan-Level Metrics
------------------

Is the plan correct and efficient before it runs? These metrics apply to the
GP3 planner and to the GP4 agent.

Validity, Length and Cost
~~~~~~~~~~~~~~~~~~~~~~~~~

For any planner:

.. admonition:: Definitions: validity, length and cost
   :class: note

   - **Validity:** every action's preconditions hold in the state where it
     runs, and the plan reaches the goal.
   - **Length:** the number of actions, that is, skill calls and service
     calls.
   - **Cost:** the sum of the action costs, if the domain defines them, or
     the time the plan takes to run.

**Checking validity.** A **validator** replays the plan on the model and names
the first action whose precondition fails. The Unified Planning Framework has
one (``PlanValidator``, from L6). For a GP4 agent, run its decisions through
the same check: turn each decision into the matching PDDL action.


A Valid Plan Is Not Always the Best Plan
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Take two plans for the same cells:

- **Plan A** sends every cell to voltage tester 1, while tester 2 sits idle.
- **Plan B** alternates the two testers.

Comparing them:

1. Both are valid: every precondition holds, and both reach the goal.
2. In Plan A each cell waits for the cell before it to leave tester 1. In
   Plan B two cells can be on testers at once.
3. So Plan A takes longer.

.. tip::

   Validity does not separate the two plans. Cost or time does, so report
   both.


Extra Measures for an LLM Planner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An LLM planner can fail in ways a PDDL planner cannot, so the GP4 comparison
has four more columns:

- **Schema-valid rate:** the share of replies that pass the JSON schema on
  the first try, and after one re-prompt.
- **Invented objects:** the number of replies that name a cell, slot, AGV or
  order ID that does not exist.
- **Tokens and dollars per decision** for a hosted model, or GPU time for a
  local one.
- **Latency per decision:** the time from the observation to a validated
  decision.

**How to report them.** Report them per decision, from the decision logs your
team has kept since L9. A list per decision gives a mean and a spread. A
single total for the run gives neither.


.. _l12-perception-metrics:

Perception Metrics
------------------

Does the system see the factory correctly? This section measures it with
precision, recall and position error.

.. note::

   Every output in this section comes from running ``perception_metrics.py``
   (Python 3.12.3) on two small labeled files, ``cells.csv`` and
   ``shell_poses.csv``. Every value in the files is chosen for this example.


Four Outcomes and Two Ratios
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Count one class at a time, for example defective cells. The detector
**flags** a cell when it says the cell is defective. Each cell then falls into
one of four outcomes:

.. list-table::
   :header-rows: 1
   :widths: 34 26 40
   :class: compact-table

   * - **Outcome**
     - **The cell is**
     - **The detector says**
   * - True positive (TP)
     - defective
     - defective (flagged)
   * - False positive (FP)
     - good
     - defective (flagged)
   * - False negative (FN)
     - defective
     - good
   * - True negative (TN)
     - good
     - good

.. admonition:: Definitions: precision and recall
   :class: note

   - **Precision** = TP / (TP + FP): of the cells we flagged, the share that
     were defective.
   - **Recall** = TP / (TP + FN): of the defective cells, the share we
     flagged.


Worked Example: Precision and Recall
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The counts (chosen for this example).** 20 cells pass inspection, and 5 of
them are defective. The detector flags 6 cells. 4 of the 6 are among the 5
defective cells.

**Step by step:**

1. True positives: 4. False positives: 6 − 4 = 2. False negatives:
   5 − 4 = 1.
2. Precision = 4 / 6 = 0.67.
3. Recall = 4 / 5 = 0.80.

.. tip::

   This detector misses 1 defective cell in 5, and 1 in 3 of its flags is a
   good cell.


The Same Counts from a Labeled Set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``cells.csv`` holds the 20 cells: the true label (``defective``) and the
detector's flag (``flagged``). The script counts the four outcomes in one
loop:

.. literalinclude:: code/perception_metrics.py
   :language: python
   :lines: 23-33
   :caption: perception_metrics.py (excerpt)

Output:

.. literalinclude:: outputs/perception.txt
   :language: text
   :lines: 1-3

The program agrees with the three steps above.


Which Error Costs More in ARIAC 2025
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The two errors do not cost the same.

**A false positive.** A good cell flagged as defective gets a failing
inspection report. The inspection door pushes it into the inspection bin.
Penalty: 50 points per cell (``GOOD_CELL_IN_INSPECTION_BIN`` in
``scoring_weights.yaml``).

**A false negative.** A defective cell passes. If it goes into a kit, ARIAC
does not accept the kit at shipping, because an accepted kit needs four good
cells (ARIAC scoring page). That loses the kit's share of the base score and
the time to rebuild the kit. The cell's report also does not count toward the
classification bonus.

.. tip::

   The two errors have different prices. Your team can set its detector
   threshold with those prices in mind. The worked example at the end of the
   lecture puts a number on each price.


What to Report for Your Detectors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Precision and recall **per defect type** (dent, bulge, scratch), as in GP2.
- For the VLM: precision and recall **per cell type** (Li-Ion against
  Ni-MH).
- ARIAC's own classification check is stricter. A report counts only if it
  has the right number of defects, and each defect's type, angle and height
  are within ARIAC's thresholds (``physical_inspection_plugin.cpp``).

**In the final demo.** The embodied-reasoning model judges defects from camera
images of the same cells your GP2 lidar detector inspects. Your comparison
table reports both with precision and recall per defect type, and the number
of cells used.


Position Error for the Top Shell
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In Task 2 the top shell spawns at a random pose on the assembly table. Your
camera chain estimates its position (L10).

.. admonition:: Definition: position error
   :class: note

   For one spawn, :math:`\Delta x` and :math:`\Delta y` are the estimated
   minus the true position along the two table axes. The **position error**
   is

   .. math::

      e = \sqrt{\Delta x^2 + \Delta y^2}

   in millimeters.

Over many spawns, report the **mean**, the **spread** (the sample standard
deviation) and the **largest** error. The 8 spawns below are in
``shell_poses.csv``, chosen for this example. Output of the same script:

.. literalinclude:: outputs/perception.txt
   :language: text
   :lines: 4-5

For example, spawn 1 has a true position of (0.412, −0.135) m and an
estimate of (0.415, −0.131) m. So :math:`\Delta x` = 0.003 m and
:math:`\Delta y` = 0.004 m, and :math:`e = \sqrt{3^2 + 4^2}` = 5.0 mm, the
first value printed.

One bad spawn can make one grasp miss even when the mean is small, so report
the largest error too.


Every Metric Needs Ground Truth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Precision, recall and position error all compare the system's answer with the
truth. In simulation, the truth comes from here:

- **Cells:** launch ARIAC with ``log_cell_info:=true``. It prints each
  spawned cell's type, voltage, rotation, defective flag and defects to the
  Gazebo log (``cheat_tools_plugin.cpp``).
- ``ariac_setup/config/defects.yaml`` holds only the shape of each defect
  type, not which cells are defective.
- **Top shell:** ``log_cell_info`` covers cells only. Read the true shell
  pose from the simulator during testing, and check how on your setup.

.. warning::

   These are test tools. Your system must not read them during a run.


.. _l12-execution-metrics:

Execution and End-to-End Metrics
--------------------------------

Do the actions and the recoveries work, and how much of the order was done?

What to Count at the Two Top Levels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Execution level:**

- **Action success rate** per skill: successes / calls, from the skill
  results.
- **Recovery rate:** failures recovered without operator help / failures
  detected.
- **Challenge handling**, for each challenge on each run: detected or not,
  the time until detection, and whether the run continued correctly.
- **Collisions:** count and duration. ARIAC charges a robot collision again
  for every 5 s of contact.

**End to end:**

- Kits and modules completed, against kits and modules wanted.
- Trial time, average inspection report time and high-priority order time.
- The ARIAC run score, worked through in :ref:`l12-scoring`.


.. _l12-how-many-runs:

How Many Runs
-------------

What chance alone does to a success rate, and how many runs a claim needs.

.. note::

   The simulation in this section comes from running ``success_spread.py``
   (Python 3.12.3, numpy 1.26.4).


Why Two Runs of the Same System Differ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the same system twice on the same trial and the results can differ. The
sources of variation in this stack:

- Sampling planners return a different path on each run (L10).
- An LLM can return a different plan for the same prompt.
- Voltage readings are noisy. Across trials, the seed changes which cells
  are defective.
- The timing between ROS 2 nodes changes from run to run.

.. tip::

   So a success rate measured over a few runs is itself a measurement, and it
   has its own spread.


The Standard Error of a Success Rate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definitions: success rate and standard error
   :class: note

   A system completes the trial on :math:`k` of :math:`n` runs. Its measured
   **success rate** is :math:`p = k / n`.

   Chance alone moves :math:`p` from one set of :math:`n` runs to the next by
   about its **standard error**:

   .. math::

      \mathrm{SE} = \sqrt{p\,(1 - p) / n}

   For the difference between the rates of two systems tested on separate
   runs:

   .. math::

      \mathrm{SE}_{\mathrm{diff}} = \sqrt{\mathrm{SE}_1^2 + \mathrm{SE}_2^2}

.. tip::

   The standard error shrinks with the square root of :math:`n`: four times
   the runs halves it.


.. _l12-gp3-gp4:

Worked Example: Comparing GP3 and GP4
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The counts (chosen for this example).** GP3 completes the trial on 17 of 20
runs. GP4 completes it on 15 of 20 runs.

**Step by step:**

1. Success rates: 17 / 20 = 0.85 and 15 / 20 = 0.75. The difference is 0.10.
2. SE for GP3: :math:`\sqrt{0.85 \times 0.15 / 20}` = 0.080. SE for GP4:
   :math:`\sqrt{0.75 \times 0.25 / 20}` = 0.097.
3. SE of the difference: :math:`\sqrt{0.080^2 + 0.097^2} = \sqrt{0.0064 +
   0.0094}` = 0.126.
4. The difference, 0.10, is smaller than one standard error, 0.126.

.. tip::

   Chance alone can explain a gap of 0.10 here, so these 20 runs do not show
   that GP4 is worse than GP3.


Simulating n Runs, Many Times Over
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The formula can be checked by simulation. ``success_spread.py`` takes a system
whose true success rate is 0.80 (chosen for this example), tests it
:math:`n` times, and repeats that test 10000 times for each :math:`n`. For each
:math:`n` it prints the middle 95% of the 10000 measured rates, their standard
deviation (``spread``) and the formula's value:

.. literalinclude:: code/success_spread.py
   :language: python
   :lines: 27-32
   :caption: success_spread.py (excerpt)

Output:

.. literalinclude:: outputs/success_spread.txt
   :language: text
   :lines: 1-6

- The seed is fixed (12), so every run of the script prints the same
  numbers.
- ``spread`` is the standard deviation of the 10000 measured rates. It
  matches the formula :math:`\sqrt{0.80 \times 0.20 / n}` at every
  :math:`n`. For example, at :math:`n = 20`:
  :math:`\sqrt{0.80 \times 0.20 / 20} = \sqrt{0.008}` = 0.089.


How Far Chance Moves a Measured Success Rate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The plot draws the same simulation. It is a plot of measured success rate
against the number of runs, not a picture of the factory.

.. image:: /_static/images/l12/success_spread.svg
   :alt: A plot of measured success rate (y axis, 0.3 to 1.0) against the
         number of runs n (x axis: 5, 10, 20, 50, 100) for a simulated system
         whose true success rate is 0.80, shown as a dashed line with tag 1.
         For each n, gray dots (tag 3) show 40 single experiments, and a dark
         bar with caps (tag 2) spans the middle 95% of 10000 experiments: n =
         5: 0.40 to 1.00; n = 10: 0.50 to 1.00; n = 20: 0.60 to 0.95; n = 50:
         0.68 to 0.90; n = 100: 0.72 to 0.87. The bar gets shorter as n grows.
   :width: 90%
   :align: center

1. The true success rate, 0.80, chosen for this example.
2. The middle 95% of 10000 simulated measurements at that :math:`n`.
3. One simulated measurement over :math:`n` runs (40 shown for each
   :math:`n`).

With 5 runs, a system that truly succeeds 80% of the time can measure
anywhere from 0.40 to 1.00. With 100 runs, the middle 95% is 0.72 to 0.87.


Two Equal Systems Still Measure Differently
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The second part of the script takes two systems that **both** succeed 80% of
the time, runs each one 20 times, and repeats the comparison 10000 times.
Output:

.. literalinclude:: outputs/success_spread.txt
   :language: text
   :lines: 7-9

1. Each system is run 20 times, and the comparison is repeated 10000 times.
2. In 54.8% of the comparisons the two measured rates differ by 0.10 or more,
   the same gap as the GP3 and GP4 example.
3. Two standard errors of the difference:
   :math:`2 \times \sqrt{2 \times 0.80 \times 0.20 / 20}` = 0.253. A gap that
   large appears in only 3.1% of the comparisons.

.. admonition:: Rule for this class
   :class: important

   A difference smaller than about two standard errors is not evidence.
   Report every success rate with its run count, so a reader can redo the
   arithmetic.


ARIAC's Choice: Five Runs, Best Two Averaged
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**How ARIAC scores a team.** Each trial is run five times. The two best run
scores are averaged, and the averages of all trials are summed (ARIAC scoring
page). That measures how well a system does on its good runs.

**How you should test.** The final demo is a single run on an unseen trial. A
good run is not guaranteed. So for your own testing, report the mean and the
spread over all runs, not the best ones.


.. _l12-controlled-comparisons:

Controlled Comparisons
----------------------

Change one variable and hold the rest, so a difference has only one cause.

The GP4 Comparison, Designed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A **controlled comparison** tests two systems that differ in one variable
only, on runs where everything else is the same. The figure lays out the GP4
comparison with GP3 that way.

.. image:: /_static/images/l12/controlled_comparison.svg
   :alt: Two columns, "GP3 runs" and "GP4 runs". Four wide gray boxes span
         both columns, marked tag 1: the trial file (seed, defect rate, time
         limit, challenges and times), the team configuration (sensors and
         poses, conveyor speed, feed rate), the software (skills release,
         executor, model name, version, settings) and the machine (the same
         computer for every run). Under them, marked tag 2, each column has
         its own box with a heavy outline: "PDDL planner (GP3)" and "LLM agent
         (GP4)". At the bottom, marked tag 3, eight runs in time order: 1
         GP3, 2 GP4, 3 GP3, 4 GP4, and so on to 8 GP4, above an arrow labeled
         time.
   :width: 90%
   :align: center

1. Held fixed for every run of both systems.
2. The one variable that changes: the planner.
3. The run order alternates the two systems.


Three Rules for a Fair Comparison
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Hold the rest fixed.** The same trial file (seed, defect rate, time
   limit, challenges and their start times), team configuration (sensors and
   poses, conveyor speed, cell feed rate), software (skills package release,
   executor, model name, version and settings) and computer. Then a
   difference has only one cause.
2. **Alternate the runs:** GP3, GP4, GP3, GP4. If the machine slows down over
   the session, both systems share the slowdown.
3. **Write the plan first**, with the number of runs. If you stop when the
   result looks good, chance picks the answer.

.. tip::

   The GP4 comparison with GP3 is the first place you use these rules. The
   final demo test plan is the second.


.. _l12-scoring:

The ARIAC 2025 Scoring Formula
------------------------------

This section reads each term of the run score, with the weights from the
ARIAC 2025 source. The sources are the
`ARIAC scoring page <https://pages.nist.gov/ARIAC_docs/en/latest/pages/scoring.html>`_,
and ``ariac_db/ariac_db/scoring.py`` with
``ariac_plugins/src/competition_manager_plugin.cpp`` (branch ariac2025,
commit 0c3e722).


Where the Numbers Come From
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The scoring page says the weights may change, and points to
``ariac_db/config/scoring_weights.yaml``. Read the file, not a copy from
memory. The copy in ``lecture12/code/scoring_weights.yaml`` is from branch
ariac2025, commit 0c3e722:

.. literalinclude:: code/scoring_weights.yaml
   :language: yaml
   :lines: 4-
   :caption: scoring_weights.yaml


The Run Score and the Base Score
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Run score.**

.. math::

   R = B + (\text{sum of the bonuses}) - (\text{sum of the penalties})

**Base score.**

.. math::

   B = W_1 \cdot k_c / k_d + W_2 \cdot m_c / m_d, \quad W_1 = 5000,\ W_2 = 12000

- :math:`k_c` and :math:`k_d`: kits completed and kits wanted.
  High-priority kits count in :math:`k_d`. A kit counts only when ARIAC
  accepts it at shipping.
- :math:`m_c` and :math:`m_d`: modules completed and modules wanted. A trial
  with no modules adds 0 for modules.
- All the modules together are worth 12000 / 5000 = 2.4 times all the kits
  together, so Task 2 carries most of the base score in a trial that asks for
  modules.


.. _l12-bonus-gate:

The Bonus Gate, and Where Docs and Code Differ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: The bonus gate
   :class: important

   Bonuses are paid only if every wanted kit and module, high-priority kits
   included, was submitted and accepted.

In the code, the competition manager marks the run aborted when not every
order is complete (``run.aborted = !orders_complete()``), and
``score_bonuses`` then sets all five bonuses to 0.

**Clamping at zero.** To **clamp** a value at zero is to replace it with 0
when it would be negative.

- The scoring page says every bonus is clamped at zero.
- The code clamps three of them with ``max(0, ...)``: inspection speed,
  high-priority speed and sensor cost.
- It does not clamp the trial time bonus, which goes below zero only if the
  run time passes the time limit. The classification bonus cannot go below
  zero.


Three Bonuses for Speed
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 18 22 10 50
   :class: compact-table

   * - **Bonus**
     - **Formula**
     - **Weight**
     - **Symbols**
   * - Trial time
     - :math:`W_3\,(1 - t_e / t_m)`
     - 1000
     - :math:`t_e`: run time, from the start of the competition to its end
       (the time limit, or your call to end the competition). :math:`t_m`:
       the trial's time limit.
   * - Inspection speed
     - :math:`W_4\,(1 - \gamma / 4\,\mathrm{s})`
     - 500
     - :math:`\gamma`: average report time. In the code, a cell's report time
       runs from the moment the cell is created on the conveyor to its
       inspection report.
   * - High-priority speed
     - :math:`W_5\,(1 - \tau / 150\,\mathrm{s})`
     - 600
     - :math:`\tau`: average time from a high-priority order's announcement
       to its submission. 0 if the trial has no high-priority order.

The 4 s and 150 s are ``NOMINAL_INSPECTION_TIME`` and
``NOMINAL_HIGH_PRIORITY_EXECUTION_DURATION`` in the weights file.


Bonuses for Sensor Cost and Classification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 18 22 10 50
   :class: compact-table

   * - **Bonus**
     - **Formula**
     - **Weight**
     - **Symbols**
   * - Sensor cost
     - :math:`W_6\,(1 - \sigma / 9600)`
     - 1000
     - :math:`\sigma`: total cost in dollars of the sensors in your team
       configuration. 9600 is ``SENSOR_BUDGET``.
   * - Inspection classification
     - :math:`W_7 \cdot \nu / \delta`
     - 500
     - :math:`\nu`: defect reports with every element right. :math:`\delta`:
       defective cells in the run. 0 if there are none.

**What a sensor costs in points:**

1. Each dollar of sensors lowers the bonus by 1000 / 9600 = 0.104 points.
2. So a sensor at $800 costs 1000 × 800 / 9600 = 83.3 bonus points, but only
   in a run that earns bonuses.


Penalties
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 45 55
   :class: compact-table

   * - **Event**
     - **Points per occurrence (weights file)**
   * - Good cell in the inspection bin
     - 50
   * - Cell in the inspection conveyor bin
     - 25
   * - Object on an invalid surface
     - 25
   * - AGV collision
     - 100
   * - Robot collision
     - 100 for every 5 s in contact. Counted twice when two robots collide:
       each robot records its own.

**Sensor cost over the budget.** The code charges
:math:`W_6\,(\sigma / 9600 - 1)` points (``score_penalties`` in
``scoring.py``), that is 1000 / 9600 = 0.104 points per dollar over the
budget. The scoring page says the penalty is per dollar, which matches.


.. _l12-worked-example:

Worked Example: Two Runs
------------------------

One trial, two runs, every step written out.

.. note::

   The calculator in this section is ``score_calculator.py`` (Python 3.12.3,
   PyYAML 6.0.1). It reads ``scoring_weights.yaml`` and follows
   ``scoring.py``.


The Trial and the Team Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The trial.**

- 2 kits plus 1 high-priority kit, so :math:`k_d = 3`. No modules. Chosen
  for this example: a GP4-style Task 1 trial.
- Time limit :math:`t_m` = 900 s: the value in the example trial file on the
  ARIAC configuration page.

**The sensors.** Two grade B lidars at $1250 each, one grade A break beam at
$400, one 1080p camera at $800. The prices are from the ARIAC sensors page;
the choice of sensors is chosen for this example.

1. 2 × 1250 = $2500.
2. 2500 + 400 + 800 = $3700, so :math:`\sigma` = $3700.


What Happened in the Runs
~~~~~~~~~~~~~~~~~~~~~~~~~

**Measurements (all chosen for this example).**

- Run time :math:`t_e` = 630 s. Average inspection report time
  :math:`\gamma` = 3 s.
- The high-priority kit is submitted :math:`\tau` = 120 s after its
  announcement.
- 4 defective cells (:math:`\delta = 4`), 3 of them reported correctly
  (:math:`\nu = 3`).
- One good cell goes to the inspection bin.
- One robot touches fixed equipment for less than 5 s: one occurrence. A
  collision between two robots would count twice.

**The two runs.**

- **Run 1** submits all three kits.
- **Run 2** is the same, except that the agent misses the high-priority
  order, so only 2 of the 3 kits are submitted.


Run 1, Step by Step
~~~~~~~~~~~~~~~~~~~

1. Base: 5000 × 3 / 3 = 5000.
2. Trial time: 1000 × (1 − 630 / 900) = 1000 × 0.30 = 300.
3. Inspection speed: 500 × (1 − 3 / 4) = 500 × 0.25 = 125.
4. High-priority speed: 600 × (1 − 120 / 150) = 600 × 0.20 = 120.
5. Sensor cost: 1000 × (1 − 3700 / 9600) = 1000 × (1 − 0.3854) =
   1000 × 0.6146 = 614.6.
6. Classification: 500 × 3 / 4 = 375.
7. Bonuses: 300 + 125 + 120 + 614.6 + 375 = 1534.6.
8. Penalties: 50 (the good cell in the bin) + 100 (one collision occurrence)
   = 150.
9. Run score: 5000 + 1534.6 − 150 = 6384.6.


Run 2, Step by Step
~~~~~~~~~~~~~~~~~~~

1. Base: 5000 × 2 / 3 = 3333.3.
2. Bonuses: 0. Not every wanted kit was submitted, so ARIAC marks the run
   aborted and sets every bonus to 0.
3. Penalties: the same 150.
4. Run score: 3333.3 − 150 = 3183.3.

.. tip::

   Run 2 ran as fast as Run 1 and classified as well. The gate still sets all
   five bonuses to 0.


The Calculator: Bonuses as in scoring.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The calculator's ``bonuses`` function applies the gate first, then the five
formulas, with the same clamping as ``scoring.py``:

.. literalinclude:: code/score_calculator.py
   :language: python
   :pyobject: bonuses
   :caption: score_calculator.py (excerpt)

Output:

.. literalinclude:: outputs/score_runs.txt
   :language: text

The program agrees with the hand steps. The last line checks the over-budget
penalty for a $10400 configuration (chosen for this example):
1000 × (10400 / 9600 − 1) = 83.3.


The Score Terms Side by Side
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /_static/images/l12/score_breakdown.svg
   :alt: A horizontal bar chart of the ARIAC 2025 score terms for two runs
         on the same trial, Run 1 in blue and Run 2 in orange. The x axis
         is points, with grid lines every 1000 from 0 to 7000; the y axis
         lists the score terms. Base score: Run 1 5000.0, Run 2 3333.3;
         Bonus: trial time: Run 1 300.0, Run 2 0.0; Bonus: inspection
         speed: Run 1 125.0, Run 2 0.0; Bonus: high-priority speed: Run 1
         120.0, Run 2 0.0; Bonus: sensor cost: Run 1 614.6, Run 2 0.0;
         Bonus: classification: Run 1 375.0, Run 2 0.0; Penalties: Run 1
         -150.0, Run 2 -150.0; Run score: Run 1 6384.6, Run 2 3183.3.
         Every Run 2 bonus is zero because Run 2 missed one kit.
   :width: 90%
   :align: center

Bar lengths are the calculator's values (``outputs/score_runs.json``).
Penalties are drawn left of zero.


What the Example Shows
~~~~~~~~~~~~~~~~~~~~~~

1. Missing one kit cost 3201.25 points: 1666.67 from the base and all
   1534.58 of the bonuses (calculator output, before rounding).
2. So finishing every order matters more than any speed bonus. A slow
   recovery that finishes the kit beats a fast system that drops one.
3. In Run 1 the sensor cost bonus, 614.6, is the largest bonus. An extra
   $800 camera for a VLM would lower it by 83.3 points, so a camera must earn
   its cost.
4. A good cell in the inspection bin costs 50 points: the price of a false
   positive. A defective cell in a kit can cost the kit, worth
   5000 / 3 = 1666.7 points of base here, and every bonus if the kit is never
   accepted: the price of a false negative.


Check the Hand Calculation Against ARIAC
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**ARIAC's own table.** At the end of a run, ARIAC's score logger prints a run
score table: run score, kits score, modules score, total bonus, total penalty,
and whether all orders were completed (``get_run_score_table`` in
``scoring.py``). Bonus and penalty tables list each term, and the ARIAC app's
results page shows the same terms.

**Instructor demonstration.** In class, the table of a recorded run is
compared term by term with a hand calculation from that run's measurements.

**Try at home.** Recompute Run 1 with your own GP4 run measurements and your
own sensor list.


.. _l12-test-plan:

A Test Plan for the Final Demo
------------------------------

What your team measures before the unseen trial.

What a Good Test Plan Has
~~~~~~~~~~~~~~~~~~~~~~~~~

1. Several trial configurations your team writes: each challenge alone and
   combined, with Task 1 and Task 2.
2. A fixed number of runs per configuration, chosen before running.
3. For each run: the ARIAC score table, plus your own metrics at the plan,
   perception and execution levels.
4. For each challenge: detected or not, the time to detection, recovered or
   not.

**What it can and cannot tell you.**

- The demo is one run on an unseen trial, so no test plan can predict it.
- The plan shows which failures are common and which recoveries hold up.
  That is what your final presentation reports.
- The final demo rubric reads the same records: the ARIAC run results for
  Task 1 and Task 2, the run log for challenges, the penalty table for a safe
  run, and your embodied-reasoning comparison table.


Next Class
----------

**L13: The Physical AI Frontier (Wednesday, April 28).**

- VLAs, robot foundation models and world models: the learned side of
  physical AI.
- Final demo questions are answered at the end of class.

**Before next class:**

- Write your team's final demo test plan: trial configurations, runs per
  configuration, and the metrics recorded per run.
- Recompute Run 1 of the worked example with your own measurements and
  sensor list.
- Run ``run_all.sh`` (see :doc:`l12_code`) and compare the outputs with the
  ones in these notes.
- Take the :doc:`L12 self-check quiz <l12_quiz>` (ungraded).
