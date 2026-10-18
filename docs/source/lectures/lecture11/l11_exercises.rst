====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work: GP4 and the final demo, listed in the
   :doc:`syllabus </syllabus/index>`. No quiz covers L11.

Six take-home exercises built on the L11 slides and on the four
demonstrations. Exercise 1 is arithmetic: the voltage window, the kit window
and the evaluation time. Exercise 2 predicts tick traces of the recovery
tree on paper. Exercises 3, 4 and 5 change the scripts: a backoff wait in
the tree, new calls for the L8 checks, and new limits for the voltage
tester watcher. Exercise 6 places new failures in the taxonomy and chooses
local or global recovery.

.. note::

   The scripts are on the :doc:`code page <l11_code>`. Source ROS 2 Jazzy
   first (``source /opt/ros/jazzy/setup.bash``) so that ``py_trees`` is
   found. Work on a copy, for example ``cp recovery_tree.py my_tree.py``, so
   the original still matches the notes. Every number in the solutions below
   comes from the arithmetic shown, or from running the changed script with
   Python 3.12.3, ``py_trees`` 2.6.0 and ``jsonschema`` 4.10.3.


.. dropdown:: Exercise 1. Windows, Kits and Evaluation Time
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Work the arithmetic behind the voltage checks and the final demo
   schedule, the way the lecture's worked examples do.

   .. raw:: html

      <hr>

   **Parts**

   ``CellTypes.msg`` gives a Li-Ion cell a nominal 3.6 V, a NiMH cell
   1.2 V, a cell tolerance of plus or minus 0.2 V and a kit tolerance of
   plus or minus 0.15 V.

   1. A window of five readings from tester 1 holds 3.61, 3.57 and 3.60 V
      (chosen for this exercise), then two readings of -1 after the
      malfunction starts. Compute the average with the -1 values kept and
      with them rejected. Which one sends a good cell to recycling? What
      does the lecture's ``TesterWatcher.average()`` return at that moment,
      and why?
   2. A high-priority kit holds four NiMH cells that read 1.18, 1.22, 1.25
      and 1.19 V (chosen for this exercise). Is the kit inside the NiMH kit
      window? By how much?
   3. Four NiMH cells each read 1.38 V. Does each cell pass the single-cell
      range? Does the kit pass? What does this say about checking cells one
      at a time?
   4. The lecture computes one evaluation run as 900 / 0.37 seconds of wall
      clock. Suppose 12 teams (a number chosen for this exercise). How many
      hours of machine time do all the runs take, back to back? How many if
      Gazebo ran at 0.5 times real time instead?

   .. dropdown:: Solution
      :color: success

      **1.** The three good readings add to
      :math:`3.61 + 3.57 + 3.60 = 10.78` V.

      1. With the two -1 values kept: :math:`10.78 - 1 - 1 = 8.78` V, and
         :math:`8.78 / 5 = 1.756` V, about 1.76 V.
      2. The Li-Ion range is 3.4 V to 3.8 V. 1.76 V is
         :math:`3.4 - 1.756 = 1.644` V, about 1.64 V, below the lower limit,
         so the average with the -1 values kept sends a good cell to
         recycling.
      3. With the -1 values rejected: :math:`10.78 / 3 = 3.593` V, about
         3.59 V, inside the range.

      ``TesterWatcher.average()`` returns ``None``. The first
      ``MALFUNCTIONING`` reading empties the window
      (``self.window.clear()``) and marks the tester down, and
      ``average()`` returns ``None`` when the tester is down or the window
      holds fewer than ``WINDOW`` (5) valid readings. The watcher gives no
      average at all, which is safer than either number above.

      **2.** :math:`1.18 + 1.22 + 1.25 + 1.19 = 4.84` V. The NiMH kit window
      is :math:`4 \times 1.2 = 4.8` V plus or minus 0.15 V, so 4.65 V to
      4.95 V. 4.84 V is inside: :math:`4.84 - 4.65 = 0.19` V above the
      bottom and :math:`4.95 - 4.84 = 0.11` V below the top.

      **3.** The NiMH cell range is :math:`1.2 \pm 0.2`, so 1.0 V to 1.4 V.
      1.38 V is inside it, so each cell passes. The kit is
      :math:`4 \times 1.38 = 5.52` V, which is :math:`5.52 - 4.95 = 0.57` V
      above the top of the kit window, so the kit fails. A cell check alone
      is not enough: four cells that each pass can still make a bad kit. For
      a kit to pass, the four cells must average between
      :math:`4.65 / 4 = 1.1625` V and :math:`4.95 / 4 = 1.2375` V.

      **4.**

      1. One run: :math:`900 / 0.37 = 2432.4` s, about 40.5 minutes (the
         lecture rounds to 41).
      2. Twelve runs: :math:`12 \times 2432.4 = 29189` s, and
         :math:`29189 / 3600 = 8.1` hours.
      3. At 0.5 times real time, one run is :math:`900 / 0.5 = 1800` s
         (30 minutes), and twelve runs take :math:`12 \times 1800 = 21600`
         s, or 6 hours.

      At the lecture's figures, the runs alone need about 8 hours of machine
      time between the code freeze and the Week 15 class.


