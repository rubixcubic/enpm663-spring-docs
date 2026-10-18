====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes, the four group projects and
   the final demo listed in the :doc:`syllabus </syllabus/index>`.

Six take-home exercises on the L2 toy factory. Exercise 1 is paper and
arithmetic on the class run. Exercises 2 and 3 change an option on the
command line. Exercises 4 and 5 change one line of the script. Exercise 6
follows one failure through the layers. In every exercise that runs the
script, **write your prediction down first**, then run the script and compare.

.. note::

   The script is on the :doc:`code page <l2_code>`. Work on a copy of
   ``toy_factory.py``, so the original still gives the outputs in the notes.
   The runs are exact: every number below was measured with Python 3.12.3 on
   2026-10-12, and the same command gives the same output on your machine.
   Exercises 4 and 5 show each change as the old line and the new line.


.. dropdown:: Exercise 1. Finish the Planner's Kit
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Repeat the planner's arithmetic for the rest of the class run, then
   compare what the planner measured with what the cells really were.

   .. raw:: html

      <hr>

   **Part A. Cells 4 to 6**

   Use ``outputs/three_layers.txt`` (in the notes, :ref:`l2-toy-result` and
   the step-by-step trace after it). The planner has already put cells 1 and
   3 on AGV 1, read at 3.72 V and 3.60 V. The room for slot :math:`k` is
   :math:`0.15 - 0.05 + 0.05 \times (4 - k)` V.

   1. Cell 4 reads 3.49 V. Which slot would it fill? Compute ``off`` and
      ``room``, and say where the cell goes.
   2. Do the same for cell 5 (3.47 V).
   3. Do the same for cell 6 (3.58 V).
   4. Cell 5 does not go to AGV 1. Is it recycled? Why or why not?

   .. raw:: html

      <hr>

   **Part B. Measured against true**

   The first line of ``outputs/summary.txt`` gives each cell's true voltage.

   5. Add the four readings the planner used for the kit. Then add the four
      true voltages of the same cells. How far apart are the two totals?
   6. For each of the four cells, how far is the reading from the true
      voltage? Compare with 0.016 V, how far an average of 10 readings
      wanders by chance.

   .. raw:: html

      <hr>

   **Part C. What plan only threw away**

   Plan only shipped cells 1, 2, 4 and 6 for 14.59 V, and recycled cells 3
   and 5.

   7. Swap cell 2 out of plan only's kit and put in cell 3 instead. Is the
      kit accepted? Then try cell 5 instead of cell 2.

   .. dropdown:: Solution
      :color: success

      **Question 1.** The kit has two cells, so cell 4 would fill slot 3.

      1. Kit so far: 3.72 + 3.60 = 7.32 V.
      2. With cell 4: 7.32 + 3.49 = 10.81 V.
      3. Target for three cells: 3 × 3.6 = 10.80 V.
      4. ``off``: 10.81 − 10.80 = 0.01 V above.
      5. ``room`` for slot 3: 0.10 + 0.05 × 1 = 0.15 V.
      6. 0.01 V is within 0.15 V, so **AGV 1**.

      **Question 2.** Cell 5 would fill slot 4.

      1. Kit so far: 10.81 V. With cell 5: 10.81 + 3.47 = 14.28 V.
      2. Target for four cells: 4 × 3.6 = 14.40 V.
      3. ``off``: 14.28 is 0.12 V below 14.40.
      4. ``room`` for slot 4: 0.10 + 0.05 × 0 = 0.10 V.
      5. 0.12 V is more than 0.10 V, so the cell does not fit: **AGV 2**.

      **Question 3.** Cell 6 still fills slot 4.

      1. 10.81 + 3.58 = 14.39 V, which is 0.01 V below 14.40 V.
      2. 0.01 V is within 0.10 V, so **AGV 1**. The kit is full and ships.

      The script works with the unrounded averages. An instrumented run gave
      ``off`` = +0.0114, −0.1141 and −0.0100 V for cells 4, 5 and 6: the
      same decisions.

      **Question 4.** No. 3.47 V is inside 3.4 V to 3.8 V, so the cell is
      good. It only fails the toy's fit rule, so the planner keeps it on
      AGV 2 for a later kit. The spare tray is a simplification of the toy.
      :doc:`GP1 Task 4 </assignments/gp1>` recycles instead: before placing
      a cell in range, check that the four-cell total can still land in
      14.25 V to 14.55 V, and recycle the cell if it cannot. Under that rule
      cell 5 would be placed: 10.81 + 3.47 = 14.28 V is inside the window.
      Defective cells never reach the robots: the inspection door lets a
      cell through only with a passing report.

      **Question 5.**

      1. Readings: 3.72 + 3.60 + 3.49 + 3.58 = 14.39 V.
      2. True voltages of cells 1, 3, 4 and 6: 3.73 + 3.61 + 3.52 + 3.60 =
         14.46 V.
      3. The planner's total is 0.07 V below the true total. Both are inside
         14.25 V to 14.55 V.

      **Question 6.** Cell 1: 3.72 against 3.73, 0.01 V low. Cell 3: 3.60
      against 3.61, 0.01 V low. Cell 4: 3.49 against 3.52, 0.03 V low.
      Cell 6: 3.58 against 3.60, 0.02 V low. Each one is within about twice
      0.016 V (0.032 V). This is why the planner keeps ``MARGIN`` = 0.05 V
      inside the window: its readings are not the true voltages.

      **Question 7.**

      1. Cell 3 instead of cell 2: 14.59 − 3.74 + 3.61 = 14.46 V. Accepted.
      2. Cell 5 instead of cell 2: 14.59 − 3.74 + 3.49 = 14.34 V. Accepted.

      Both cells that plan only recycled would have fixed its kit. Plan only
      lost them because it read the malfunctioning tester's −1 V as a voltage.


