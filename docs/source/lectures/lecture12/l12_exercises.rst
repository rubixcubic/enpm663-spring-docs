====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes, the four group projects and
   the final demo listed in the :doc:`syllabus </syllabus/index>`.

Six take-home exercises on the L12 slides and three of the L12 scripts.
Exercise 1 changes the detector's threshold in ``cells.csv`` and prices each
error in ARIAC points. Exercise 2 is paper and arithmetic: how many runs a
0.10 difference needs. Exercise 3 changes ``success_spread.py`` to check that
answer by simulation. Exercises 4 to 6 use ``score_calculator.py``: a Task 2
run you score, the effect of the bonus gate, and a sensor setup over the
budget.

.. note::

   The scripts are on the :doc:`code page <l12_code>`. Work on a copy of
   each script and data file, so the originals still give the outputs in the
   notes. Every number in the solutions was computed by hand and checked by
   running the changed script (Python 3.12.3, numpy 1.26.4, PyYAML 6.0.1) on
   2026-10-12. ``success_spread.py`` uses a fixed seed, so your simulated
   numbers match the ones below only if you insert the new code at the same
   place.


.. dropdown:: Exercise 1. Precision and Recall at a Different Threshold
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   See how moving the detector's threshold trades precision for recall, and
   what each error costs in ARIAC points.

   .. raw:: html

      <hr>

   **Part A. A lower threshold**

   A detector usually gives each cell a score and flags the cell when the
   score is above a **threshold**. A lower threshold flags more cells. Your
   team lowers it, and the detector now also flags cells ``c09``, ``c14`` and
   ``c19`` (chosen for this exercise). Every other flag in ``cells.csv`` stays
   the same.

   1. Look up the true labels of ``c09``, ``c14`` and ``c19`` in
      ``cells.csv``. Count TP, FP, FN and TN by hand.
   2. Compute precision and recall.
   3. Change the ``flagged`` column of those three rows to 1 in a copy of
      ``cells.csv``, run ``perception_metrics.py``, and compare.

   .. raw:: html

      <hr>

   **Part B. A higher threshold**

   Start again from the original ``cells.csv``. This time the team raises the
   threshold, and the detector stops flagging ``c05``, ``c11`` and ``c16``.

   4. Count the four outcomes, then compute precision and recall.
   5. Check with the script.

   .. raw:: html

      <hr>

   **Part C. The price of each setting**

   6. For the original detector and the two new settings, how many good
      cells go to the inspection bin, and what is the penalty in points?
   7. How many defective cells pass inspection in each setting? Say what a
      passed defective cell can cost, using the worked example of the
      lecture.
   8. A detector that flags no cell at all: what is its recall? What happens
      to precision, and what does the script do? (Try it.)

   .. dropdown:: Solution
      :color: success

      **Question 1.** ``c14`` is defective; ``c09`` and ``c19`` are good. In
      the original file ``c14`` was the one false negative. Now:

      1. TP: the 4 from before plus ``c14`` = 5.
      2. FP: the 2 from before (``c05``, ``c16``) plus ``c09`` and ``c19``
         = 4.
      3. FN: 5 defective cells − 5 flagged = 0.
      4. TN: 20 − 5 − 4 − 0 = 11.

      **Question 2.** Precision = 5 / (5 + 4) = 5 / 9 = 0.56. Recall =
      5 / (5 + 0) = 5 / 5 = 1.00.

      **Question 3.** The script prints:

      .. code-block:: text

         20 cells: TP 5, FP 4, FN 0, TN 11
         precision = 5/9 = 0.56
         recall    = 5/5 = 1.00

      **Question 4.** ``c05`` and ``c16`` are good, so the two false
      positives disappear. ``c11`` is defective, so one true positive becomes
      a false negative.

      1. TP: 4 − 1 = 3.
      2. FP: 2 − 2 = 0.
      3. FN: 1 (``c14``) + 1 (``c11``) = 2.
      4. TN: 20 − 3 − 0 − 2 = 15.
      5. Precision = 3 / (3 + 0) = 1.00. Recall = 3 / (3 + 2) = 3 / 5 =
         0.60.

      **Question 5.** The script prints:

      .. code-block:: text

         20 cells: TP 3, FP 0, FN 2, TN 15
         precision = 3/3 = 1.00
         recall    = 3/5 = 0.60

      **Question 6.** Each false positive is a good cell with a failing
      report. The inspection door stays closed, and the cell drops into the
      inspection bin, at 50 points each (``GOOD_CELL_IN_INSPECTION_BIN``):

      - Original: 2 × 50 = 100 points.
      - Lower threshold: 4 × 50 = 200 points.
      - Higher threshold: 0 × 50 = 0 points.

      **Question 7.** The false negatives pass: 1 (original), 0 (lower
      threshold), 2 (higher threshold). GP1 requires the check kit quality
      call before the AGV moves, so a passed defective cell that goes into a
      kit is caught at the AGV inspection station. It costs a recycled tray,
      with its good cells, and the time to rebuild the kit. Only if the
      rebuild does not finish before the time limit does it cost the kit,
      5000 / 3 = 1666.7 points of base in the lecture's trial
      (:math:`k_d = 3`), and, through the bonus gate, every bonus (1534.58
      points in Run 1): 3201.25 points in all. So the lower threshold pays
      100 more points of penalties than the original, every run, to save one
      tray rebuild and remove that risk. The higher threshold saves 100
      points of penalties and doubles the rebuilds. Which setting wins
      depends on how often a rebuild misses the time limit, which your own
      runs can measure. These prices hold for this trial; another trial
      needs its own arithmetic.

      **Question 8.** Recall = 0 / 5 = 0. Precision is 0 / 0, which is not
      defined: there are no flags to judge. The script stops with a
      ``ZeroDivisionError`` on the precision line. A report should say
      "undefined (no flags)" instead of a number.


