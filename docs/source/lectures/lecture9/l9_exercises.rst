====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes and the group projects listed in
   the :doc:`syllabus </syllabus/index>`.

Five take-home exercises built on the L9 slides and on the two demonstrations.
Exercises 1 and 2 are paper and arithmetic: the kit windows and the decision
chart. Exercises 3 and 4 change the scripts: the closed-loop timings, and a new
mismatch in the VLM checker. Exercise 5 extends the retry, wait or replan
chart to the high-priority order, on paper and then in ``closed_loop.py``.

.. note::

   The scripts are on the :doc:`code page <l9_code>`. They need Python 3 and
   ``jsonschema`` (on Ubuntu 24.04: ``sudo apt install python3-jsonschema``).
   Work on a copy, for example ``cp closed_loop.py my_loop.py``, so the
   original still matches the notes. Every number in the solutions below
   comes from the arithmetic shown, or from running the changed script with
   Python 3.12.3 and jsonschema 4.10.3.

   The models in both scripts are scripted stand-ins. When you change the
   factory, the canned replies do not change, so a run that needs a reply the
   script does not hold stops early. Exercise 3 stays within the replies the
   script has.


.. dropdown:: Exercise 1. Kit Windows and the Type Check
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Work the voltage arithmetic that the lecture keeps in code, and see what
   the type check in ``vlm_check.py`` can and cannot tell.

   .. raw:: html

      <hr>

   **Parts**

   ``CellTypes.msg`` gives a Li-Ion cell a nominal 3.6 V, a NiMH cell 1.2 V, a
   cell tolerance of 0.2 V and a kit tolerance of 0.15 V.

   1. In ``vlm_check.py``, the four cells on the high-priority tray read 1.21,
      1.18, 1.24 and 1.22 V on a tester. Compute the kit total and say whether
      it is inside the NiMH kit window.
   2. In ``closed_loop.py``, cells c1, c2 and c3 read 3.58, 3.61 and 3.55 V.
      What readings of c4 give a valid Li-Ion kit? Use both the kit window
      and the single-cell range in the script (``CELL_MIN`` and ``CELL_MAX``).
   3. A cell on the high-priority tray reads 2.40 V. What does
      ``type_from_volts()`` return? What verdict does ``cross_check()`` give
      if the VLM says ``NIMH`` for that slot, and what if the VLM says
      ``UNKNOWN``? Is the second verdict what you want?
   4. The lecture says choosing four cells that fit is a job for a function
      the agent calls, not for the LLM. Give the reason from the slides.

   .. dropdown:: Solution
      :color: success

      **1.** :math:`1.21 + 1.18 + 1.24 + 1.22 = 4.85` V. The NiMH window is
      :math:`4 \times 1.2 = 4.8` V plus or minus 0.15 V, so 4.65 V to
      4.95 V. 4.85 V is inside it: :math:`4.85 - 4.65 = 0.20` V above the
      bottom and :math:`4.95 - 4.85 = 0.10` V below the top.

      **2.** The three known cells add to
      :math:`3.58 + 3.61 + 3.55 = 10.74` V. The Li-Ion window is 14.25 V to
      14.55 V.

      1. Lowest c4: :math:`14.25 - 10.74 = 3.51` V.
      2. Highest c4 for the kit: :math:`14.55 - 10.74 = 3.81` V.
      3. The single-cell range is 3.4 V to 3.8 V (``3.6 +/- 0.2``), so c4
         must also be at most 3.80 V.

      So c4 must read from **3.51 V to 3.80 V**. The real c4 read 3.63 V,
      inside, and the kit totals 14.37 V, as the demonstration printed.

      **3.** 2.40 V is above the NiMH range (1.0 V to 1.4 V) and below the
      Li-Ion range (3.4 V to 3.8 V), so ``type_from_volts()`` returns
      ``"UNKNOWN"``.

      - VLM says ``NIMH``: the test is ``"NIMH" not in ("UNKNOWN",
        "UNKNOWN")``, which is true, so the verdict is ``DISAGREE: type``.
      - VLM says ``UNKNOWN``: ``"UNKNOWN"`` is in the tuple, so the verdict is
        ``agree``.

      The second verdict is not what you want: two sources that both do not
      know the type "agree", and the slot is not flagged. A reading outside
      both ranges says something is wrong with the cell or the reading, so
      it should be a flag of its own. Exercise 4 adds checks of this kind.

      **4.** LLMs make arithmetic slips, and ARIAC rejects the kit on any
      slip. A function gets the sum right every time, and the agent calls it
      as a tool.


