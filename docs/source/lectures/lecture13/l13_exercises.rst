====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work. After L13, that is the final demo, which includes the
   embodied-reasoning comparison table these exercises practice.

Six take-home exercises on the L13 slides and the demonstration code.
Exercises 1 to 4 score the ER answers in new ways: on a different set of
cells, with one more cell, with a different mistake, and with a weaker
schema. Each one asks you to predict the table on paper first and then check
it by changing ``er_demo.py`` or ``score_er.py``. Exercise 5 is on paper: the
audit traces of the two designs for one failure. Exercise 6 is arithmetic:
what the camera for the ER step costs in sensor points.

.. note::

   The scripts and how to run them are on the :doc:`code page <l13_code>`.
   Work on a copy, so the original still gives the output in the notes. Every
   output below was measured with Python 3.12.3, ``google-genai`` 2.29.0,
   ``httpx`` 0.28.1 and ``jsonschema`` 4.10.3 on 2026-10-12. The scripts' own
   outputs are the same under ``google-genai`` 2.31.0 and ``jsonschema``
   4.26.0, the versions on the code page (checked 2026-10-18). All labels are
   the example's: ``TRUTH`` and ``LIDAR`` are chosen for the example, and the
   ER labels come from the scripted stand-in.

For reference, the labels of the 12 cells (from ``score_er.py`` and the schema
check in ``outputs/er_demo.txt``; "none" means no defect):

.. list-table::
   :header-rows: 1
   :widths: 16 28 28 28
   :class: compact-table

   * - **Cell**
     - **Truth**
     - **Lidar (GP2)**
     - **ER (stand-in)**
   * - c01
     - none
     - none
     - none
   * - c02
     - DENT
     - DENT
     - DENT
   * - c03
     - none
     - none
     - none
   * - c04
     - SCRATCH
     - SCRATCH
     - none
   * - c05
     - none
     - none
     - DENT
   * - c06
     - BULGE
     - BULGE
     - BULGE
   * - c07
     - DENT
     - DENT
     - BULGE
   * - c08
     - none
     - none
     - none
   * - c09
     - SCRATCH
     - none
     - SCRATCH
   * - c10
     - none
     - none
     - rejected (CRACK)
   * - c11
     - BULGE
     - BULGE
     - BULGE
   * - c12
     - none
     - none
     - none


.. dropdown:: Exercise 1. Rescore the Table on Six Cells
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   See how the choice of cells changes precision and recall, and meet a
   precision that cannot be computed.

   .. raw:: html

      <hr>

   **Part A. On paper**

   Score only cells c01 to c06 (c10 is outside this set).

   1. For each defect type and each detector, count TP, FP and FN.
   2. Compute precision and recall. If a detector never calls a type, what
      happens to its precision?
   3. On the full 11 cells, ER's SCRATCH recall was 0.50. What is it on these
      six cells, and why?
   4. On how many of the six cells do ER and lidar give the same label?

   .. raw:: html

      <hr>

   **Part B. Check it**

   5. In ``main`` of ``score_er.py``, change the line that picks the cells to

      .. code-block:: python

         cells = [c for c in TRUTH if c in er and c <= "c06"]

      and run the script. Compare with your table. The second line still says
      ``rejected by the schema: c10``: explain why.

   .. dropdown:: Solution
      :color: success

      **Questions 1 and 2.** Cells c01 to c06 hold one dent (c02), one scratch
      (c04) and one bulge (c06), so each type has 1 defective cell.

      - **Lidar** labels all six cells right: for each type, TP 1, FP 0, FN 0,
        precision 1 / 1 = 1.00, recall 1 / 1 = 1.00.
      - **ER, DENT:** c02 is a TP, c05 (no defect, called a dent) is an FP.
        TP 1, FP 1, FN 0: precision 1 / 2 = 0.50, recall 1 / 1 = 1.00.
      - **ER, SCRATCH:** c04 has a scratch and ER said none, so FN 1. ER
        never says SCRATCH on these cells: TP 0, FP 0. Recall 0 / 1 = 0.00.
        Precision is 0 / (0 + 0): the denominator is zero, so precision has
        no value. The script prints ``no calls``.
      - **ER, BULGE:** c06 is a TP. TP 1, FP 0, FN 0: precision 1.00, recall
        1.00.

      **Question 3.** SCRATCH recall drops from 0.50 to 0.00. On 11 cells ER
      found c09 and missed c04 (1 of 2). c09 is not in the set, so only the
      miss is left (0 of 1). With one defective cell, recall can only be 0 or
      1.

      **Question 4.** ER and lidar agree on c01, c02, c03 and c06, and
      disagree on c04 (lidar SCRATCH, ER none) and c05 (lidar none, ER DENT):
      4 of 6.

      **Question 5.** Measured output:

      .. code-block:: text

         Cells used: 6 of 12
           rejected by the schema: c10
         DENT
           lidar  TP 1  FP 0  FN 0   precision 1/1 = 1.00    recall 1/1 = 1.00
           ER     TP 1  FP 1  FN 0   precision 1/2 = 0.50    recall 1/1 = 1.00
         SCRATCH
           lidar  TP 1  FP 0  FN 0   precision 1/1 = 1.00    recall 1/1 = 1.00
           ER     TP 0  FP 0  FN 1   precision no calls      recall 0/1 = 0.00
         BULGE
           lidar  TP 1  FP 0  FN 0   precision 1/1 = 1.00    recall 1/1 = 1.00
           ER     TP 1  FP 0  FN 0   precision 1/1 = 1.00    recall 1/1 = 1.00
         ER and lidar give the same label: 4 of 6
         Latency and cost per call: not measured (stand-in)

      ``rejected`` comes from ``er_labels``, which runs over all 12 answers
      before the cells are chosen. A report should say which cells were left
      out and why, so the reader can tell a schema rejection from a cell you
      chose not to score.


