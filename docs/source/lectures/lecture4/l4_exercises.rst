====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes and the four group projects
   listed in the :doc:`syllabus </syllabus/index>`.

Six take-home exercises on the L4 slides and scripts. Exercise 1 is on paper:
it counts what an FSM and a BT cost for two more changes. Exercises 2 to 6
change the scripts: predict composite statuses, change the retry count and
the memory flag, move the tester malfunction in the parallel, remove and
rewrite the condition after the kit check service, and build a selector for
the recycle branch. For every script exercise, **predict the output first,
write it down, then run the script.**

.. note::

   The scripts are on the :doc:`code page <l4_code>`. Work on a copy, so the
   original still gives the output in the notes. Every output below was
   measured on 2026-10-12 with Python 3.12.3, ``py_trees`` 2.6.0 and
   ``py_trees_ros`` 2.6.0 under ROS 2 Jazzy. In the outputs of
   ``ros_tree_demo.py``, the times can move by 0.1 s from run to run; the
   statuses do not.


.. dropdown:: Exercise 1. Two More Changes, Counted
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Count what an FSM and a BT each cost when the step gains more retries, and
   see which costs grow.

   .. raw:: html

      <hr>

   **Specification**

   Start from the end of :ref:`l4-fsm-bt`: after Change 1 and Change 2, the
   FSM has 7 states (the 6 states plus ``pick_again``) and 12 transitions, and
   the BT has 9 nodes (8 plus one ``Retry``, with ``num_failures=2``).

   .. raw:: html

      <hr>

   **Parts**

   1. **Change 3: try the place a second time.** How many states and
      transitions does the FSM have now? How many nodes does the BT have?
   2. **Change 4: allow a third pick attempt.** Answer the same two
      questions, starting from your answer to part 1.
   3. Which change cost the BT no new node at all, and why?

   .. dropdown:: Solution
      :color: success

      **Part 1.** The FSM needs a new state, ``place_again``, to remember
      that the place is on its second attempt.

      1. New arrows: one into ``place_again`` from ``place_in_slot`` (the
         first place failed), and two out of it, to ``done`` and to
         ``stopped``: 3 new arrows.
      2. The first place's arrow to ``stopped`` goes away: the first failure
         now leads to ``place_again``.
      3. Transitions: 12 − 1 + 3 = 14. States: 7 + 1 = 8.

      The BT wraps ``place_in_slot`` in a second ``Retry``: 9 + 1 = 10
      nodes.

      **Part 2.** The FSM needs another state, ``pick_third``.

      1. New arrows: one into it from ``pick_again``, and three out of it (to
         ``place_in_slot``, ``recycle_cell`` and ``stopped``): 4 new arrows.
      2. ``pick_again``'s arrow to ``stopped`` goes away.
      3. Transitions: 14 − 1 + 4 = 17. States: 8 + 1 = 9.

      The BT changes one number: ``num_failures=2`` becomes
      ``num_failures=3``. Still 10 nodes. (Exercise 3, part C, measures that
      ``num_failures=3`` gives three attempts.)

      **Part 3.** Change 4. A ``Retry`` already counts the attempts, so a
      third attempt is a parameter, not new structure. In the FSM, the count
      lives in which state the machine is in, so every extra attempt is a new
      state with its own arrows.