.. dropdown:: Exercise 2. Place Each Mismatch on the Decision Chart
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Use the retry, wait or replan chart on cases the lecture did not show,
   and check each answer against ``decide()`` in ``closed_loop.py``.

   .. raw:: html

      <hr>

   **Parts**

   For each case, follow the chart from "Goal changed?" and name the exit:
   retry, wait or replan (and the tag, if the exit has one). Give the
   question that decides it.

   1. ``unload_to_tray(2, 3)`` reports a lost grasp. Slot 3 is empty and
      tester 2 still reads 3.63 V. It is the first failure of this step.
   2. Same step, slot 3 empty, but tester 2 now reads 0.00 V.
   3. Same as case 1, but it is the third failure in a row of this step
      (``RETRY_CAP`` is 2).
   4. Both voltage testers report ``MALFUNCTIONING`` at once. (The
      challenges page says one or both testers can fail.)
   5. Tester 1 reports ``MALFUNCTIONING`` right after a ``load_tester`` to
      it, while a tested cell still waits on tester 2 to be moved to the
      tray.
   6. A high-priority order arrives while tester 1 is down.

   .. dropdown:: Solution
      :color: success

      **1. Retry (tag 4).** Goal changed? no. Device down? no. Plan holds?
      yes: the 3.63 V reading says the cell is still on tester 2, as the
      plan assumes. Retries left? yes (0 of 2 used). This is the case at
      t = 190 s in the demonstration.

      **2. Replan (the blue box above "Plan holds?").** A reading of
      0.00 V means the tester is empty, and the slot is empty too: the cell
      left the tester but did not reach the tray. The plan assumed the cell
      was on tester 2, so the plan no longer holds. In the code, ``after()``
      sets ``on_tester`` to ``False`` because 0.00 V is outside 3.4 V to
      3.8 V, and ``decide(False, False, False, False, retries)`` returns
      ``"REPLAN"``.

      **3. Replan (the blue box left of "Retries left?").** The plan still
      holds, but two retries are used up. In the code,
      ``retries < RETRY_CAP`` is ``2 < 2``, false, so ``decide()`` returns
      ``"REPLAN"``. The cap stops the loop from retrying forever.

      **4. Wait (tag 3).** Device down? yes. Another free? no: the other
      tester is down too. Keep the plan and watch both status topics.

      **5. Wait (tag 3).** Device down? yes. Another free? no: tester 2
      holds a cell, so it is not free. The code makes the same call:
      ``free = f.on_tester[other] is None ...`` is ``False``, and
      ``decide(False, True, False, ...)`` returns ``"WAIT"``.

      **6. Replan (tag 1).** "Goal changed?" is the first question, so a new
      goal wins over a device that is down. The new plan must still avoid
      tester 1: in the code, ``problems()`` rejects any plan step that loads
      a tester reporting ``MALFUNCTIONING``, as it rejected model call 2 in
      the demonstration.