.. dropdown:: Exercise 2. What One More Correct Cell Does to Recall
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Measure how far one cell moves recall when each type has only two
   defective cells, and how that shrinks with more cells.

   .. raw:: html

      <hr>

   **Part A. On paper**

   A 13th cell, c13, arrives. It has a scratch, and the lidar detector finds
   it.

   1. Suppose ER also finds it. What are the SCRATCH recall values of lidar
      and ER now? By how much did each one move?
   2. Suppose instead ER answers "no defect" for c13. What is ER's SCRATCH
      recall now?
   3. In case 1, what happens to SCRATCH precision for both detectors, and to
      the "same label" count?
   4. If a type had 20 defective cells, by how much would one cell move its
      recall? How many defective cells would you need before one cell moves
      recall by 0.02 or less?

   .. raw:: html

      <hr>

   **Part B. Check it**

   5. Add c13 to the example: in ``er_demo.py`` change ``range(1, 13)`` to
      ``range(1, 14)`` and add ``one("SCRATCH", 310, 502)`` at the end of
      ``SCRIPT`` (the point is chosen for this exercise); in ``score_er.py``
      add ``"c13": "SCRATCH"`` to both ``TRUTH`` and ``LIDAR``. Run
      ``score_er.py``. Then change the last ``SCRIPT`` entry to ``NONE`` and
      run it again.

   .. dropdown:: Solution
      :color: success

      **Question 1.** SCRATCH now has 3 defective cells (c04, c09, c13).
      Lidar found c04 and c13: recall 2 / 3 = 0.67. ER found c09 and c13:
      recall 2 / 3 = 0.67. Each moved up by 0.67 - 0.50 = 0.17. They still
      have the same recall, from different cells (lidar misses c09, ER misses
      c04).

      **Question 2.** ER finds only c09: recall 1 / 3 = 0.33. It moved down by
      0.50 - 0.33 = 0.17. Whether ER finds c13 or not changes its recall by
      0.67 - 0.33 = 0.33, one cell out of three.

      **Question 3.** Both detectors add one TP and no FP, so precision stays
      2 / 2 = 1.00 for lidar and becomes 2 / 2 = 1.00 for ER (it was 1 / 1).
      Both say SCRATCH on c13, so the same-label count goes from 7 of 11 to 8
      of 12.

      **Question 4.** With 20 defective cells, one cell moves recall by
      1 / 20 = 0.05. To move it by 0.02 or less you need
      1 / n ≤ 0.02, so n ≥ 1 / 0.02 = 50 defective cells of that type. With
      2 per type, as in the lecture, one cell moves recall by 0.50.

      **Question 5.** Measured, with ER finding c13:

      .. code-block:: text

         Cells used: 12 of 13
           rejected by the schema: c10
         DENT
           lidar  TP 2  FP 0  FN 0   precision 2/2 = 1.00    recall 2/2 = 1.00
           ER     TP 1  FP 1  FN 1   precision 1/2 = 0.50    recall 1/2 = 0.50
         SCRATCH
           lidar  TP 2  FP 0  FN 1   precision 2/2 = 1.00    recall 2/3 = 0.67
           ER     TP 2  FP 0  FN 1   precision 2/2 = 1.00    recall 2/3 = 0.67
         BULGE
           lidar  TP 2  FP 0  FN 0   precision 2/2 = 1.00    recall 2/2 = 1.00
           ER     TP 2  FP 1  FN 0   precision 2/3 = 0.67    recall 2/2 = 1.00
         ER and lidar give the same label: 8 of 12
         Latency and cost per call: not measured (stand-in)

      With ER answering ``NONE`` for c13, only the ER SCRATCH row and the last
      count change:

      .. code-block:: text

         SCRATCH
           ER     TP 1  FP 0  FN 2   precision 1/1 = 1.00    recall 1/3 = 0.33
         ER and lidar give the same label: 7 of 12


