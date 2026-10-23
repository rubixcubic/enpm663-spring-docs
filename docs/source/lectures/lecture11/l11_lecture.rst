====================================================
Lecture
====================================================

.. note::

   These notes follow the L11 slides shown in class, in the same order and
   with the same sections, so you can read them at home. Every program
   output below is copied from the files the four L11 scripts wrote when
   they ran with Python 3.12.3, ``py_trees`` 2.6.0 and ``jsonschema``
   4.10.3. The scripts and how to run them are on the
   :doc:`code page <l11_code>`.

.. important::

   **None of the demonstrations needs ARIAC or a model.** The skills in the
   behavior tree demonstrations are stubs that follow a script of outcomes.
   The LLM in the output checker is a scripted stand-in: a fixed list of
   replies. A real model's answers vary. The voltage readings in the watcher
   demonstration are synthetic, and the notes say where each value comes
   from.


.. _l11-recap:

Recap
-----

Quiz 5 First
~~~~~~~~~~~~

Quiz 5 opens the class: 20 minutes, closed notes, on L9 and L10. It is the
last quiz of the course.


From L9 and L10
~~~~~~~~~~~~~~~

- **L9:** the agent compares the state it expects with fresh observations.
  When they differ, it retries a step, waits for a device, or replans.
- **L10:** frames, transforms and motion planning, the motion layer under
  the skills package, and the seven failure results a skill can return.


Today's Question
~~~~~~~~~~~~~~~~

**What does the system do when something goes wrong, and which layer
handles it?**


.. _l11-final-demo:

The Final Demo Specification
----------------------------

The specification is posted today on ELMS-Canvas and on the course site
(:doc:`Final Demo </assignments/final_demo>`). The demo is in Week 15
(05/05), and it is 20% of the course grade.


What Your System Must Do
~~~~~~~~~~~~~~~~~~~~~~~~

1. Run a full ARIAC 2025 trial with one system built from GP1 to GP4:
   Task 1 (inspection and kit building) and Task 2 (module construction with
   the assembly robots and the gantry welder).
2. Handle any of the four ARIAC challenges. Any of them can occur in the
   trial.
3. Use a hosted **embodied-reasoning model** (for example Google's Gemini
   Robotics ER) for one perception step: it judges cell defects from a
   camera image of the inspection conveyor. An embodied-reasoning model
   is a VLM built to answer spatial questions about an image (L9).
4. Measure that model with **precision and recall** (L5) on the same cells
   as your GP2 lidar detector.
5. Run from a Dockerfile.

.. note::

   **Task 2 brings the vacuum tool malfunction.** GP4 does not test it, so
   the final demo is the first place your system meets it.


How the Demo Is Run and Graded
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Before the Week 15 class:**

1. Your team tags its code at the **code freeze**, the last commit the
   evaluation uses.
2. The instructor builds every team's Docker image from that tag and runs
   it on the same ARIAC trial, which no team has seen, on one machine.
3. ARIAC scores each run. Each team gets its own results and its recorded
   run.

**In class (Week 15, 05/05):**

- Each team presents for 5 to 6 minutes with its recorded run:
  architecture, design decisions, failure modes met, and how the system
  handled them.
- Peer review follows the demo.


What Is Set
~~~~~~~~~~~

**Set: the code freeze is Friday, April 30, 2027, at 11:59 pm.** The ARIAC
docs' example trial has a time limit of 900 s of simulation time. Gazebo ran
at about 0.37 times real time on the development PC, so one run takes about
:math:`900 / 0.37 = 2432` s, or 41 minutes, of wall-clock time. For 12 teams:
:math:`12 \times 41 = 492` minutes, about 8 hours, before the Week 15 class.

**Set: the grading rubric.** 75 points for the run and 25 for the class
session, scaled to 20% of the course grade. The final demo page lists each
criterion and how its points are computed.

**Set: the model.** Gemini Robotics ER is the course example. Your team may
use another vision-language model if it is a Google model that runs on the
course key, or a model that runs locally, and if it reports the same
comparison. The instructor runs every image with one course API key.

**Set: who pays.** The course key runs the graded runs only (GP4 and the
final demo). While you develop, your team uses its own free-tier Gemini key.


What the Unseen Trial Means
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- You cannot tune your system for a known order of challenges. Detection and
  recovery must work for any order. That is this lecture; L12 shows how to
  measure whether it works.
- Read the specification as a team and bring your questions to L13.


.. _l11-taxonomy:

A Failure Taxonomy
------------------

This section names four types of failure, the signal that detects each one,
and where its recovery starts.


Four Failure Types and the Signal for Each
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: the four failure types
   :class: note

   - An **action failure**: a skill or service call does not do what it was
     asked.
   - A **sensor failure**: a device gives no data or wrong data.
   - A **plan failure**: the plan is invalid.
   - **World drift**: the world changed, and no single action failed.