.. dropdown:: Exercise 2. How Many Runs Does a 0.10 Difference Need?
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Use the standard error formula to find how many runs the GP3 and GP4
   comparison needs before a gap of 0.10 counts as evidence. The lecture
   gives the answer (:ref:`l12-runs-a-claim-needs`); work it out yourself,
   step by step.

   .. raw:: html

      <hr>

   **Part A. The class example, with more runs**

   Keep the class's success rates, 0.85 for GP3 and 0.75 for GP4, and give
   both systems the same number of runs :math:`n`.

   1. Write :math:`\mathrm{SE}_{\mathrm{diff}}` as one square root of a
      number divided by :math:`n`.
   2. Compute :math:`\mathrm{SE}_{\mathrm{diff}}` and two standard errors for
      :math:`n` = 20 and :math:`n` = 50. Is a gap of 0.10 evidence at either
      one, by the class rule?

   .. raw:: html

      <hr>

   **Part B. The number of runs**

   3. Find the smallest :math:`n` for which two standard errors of the
      difference are 0.10 or less.
   4. How many runs is that in total, for both systems?

   .. raw:: html

      <hr>

   **Part C. Reading the result**

   5. A team ran each system 5 times: GP3 completed 5 of 5, GP4 4 of 5.
      Compute the two success rates, their standard errors and
      :math:`\mathrm{SE}_{\mathrm{diff}}`. What can the team say?

   .. dropdown:: Solution
      :color: success

      **Question 1.** :math:`\mathrm{SE}_1^2 = 0.85 \times 0.15 / n =
      0.1275 / n` and :math:`\mathrm{SE}_2^2 = 0.75 \times 0.25 / n =
      0.1875 / n`. So

      .. math::

         \mathrm{SE}_{\mathrm{diff}} = \sqrt{(0.1275 + 0.1875) / n}
                                     = \sqrt{0.315 / n}

      **Question 2.**

      1. :math:`n = 20`: 0.315 / 20 = 0.01575, and
         :math:`\sqrt{0.01575}` = 0.1255. Two standard errors: 0.251. (The
         slide gets 0.126 for one SE from the rounded 0.080 and 0.097.)
      2. :math:`n = 50`: 0.315 / 50 = 0.0063, and :math:`\sqrt{0.0063}` =
         0.0794. Two standard errors: 0.159.
      3. A gap of 0.10 is smaller than two standard errors in both cases, so
         it is not evidence at either :math:`n`.

      **Question 3.** Two standard errors must be at most 0.10:

      1. :math:`2 \sqrt{0.315 / n} \le 0.10`, so
         :math:`\sqrt{0.315 / n} \le 0.05`.
      2. Square both sides: :math:`0.315 / n \le 0.0025`.
      3. :math:`n \ge 0.315 / 0.0025` = 126.

      So each system needs at least **126 runs**.

      **Question 4.** 2 × 126 = 252 runs in total.

      **Question 5.**

      1. Rates: 5 / 5 = 1.00 and 4 / 5 = 0.80. The difference is 0.20.
      2. SE for GP3: :math:`\sqrt{1.00 \times 0.00 / 5}` = 0. The formula
         says "no spread" only because the measured rate is 1.00; 5 runs
         cannot show that the true rate is 1.00.
      3. SE for GP4: :math:`\sqrt{0.80 \times 0.20 / 5} = \sqrt{0.032}` =
         0.179.
      4. :math:`\mathrm{SE}_{\mathrm{diff}} = \sqrt{0^2 + 0.179^2}` = 0.179.
         Two standard errors: 0.358.

      The gap, 0.20, is smaller than 0.358, so 5 runs each do not show that
      GP3 is better. The lecture's simulation agrees: with :math:`n = 5`, a
      system whose true rate is 0.80 measures anywhere from 0.40 to 1.00 in
      the middle 95% of experiments. With 5 runs, report the counts and say
      that they cannot separate the two systems.


