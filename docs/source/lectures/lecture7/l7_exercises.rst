====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes and the four group projects
   listed in the :doc:`syllabus </syllabus/index>`.

Six take-home exercises on the L7 slides and scripts. Exercises 1 and 6 start
on paper; Exercises 2 to 5 change a script or write a new tree. In every
exercise, predict the result first, write the prediction down, then run the
script.

.. note::

   The scripts are on the :doc:`code page <l7_code>`. Work on a copy of the
   ``code/`` folder, so the original still gives the outputs in the notes.
   Every run below was measured on 2026-10-12 with Python 3.12.3,
   ``py_trees`` 2.6.0 and BehaviorTree.CPP 4.10.0, after
   ``source /opt/ros/jazzy/setup.bash``. Tick counts are exact; times in
   seconds (Exercise 3) can differ by a hundredth on your machine.


.. dropdown:: Exercise 1. Count the Ticks
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Predict a tick trace from the rules of a Sequence with memory and of
   Retry, then check it.

   .. raw:: html

      <hr>

   **Part A. Slower skills**

   In Demo 1 each mock skill returns its result on its second tick and the
   AGV move on its third, and the five-step plan ends after 7 ticks. In your
   copy of ``executor.py``, make every mock skill take 3 ticks and the move
   take 5:

   - in ``class Act``, change ``ticks=2`` to ``ticks=3`` in ``__init__``;
   - in ``build_move_agv``, change ``ticks=3`` to ``ticks=5``.

   1. Before you run anything: on which tick does each of the five steps end?
      How many ticks does the plan take, and how many goals are sent?
   2. Write a formula for the number of ticks of a plan of :math:`k` skill
      steps that each take :math:`n` ticks, followed by one move that takes
      :math:`m` ticks. Check it against the 7 ticks of Demo 1.
   3. Run ``python3 demo_factory.py trace``.

   .. raw:: html

      <hr>

   **Part B. The same change with Retry**

   4. With the same edit, predict the trace of ``python3 demo_retry.py 2``
      (the pick fails twice, then succeeds; ``num_failures=3``). On which
      tick does each pick attempt start and end? How many ticks in all?
   5. Run it.
   6. A finished step hands over to the next step in the same tick, but a
      failed attempt does not start again in the same tick. Which slide
      rule explains each of the two?

   .. dropdown:: Solution
      :color: success

      **Question 1.** An act leaf with ``ticks`` equal to :math:`n` returns
      its result on its :math:`n`-th tick. The guard and the act's first
      tick happen on the tick the step starts, and a finished step hands
      over to the next one in the same tick.

      1. Step 1 starts on tick 1 and ends on tick 1 + 3 − 1 = 3.
      2. Step 2 starts on tick 3 and ends on tick 5; step 3 ends on tick 7;
         step 4 ends on tick 9.
      3. Step 5, the move, starts on tick 9 and ends on tick 9 + 5 − 1 = 13.

      The plan takes **13 ticks**, and sends **5 goals** (one per step, as
      before).

      **Question 2.** Ticks = 1 + :math:`k(n - 1) + (m - 1)`. Demo 1 has
      :math:`k = 4`, :math:`n = 2`, :math:`m = 3`:
      1 + 4 × 1 + 2 = 7, the 7 ticks on the slide. Part A gives
      1 + 4 × 2 + 4 = 13.

      **Question 3.** Measured:

      .. code-block:: text

         tick  1: 1 pick-from-tester RUNNING
         tick  3: 1 pick-from-tester SUCCESS
         tick  3: 2 place-in-slot RUNNING
         tick  5: 2 place-in-slot SUCCESS
         tick  5: 3 pick-from-tester RUNNING
         tick  7: 3 pick-from-tester SUCCESS
         tick  7: 4 place-in-slot RUNNING
         tick  9: 4 place-in-slot SUCCESS
         tick  9: 5 move-agv RUNNING
         tick 13: 5 move-agv SUCCESS
         plan SUCCESS after 13 ticks; 5 goals sent

      **Question 4.** When the child fails, Retry returns RUNNING and starts
      the child again on the **next** tick.

      1. Attempt 1: ticks 1 to 3, fails on tick 3.
      2. Attempt 2: ticks 4 to 6, fails on tick 6.
      3. Attempt 3: ticks 7 to 9, succeeds on tick 9.
      4. The place step starts on tick 9 and ends on tick 9 + 3 − 1 = 11.

      **11 ticks**, and 4 goals (3 picks and 1 place). The same steps give
      the 7 ticks of Demo 2: attempts on ticks 1 to 2, 3 to 4 and 5 to 6, and
      the place on ticks 6 to 7.

      **Question 5.** Measured:

      .. code-block:: text

         tick  1: 1 pick-from-tester RUNNING
         tick  1: retry 1 RUNNING
         tick  3: 1 pick-from-tester FAILURE
         tick  3:   act: GRASP_FAILED
         tick  4: 1 pick-from-tester RUNNING
         tick  6: 1 pick-from-tester FAILURE
         tick  6:   act: GRASP_FAILED
         tick  7: 1 pick-from-tester RUNNING
         tick  9: 1 pick-from-tester SUCCESS
         tick  9: retry 1 SUCCESS
         tick  9: 2 place-in-slot RUNNING
         tick 11: 2 place-in-slot SUCCESS
         plan SUCCESS after 11 ticks; 4 goals sent

      **Question 6.** The Demo 1 trace slide: "A step that finishes hands
      over to the next step in the same tick." The Retry slide: "When the
      child fails, Retry returns RUNNING and starts the child again on the
      next tick." So each failed attempt costs one tick more than a finished
      step.