.. dropdown:: Exercise 2. Predict the Composite, Then Run It
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Predict the status of a sequence, a selector and a decorator from their
   children's statuses, including which children are never ticked.

   .. raw:: html

      <hr>

   **Specification**

   In a copy of ``composite_status.py``, change the cases:

   - Sequence (``memory=True``, children ``pick``, ``place``, ``update``):
     replace ``((S, S, S), (S, F, S), (S, R, S))`` with
     ``((F, S, S), (R, F, S), (S, S, F))``.
   - Selector (``memory=False``, children ``place_if_good``, ``recycle``):
     replace ``((S, S), (F, S), (F, F))`` with ``((R, S), (F, R), (S, F))``.
   - Decorators: replace the four ``Inverter`` and ``FailureIsSuccess`` cases
     with ``((FailureIsSuccess, S), (FailureIsSuccess, R))``. Keep the
     ``Timeout`` lines.

   .. raw:: html

      <hr>

   **Parts**

   1. For each of the six composite cases, write the line the script will
      print: every child's status (``INVALID`` if it is not ticked) and the
      parent's.
   2. For the two ``FailureIsSuccess`` cases, write the parent's status.
   3. Run the script and compare. For every line you got wrong, say which
      rule you missed.

   .. dropdown:: Solution
      :color: success

      .. code-block:: text

         Sequence move_cell (memory=True)
           1: pick=FAILURE place=INVALID update=INVALID -> FAILURE
           2: pick=RUNNING place=INVALID update=INVALID -> RUNNING
           3: pick=SUCCESS place=SUCCESS update=FAILURE -> FAILURE
         Selector place_or_recycle (memory=False)
           4: place_if_good=RUNNING recycle=INVALID -> RUNNING
           5: place_if_good=FAILURE recycle=RUNNING -> RUNNING
           6: place_if_good=SUCCESS recycle=INVALID -> SUCCESS
         Decorators
           FailureIsSuccess: child=SUCCESS -> SUCCESS
           FailureIsSuccess: child=RUNNING -> RUNNING
           Timeout tick 1: child=RUNNING -> RUNNING
           Timeout tick 2, after 0.3 s: child=INVALID -> FAILURE

      - **Case 1:** the first child fails, so the sequence fails at once.
        ``place`` and ``update`` are never ticked.
      - **Case 2:** a running child ends the sequence's tick. ``place`` would
        fail, but it is not ticked on this tick, so the sequence returns
        ``RUNNING``, not ``FAILURE``.
      - **Case 3:** a sequence needs every child to succeed; the last one
        fails.
      - **Case 4:** a running child also ends a selector's tick. ``recycle``
        is not ticked.
      - **Case 5:** the first child fails, so the selector tries the second,
        which is running.
      - **Case 6:** the first child succeeds, so the selector succeeds at
        once. ``recycle`` would fail, but it is never ticked.
      - ``FailureIsSuccess`` changes only ``FAILURE``. It passes ``SUCCESS``
        and ``RUNNING`` through, as ``Inverter`` passes ``RUNNING`` through.