.. dropdown:: Exercise 2. Move the Malfunction to Tester 2
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Predict how a fixed plan behaves when the other tester malfunctions, then
   check whether one good run means the architecture works.

   .. raw:: html

      <hr>

   **Part A. Predict the plan only trace**

   You will run ``python3 toy_factory.py --arch "plan only" --tester 2``.
   Tester 2 now malfunctions from 20 s to 65 s, and tester 1 works all the
   time. Use the step times on the :doc:`code page <l2_code>` (pick 4 s,
   place 3 s, 10 readings 1 s, tray 6 s, bin 4 s) and the class trace
   ``outputs/plan_only.txt``.

   1. The plan still sends cells to testers 1, 2, 1, 2, and so on. At what
      time is each of the first five tests logged, and which tests fall
      inside 20 s to 65 s at tester 2?
   2. Which cells go to the bin as a result?
   3. The grasp failures come from their own random number generator, one
      draw per pick. Which picks fail, and where do the two ``no cell`` lines
      appear?
   4. Which four cells end on AGV 1? Using their true voltages from
      ``outputs/summary.txt``, is the kit accepted?

   .. raw:: html

      <hr>

   **Part B. Run it**

   5. Run the command and compare with your prediction.
   6. Then run ``python3 toy_factory.py --sweep 1000 --tester 2`` and
      compare the plan only row with ``outputs/sweep.txt``. Does plan only
      work when tester 2 malfunctions?

   .. dropdown:: Solution
      :color: success

      **Question 1.** Each test logs after a pick (4 s), a place (3 s) and
      10 readings (1 s): 8 s after the step starts.

      1. Cell 1 at tester 1: 0 + 8 = 8.0 s. Tray: 8 + 6 = 14 s.
      2. Cell 2 at tester 2: 14 + 8 = 22.0 s. Its readings run from 21 s to
         22 s: inside the malfunction.
      3. Cell 2 reads −1.00 V and goes to the bin: 22 + 4 = 26 s.
      4. Cell 3 at tester 1: 26 + 8 = 34.0 s. Tray: 34 + 6 = 40 s.
      5. Cell 4 at tester 2: 40 + 8 = 48.0 s, inside the malfunction. Bin:
         48 + 4 = 52 s.
      6. Cell 5 at tester 1: 52 + 8 = 60.0 s. Tray: 60 + 6 = 66 s.

      **Question 2.** Cells 2 and 4. Both are good cells (3.74 V and 3.52 V).

      **Question 3.** The grasp generator gives one number per pick, in the
      same order whatever the testers do, so the picks fail as in class: the
      6th and 7th picks fail and the 8th succeeds. So the ``no cell`` lines come at
      66 + 8 = 74.0 s (tester 2, which works again after 65 s) and, after a
      4 s move to the bin, at 78 + 8 = 86.0 s (tester 1). The 8th pick brings
      cell 6 to tester 2, logged at 90 + 8 = 98.0 s.

      **Question 4.** Cells 1, 3, 5 and 6:
      3.73 + 3.61 + 3.49 + 3.60 = 14.43 V, inside 14.25 V to 14.55 V. The kit
      is accepted, and it ships at 98 + 6 + 10 = 114 s.

      **Question 5.** The run gives:

      .. code-block:: text

            8.0 s  cell 1: tester 1 reads  3.72 V -> AGV 1
           22.0 s  cell 2: tester 2 reads -1.00 V -> bin
           34.0 s  cell 3: tester 1 reads  3.59 V -> AGV 1
           48.0 s  cell 4: tester 2 reads -1.00 V -> bin
           60.0 s  cell 5: tester 1 reads  3.48 V -> AGV 1
           74.0 s  no cell: tester 2 reads -0.03 V -> bin
           86.0 s  no cell: tester 1 reads -0.02 V -> bin
           98.0 s  cell 6: tester 2 reads  3.57 V -> AGV 1
          114.0 s  kit accepted: total 14.43 V

      **Question 6.** The sweep gives:

      .. code-block:: text

         seeds 1 to 1000, malfunction on
                       accepted    total bad cell    short  stopped  binned
         plan only          582      387       12       19        0    1554
         react only         609      346       45        0        0     177
         three layers       919        4        6        0       71      42

      Plan only accepts 582 kits, against 600 with tester 1. The difference
      is 18 kits, close to one chance-wander (15 kits in 1000, from the
      lecture), so it is not a clear change. It still recycles 1554 good cells. Seed 1
      was a lucky run: plan only did not choose cells 1, 3, 5 and 6, it got
      them. One run is one sample.