.. dropdown:: Exercise 2. Add an Action to the Registry
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Write a builder for an action the registry does not have yet,
   ``submit-kit``, and see what the guard does when the plan leaves out a
   step.

   The L6 domain defines it as:

   .. code-block:: text

      (:action submit-kit
        :parameters (?a - agv)
        :precondition (and (kit-checked ?a) (agv-at ?a shipping))
        :effect (submitted ?a))

   .. raw:: html

      <hr>

   **Part A. Before the builder**

   In your copy of ``demo_factory.py``, add a sixth step to ``PLAN``, after
   the move: ``"(submit-kit agv1)"``.

   1. Predict what ``python3 demo_factory.py build`` prints. How many goals
      are sent?

   .. raw:: html

      <hr>

   **Part B. Write the builder**

   2. In your copy of ``executor.py``, give ``MockFactory`` a list
      ``self.submitted = []`` and a skill ``submit_kit(self, agv)`` that
      succeeds only when the AGV is at shipping (``station_id`` 3) and then
      adds the AGV's number to ``submitted``. Use ``self.result`` as the
      other skills do.
   3. Write ``build_submit_kit(f, label, a)`` with the four leaves: the guard
      checks the precondition, the act calls ``submit_kit``, the verify checks
      ``submitted``, the update adds the effect. Add it to ``REGISTRY``.
   4. Predict the output of ``python3 demo_factory.py trace``. Then run it.

   .. raw:: html

      <hr>

   **Part C. Make the guard pass**

   5. Why did step 6 fail in Part B? Is that a bug in the executor or in the
      plan?
   6. As a stand-in for a ``check-kit`` step, add ``("kit-checked", "agv1")``
      to ``START``. Predict the trace: the tick on which step 6 ends, the
      total ticks and the goals sent. Run it.

   .. dropdown:: Solution
      :color: success

      **Question 1.** The plan prints with six steps, then ``build_tree``
      raises ``KeyError`` on step 6. The ``build`` mode does not catch it
      (only ``unknown`` does), so Python prints a traceback that ends with:

      .. code-block:: text

         KeyError: 'step 6: no builder for submit-kit'

      **0 goals**: the factory stops before it returns a tree.

      **Questions 2 and 3.** One answer:

      .. code-block:: python

         # in MockFactory.__init__
         self.submitted = []  # AGVs whose kit was submitted

         # a new MockFactory method
         def submit_kit(self, agv):  # stand-in for /submit_kitting_order
             ok = self.station[agv] == 3  # the AGV is at shipping
             code = self.result("submit_kit", ok)
             if code == "SUCCESS":
                 self.submitted.append(agv)
             return code

         # a new builder, above REGISTRY
         def build_submit_kit(f, label, a):
             goal = (number(a),)  # agv1 -> 1
             return subtree(
                 label, [("kit-checked", a), ("agv-at", a, "shipping")],
                 Act("act", f, "submit_kit", goal),
                 Verify("verify", lambda: goal[0] in f.submitted,
                        f"{a} submitted"),
                 add=[("submitted", a)], delete=[])

         # in REGISTRY
         "submit-kit": build_submit_kit,

      The comment in the L6 domain names ARIAC's ``/submit_kitting_order``
      service for this action; in GP3 your act leaf calls it.

      **Question 4.** Steps 1 to 5 run as in Demo 1, so the move ends on
      tick 7. Step 6 starts on tick 7, and its guard fails at once:
      ``(kit-checked agv1)`` is not on the blackboard. Measured:

      .. code-block:: text

         tick  1: 1 pick-from-tester RUNNING
         tick  2: 1 pick-from-tester SUCCESS
         tick  2: 2 place-in-slot RUNNING
         tick  3: 2 place-in-slot SUCCESS
         tick  3: 3 pick-from-tester RUNNING
         tick  4: 3 pick-from-tester SUCCESS
         tick  4: 4 place-in-slot RUNNING
         tick  5: 4 place-in-slot SUCCESS
         tick  5: 5 move-agv RUNNING
         tick  7: 5 move-agv SUCCESS
         tick  7: 6 submit-kit FAILURE
         tick  7:   guard: (kit-checked agv1) is false
         plan FAILURE after 7 ticks; 5 goals sent

      Still 5 goals: the guard stopped step 6 before its act sent one.

      **Question 5.** The plan is wrong, and the executor is right to refuse
      it. A plan from the L6 domain has a ``check-kit`` step before the move,
      because ``submit-kit`` needs ``(kit-checked agv1)``. This hand-written
      plan leaves it out, and the guard catches that before a submission
      that ARIAC would reject.

      **Question 6.** Step 6 now starts on tick 7 and, like every skill,
      returns its result on its second tick: tick 8. **8 ticks, 6 goals.**
      Measured:

      .. code-block:: text

         tick  1: 1 pick-from-tester RUNNING
         tick  2: 1 pick-from-tester SUCCESS
         tick  2: 2 place-in-slot RUNNING
         tick  3: 2 place-in-slot SUCCESS
         tick  3: 3 pick-from-tester RUNNING
         tick  4: 3 pick-from-tester SUCCESS
         tick  4: 4 place-in-slot RUNNING
         tick  5: 4 place-in-slot SUCCESS
         tick  5: 5 move-agv RUNNING
         tick  7: 5 move-agv SUCCESS
         tick  7: 6 submit-kit RUNNING
         tick  8: 6 submit-kit SUCCESS
         plan SUCCESS after 8 ticks; 6 goals sent