.. dropdown:: Exercise 2. Predict the Tick Trace
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Read the recovery tree tick by tick, then check your prediction by
   running it.

   .. raw:: html

      <hr>

   **Parts**

   Use the tree in ``recovery_tree.py`` (selector with memory on; a guard
   around Retry with 3 failures around ``place_on_tester_1``; then
   ``place_on_tester_2``, which succeeds after 2 ticks; then ``hold_cell``).

   1. Tester 1's script is ``["fail", "fail", 1]``: two failures, then an
      attempt that succeeds on its first tick. Write the trace tick by tick.
      Through which child does ``place_cell`` succeed?
   2. Run C again (script ``[3]``, tester 1 breaks before tick 2), but with
      selector memory **off**. Does the selector go back to tester 1 on
      ticks 3 and 4, as it did in Run D? Explain the difference from Run D.
   3. Change ``place_on_tester_2``'s script to ``["fail"]`` and run Run B's
      script (three failures) for 6 ticks. What does the tree return, and
      what is the robot doing? Which layer must notice?

   To check part 1 and part 2, add these lines at the end of the
   ``__main__`` block of your copy:

   .. code-block:: python

      run("E2a: fail, fail, then 1 tick", ["fail", "fail", 1])
      run("E2b: Run C with memory off", [3], flip_at=2, memory=False)

   For part 3, use a second copy: in ``build()``, change
   ``StubSkill("place_on_tester_2", [2], robot)`` to
   ``StubSkill("place_on_tester_2", ["fail"], robot)``, and run
   ``run("Both testers fail", ["fail"] * 3, ticks=6)``.

   .. dropdown:: Solution
      :color: success

      **1.** The run printed:

      .. code-block:: text

         E2a: fail, fail, then 1 tick
         tick 1
                 place_on_tester_1: attempt 1 starts
                 place_on_tester_1: attempt 1 FAILED (injected)
                 retry_3: attempt failed [status: 1 failure from 3]
         tick 2
                 place_on_tester_1: attempt 2 starts
                 place_on_tester_1: attempt 2 FAILED (injected)
                 retry_3: attempt failed [status: 2 failure from 3]
         tick 3
                 place_on_tester_1: attempt 3 starts
                 place_on_tester_1: attempt 3 SUCCEEDED
                 place_cell: SUCCESS through tester_1_ok

      After 2 failures, Retry has seen fewer than 3, so it returns
      ``RUNNING`` both times. The third attempt succeeds, so Retry returns
      ``SUCCESS``, and ``place_cell`` succeeds through ``tester_1_ok``.
      Tester 2 is never tried.

      **2.** The run printed:

      .. code-block:: text

         E2b: Run C with memory off
         tick 1
                 place_on_tester_1: attempt 1 starts
         tick 2
                 tester 1 status is now MALFUNCTIONING
                 tester_1_ok: condition false, stops its branch
                 place_on_tester_1: stopped, cancel sent
                 place_on_tester_2: attempt 1 waits for robot 1
         tick 3
                 place_on_tester_1: CANCELED, robot 1 parked
                 tester_1_ok: condition false, its branch does not start
                 place_on_tester_2: attempt 1 starts
         tick 4
                 tester_1_ok: condition false, its branch does not start
                 place_on_tester_2: attempt 1 SUCCEEDED
                 place_cell: SUCCESS through place_on_tester_2

      With memory off, the selector does start from its first child on
      ticks 3 and 4: the guard is ticked again. But its condition is still
      false, so the guard returns ``FAILURE`` at once, its branch does not
      start, and the selector moves on to tester 2. On tick 3 the cancel's
      ``CANCELED`` result is back, so tester 2 sends its goal, and it
      succeeds on tick 4. Tester 2 is not stopped.

      In Run D the first child does not fail on tick 4. Retry's count had
      reset, and its new attempt waits for robot 1, so Retry returned
      ``RUNNING``. A ``RUNNING`` first child wins the selector, and the
      selector stops tester 2. Memory off is harmful when an earlier child
      can return ``RUNNING`` again; it does no harm when that child keeps
      failing.

      **3.** The run printed:

      .. code-block:: text

         Both testers fail
         tick 1
                 place_on_tester_1: attempt 1 starts
                 place_on_tester_1: attempt 1 FAILED (injected)
                 retry_3: attempt failed [status: 1 failure from 3]
         tick 2
                 place_on_tester_1: attempt 2 starts
                 place_on_tester_1: attempt 2 FAILED (injected)
                 retry_3: attempt failed [status: 2 failure from 3]
         tick 3
                 place_on_tester_1: attempt 3 starts
                 place_on_tester_1: attempt 3 FAILED (injected)
                 retry_3: final failure [status: 3 failure from 3]
                 tester_1_ok: FAILURE, because its child failed
                 place_on_tester_2: attempt 1 starts
                 place_on_tester_2: attempt 1 FAILED (injected)
         tick 4
         tick 5
         tick 6

      On tick 3 both testers fail, and the selector reaches ``hold_cell``,
      which returns ``RUNNING`` on every tick. The tree never returns
      ``FAILURE``: the robot holds the cell and nothing else happens. The
      tree cannot fix this itself, so the status must move up to the planner
      or agent. A Timeout around the selector, or a monitor that reports how
      long the tree has held the cell, gives that layer its signal.