.. dropdown:: Exercise 3. Change n and the True Rate in the Simulation
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Use ``success_spread.py`` to see how the true rate changes the spread,
   and to check Exercise 2's 126 runs by simulation.

   .. raw:: html

      <hr>

   **Part A. A different true rate**

   1. Before running anything, use the formula to predict the spread at
      :math:`n = 20` for a true rate of 0.95 and of 0.50.
   2. Set ``P_TRUE = 0.95`` and run the script. Then set ``P_TRUE = 0.50``
      and run it again. Compare the ``spread`` column with your predictions.
   3. For each true rate, how often do two equal systems with 20 runs each
      differ by 0.10 or more? Why is it rarer at 0.95?

   .. raw:: html

      <hr>

   **Part B. Two different systems**

   Set ``P_TRUE`` back to 0.80. Now simulate the class example as if the true
   rates were known: GP3 succeeds 85% of the time and GP4 75% of the time.
   Add this block after the "Two equal systems" part, just before the line
   ``out = pathlib.Path(...)``:

   .. code-block:: python

      print("GP3 true 0.85, GP4 true 0.75:")
      for n in [20, 50, 126, 250]:
          a = rng.binomial(n, 0.85, size=REPEATS) / n
          b = rng.binomial(n, 0.75, size=REPEATS) / n
          two_se = 2 * math.sqrt((0.85 * 0.15 + 0.75 * 0.25) / n)
          print(f"  n = {n:3d}: 2 SE {two_se:.3f}, "
                f"gap above 2 SE {np.mean(a - b > two_se):.1%}, "
                f"GP4 looks as good or better {np.mean(b >= a):.1%}")

   4. Before running it: at :math:`n = 126`, where two standard errors equal
      the true gap of 0.10, in what share of comparisons do you expect the
      measured gap to pass two standard errors? (Hint: around which value is
      the measured gap centered?)
   5. Run it. How often does GP4, the worse system, look as good or better at
      :math:`n = 20`?
   6. How many runs does the simulation say you need to see the 0.10
      difference in about 4 comparisons out of 5?

   .. dropdown:: Solution
      :color: success

      **Question 1.**

      1. :math:`p = 0.95`: :math:`\sqrt{0.95 \times 0.05 / 20} =
         \sqrt{0.002375}` = 0.049.
      2. :math:`p = 0.50`: :math:`\sqrt{0.50 \times 0.50 / 20} =
         \sqrt{0.0125}` = 0.112.

      **Question 2.** With ``P_TRUE = 0.95`` the script prints:

      .. code-block:: text

         True success rate 0.95, 10000 repeats per n
           n =   5: middle 95% 0.80 to 1.00, spread 0.098, formula 0.097
           n =  10: middle 95% 0.80 to 1.00, spread 0.069, formula 0.069
           n =  20: middle 95% 0.85 to 1.00, spread 0.048, formula 0.049
           n =  50: middle 95% 0.88 to 1.00, spread 0.031, formula 0.031
           n = 100: middle 95% 0.90 to 0.99, spread 0.022, formula 0.022
         Two equal systems, 20 runs each:
           gap of 0.10 or more: 25.1%
           gap above 2 SE (0.138): 6.5%

      With ``P_TRUE = 0.50``:

      .. code-block:: text

         True success rate 0.50, 10000 repeats per n
           n =   5: middle 95% 0.00 to 1.00, spread 0.223, formula 0.224
           n =  10: middle 95% 0.20 to 0.80, spread 0.156, formula 0.158
           n =  20: middle 95% 0.30 to 0.70, spread 0.111, formula 0.112
           n =  50: middle 95% 0.36 to 0.64, spread 0.070, formula 0.071
           n = 100: middle 95% 0.40 to 0.60, spread 0.050, formula 0.050
         Two equal systems, 20 runs each:
           gap of 0.10 or more: 63.4%
           gap above 2 SE (0.316): 4.4%

      At :math:`n = 20` the spreads, 0.048 and 0.111, match the predictions,
      0.049 and 0.112. The spread is largest at 0.50 and shrinks as the rate
      nears 1, because :math:`p(1 - p)` is largest at :math:`p = 0.50`
      (0.25) and small at 0.95 (0.0475).

      **Question 3.** Two equal systems differ by 0.10 or more in 25.1% of
      comparisons at 0.95, 54.8% at 0.80 (the lecture), and 63.4% at 0.50. A
      rate near 1 has a smaller spread, so chance gaps are smaller. Note
      that the share above two standard errors is 6.5% at 0.95, against 3.1%
      at 0.80: with 20 runs and a rate near 1, a measured rate can take only
      a few values, so the 2 SE rule is rougher there.

      **Question 4.** The measured gap is centered on the true gap, 0.10.
      If 0.10 is exactly two standard errors, about half the comparisons land
      above it and half below: expect about 50%.

      **Question 5.** The new lines print:

      .. code-block:: text

         GP3 true 0.85, GP4 true 0.75:
           n =  20: 2 SE 0.251, gap above 2 SE 8.4%, GP4 looks as good or better 27.4%
           n =  50: 2 SE 0.159, gap above 2 SE 26.3%, GP4 looks as good or better 12.9%
           n = 126: 2 SE 0.100, gap above 2 SE 50.5%, GP4 looks as good or better 2.6%
           n = 250: 2 SE 0.071, gap above 2 SE 79.3%, GP4 looks as good or better 0.3%

      At :math:`n = 20`, GP4 looks as good as or better than GP3 in 27.4% of
      comparisons, even though it is truly worse. The 2 SE values match
      Exercise 2 (0.251, 0.159, 0.100). At :math:`n = 126` the gap passes two
      standard errors in 50.5% of comparisons, as Question 4 predicted.

      **Question 6.** About 250 runs per system: at :math:`n = 250` the gap
      passes two standard errors in 79.3% of comparisons. So 126 runs is the
      point where a 0.10 gap **can** count as evidence, not the point where
      you will usually see it. These two-standard-error values use the true
      rates, which the simulation knows; a real test uses the measured rates.


