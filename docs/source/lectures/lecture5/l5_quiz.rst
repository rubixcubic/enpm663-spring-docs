====================================================
Quiz
====================================================

.. important::

   **This quiz is not submitted and it is not graded.** It is a self-check,
   and the answers are published so you can use it that way.

   The graded quizzes are the **five in-class quizzes** listed in the
   :doc:`syllabus </syllabus/index>`. Those are closed-notes, given at the
   start of class, and they **use different questions from these**. Quiz 3,
   at the start of Week 7, covers L5 and L6. Working through this page is
   good preparation for it. Memorizing the answers below is not.

This quiz covers Lecture 5: the ARIAC sensors and the budget, point clouds in
ROS 2, lidar geometry, the cylinder-fit defect detector, the inspection report,
the voltage readings, and precision and recall. Every question can be answered
from the slides shown in class.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences, or the steps of a
     calculation.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1 to 12)
===================================

.. admonition:: Question 1
   :class: hint

   A team declares a lidar at 10 Hz with :math:`H` = 10 and :math:`V` = 20
   samples. Which grade does ARIAC's billing code (``Lidar.grade`` in
   ``ariac_setup/structures.py``) give it?

   A. Grade A

   B. Grade B

   C. Grade C

   D. None: ARIAC refuses it

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   10 × 20 = 200 samples. The Sensors page lists grade C as
   :math:`H \times V \leq 200`, but the code bills exactly 200 samples as
   grade B. For grade C, use at most 199 samples. ARIAC refuses a lidar with
   more than 400 samples, a rate other than 10 or 20 Hz, or a pose outside
   the boxes; this one has none of those.


.. admonition:: Question 2
   :class: hint

   The ARIAC lidar model (``lidar/model.sdf``) has a range of 0.04 to 0.2 m.
   What does that mean for placing a lidar?

   A. Nothing: the team configuration file sets the range.

   B. The lidar must be aimed within 20 cm of the cell it measures.

   C. The lidar must sit in box C, over the belt.

   D. The lidar must scan at 20 Hz.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The team configuration file sets only the samples, angles, pose and rate.
   It cannot change the range, so a surface more than 0.2 m away gives no
   point.


.. admonition:: Question 3
   :class: hint

   A ``PointCloud2`` holds 400 points, each with the fields x, y and z as
   4-byte floats, in one row. What is ``row_step``?

   A. 12 bytes

   B. 400 bytes

   C. 1200 bytes

   D. 4800 bytes

.. dropdown:: Answer
   :class-container: sd-border-success

   **D**.

   ``point_step`` is 3 × 4 = 12 bytes per point. One row of 400 points is
   400 × 12 = 4800 bytes, as ``pc2_roundtrip.py`` printed.


.. admonition:: Question 4
   :class: hint

   ``read_points_numpy(msg, field_names=["x", "y", "z"], skip_nans=True)``
   reads a cloud in which one row is NaN and 136 rays that hit nothing are
   ``inf``. What does ``skip_nans=True`` remove?

   A. All 137 rows that are not finite

   B. Only the NaN row

   C. Only the 136 ``inf`` rows

   D. Nothing: it only marks them

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The demo read back 399 rows, 136 of them still not finite.
   ``np.isfinite`` removed the rest, leaving 263.


.. admonition:: Question 5
   :class: hint

   ``buf.lookup_transform("world", "lidar_a_frame", rclpy.time.Time())``
   returns a transform. What does it do to a point?

   A. Maps a point in the lidar's frame into the world frame.

   B. Maps a point in the world frame into the lidar's frame.

   C. Maps a point from one lidar's frame into another lidar's frame.

   D. Nothing until the cell's frame is published.

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   The first argument is the target frame (``world``) and the second is the
   source frame (``lidar_a_frame``), so the result takes lidar points into the
   world. ARIAC publishes no frame for a cell.


.. admonition:: Question 6
   :class: hint

   The docs' example lidar has :math:`H` = 50 samples from −1.57 to 1.57 rad.
   What is the angle between neighboring horizontal rays?

   A. 3.14 / 50 = 0.063 rad

   B. 3.14 / 49 = 0.064 rad

   C. 1.0 / 7 = 0.143 rad

   D. 1.57 / 50 = 0.031 rad

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   :math:`\Delta = (a_{\max} - a_{\min}) / (N - 1)`: 50 rays have 49 gaps
   between them. 0.143 rad is the vertical step (8 samples over 1.0 rad).


.. admonition:: Question 7
   :class: hint

   The belt runs at 0.1 m/s and a lidar scans at 10 Hz. How far does the cell
   move between two scans?

   A. 1 mm

   B. 5 mm

   C. 10 mm

   D. 100 mm

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   :math:`v / f` = 0.1 / 10 = 0.01 m = 10 mm. At 20 Hz it would be 5 mm.


.. admonition:: Question 8
   :class: hint

   With a threshold of 0.9 mm, a point on a cell has residual
   :math:`d` = −1.2 mm. What does the detector do with it?

   A. Ignores it: negative residuals are noise.

   B. Flags it as a set-in point, a candidate for a dent or a scratch.

   C. Flags it as a sticking-out point, a candidate for a bulge.

   D. Reports a dent at once.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   :math:`|d|` = 1.2 mm is above 0.9 mm, so the point is flagged. Negative
   :math:`d` means the surface is set in. One point is not yet a defect: step
   7 needs a cluster of at least 3 flagged points within 3 mm.


