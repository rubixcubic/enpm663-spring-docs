====================================================
Quiz
====================================================

.. important::

   **This quiz is not submitted and it is not graded.** It is a self-check,
   and the answers are published so you can use it that way.

   The graded quizzes are the **five in-class quizzes** listed in the
   :doc:`syllabus </syllabus/index>`. No graded quiz covers L12: this lecture
   is assessed through the final demo, whose test plan and comparison table
   use its metrics. Working through this page is good preparation for that.
   Memorizing the answers below is not.

This quiz covers Lecture 12: the three things a measurement needs, the four
levels of metrics, plan-level metrics for PDDL and LLM planners, precision,
recall and position error, execution metrics, the standard error of a success
rate, controlled comparisons, and the ARIAC 2025 scoring formula with its
worked example. Every question can be answered from the slides shown in
class.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True or false questions ask whether the statement holds as stated in
     the lecture.
   - Short answer questions want two to four sentences.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1 to 8)
==================================

.. admonition:: Question 1
   :class: hint

   Which of these is **not** one of the three things the lecture says every
   measurement needs?

   A. A defined metric: what is counted, and from which log or topic

   B. A source of truth to compare against

   C. A known run-to-run variation

   D. A result that matches the team's expectation

.. dropdown:: Answer
   :class-container: sd-border-success

   **D**.

   The three are a defined metric, a source of truth (the true defects, the
   true pose, the orders wanted) and a known run-to-run variation: how far the
   number moves when nothing in the system changes. A result is not checked
   against what the team expected.


.. admonition:: Question 2
   :class: hint

   A team's detector inspects 30 cells. 6 are defective. It flags 8 cells, and
   5 of the 8 are defective. What are its precision and recall?

   A. Precision 5 / 6 = 0.83, recall 5 / 8 = 0.63

   B. Precision 5 / 8 = 0.63, recall 5 / 6 = 0.83

   C. Precision 8 / 30 = 0.27, recall 6 / 30 = 0.20

   D. Precision 5 / 30 = 0.17, recall 5 / 6 = 0.83

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   TP = 5, FP = 8 − 5 = 3, FN = 6 − 5 = 1. Precision = TP / (TP + FP) =
   5 / 8 = 0.63: of the flagged cells, the share that were defective. Recall
   = TP / (TP + FN) = 5 / 6 = 0.83: of the defective cells, the share
   flagged. **A** swaps the two.


.. admonition:: Question 3
   :class: hint

   In ARIAC 2025, what happens to a **good** cell that the detector flags as
   defective?

   A. Nothing; it continues to the voltage tester

   B. It gets a failing inspection report, the inspection door stays closed,
      the cell drops into the inspection bin, and the run loses 50 points

   C. The kit it goes into is refused at shipping

   D. The run is marked aborted

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   That is a false positive. The penalty is ``GOOD_CELL_IN_INSPECTION_BIN``,
   50 points per cell in ``scoring_weights.yaml``. **C** is what a false
   negative can cause when the kit is submitted without the check kit quality
   call: a defective cell that passes and goes into a kit.


.. admonition:: Question 4
   :class: hint

   Plan A sends every cell to voltage tester 1 while tester 2 sits idle. Plan
   B alternates the two testers. Both are valid. Which metric separates them?

   A. Validity

   B. The schema-valid rate

   C. Cost or time

   D. The number of invented objects

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**.

   Both plans are valid, so validity cannot separate them. In Plan A each
   cell waits for the one before it to leave tester 1, so Plan A takes longer
   when the voltage tester, not the robots, is the slowest step.
   That is why the lecture says to report cost or time along with validity.
   **B** and **D** are measures for LLM replies, not for these two plans.


.. admonition:: Question 5
   :class: hint

   A system completes 18 of 25 runs. What is the standard error of its
   success rate?

   A. :math:`\sqrt{0.72 \times 0.28 / 25}` = 0.090

   B. :math:`0.72 \times 0.28 / 25` = 0.008

   C. :math:`\sqrt{0.72 / 25}` = 0.170

   D. :math:`\sqrt{18 \times 7 / 25}` = 2.245

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**.

   :math:`p = 18 / 25 = 0.72`, so :math:`1 - p = 0.28`, and
   :math:`\mathrm{SE} = \sqrt{p(1 - p)/n} = \sqrt{0.2016 / 25} =
   \sqrt{0.008064}` = 0.090. **B** forgets the square root.


.. admonition:: Question 6
   :class: hint

   A team runs its system 20 times and gets a standard error of 0.10. About
   how many runs would bring the standard error to 0.05?

   A. 40

   B. 80

   C. 25

   D. 400

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The standard error shrinks with the square root of :math:`n`: four times
   the runs halves it. 4 × 20 = 80 runs. Doubling the runs (**A**) divides
   it only by :math:`\sqrt{2}`, about 1.41.


.. admonition:: Question 7
   :class: hint

   A trial asks for 4 kits (one of them high-priority) and no modules. The
   run submits 3 kits that ARIAC accepts. What is the base score?

   A. 5000 × 3 / 3 = 5000

   B. 5000 × 3 / 4 = 3750

   C. 5000 × 3 / 4 + 12000 = 15750

   D. 12000 × 3 / 4 = 9000

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   :math:`B = W_1 \cdot k_c / k_d + W_2 \cdot m_c / m_d`. High-priority kits
   count in :math:`k_d`, so :math:`k_d = 4`, and a trial with no modules adds
   0 for modules: 5000 × 3 / 4 = 3750. **A** leaves the high-priority kit out
   of :math:`k_d`.