.. dropdown:: Exercise 3. No Retries
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   See what the executive's retry is worth, and why it belongs in the
   executive and not in the skill.

   .. raw:: html

      <hr>

   **Part A. One run**

   1. Look at the class trace ``outputs/three_layers.txt``. When does the
      first pick fail?
   2. Predict the last two lines of
      ``python3 toy_factory.py --arch "three layers" --retries 0``. Then run
      it.

   .. raw:: html

      <hr>

   **Part B. The sweep**

   3. You will run ``python3 toy_factory.py --sweep 1000 --retries 0``.
      Which rows of the table can change? Which cannot, and why?
   4. A kit needs at least four successful picks. Each pick succeeds with
      probability 0.8. With no retries, what is the most kits the three
      layers can accept, out of 1000?
   5. Run the sweep and compare.

   .. raw:: html

      <hr>

   **Part C. Where the retry lives**

   6. With the default ``--retries 2``, what is the chance that one pick
      fails on all three attempts?
   7. The pick skill, ``pick_from_conveyor``, never retries. It returns
      ``GRASP_FAILED`` and the executive decides. Give two reasons the
      course skills package works the same way.

   .. dropdown:: Solution
      :color: success

      **Question 1.** At 79.3 s (``pick: GRASP_FAILED, attempt 1 of 3``).
      No ``pick:`` line comes before it, so every earlier pick succeeded.

      **Question 2.** The number of retries changes nothing until a pick
      fails, so the run is the same up to 79.3 s. Then the executive has no
      attempt left:

      .. code-block:: text

           79.3 s  pick: GRASP_FAILED, attempt 1 of 1
           79.3 s  stopped cleanly: pick: GRASP_FAILED 1 times

      The executive reports the failure up, and the run stops cleanly with no
      kit.

      **Question 3.** Only the three layers row can change. ``--retries`` is
      read only by the three-layer executive; plan only and react only do not
      use it.

      **Question 4.** All four picks must succeed: 0.8 × 0.8 × 0.8 × 0.8 =
      0.8\ :sup:`4` = 0.4096. So at most about 410 kits in 1000. Fewer in
      practice, because a run that sets cells aside needs more than four
      picks, and each extra pick is another chance to stop.

      **Question 5.**

      .. code-block:: text

         seeds 1 to 1000, malfunction on
                       accepted    total bad cell    short  stopped  binned
         plan only          600      371       11       18        0    1570
         react only         612      343       45        0        0     177
         three layers       283        2        1        0      714      22

      Plan only and react only are the same as in ``outputs/sweep.txt``. The
      three layers accept 283 kits, below the 410 bound, and stop cleanly in
      714 runs (against 919 and 70 with two retries).

      **Question 6.** 0.2 × 0.2 × 0.2 = 0.008 per pick, or 8 picks in 1000.

      **Question 7.**

      1. The executive knows the context and the skill does not: how many
         tries the step is worth, whether to try another cell, whether to
         stop. In GP1 your tree retries a skill that fails once and stops
         cleanly when it keeps failing.
      2. A skill that retried on its own would hide its failures. A skill
         stops and returns a failure reason, so the failures and the ARIAC
         challenges reach your code, and recovery stays your team's job
         (L7, L11).