.. figure:: /_static/images/l11/failure_taxonomy.svg
   :alt: A block diagram in four rows and four columns. Row Failure type: tag 1 Action, tag 2 Sensor, tag 3 Plan and tag 4 World drift, in amber boxes. Row Signal, under each type: skill returns a failure reason; status field, impossible value or silence; fails a check before it runs; fresh observation differs from the expected state. Row Recovery starts in: under Action, a blue box, behavior tree (retry, fallback); under Sensor, a black box, a check before the value is used; under Plan and World drift, one red box, planner or agent (a new plan). Row New source, on top: two dashed boxes, VLM output with a dashed arrow into Sensor, and LLM output with a dashed arrow into Plan.
   :width: 95%
   :align: center

   1: action. 2: sensor. 3: plan. 4: world drift. Dashed: new sources of
   failure from AI components. Amber: a failure. Blue: the behavior tree.
   Red: the planner or agent.

Read the figure one column at a time, top to bottom: the failure type, the
signal that detects it, and the layer where recovery starts. The two dashed
boxes on top are new sources of failure that come with AI components: VLM
output feeds the sensor column, and LLM output feeds the plan column.


Each Type in ARIAC 2025
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 14 44 42
   :class: compact-table

   * - **Type**
     - **ARIAC example**
     - **Signal**
   * - Action
     - A skill or service call does not do what it was asked: a grasp fails.
     - The skill's failure result, or a service response with ``success``
       false
   * - Sensor
     - A device gives no data or wrong data: a voltage tester malfunction.
     - A status field, an impossible value, or no new message within a time
       limit
   * - Plan
     - The plan is invalid: an LLM plan puts a fifth cell on a four-slot
       tray.
     - A check before the plan runs
   * - World drift
     - The world changed, and no single action failed: a high-priority order
       arrives in the middle of a kit.
     - The expected state differs from fresh observations (the L9 loop)

.. important::

   **The type decides where recovery lives.** Action failures are handled
   close to the action, in the tree. Plan failures and world drift go back
   to the planner or agent. Sensor failures need a check before the value is
   used.

.. admonition:: Definition: local and global recovery
   :class: note

   - **Local recovery** keeps the plan: the skill or the behavior tree
     retries a step or waits.
   - **Global recovery** changes the plan: the planner or LLM agent replans,
     or takes a new goal.


Action Failures: The Seven Skill Results from L10, and the Response to Each
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every course skill ends with a result code (``SkillResult.msg``, skills
README of v0.2.0). L10 named the seven failure results: grasp failed,
precondition failed, place not found, no path found, execution failed, zone
busy and canceled. Each one calls for a different response.

.. list-table::
   :header-rows: 1
   :widths: 28 72
   :class: compact-table

   * - **Result code**
     - **Response, and why**
   * - ``GRASP_FAILED``
     - Retry once, locally (L10). First check that the part is there: a pick
       from an empty tester also ends this way.
   * - ``PRECONDITION_FAILED``
     - Replan (L10): the robot holds the wrong object or the AGV is at the
       wrong station. After a conveyor stop during a catch: wait for
       ``OPERATIONAL``, then catch the next cell (README).
   * - ``PLACE_NOT_FOUND``
     - Replan (L10): a TF2 lookup failed, so the world is not what the plan
       assumed.
   * - ``PLANNING_FAILED``
     - Replan: the skill already tried Pilz, then OMPL (README,
       ``attempts``). Choose another tester, slot or AGV.
   * - ``EXECUTION_FAILED``
     - Retry once, then replan: the skill already re-ran once after MoveIt's
       "controller is taking too long" error (README).
   * - ``ZONE_BUSY_TIMEOUT``
     - Wait, then retry: the other robot held the shared zone too long, and
       the plan still holds.
   * - ``CANCELED``
     - None: your own code sent the cancel (a guard or a Timeout), and that
       code decides what runs next.

The first three responses are L10's. The other four are a starting rule
chosen for this course.


.. _l11-bt-recovery:

Behavior Tree Recovery
----------------------

This section covers fallbacks, Retry, Timeout and guards in ``py_trees``
2.6.0, the version installed with ROS 2 Jazzy. A demonstration then injects
failures into a small tree, with no simulator.


The Building Blocks
~~~~~~~~~~~~~~~~~~~

Each behavior in a tree returns one of three statuses when it is **ticked**
(run once): ``SUCCESS``, ``FAILURE`` or ``RUNNING`` (L4).

