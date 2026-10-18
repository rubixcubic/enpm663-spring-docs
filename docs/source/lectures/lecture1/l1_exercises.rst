====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes, the four group projects and
   the final demo listed in the :doc:`syllabus </syllabus/index>`.

Five take-home exercises on the L1 slides and the four L1 scripts.
Exercise 1 is paper and arithmetic: the kit voltage window for Ni-MH, the cell
type of a high-priority order. Exercises 2 to 5 change one script each:
predict the result first, write the prediction down, then run the script.

.. note::

   The scripts are on the :doc:`code page <l1_code>`. Work on a copy of each
   script, so the original still gives the outputs in the notes. Every run
   below was measured on ROS 2 Jazzy on 2026-10-12, on a machine with 32 CPU
   cores. Counts that depend on timing (Exercise 3) can differ a little on
   your machine; the solutions say which numbers are exact and which are not.


.. dropdown:: Exercise 1. The Kit Voltage Window for Ni-MH
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Repeat the class's kit voltage window for Ni-MH cells, then use it to pick
   the last cell of a high-priority kit.

   .. raw:: html

      <hr>

   **Part A. The window**

   A Ni-MH cell has a nominal voltage of 1.2 V (``CellTypes.msg``). The tolerances
   are the same as for Li-Ion: plus or minus 0.2 V per cell, plus or minus
   0.15 V per kit.

   1. Compute the target total of a Ni-MH kit and its window.
   2. Compute the range a single Ni-MH cell may be in.
   3. Four Ni-MH cells all sit at the top of that range. What is the kit
      total, and how far is it from the target?

   .. raw:: html

      <hr>

   **Part B. Same tolerance, different share**

   4. For each cell type, write the kit tolerance (0.15 V) as a percent of the
      kit target, and the cell tolerance (0.2 V) as a percent of the nominal
      voltage.
   5. For which cell type is each tolerance looser, compared with the size of
      the voltage?

   .. raw:: html

      <hr>

   **Part C. The last cell of a high-priority kit**

   A high-priority order arrives. Three Ni-MH cells are already on the tray,
   measured at 1.18 V, 1.25 V and 1.21 V (values chosen for this exercise).

   6. Compute the range the fourth cell must be in.
   7. A tested cell reads 1.35 V. Does it pass on its own? Can it go in this
      kit?
   8. Why must your system decide this before the robot places the cell?

   .. dropdown:: Solution
      :color: success

      **Question 1.**

      1. Target: 4 × 1.2 = 4.8 V.
      2. Window: 4.8 − 0.15 = 4.65 V to 4.8 + 0.15 = 4.95 V.

      **Question 2.** 1.2 − 0.2 = 1.0 V to 1.2 + 0.2 = 1.4 V.

      **Question 3.** 4 × 1.4 = 5.6 V, which is 5.6 − 4.8 = 0.8 V above the
      target, the same 0.8 V as the Li-Ion case in class, and far outside the
      0.15 V window. Four good cells can make a bad kit for Ni-MH too.

      **Question 4.**

      .. list-table::
         :header-rows: 1
         :widths: 20 40 40
         :class: compact-table

         * - **Type**
           - **Kit: 0.15 V of the target**
           - **Cell: 0.2 V of the nominal**
         * - Li-Ion
           - 0.15 / 14.4 = 1.04%
           - 0.2 / 3.6 = 5.56%
         * - Ni-MH
           - 0.15 / 4.8 = 3.13%
           - 0.2 / 1.2 = 16.7%

      **Question 5.** Both tolerances are looser for Ni-MH, because the same
      volts are a larger share of a smaller voltage. The cell range is still
      much wider than the kit window in both cases (16.7% against 3.13% for
      Ni-MH), so cell choice matters for both types.

      **Question 6.**

      1. The three cells total 1.18 + 1.25 + 1.21 = 3.64 V.
      2. The fourth cell must be between 4.65 − 3.64 = 1.01 V and
         4.95 − 3.64 = 1.31 V.
      3. A single cell may only be 1.0 V to 1.4 V. The range from step 2 lies
         inside it, so the answer is **1.01 V to 1.31 V**.

      **Question 7.** It passes on its own: 1.35 V is inside 1.0 V to 1.4 V.
      It cannot go in this kit: 3.64 + 1.35 = 4.99 V, which is 0.04 V above
      4.95 V. It is a good cell, so it belongs in another kit, not in the
      recycling bin.

      **Question 8.** Cells lock to the tray once placed (Task 1, step 1d).
      A wrong cell cannot be taken back, so the kit would fail the check kit
      quality service. Your system must keep each cell's measured voltage
      and choose before it places. L3 does this same computation for a
      Li-Ion kit.