.. dropdown:: Exercise 3. Change the Retry Count and the Memory
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Predict how ``num_failures`` and the memory flag change the run of
   ``retry_demo.py``, and find which of the two causes the run without
   memory to never end.

   .. raw:: html

      <hr>

   **Specification**

   Each part changes one thing in ``build`` of a fresh copy of
   ``retry_demo.py``. The script runs each tree with ``memory=True`` and then
   ``memory=False``. Recall: each action leaf returns ``RUNNING`` for one
   tick, then its next result.

   .. raw:: html

      <hr>

   **Parts**

   A. Set ``num_failures=1``. The pick still fails once, then succeeds. On
      which tick does each run end, and with what status?

   B. Back to ``num_failures=2``. Make the pick fail twice before it
      succeeds: ``[Status.FAILURE, Status.FAILURE, Status.SUCCESS]``. On
      which tick does each run end, and with what status?

   C. Keep the pick of part B and set ``num_failures=3``. On which tick does
      the run with memory end? How many times is the pick updated?

   D. Make the pick never fail (``[Status.SUCCESS]``), with
      ``num_failures=2``. Does the run without memory still go on for 14
      ticks? Then remove the ``Retry`` and put ``pick`` straight into the
      sequence (``children=[check, pick, place]``). What happens now? What
      causes the run without memory to never end: the ``Retry``, or the
      memory flag?

   .. dropdown:: Solution
      :color: success

      **Part A.** Both runs end on tick 2 with ``FAILURE``. The pick fails
      on tick 2; with 1 failure allowed, the ``Retry`` passes the
      ``FAILURE`` up at once, and the sequence fails.

      .. code-block:: text

         memory=True
           tick 1: root=RUNNING check=SUCCESS pick=RUNNING place=INVALID
           tick 2: root=FAILURE check=SUCCESS pick=FAILURE place=INVALID
           check_tester_ok updated 1 times, pick updated 2 times
         memory=False
           tick 1: root=RUNNING check=SUCCESS pick=RUNNING place=INVALID
           tick 2: root=FAILURE check=SUCCESS pick=FAILURE place=INVALID
           check_tester_ok updated 2 times, pick updated 2 times

      ``num_failures`` counts failures, not retries: ``num_failures=1``
      gives one attempt and no retry.

      **Part B.** Both runs end on tick 4 with ``FAILURE``. Attempt 1 runs
      on ticks 1 and 2 and fails; the ``Retry`` counts 1 of 2. Attempt 2
      runs on ticks 3 and 4 and fails; that is failure 2 of 2, so the
      ``Retry`` returns ``FAILURE``.

      .. code-block:: text

         memory=True
           tick 1: root=RUNNING check=SUCCESS pick=RUNNING place=INVALID
           tick 2: root=RUNNING check=SUCCESS pick=FAILURE place=INVALID
           tick 3: root=RUNNING check=SUCCESS pick=RUNNING place=INVALID
           tick 4: root=FAILURE check=SUCCESS pick=FAILURE place=INVALID
           check_tester_ok updated 1 times, pick updated 4 times
         memory=False
           tick 1: root=RUNNING check=SUCCESS pick=RUNNING place=INVALID
           tick 2: root=RUNNING check=SUCCESS pick=FAILURE place=INVALID
           tick 3: root=RUNNING check=SUCCESS pick=RUNNING place=INVALID
           tick 4: root=FAILURE check=SUCCESS pick=FAILURE place=INVALID
           check_tester_ok updated 4 times, pick updated 4 times

      This is GP1's "skill that keeps failing": the failure reaches the
      root, and the tree stops instead of looping.

      **Part C.** The run with memory ends on tick 7 with ``SUCCESS``.
      Three attempts of two ticks each take ticks 1 to 6 (fail, fail,
      succeed); the place starts on tick 6 and succeeds on tick 7. The pick
      is updated 3 × 2 = 6 times.

      .. code-block:: text

         memory=True
           tick 1: root=RUNNING check=SUCCESS pick=RUNNING place=INVALID
           tick 2: root=RUNNING check=SUCCESS pick=FAILURE place=INVALID
           tick 3: root=RUNNING check=SUCCESS pick=RUNNING place=INVALID
           tick 4: root=RUNNING check=SUCCESS pick=FAILURE place=INVALID
           tick 5: root=RUNNING check=SUCCESS pick=RUNNING place=INVALID
           tick 6: root=RUNNING check=SUCCESS pick=SUCCESS place=RUNNING
           tick 7: root=SUCCESS check=SUCCESS pick=SUCCESS place=SUCCESS
           check_tester_ok updated 1 times, pick updated 6 times

      The run without memory reaches the place on tick 6, then repeats the
      two-tick loop of the notes and is still ``RUNNING`` after 14 ticks
      (pick updated 14 times).

      **Part D.** Yes. With the ``Retry`` and a pick that never fails, the
      run without memory still goes on for 14 ticks. Without the ``Retry``,
      the result is the same:

      .. code-block:: text

         memory=True
           tick 1: root=RUNNING check=SUCCESS pick=RUNNING place=INVALID
           tick 2: root=RUNNING check=SUCCESS pick=SUCCESS place=RUNNING
           tick 3: root=SUCCESS check=SUCCESS pick=SUCCESS place=SUCCESS
           check_tester_ok updated 1 times, pick updated 2 times
         memory=False
           tick 1: root=RUNNING check=SUCCESS pick=RUNNING place=INVALID
           tick 2: root=RUNNING check=SUCCESS pick=SUCCESS place=RUNNING
           tick 3: root=RUNNING check=SUCCESS pick=RUNNING place=INVALID
           tick 4: root=RUNNING check=SUCCESS pick=SUCCESS place=RUNNING
           tick 5: root=RUNNING check=SUCCESS pick=RUNNING place=INVALID
           tick 6: root=RUNNING check=SUCCESS pick=SUCCESS place=RUNNING
           tick 7: root=RUNNING check=SUCCESS pick=RUNNING place=INVALID
           tick 8: root=RUNNING check=SUCCESS pick=SUCCESS place=RUNNING
           tick 9: root=RUNNING check=SUCCESS pick=RUNNING place=INVALID
           tick 10: root=RUNNING check=SUCCESS pick=SUCCESS place=RUNNING
           tick 11: root=RUNNING check=SUCCESS pick=RUNNING place=INVALID
           tick 12: root=RUNNING check=SUCCESS pick=SUCCESS place=RUNNING
           tick 13: root=RUNNING check=SUCCESS pick=RUNNING place=INVALID
           tick 14: root=RUNNING check=SUCCESS pick=SUCCESS place=RUNNING
           check_tester_ok updated 14 times, pick updated 14 times

      The memory flag
      causes the loop. Without memory, every tick starts at the first child.
      The pick's last status was ``SUCCESS``, not ``RUNNING``, so
      ``py_trees`` calls its ``initialise`` again and the pick starts over.
      A pick that fails once only made the loop start two ticks later.