.. dropdown:: Exercise 4. Give Plan Only a Status Check
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Add one executive behavior to the fixed plan, and see what it fixes and
   what it does not.

   .. raw:: html

      <hr>

   **The change**

   In ``plan_only``, replace the line that ignores the status:

   .. code-block:: python

      # old
              v, _ = average(f, n)         # status not checked
              sort_cell(f, n, v)

      # new
              v, s = average(f, n)
              if s == MALFUNCTIONING:      # new rule: check the status
                  f.tester_to_tester(n, 3 - n)
                  n = 3 - n
                  v, s = average(f, n)
              sort_cell(f, n, v)

   The plan now does what the three-layer executive does at a malfunction:
   it moves the cell to the other tester and reads again. It still has no
   planner.

   .. raw:: html

      <hr>

   **Part A. Predict seed 1**

   1. Run ``python3 toy_factory.py --arch "plan only"`` in your head. What
      happens to cell 3? (The move is not logged: only ``sort_cell`` writes a
      line.)
   2. Which four cells end on AGV 1, and is the kit accepted? At what time
      does the run end?

   .. raw:: html

      <hr>

   **Part B. Predict the sweep**

   3. Before running ``python3 toy_factory.py --sweep 1000``, predict the
      plan only row: about how many in-range cells are recycled now, and about
      how many kits are accepted? Use ``outputs/sweep.txt`` and
      ``outputs/sweep_off.txt``.
   4. Run both commands and compare.
   5. Which layer did you add to plan only, and what does the result say
      about the missing one?

   .. dropdown:: Solution
      :color: success

      **Question 1.** Cell 3 reaches tester 1 during the malfunction, as in
      class. Its 10 readings end at 36.0 s with ``MALFUNCTIONING``. The new
      rule moves it to tester 2 (4 s) and reads again (1 s), so it is logged
      at 36 + 4 + 1 = 41.0 s at tester 2, at 3.60 V, the same reading the
      three-layer run got.

      **Question 2.** Cell 3 is no longer recycled, and the next pick
      succeeds, so cells 1, 2, 3 and 4 fill the tray. Their true total is
      3.73 + 3.74 + 3.61 + 3.52 = 14.60 V: **rejected**, the same kit as react
      only. Timing: cell 3 to the tray ends at 41 + 6 = 47 s; cell 4 is logged
      at 47 + 8 = 55.0 s (tester 2); tray and ship take 55 + 6 + 10 = 71 s.

      .. code-block:: text

            8.0 s  cell 1: tester 1 reads  3.72 V -> AGV 1
           22.0 s  cell 2: tester 2 reads  3.72 V -> AGV 1
           41.0 s  cell 3: tester 2 reads  3.60 V -> AGV 1
           55.0 s  cell 4: tester 2 reads  3.49 V -> AGV 1
           71.0 s  kit rejected: total 14.60 V is outside 14.25 to 14.55 V

      **Question 3.** The recycled count should drop from 1570 to near the 28
      of the no-malfunction sweep, because the status check removes the −1 V
      readings. The accepted count should stay near 600 to 613, because still
      nobody chooses the cells.

      **Question 4.**

      .. code-block:: text

         seeds 1 to 1000, malfunction on
                       accepted    total bad cell    short  stopped  binned
         plan only          615      371       13        1        0      30
         react only         612      343       45        0        0     177
         three layers       919        4        7        0       70      43

      Recycled cells: 30. Accepted: 615, 15 more than 600, which is about one
      chance-wander (15 kits in 1000): no clear change. The other two rows
      are unchanged, because the change touched only ``plan_only``.

      **Question 5.** You added an executive behavior: the failure is seen
      and handled where it is seen. It stops the loss of good cells. It does
      not choose a kit: the kit is still whatever four cells come first, so
      about 4 kits in 10 are rejected. Choosing the cells is the
      deliberative layer's job.


