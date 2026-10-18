====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes, the four group projects and
   the final demo listed in the :doc:`syllabus </syllabus/index>`.

Six take-home exercises on the L5 slides and scripts. Exercises 1, 3 and 6
are on paper: lidar point spacing and point count, the confusion matrix with
precision and recall, and what the four-lidar layout costs against the
two-lidar layout. Exercises 2 and 4 change the scripts: a grade C lidar
layout in ``point_count.py``, and lower thresholds in
``precision_recall.py``; Exercise 2 also works the two-sensor-setup budget
trade-off on paper. Exercise 5 works the voltage-averaging probability on
paper and checks it with ``voltage_average.py``. For every script exercise,
**predict the output first, write it down, then run the script.**

.. note::

   The scripts are on the :doc:`code page <l5_code>`. Work on a copy, so the
   original still gives the output in the notes. Every output below was
   measured on 2026-10-12 (Exercise 4 run A rerun on 2026-10-18) with Python
   3.12.3 and NumPy 1.26.4. All point
   clouds and voltage readings in these scripts are **synthetic**: made in
   NumPy, not by ARIAC. The scripts use fixed random seeds, so your outputs
   should match the ones below.


.. dropdown:: Exercise 1. Point Spacing and Point Count for a 16 by 25 Scan
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Predict how many points of one scan land on a cell, from the angular step
   and the distance, then check the estimate against the ray casting in
   ``point_count.py``.

   .. raw:: html

      <hr>

   **Specification**

   A lidar (chosen for this exercise) has :math:`H` = 16 samples from −0.15
   to 0.15 rad and :math:`V` = 25 samples from −0.4 to 0.4 rad, at 20 Hz. The
   cell's axis is :math:`D` = 0.1 m in front of it, as in the lecture's
   worked example. The cell has radius 10.5 mm and length 70 mm, and spans
   about 0.21 rad across and 0.67 rad up from 0.1 m (see
   :ref:`l5-spacing-example`).

   .. raw:: html

      <hr>

   **Parts**

   1. How many samples does the lidar have, and which grade does ARIAC bill
      it as?
   2. Compute the horizontal and vertical angular steps, and the spacing
      between neighboring points on the cell in each direction.
   3. Estimate how many points of one scan land on the cell.
   4. In a copy of ``point_count.py``, add this line to ``LAYOUTS``, after
      the ``"narrow 10x40"`` line, and run it:

      .. code-block:: python

         "narrow 16x25": ((16, -0.15, 0.15), (25, -0.4, 0.4)),

      Does the count fall inside your estimate?
   5. The 10 by 40 layout puts 212 points on the cell with steps of 0.033 and
      0.021 rad. Which of the two layouts would you pick for a cell moving
      along the belt, and why?

   .. dropdown:: Solution
      :color: success

      **Part 1.** 16 × 25 = 400 samples. At 20 Hz with at most 400 samples,
      ARIAC bills it as grade A ($1500).

      **Part 2.**

      1. Horizontal step: (0.15 − (−0.15)) / (16 − 1) = 0.3 / 15 = 0.020 rad.
      2. Vertical step: (0.4 − (−0.4)) / (25 − 1) = 0.8 / 24 = 0.033 rad.
      3. Spacing at 0.1 m = 100 mm: 0.020 × 100 = 2.0 mm across, and
         0.033 × 100 = 3.3 mm up.

      **Part 3.**

      1. Columns on the cell: 0.21 / 0.020 = 10.5, so 10 or 11.
      2. Rows on the cell: 0.67 / 0.033 = 20.1, so 20 or 21.
      3. Points: from 10 × 20 = 200 to 11 × 21 = 231.

      Both scan ranges are wider than the cell (0.3 rad against 0.21 rad, and
      0.8 rad against 0.67 rad), so the cell does not overflow the scan.

      **Part 4.** The new line of output:

      .. code-block:: text

         narrow 16x25: steps 0.020 and 0.033 rad, 216 of 400 rays hit the cell

      216 is inside the 200 to 231 estimate. The other lines are unchanged.
      You may also see ``RuntimeWarning: invalid value encountered in
      multiply`` from ``synth.py``. With 25 vertical samples from −0.4 to 0.4,
      one row of rays is at exactly 0 rad, so its :math:`z` direction is 0,
      and a ray that misses gives 0 × inf = NaN. That row is dropped like any
      other miss, so the count does not change.

      **Part 5.** The 10 by 40 layout. The belt moves the cell 5 mm between
      scans at 20 Hz, and each scan sees it from a slightly different angle,
      so stacking scans fills in the horizontal direction. Nothing fills in
      the vertical direction. The 10 by 40 layout spends its samples there:
      2.1 mm up instead of 3.3 mm, for about the same number of points per
      scan (212 against 216).