.. dropdown:: Exercise 3. A Wrong Type Against a Missed Defect
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   See why one wrong type counts twice, and compare it with a plain miss and
   with a right answer.

   .. raw:: html

      <hr>

   **Part A. On paper**

   Cell c07 has a dent. The stand-in called it a bulge.

   1. Which counts does the c07 answer add to the DENT rows and to the BULGE
      rows of ER?
   2. Suppose ER had answered "no defect" for c07. Recompute ER's DENT and
      BULGE precision and recall.
   3. Suppose ER had answered "DENT" for c07. Recompute them again.
   4. Rank the three answers (BULGE, "no defect", DENT) by how many errors
      they add to ER's rows, counting every FP and FN over the three types.

   .. raw:: html

      <hr>

   **Part B. Check it**

   5. In ``SCRIPT`` (``er_demo.py``), the seventh entry is c07's answer,
      ``one("BULGE", 431, 515)``. Replace it with ``NONE`` and run
      ``score_er.py``. Then replace it with ``one("DENT", 431, 515)`` and run
      again.

   .. dropdown:: Solution
      :color: success

      **Question 1.** c07's truth is DENT and ER said BULGE. For DENT, ER did
      not say DENT on a dented cell: one **FN**. For BULGE, ER said BULGE on a
      cell without a bulge: one **FP**. One wrong answer, two errors.

      **Question 2.** "No defect" on c07:

      - DENT: c02 TP, c05 FP, c07 FN (still missed). TP 1, FP 1, FN 1:
        precision 1 / 2 = 0.50, recall 1 / 2 = 0.50. No change.
      - BULGE: c06 and c11 TP, and no FP now. Precision 2 / 2 = 1.00 (was
        0.67), recall 2 / 2 = 1.00.

      **Question 3.** "DENT" on c07:

      - DENT: c02 and c07 TP, c05 FP. TP 2, FP 1, FN 0: precision 2 / 3 =
        0.67, recall 2 / 2 = 1.00.
      - BULGE: TP 2, FP 0: precision 1.00, recall 1.00.

      **Question 4.** BULGE adds two errors (a DENT FN and a BULGE FP).
      "No defect" adds one (the DENT FN). DENT adds none. In the table, a
      wrong type costs more than a miss: it lowers recall for the true type
      and precision for the type it named.

      **Question 5.** Measured with ``NONE`` for c07:

      .. code-block:: text

         DENT
           ER     TP 1  FP 1  FN 1   precision 1/2 = 0.50    recall 1/2 = 0.50
         BULGE
           ER     TP 2  FP 0  FN 0   precision 2/2 = 1.00    recall 2/2 = 1.00
         ER and lidar give the same label: 7 of 11

      Measured with ``DENT`` for c07:

      .. code-block:: text

         DENT
           ER     TP 2  FP 1  FN 0   precision 2/3 = 0.67    recall 2/2 = 1.00
         BULGE
           ER     TP 2  FP 0  FN 0   precision 2/2 = 1.00    recall 2/2 = 1.00
         ER and lidar give the same label: 8 of 11

      The lidar rows and the SCRATCH rows do not change in either run.