.. dropdown:: Exercise 4. Score a Task 2 Run You Design
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Score a trial with modules by hand, check it with the calculator, and see
   what one missing module costs.

   .. raw:: html

      <hr>

   **Part A. The trial and the run**

   The trial uses the counts of the example trial file on the ARIAC
   configuration page: 3 kits, 2 modules, a 900 s time limit. It has no
   high-priority order (chosen for this exercise). The sensors are the
   lecture's, $3700. The measurements of Run 4 are chosen for this exercise:

   - All 3 kits and both modules are submitted and accepted.
   - Run time :math:`t_e` = 870 s. Average inspection report time
     :math:`\gamma` = 3.6 s.
   - 6 defective cells, 4 of them reported correctly.
   - One cell falls into the inspection conveyor bin.
   - Two robots collide for less than 5 s.

   1. Compute the base score.
   2. Compute each of the five bonuses, and their sum.
   3. Compute the penalties. (How many occurrences does the robot collision
      count?)
   4. Compute the run score.

   .. raw:: html

      <hr>

   **Part B. One module short**

   Run 3 is the same, except that only 1 of the 2 modules is submitted.

   5. Compute its run score.
   6. How many points did the missing module cost, and how do they split
      between the base and the bonuses? Compare with the 3201.25 points of
      the missing kit in the lecture.

   .. raw:: html

      <hr>

   **Part C. Check with the calculator**

   7. In a copy of ``score_calculator.py``, add the two runs just before the
      line ``out = HERE.parent ...`` and print them. Use ``hp_s=[]`` for "no
      high-priority order".

   .. dropdown:: Solution
      :color: success

      **Question 1.** Base: 5000 × 3 / 3 + 12000 × 2 / 2 = 5000 + 12000 =
      17000.

      **Question 2.**

      1. Trial time: 1000 × (1 − 870 / 900) = 1000 × 0.0333 = 33.33.
      2. Inspection speed: 500 × (1 − 3.6 / 4) = 500 × 0.10 = 50.
      3. High-priority speed: 0, because the trial has no high-priority
         order.
      4. Sensor cost: 1000 × (1 − 3700 / 9600) = 614.58, as in the lecture.
      5. Classification: 500 × 4 / 6 = 333.33.
      6. Sum: 33.33 + 50 + 0 + 614.58 + 333.33 = 1031.25.

      **Question 3.** A collision between two robots counts twice, because
      each robot records its own: 2 occurrences × 100 = 200. The cell in the
      conveyor bin: 25. Penalties: 200 + 25 = 225.

      **Question 4.** Run 4: 17000 + 1031.25 − 225 = 17806.25.

      **Question 5.** Run 3:

      1. Base: 5000 × 3 / 3 + 12000 × 1 / 2 = 5000 + 6000 = 11000.
      2. Bonuses: 0, because not every wanted module was submitted (the
         bonus gate).
      3. Penalties: the same 225.
      4. Run score: 11000 − 225 = 10775.

      **Question 6.** 17806.25 − 10775 = 7031.25 points: 6000 from the base
      (half of 12000) and 1031.25 of bonuses. The missing kit in the lecture
      cost 3201.25. A module is worth far more base than a kit here
      (12000 / 2 = 6000 against 5000 / 3 = 1666.7), which is why Task 2
      carries most of the base score in a trial with modules.

      **Question 7.** The block added to the copy:

      .. code-block:: python

         run_4 = {
             "kits_wanted": 3, "kits_done": 3,
             "modules_wanted": 2, "modules_done": 2,
             "tm": 900, "te": 870,
             "report_s": 3.6, "hp_s": [],
             "cost": cost, "defective": 6, "correct": 4,
             "events": {"CELL_IN_CONVEYOR_BIN": 1,
                        "ROBOT_COLLISION": 2},
         }
         run_3 = dict(run_4, modules_done=1)  # one module short
         r3, r4 = terms(run_3), terms(run_4)
         print(f"{'term':<27}{'Run 3':>8}{'Run 4':>8}")
         for (name, a), (_, b) in zip(rows(r3), rows(r4)):
             print(f"{name:<27}{a:>9.2f}{b:>9.2f}")

      It prints, after the lecture's lines:

      .. code-block:: text

         term                          Run 3   Run 4
         base                        11000.00 17000.00
         bonus trial time                0.00    33.33
         bonus inspection speed          0.00    50.00
         bonus high-priority speed       0.00     0.00
         bonus sensor cost               0.00   614.58
         bonus classification            0.00   333.33
         penalties                     225.00   225.00
         run score                   10775.00 17806.25