.. dropdown:: Exercise 3. Change the Closed-Loop Timings: Wait or Replan?
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Predict, on paper, how the replan policy and the wait policy finish when
   the malfunctions move, then run both and check. Find the rule behind the
   time difference.

   .. raw:: html

      <hr>

   **Parts**

   Each part changes one line at the top of a copy of ``closed_loop.py``
   and keeps every other value. The actions take 25 s (``load_tester``),
   20 s (``unload_to_tray``) and 15 s (``move_agv``); a wait polls every
   5 s. For each part, predict the finish time and the number of model calls
   of both runs (``python3 my_loop.py`` and ``python3 my_loop.py --wait``),
   then run them. Compute the time saved by replanning and the largest model
   latency :math:`L` for which replanning still wins, as the lecture did
   (replanning made two model calls).

   1. Tester 1 ``DURATION`` 20 s instead of 45 s.
   2. Tester 1 ``START_TIME`` 200 s instead of 140 s.
   3. Tester 1 ``DURATION`` 90 s instead of 45 s.
   4. Conveyor ``DURATION`` 60 s instead of 30 s (tester back to the
      original values).
   5. From parts 1, 3 and 4 and the original run, state a rule for the time
      replanning saves.

   .. dropdown:: Solution
      :color: success

      **1. Tester down from 140 s to 160 s.** Until 145 s nothing changes.

      - *Replan:* the run is the same as the original. Tester 1 is checked
        again at 210 s, long after it recovered at 160 s. Finish at
        **245 s**, **3 model calls**.
      - *Wait:* polls at 150, 155 and 160 s; at 160 s the tester is back.
        Then ``unload_to_tray(1, 3)`` 160 to 180 s, ``load_tester(c4, 2)``
        180 to 205 s, the lost grasp 205 to 225 s, the retry 225 to 245 s,
        ``move_agv`` 245 to 260 s. Finish at **260 s**, **1 model call**.
      - Saved: :math:`260 - 245 = 15` s. Replanning wins while
        :math:`2L < 15` s, so while :math:`L < 7.5` s.

      The last lines of the two runs:

      .. code-block:: text

         t=245  done: agv1 at SHIPPING after 3 model calls

      .. code-block:: text

         t=160  check again: OPERATIONAL -> resume the plan
         t=160  check tester 1: 3.55 V -> match
         t=160  act unload_to_tray(1, 3)
         ...
         t=260  done: agv1 at SHIPPING after 1 model call

      **2. Tester down from 200 s to 245 s.** At 145 s tester 1 still works,
      so c3 reads 3.55 V, and its unload ends at 165 s. After that, the plan
      uses only tester 2. No step ever meets the broken tester, so there is
      no mismatch and no replan. Both runs are the same: ``load_tester(c4,
      2)`` 165 to 190 s, the lost grasp 190 to 210 s, the retry 210 to 230 s,
      ``move_agv`` 230 to 245 s. Both finish at **245 s** with **1 model
      call**. Saved: 0 s.

      .. code-block:: text

         t=145  observe tester 1: 3.55 V, OPERATIONAL -> match
         t=145  act unload_to_tray(1, 3)
         t=165  result success; slot 3 occupied, tester 1 0.00 V -> match
         ...
         t=245  done: agv1 at SHIPPING after 1 model call

      A malfunction on a device the plan no longer needs triggers nothing.
      The loop reacts to what it observes, not to what the trial file says.

      **3. Tester down from 140 s to 230 s.**

      - *Replan:* the same as the original until 210 s. Then the step
        ``unload_to_tray(1, 4)`` needs tester 1, which is still down, and
        tester 2 has nothing left to do: the chart says **wait**. Polls
        until 230 s, unload 230 to 250 s, ``move_agv`` 250 to 265 s.
        Finish at **265 s**, **3 model calls**.
      - *Wait:* waits from 145 s to 230 s. Unload c3 230 to 250 s, load c4
        250 to 275 s, the lost grasp 275 to 295 s, the retry 295 to 315 s,
        ``move_agv`` 315 to 330 s. Finish at **330 s**, **1 model call**.
      - Saved: :math:`330 - 265 = 65` s. Replanning wins while
        :math:`2L < 65` s, so while :math:`L < 32.5` s.

      .. code-block:: text

         t=210  check tester 1: MALFUNCTIONING -> MISMATCH
         t=210        expected OPERATIONAL; the cell is on it
         t=210  decision WAIT: keep the plan, watch the status
         t=230  check again: OPERATIONAL -> resume the plan
         ...
         t=265  done: agv1 at SHIPPING after 3 model calls

      .. code-block:: text

         t=330  done: agv1 at SHIPPING after 1 model call

      **4. Conveyor down from 90 s to 150 s.** Both runs wait at 90 s and
      resume at 150 s. ``load_tester(c3, 1)`` runs 150 to 175 s, and tester
      1 is down (140 to 185 s), so the mismatch comes at 175 s instead of
      145 s.

      - *Replan:* load c4 on tester 2 175 to 200 s, the lost grasp 200 to
        220 s, the retry 220 to 240 s, tester 1 (back since 185 s) reads
        3.55 V, unload 240 to 260 s, ``move_agv`` 260 to 275 s. Finish at
        **275 s**, **3 model calls**.
      - *Wait:* polls at 180 and 185 s; back at 185 s. Unload c3 185 to
        205 s, load c4 205 to 230 s, the lost grasp 230 to 250 s, the retry
        250 to 270 s, ``move_agv`` 270 to 285 s. Finish at **285 s**,
        **1 model call**.
      - Saved: :math:`285 - 275 = 10` s. Replanning wins while
        :math:`2L < 10` s, so while :math:`L < 5` s.

      **5. The rule.** Replanning saves the time the tester stays down after
      the mismatch, minus any time the replanned run still has to wait:

      .. list-table::
         :header-rows: 1
         :widths: 22 26 26 26
         :class: compact-table

         * - **Run**
           - **Down after the mismatch**
           - **Replan still waits**
           - **Saved**
         * - Original
           - :math:`185 - 145 = 40` s
           - 0 s
           - 40 s
         * - Part 1
           - :math:`160 - 145 = 15` s
           - 0 s
           - 15 s
         * - Part 3
           - :math:`230 - 145 = 85` s
           - :math:`230 - 210 = 20` s
           - :math:`85 - 20 = 65` s
         * - Part 4
           - :math:`185 - 175 = 10` s
           - 0 s
           - 10 s

      The replan fills the down time with work on the other tester. Here
      that work (load c4, the lost grasp and the retry) takes
      :math:`25 + 20 + 20 = 65` s, so it can hide at most 65 s of down time.
      Whether replanning pays depends on how long the device stays down,
      which the agent does not know when it decides, and on the model's
      latency.