.. dropdown:: Exercise 4. What the Schema Check Protects
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   See what happens to the scores when the schema lets an answer through
   that it should reject.

   .. raw:: html

      <hr>

   **Part A. On paper**

   c10 has no defect. The stand-in answered ``CRACK``, and the schema
   rejected it.

   1. Suppose someone adds ``"CRACK"`` to the schema's list of types, so c10
      is accepted with the label CRACK. How many cells are used? Which counts
      in the three per-type tables change?
   2. Is the CRACK answer right or wrong? Where in the table does that
      mistake show?
   3. Now suppose instead the stand-in had answered ``BULGE`` for c10 (a
      valid type). Recompute ER's BULGE precision.
   4. ARIAC's ``CellDefect.msg`` has three types. Why should the schema list
      exactly those three?

   .. raw:: html

      <hr>

   **Part B. Check it**

   5. In ``ANSWER_SCHEMA`` (``er_demo.py``), change the enum to
      ``["DENT", "SCRATCH", "BULGE", "CRACK"]`` and run ``er_demo.py`` and
      ``score_er.py``. Then restore the enum, change c10's answer in
      ``SCRIPT`` from ``one("CRACK", 520, 505)`` to ``one("BULGE", 520, 505)``,
      and run ``score_er.py``.

   .. dropdown:: Solution
      :color: success

      **Question 1.** All 12 cells are used. No per-type count changes. For
      each of DENT, SCRATCH and BULGE, c10's truth is not that type and the
      ER label (CRACK) is not that type, so c10 adds no TP, no FP and no FN.

      **Question 2.** It is wrong: c10 has no defect, and ER called it
      defective. The per-type tables cannot show the mistake, because CRACK is
      none of their types. Only the same-label count sees it: ER (CRACK) and
      lidar (none) disagree, so the count is 7 of 12. The error is in the
      answers but missing from every precision and recall.

      **Question 3.** With BULGE, c10 is a second BULGE FP (after c07). ER's
      BULGE row: TP 2, FP 2, FN 0, precision 2 / 4 = 0.50, recall 2 / 2 =
      1.00. Now the mistake shows.

      **Question 4.** Every label in the comparison must use the same types.
      The GP2 inspection report uses the types of ``CellDefect.msg`` (DENT,
      BULGE, SCRATCH), and so does the ground truth that ARIAC prints. An ER
      label outside those three cannot be compared with either, and it drops
      out of every per-type score (Question 2). The schema rejects such an
      answer at once, and the comparison table counts the rejected cell, so
      the mistake stays visible.

      **Question 5.** Measured, with CRACK allowed: ``er_demo.py`` prints
      ``c10 valid     defects: CRACK``, and ``score_er.py`` prints:

      .. code-block:: text

         Cells used: 12 of 12
           rejected by the schema:
         DENT
           lidar  TP 2  FP 0  FN 0   precision 2/2 = 1.00    recall 2/2 = 1.00
           ER     TP 1  FP 1  FN 1   precision 1/2 = 0.50    recall 1/2 = 0.50
         SCRATCH
           lidar  TP 1  FP 0  FN 1   precision 1/1 = 1.00    recall 1/2 = 0.50
           ER     TP 1  FP 0  FN 1   precision 1/1 = 1.00    recall 1/2 = 0.50
         BULGE
           lidar  TP 2  FP 0  FN 0   precision 2/2 = 1.00    recall 2/2 = 1.00
           ER     TP 2  FP 1  FN 0   precision 2/3 = 0.67    recall 2/2 = 1.00
         ER and lidar give the same label: 7 of 12
         Latency and cost per call: not measured (stand-in)

      Every per-type row matches the lecture's table. Measured, with BULGE
      for c10 and the original schema:

      .. code-block:: text

         Cells used: 12 of 12
         BULGE
           ER     TP 2  FP 2  FN 0   precision 2/4 = 0.50    recall 2/2 = 1.00
         ER and lidar give the same label: 7 of 12