.. dropdown:: Exercise 3. Add a Backoff Wait to the Retry
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Build the "Retry with a wait" pattern from the lecture and see what it
   costs in ticks.

   .. raw:: html

      <hr>

   **Parts**

   The lecture puts a wait in a sequence before the action and wraps the
   sequence in Retry. ``py_trees.timers.Timer`` waits a number of seconds;
   the demonstration counts ticks instead of seconds, so use
   ``py_trees.behaviours.TickCounter``, which returns ``RUNNING`` for
   ``duration`` ticks and then the status you give it.

   1. In your copy of ``recovery_tree.py``, change ``build()`` so that Retry
      wraps a sequence (memory on) of a 2-tick wait and the place on
      tester 1:

      .. code-block:: python

         place_t1 = StubSkill("place_on_tester_1", script_t1, robot)
         wait = py_trees.behaviours.TickCounter(
             "wait_2_ticks", duration=2, completion_status=Status.SUCCESS)
         attempt = py_trees.composites.Sequence(
             "wait_then_place", memory=True, children=[wait, place_t1])
         retry = LoggedRetry(
             "retry_3", attempt, num_failures=3)

      Also change the default ``ticks=6`` of ``run()`` to ``ticks=12``. Run
      the script. On which tick does each attempt start in Run B, and on
      which tick does ``place_cell`` succeed? Compare with Run B in the
      notes.
   2. Why does the first attempt also wait?
   3. In Run C with the wait, the trace has no ``place_on_tester_1: stopped
      by its parent`` line. Why not?

   .. dropdown:: Solution
      :color: success

      **1.** Run B printed:

      .. code-block:: text

         Run B: tester 1 place fails three times
         tick 1
         tick 2
         tick 3
                 place_on_tester_1: attempt 1 starts
                 place_on_tester_1: attempt 1 FAILED (injected)
                 retry_3: attempt failed [status: 1 failure from 3]
         tick 4
         tick 5
         tick 6
                 place_on_tester_1: attempt 2 starts
                 place_on_tester_1: attempt 2 FAILED (injected)
                 retry_3: attempt failed [status: 2 failure from 3]
         tick 7
         tick 8
         tick 9
                 place_on_tester_1: attempt 3 starts
                 place_on_tester_1: attempt 3 FAILED (injected)
                 retry_3: final failure [status: 3 failure from 3]
                 tester_1_ok: FAILURE, because its child failed
                 place_on_tester_2: attempt 1 starts
         tick 10
                 place_on_tester_2: attempt 1 SUCCEEDED
                 place_cell: SUCCESS through place_on_tester_2

      ``TickCounter`` returns ``RUNNING`` on its first 2 ticks and
      ``SUCCESS`` on the third, and the sequence starts the place in that
      same tick. So each attempt takes 3 ticks, and the attempts start on
      ticks 3, 6 and 9. Tester 2 starts on tick 9 and succeeds on tick 10.

      Without the wait (Run B in the notes), ``place_cell`` succeeded on
      tick 4. The wait cost :math:`10 - 4 = 6` ticks: 2 waiting ticks for
      each of the 3 attempts. Run A, with one failure (its output is on the
      :doc:`code page <l11_code>`), now succeeds on tick 7 instead of
      tick 3.

      **2.** The wait is the first child of the sequence, and Retry runs the
      whole sequence on every attempt, the first one included. To wait only
      before a retry, the wait must know whether a failure has happened, for
      example from a value on the blackboard that the place writes when it
      fails.

      **3.** In Run C, tester 1 breaks before tick 2. On tick 2 the sequence
      is still in its wait (``TickCounter`` runs for ticks 1 and 2), so the
      place has not started. The guard stops the wait, not the place, and
      ``StubSkill.terminate()`` prints only when a running place is
      stopped. No goal was sent, so there is no cancel, and tester 2 starts
      in the same tick.