.. dropdown:: Exercise 2. A Grade C Layout: Fewer Points for Less Money
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Change the lidar layout and scan rate in ``point_count.py`` to a grade C
   lidar, predict how many points a whole pass gives, and weigh them against
   the sensor cost bonus.

   .. raw:: html

      <hr>

   **Specification**

   Start from the two demo lidars with the 10 by 40 layout (:math:`H` 10 over
   −0.15 to 0.15 rad, :math:`V` 40 over −0.4 to 0.4 rad, 20 Hz). The lecture's
   output for them:

   .. code-block:: text

      narrow 10x40: steps 0.033 and 0.021 rad, 212 of 400 rays hit the cell
      two lidars, 10x40: 3072 points, seen at t = 0.75 to 1.25

   The grade C version (chosen for this exercise) keeps :math:`H` 10 over the
   same range and uses :math:`V` = 19 samples over −0.4 to 0.4 rad, at 10 Hz.

   .. raw:: html

      <hr>

   **Parts**

   1. Why 19 vertical samples and not 20? Why must the rate change too?
   2. Predict how many rays of one grade C scan hit the cell.
   3. Predict the number of points in a whole pass of the two grade C lidars.
      Scans happen at multiples of 1 / :math:`f` after spawn.
   4. In a copy of ``point_count.py``, add this line to ``LAYOUTS``:

      .. code-block:: python

         "grade C 10x19": ((10, -0.15, 0.15), (19, -0.4, 0.4)),

      and these lines right after the ``PASSES`` dictionary:

      .. code-block:: python

         grade_c = S.two_lidars(x, *LAYOUTS["grade C 10x19"])
         for lidar in grade_c:
             lidar.rate = 10
         PASSES["two lidars, 10x19, 10 Hz"] = grade_c

      Run it and compare with parts 2 and 3.
   5. How many points does the sensor cost bonus gain if the team swaps its
      two grade A lidars for these two grade C lidars?
   6. Each good cell wrongly sent to the inspection bin costs 50 points
      (``GOOD_CELL_IN_INSPECTION_BIN``). How many wrongly rejected good
      cells would it take to lose more than the gain from part 5?

   .. dropdown:: Solution
      :color: success

      **Part 1.** 10 × 20 = 200 samples, and ARIAC's billing code
      (``Lidar.grade``) bills exactly 200 samples as grade B. 10 × 19 = 190
      stays at or below 199. The code gives grade A to any lidar at exactly
      20 Hz, whatever its samples, so the rate must change to 10 Hz for grade
      C.

      **Part 2.**

      1. Steps: 0.3 / 9 = 0.033 rad across; 0.8 / 18 = 0.044 rad up.
      2. Columns: 0.21 / 0.033 = 6.3, so 6 or 7. Rows: 0.67 / 0.044 = 15.2,
         so 15 or 16.
      3. Points: from 6 × 15 = 90 to 7 × 16 = 112.

      **Part 3.**

      1. At 20 Hz the cell is seen at t = 0.75 to 1.25 s, every 0.05 s:
         (1.25 − 0.75) / 0.05 + 1 = 11 scan times.
         3072 / 11 = 279 points per scan time from the two lidars.
      2. Part 2 estimates about 100 rays on the cell per grade C scan (the
         middle of 90 to 112), against 212 for the 10 by 40 scan: a ratio of
         100 / 212.
      3. At 10 Hz, scans happen every 0.1 s. Inside 0.75 to 1.25 s they fall
         at 0.8, 0.9, 1.0, 1.1 and 1.2 s: 5 scan times, not 11.
      4. Prediction: 279 × (100 / 212) × 5 = 659 points.

      **Part 4.** The two new lines of output:

      .. code-block:: text

         grade C 10x19: steps 0.033 and 0.044 rad, 100 of 190 rays hit the cell
         two lidars, 10x19, 10 Hz: 660 points, seen at t = 0.80 to 1.20

      100 is inside the 90 to 112 estimate, and 660 is within 1 point of the
      prediction. The grade C pass gives 660 / 3072 = 21% of the points. The
      ``RuntimeWarning`` from Exercise 1 may appear here too, for the same
      reason (19 samples from −0.4 to 0.4 include 0 rad); it does not change
      the counts.

      **Part 5.** The two lidars cost 2 × $1500 = $3000 at grade A and
      2 × $1000 = $2000 at grade C: $1000 less. The bonus is
      1000 × (1 − cost / 9600), so it rises by 1000 × 1000 / 9600 = 104.2
      points. That is about two good cells wrongly rejected (2 × 50 = 100
      points). Whether the trade pays off depends on what your detector
      misses with a fifth of the points, which only your own measurement can
      say.

      **Part 6.** 104.2 / 50 = 2.08, so three wrongly rejected good cells
      (3 × 50 = 150 points) already cost more than the 104.2-point gain, and
      two (2 × 50 = 100 points) nearly do. A grade C lidar has a fifth of
      the points of grade A (part 4), so the cheaper layout is worth it only
      if your own measurement shows it does not cost you two or more good
      cells, out of however many your team inspects.


