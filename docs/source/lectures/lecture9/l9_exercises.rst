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
chart. Exercises 3 and 4 change the scripts: the closed loop on a stand-in
factory, and a new mismatch in the VLM checker. Exercise 5 extends the retry,
wait or replan chart to the high-priority order, on paper and against the
replan recording.

.. note::

   The scripts are on the :doc:`code page <l9_code>`. Exercises 3 and 4 run
   offline, with Python 3 and ``jsonschema`` (on Ubuntu 24.04:
   ``sudo apt install python3-jsonschema``), no ARIAC and no API key. Keep
   the course layout, ``lecture9/code`` next to ``lecture8/code``, and work
   on a copy, for example ``cp vlm_check.py my_check.py``, so the original
   still matches the notes. Every number in the solutions below comes from
   the arithmetic shown, from the recordings in the notes, or from running
   the changed script with Python 3.12.3 and jsonschema 4.10.3 on
   2026-10-17.

   The model in Exercises 3 and 4 is scripted: it returns fixed replies, so
   your outputs should match these exactly. When you change the factory, the
   replies do not change, so a run that needs a reply the list does not hold
   stops early.


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
   2. In the replan recording, the first three cells in agv1's tray have the
      records 3.540, 3.444 and 3.645 V (``record.json``). What readings of the
      fourth cell would have given a kit inside ARIAC's window? Use both the
      kit window and the single-cell range in the code (``CELL_MIN`` and
      ``CELL_MAX`` in ``orchestrator.py``). The fourth cell placed read
      3.465 V: was it inside?
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

      **2.** The three cells add to
      :math:`3.540 + 3.444 + 3.645 = 10.629` V. The Li-Ion window is
      14.25 V to 14.55 V.

      1. Lowest fourth cell: :math:`14.25 - 10.629 = 3.621` V.
      2. Highest fourth cell for the kit: :math:`14.55 - 10.629 = 3.921` V.
      3. The single-cell range is 3.4 V to 3.8 V (``3.6 +/- 0.2``), so the
         fourth cell must also be at most 3.80 V.

      So the fourth cell had to read from **3.621 V to 3.80 V**. The cell
      placed read 3.465 V: inside the cell range, so the guard let it in,
      but 3.621 − 3.465 = 0.156 V under the lowest value for the kit. The
      total came out 14.094 V, the 0.156 V short of 14.25 V that the
      lecture shows. The agent had no kit tool, so nothing chose the fourth
      cell for the kit.

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
   and compare the answers with what the demonstration's code and Gemini
   did.

   .. raw:: html

      <hr>

   **Parts**

   For each case, follow the chart from "Goal changed?" and name the exit:
   retry, wait or replan (and the tag, if the exit has one). Give the
   question that decides it. Your team's retry cap is 2 (chosen for this
   exercise).

   1. ``robot2_pick_from_tester(2)`` returns ``GRASP_FAILED``, and robot 2
      holds ``NOTHING``. Tester 2 still reads 3.63 V. It is the first failure
      of this step.
   2. Same step, but tester 2 now reads 0.00 V, and no slot has the cell.
   3. Same as case 1, but it is the third failure in a row of this step.
   4. Both voltage testers report ``MALFUNCTIONING`` at once. (The
      challenges page says one or both testers can fail.)
   5. Tester 1 reports ``MALFUNCTIONING`` while robot 2 holds the cell it
      just picked from tester 1, and tester 2 is empty. This happened in the
      replan recording at obs 3. What did Gemini do next?
   6. A high-priority order arrives while tester 1 is down.
   7. Tester 1 reports ``MALFUNCTIONING``. Which of these calls does the L8
      ``guard()`` refuse: ``robot1_place_on_tester(1)``, and
      ``robot2_pick_from_tester(1)``?

   .. dropdown:: Solution
      :color: success

      **1. Retry (tag 4).** Goal changed? no. Device down? no. Plan holds?
      yes: the 3.63 V reading says the cell is still on tester 2, as the
      plan assumes. Retries left? yes (0 of 2 used).

      **2. Replan (the blue box above "Plan holds?").** A reading of
      0.00 V means the tester is empty, and no slot has the cell: the cell
      left the tester but did not reach the tray. The plan assumed the cell
      was on tester 2, so the plan no longer holds.

      **3. Replan (the blue box left of "Retries left?").** The plan still
      holds, but two retries are used up. The cap stops the loop from
      retrying forever.

      **4. Wait (tag 3).** Device down? yes. Another free? no: the other
      tester is down too. Keep the plan and watch both status topics.

      **5. Replan (tag 2).** Device down? yes. Another free? yes: tester 2 is
      empty and working. In the recording, Gemini put robot 2's cell in
      slot 1 (call 4), then placed the next cell on tester 2 (call 6), which
      read 3.44 V (obs 6). The cell robot 2 held already had its reading
      (3.54 V, obs 2), so the broken tester did not stop it.

      **6. Replan (tag 1).** "Goal changed?" is the first question, so a new
      goal wins over a device that is down. The new plan must still avoid
      tester 1 while it is down.

      **7.** ``guard()`` refuses ``robot1_place_on_tester(1)`` with "tester 1
      is MALFUNCTIONING", and allows ``robot2_pick_from_tester(1)``
      (``orchestrator.py`` lines 119 to 125). Placing a new cell on a broken
      tester gives no reading; taking a cell off it moves the cell to where
      it can still be used, as in case 5.