.. list-table::
   :header-rows: 1
   :widths: 31 42 27
   :class: compact-table

   * - **py_trees class (arguments)**
     - **What it does**
     - **Use in ARIAC**
   * - ``composites.Selector`` (name, memory, children)
     - Ticks its children in order until one succeeds
     - Tester 1, else tester 2, else hold the cell
   * - ``decorators.Retry`` (name, child, num_failures)
     - Runs its child again after a failure, up to ``num_failures``
       failures
     - A grasp that failed once
   * - ``decorators.Timeout`` (name, child, duration)
     - Fails its child if it is still running after ``duration`` seconds
     - A skill that hangs
   * - ``composites.Parallel`` (name, policy, children)
     - Ticks every child on each tick
     - A monitor beside the work
   * - ``decorators.EternalGuard`` (name, child, condition)
     - Checks the condition before every tick, and stops its child when the
       condition fails
     - Stop work when a tester or the conveyor malfunctions

The signatures were read from the installed ``py_trees`` 2.6.0. A
**decorator** is a node with one child that changes what its child's status
means. A **guard** is a decorator that checks a condition before it ticks its
child; ``EternalGuard`` is the ``py_trees`` guard.


What Retry Does on Each Tick, and How to Add a Wait
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From the ``py_trees`` 2.6.0 source, Retry does one of three things after its
child is ticked:

1. The child fails, and Retry has seen fewer than ``num_failures`` failures:
   Retry returns ``RUNNING``. On the next tick, the child starts again.
2. The child fails for the ``num_failures``-th time: Retry returns
   ``FAILURE``.
3. The child succeeds: Retry returns ``SUCCESS``.

.. admonition:: Definition: backoff
   :class: note

   **Backoff** is a wait before a retry, so a tool or device has time to
   recover before the next attempt.

Retry starts the child again on the very next tick, with no wait. To back
off, put a wait (``py_trees.timers.Timer``) in a sequence before the action,
and wrap the sequence in Retry. Exercise 3 on the
:doc:`exercises page <l11_exercises>` builds this.


The Demonstration Tree: Place a Cell on a Voltage Tester
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Inspection robot 1 must place a cell on a voltage tester. Tester 1 is the
first choice; tester 2 is the fallback; holding the cell is the last resort.

.. figure:: /_static/images/l11/recovery_tree.svg
   :alt: A behavior tree drawn top to bottom. At the top, tag 1, a blue box: Selector (memory on), named place_cell. Lines lead to its three children, left to right: tag 2, a blue box, EternalGuard named tester_1_ok; a gray box, skill place_on_tester_2; tag 4, a blue box, Running named hold_cell. Under the guard is tag 3, a blue box, Retry, 3 failures, named retry_3, and under it a gray box, skill place_on_tester_1. A note beside the tree says children are tried left to right.
   :width: 85%
   :align: center

   1: selector, tries its children left to right until one succeeds.
   2: guard, checks tester 1's status before every tick. 3: Retry, allows 3
   failures. 4: last resort, hold the cell (always ``RUNNING``). Blue: tree
   nodes. Gray: skill calls.

Runs B, C and D below are **separate runs of this tree**, each with its own
injected failure.


The Tree in Code
~~~~~~~~~~~~~~~~

.. literalinclude:: code/recovery_tree.py
   :language: python
   :pyobject: build
   :caption: lecture11/code/recovery_tree.py (excerpt)

- Each skill is a stub (no ROS, no simulator) that follows a script chosen
  for this example: fail, or run for some ticks and succeed. The tester 2
  place takes 2 ticks.