.. dropdown:: Exercise 3. Confusion Matrix, Precision and Recall
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Fill in a confusion matrix from a test run, compute precision and recall,
   put each error into ARIAC points, and read the same numbers off the
   lecture's demo output.

   .. raw:: html

      <hr>

   **Specification**

   A team tests its detector on 60 cells, 12 of them defective. The detector
   rejects 14 cells, and 10 of those are defective. (Numbers chosen for this
   exercise.) The trial asks for 3 kits, as in the lecture's example, so a kit
   is worth 5000 / 3 = 1667 base points.

   .. raw:: html

      <hr>

   **Parts**

   1. Find TP, FP, FN and TN.
   2. Compute precision and recall.
   3. How much would one more missed defect move recall?
   4. What do the false positives cost in ARIAC points? What can the false
      negatives cost?
   5. From the lecture's ``precision_recall.py`` output for two lidars,
      compute precision and recall by hand for the 0.5 mm and 1.5 mm lines,
      and check them against the printed values.

      .. literalinclude:: outputs/precision_recall.txt
         :language: text
         :lines: 1-12

   6. Going from 0.9 mm to 0.5 mm with two lidars, what does the team give
      up and what does it gain?

   .. dropdown:: Solution
      :color: success

      **Part 1.**

      1. TP = defective and rejected = 10.
      2. FP = rejected but good = 14 − 10 = 4.
      3. FN = defective but passed = 12 − 10 = 2.
      4. TN = the rest = 60 − 10 − 4 − 2 = 44.

      Check: 10 + 4 + 2 + 44 = 60 cells.

      **Part 2.** Precision = TP / (TP + FP) = 10 / 14 = 0.71. Recall =
      TP / (TP + FN) = 10 / 12 = 0.83.

      **Part 3.** Recall would become 9 / 12 = 0.75, a drop of
      1 / 12 = 0.083. With only 12 defective cells, each one moves recall by
      more than 0.08, so report the counts with the ratios.

      **Part 4.** Each false positive sends a good cell into the inspection
      bin: 4 × 50 = 200 points. Each false negative lets a defective cell
      through the door. If it goes into a kit, the kit fails at submission:
      up to 1667 base points per kit, and up to 2 × 1667 = 3333 if the two
      missed cells end up in different kits.

      **Part 5.**

      1. 0.5 mm: precision = 55 / (55 + 5) = 55 / 60 = 0.917, printed as
         0.92. Recall = 55 / (55 + 1) = 55 / 56 = 0.982, printed as 0.98.
      2. 1.5 mm: precision = 52 / (52 + 0) = 1.00. Recall =
         52 / (52 + 4) = 52 / 56 = 0.929, printed as 0.93.

      **Part 6.**

      1. Given up: 5 false alarms instead of 0, so 5 × 50 = 250 points. The
         classification count also falls from 51 to 47 of 56:
         500 × 4 / 56 = 35.7 points of the classification bonus.
      2. Gained: 2 fewer missed defects (FN 1 instead of 3).
      3. One missed cell that reaches a kit costs about 1667 points, more than
         the 250 + 35.7 = 285.7 given up. This is why the lecture says to
         favor recall: 0.5 mm is the better choice if either of those two
         cells would have reached a kit.