.. dropdown:: Exercise 5. The Planner's Margin
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Find out why the three layers shipped a bad kit on one seed, try a larger
   safety margin, and measure what it costs.

   .. raw:: html

      <hr>

   **Part A. Seed 27**

   1. Run ``python3 toy_factory.py --seed 27 --arch "three layers"`` and
      ``python3 toy_factory.py --seed 27``. Add the four readings the planner
      used for AGV 1, and the four true voltages of the same cells.
   2. Check the planner's slot 4 decision with the readings. Why did it
      accept the fourth cell?
   3. Which cell's reading is furthest from its true voltage? Compare with
      0.016 V.

   .. raw:: html

      <hr>

   **Part B. A larger margin**

   Change one constant at the top of the script:

   .. code-block:: python

      # old
      MARGIN = 0.05       # V, the planner stays this far inside the window
      # new
      MARGIN = 0.10       # V, the planner stays this far inside the window

   4. Compute the new room for slots 1 to 4.
   5. Predict the class run (seed 1, ``--arch "three layers"``): does any
      decision change? Use the class ``off`` values for cells 1 to 6: 0.12 V
      above, 0.24 V above, 0.12 V above, 0.01 V above, 0.12 V below and
      0.01 V below.
   6. Predict cell 2's destination for seed 27. Then run both seeds.

   .. raw:: html

      <hr>

   **Part C. What the margin costs**

   7. Predict how the three layers row of ``--sweep 1000`` changes: the
      ``total`` column, and the ``stopped`` column. Then run it.
   8. Is ``MARGIN = 0.10`` better than 0.05?

   .. dropdown:: Solution
      :color: success

      **Question 1.** The trace:

      .. code-block:: text

            8.0 s  cell 1: tester 1 reads  3.51 V -> AGV 1
           22.0 s  cell 2: tester 2 reads  3.53 V -> AGV 1
           36.0 s  cell 3: tester 1 MALFUNCTIONING -> move to tester 2
           41.0 s  cell 3: tester 2 reads  3.65 V -> AGV 1
           55.1 s  cell 4: tester 2 reads  3.61 V -> AGV 1
           71.1 s  kit rejected: total 14.23 V is outside 14.25 to 14.55 V

      The true voltages for seed 27 are
      ``3.51 3.48 3.66 3.58 3.77 3.67 3.55 3.68 3.63 3.54``.

      1. Readings: 3.51 + 3.53 + 3.65 + 3.61 = 14.30 V.
      2. True voltages of cells 1 to 4: 3.51 + 3.48 + 3.66 + 3.58 = 14.23 V.
      3. The true total is 0.02 V below 14.25 V, so ARIAC's check rejects it.

      **Question 2.** 14.30 V is 0.10 V below 14.40 V, and the room for slot
      4 is 0.10 V, so the cell fits, just. (The unrounded ``off`` was 0.0925 V
      below, from an instrumented run.)

      **Question 3.** Cell 2: it read 3.53 V and is really 3.48 V, 0.05 V
      high. That is about three times 0.016 V. For a normal spread, about 3
      averages in 1000 land that far from the truth (0.27% beyond three
      standard deviations), and a sweep tests thousands of cells, so some
      runs meet one. The other three readings are within 0.01 V.

      **Question 4.** ``room`` = 0.15 − 0.10 + 0.05 × (4 − k):

      1. Slot 1: 0.05 + 0.15 = 0.20 V.
      2. Slot 2: 0.05 + 0.10 = 0.15 V.
      3. Slot 3: 0.05 + 0.05 = 0.10 V.
      4. Slot 4: 0.05 + 0 = 0.05 V.

      **Question 5.** No decision changes:

      1. Cell 1: 0.12 within 0.20, AGV 1.
      2. Cell 2: 0.24 above 0.15, AGV 2.
      3. Cell 3: 0.12 within 0.15, AGV 1.
      4. Cell 4: 0.01 within 0.10, AGV 1.
      5. Cell 5: 0.12 above 0.05, AGV 2.
      6. Cell 6: 0.01 within 0.05, AGV 1.

      The run gives the same trace as ``outputs/three_layers.txt``, ending
      with ``107.3 s  kit accepted: total 14.46 V``.

      **Question 6.** Cell 1: 3.51 is 0.09 V below 3.60, within 0.20, so
      AGV 1. Cell 2: 3.51 + 3.53 = 7.04 V, 0.16 V below 7.20 V, more than
      0.15 V, so **AGV 2**. After that, the readings depend on noise you
      cannot predict by hand. The run gives:

      .. code-block:: text

            8.0 s  cell 1: tester 1 reads  3.51 V -> AGV 1
           22.0 s  cell 2: tester 2 reads  3.53 V -> AGV 2
           36.0 s  cell 3: tester 1 MALFUNCTIONING -> move to tester 2
           41.0 s  cell 3: tester 2 reads  3.65 V -> AGV 1
           55.1 s  cell 4: tester 2 reads  3.61 V -> AGV 1
           69.2 s  cell 5: tester 2 reads  3.78 V -> AGV 2
           75.3 s  tester 1 OPERATIONAL again
           83.3 s  cell 6: tester 1 reads  3.68 V -> AGV 2
           97.3 s  cell 7: tester 2 reads  3.54 V -> AGV 2
          111.3 s  cell 8: tester 1 reads  3.68 V -> AGV 3
          121.3 s  pick: GRASP_FAILED, attempt 1 of 3
          129.3 s  cell 9: tester 2 reads  3.63 V -> AGV 1
          145.3 s  kit accepted: total 14.38 V

      Check: cells 1, 3, 4 and 9 are really 3.51 + 3.66 + 3.58 + 3.63 =
      14.38 V. Cell 8 goes to AGV 3 because AGV 2 already holds four spares
      (cells 2, 5, 6 and 7).

      **Question 7.** A smaller room means fewer kits near the edge, so the
      ``total`` column should fall. It also means more cells set aside, so
      more runs use up all 10 cells: ``stopped`` should rise.

      .. code-block:: text

         seeds 1 to 1000, malfunction on
                       accepted    total bad cell    short  stopped  binned
         plan only          600      371       11       18        0    1570
         react only         612      343       45        0        0     177
         three layers       824        0        3        0      173      46

      ``total`` fell from 4 to 0 and ``bad cell`` from 7 to 3. ``stopped``
      rose from 70 to 173. An instrumented count split the 173 into 124 runs
      where the cells ran out (34 before) and 49 where a grasp failed three
      times (36 before; longer runs make more picks).

      **Question 8.** No, not for this toy: the three layers accept 824 kits
      instead of 919. The margin removed (4 − 0) + (7 − 3) = 8 rejected kits
      but added 173 − 70 = 103 clean stops, and 103 − 8 = 95 = 919 − 824. A margin trades one failure for another; the
      right value depends on how many cells you have and on what each kind of
      failure costs. L12 covers how ARIAC scores such tradeoffs.