.. dropdown:: Exercise 4. Find the Gaps in the Checks
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Predict which check of ``check_call()`` refuses each call, then find
   calls that pass all three checks and are still wrong, and close one gap
   with an extra guard.

   .. raw:: html

      <hr>

   **Parts**

   ``llm_output_checker.py`` imports L8's code from ``lecture8/code``, so
   keep the two folders side by side, as in the course repository. In a new
   file next to ``llm_output_checker.py``, check calls in the demonstration's
   state (robot 1 holds a cell; robot 2 holds a cell that read 3.55 V; agv1
   slot 1 is occupied; tester 1 is ``MALFUNCTIONING``):

   .. code-block:: python

      from llm_output_checker import DECLS, check_call, make_state, which_check

      tools, rec = make_state()
      snap = tools.snapshot()


      def show(label, name, args):
          error = check_call(name, args, DECLS, snap, rec)
          print(label, "accepted" if error is None
                else f"refused at check {which_check(error)}: {error}")

   1. Predict the check and the message for each call, then run them:

      - G: ``show("G", "robot2_place_in_slot", {"agv": 1})``
      - H: ``show("H", "robot2_place_in_slot", {"agv": "1", "slot": 2})``
      - I: ``show("I", "robot1_pick_from_conveyor", {})``
      - J: ``show("J", "robot2_drop_in_recycling", {})``

   2. Run ``show("K", "robot2_place_in_slot", {"agv": 2, "slot": 1})``.
      The demonstration's goal is "Put the cell robot 2 holds into agv1
      slot 2." What happens, and which part of L8's ``run()`` would notice?
   3. Set ``rec.holding["robot2"] = "NOTHING"``, a record that is out of
      date, and run
      ``show("L", "robot2_pick_from_tester", {"tester": 1})``. What happens,
      and what would the skill do with this call?
   4. Write an extra guard, a function with the same arguments as
      ``guard()``, that refuses to drop a held cell whose reading is inside
      the 3.4 V to 3.8 V window. Check J and the good call A with
      ``check_call()`` and then your guard. L8's ``run()`` takes such a
      function as ``extra_guard``; L9's policy check is one.

   .. dropdown:: Solution
      :color: success

      **1.** The runs printed:

      .. code-block:: text

         G refused at check 2: schema: 'slot' is a required property
         H refused at check 2: schema: '1' is not of type 'integer'
         I refused at check 3 (guard): robot 1 holds CELL, needs NOTHING
         J accepted

      - G: ``robot2_place_in_slot`` requires both ``agv`` and ``slot``.
      - H: ``"1"`` is a string, and the schema asks for an integer.
      - I: the record says robot 1 already holds a cell, and a pick needs
        ``NOTHING``.
      - J: the call is well formed and robot 2 holds a cell, so all three
        checks pass. But that cell read 3.55 V, inside the window: the call
        throws a good cell away. No check refuses it.

      **2.** ``K accepted``: agv2 is at ``INSPECTION`` and its slot 1 is
      free, so every check passes. The call is safe, but it does not serve
      the goal, which names agv1. None of the three checks reads the goal.
      ``run()`` checks the goal in code only when the model says it is done
      (``goal_check``), and the step limit stops a run that never gets there.

      **3.** ``L accepted``. The record now says robot 2 holds nothing, and
      the guard allows a pick from a ``MALFUNCTIONING`` tester. Robot 2 still
      holds the cell, and ``pick_from_tester`` needs the robot to hold
      nothing (skills README), so the skill would end with a failure result
      instead. This is the warning in the notes: a record that is out of
      date passes calls that will fail.

      **4.** One answer:

      .. code-block:: python

         from orchestrator import CELL_MAX, CELL_MIN


         def keep_good_cells(name, args, snap, rec):
             """Refuse to recycle a held cell whose reading is inside the window."""
             volts = rec.held_volts
             if (name == "robot2_drop_in_recycling" and volts is not None
                     and CELL_MIN <= volts <= CELL_MAX):
                 return f"the held cell read {volts:.2f} V, inside {CELL_MIN} to {CELL_MAX} V"
             return None

      Checking J and A with ``check_call()`` and then ``keep_good_cells()``
      printed:

      .. code-block:: text

         robot2_drop_in_recycling refused: the held cell read 3.55 V, inside 3.4 to 3.8 V
         robot2_place_in_slot accepted

      The original script's output did not change: its six replies and two
      policy runs never call ``robot2_drop_in_recycling``.