.. dropdown:: Exercise 4. Move the Tester Malfunction
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   See GP1 trap 1 again with a malfunction that starts later, and compute
   what the broken readings do to the cell's average.

   .. raw:: html

      <hr>

   **Specification**

   In a copy of ``parallel_watch.py``, make the tester work for three ticks
   before it breaks:

   .. code-block:: python

      TESTER = [(3.61, "OPERATIONAL")] * 3 + [(-1.0, "MALFUNCTIONING")] * 7

   .. raw:: html

      <hr>

   **Parts**

   1. Predict both runs (``synchronise=True`` and ``False``): the tick on
      which each ends, its status, and how many times ``tester_ok`` is
      checked.
   2. Compute the average the ``synchronise=True`` run prints, in steps.
   3. A Li-Ion cell is good from 3.4 V to 3.8 V. If the tree used this
      average, what would ``place_or_recycle`` do with the cell? What should
      happen instead?
   4. Change the policy to ``ParallelPolicy.SuccessOnAll(synchronise=sync)``.
      Does either run change?

   .. dropdown:: Solution
      :color: success

      **Part 1.**

      .. code-block:: text

         synchronise=True
           tick 1: tester OPERATIONAL    ok=SUCCESS wait=RUNNING -> RUNNING
           tick 2: tester OPERATIONAL    ok=SUCCESS wait=RUNNING -> RUNNING
           tick 3: tester OPERATIONAL    ok=SUCCESS wait=RUNNING -> RUNNING
           tick 4: tester MALFUNCTIONING ok=SUCCESS wait=RUNNING -> RUNNING
           tick 5: tester MALFUNCTIONING ok=SUCCESS wait=SUCCESS -> SUCCESS
           tester_ok checked 1 times
           average of 5 readings: 1.766 V
         synchronise=False
           tick 1: tester OPERATIONAL    ok=SUCCESS wait=RUNNING -> RUNNING
           tick 2: tester OPERATIONAL    ok=SUCCESS wait=RUNNING -> RUNNING
           tick 3: tester OPERATIONAL    ok=SUCCESS wait=RUNNING -> RUNNING
           tick 4: tester MALFUNCTIONING ok=FAILURE wait=INVALID -> FAILURE
           tester_ok checked 4 times

      With ``synchronise=True``, ``tester_ok`` succeeds on tick 1 and is
      skipped from then on, so the run succeeds on tick 5 as if the tester
      were fine. With ``synchronise=False``, the check runs on every tick
      and fails on tick 4, the first broken tick; the parallel fails and
      stops ``wait_for_voltage`` (``INVALID``).

      **Part 2.**

      1. Three good readings: 3 × 3.61 = 10.83 V.
      2. Two broken readings: 2 × (−1.0) = −2.0 V, so the sum is 10.83 V
         less 2.0 V = 8.83 V.
      3. Average: 8.83 / 5 = 1.766 V.

      **Part 3.** 1.766 V is below 3.4 V, so ``voltage_in_range`` fails and
      the selector recycles the cell. The cell read 3.61 V while the tester
      worked, inside 3.4 V to 3.8 V, so a good cell would be thrown away.
      Instead, the wait should fail on tick 4, as the ``synchronise=False``
      run does, so the tree can handle the malfunction (for example, wait
      for the tester and read the cell again) instead of deciding on bad
      data.

      **Part 4.** No. The output is the same, line for line. ``SuccessOnAll``
      also takes ``synchronise``, ``True`` by default, so it has the same
      trap. The fix is the flag, not the policy.