.. admonition:: Question 9
   :class: hint

   A cluster of set-in points spreads about 6 times as far along the cell as
   across it. How does the demo detector classify it?

   A. Dent

   B. Bulge

   C. Scratch

   D. Not a defect

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Set in and long and narrow is a scratch. The demo calls a cluster long when
   its spread in one direction is more than 2.5 times its spread in the
   other. A bulge sticks out.


.. admonition:: Question 10
   :class: hint

   Your node submits a cell's report when that cell is already at
   :math:`x` = 1.1 m. What happens?

   A. The report is attached to that cell, and the door opens late.

   B. ARIAC rejects the report.

   C. The report lands on the next cell upstream that has no report, and the
      cell at 1.1 m, which had no report at the door, goes into the inspection
      bin.

   D. The report is attached to the cell that was reported before it.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   ARIAC attaches a report to the cell nearest the door, upstream of
   :math:`x` = 1.0 m (plus a 5 mm margin), that has no report yet. A cell with
   a missing report is pushed into the inspection bin, which costs 50 points
   if it was good.


.. admonition:: Question 11
   :class: hint

   The average time from a cell's spawn to its report is :math:`g` = 2 s. What
   is the inspection speed bonus?

   A. 0 points

   B. 125 points

   C. 250 points

   D. 500 points

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   500 × (1 − 2 / 4) = 500 × 0.5 = 250 points. :math:`g` of 4 s or more gives
   0.


.. admonition:: Question 12
   :class: hint

   Each voltage reading has normal noise with :math:`\sigma` = 0.05 V. By about
   how much does the average of 25 readings wander?

   A. 0.002 V

   B. 0.01 V

   C. 0.016 V

   D. 0.05 V

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   :math:`\sigma / \sqrt{n}` = 0.05 / √25 = 0.05 / 5 = 0.01 V. 0.016 V is the
   value for 10 readings.


----


True or False (Questions 13 to 16)
==================================

.. admonition:: Question 13
   :class: hint

   **True or false:** ARIAC's training cell meshes agree with the Scenario
   page's statement that every defect is at least 2 mm from the normal
   surface at its furthest point.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   ``mesh_depths.py`` measured the 15 training defects at 0.84 to 2.49 mm,
   and 10 of the 15 are under 2 mm. A threshold just under 2 mm would miss
   most of them.


.. admonition:: Question 14
   :class: hint

   **True or false:** With two lidars, raising the threshold from 0.9 mm to
   1.5 mm caught the three defects that 0.9 mm missed.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   At 1.5 mm the detector missed 4, one more than at 0.9 mm. Each of the
   three misses sat within 0.26 rad of :math:`\theta` = 0 or :math:`\pm\pi`.
   Points landed on each, but at most one per defect passed 0.9 mm, and a
   cluster needs 3. A higher threshold flags fewer points, not more; the
   four-lidar layout caught all 56.


.. admonition:: Question 15
   :class: hint

   **True or false:** During a voltage tester malfunction, the tester stops
   publishing.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The Challenges page says it stops, but ``voltage_tester_plugin.cpp`` keeps
   publishing, with voltage −1 and ``operation_status`` MALFUNCTIONING (2).
   Skip those readings, and the 0 V readings with no cell in the tester.


.. admonition:: Question 16
   :class: hint

   **True or false:** A report with ``passed = false`` and an empty
   ``defects`` list is enough to reject a cell.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   Classifying is optional: ``passed = false`` alone rejects the cell. The
   defect list earns the classification bonus, which needs the right number
   of defects, each matching in type, in :math:`z` within 5 mm and in
   :math:`\theta` within 0.26 rad.


----


Short Answer (Questions 17 to 19)
=================================

.. admonition:: Question 17
   :class: hint

   A team chooses two grade A lidars, a grade A distance sensor and a 720p
   camera. Compute the total cost and the sensor cost bonus. What must the
   team also do to earn the bonus?

.. dropdown:: Answer
   :class-container: sd-border-success

   1. Lidars: 2 × $1500 = $3000.
   2. Total: $3000 + $600 + $500 = $4100, under the $9600 budget.
   3. Bonus: 1000 × (1 − 4100 / 9600) = 1000 × 0.573 = 572.9 points.

   The bonus counts only if the team submitted every kit and module the trial
   asked for.


.. admonition:: Question 18
   :class: hint

   A detector is tested on 100 cells, 20 of them defective. It rejects 18
   cells, and 16 of those are defective. Find TP, FP, FN and TN, then
   precision and recall. What do the false positives cost in ARIAC?

.. dropdown:: Answer
   :class-container: sd-border-success

   1. TP = 16, FP = 18 − 16 = 2, FN = 20 − 16 = 4,
      TN = 100 − 16 − 2 − 4 = 78.
   2. Precision = 16 / 18 = 0.89. Recall = 16 / 20 = 0.80.
   3. Each false positive puts a good cell in the inspection bin:
      2 × 50 = 100 points. The 4 misses can each fail a kit.


.. admonition:: Question 19
   :class: hint

   The demo detector fits the circle for the cell's axis twice. Why, and what
   does the second fit leave out?

.. dropdown:: Answer
   :class-container: sd-border-success

   A defect moves the points near it in or out, and a least-squares fit uses
   every point, so the first fit's axis is pulled toward the defect. The
   second fit leaves out the points that look defective (:math:`|d|` above
   the threshold), so the axis comes from the normal surface, and the
   residuals of the defect points are measured from it.