- ``robot`` stands for robot 1's action server. The stubs follow two rules
  of the course skills (README of v0.2.0, "One goal per arm" and "Cancel
  stops the arm and retreats"): robot 1 runs one goal at a time across all
  its skills, and a cancel parks the arm before the result ``CANCELED``
  comes back. A stub sends its goal only once robot 1 is free, and waits
  until then.
- ``LoggedRetry`` and ``LoggedGuard`` are Retry and EternalGuard with a print
  added, so the trace shows what they do.
- ``num_failures=3`` is chosen for this example. This Retry fires on any
  failure. A real one should fire only on a result worth retrying, such as
  ``GRASP_FAILED`` (the results table above).

The script also prints a Run A, with one injected failure and one retry. Its
output is on the :doc:`code page <l11_code>`.


Run B: Three Failures, Then the Fallback
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/recovery_tree.txt
   :language: text
   :lines: 12-29

On the third failure, Retry returns ``FAILURE``, so the guard fails, and the
selector starts tester 2 in the same tick. Robot 1 is free: a skill reports a
failure only after its arm retreats (L10).


Run C: The Guard Stops a Running Branch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/recovery_tree.txt
   :language: text
   :lines: 31-44

1. The place on tester 1 needs 3 ticks (chosen). Before tick 2, tester 1's
   status changes to ``MALFUNCTIONING``. On tick 2 the guard checks its
   condition first, finds it false, and stops the place, which cancels its
   action goal.
2. Skills README (v0.2.0): robot 1 runs one goal at a time, and a cancel
   lifts the arm clear and parks it before ``CANCELED`` comes back. So the
   tester 2 place waits for that result (1 tick here, chosen) before it sends
   its goal. A goal sent at once would be rejected.
3. Tester 1 being down is global recovery: the plan's two testers are now
   one. The new plan, tester 2, is written into this tree in advance; in GP4
   the agent chooses it.


Run D: Why the Selector Has Memory On
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: selector memory
   :class: note

   A selector with **memory on** goes on from the child that was running on
   the last tick. With **memory off**, it starts again from its first child
   on every tick.

Run D is Run B again, with tester 1 still failing, but with selector memory
off. Ticks 1 to 3 are the same as in Run B: tester 2 starts on tick 3. Ticks
4 and 5:

.. literalinclude:: outputs/recovery_tree.txt
   :language: text
   :lines: 61-68

1. With memory off, the selector starts again from its first child on every
   tick. On tick 4 it goes back to tester 1 and stops the place on tester 2
   halfway, which cancels it.
2. On tick 5 the cancel is done, tester 1 is tried again, and the Retry count
   starts again at 1.
3. With memory on (Runs B and C), the selector goes on from its running
   child, so it stays with tester 2.


Timeout Turns a Hang into a Failure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A skill that **hangs** never returns ``SUCCESS`` or ``FAILURE``: it stays
``RUNNING``. Nothing in a tree reacts to that until something turns it into
a failure.

.. literalinclude:: code/timeout_demo.py
   :language: python
   :lines: 28-33
   :caption: lecture11/code/timeout_demo.py (excerpt)

The tree is ticked every 0.2 s, and the Timeout duration is 0.5 s. Both
durations are chosen for this example. Ticks 3 and 4 of the output:

.. literalinclude:: outputs/timeout_demo.txt
   :language: text
   :lines: 5-10

``pick_cell`` never finishes. At 0.6 s, more than 0.5 s after it started,
Timeout stops it and fails. The selector then runs ``report_to_planner``, a
stub that stands for the report to the planner.


.. _l11-llm-checks:

Checking LLM Output
-------------------

This section puts the checks of the L8 orchestrator's ``check_call()``
between the model and the robot, in their order, with the L8 agent's ten
tools.

.. note::

   The model in this section is a scripted stand-in: a fixed list of
   replies. A real model's answers vary.


The Three Checks of L8's Orchestrator, in Its Order
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Tool:** is the name one of the ten tools the orchestrator declared?
   L8's ten are the seven skills of the two inspection robots and three
   readings (testers, conveyor, one AGV).
2. **Schema:** do the arguments fit that tool's JSON schema? Each schema
   gives the types and ranges (AGV 1 to 3, slot 1 to 4, tester 1 or 2) and
   allows no other arguments.
3. **Guard:** does ``guard()`` allow the call in the current state?

A call stops at the first check it fails. The **state** the guard reads has
two parts: the observation read just before the call (testers, conveyor,
AGVs) and the orchestrator's **record** (what each robot holds, each tested
cell's voltage).

.. warning::

   **The guard is only as good as the observation and the record.** A record
   that is out of date passes calls that will fail.


The Checks in Code
~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../lecture8/code/orchestrator.py
   :language: python
   :pyobject: check_call
   :caption: lecture8/code/orchestrator.py, check_call()

- ``decls`` maps each declared tool's name to its declaration; ``snap`` is
  the observation and ``rec`` the record. Each check returns an error text,
  or the next check runs.
- With function calling, the API returns the call already split into a name
  and its arguments, so there is no JSON parse step. L8's ``validator.py``
  adds one for a reply that is plain text.
- No L8 tool takes a cell ID. ARIAC publishes no cell positions (L3), so the
  record keeps track of cells, not the model.


One Accepted Call and Five Refusals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``lecture11/code/llm_output_checker.py`` checks six separate replies, each
in the same state, and runs none of them. The state comes from L8's
``FakeTools`` (no ARIAC): eight calls that all pass the checks, with cell
voltages and a tester 1 malfunction chosen for this example.

.. literalinclude:: outputs/llm_output_checker.txt
   :language: text
   :lines: 1-14


Reading the Six Results
~~~~~~~~~~~~~~~~~~~~~~~

1. **B:** ``robot1_place_in_slot`` is not a tool: robot 2 places cells in
   slots. Check 1 stops it before any schema is read.
2. **C and D:** real tools with wrong arguments. C asks for slot 5, and the
   schema allows 1 to 4. D adds a cell ID; the schema allows no other
   arguments, so an invented cell never reaches a robot. Gemini's own
   parameter schema has no ``additionalProperties``, so ``check_call()``
   enforces it (L8).
3. **E and F:** well formed, and wrong for the factory now. Slot 1 already
   holds a cell, and tester 1 is ``MALFUNCTIONING``. No schema can stop
   these, because a slot's contents and a tester's status change during a
   run. Only the guard, which reads the state, catches them.
4. **A** passes all three checks. Only then does the orchestrator send it to
   the skills.


Re-Prompt Once, Then Fall Back
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The policy** (L8's ``run()``):

1. A refused call goes back to the model as that call's result, with the
   exact error. Asking again this way is a **re-prompt**.
2. Two refused calls in a row end the run (``MAX_INVALID = 2``, chosen in
   L8). Then fall back to a safe action: hold the cell, pause the feed, or
   hand the step to the GP3 PDDL plan.

The output shows **two separate runs of L8's** ``run()`` **in the same
state**:

.. literalinclude:: outputs/llm_output_checker.txt
   :language: text
   :lines: 16-29


.. _l11-vlm:

Cross-Checking the VLM
----------------------

A VLM error is well formed, so a schema check passes it. Compare the VLM
with a **second source**: another way to learn the same fact.


Four Second Sources in ARIAC
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 75
   :class: compact-table

   * - **Second source**
     - **How to compare**
   * - The VLM again
     - Send the same image twice, or two images a moment apart. If the
       answers differ, that item is not reliable.
   * - A structured topic
     - ``/agvN/tray_status`` says which of the four slots are occupied. If
       the VLM says slot 3 is empty and the topic says occupied, flag it.
   * - Your GP2 lidar detector
     - It checks each cell for dents, scratches and bulges. Flag a VLM defect
       that the point cloud does not support, and the reverse.
   * - The factory's own check
     - ``/agvN/check_kit_quality`` says whether the kit on an AGV tray is
       good. The ARIAC scenario page says to call it before you move the
       AGV.


What to Do on Disagreement, and When to Pay for a Cross-Check
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**On disagreement**, take the cautious action whose cost you know.

- A wrong kit sent to shipping is rejected, and the AGV must go to the
  recycling station. The cells and the time are lost (ARIAC scenario page).
- Pausing to look again costs one more VLM call.

**The cost of cross-checks.**

- L9 measured one VLM call with one camera image: 1377 input and 147 output
  tokens, 2.02 s, $0.000781 (gemini-3.5-flash-lite, L9's VLM check, recorded
  once).
- Cross-check the decisions that are expensive to get wrong, such as
  shipping a kit or discarding a cell, not every frame.


.. _l11-equipment:

Equipment That Stops Giving Valid Readings
------------------------------------------

This section works through the voltage tester case: what the ARIAC docs say,
what the ARIAC code does, and a watcher that handles both.


The Docs and the Code Disagree
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The ARIAC challenges page:**

   "When the voltage tester malfunction occurs, one or both voltage testers
   will stop publishing data."

**The ARIAC code** (commit 0c3e722, ``voltage_tester_plugin.cpp``):

- A timer publishes on ``/voltage_tester_N/voltage`` every 0.1 s of wall
  clock (``create_wall_timer``), malfunction or not (line 88). At 0.37 times
  real time, that is about :math:`10 / 0.37 = 27` messages per second of
  simulation time, so set a time limit on the right clock.
- During a malfunction, each message has voltage ``-1`` and
  ``operation_status`` ``MALFUNCTIONING`` (lines 126 and 127).

.. warning::

   **A check that waits for the messages to stop never fires on the current
   code.** Handle both behaviors.


Four Rules for a Robust Watcher
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: watcher
   :class: note

   A **watcher** is code that reads a device's messages and decides, at any
   moment, whether the device is up (giving valid readings) or down.

1. **Status:** check ``operation_status`` on every reading.
   ``MALFUNCTIONING`` means the tester is down.
2. **Value:** keep impossible values out of the average. No cell reads a
   negative voltage.
3. **Time limit:** if no reading arrives within the limit, treat the tester
   as down. Check this from a timer, because silence never calls the message
   callback.
4. **Cached state:** keep the last good reading with its time, and stop
   trusting it once the limit passes.

.. important::

   **The value rule needs care.** With no cell on it, the tester publishes
   noise around 0 V with status ``OPERATIONAL``
   (``voltage_tester_plugin.cpp``, line 144), so about half of those
   readings are negative. A low reading means an empty tester, not a broken
   one. **Check the status first**, then the value.


The Watcher in Code
~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/tester_watcher.py
   :language: python
   :lines: 38-58
   :caption: lecture11/code/tester_watcher.py (excerpt)

``on_reading()`` checks the status before the value: a ``MALFUNCTIONING``
reading marks the tester down whatever its voltage. A reading below
``NO_CELL_BELOW`` with status ``OPERATIONAL`` only empties the window (no
cell). ``on_timer()`` covers silence.


The Watcher Catches Both Behaviors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The readings are synthetic; there is no simulator.

- 10 readings per second; a Li-Ion cell at 3.60 V (chosen for this example)
  with noise of standard deviation 0.05 V (the tester's ``model.sdf``).
- Tester 1 fails from 180 s to 225 s: ``START_TIME`` 180 and ``DURATION`` 45
  in the ARIAC docs' example trial file.
- Watcher limits, chosen for this example: down when the last reading is
  more than 0.5 s old; below 0.5 V means no cell; the average uses the last 5
  valid readings. In Run 2 the last reading came at 179.9 s, so the watcher
  went DOWN at 180.5 s, on the sixth missed reading.

Run 1 sends what the ARIAC code sends. Run 2 sends nothing during the
malfunction, which is what the ARIAC docs describe.

.. literalinclude:: outputs/tester_watcher.txt
   :language: text
   :lines: 1-13


Worked Example: Averaging In the -1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Setup.**

- The testers are noisy, so you average a short window of readings (ARIAC
  scenario page, Step 1c).
- A Li-Ion cell is good if it reads within 3.6 V plus or minus 0.2 V, so
  3.4 V to 3.8 V (``CellTypes.msg``).
- The window holds 3.62, 3.58 and 3.61 V (chosen for this example), then -1
  when the malfunction starts (what the ARIAC code publishes).

**Steps.**

1. Sum with the -1 kept: :math:`3.62 + 3.58 + 3.61 - 1 = 9.81` V.
2. Average: :math:`9.81 / 4 = 2.45` V.
3. 2.45 V is 0.95 V below the 3.4 V lower limit, so the code sends a good
   cell to recycling.
4. With the -1 rejected: :math:`10.81 / 3 = 3.60` V, inside the limits.

**The program agrees:**

.. literalinclude:: outputs/tester_watcher.txt
   :language: text
   :lines: 15-17


Degraded Operation: A Malfunction and the Recovery Over Time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: degraded operation
   :class: note

   **Degraded operation** means the system keeps working, more slowly or
   with fewer devices, while one device is down.

.. figure:: /_static/images/l11/tester_timeline.svg
   :alt: A timeline from 165 s to 240 s, the time since the competition started. Top: a plot of tester 1's reading in volts, from -1 to 4. The reading stays near 3.6 V, drops to -1 at 180 s, stays at -1 until 225 s, then returns to about 3.6 V. Dashed vertical lines mark 180 s, tag 1, and 225 s, tag 2. Below, three rows of bars. Status: OPERATIONAL, then MALFUNCTIONING in amber from 180 s to 225 s, then OPERATIONAL. Watcher: UP, then DOWN in amber, then UP. Plan uses: both testers, then tester 2 only (new plan) in red, then both testers in red.
   :width: 95%
   :align: center

   A timeline, not a picture of the factory. Synthetic readings as in Run 1
   of the watcher. 1: at 180 s, tester 1 starts sending -1 with
   ``MALFUNCTIONING``; the watcher goes DOWN on that reading, and a new plan
   uses tester 2 only (global recovery). 2: at 225 s, the status is
   ``OPERATIONAL`` again; the watcher goes UP, and a new plan uses both
   testers. Red: the planner or agent.


.. _l11-challenges:

The ARIAC Challenges as Failure Scenarios
-----------------------------------------

For each challenge, this section gives what happens, the signal, the
recovery (retry, wait or replan), and whether it is local (the plan stays) or
global (the plan changes), as defined in :ref:`l11-taxonomy`. GP4 tests the conveyor malfunction, the voltage
tester malfunction and high-priority orders; the final demo adds the vacuum
tool malfunction.


Conveyor Malfunction: The Docs and the Code Disagree
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- The inspection conveyor stops for ``DURATION`` seconds (trial file).
- The ARIAC challenges page says the cell feed pauses too, so no new cells
  arrive.
- In the ARIAC code (commit 0c3e722), only the conveyor reacts:
  ``linear_conveyor_plugin.cpp`` sets the speed to 0 and the status to
  ``MALFUNCTIONING``. ``cell_feed_plugin.cpp`` spawns a cell every
  1 / feed rate seconds and never checks for a malfunction.

.. warning::

   **Not checked in simulation yet:** whether new cells still spawn on the
   stopped belt. Do not assume that no cells arrive during the stop.


Conveyor and Voltage Tester Malfunctions: Signal and Recovery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 14 46 40
   :class: compact-table

   * -
     - **Conveyor malfunction**
     - **Voltage tester malfunction**
   * - Signal
     - ``/inspection_conveyor/status``: status ``MALFUNCTIONING``, speed 0
     - Status ``MALFUNCTIONING`` with voltage -1, or no reading within the
       time limit
   * - Recovery
     - Wait (L9): pause the work that needs the belt, watch the status, and
       resume when it reports ``OPERATIONAL``
     - Replan (L9): send cells to the working tester; replan for both
       testers when the status returns to ``OPERATIONAL``
   * - Local or global
     - Local: the plan stays and waits, because no other conveyor can do the
       job
     - Global: the plan assumed two testers, and tester 2 can do the job


Vacuum Tool Malfunction (Task 2, Final Demo)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**What happens.**

- One grasp of VG_2 or VG_4 fails. In the docs' example, a grasp occurrence
  of 3 means the first two grasps work and the third fails.
- Signal: the grasp service (``/vacuum_tool/vg_2/grasp`` or ``vg_4``)
  returns ``success`` false with "Vacuum gripper is malfunctioning", and the
  skill returns a grasp failure.

**What the code adds** (``vacuum_tool_plugin.cpp``):

- The malfunction clears only after every suction pad has lost contact with
  the shell.
- So a retry in place fails again. Move the gripper away from the shell
  first, then approach and grasp again, as the challenges page says.

**Recovery: retry, which is local.** The tree retries a sequence that starts
by moving the gripper away.


High-Priority Order: The Goal Changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Signal.** An order with an ID arrives on ``/high_priority_orders``, and
ARIAC starts a timer.

**Recovery (replan, global: the goal changed).**

1. Switch the cell feed to NiMH (``/inspection_conveyor/cell_feed/control``).
2. Build a kit of four NiMH cells: :math:`4 \times 1.2 = 4.8` V, inside the
   window of 4.8 V plus or minus 0.15 V, so 4.65 V to 4.95 V
   (``CellTypes.msg``).
3. Move the AGV to shipping, and submit with ``/submit_high_priority_order``
   and the same ID.
4. Switch the feed back to Li-Ion.

.. warning::

   **World drift inside this challenge.** Li-Ion cells already on the
   conveyor still arrive after the switch, and a Li-Ion kit may be half built
   on another AGV.


Defective Cells, in Every Trial
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- A cell passes the inspection door only after your team submits a passing
  inspection report for it.
- A failing report, or no report, sends the cell to the inspection bin.
- A good cell in the inspection bin costs 50 points
  (``GOOD_CELL_IN_INSPECTION_BIN`` in ``scoring_weights.yaml``).

.. important::

   **A detector that flags too many cells has a cost you can count:** 50
   points for each good cell it rejects. L12 uses this to compare detectors.


.. _l11-local-global:

Local or Global Recovery
------------------------

The order of recovery comes from L3: the second idea the course took from
4D/RCS, the NIST reference model architecture described in NISTIR 6910. This
section then gives L9's rule (retry, wait or replan), where the LLM fits, and
three worked examples from ARIAC. Local and global recovery are defined in
:ref:`l11-taxonomy`.


Errors Are Handled Where They Are Seen; Status Moves Up
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l11/escalation_ladder.svg
   :alt: Three stacked boxes with arrows between them. Bottom, tag 1, gray: Skill, success, or a failure result. Middle, tag 2, blue: Behavior tree, retry, wait, timeout, other branch. Top, tag 3, red: Planner or LLM agent, new plan or new goal. Arrows on the left point up, labeled status and failure result move up. Arrows on the right point down, labeled commands move down. On the far right, a blue bracket labeled local spans the skill and the tree, and a red bracket labeled global spans the planner or agent.
   :width: 85%
   :align: center

   1: skill. 2: behavior tree. 3: planner or LLM agent. Gray, blue and red
   mark the same three layers on every figure in this lecture.

**The skill never retries a task itself.** It returns success or a failure
result. The behavior tree decides first (retry, wait, timeout, another
branch).
Only when the tree cannot fix the failure does it move up to the planner or
agent.


The Rule for Choosing
~~~~~~~~~~~~~~~~~~~~~

**From 4D/RCS** (NISTIR 6910, quoted in L3):

- Commands flow down the hierarchy, and status feedback flows up (p. 19,
  Figure 1).
- An executor that "senses an error between its output CommandGoal and the
  predicted state ... may react by modifying the commanded action so as to
  cope with that error" (p. 45).

**The rule (L9's three cases):**

1. **Retry** (local) when the failure looks temporary and every assumption of
   the plan still holds.
2. **Wait** (local) when a device the plan needs is down and will come back,
   and no other device can do its job: keep the plan and watch the device's
   status.
3. **Replan** (global) when an assumption of the plan is false and another
   way exists, such as a second device, or when the goal changed.

4D/RCS gives the reason for the order: a layer copes with the error it sees,
and status moves up only when it cannot.


Where the LLM Fits: Two Designs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The L8 and L9 agent: the model at every step.** The agent calls the model
for every step, recovery included. In L9's replan recording, one kit took 26
model calls and 122,861 input tokens.

**A hybrid, which GP4 allows** (:doc:`GP4 page </assignments/gp4>`, L9):

- Rule-based handlers cover the common cases: the retry, wait and replan
  answers in this lecture's tables.
- Call the LLM only when no handler covers the case. The common cases then
  cost no tokens. Your team defends the choice in its GP4 reflection.

**Both are agentic.** L1's definition: the agent "picks the next step from
what it observes, not from a fixed script". In both designs, what runs next
depends on what was observed.


Example A: The Vacuum Grasp Fails on the Third Grasp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Check the assumptions:**

1. The top shell is still where it was.
2. The tool is still attached.

**Decision.** Both assumptions hold, and the failure clears once the pads
lose contact, so it is temporary. So: **local**. The tree's Retry runs the
grasp sequence again, starting with a move away from the shell. No LLM call.


Example B: Tester 1 Goes Down for 70 s During a Kit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Setup: L9's trial and its two recordings.**

- Tester 1 malfunctions at ``START_TIME`` 30 s for ``DURATION`` 70 s (L9's
  ``config/l9_trial.yaml``). Gemini fills agv1's four slots, once with a
  replan policy and once with a wait policy (tester 1 only).
- Recorded once, on 2026-10-17, with gemini-3.5-flash-lite. A rerun gives
  different answers. Recording 1 of 1 each (``lecture9/outputs/``).

**Steps.**

1. The plan assumes two testers, and one is down. Tester 2 can do its job,
   so by the rule: replan.
2. Replan recording: Gemini sent cells 2 and 3 to tester 2. Slot 3 was filled
   at 108.8 s; the scripted dry run, with no malfunction, filled it at
   105.1 s.
3. Wait recording: Gemini waited 5, 10, 20 and 30 s while robot 2 held a
   tested cell that could already go to slot 1: :math:`112.6 - 38.2 = 74.4`
   s. The goal text did not say so (L9).
4. Both finished at about 225 s, because by chance two cells in the replan
   run read under 3.4 V and went to recycling (80.0 s). One recording each
   cannot say which policy is faster.

**Decision.** So: **global**. Replan to use tester 2 only, and replan again
when tester 1 returns.


Example C: A High-Priority Order Arrives with Two Cells on AGV 1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Setup.** AGV 1's tray holds two cells of a Li-Ion kit (chosen for this
example).

**Decision.**

- The goal changed, so the response is **global**.
- This is where the LLM agent is useful. It chooses which AGV takes the NiMH
  kit, whether to finish the Li-Ion kit first, and when to switch the feed
  back.
- Each of its tool calls still passes ``check_call()`` (tool, schema,
  guard) before any robot moves.


Class Discussion: Which Examples GP3 Handles with No Change
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This continues L9's discussion (would your GP3 domain handle each challenge
with no change?), now with the three worked examples. Your GP3 system is a
PDDL planner with a behavior tree executor. Take
Examples A, B and C in turn. For each one, say whether GP3 handles it as
written, and if not, what is missing: in the tree, or in the PDDL domain.
(RO01: answer in the session chat.)

.. dropdown:: What GP3 handles and what it does not
   :class-container: sd-border-success

   1. **Example A:** the tree handles it, not the planner, and only if the
      tree has a retry around the grasp.
   2. **Example B:** needs a predicate for tester status that the GP3 domain
      was not asked to model.
   3. **Example C:** needs actions and goals for a new order that the GP3
      domain was not asked to model.

   This is why GP4 adds an agent: B and C are the cases a fixed domain did
   not plan for.


Next Class
----------

**GP4 (due Friday, April 23, at 11:59 pm).**

- Add the checks and the challenge handling from today: retry, wait or
  replan for each failure. Log every detection and recovery.
- Log each one with its time, and for a refused LLM call, the check that
  refused it and the error message.
- The GP4 reflection and the final demo presentation both ask how failures
  were caught. The log is your evidence.

**Before L12:**

- Read the final demo specification as a team, and list your questions for
  L13.
- Start your **challenge test matrix**, a table of test runs: each
  challenge, alone and combined, on several trial configurations. Run each
  cell of the matrix more than once.
- Take the :doc:`L11 self-check quiz <l11_quiz>` (ungraded). The
  demonstration code is on ELMS-Canvas and on the :doc:`code page
  <l11_code>`.

**L12: Evaluation and Measurement Science for Agentic Systems.** How to
measure an agentic system with the ARIAC scoring formula, recovery included:
recovery rate, challenge handling, and how the ARIAC score rewards or
penalizes each choice.