.. dropdown:: Exercise 5. The Condition after the Kit Check
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   See GP1 trap 2 in a running tree, then write the condition that catches
   it.

   .. raw:: html

      <hr>

   **Specification**

   In a copy of ``ros_tree_demo.py``, delete the line ``KitIsGood(),`` from
   the sequence in ``build``. Run ``python3 ros_tree_demo.py bad_kit``.

   .. raw:: html

      <hr>

   **Parts**

   A. Before you run it, predict the last four tree lines and the
      ``tree finished`` line. How many ticks, and what status?

   B. Without looking at ``KitIsGood`` in the original, write a condition
      leaf ``kit_is_good`` that reads ``/kit/check`` and returns ``SUCCESS``
      only if the reply says ``success``. Put it back after ``check`` and run
      ``bad_kit`` again.

   C. In GP1 the service is ARIAC's check kit quality service
      (``ariac_interfaces/srv/CheckKitQuality``). Its reply has two fields:
      ``bool is_good`` and ``string message``. What one line of your leaf
      changes?

   .. dropdown:: Solution
      :color: success

      **Part A.** The tree **succeeds** after 21 ticks, although the reply
      says the kit was rejected:

      .. code-block:: text

          2.0 s  tick 20: check_kit RUNNING
          2.1 s  tick 21: check_kit SUCCESS
          2.1 s  tick 21: move_cell SUCCESS
         check_kit reply: success=False, message='stand-in: kit rejected'
         tree finished: SUCCESS after 21 ticks; 21 voltage messages heard

      ``check_kit`` returns ``SUCCESS`` as soon as the reply arrives, and it
      is now the last child of the sequence, so the sequence succeeds. In
      GP1, the next leaves would move the AGV to shipping and submit a
      rejected kit.

      **Part B.** One way, the same as the script's ``KitIsGood``:

      .. literalinclude:: code/ros_tree_demo.py
         :language: python
         :pyobject: KitIsGood

      With it back after ``check``, ``bad_kit`` ends as in the notes
      (:ref:`l4-run3`): ``kit_is_good FAILURE``, ``move_cell FAILURE``,
      ``tree finished: FAILURE after 21 ticks``.

      **Part C.** The test on the reply:
      ``return Status.SUCCESS if reply.is_good else Status.FAILURE``. The
      field name is the only change: ``std_srvs/Trigger`` calls it
      ``success``, ARIAC's service calls it ``is_good``.