.. dropdown:: Exercise 5. What the Bonus Gate Is Worth
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Compare a slow run that finishes every kit with the lecture's Run 2, which
   dropped one kit, and find how much slower or clumsier the complete run can
   be before it loses.

   .. raw:: html

      <hr>

   **Part A. The largest possible bonus**

   1. Using the weights, what is the largest total bonus a run could earn in
      the lecture's trial? Which conditions would that need, and can a real
      run meet them?

   .. raw:: html

      <hr>

   **Part B. A slow run that finishes**

   Run 5 is the lecture's Run 1, but slow on everything (chosen for this
   exercise): run time 895 s, average inspection report time 4.5 s, and the
   high-priority kit submitted 200 s after its announcement. All three kits
   are still submitted and accepted.

   2. Compute each bonus. Which ones does the clamping set to 0?
   3. Compute the run score, and compare it with Run 2 (3183.3).
   4. Check with the calculator: ``run_5 = dict(run_1, te=895,
      report_s=4.5, hp_s=[200.0])``.

   .. raw:: html

      <hr>

   **Part C. How clumsy can it be?**

   5. Run 5 also has extra robot collisions with fixed equipment, each under
      5 s. How many extra occurrences can it have and still score more than
      Run 2?

   .. dropdown:: Solution
      :color: success

      **Question 1.** Each bonus is largest when its fraction is largest:
      trial time 1000 (if :math:`t_e = 0`), inspection speed 500 (if
      :math:`\gamma = 0`), high-priority speed 600 (if :math:`\tau = 0`),
      sensor cost 1000 (if :math:`\sigma = 0`), classification 500 (if every
      report is right). Sum: 1000 + 500 + 600 + 1000 + 500 = 3600. No real run
      takes 0 s or uses no sensors, so a real run earns less. The bonus gate
      removes all of it, whatever the run earned.

      **Question 2.**

      1. Trial time: 1000 × (1 − 895 / 900) = 1000 × 0.00556 = 5.56.
      2. Inspection speed: 500 × (1 − 4.5 / 4) = 500 × (−0.125) = −62.5,
         clamped to **0**.
      3. High-priority speed: 600 × (1 − 200 / 150) = 600 × (−0.333) =
         −200, clamped to **0**.
      4. Sensor cost: 614.58, unchanged.
      5. Classification: 375, unchanged.
      6. Bonuses: 5.56 + 0 + 0 + 614.58 + 375 = 995.14.

      **Question 3.** 5000 + 995.14 − 150 = 5845.14. That is
      5845.14 − 3183.33 = 2661.81 points more than Run 2, the fast run that
      dropped a kit.

      **Question 4.** The calculator prints:

      .. code-block:: text

         base                         5000.00
         bonus trial time                5.56
         bonus inspection speed          0.00
         bonus high-priority speed       0.00
         bonus sensor cost             614.58
         bonus classification          375.00
         penalties                     150.00
         run score                    5845.14

      **Question 5.** Each extra occurrence costs 100 points. Run 5 stays
      ahead while 5845.14 − 100 × :math:`x` > 3183.33, that is
      :math:`x` < 2661.81 / 100 = 26.6. So it can have **26** extra
      occurrences (5845.14 − 2600 = 3245.14) and still beat Run 2; at 27 it
      scores 3145.14 and loses. In this trial, finishing every order is worth
      more than any speed bonus and many penalties.