.. dropdown:: Exercise 4. Lower the Threshold for Shallow Defects
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Change the threshold in ``precision_recall.py`` for the set of shallow
   defects, predict what happens to the misses and the false alarms, and
   explain why the calibration rule is cautious.

   .. raw:: html

      <hr>

   **Specification**

   Set 2 has 200 synthetic cells, 55 defective, with defects 0.8 to 2.5 mm
   deep, the range measured in ARIAC's meshes. With four lidars at 0.9 mm the
   lecture got:

   .. literalinclude:: outputs/precision_recall.txt
      :language: text
      :lines: 16-22

   On 20 good cells with four lidars, ``calibrate.py`` found the largest
   :math:`|d|` per cell from 0.63 to 0.81 mm. The detector flags points with
   :math:`|d|` above the threshold, and reports a defect only for a cluster of
   at least 3 flagged points within 3 mm of each other.

   The change: in a copy of ``precision_recall.py``, the last call to
   ``score`` is

   .. code-block:: python

      missed = score(truths, LAYOUTS["four lidars"], 0.0009, rng)

   Run A changes ``0.0009`` to ``0.0007``. Run B changes it to ``0.0005``.
   Changing a threshold value does not change the cells or the noise, so every
   other line of the output stays the same. Each run of the script took about
   4 minutes (252 s) on the instructor's PC (Intel Core i9-14900HX).

   .. raw:: html

      <hr>

   **Parts**

   1. Before running: in run A, do you expect the two missed dents (0.82 and
      0.91 mm deep) to be caught? Do you expect false alarms, given that some
      good cells have a point with :math:`|d|` up to 0.81 mm?
   2. Run A and run B. Write down TP, FP, FN, TN, precision, recall and the
      classified count for each.
   3. Why did run A have no false alarms, when the calibration rule says the
      threshold must be at least 0.9 mm?
   4. Compare run A with the original 0.9 mm line in ARIAC points: false
      alarms and the classification bonus.
   5. What is the risk of moving your GP2 threshold to 0.7 mm based on this
      one run?

   .. dropdown:: Solution
      :color: success

      **Part 1.** A dent whose deepest point is 0.82 or 0.91 mm has several
      points with :math:`|d|` above 0.7 mm near its center, so both dents
      should be caught. A good cell's largest :math:`|d|` can pass 0.7 mm, so
      a few false alarms are possible.

      **Part 2.** The new last lines (they replace the 0.9 mm line and the
      ``missed`` table; with no miss, the script prints no table):

      Run A, 0.7 mm:

      .. code-block:: text

          four lidars
           0.7 mm: TP 55 FP  0 FN  0 TN 145  precision 1.00 recall 1.00
                   classified (ARIAC rule) 54 of 55

      Run B, 0.5 mm:

      .. code-block:: text

          four lidars
           0.5 mm: TP 55 FP  9 FN  0 TN 136  precision 0.86 recall 1.00
                   classified (ARIAC rule) 49 of 55

      Precision in run B: 55 / (55 + 9) = 55 / 64 = 0.86.

      **Part 3.** The calibration rule looks at the single largest
      :math:`|d|` on each good cell. A false alarm needs more: at least 3
      flagged points within 3 mm of each other. A counting line added to a
      copy of the script (run 2026-10-12) shows what happened at 0.7 mm: 77 of
      the 145 good cells had at least one flagged point, at most 4 on one
      cell, and none of them formed a cluster of 3. The cluster step removed
      those scattered points. At 0.5 mm many more noisy points pass the
      threshold, and 9 good cells got a cluster of 3. The rule is cautious: it
      gives a threshold that flags no point at all on the good cells it
      measured.

      **Part 4.**

      1. False alarms: 0 in both, so no penalty either way.
      2. Classification: 54 of 55 instead of 51 of 55, so
         500 × 3 / 55 = 27.3 more points of the classification bonus.
      3. Recall: 1.00 instead of 0.96, 2 more defective cells caught.

      **Part 5.** The 0 false alarms come from one set of 145 good cells, with
      synthetic noise of 0.2 mm chosen for the lecture. ARIAC's lidar sets no
      noise; in simulation the spread of :math:`d` comes from the meshes and
      from your motion correction, and it may be larger or smaller. Measure
      the false alarms on your own good cells in simulation before you move
      the threshold, and report how many good cells you tested.