.. dropdown:: Exercise 5. Change the Watcher's Limits
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   See what each of the watcher's limits and rules buys, by changing one at
   a time.

   .. raw:: html

      <hr>

   **Parts**

   Work on copies of ``tester_watcher.py``; start each part from the
   original.

   1. Set ``STALE_AFTER = 1.0``. When does Run 2 mark tester 1 DOWN? Explain
      the exact time from the last reading before the failure.
   2. A high-priority order puts NiMH cells on the testers. Change the cell
      in ``run()`` from ``3.60`` to ``1.20`` V. Run it with
      ``NO_CELL_BELOW = 0.5``, then with ``NO_CELL_BELOW = 1.5``. What
      changes? What range must ``NO_CELL_BELOW`` stay in?
   3. Delete the status check from ``on_reading()`` (the five lines of the
      ``if status == MALFUNCTIONING:`` block). What does Run 1 print now,
      and what would the tree do with tester 1?

   .. dropdown:: Solution
      :color: success

      **1.** Run 2 printed:

      .. code-block:: text

         Run 2: the docs' behavior (no messages)
           t =  179.5 s  average of last 5: 3.60 V
           t =  181.0 s  tester_1 DOWN: no reading for more than 1.0 s
           t =  200.0 s  average of last 5: none
           t =  225.0 s  tester_1 UP: status OPERATIONAL again
           t =  229.5 s  average of last 5: 3.60 V

      The last reading arrives at 179.9 s (the failure starts at 180.0 s).
      The timer runs every 0.1 s, and the rule is "more than
      ``STALE_AFTER``". At 180.9 s the gap is
      :math:`180.9 - 179.9 = 1.0` s, which is not more than 1.0 s. At
      181.0 s the gap is 1.1 s, so the watcher goes DOWN at 181.0 s. With
      the original 0.5 s it went DOWN at 180.5 s (gap 0.6 s). Doubling the
      limit doubles the time to detect silence, from 0.5 s to 1.0 s after
      the failure starts.

      **2.** With ``NO_CELL_BELOW = 0.5``, Run 1 printed:

      .. code-block:: text

         Run 1: the code's behavior (-1 and MALFUNCTIONING)
           t =  179.5 s  average of last 5: 1.20 V
           t =  180.0 s  tester_1 DOWN: status MALFUNCTIONING, voltage -1
           t =  200.0 s  average of last 5: none
           t =  225.0 s  tester_1 UP: status OPERATIONAL again
           t =  229.5 s  average of last 5: 1.20 V

      With ``NO_CELL_BELOW = 1.5``, both runs print ``none`` for every
      average, including at 179.5 s and 229.5 s: every NiMH reading is below
      1.5 V, so the watcher treats it as "no cell" and empties the window.
      The DOWN and UP lines do not change, because the status and the time
      limit do not depend on the value rule. The high-priority kit could
      never be tested.

      ``NO_CELL_BELOW`` must sit below the lowest reading of a good cell of
      any type, which is the NiMH lower limit, :math:`1.2 - 0.2 = 1.0` V. It
      must also sit well above the empty-tester noise around 0 V: with a
      standard deviation of 0.05 V, 0.5 V is :math:`0.5 / 0.05 = 10`
      standard deviations above 0 V.

      **3.** Run 1 printed:

      .. code-block:: text

         Run 1: the code's behavior (-1 and MALFUNCTIONING)
           t =  179.5 s  average of last 5: 3.60 V
           t =  200.0 s  average of last 5: none
           t =  229.5 s  average of last 5: 3.60 V

      There is no DOWN line. The -1 readings now reach the value rule, which
      reads them as "no cell": the window is emptied, but the watcher stays
      UP. Run 2 is unchanged, because silence is caught by the timer. With
      the code's behavior, the tree would see tester 1 as up and empty, and
      keep placing cells on it for the whole outage. This is why the status
      is checked first.