.. dropdown:: Exercise 3. Replan or Wait on a Stand-in Factory
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Run the L9 closed loop offline, on L8's stand-in factory ``FakeTools``,
   with a scripted model that replans and one that waits. Predict the finish
   time of each on paper, run both, and find the rule behind the
   difference.

   ``FakeTools`` adds 20 s of simulation time per skill call, and a
   ``wait(seconds)`` call adds its seconds. Its cells read 3.61, 3.55, 3.66
   and 3.58 V. These values are chosen for the example. Save this as
   ``my_closed_loop.py`` in ``lecture9/code``:

   .. code-block:: python

      """Exercise 3: the L9 closed loop on the stand-in factory, with scripted replies. No ARIAC."""
      import sys

      import closed_loop as cl          # first: it puts ../../lecture8/code on the import path
      from fake_tools import FakeTools
      from orchestrator import ScriptedModel, run

      DOWN = (50, 120)   # tester 1 MALFUNCTIONING from 50 s to 120 s of simulation time, chosen here
      WAIT_S = 20        # simulation s robot 1 waits before tester 1 is back, chosen here


      def cycle(tester, slot):
          return [cl.act("robot1_pick_from_conveyor"), cl.act("robot1_place_on_tester", tester=tester),
                  cl.act("robot2_pick_from_tester", tester=tester), cl.act("robot2_place_in_slot", agv=1, slot=slot)]


      REPLAN = cycle(1, 1) + cycle(2, 2) + cycle(2, 3) + cycle(2, 4) + [{"text": "done"}]
      WAIT = (cycle(1, 1) + [cl.act("robot1_pick_from_conveyor"), cl.act("wait", seconds=WAIT_S)]
              + cycle(1, 2)[1:] + cycle(1, 3) + cycle(1, 4) + [{"text": "done"}])

      policy = sys.argv[1]
      fake = FakeTools(tester_down={1: DOWN})
      tools = cl.PolicyTools(fake, policy)
      stop = run(ScriptedModel(REPLAN if policy == "replan" else WAIT), tools,
                 f"{cl.GOAL} {cl.POLICY[policy]}", cl.four_slots, cl.tool_names(policy),
                 max_steps=cl.MAX_STEPS, extra_guard=cl.policy_guard(policy), out=lambda line: None)
      print(f"policy {policy}: stop: {stop}; t = {fake.t:.0f} s; {len(fake.calls)} tool calls")

   It uses the same loop, guard, policies and goal check as the
   demonstration. ``out=lambda line: None`` hides the trace; use
   ``out=print`` to see it.

   .. raw:: html

      <hr>

   **Parts**

   1. Predict the finish time and the number of tool calls of the replan
      list. When does it first need tester 1 after the break?
   2. The wait list picks the second cell at 80 s to 100 s. Why does it wait
      20 s before it places the cell on tester 1? Predict its finish time.
   3. Run both: ``python3 my_closed_loop.py replan`` and
      ``python3 my_closed_loop.py wait``.
   4. Set ``WAIT_S = 10``. Predict what the guard does, and how the run
      ends.
   5. Set ``DOWN = (50, 200)``. Which list must change, and how? (The
      ``wait`` tool takes 5 to 60 s.) Predict both finish times.
   6. State a rule for the time replanning saves here. Then say why the two
      Gemini recordings of the lecture, which finished at about 225 s each,
      do not show it.

   .. dropdown:: Solution
      :color: success

      **1. 320 s, 16 tool calls.** Sixteen skill calls at 20 s each:
      :math:`16 \times 20 = 320` s. Cycle 1 places its cell on tester 1 from
      20 s to 40 s, before the break at 50 s, and robot 2 picks it from 40 s
      to 60 s: the guard checks the observation at 40 s, when tester 1 still
      works. After that the list uses tester 2 only, so it never needs
      tester 1 again.

      **2. 340 s.** After cycle 1 and the second pick, the time is
      :math:`5 \times 20 = 100` s. Tester 1 is down until 120 s, and the
      guard refuses a place on a ``MALFUNCTIONING`` tester, so robot 1 waits
      :math:`120 - 100 = 20` s. Then 11 more skill calls:
      :math:`120 + 11 \times 20 = 340` s. The wait run makes 17 tool calls:
      16 skills and 1 ``wait``.

      **3.** The two runs print:

      .. code-block:: text

         policy replan: stop: goal reached; t = 320 s; 16 tool calls

      .. code-block:: text

         policy wait: stop: goal reached; t = 340 s; 17 tool calls

      **4.** After a 10 s wait the time is 110 s, and tester 1 is still
      down. With ``out=print``, the call lines at the end of the trace are
      (the ``obs`` lines are left out here):

      .. code-block:: text

         call 6: 11 messages; scripted
           model:  wait({"seconds": 10})
           result: {"waited_sim_s": 10.0}
         call 7: 13 messages; scripted
           model:  robot1_place_on_tester({"tester": 1})
           orch:   {"error": "refused: tester 1 is MALFUNCTIONING"}
         call 8: 15 messages; scripted
           model:  robot2_pick_from_tester({"tester": 1})
           result: {"code": "GRASP_FAILED", "holding": "NOTHING", "message": "nothing on the tester", "attempts": 1, "wall_s": 0.0}
         call 9: 17 messages; scripted
           model:  robot2_place_in_slot({"agv": 1, "slot": 2})
           orch:   {"error": "refused: robot 2 holds NOTHING, needs CELL"}
         call 10: 19 messages; scripted
           model:  robot1_pick_from_conveyor({})
           orch:   {"error": "refused: robot 1 holds CELL, needs NOTHING"}
         policy wait: stop: 2 invalid outputs in a row; t = 130 s; 7 tool calls

      The guard refused the place, but the scripted list did not change its
      plan: it went on as if the cell were on tester 1. The pick ran and
      failed (``GRASP_FAILED``; a failed skill is not an invalid output), and
      the next two calls broke the guard's holding rule, which ended the run
      on ``MAX_INVALID``. A real model reads the refusal and can choose
      again; a fixed list cannot.

      **5.** The replan list does not change: it never needs tester 1 after
      the break, so it still finishes at **320 s**. The wait list must wait
      :math:`200 - 100 = 100` s, more than one ``wait`` call allows, so
      replace the single ``wait`` with
      ``cl.act("wait", seconds=60), cl.act("wait", seconds=40)``. It
      finishes at :math:`200 + 11 \times 20 =` **420 s**, with 18 tool calls.
      (With the 20 s wait left in, the run ends on
      ``2 invalid outputs in a row`` at 140 s.)

      **6. The rule.** Here replanning saves the time tester 1 is still down
      when the wait run next needs it: :math:`120 - 100 = 20` s in parts 1
      to 3, and :math:`200 - 100 = 100` s in part 5. It saves nothing if the
      other tester has no free time, or if the broken tester comes back
      before the plan needs it. In ARIAC each model call also costs time,
      which this factory does not count.

      The lecture's recordings do not show this saving because other things
      cost more. The replan run lost 80.0 s to two cells under 3.4 V, one of
      them by 0.01 V, which chance alone moves. The wait run held a tested
      cell for 74.4 s, because the goal text did not say it could go to the
      tray. One run of each cannot say which policy is faster, as the
      lecture says.