.. dropdown:: Exercise 5. How Many Voltage Readings to Average
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Compute how often noise pushes a good cell's reading out of range, for one
   reading and for an average, then check the numbers with
   ``voltage_average.py``.

   .. raw:: html

      <hr>

   **Specification**

   A Li-Ion cell is in range from 3.4 V to 3.8 V. Each reading has normal
   noise with :math:`\sigma` = 0.05 V, and the average of :math:`n` readings
   has a standard deviation of :math:`\sigma / \sqrt{n}`. A cell's true
   voltage is 3.77 V (chosen for this exercise). The tester publishes one
   reading every 0.1 s.

   The share of a normal distribution more than :math:`z` standard
   deviations above its mean (computed with the error function):

   .. list-table::
      :header-rows: 1
      :class: compact-table

      * - :math:`z`
        - 0.4
        - 0.6
        - 1.2
        - 1.9
        - 2.33
        - 2.4
      * - Share above
        - 0.345
        - 0.274
        - 0.115
        - 0.029
        - 0.0099
        - 0.008

   .. raw:: html

      <hr>

   **Parts**

   1. What is the probability that one reading lands above 3.8 V?
   2. What is the probability that the average of 10 readings lands above
      3.8 V?
   3. What is the smallest :math:`n` for which the average lands above 3.8 V
      with probability below 0.01? How long does the tester take to publish
      that many readings?
   4. In a copy of ``voltage_average.py``, change ``TRUE_V`` from 3.78 to
      3.77 and run it. Then also change ``(trials, 10)`` to
      ``(trials, 16)`` and run it again. Compare with parts 1 to 3.

   .. dropdown:: Solution
      :color: success

      **Part 1.**

      1. 3.8 V is 3.8 − 3.77 = 0.03 V above the true voltage.
      2. 0.03 / 0.05 = 0.6 standard deviations.
      3. Probability: 0.274.

      **Part 2.**

      1. The average of 10 has a standard deviation of
         0.05 / √10 = 0.0158 V.
      2. 0.03 / 0.0158 = 1.9 standard deviations.
      3. Probability: 0.029.

      **Part 3.**

      1. A probability below 0.01 needs :math:`z` of at least 2.33
         (share 0.0099).
      2. So 0.03 / (0.05 / √n) ≥ 2.33, which gives √n ≥ 2.33 × 0.05 / 0.03 =
         3.88, and n ≥ 3.88 × 3.88 = 15.1.
      3. The smallest whole number is n = 16: 0.05 / √16 = 0.0125 V, and
         0.03 / 0.0125 = 2.4 standard deviations, probability 0.008.
      4. Time: 16 × 0.1 s = 1.6 s of real time, against 1 s for 10 readings.

      **Part 4.** With ``TRUE_V = 3.77``:

      .. code-block:: text

         100000 trials, true voltage 3.77 V
           one reading above 3.8 V:     0.274
           average of 10 above 3.8 V:   0.029
           spread of the average of 10: 0.0158 V
         stream: 17 messages, 12 valid
            0.00 -0.11  3.70  3.77  3.84  3.71  3.77  3.81 -1.00
           -1.00 -1.00  3.76  3.77  3.77  3.79  3.74  3.76
           average of the last 10 valid: 3.772 V -> in range

      With ``(trials, 16)`` as well, the first four lines become:

      .. code-block:: text

         100000 trials, true voltage 3.77 V
           one reading above 3.8 V:     0.274
           average of 10 above 3.8 V:   0.008
           spread of the average of 10: 0.0125 V

      The labels still say "10" because they are fixed text in the
      ``print`` calls; the numbers are for 16 readings. All three
      probabilities match parts 1 to 3. With 100000 trials, chance moves
      each fraction by about 0.001 to 0.002. Part 2 of the output shows the
      same stream as the lecture, 0.01 V lower, because the noise draws come
      from the same seed.