.. dropdown:: Exercise 6. One Failure, Layer by Layer
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Trace a grasp failure that the executive cannot fix, using the three
   questions of the lecture: who sees it, who handles it, what moves up.

   .. raw:: html

      <hr>

   **Part A. Seed 113**

   1. Run ``python3 toy_factory.py --seed 113 --arch "three layers"``.
   2. Fill one row of the lecture's table (Event, Who sees it, Who handles
      it, What moves up) for this run's failure. Use the code of
      ``Executive.pick``, ``Executive.test_cell`` and ``three_layers``.
   3. The first line says cell 1 reads 3.80 V and goes to the bin, though
      3.80 V is the top of the 3.4 V to 3.8 V range. How can that be?

   .. raw:: html

      <hr>

   **Part B. One more attempt**

   4. With ``--retries 3`` the executive makes up to four attempts. What are
      the two possible outcomes of the fourth attempt, and what happens next
      in each case? Run
      ``python3 toy_factory.py --seed 113 --arch "three layers" --retries 3``
      to see which one happens.

   .. raw:: html

      <hr>

   **Part C. The skills package**

   5. In GP1, the pick skill of the course skills package fails. What does
      the skill do, and which part of your system decides what happens next?

   .. dropdown:: Solution
      :color: success

      **Question 1.** The run gives:

      .. code-block:: text

            8.0 s  cell 1: tester 1 reads  3.80 V -> bin
           16.0 s  pick: GRASP_FAILED, attempt 1 of 3
           20.0 s  pick: GRASP_FAILED, attempt 2 of 3
           24.0 s  pick: GRASP_FAILED, attempt 3 of 3
           24.0 s  stopped cleanly: pick: GRASP_FAILED 3 times

      **Question 2.**

      .. list-table::
         :header-rows: 1
         :widths: 22 22 26 30
         :class: compact-table

         * - **Event**
           - **Who sees it**
           - **Who handles it**
           - **What moves up**
         * - Grasp fails 3 times
           - Skill: ``GRASP_FAILED``, three times
           - Executive: three attempts, then gives up
           - ``pick: GRASP_FAILED 3 times`` to the top loop, which stops
             cleanly

      In the code: ``Executive.pick`` returns ``"GRASP_FAILED 3 times"``;
      ``test_cell`` turns it into a report ``{"error": ...}``; and
      ``three_layers`` sees the error and returns ``stopped cleanly``. This
      is the "Nothing, unless all 3 fail" case of the lecture's table.

      **Question 3.** The trace rounds to two decimals. An instrumented run
      gave the average as 3.80099 V, just above 3.8 V, so ``in_range`` is
      false and the planner sends the cell to the bin. Cell 1's true voltage
      is 3.80 V (the first line of ``python3 toy_factory.py --seed 113``):
      the reading noise pushed it over the edge.

      **Question 4.** Before you run: the fourth attempt either fails (the
      executive gives up, and the run stops cleanly with ``GRASP_FAILED 4
      times``) or succeeds (the run goes on and tests cell 2). It succeeds
      with probability 0.8, but only the run tells you which. The run gives:

      .. code-block:: text

            8.0 s  cell 1: tester 1 reads  3.80 V -> bin
           16.0 s  pick: GRASP_FAILED, attempt 1 of 4
           20.0 s  pick: GRASP_FAILED, attempt 2 of 4
           24.0 s  pick: GRASP_FAILED, attempt 3 of 4
           32.0 s  cell 2: tester 2 reads  3.63 V -> AGV 1
           46.0 s  cell 3: tester 1 MALFUNCTIONING -> move to tester 2
           51.0 s  cell 3: tester 2 reads  3.61 V -> AGV 1
           65.1 s  cell 4: tester 2 reads  3.61 V -> AGV 1
           71.2 s  tester 1 OPERATIONAL again
           79.2 s  cell 5: tester 1 reads  3.54 V -> AGV 1
           95.2 s  kit accepted: total 14.35 V

      The fourth attempt succeeded, and the kit was accepted.

      **Question 5.** The skill stops and returns a failure reason in its
      action result. It never retries the task itself. Your behavior tree,
      the executive, reads the result and decides: retry, try something else,
      or stop cleanly.