.. dropdown:: Exercise 4. Add a New Mismatch to the VLM Checker
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Find a mistake that the slot-by-slot cross-check in ``vlm_check.py``
   misses, and add the checks that catch it. The lecture's live run showed
   one already: ``decision()`` said "submit" for a kit whose total was under
   ARIAC's window.

   .. raw:: html

      <hr>

   **Parts**

   Work on a copy, ``my_check.py``, and run the scripted check with
   ``python3 my_check.py``.

   1. Change ``RECORD`` so slot 3 holds a Li-Ion cell that read 3.62 V:
      ``RECORD = {1: 1.21, 2: 1.18, 3: 3.62, 4: 1.22}``. The stand-in VLM
      still says ``LI_ION`` for slot 3. Predict the verdict for slot 3 and the
      decision line, then run the script.
   2. The two sources agree on slot 3, yet the kit is wrong for this order.
      Add a third check in ``cross_check()``: after the occupancy and type
      checks, flag a slot whose recorded type is not the order's type
      (``ORDER_TYPE = "NIMH"``) with the verdict
      ``WRONG TYPE: order needs NIMH``.
   3. Add a kit check at the end of ``cross_check()``: sum the record,
      compare the total with the NiMH kit window, print one line, and flag
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
         3     LI_ION (0.6)      occupied     LI_ION 3.62 V agree
         4     empty (0.7)       occupied     NIMH 1.22 V   DISAGREE: occupancy
         decision: do not submit; slots 4 disagree

      The script still does not submit, but only because of slot 4. If the
      VLM had seen slot 4 correctly, it would have submitted a kit with a
      Li-Ion cell in it. Two sources agreeing with each other does not mean
      the world matches the goal. ("slots 4" comes from the script's print
      format.)

      **2 and 3.** The changes (three blocks). Above ``RECORD``:

      .. code-block:: python

         ORDER_TYPE = "NIMH"                 # the high-priority order's cells
         KIT_MIN, KIT_MAX = 4.65, 4.95       # 4 x 1.2 V +/- 0.15 V, CellTypes.msg

      In ``cross_check()``, after the type check:

      .. code-block:: python

         elif kind is not None and kind != ORDER_TYPE:
             verdict = f"WRONG TYPE: order needs {ORDER_TYPE}"

      At the end of ``cross_check()``, after the loop:

      .. code-block:: python

             total = sum(v for v in record.values() if v is not None)
             ok = KIT_MIN <= total <= KIT_MAX
             print(f"kit total {total:.2f} V, window {KIT_MIN} to {KIT_MAX} V -> {'match' if ok else 'MISMATCH'}")
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
         3     LI_ION (0.6)      occupied     LI_ION 3.62 V WRONG TYPE: order needs NIMH
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

      With the Li-Ion window (14.25 V to 14.55 V) in place of the NiMH one,
      the same kit check would have flagged the lecture's live run: its
      total was 14.09 V.

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
   the new plan holds, which mismatches it can meet, and when the closed
   loop of the demonstration could notice the order.

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
   4. The orchestrator's observation, ``snapshot()`` in ``skill_tools.py``,
      reads the simulation time, the testers, the conveyor and the three
      AGVs. Could the demonstration's agent notice a high-priority order?
      What would you add?
   5. Suppose you add the order to the observation. In the replan recording,
      obs 4 came at :math:`t` = 37.1 s and obs 5 at :math:`t` = 48.2 s. An
      order arrives at :math:`t` = 40 s. When does the loop first see it,
      and what share of the 150 s high-priority target is gone by then?

   .. dropdown:: Solution
      :color: success

      **1. Replan (tag 1).** "Goal changed?" is the first question on the
      chart. A new goal makes the whole current plan the wrong plan, so
      retrying a step of it or waiting for a device it needs would spend
      time on work that may no longer be wanted.

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

      **4.** No. ``snapshot()`` returns ``sim_time_s``, ``testers``,
      ``conveyor`` and ``agvs``, and no tool reads ``/high_priority_orders``,
      so neither the model nor the guard ever sees an order. Add a reading
      of that topic to ``snapshot()``, so every observation carries the
      latest order, or add a tool that reads it. The first is safer: the
      model cannot forget to call it, and the goal check in code can see the
      order too.

      **5.** The loop observes only after each tool call. The call in
      progress at 40 s ends with obs 5, so the loop first sees the order at
      **48.2 s**, :math:`48.2 - 40 = 8.2` s after it arrived. That is
      :math:`8.2 / 150 = 5.5\%` of the 150 s target
      (``NOMINAL_HIGH_PRIORITY_EXECUTION_DURATION``), before the model has
      even been asked. The model's call then adds its own latency: 0.61 to
      0.85 s of wall time per call in L8's Run 1.