.. dropdown:: Exercise 4. Add a New Mismatch to the VLM Checker
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Find a mistake that the slot-by-slot cross-check in ``vlm_check.py``
   misses, and add the checks that catch it.

   .. raw:: html

      <hr>

   **Parts**

   Work on a copy, ``my_check.py``.

   1. Change ``RECORD`` so slot 3 holds a Li-Ion cell that read 3.62 V:
      ``RECORD = {1: 1.21, 2: 1.18, 3: 3.62, 4: 1.22}``. The stand-in VLM
      still says ``LI_ION`` for slot 3. Predict the verdict for slot 3 and the
      decision line, then run the script.
   2. The two sources agree on slot 3, yet the kit is wrong for this order.
      Add a third check in ``cross_check()``: after the occupancy and type
      checks, flag a slot whose recorded type is not the order's type
      (``ORDER_TYPE = "NIMH"``) with the verdict
      ``WRONG TYPE: order needs NIMH``.
   3. Add a kit check at the end of ``cross_check()``: sum ``RECORD``, compare
      the total with the NiMH kit window, print one line, and flag
      ``"kit"`` if the total is outside it. Predict the total, then run.
   4. Run your version with the original ``RECORD``. Does anything change?
   5. Neither new check uses the VLM's reply. What does that say about
      where the VLM is worth its cost?

   .. dropdown:: Solution
      :color: success

      **1.** For slot 3, ``type_from_volts(3.62)`` is ``LI_ION`` (3.62 V is
      inside 3.4 V to 3.8 V), and the VLM says ``LI_ION``, so the verdict is
      ``agree``. Only slot 4 is flagged. The output (copied from the run):

      .. code-block:: text

         Cross-check before /submit_high_priority_order:
         slot  vlm (conf.)       tray_status  record        verdict
         1     NIMH (0.9)        occupied     NIMH 1.21 V   agree
         2     NIMH (0.85)       occupied     NIMH 1.18 V   agree
         3     LI_ION (0.6)      occupied     LI_ION 3.62 V   agree
         4     empty (0.7)       occupied     NIMH 1.22 V   DISAGREE: occupancy
         decision: do not submit; slots 4 disagree

      The script still does not submit, but only because of slot 4. If the
      VLM had seen slot 4 correctly, it would have submitted a kit with a
      Li-Ion cell in it. Two sources agreeing with each other does not mean
      the world matches the goal. (The column shifts and "slots 4" come from
      the script's print format.)

      **2 and 3.** The changes (three blocks):

      .. code-block:: python

         ORDER_TYPE = "NIMH"                 # the high-priority order's cells
         KIT_MIN, KIT_MAX = 4.65, 4.95       # 4 x 1.2 V +/- 0.15 V, CellTypes.msg

      .. code-block:: python

         elif r["cell_type"] not in ("UNKNOWN", kind):
             verdict = "DISAGREE: type"
         elif kind != ORDER_TYPE:
             verdict = f"WRONG TYPE: order needs {ORDER_TYPE}"

      .. code-block:: python

             total = sum(RECORD.values())
             ok = KIT_MIN <= total <= KIT_MAX
             print(f"kit total {total:.2f} V, window {KIT_MIN} to {KIT_MAX} V -> "
                   f"{'match' if ok else 'MISMATCH'}")
             if not ok:
                 flags.append("kit")
             return flags

      Predicted total: :math:`1.21 + 1.18 + 3.62 + 1.22 = 7.23` V, far above
      4.95 V. The output:

      .. code-block:: text

         Cross-check before /submit_high_priority_order:
         slot  vlm (conf.)       tray_status  record        verdict
         1     NIMH (0.9)        occupied     NIMH 1.21 V   agree
         2     NIMH (0.85)       occupied     NIMH 1.18 V   agree
         3     LI_ION (0.6)      occupied     LI_ION 3.62 V   WRONG TYPE: order needs NIMH
         4     empty (0.7)       occupied     NIMH 1.22 V   DISAGREE: occupancy
         kit total 7.23 V, window 4.65 to 4.95 V -> MISMATCH
         decision: do not submit; slots 3 and 4 and kit disagree

      **4.** With the original record the verdicts are the same as in the
      lecture, and the new kit line passes:
      :math:`1.21 + 1.18 + 1.24 + 1.22 = 4.85` V.

      .. code-block:: text

         3     LI_ION (0.6)      occupied     NIMH 1.24 V   DISAGREE: type
         4     empty (0.7)       occupied     NIMH 1.22 V   DISAGREE: occupancy
         kit total 4.85 V, window 4.65 to 4.95 V -> match
         decision: do not submit; slots 3 and 4 disagree

      **5.** The order-type check and the kit check use only the tester
      readings your team recorded. That is the lecture's point about
      occupancy too: when a topic or your own record already answers a
      question, it answers it for free. The VLM is worth its cost for what no
      record holds: the tray as it looks now, which shows whether a cell went
      where the record says.


.. dropdown:: Exercise 5. The High-Priority Order on the Chart and in the Loop
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Extend the retry, wait or replan chart to the high-priority order: what
   the new plan holds, which mismatches it can meet, and how the closed loop
   detects the order.

   .. raw:: html

      <hr>

   **Parts**

   1. An order arrives on ``/high_priority_orders`` in the middle of the
      demonstration's Li-Ion kit. Which exit of the chart does it take, and
      why does the chart ask about it first?
   2. List the steps the new plan must hold, from the ARIAC challenges page.
      For each step, name something the orchestrator can observe to check
      the step's expected effect.
   3. During the NiMH kit, a cell placed on tester 2 reads 3.59 V. Where
      does this land on the chart, and why can it happen?
   4. In a copy of ``closed_loop.py``, add the order:
      ``HIGH_PRIORITY_ORDER = {"START_TIME": 60, "ID": "HP1"}`` (keys as in
      an ARIAC trial file; the time is chosen for this exercise). Add a
      check at the top of ``before()`` that calls ``decide()`` with
      ``goal_changed=True`` the first time the order is seen. In ``main()``,
      when ``before()`` returns ``"REPLAN"``, log the decision and stop: the
      stand-in model holds no NiMH plan, and building one is GP4's work.
      Predict the time at which the run detects the order, then run it.
   5. Move the order to ``START_TIME`` 100 s, during the conveyor wait. What
      must your ``main()`` do so that the wait loop does not print "resume
      the plan"? At what time is the order detected?

   .. dropdown:: Solution
      :color: success

      **1. Replan (tag 1).** "Goal changed?" is the first question on the
      chart. A new goal makes the whole current plan the wrong plan, so
      retrying a step of it or waiting for a device it needs would spend
      time on work that may no longer be wanted. In ``decide()``, the
      ``if goal_changed`` test comes first for the same reason.

      **2.** The steps come from the challenges page. The checks use ARIAC
      interfaces named in the lecture and on the ARIAC API page.

      .. list-table::
         :header-rows: 1
         :widths: 40 60
         :class: compact-table

         * - **Step**
           - **What the orchestrator observes**
         * - Switch the cell feed to NiMH
             (``/inspection_conveyor/cell_feed/control``)
           - ``/inspection_conveyor/cell_feed/status`` reports the NiMH cell
             type.
         * - Test each NiMH cell on a tester
           - The tester reads 1.0 V to 1.4 V, ``OPERATIONAL``.
         * - Place four NiMH cells on the tray
           - ``/agvN/tray_status`` shows the slot occupied; the tester reads
             near 0 V.
         * - Check the kit before it ships
           - The recorded total is from 4.65 V to 4.95 V; the VLM
             cross-check of the tray agrees on every slot.
         * - Move the AGV to shipping (``/{agv_name}/move``)
           - ``/{agv_name}/info`` reports the shipping station.
         * - Submit with ``/submit_high_priority_order`` and the order ID
           - The service response.
         * - Switch the feed back to Li-Ion
           - ``/inspection_conveyor/cell_feed/status`` reports the Li-Ion
             cell type.

      **3.** 3.59 V is inside the Li-Ion range (3.4 V to 3.8 V): a Li-Ion
      cell. The lecture says why it can happen: Li-Ion cells already on the
      conveyor when the feed switched can still arrive. On the chart: Goal
      changed? no (the goal is still the NiMH kit). Device down? no. Plan
      holds? **no**: the plan assumed this cell is NiMH and goes into the
      kit. So the exit is **replan** (the blue box above "Plan holds?"). The
      new plan must keep the Li-Ion cell out of the NiMH kit.

      **4.** The order arrives at 60 s, but the run detects it at **70 s**.
      The orchestrator checks the topic in ``before()``, between steps, and
      ``load_tester(c2, 2)`` runs from 45 s to 70 s. So 10 s of the 150 s
      high-priority target (``NOMINAL_HIGH_PRIORITY_EXECUTION_DURATION``)
      are gone before the agent reacts.

      One way to write it (the lines added or changed):

      .. code-block:: python

         HIGH_PRIORITY_ORDER = {"START_TIME": 60, "ID": "HP1"}   # chosen here

      In ``Factory``, after ``self.grasp_fails``:

      .. code-block:: python

                 self.order_seen = False

             def high_priority(self):          # /high_priority_orders
                 if self.t >= HIGH_PRIORITY_ORDER["START_TIME"]:
                     return HIGH_PRIORITY_ORDER["ID"]
                 return None

      At the top of ``before()``, after the ``say = ...`` line:

      .. code-block:: python

             order = f.high_priority()
             if order and not f.order_seen:    # first on the chart: the goal
                 f.order_seen = True
                 log(f, f"check /high_priority_orders: {order} -> MISMATCH")
                 log(f, "      expected the Li-Ion kit to stay the goal")
                 return decide(True, False, alternative=False,
                               world_matches=True, retries=0)

      In ``main()``, in place of the first ``if before(f, step) == "WAIT":``
      block:

      .. code-block:: python

                 decision = before(f, step)
                 if decision == "WAIT":
                     log(f, "decision WAIT: keep the plan, watch the status")
                     while (decision := before(f, step, quiet=True)) == "WAIT":
                         f.t += 5                  # poll every 5 s
                     if decision is None:
                         log(f, "check again: OPERATIONAL -> resume the plan")
                         continue
                 if decision == "REPLAN":          # only a goal change gets here
                     log(f, "decision REPLAN: the goal changed (tag 1)")
                     raise SystemExit("stop: the NiMH kit plan is GP4's work")

      The order check logs even in quiet mode, so the wait loop shows it.
      Output with ``START_TIME`` 60:

      .. code-block:: text

         t= 45  act load_tester(c2, 2)
         t= 70  observe tester 2: 3.61 V, OPERATIONAL -> match
         t= 70  check /high_priority_orders: HP1 -> MISMATCH
         t= 70        expected the Li-Ion kit to stay the goal
         t= 70  decision REPLAN: the goal changed (tag 1)
         stop: the NiMH kit plan is GP4's work

      **5.** The wait loop calls ``before()`` every 5 s. In the original
      code, the loop ends on any result other than ``"WAIT"`` and then prints
      "check again: OPERATIONAL -> resume the plan", which would be false
      here: the conveyor is still down. The code above keeps the result in
      ``decision`` and prints "resume" only when it is ``None``. The loop
      polls at 90, 95 and 100 s, so the order is detected at **100 s**, the
      time it arrives:

      .. code-block:: text

         t= 90  check /inspection_conveyor/status: MALFUNCTIONING -> MISMATCH
         t= 90        expected OPERATIONAL; no other conveyor
         t= 90  decision WAIT: keep the plan, watch the status
         t=100  check /high_priority_orders: HP1 -> MISMATCH
         t=100        expected the Li-Ion kit to stay the goal
         t=100  decision REPLAN: the goal changed (tag 1)
         stop: the NiMH kit plan is GP4's work

      With ``START_TIME`` set past the end of the run, the changed script
      prints the same output as the original, line for line.