.. dropdown:: Exercise 2. Change the QoS Profile
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Learn which pairs of reliability settings connect, and find out why the
   matched run in class received 19 of 20 messages.

   .. raw:: html

      <hr>

   **Part A. Swap the profiles**

   In a copy of ``qos_mismatch.py``, change the publisher's profile from
   ``qos_profile_sensor_data`` to ``10`` (the default profile: reliable,
   depth 10). Leave the subscriber line as it is.

   1. Predict the counts with ``--match`` (reliable publisher, best-effort
      subscriber). Run it.
   2. Predict the counts without ``--match`` (both reliable). Run it.
   3. State the rule that covers all four runs: the two from class and your
      two.

   .. raw:: html

      <hr>

   **Part B. The missing message**

   Go back to the original script. With ``--match`` it prints
   ``sent 20, received 19``.

   4. Add one more ``rclpy.spin_once(node, timeout_sec=0.05)`` after the
      ``while`` loop, before the ``print``. Predict, then run with
      ``--match``.
   5. Was the 20th message lost? Explain where it was.

   .. raw:: html

      <hr>

   **Part C. ARIAC**

   6. Your GP1 node subscribes to the change topic of a break beam your team
      placed. Which profile does the subscription need, and what does your
      node print if you get it wrong?

   .. dropdown:: Solution
      :color: success

      **Question 1.** Prediction: they connect, because a reliable
      publisher can serve a best-effort subscriber. Measured (three runs):

      .. code-block:: text

         sent 20, received 19

      **Question 2.** Prediction: they connect, because the profiles are the
      same. Measured (three runs):

      .. code-block:: text

         sent 20, received 19

      **Question 3.** The only pair that fails is a best-effort publisher
      with a reliable subscriber. A subscriber can ask for less than the
      publisher offers, never more.

      .. list-table::
         :header-rows: 1
         :widths: 30 30 40
         :class: compact-table

         * - **Publisher**
           - **Subscriber**
           - **Measured**
         * - best effort
           - reliable
           - sent 20, received 0, with the RELIABILITY warning (class)
         * - best effort
           - best effort
           - sent 20, received 19 (class)
         * - reliable
           - best effort
           - sent 20, received 19
         * - reliable
           - reliable
           - sent 20, received 19

      **Question 4.** Measured (three runs):

      .. code-block:: text

         sent 20, received 20

      **Question 5.** No. The timer publishes the 20th message during the
      last pass of the ``while`` loop, and the loop then ends before another
      ``spin_once`` takes that message from the subscription. One more spin
      delivers it. A count of 19 is a property of how the script stops, not
      a lost message.

      **Question 6.** ``qos_profile_sensor_data`` (best effort), the profile
      ARIAC's break beam publishes with. With the default profile your node
      runs with no error, prints the two "incompatible QoS" warnings that
      name RELIABILITY, and receives nothing.


.. dropdown:: Exercise 3. Add a Third Callback
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Predict how many status reads a node gets when a second slow callback is
   added, and see that the callback groups, not the number of threads,
   decide the answer.

   .. raw:: html

      <hr>

   **Specification**

   In a copy of ``executor_blocking.py``, add a second slow timer to
   ``Cell.__init__``: a second skill the node waits on. Under the line that
   creates ``fast``, add:

   .. code-block:: python

      other = MutuallyExclusiveCallbackGroup() if two_groups else None

   and under the line that creates the status timer, add:

   .. code-block:: python

      self.create_timer(1.0, self.wait_on_skill, callback_group=other)

   Run every case with ``multi``. Before each run, write down your
   prediction of the status reads in 5 s.

   1. The new timer in its own group, ``other``, as above.
   2. The new timer in the status group: ``callback_group=fast``.
   3. The new timer in the first skill's group: ``callback_group=slow``.
   4. Back to the original script, with ``multi`` but one group: change
      ``Cell(two_groups=(mode == "multi"))`` to ``Cell(two_groups=False)``.
   5. Which matters for the status reads: the executor, or the group the
      status timer shares?

   .. dropdown:: Solution
      :color: success

      The counts come from timing. Each case below ran at least twice on the
      course machine; the numbers for cases 2 and 4 were the same in every
      run, but expect them to differ a little on another machine.

      .. list-table::
         :header-rows: 1
         :widths: 34 26 40
         :class: compact-table

         * - **Case (multi-threaded executor)**
           - **Status reads in 5 s**
           - **Why**
         * - 1. Third timer in its own group
           - 50 in six of seven runs, 49 in one
           - Three groups, so the three callbacks can run at the same
             time. Nothing blocks the status timer.
         * - 2. Third timer shares the status group
           - 13 (two runs)
           - The status timer now waits whenever the second skill callback
             sleeps, which is almost all the time.
         * - 3. Third timer shares the first skill's group
           - 50 (two runs)
           - The two slow callbacks block each other, but the status timer
             has a group of its own.
         * - 4. One default group, multi-threaded
           - 9 (two runs)
           - Both timers are in one mutually exclusive group, so the extra
             threads cannot help.

      **Question 5.** The group. Case 4 uses a multi-threaded executor and
      still gets 9 reads, about as few as the single-threaded run in class
      (11). Case 2 gets 13 with two groups in use. A status callback stays fast
      only if no slow callback shares its mutually exclusive group. In GP1,
      put the callbacks that read status topics in their own group.

      In the case 1 run that gave 49, the script also printed
      ``The following exception was never retrieved: cannot use Destroyable
      because destruction was requested`` at shutdown. The other six runs
      printed only the count.