.. dropdown:: Exercise 3. Swap the Nesting and Predict the Timing
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Predict how long a step takes under ``Retry(Timeout(act))`` and under
   ``Timeout(Retry(act))``, first with round numbers, then with the ticks
   of Demo 4.

   .. raw:: html

      <hr>

   **Part A. On paper (round numbers)**

   The limit is 10 s and Retry allows three attempts, as in the slide
   "Choosing the Order and Setting the Limit". Ignore the tick period.

   1. Each attempt of the act fails after 4 s. For each nesting order, when
      does the step end, with what status, and how many attempts start?
   2. The act fails after 4 s twice, then the third attempt succeeds after
      4 s. Same questions.
   3. From Question 2: what must a ``Timeout(Retry(act))`` limit cover, if
      every allowed attempt should get to finish?

   .. raw:: html

      <hr>

   **Part B. In the demo (with ticks)**

   In your copy of ``demo_nesting.py``, change the line that sets
   ``fail_after`` so that the first argument is the time after which each
   attempt fails:

   .. code-block:: python

      fail_after = None if sys.argv[1] == "hang" else float(sys.argv[1])

   The limit stays 0.2 s, ``num_failures`` 3 and the tick period 0.02 s.

   4. The act checks the time only when it is ticked, every 0.02 s. An
      attempt that fails after 0.05 s: on which tick time does the act see
      the failure?
   5. Predict, for ``0.05`` and for ``0.12``, the start times of the
      attempts and the end time of the step under each nesting order. Use the
      Demo 4 rule: each new attempt starts about one tick (0.02 s) after the
      last one ends.
   6. Run ``python3 demo_nesting.py 0.05 --starts`` and
      ``python3 demo_nesting.py 0.12 --starts``.

   .. dropdown:: Solution
      :color: success

      **Question 1.**

      - ``Retry(Timeout(act))``: each attempt has its own 10 s, and 4 s is
        less than 10 s, so Timeout never fires. Three attempts fail at 4, 8
        and 12 s. **FAILURE at 3 × 4 = 12 s, 3 attempts.**
      - ``Timeout(Retry(act))``: attempts start at 0, 4 and 8 s. The third
        would fail at 12 s, but the shared limit ends at 10 s. **FAILURE at
        10 s, 3 attempts started**, the third cut off after 10 − 8 = 2 s.

      **Question 2.**

      - ``Retry(Timeout(act))``: the third attempt succeeds at
        4 + 4 + 4 = 12 s. **SUCCESS at 12 s.**
      - ``Timeout(Retry(act))``: the third attempt would succeed at 12 s,
        after the 10 s limit. **FAILURE at 10 s.** The shared limit kills an
        attempt that was going to succeed.

      **Question 3.** The longest normal attempt times the number of
      attempts: here 3 × 4 = 12 s or more. Otherwise the last attempts never
      get their full time.

      **Question 4.** Ticks fall at about 0.02, 0.04, 0.06 s after the
      attempt starts. At 0.04 s the attempt is still RUNNING, so the act sees
      the failure on the tick at about **0.06 s**. An attempt that fails
      after 0.12 s, a multiple of 0.02 s, is seen at about 0.12 s.

      **Question 5.** Call :math:`d'` the time at which the act sees the
      failure: 0.06 s for ``0.05`` and 0.12 s for ``0.12``. The limit of
      0.2 s is longer than :math:`d'`, so in ``Retry(Timeout(act))`` the
      Timeout never fires.

      1. Attempts start every :math:`d'` + 0.02 s: every 0.08 s for ``0.05``
         (0.00, 0.08, 0.16 s) and every 0.14 s for ``0.12`` (0.00, 0.14,
         0.28 s).
      2. ``Retry(Timeout(act))`` ends when the third attempt fails:
         0.16 + 0.06 = **0.22 s** for ``0.05``, and 0.28 + 0.12 = **0.40 s**
         for ``0.12``. Three attempts each time.
      3. ``Timeout(Retry(act))``: Retry alone would end at those same times,
         0.22 s and 0.40 s. Both are after 0.20 s, so the Timeout ends the
         step at **0.20 s**. For ``0.05`` the attempts that started before
         0.20 s are at 0.00, 0.08 and 0.16 s: **3 attempts**, the third cut
         off. For ``0.12`` they are at 0.00 and 0.14 s: **2 attempts**.

      **Question 6.** Measured (two runs of the script, five trials each; all
      ten trials gave the same numbers):

      .. code-block:: text

         Retry(Timeout(act)): FAILURE after 0.22 s, attempts [3]
           run 1 attempts started at 0.00, 0.08, 0.16 s, ended at 0.22 s
         Timeout(Retry(act)): FAILURE after 0.20 s, attempts [3]
           run 1 attempts started at 0.00, 0.08, 0.16 s, ended at 0.20 s

      .. code-block:: text

         Retry(Timeout(act)): FAILURE after 0.40 s, attempts [3]
           run 1 attempts started at 0.00, 0.14, 0.28 s, ended at 0.40 s
         Timeout(Retry(act)): FAILURE after 0.20 s, attempts [2]
           run 1 attempts started at 0.00, 0.14 s, ended at 0.20 s

      The same rule gives the ``fail`` output of Demo 4: 0.15 s is seen at
      0.16 s, attempts start at 0.00, 0.18 and 0.36 s, and the step fails at
      0.36 + 0.16 = 0.52 s.