.. dropdown:: Exercise 6. Classify, Then Choose Local or Global
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Use the failure taxonomy and the rule for choosing on cases the lecture
   did not work.

   .. raw:: html

      <hr>

   **Parts**

   For each case, give the failure type, the signal, the response (retry,
   wait or replan), and whether the recovery is local or global, with the
   reason from the rule. Use the ARIAC
   docs' example files: a feed rate of 0.1 cells per second, and the trial
   file's second voltage tester malfunction (``START_TIME`` 300,
   ``DURATION`` 25, ``TESTER`` 2) and conveyor malfunction (``START_TIME``
   120, ``DURATION`` 30).

   1. Tester 2 goes down for 25 s while tester 1 works.
   2. The conveyor stops for 30 s. If the cell feed keeps spawning cells, as
      the ARIAC code suggests, how many could appear on the stopped belt?
   3. The vacuum tool malfunction has ``TOOL`` 2 and ``GRASP_OCCURRENCE`` 5.
      The skill reports a grasp failure on the fifth grasp. A teammate adds
      Retry with 3 failures directly around the grasp skill. Does it work?
   4. After the feed switches to NiMH for a high-priority order, a cell on
      tester 1 reads 3.6 V.
   5. The LLM agent asks for ``robot2_place_in_slot`` with slot 5, the
      refusal goes back to it, and its next call asks for slot 5 again.

   .. dropdown:: Solution
      :color: success

      **1.** Sensor failure; the signal is status ``MALFUNCTIONING`` with
      voltage -1, or silence past the time limit. **Replan, which is
      global**, as in Example B: the plan assumed two working testers, that
      assumption is false for the whole outage, and tester 1 can do the job.
      Replan to use tester 1 only, and again when tester 2 returns.

      **2.** Sensor failure of the conveyor, with the signal on
      ``/inspection_conveyor/status`` (status ``MALFUNCTIONING``, speed 0).
      At one cell every 10 s, :math:`30 / 10 = 3`, so up to three cells
      could spawn during the stop. This is not checked in simulation, so do
      not count on either zero or three. **Wait, which is local**: no other
      conveyor can do the job, so the plan stays. Pause the work that needs
      the belt, watch the status, and resume.

      **3.** Action failure; the signal is the grasp service returning
      ``success`` false with "Vacuum gripper is malfunctioning", and the
      skill returning a grasp failure. The recovery is **retry, which is
      local** (the shell and the tool are where they were, and the failure is
      temporary). But
      a Retry directly around the grasp does not work: ``vacuum_tool_plugin.cpp``
      clears the malfunction only after every suction pad has lost contact
      with the shell, so a retry in place fails again, three times, and then
      the failure moves up for no reason. Retry must wrap a sequence that
      first moves the gripper away, then approaches and grasps again.

      **4.** World drift: the world changed (a Li-Ion cell already on the
      conveyor arrived after the switch), and no single action failed. The
      signal is a fresh observation, 3.6 V, that differs from the expected
      state, a NiMH cell near 1.2 V. **Replan, which is global**: the
      planner or agent
      decides where this cell goes, for example to a Li-Ion kit on another
      AGV, because the current plan assumed every new cell is NiMH. The
      lecture names this case as world drift inside the high-priority order
      challenge.

      **5.** Plan failure, caught by check 2 (schema) of ``check_call()``:
      slot 5 is greater than the maximum of 4. Two refused calls in a row
      end L8's ``run()`` (``MAX_INVALID = 2``), so the policy stops asking
      and falls back: robot 2 keeps the cell, and the GP3 plan takes the
      step, as in policy run 2 of the demonstration. The call does not reach
      a robot.