.. dropdown:: Exercise 6. What the Four-Lidar Layout Costs
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Weigh the four-lidar layout's sensor cost and inspection speed against
   the two-lidar layout's, in ARIAC points, from the lecture's own outputs.

   .. raw:: html

      <hr>

   **Specification**

   From ``point_count.py``, a whole pass at 0.1 m/s and 20 Hz:

   .. literalinclude:: outputs/point_count.txt
      :language: text
      :lines: 7-8

   From ``precision_recall.py``, set 1 (200 cells, 56 defective, depth 2 to
   3 mm) at the 0.9 mm threshold:

   .. literalinclude:: outputs/precision_recall.txt
      :language: text
      :lines: 2,5-6,13-15

   The sensor cost bonus is 1000 × (1 − cost / 9600) points. The inspection
   speed bonus is 500 × (1 − t / 4) points, where :math:`t` is the time the
   cell is last seen (in seconds after spawn), and the classification bonus
   is 500 points shared equally across the set's defective cells.

   .. raw:: html

      <hr>

   **Parts**

   1. Two more grade A lidars cost 2 × $1500 = $3000. How many sensor cost
      bonus points does that give up?
   2. With two lidars the cell is last seen at t = 1.25 s; with four, at
      t = 2.55 s. How many inspection speed bonus points does that give up?
   3. Add parts 1 and 2: how many points does the four-lidar layout give up
      in total?
   4. With two lidars, 51 of 56 defective cells in set 1 are classified;
      with four, all 56 are. How many classification bonus points does that
      gain?
   5. Is the four-lidar layout worth it on set 1 alone (parts 3 and 4)? What
      would change the answer, and where does that number come from?

   .. dropdown:: Solution
      :color: success

      **Part 1.** 1000 × 3000 / 9600 = 312.5 points given up.

      **Part 2.** 500 × (1 − 1.25 / 4) = 343.75 points with two lidars;
      500 × (1 − 2.55 / 4) = 181.25 points with four. 343.75 − 181.25 =
      162.5 points given up.

      **Part 3.** 312.5 + 162.5 = 475 points given up.

      **Part 4.** 500 × (56 − 51) / 56 = 500 × 5 / 56 = 44.6 points gained.

      **Part 5.** No: 475 points given up against 44.6 gained from
      classification alone, so the four-lidar layout loses 475 − 44.6 =
      430.4 points on set 1. It would change if the cells the two-lidar
      layout missed (the ones within 0.26 rad of :math:`\theta` = 0 or
      :math:`\pm\pi`, grazing the side lidars) went on to fail a kit: one
      failed kit is about 1667 points (``scoring_weights.yaml``), which is
      more than the 475 points given up. That number is not measured here;
      it depends on where the defect sits in the kit your team builds.