.. dropdown:: Exercise 4. Replan After a Failed Inspection
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Trigger a replan from the event that GP3 must show, a cell that fails
   inspection, instead of a voltage out of range.

   In Demo 5, ``c3`` was queued for ``tester1`` and turned out to measure
   3.86 V. Now ``c3`` fails inspection: the inspection door pushes it into the
   inspection bin, so it never reaches a tester. Your team's inspection
   report tells your executor, which removes ``c3`` from its record.

   .. raw:: html

      <hr>

   **Part A. Change the demo**

   In your copy of ``demo_replan.py``, make two changes:

   - The mock factory: ``c3`` never reaches ``tester1``, so the queue for
     ``tester1`` becomes ``["c5"]``.

     .. code-block:: python

        factory = ex.MockFactory({1: "c1", 2: "c2"},
                                 {1: ["c5"], 2: ["c4"]}, VOLTS)  # c3 is in the bin

   - The team's record: while plan 1 runs, remove ``c3`` from the
     blackboard. Add these lines just before ``print(f"run plan
     {replans + 1}:")``:

     .. code-block:: python

        if replans == 0:  # c3 fails inspection while plan 1 runs
            ex.set_facts(ex.get_facts() - {("queued", "c3", "tester1")},
                         ex.get_volts())

   1. Plan 1 is made before ``c3`` fails, so it is the same 11 steps as in
      Demo 5. Which step fails now, which leaf fails it, and what does the
      leaf print?
   2. Is the robot holding a cell when the plan stops? Is the stop safe?
   3. Predict the facts that changed in the new problem, and plan 2. Which
      cells ship, and what is the kit voltage?
   4. Run it.

   .. raw:: html

      <hr>

   **Part B. A record that is not updated**

   5. Remove the ``if replans == 0`` lines but keep the factory change: the
      team's record still says ``c3`` is queued. Predict what changes in the
      output, and run it.

   .. raw:: html

      <hr>

   **Part C. One more bad cell**

   6. Set ``c5``'s true voltage to 3.85 V in ``VOLTS``. Run the Part A
      version and the Part B version. Where does each one stop, and why are
      the two endings different?

   .. dropdown:: Solution
      :color: success

      **Question 1.** Step 1 picks ``c1`` and frees ``tester1``. The next
      cell to land on it is ``c5``, not ``c3``. Step 5, ``check-voltage c3
      tester1``, has the guard ``(on-tester c3 tester1)``, which is false.
      The **guard** fails the step, before the act reads any voltage:
      ``guard: (on-tester c3 tester1) is false``.

      **Question 2.** No. Step 4 placed ``c2`` and freed the hand, and step 5
      fails at its guard, between subtrees. It is a safe point.

      **Question 3.** The blackboard now has ``c1`` and ``c2`` in slots
      ``s1`` and ``s2``, ``c4`` on ``tester2``, ``c5`` on ``tester1``, and no
      queued cell. There is no ``voltage-bad`` fact this time: no cell was
      measured out of range. The stand-in planner has two free slots and two
      cells on testers, neither measured yet, so plan 2 checks, picks and
      places ``c4`` into ``s3`` and ``c5`` into ``s4``, then moves the AGV:
      2 × 3 + 1 = 7 steps. The kit is ``c1 c2 c4 c5``, the same four cells as
      in Demo 5: 3.58 + 3.62 + 3.60 + 3.59 = 14.39 V, inside 14.25 V to
      14.55 V.

      **Question 4.** Measured:

      .. code-block:: text

         plan 1, 11 steps:
            1 (pick-from-tester inspection_robot_2 c1 tester1)
            2 (place-in-slot inspection_robot_2 c1 agv1 s1)
            3 (pick-from-tester inspection_robot_2 c2 tester2)
            4 (place-in-slot inspection_robot_2 c2 agv1 s2)
            5 (check-voltage c3 tester1)
            6 (pick-from-tester inspection_robot_2 c3 tester1)
            7 (place-in-slot inspection_robot_2 c3 agv1 s3)
            8 (check-voltage c4 tester2)
            9 (pick-from-tester inspection_robot_2 c4 tester2)
           10 (place-in-slot inspection_robot_2 c4 agv1 s4)
           11 (move-agv agv1 inspection shipping)
         run plan 1:
           1 pick-from-tester SUCCESS
           2 place-in-slot SUCCESS
           3 pick-from-tester SUCCESS
           4 place-in-slot SUCCESS
           5 check-voltage FAILURE
             guard: (on-tester c3 tester1) is false
         stopped between steps; replans 1 of 3
         new problem, facts that changed:
           + (in-slot c1 agv1 s1)
           + (in-slot c2 agv1 s2)
           + (on-tester c4 tester2)
           + (on-tester c5 tester1)
           - (on-tester c1 tester1)
           - (on-tester c2 tester2)
           - (queued c3 tester1)
           - (queued c4 tester2)
           - (queued c5 tester1)
           - (slot-free agv1 s1)
           - (slot-free agv1 s2)
         plan 2, 7 steps:
            1 (check-voltage c4 tester2)
            2 (pick-from-tester inspection_robot_2 c4 tester2)
            3 (place-in-slot inspection_robot_2 c4 agv1 s3)
            4 (check-voltage c5 tester1)
            5 (pick-from-tester inspection_robot_2 c5 tester1)
            6 (place-in-slot inspection_robot_2 c5 agv1 s4)
            7 (move-agv agv1 inspection shipping)
         run plan 2:
           1 check-voltage SUCCESS
           2 pick-from-tester SUCCESS
           3 place-in-slot SUCCESS
           4 check-voltage SUCCESS
           5 pick-from-tester SUCCESS
           6 place-in-slot SUCCESS
           7 move-agv SUCCESS
         done: agv1 shipped c1 c2 c4 c5 (14.39 V), replans 1

      **Question 5.** The only change is in the list of facts that changed:
      the line ``- (queued c3 tester1)`` is missing, because the record still
      holds that fact. Plan 2 and the shipped kit are the same. The stand-in
      planner takes the cells on the testers first and the queued cells
      after them, and two cells on testers fill the two free slots, so the
      stale ``c3`` is never used. The run looks correct, but the problem the
      planner received describes a cell that does not exist. Part C shows
      when that matters.

      **Question 6.** With ``c5`` at 3.85 V (0.05 V above 3.8 V), plan 2
      places ``c4`` in ``s3``, then step 4's verify fails on ``c5``. The two
      versions then differ.

      Part A version (record updated), from ``run plan 2:`` on:

      .. code-block:: text

         run plan 2:
           1 check-voltage SUCCESS
           2 pick-from-tester SUCCESS
           3 place-in-slot SUCCESS
           4 check-voltage FAILURE
             verify: expected c5 in 3.4 V to 3.8 V
         stopped between steps; replans 2 of 3
         new problem, facts that changed:
           + (in-slot c4 agv1 s3)
           + (voltage-bad c5)
           + (voltage-ok c4)
           - (on-tester c4 tester2)
           - (slot-free agv1 s3)
         no plan: stop and report

      The record knows no good cell for ``s4``, so the stand-in planner
      returns no plan, and the executor **stops and reports** (step 5 of the
      loop). In ARIAC more cells would arrive; in this demo there are only
      five.

      Part B version (record not updated), from ``plan 3`` on:

      .. code-block:: text

         plan 3, 6 steps:
            1 (pick-from-tester inspection_robot_2 c5 tester1)
            2 (recycle inspection_robot_2 c5)
            3 (check-voltage c3 tester1)
            4 (pick-from-tester inspection_robot_2 c3 tester1)
            5 (place-in-slot inspection_robot_2 c3 agv1 s4)
            6 (move-agv agv1 inspection shipping)
         run plan 3:
           1 pick-from-tester SUCCESS
           2 recycle SUCCESS
           3 check-voltage FAILURE
             guard: (on-tester c3 tester1) is false
         stopped between steps; replans 3 of 3
         new problem, facts that changed:
           - (on-tester c5 tester1)
         plan 4, 4 steps:
            1 (check-voltage c3 tester1)
            2 (pick-from-tester inspection_robot_2 c3 tester1)
            3 (place-in-slot inspection_robot_2 c3 agv1 s4)
            4 (move-agv agv1 inspection shipping)
         run plan 4:
           1 check-voltage FAILURE
             guard: (on-tester c3 tester1) is false
         stopped between steps; replans 4 of 3
         replan limit passed: stop and report

      The stale fact ``(queued c3 tester1)`` makes the planner
      count on ``c3`` again and again, and every plan fails at the same
      guard. Only the replan limit stops the loop, after four replans. With
      the record updated, the executor stopped after two replans and with
      the right reason. The new problem is only as good as the blackboard it
      comes from.


.. dropdown:: Exercise 5. Translate a py_trees Subtree to BehaviorTree.CPP XML
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Write the BehaviorTree.CPP XML for a ``py_trees`` subtree, using the
   mapping table of the lecture.

   .. raw:: html

      <hr>

   **Part A. Translate**

   This subtree reads a cell's voltage with a 2 s limit, then either accepts
   the cell or recycles it, with up to two attempts at recycling:

   .. code-block:: python

      root = py_trees.composites.Sequence("CheckVoltage", memory=True, children=[
          py_trees.decorators.Timeout(
              "timeout", ReadVoltage("read"), duration=2.0),
          py_trees.composites.Selector("ok or recycle", memory=True, children=[
              VoltageInRange("in range"),
              py_trees.decorators.Retry(
                  "retry", Recycle("recycle"), num_failures=2),
          ]),
      ])

   ``ReadVoltage`` reads the blackboard key ``tester`` and writes the key
   ``volts``. ``VoltageInRange`` reads ``volts``. ``Recycle`` uses no key.
   In the XML, the node names are ``ReadVoltage``, ``VoltageInRange`` and
   ``Recycle``, and each port has the same name as its key.

   1. Write the XML file, with ``BTCPP_format="4"`` and the tree ID
      ``CheckVoltage``.
   2. What number goes in the Timeout's port, and in what unit?

   .. raw:: html

      <hr>

   **Part B. Change the memory**

   3. Which XML node names change if both composites are built with
      ``memory=False`` instead?

   .. raw:: html

      <hr>

   **Part C (optional). Load it**

   4. Following ``btcpp/place_cell.cpp``, write a small C++ program that
      registers three mock nodes, sets ``tester`` on the root blackboard,
      loads your XML with ``createTreeFromFile`` and ticks it. Build it with
      the ``g++`` line from the :ref:`code page <l7-code-btcpp>`.

   .. dropdown:: Solution
      :color: success

      **Question 1.**

      .. code-block:: xml

         <root BTCPP_format="4">
           <BehaviorTree ID="CheckVoltage">
             <Sequence>
               <Timeout msec="2000">
                 <ReadVoltage tester="{tester}" volts="{volts}"/>
               </Timeout>
               <Fallback>
                 <VoltageInRange volts="{volts}"/>
                 <RetryUntilSuccessful num_attempts="2">
                   <Recycle/>
                 </RetryUntilSuccessful>
               </Fallback>
             </Sequence>
           </BehaviorTree>
         </root>

      Each line comes from the mapping table:

      - ``Sequence`` with memory becomes ``Sequence``.
      - ``Selector`` with memory becomes ``Fallback``.
      - ``Retry(num_failures=2)`` becomes ``RetryUntilSuccessful
        num_attempts="2"``: both allow two attempts in all.
      - The blackboard keys become ports written as ``{key}``. ``volts`` is
        an output port of ``ReadVoltage`` and an input port of
        ``VoltageInRange``; the shared ``{volts}`` connects them.

      **Question 2.** ``msec="2000"``: the BehaviorTree.CPP Timeout counts
      milliseconds, and 2.0 s × 1000 = 2000 ms.

      **Question 3.** ``Sequence`` becomes ``ReactiveSequence`` and
      ``Fallback`` becomes ``ReactiveFallback``. The decorators do not
      change.

      **Question 4.** One answer, with mock nodes that print what they do. The
      first argument is the XML file, the second the voltage that
      ``ReadVoltage`` reports.

      .. code-block:: cpp

         #include <behaviortree_cpp/bt_factory.h>

         #include <filesystem>
         #include <iostream>
         #include <string>

         using namespace BT;

         double true_volts{3.62};

         class ReadVoltage : public SyncActionNode {
          public:
           ReadVoltage(const std::string& name, const NodeConfig& config)
               : SyncActionNode(name, config) {}
           static PortsList providedPorts() {
             return {InputPort<std::string>("tester"),
                     OutputPort<double>("volts")};
           }
           NodeStatus tick() override {
             setOutput("volts", true_volts);
             std::cout << "read " << getInput<std::string>("tester").value()
                       << ": " << true_volts << " V\n";
             return NodeStatus::SUCCESS;
           }
         };

         class VoltageInRange : public ConditionNode {
          public:
           VoltageInRange(const std::string& name, const NodeConfig& config)
               : ConditionNode(name, config) {}
           static PortsList providedPorts() {
             return {InputPort<double>("volts")};
           }
           NodeStatus tick() override {
             double volts{getInput<double>("volts").value()};
             bool ok{3.4 <= volts && volts <= 3.8};
             std::cout << "in range: " << (ok ? "yes" : "no") << '\n';
             return ok ? NodeStatus::SUCCESS : NodeStatus::FAILURE;
           }
         };

         class Recycle : public SyncActionNode {
          public:
           Recycle(const std::string& name, const NodeConfig& config)
               : SyncActionNode(name, config) {}
           static PortsList providedPorts() { return {}; }
           NodeStatus tick() override {
             std::cout << "recycle\n";
             return NodeStatus::SUCCESS;
           }
         };

         int main(int argc, char** argv) {
           true_volts = std::stod(argv[2]);
           BehaviorTreeFactory factory;
           factory.registerNodeType<ReadVoltage>("ReadVoltage");
           factory.registerNodeType<VoltageInRange>("VoltageInRange");
           factory.registerNodeType<Recycle>("Recycle");
           auto tree = factory.createTreeFromFile(
               std::filesystem::absolute(argv[1]));
           tree.rootBlackboard()->set("tester", std::string("tester1"));
           NodeStatus status{tree.tickWhileRunning()};
           std::cout << "tree: " << toStr(status) << '\n';
         }

      Measured with BehaviorTree.CPP 4.10.0, for a cell at 3.62 V and one at
      3.86 V (files saved as ``check_voltage.cpp`` and
      ``check_voltage.xml``, program built as ``check_voltage``):

      .. code-block:: text

         $ ./check_voltage check_voltage.xml 3.62
         read tester1: 3.62 V
         in range: yes
         tree: SUCCESS
         $ ./check_voltage check_voltage.xml 3.86
         read tester1: 3.86 V
         in range: no
         recycle
         tree: SUCCESS

      The ``py_trees`` subtree of Part A, with the same three leaves written
      in Python, printed the same lines for both voltages. A tree whose cell
      is recycled still returns SUCCESS: the Fallback succeeds when its
      second child does. Your executor learns that the cell was bad from the
      blackboard (``volts``), not from the tree's status.


.. dropdown:: Exercise 6. Classify Failures and Find the Leaf That Sees Them
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Apply the four responses (retry, wait, replan, stop) to events of ARIAC
   2025, and name the part of the tree that detects each one.

   .. raw:: html

      <hr>

   **Part A. Classify**

   For each event, give the response and the leaf, decorator or branch that
   detects it.

   1. The inspection conveyor stops while the plan waits for the next cell,
      and ``/inspection_conveyor/status`` reports it.
   2. ``tester2`` starts publishing voltage −1 with ``MALFUNCTIONING`` while
      ``c4`` sits on it.
   3. In Task 2, a grasp of ``assembly_robot_2``'s vacuum tool fails once.
   4. Three cells at 3.75 V are on the tray, and the fourth slot is free.
   5. A high-priority order ID arrives on ``/high_priority_orders`` while
      inspection robot 2 carries a cell to the tray.
   6. The executor has replanned three times, the limit in Demo 5, and the
      fourth plan fails too.

   .. raw:: html

      <hr>

   **Part B. Safe points**

   7. For event 5, where can the executor stop the current plan? What if an
      AGV move is running at that moment?

   .. dropdown:: Solution
      :color: success

      **Question 1. Wait.** The belt comes back and the plan is still right
      once it does. The Challenges page asks teams to pause, watch the status
      until it reports operational, and resume. A branch that watches the
      status topic next to the plan detects it. A Timeout on the pick from
      the conveyor would turn the stop into a failure instead, which is the
      wrong response here.

      **Question 2. Replan.** The plan counts on ``tester2``, so its facts
      are no longer true. The new plan uses only ``tester1``. The Timeout
      around the reading leaf of ``check-voltage c4 tester2`` detects it:
      the leaf skips every message with ``MALFUNCTIONING`` or −1, collects no
      valid reading, and the Timeout fails the step (Demo 3, ``malfunction``).

      **Question 3. Retry.** A second attempt can succeed with the world
      unchanged. A Retry around the grasp subtree detects it from the grasp
      result. The subtree must move the gripper away before it grasps again,
      because the plugin clears the failure only after every suction cup has
      lost contact.

      **Question 4. Replan.** The kit window has closed:
      3 × 3.75 = 11.25 V, so the fourth cell would need 14.25 − 11.25 =
      3.00 V to 14.55 − 11.25 = 3.30 V, below the 3.4 V of any acceptable
      cell. The AGV goes to recycling and the kit starts over. No leaf of
      the running step fails: a check of the cells on the tray against the
      kit window, a branch that watches the blackboard next to the plan,
      detects it.

      **Question 5. Replan.** A new goal arrives, so the remaining steps of
      the current plan are no longer the right ones. The current plan stops
      at a safe point and a Ni-MH kit is planned. A branch that watches
      ``/high_priority_orders`` next to the plan detects it.

      **Question 6. Stop.** Past the replan limit, the executor stops the
      robots and reports why (step 5 of the loop).

      **Question 7.** Between subtrees: let the place finish (the next step
      has not started), or cancel the running skill, which stops the robot
      and retreats out of any shared zone with what it holds. An AGV move
      cannot be cancelled: ``/agvN/move`` rejects cancel requests, so the
      executor waits for its result before it replans. Either way, the
      blackboard must say what the robot holds before the new problem is
      written.