.. dropdown:: Exercise 4. Cancel at a Different Time
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Predict exactly what a cancelled action returns, from the server's step
   size and period, before running it.

   .. raw:: html

      <hr>

   **Part A. A rule for the cancel**

   The server in ``action_gripper.py`` starts at 0.085 m, sleeps 0.2 s, moves
   0.0085 m and sends feedback, and checks for a cancel request before each
   step.

   1. At what times does each step end? Write a rule: if the cancel request
      arrives at time *t* (between two step ends), how many feedback
      messages arrive, and what position is in the result?
   2. Why is a cancel at exactly 0.4 s a bad test?

   .. raw:: html

      <hr>

   **Part B. Three cancel times**

   In a copy of the script, replace the two ``run_goal`` lines in ``main``
   with:

   .. code-block:: python

      run_goal(client, 0.0, cancel_after=0.3)
      run_goal(client, 0.0, cancel_after=0.9)
      run_goal(client, 0.0, cancel_after=2.5)

   3. Predict the feedback count, the status and the result position for
      each goal. Then run the script.

   .. raw:: html

      <hr>

   **Part C. A goal that is not a whole number of steps**

   Change the three lines to:

   .. code-block:: python

      run_goal(client, 0.04)
      run_goal(client, 0.04, cancel_after=0.5)

   4. Predict, then run. How many steps does the first goal take, and
      where does it stop?

   .. dropdown:: Solution
      :color: success

      **Question 1.** Steps end at 0.2 s, 0.4 s, 0.6 s, and so on: step *k*
      ends at 0.2 × *k* s. A cancel at time *t* arrives during step *k*,
      the first step that ends after *t*. That step finishes, the server
      sees the cancel at its next check, and the result holds *k* feedback
      messages and the position 0.085 − *k* × 0.0085 m.

      **Question 2.** At 0.4 s the second step ends at the same moment the
      cancel arrives. Which comes first depends on a few milliseconds of
      timing, so the answer could be 2 or 3 steps.

      **Question 3.** Predictions from the rule:

      - 0.3 s falls in step 2 (0.2 s to 0.4 s): 2 feedback messages,
        0.085 − 2 × 0.0085 = 0.068 m, ``CANCELED``.
      - 0.9 s falls in step 5 (0.8 s to 1.0 s): 5 feedback messages,
        0.085 − 5 × 0.0085 = 0.0425 m, ``CANCELED``.
      - 2.5 s is after the goal ended: 10 steps take 10 × 0.2 = 2.0 s. The
        goal already succeeded, so the cancel request comes too late:
        10 feedback messages, 0.0000 m, ``SUCCEEDED``.

      Measured (three runs, the same each time):

      .. code-block:: text

         goal to 0.000 m: accepted=True
           cancel requested after 0.3 s
           2 feedback messages, last 0.0680 m
           status CANCELED, result position 0.0680 m
         goal to 0.000 m: accepted=True
           cancel requested after 0.9 s
           5 feedback messages, last 0.0425 m
           status CANCELED, result position 0.0425 m
         goal to 0.000 m: accepted=True
           cancel requested after 2.5 s
           10 feedback messages, last 0.0000 m
           status SUCCEEDED, result position 0.0000 m

      The script still prints "cancel requested after 2.5 s": the client
      sent the request, but the goal had already ended. A behavior tree that
      cancels a skill must read the final status, not assume the cancel
      worked.

      **Question 4.**

      1. The gripper must close 0.085 − 0.04 = 0.045 m, and
         0.045 / 0.0085 = 5.29 steps.
      2. After 5 steps it is at 0.085 − 5 × 0.0085 = 0.0425 m, still above
         0.04 m, so the loop runs a sixth step.
      3. The sixth step would reach 0.0425 − 0.0085 = 0.034 m, but
         ``max(target, position - STEP)`` stops it at 0.04 m.

      So the first goal gives 6 feedback messages, 0.0400 m,
      ``SUCCEEDED``. The second goal is cancelled during step 3, as in
      class: 3 feedback messages, 0.0595 m, ``CANCELED``. Measured (three
      runs):

      .. code-block:: text

         goal to 0.040 m: accepted=True
           6 feedback messages, last 0.0400 m
           status SUCCEEDED, result position 0.0400 m
         goal to 0.040 m: accepted=True
           cancel requested after 0.5 s
           3 feedback messages, last 0.0595 m
           status CANCELED, result position 0.0595 m