.. dropdown:: Exercise 6. A Selector for the Recycle Branch
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Use a selector to give the kit check a fallback: ship a good kit, recycle
   a rejected one.

   .. raw:: html

      <hr>

   **Specification**

   The GP1 handout says: if the kit is not accepted, send the AGV to the
   recycling station and recycle the tray. In a copy of ``ros_tree_demo.py``,
   replace ``KitIsGood()`` at the end of the sequence with a selector
   ``ship_or_recycle`` that has two children:

   - a sequence ``ship_if_good``: ``KitIsGood()``, then a stand-in leaf
     ``ship_kit``;
   - a stand-in leaf ``recycle_tray``.

   For the stand-ins, use ``py_trees.behaviours.Success("ship_kit")`` and
   ``py_trees.behaviours.Success("recycle_tray")``: leaves that return
   ``SUCCESS`` on every tick. In GP1, ``ship_kit`` would be a subtree that
   moves the AGV to shipping with ``/agvN/move`` and submits the kit, and
   ``recycle_tray`` one that moves the AGV to the recycling station and calls
   ``/agvN/recycle_cells`` (listed in the ARIAC ROS API).

   .. raw:: html

      <hr>

   **Parts**

   1. Write the new end of the sequence. Choose memory for the selector and
      the inner sequence, and say why.
   2. Predict the tree lines from tick 21 for ``ok`` and for ``bad_kit``,
      and the final status of each run.
   3. With this selector, ``bad_kit`` ends with the root at ``SUCCESS``. Is
      that right? What must the tree add so a reader of the run log can tell
      a shipped kit from a recycled one?

   .. dropdown:: Solution
      :color: success

      **Part 1.**

      .. code-block:: python

         check,
         py_trees.composites.Selector("ship_or_recycle", True, [
             py_trees.composites.Sequence("ship_if_good", True, [
                 KitIsGood(),
                 py_trees.behaviours.Success("ship_kit"),
             ]),
             py_trees.behaviours.Success("recycle_tray"),
         ]),

      Memory on both. The decision is made once, from one reply, and the
      children after it are actions. In GP1, ``ship_kit`` is an AGV move
      that runs for many ticks and that ARIAC will not cancel. Without
      memory, each of those ticks would start again at ``kit_is_good``;
      with memory, the tree resumes at the running move. The printed tree
      shows the memory as braces:

      .. code-block:: text

         {-} move_cell
             --> read_voltage
             -^- retry_pick
                 --> pick_from_tester
             -^- timeout_place
                 --> place_in_slot
             --> check_kit
             {o} ship_or_recycle
                 {-} ship_if_good
                     --> kit_is_good
                     --> ship_kit
                 --> recycle_tray

      **Part 2.** For ``ok``, the first child of the selector succeeds and
      ``recycle_tray`` is never ticked:

      .. code-block:: text

          2.1 s  tick 21: check_kit SUCCESS
          2.1 s  tick 21: kit_is_good SUCCESS
          2.1 s  tick 21: ship_kit SUCCESS
          2.1 s  tick 21: ship_if_good SUCCESS
          2.1 s  tick 21: ship_or_recycle SUCCESS
          2.1 s  tick 21: move_cell SUCCESS
         check_kit reply: success=True, message='stand-in: kit accepted'
         tree finished: SUCCESS after 21 ticks; 21 voltage messages heard

      For ``bad_kit``, ``kit_is_good`` fails, so ``ship_if_good`` fails
      before ``ship_kit`` runs, and the selector tries ``recycle_tray``:

      .. code-block:: text

          2.1 s  tick 21: check_kit SUCCESS
          2.1 s  tick 21: kit_is_good FAILURE
          2.1 s  tick 21: ship_if_good FAILURE
          2.1 s  tick 21: recycle_tray SUCCESS
          2.1 s  tick 21: ship_or_recycle SUCCESS
          2.1 s  tick 21: move_cell SUCCESS
         check_kit reply: success=False, message='stand-in: kit rejected'
         tree finished: SUCCESS after 21 ticks; 21 voltage messages heard

      Both runs end with ``SUCCESS`` after 21 ticks.

      **Part 3.** It is right for the tree: the selector handled the
      rejected kit, which is what a fallback is for, so its parent sees
      success. But the root status no longer says whether the kit shipped.
      The run log must say it: write the outcome to a blackboard key (for
      example ``/kit/status``, written by ``ship_kit`` or ``recycle_tray``
      after it succeeds) and log it with the reason, the reply's
      ``message``. GP1's run log asks for the kit submission result.