.. admonition:: Question 8
   :class: hint

   A team's sensors cost $4400. In a run where every order is complete, what
   is the sensor cost bonus?

   A. 1000 × 4400 / 9600 = 458.3

   B. 1000 × (1 − 4400 / 9600) = 541.7

   C. 0, because sensors never earn a bonus

   D. 1000 × (4400 / 9600 − 1) = −541.7

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**.

   The bonus is :math:`W_6 (1 - \sigma / 9600)` with :math:`W_6 = 1000`:
   1 − 4400 / 9600 = 1 − 0.4583 = 0.5417, times 1000 = 541.7. **D** is the
   over-budget penalty formula, which applies only when :math:`\sigma` is
   above $9600.


----


True or False (Questions 9 to 14)
=================================

.. admonition:: Question 9
   :class: hint

   A good ARIAC score proves that every lower-level metric is good.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   A good score next to poor lower-level metrics can mean that the trial did
   not test the weak part. The lecture's example: a trial with few defective
   cells gives a detector few defects to miss. Chance can also give a weak
   system one good run.


.. admonition:: Question 10
   :class: hint

   GP3 completes 17 of 20 runs and GP4 completes 15 of 20. These runs show
   that GP4 is worse than GP3.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The difference is 0.85 − 0.75 = 0.10. The standard error of the
   difference is :math:`\sqrt{0.080^2 + 0.097^2}` = 0.126, so the gap is
   smaller than one standard error of the difference. In the lecture's
   simulation, two systems
   with the **same** true rate of 0.80 differ by 0.10 or more in 54.8% of
   comparisons of 20 runs each.


.. admonition:: Question 11
   :class: hint

   If a run misses one wanted kit, ARIAC still pays the speed bonuses the run
   earned, but not the classification bonus.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Bonuses are paid only if every wanted kit and module was submitted and
   accepted. Otherwise the competition manager marks the run aborted, and
   ``score_bonuses`` sets **all five** bonuses to 0. In the worked example,
   Run 2 ran as fast as Run 1 and still got 0 bonus points.


.. admonition:: Question 12
   :class: hint

   In the ARIAC 2025 code, the trial time bonus is not clamped at zero.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   The scoring page says every bonus is clamped at zero, but the code clamps
   only three with ``max(0, ...)``: inspection speed, high-priority speed and
   sensor cost. The trial time bonus goes below zero only if the run time
   passes the time limit. The classification bonus cannot go below zero.


.. admonition:: Question 13
   :class: hint

   Two robots collide with each other for 3 s. ARIAC records one robot
   collision occurrence, 100 points.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Contact under 5 s is one occurrence per robot, but a collision between two
   robots is counted twice, because each robot records its own: 2 × 100 =
   200 points.


.. admonition:: Question 14
   :class: hint

   ARIAC averages the two best of five runs per trial, so your own testing
   should also report the best runs.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   ARIAC's rule measures how well a system does on its good runs. The final
   demo is a single run on an unseen trial, and a good run is not
   guaranteed. So for your own testing, report the mean and the spread over
   all runs.


----


Short Answer (Questions 15 to 18)
=================================

.. admonition:: Question 15
   :class: hint

   Name the four extra measures the lecture adds for an LLM planner, and say
   why they are reported per decision rather than as one total for the run.

.. dropdown:: Answer
   :class-container: sd-border-success

   The **schema-valid rate** (first try and after one re-prompt), the number
   of **invented objects** (a cell, slot, AGV or order ID that does not
   exist), **tokens and dollars per decision** (or GPU time for a local
   model), and **latency per decision**. A list per decision, from the
   decision logs kept since L9, gives a mean and a spread.


.. admonition:: Question 16
   :class: hint

   Eight top shell spawns give position errors with a mean of 5.5 mm, a
   sample standard deviation of 1.9 mm and a largest error of 8.9 mm. Why
   does the lecture ask you to report the largest error as well as the mean?

.. dropdown:: Answer
   :class-container: sd-border-success

   Each spawn is one grasp. One bad spawn can make that grasp miss even when
   the mean is small. The mean of 5.5 mm hides the 8.9 mm spawn; the largest
   error shows it.


.. admonition:: Question 17
   :class: hint

   You are designing the GP4 comparison with GP3. Name what you hold fixed,
   what changes, and how you order the runs. Why does the order matter?

.. dropdown:: Answer
   :class-container: sd-border-success

   Hold fixed the trial file (seed, defect rate, time limit, challenges and
   their start times), the team configuration (sensors and poses, conveyor
   speed, cell feed rate), the software (skills release, executor, model name,
   version and settings) and the computer. Only the planner changes. Alternate
   the runs (GP3, GP4, GP3, GP4), so that if the machine slows down over the
   session, both systems share the slowdown. Write the plan, with the number
   of runs, before running.


.. admonition:: Question 18
   :class: hint

   In the worked example, Run 1 scores 6384.6 and Run 2, which missed the
   high-priority kit, scores 3183.3. Where does the difference come from, and
   what does it say about speed against finishing every order?

.. dropdown:: Answer
   :class-container: sd-border-success

   The difference is 3201.25 points: 1666.67 from the base (one kit of three,
   5000 / 3) and all 1534.58 of the bonuses, which ARIAC sets to 0 because
   not every wanted kit was submitted. So finishing every order matters more
   than speed: Run 1's three speed bonuses total 300 + 125 + 120 = 545
   points.