.. dropdown:: Exercise 5. Look Up a Different Slot
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Predict a TF2 lookup by hand, check it with the script, and find where
   the small error in the class result comes from.

   .. raw:: html

      <hr>

   **Part A. Slot 4 by hand**

   ARIAC's AGV model file (``ariac_gz/models/agv/model.sdf``, branch
   ``ariac2025``) puts slot 4 at (0.065, −0.05, 0.032) m in the tray frame.
   ARIAC names its frame ``agv1_slot4_frame``.

   1. Use the class's rule, (a, b) maps to about (b, −a), to predict where
      slot 4 is in ``agv1_frame``.

   .. raw:: html

      <hr>

   **Part B. Slot 4 with the script**

   2. In a copy of ``tf_slot_lookup.py``, change the second transform to
      ``agv1_slot4_frame`` at ``(0.065, -0.05, 0.032)``, change ``slot`` to
      ``"agv1_slot4_frame"``, and change "slot 1" to "slot 4" in the
      ``print``. Run it and compare with your prediction.

   .. raw:: html

      <hr>

   **Part C. The exact turn**

   A turn by angle θ about z maps (a, b) to
   (a cos θ − b sin θ, a sin θ + b cos θ).

   3. With θ = −1.57 rad, cos θ = 0.000796 and sin θ = −0.9999997. Compute
      the x of slot 1, (−0.065, 0.05), to five decimal places. Does it
      explain the 0.0499 the script printed in class?
   4. In the original script, replace ``-1.57`` with ``-math.pi / 2`` and run
      it. Predict the output first.

   .. dropdown:: Solution
      :color: success

      **Question 1.** z = 0.35 + 0.032 = 0.382 m, as for slot 1. In the
      plane, (a, b) = (0.065, −0.05) maps to about (b, −a) = (−0.05, −0.065).
      Slot 4 is diagonally opposite slot 1 on the tray: in the tray frame
      both of its numbers have the opposite sign to slot 1's, so its result
      does too.

      **Question 2.** Measured:

      .. code-block:: text

         slot 4 in agv1_frame: x = -0.0499 m, y = -0.0650 m, z = 0.3820 m

      It matches the prediction, with the same 0.0499 in place of 0.05 as
      in class.

      **Question 3.**

      1. a cos θ = −0.065 × 0.000796 = −0.0000517.
      2. b sin θ = 0.05 × (−0.9999997) = −0.0499999, so
         −b sin θ = +0.0499999.
      3. x = −0.0000517 + 0.0499999 = 0.04995 m (more digits, from Python:
         0.0499482).

      Printed to four decimals, 0.0499482 is 0.0499. The small cos θ term,
      0.000796 instead of 0, moves x by 0.065 × 0.000796 = 0.00005 m: almost
      all of the difference from 0.05.

      **Question 4.** With an exact quarter turn, cos θ = 0, so x is exactly
      b = 0.05. Measured:

      .. code-block:: text

         slot 1 in agv1_frame: x = 0.0500 m, y = 0.0650 m, z = 0.3820 m

      The class script keeps −1.57 because that is the value in ARIAC's
      model file. The difference in x is 0.00005 m, or 0.05 mm.