.. dropdown:: Exercise 6. A Sensor Setup over the Budget
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Price a sensor setup that goes over the $9600 budget, and find the
   cheapest way back.

   .. raw:: html

      <hr>

   **Part A. The setup**

   A team wants a lidar in each of the three lidar boxes, cameras for the VLM
   and the top shell, and extra sensors on the conveyor. Its list (chosen for
   this exercise; prices from the ARIAC sensors page):

   - 3 grade A lidars at $1500 each.
   - 2 grade A break beams at $400 each.
   - 1 grade A distance sensor at $600.
   - 5 grade A (1080p) cameras at $800 each.

   1. Compute the total cost :math:`\sigma`, step by step.
   2. Compute the sensor cost bonus and the over-budget penalty.

   .. raw:: html

      <hr>

   **Part B. The two runs with this setup**

   3. Rescore the lecture's Run 1 and Run 2 with this setup. Does the bonus
      gate remove the over-budget penalty from Run 2?
   4. How many points does Run 1 lose against the lecture's $3700 setup?

   .. raw:: html

      <hr>

   **Part C. Getting back under the budget**

   5. Swap the grade A distance sensor for a grade B one ($300). Compute the
      new cost, bonus and penalty.
   6. Instead, keep the grade A distance sensor and use five grade B (720p)
      cameras at $500 each. Compute the new cost and bonus.
   7. Check all three setups with the calculator by changing its ``SENSORS``
      list.

   .. dropdown:: Solution
      :color: success

      **Question 1.**

      1. Lidars: 3 × 1500 = $4500.
      2. Break beams: 2 × 400 = $800.
      3. Distance sensor: $600.
      4. Cameras: 5 × 800 = $4000.
      5. Total: 4500 + 800 + 600 + 4000 = $9900, which is $300 over the
         budget.

      **Question 2.** Sensor cost bonus: 1000 × (1 − 9900 / 9600) =
      1000 × (−0.03125) = −31.25, clamped to **0**. Over-budget penalty:
      1000 × (9900 / 9600 − 1) = 1000 × 0.03125 = **31.25**, that is
      300 × 0.104 points.

      **Question 3.**

      1. Run 1: 5000 + (300 + 125 + 120 + 0 + 375) − (150 + 31.25) =
         5000 + 920 − 181.25 = 5738.75.
      2. Run 2: 3333.33 + 0 − 181.25 = 3152.08.

      No. In ``scoring.py`` the bonus gate sets only the bonuses to 0;
      ``score_penalties`` charges the over-budget penalty in every run, so
      Run 2 pays it too.

      **Question 4.** 6384.58 − 5738.75 = 645.83 points: the 614.58 sensor
      bonus it no longer earns, plus the 31.25 penalty.

      **Question 5.** 9900 − 600 + 300 = $9600, exactly the budget. Bonus:
      1000 × (1 − 9600 / 9600) = 0. Penalty: 1000 × (9600 / 9600 − 1) = 0.
      Run 1 scores 5000 + 920 − 150 = 5770.

      **Question 6.** Cameras: 5 × 500 = $2500, so the total is
      9900 − 4000 + 2500 = $8400. Bonus: 1000 × (1 − 8400 / 9600) =
      1000 × 0.125 = 125. Run 1 scores 5000 + 920 + 125 − 150 = 5895.
      Whether 720p images are good enough for the VLM and the top shell is a
      separate question, to measure with the precision, recall and position
      error of this lecture.

      **Question 7.** The changed list for Part A:

      .. code-block:: python

         SENSORS = [
             ("lidar, grade A", 1500),
             ("lidar, grade A", 1500),
             ("lidar, grade A", 1500),
             ("break beam, grade A", 400),
             ("break beam, grade A", 400),
             ("distance, grade A", 600),
         ] + [("camera, 1080p", 800)] * 5

      The calculator prints (Part A):

      .. code-block:: text

         Sensor cost: $9900 (budget $9600)
         term                          Run 1   Run 2
         base                         5000.0  3333.3
         bonus trial time              300.0     0.0
         bonus inspection speed        125.0     0.0
         bonus high-priority speed     120.0     0.0
         bonus sensor cost               0.0     0.0
         bonus classification          375.0     0.0
         penalties                     181.2   181.2
         run score                    5738.8  3152.1
         Run 1 minus Run 2: 2586.67 = base 1666.67 + bonuses 920.00
         Over-budget penalty at $10400: 83.3

      The table rounds to one decimal: 181.25 prints as 181.2 and 5738.75 as
      5738.8. With the grade B distance sensor (Question 5) the first line is
      ``Sensor cost: $9600 (budget $9600)``, the penalties are 150.0 and Run 1
      scores 5770.0. With the 720p cameras (Question 6) it is
      ``Sensor cost: $8400 (budget $9600)``, the sensor bonus is 125.0 and
      Run 1 scores 5895.0. Run 2 scores 3183.3 in both.