.. dropdown:: Exercise 5. Two Audit Traces for One Failure
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Compare what a person can read after the same failure in your stack and
   in a VLA, using the audit trace figure of the lecture.

   .. raw:: html

      <hr>

   **The failure** (chosen for this exercise)

   The step is the lecture's: place a cell in voltage tester 1. On the way to
   the tester, the cell slips out of the gripper and falls.

   **Part A. Your stack**

   1. For each of the four records in row 1 of the figure (the agent's tool
      call, the schema check, the behavior tree's node status, the skill
      result), say what it shows for this failure.
   2. Which record tells you **where** the step failed? Which part of your
      system acts next, and how does it know it must?

   **Part B. A VLA**

   3. For each box in row 2 of the figure, say what a person can read after
      this failure.
   4. How do you find out that the step failed? What would you have to add
      to the system to find out during the run, not after it?

   **Part C. Compare**

   5. A plant engineer asks: "Was the plan wrong, or did the motion fail?"
      Which trace can answer, and from which record?

   .. dropdown:: Solution
      :color: success

      **Question 1.**

      - **Tool call:** the agent asked for the right step, with its name and
        arguments (the cell and tester 1). It looks normal.
      - **Schema check:** valid. The call passed.
      - **Behavior tree:** the node that runs the place step reports failure;
        the nodes before it report success.
      - **Skill result:** failure, with a reason. The exact text depends on
        your skills package.

      **Question 2.** The skill result says where: in the reactive layer,
      during the place motion. The first two records show that the
      deliberative layer and the interface were fine. The behavior tree acts
      next: it checks each skill result before the next step and stops
      cleanly on failure (L4, L7, L11), and passes the status up to the agent
      (tag 6 of the three-designs figure). L11's recovery structures decide
      what happens then.

      **Question 3.**

      - **Camera images and instruction:** readable. They show what the model
        saw and was told.
      - **The VLA model:** learned features, not readable. Nothing says what
        the model meant to do.
      - **Robot actions:** readable as numbers (the motion it sent), but no
        step in them says "failed".
      - **Outcome:** the cell was dropped. If ARIAC charges a penalty for
        where it lands (the lecture lists a cell in the conveyor bin, 25, and
        an object on an invalid surface, 25), the score shows the penalty,
        not the reason.

      **Question 4.** From the outcome only: the cell is not in the tester,
      or a penalty appears in the score. No step returns failure. To find it
      during the run, you would add your own check of the outcome after each
      step, from a sensor or an ARIAC topic: the lecture's discussion point
      "a way to detect a failed pick, since the policy will not report one".

      **Question 5.** Only your stack's trace can answer. The tool call and a
      valid schema check show the plan asked for the right step; the skill
      result shows the motion failed. The VLA trace has no plan to inspect:
      the instruction is the only "plan", and the model's inside cannot be
      read, so you see what the robot did, not why.


.. dropdown:: Exercise 6. What the ER Camera Costs in Points
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Put a price, in run score points, on the camera the ER step needs.

   .. raw:: html

      <hr>

   **The setup** (chosen for this exercise)

   Your team's sensors cost $9200 before you add a camera. An RGB camera
   costs $800 at 1080p and $500 at 720p (ARIAC sensors page). The lecture
   gives the over-budget penalty, 1000 × (cost / 9600 - 1). The sensor cost bonus, from the ARIAC
   scoring page and ``scoring.py`` (L12), is 1000 × (1 - cost / 9600), and
   never below zero. The bonus counts only if every kit and module was
   submitted.

   1. Compute the sensor cost bonus at $9200.
   2. Add a 1080p camera. What is the new cost? Compute the bonus and the
      penalty, and the change in the run score.
   3. Repeat with a 720p camera.
   4. Suppose the run misses one kit. Which of the numbers above still
      matter?
   5. Name one reason to pay for the 1080p camera anyway.

   .. dropdown:: Solution
      :color: success

      **Question 1.** 1000 × (1 - 9200 / 9600):

      1. 1 - 9200 / 9600 = (9600 - 9200) / 9600 = 400 / 9600,
      2. 400 / 9600 = 0.041667,
      3. 1000 × 0.041667 = 41.67 points of bonus.

      **Question 2.** 9200 + 800 = $10000, which is $400 over the budget.

      - Bonus: 1 - 10000 / 9600 is below zero, so the bonus is 0.
      - Penalty: 10000 / 9600 - 1 = 400 / 9600 = 0.041667;
        1000 × 0.041667 = 41.67 points.
      - Change: the run loses the 41.67 bonus and pays the 41.67 penalty:
        41.67 + 41.67 = 83.33 points less.

      **Question 3.** 9200 + 500 = $9700, $100 over the budget.

      - Bonus: 0.
      - Penalty: 9700 / 9600 - 1 = 100 / 9600 = 0.010417;
        1000 × 0.010417 = 10.42 points.
      - Change: 41.67 + 10.42 = 52.08 points less.

      **Question 4.** Bonuses count only if every kit and module was
      submitted, so with a missed kit the bonus is 0 with or without the
      camera. Only the penalty changes the score: 41.67 points with the 1080p
      camera, 10.42 with the 720p one.

      **Question 5.** Whether defects under 2.5 mm deep show in a camera
      image is part of what your team measures. If they show only at 1080p, the 720p camera
      saves 31.25 points (83.33 - 52.08) but gives the ER step images it
      cannot use. Measure both before you choose.
