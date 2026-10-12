====================================================
Lecture
====================================================

.. note::

   These notes follow the L9 slides shown in class, in the same order and with
   the same sections, so you can read them at home. Every program output below
   is copied from the files the two L9 scripts wrote when they ran with
   Python 3.12.3 and jsonschema 4.10.3. The scripts and how to run them are on
   the :doc:`code page <l9_code>`.

.. important::

   **Both demonstrations use stand-ins, not real models.** ``stand_in_vlm()``
   and ``stand_in_model()`` return canned replies in a fixed order, written to
   contain the mistakes the checks must catch. A real model's answers vary
   from run to run. The factory in the closed-loop demonstration is a
   stand-in too: plain Python that copies the payloads of the ARIAC 2025
   topics, with no simulator.


.. _l9-recap:

Recap
-----

From L8
~~~~~~~

The **orchestrator** is the program that runs the loop around the LLM. It
observes, asks the model, checks the model's output against a JSON schema,
calls a tool, and reads the result.

The L8 agent had two gaps:

- It observed ROS 2 topics only. No topic says what a cell looks like or
  which cell type sits in which tray slot.
- It ran its plan without checking the world after each step, so it did not
  notice when the factory changed under it.


Today Adds Two Things
~~~~~~~~~~~~~~~~~~~~~

1. **Grounding:** a vision-language model (VLM) describes what a camera sees,
   so the agent's decisions rest on the factory as it is.
2. **Replanning:** after each action the orchestrator observes again,
   compares, and asks for a new plan only when it must.


Today's Milestones
~~~~~~~~~~~~~~~~~~

Quiz 4 (L7 and L8) opened the class. GP3 (PDDL planner and behavior tree
executor) is due. GP4 (LLM agent with VLM grounding) is posted and builds on
today.


.. _l9-vlms:

VLMs for a Robot Cell
---------------------

This section covers what a VLM takes and returns, which ones exist, and where
its images come from in ARIAC 2025.


What a VLM Is, and Three Families
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: vision-language model (VLM)
   :class: note

   A **VLM** takes images and text in the same prompt and returns text. It
   returns positions only if you ask for coordinates in the text, and it can
   be wrong with full confidence.

Compared with the L8 text call, one input is new: the image. The prompt and
the checked, structured output work the same way as in L8.

.. list-table::
   :header-rows: 1
   :widths: 20 50 30
   :class: compact-table

   * - **Family**
     - **Examples**
     - **Cost**
   * - Hosted APIs
     - Claude, GPT and Gemini accept images in a request.
     - An API key; billed per token, and an image counts as input tokens.
   * - Local open-weight
     - Qwen-VL and LLaVA, run with Ollama (``ollama pull qwen2.5vl``, see the
       :doc:`AI Access </ariac/ai_setup>` page).
     - No fee per call; needs a GPU with enough memory.
   * - Embodied reasoning
     - Google's Gemini Robotics ER: it points at a part or draws a box around
       it. The Gemini API listed ``gemini-robotics-er-2-preview`` (a preview)
       on 2026-10-12.
     - Hosted. The final demo uses one model of this kind.

An **embodied-reasoning model** is a VLM built to answer spatial questions
about an image, such as where a part is.


Where the Images Come From in ARIAC 2025
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Cameras are yours to place.**

- Your team configuration file places RGB cameras. Each one publishes
  ``/{camera_name}/image`` (``sensor_msgs/Image``) and
  ``/{camera_name}/info`` (``sensor_msgs/CameraInfo``).
- A 1080p camera costs $800 and a 720p camera $500 (ARIAC sensors page), out
  of a $9600 budget (``SENSOR_BUDGET`` in
  ``ariac_db/config/scoring_weights.yaml``). Each camera you add for the VLM
  lowers the sensor cost bonus, which L12 works out.

**What each sensor is for.**

- Lidar finds defects (GP2). It may only sit in three boxes around the
  inspection conveyor.
- Cameras feed the VLM: one over an AGV tray at the inspection station, one
  over the conveyor, or, for the final demo, one over the assembly table,
  where the top shell appears at a random pose.


A VLM in the Stack: Camera to Checked Record to Agent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l9/vlm_stack.svg
   :alt: Block diagram of a VLM in the robot stack. Top row, left to right: Camera, Encode and ask, VLM (blue, a model). Arrow 1 goes from the camera to Encode and ask; arrow 2 from Encode and ask to the VLM; arrow 3 goes down from the VLM to Check. Bottom row, right to left: ROS topics, Check, Record, LLM agent (blue, a model). Arrow 6 goes from ROS topics to Check, arrow 4 from Check to Record, arrow 5 from Record to the LLM agent. A red dashed arrow, 7, goes from Check back up to Encode and ask.
   :width: 95%
   :align: center

   A VLM in the stack. Blue boxes are model calls; gray boxes are your code
   and ROS. The red dashed arrow is taken after a mismatch.

The numbered arrows carry:

1. The image message from the camera topic.
2. The image, the prompt and the JSON schema.
3. The VLM's reply: text that should be JSON.
4. A record that passed every check.
5. The record, inside the agent's observation.
6. A second source: the tray status and the tester readings.
7. A failed check: re-prompt once with the error.

The VLM never writes to the agent directly. Its reply goes through **Check**
first, and only a record that passed reaches the agent.


From an Image Topic to a Request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Subscribe to ``/{camera_name}/image`` and keep the latest frame.
2. Convert the ROS image to an OpenCV image with ``cv_bridge``
   (``CvBridge.imgmsg_to_cv2``), then encode it as a PNG or JPEG file in
   memory.
3. Encode the file the way the provider's API expects. Each provider's vision
   page shows the request format.
4. Send the image with the text prompt and the schema, and log the time and
   the token count of the call.

.. tip::

   Only step 4 depends on the provider. Steps 1 to 3 are the same for every
   VLM, so write them once and test them without a model.


.. _l9-prompts:

Scene Description Prompts
-------------------------

This section goes from "describe the image" to a JSON record that your code
can check.


The Weak Prompt, and Steps 1 and 2 of a Strong One
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The weak prompt: "Describe this image."** The answer is a paragraph. The
agent needs another model to read it, and the paragraph may leave out the one
fact the agent needs.

**Building the strong prompt, on an AGV tray:**

1. **Say what the camera shows:** "This image is from a camera above the tray
   of agv1. The tray has four slots, numbered 1 to 4 from the left of the
   image." The model cannot know the slot numbers unless you tell it. The
   order in the image depends on how the camera is mounted, so check it once
   against ``/agvN/tray_status``.
2. **Ask for one record per slot:** occupied or empty, cell type, visible
   damage, and a confidence.


Steps 3 and 4: A Schema with Enums, and a Way to Say UNKNOWN
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

3. **Give a JSON schema with enums.** An enum lists the only values a field
   may take.
4. **Allow** ``UNKNOWN``, and tell the model to use it when it cannot see a
   value.

.. literalinclude:: code/vlm_check.py
   :language: python
   :lines: 28-42
   :caption: lecture9/code/vlm_check.py (excerpt)

- ``LI_ION`` and ``NIMH`` (from ``CellTypes.msg``) and ``DENT``, ``BULGE``
  and ``SCRATCH`` (from ``CellDefect.msg``) are the factory's own names, so
  the agent's world state uses the same names as ARIAC.
- ``NONE`` and ``UNKNOWN`` are added for this schema: ``CellDefect.msg`` has
  no value for "no defect". A model that must pick a label will guess, so
  allow ``UNKNOWN``.


Ask for Relations, and Validate as in L8
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Relations, not only labels.** "Which slot is empty?" and "Is the cell in
slot 3 the same type as the others?" are questions the agent acts on. A list
of labels with no slot numbers is not.

**Validation, the same steps as L8:**

1. Parse the reply as JSON.
2. Check it against the schema.
3. On a failure, re-prompt once with the validation error.
4. On a second failure, stop and report.

.. tip::

   The orchestrator writes the result into the world state, not the VLM.


.. _l9-high-priority:

The Running Example: a High-Priority Order
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

What ARIAC asks (challenges page):

1. An order arrives on ``/high_priority_orders`` with an ID.
2. Switch the cell feed to NiMH, build a kit of four NiMH cells, and move the
   AGV to shipping.
3. Submit with ``/submit_high_priority_order`` and the same ID, then switch
   the feed back to Li-Ion.

**The NiMH kit window.** ``CellTypes.msg`` gives a NiMH cell a nominal
voltage of 1.2 V and a kit a tolerance of 0.15 V. The **kit window** is the
range the kit's total voltage must fall in:

1. Four cells: :math:`4 \times 1.2 = 4.8` V.
2. The kit must be from :math:`4.8 - 0.15 = 4.65` V to
   :math:`4.8 + 0.15 = 4.95` V.

.. tip::

   Before submitting, the agent asks the VLM whether all four cells on the
   tray are NiMH. Li-Ion cells already on the conveyor when the feed switched
   can still arrive.


.. _l9-checking:

Checking the VLM's Record
-------------------------

This section gives each field of the record a second source, and shows a
demonstration with a scripted stand-in VLM.


Which Second Source Checks Which Field
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 15 30 55
   :class: compact-table

   * - **Field**
     - **Second source**
     - **Why it is stronger**
   * - Occupied
     - ``/agvN/tray_status``
     - ARIAC's own signal: four booleans, no cell type
       (``AgvTrayStatus.msg``).
   * - Cell type
     - The voltage your team recorded for the cell on a tester
     - Nominal 3.6 V against 1.2 V: 2.4 V apart, 24 times the 0.1 V spread of
       cell voltages (``cell_feed_plugin.hpp``).
   * - Damage
     - None in ARIAC; GP2's lidar decides the inspection report
     - Defects are 0.84 to 2.49 mm deep (L5), and nobody has checked that a
       camera image shows them.

The "24 times" in the table is :math:`(3.6 - 1.2) / 0.1 = 2.4 / 0.1 = 24`.
The two types are so far apart that one tester reading settles the type.

.. important::

   **A disagreement is a flag, not a verdict.** At least one source is wrong.
   The agent does not act on the field until a third observation settles it.


Demonstration Setup, and the Weak Prompt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::

   ``stand_in_vlm()`` is a scripted stand-in for the model: it returns canned
   replies, written to hold mistakes for the checker to find. A real model's
   answers vary.

The tray status and the recorded voltages are stand-in values chosen for this
example. To run it, see :doc:`l9_code`.

Output for the weak prompt:

.. literalinclude:: outputs/vlm_check.txt
   :language: text
   :lines: 1-5

``json.loads`` rejects the paragraph. Its hint, "one near the right", names no
slot.


Parse, Validate, Re-prompt Once
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/vlm_check.py
   :language: python
   :lines: 76-84
   :caption: lecture9/code/vlm_check.py (excerpt)

Output for the structured prompt:

.. literalinclude:: outputs/vlm_check.txt
   :language: text
   :lines: 6-10

The first reply numbered the slots 0 to 3. The schema's ``minimum`` of 1
caught it, and the second reply passed.


The Cross-Check, Slot by Slot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/vlm_check.py
   :language: python
   :lines: 108-124
   :caption: lecture9/code/vlm_check.py (excerpt)

``type_from_volts()`` turns a recorded voltage into a type: 1.0 V to 1.4 V is
``NIMH``, 3.4 V to 3.8 V is ``LI_ION``. Each range is the nominal voltage
plus or minus the 0.2 V cell tolerance in ``CellTypes.msg``: for NiMH,
:math:`1.2 - 0.2 = 1.0` V and :math:`1.2 + 0.2 = 1.4` V.

The checks run in order. Occupancy is compared first. Only if it agrees does
the code compare the type, and a VLM answer of ``UNKNOWN`` never counts as a
type disagreement.


Output: Two Disagreements Before the Submit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/vlm_check.txt
   :language: text
   :lines: 11-17

1. **Slot 3:** the VLM says ``LI_ION``, but the cell read 1.24 V, inside the
   NiMH range of :math:`1.2 \pm 0.2` V (1.0 V to 1.4 V).
2. **Slot 4:** the VLM says empty, but ``/agv1/tray_status`` says occupied.
   The topic is ARIAC's own signal, so the VLM is wrong here, and its other
   answers from the same image are now in doubt.
3. The agent does **not submit**. It takes a new image and asks again, and
   the slot 3 question stays open until a third check settles it.


What the Demonstration Shows, and What a Live Call Adds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Read from the output:**

- The confidences of the two wrong slots were 0.6 and 0.7. A confidence is
  the model's own number, not a check.
- For occupancy, the topic gives the answer for free. The VLM is worth its
  cost for what no topic reports: the tray as it looks now, which shows
  whether a cell went where your record says.

**A live call:**

- With an API key and an ARIAC camera, the same script calls a real VLM.
  Print the time and the token count of each call next to its output: these
  are the latency and cost columns of the GP4 comparison.
- The stand-in has no time or token count, so these notes show none.


.. _l9-closed-loop:

The Agentic Closed Loop
-----------------------

The loop: act, observe again, compare the observed state with the expected
state, and decide.


The Loop, One Box per Step
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l9/closed_loop.svg
   :alt: A loop of boxes. Top row, left to right: Observe, Reason (LLM, blue), Act. An arrow goes down from Act to Observe again, at the bottom right. Bottom row, right to left: Observe again, Compare, and Expected effect, which also feeds Compare from the left. An arrow goes up from Compare to Decide, in the middle. Decide has two exits: tag 1, a gray arrow right and up to Act; tag 2, a red arrow up to Reason (LLM).
   :width: 95%
   :align: center

   The agentic closed loop. Blue: the model call. Decide has two exits,
   tagged 1 and 2.

1. The world matches, so the next step runs; or the decision is to retry the
   step or to wait.
2. The decision is to **replan**, so the LLM is asked for a new plan. This is
   the only exit that calls a model.


What the Agent Observes, and Where the Expected State Lives
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Observe:** ``/inspection_conveyor/status``, ``/voltage_tester_1/voltage``,
``/voltage_tester_2/voltage``, ``/agvN/tray_status``,
``/high_priority_orders``, ``/competition_status``, and the VLM record.

**Keep the expected state outside the LLM.**

- The orchestrator keeps the world-state record from L3: cells, testers, tray
  slots, AGV stations, orders.
- Each action has an **expected effect**, the same idea as a PDDL effect:
  after ``load_tester``, the tester reads 3.4 V to 3.8 V.
- After the action, the orchestrator checks that effect against fresh
  observations. The model never grades its own plan.


Drift: the World Is Not What the Plan Assumed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Drift** means the factory no longer matches what the plan assumed. Four
ARIAC examples:

1. A place skill reports success, but ``/agvN/tray_status`` shows the target
   slot still empty.
2. ``/inspection_conveyor/status`` reports ``operating_status``
   ``MALFUNCTIONING``: the belt has stopped.
3. A voltage tester's topic carries voltage ``-1`` and ``operation_status``
   ``MALFUNCTIONING`` in the middle of a kit.
4. A high-priority order arrives: the goal itself changed.

.. warning::

   The ARIAC challenges page says the cell feed also pauses during a conveyor
   malfunction. In the 2025 source, ``linear_conveyor_plugin.cpp`` stops only
   the belt, and ``cell_feed_plugin.cpp`` has no malfunction check. Watch the
   feed in simulation before you rely on either.


Bound the Loop
~~~~~~~~~~~~~~

- A step limit per decision and a retry cap, as in L8.
- One re-prompt after an invalid reply, then stop and report.

**Why the bounds matter in ARIAC:**

- A loop that replans forever spends tokens and trial time.
- The trial time bonus and the high-priority speed bonus both shrink while it
  runs. ARIAC's target for a high-priority order is 150 s
  (``NOMINAL_HIGH_PRIORITY_EXECUTION_DURATION`` in ``scoring_weights.yaml``;
  the scoring page says the targets can change). L12 works the formulas.


.. _l9-retry-wait-replan:

Retry, Wait or Replan
---------------------

This section covers what the orchestrator does after a mismatch, applied to
the four ARIAC 2025 challenges.


The Rule
~~~~~~~~

**Two cases:**

- **Retry one action** when the failure looks temporary and every assumption
  of the plan still holds.
- **Ask for a new plan** when an assumption of the plan is now false, or when
  the goal changed.

**A third case: a device is down.** The plan assumes the device works, but
the device will come back.

- If another device can do the job, replan around it: ARIAC has two voltage
  testers.
- If no other device can, keep the plan and **wait** while you watch its
  status topic: ARIAC has one inspection conveyor.


The Rule as a Decision Chart
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l9/retry_replan.svg
   :alt: Decision chart. A red Mismatch box leads right to the question Goal changed? Yes goes up to Replan (blue, tag 1). No goes right to Device down? Yes goes down to Another free?, whose yes goes left to Replan (blue, tag 2) and whose no goes down to Wait, watch (gray, tag 3). Device down? no goes right to Plan holds? Its no goes up to Replan (blue). Its yes goes down to Retries left?, whose yes goes down to Retry action (gray, tag 4) and whose no goes left to Replan (blue).
   :width: 100%
   :align: center

   The retry, wait or replan chart. Blue boxes call the LLM; gray boxes do
   not.

The tags mark the example for each exit:

1. A high-priority order arrives.
2. Tester 1 is down; tester 2 is free.
3. The conveyor is down.
4. A grasp failed; the cell is still in reach.

"Plan holds?" asks whether the world is still as the plan assumes, for
example that the cell is still on the tester. The questions are asked in
order from the left, so a changed goal is checked before anything else.


The Four ARIAC 2025 Challenges
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 18 44 38
   :class: compact-table

   * - **Challenge**
     - **What the agent observes**
     - **Response**
   * - Conveyor malfunction
     - ``operating_status`` ``MALFUNCTIONING`` on
       ``/inspection_conveyor/status``
     - Wait (tag 3): pause, watch the status topic, resume. No new plan.
   * - Voltage tester malfunction
     - Voltage ``-1`` and ``operation_status`` ``MALFUNCTIONING`` on the
       tester's topic
     - Replan (tag 2): use the working tester until the broken one recovers.
   * - High-priority order
     - ``/high_priority_orders`` publishes an order
     - Replan (tag 1): the goal changed.
   * - Vacuum tool malfunction
     - The grasp service of VG_2 or VG_4 reports a failure
     - Retry (tag 4): move away and grasp again. Task 2 only, so the final
       demo tests it, not GP4.


.. _l9-broken-tester:

Detect a Broken Tester From Its Status, Not From Silence
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::

   The ARIAC challenges page says a malfunctioning tester stops publishing. In
   the 2025 source (``voltage_tester_plugin.cpp``), the topic keeps publishing
   every 0.1 s, with voltage ``-1`` and ``operation_status`` 2
   (``MALFUNCTIONING`` in ``OperationStates.msg``). A check that waits for the
   topic to go quiet never fires.

The demonstration's stand-in topic follows the source:

.. literalinclude:: code/closed_loop.py
   :language: python
   :lines: 95-102
   :caption: lecture9/code/closed_loop.py (excerpt)

With no cell on it, a working tester reads 0 V plus noise (same source file),
so a reading near 0 V means the tester is empty.


The Same Two Levels as L7
~~~~~~~~~~~~~~~~~~~~~~~~~

- In GP3, the behavior tree used retry and timeout decorators for one-off
  failures, and asked the planner for a new plan when a cell failed
  inspection.
- The agent keeps the same two levels. Only the source of the new plan
  changes: the LLM instead of the PDDL planner.

**The skills package never retries by itself.**

- A skill returns a result that says what went wrong and what the robot
  holds.
- Recovery is your team's code, so the ARIAC challenges show up in your logs
  instead of being hidden. L11 covers recovery in depth.


.. _l9-demo:

Demonstration: the Closed Loop
------------------------------

One Li-Ion kit on agv1 meets a conveyor malfunction and a tester malfunction,
in plain Python (``lecture9/code/closed_loop.py``).

The values below are **chosen for this example**:

- Malfunction times, with the keys of an ARIAC trial file: conveyor
  ``START_TIME`` 90 s, ``DURATION`` 30 s; tester 1 ``START_TIME`` 140 s,
  ``DURATION`` 45 s.
- Action times: ``load_tester`` takes 25 s, ``unload_to_tray`` 20 s,
  ``move_agv`` 15 s.
- Cells c1 to c4 read 3.58, 3.61, 3.55 and 3.63 V.
- The first unload of c4 loses its grasp.

.. warning::

   The factory and the model are stand-ins. The model is scripted: it returns
   canned JSON plans in order, and a real model's answers vary. Its calls take
   0 s here.

.. note::

   **The action names are stand-ins too.** ``load_tester`` (move a cell onto
   a voltage tester) and ``unload_to_tray`` (move a cell from a tester to a
   tray slot) are names made up for this demonstration. They are **not** the
   names of the course skills package's skills. ``move_agv`` stands in for
   ARIAC's own ``/{agv_name}/move`` action, which your team calls directly.
   In GP4, your agent's tools are the real skills and ARIAC interfaces.


The Decision Chart in Code
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/closed_loop.py
   :language: python
   :lines: 129-138
   :caption: lecture9/code/closed_loop.py (excerpt)

- ``before()`` checks each step's preconditions, and ``after()`` compares the
  step's expected effect with fresh observations. Both call ``decide()`` on a
  mismatch.
- ``RETRY_CAP`` is 2, chosen for this example. Every plan from the model goes
  through the schema and a check against the observed state before it runs.

The ``if`` statements follow the chart from left to right: goal changed,
device down (with or without another free device), then plan holds with
retries left.


Trace, Part 1: Two Cells, Then the Conveyor Stops
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/closed_loop.txt
   :language: text
   :lines: 1-14

At t = 90 s the precondition of ``load_tester`` fails: the conveyor that
brings the next cell is down. There is no other conveyor, so the chart says
**wait** (tag 3). The plan resumes at 120 s, when the 30 s malfunction ends
(:math:`90 + 30 = 120` s).


Trace, Part 2: Tester 1 Breaks, the Agent Replans
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/closed_loop.txt
   :language: text
   :lines: 15-20

1. The expected effect of ``load_tester(c3, 1)`` is a reading from 3.4 V to
   3.8 V. The topic says -1 V, ``MALFUNCTIONING``.
2. Tester 2 is free, so the chart says **replan** (tag 2).
3. Model call 2 still sends a cell to tester 1. The check against the observed
   state rejects it before any robot moves, and the re-prompt gets a valid
   plan.
4. Cell c3 stays on tester 1 until that tester can read it.


Trace, Part 3: a Lost Grasp, a Retry, and the Kit Check
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/closed_loop.txt
   :language: text
   :lines: 21-34

- At 190 s the slot is empty, but tester 2 still reads 3.63 V: the cell never
  left. The plan still holds, so the chart says **retry** (tag 4).
- By 210 s tester 1 has recovered (:math:`140 + 45 = 185` s), and c3 reads
  3.55 V. The kit total is checked in code before the AGV moves.


Replan or Wait: the Same Run With a Wait-Only Policy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``closed_loop.py --wait`` runs the same factory, but never replans around a
broken tester: it waits for it. Excerpt of its output (the full output is on
the :doc:`code page <l9_code>`):

.. literalinclude:: outputs/closed_loop_wait.txt
   :language: text
   :lines: 16-22,36

1. Replanning finished at 245 s; waiting finished at 285 s.
   :math:`285 - 245 = 40` s.
2. After the mismatch at 145 s, tester 1 stayed down until 185 s:
   :math:`185 - 145 = 40` s. The replan used that time on tester 2.
3. The replan made two model calls at 0 s each. If each real call takes
   :math:`L` seconds, replanning still wins while :math:`2L < 40` s, that is,
   while :math:`L < 20` s.


.. _l9-pddl:

When PDDL Is the Better Tool
----------------------------

This section gives a rule you can defend for choosing between the GP3 planner
and the GP4 agent.


Five Axes for Comparing a Planner and an Agent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l9/pddl_vs_agent.svg
   :alt: Five horizontal axes, each with a name on the left and words at both ends; the left end is marked better for the cell. Cost per decision: none to tokens or GPU time. Same input, same plan: always to not guaranteed. Why this plan: domain file to model weights. Latency per decision: planner run to network, generation. On these four axes marker 1 (PDDL planner, gray) is at the left end and marker 2 (LLM agent, blue) at the right end. Cases outside the domain: can try them to only modeled actions; here marker 2 is at the left end and marker 1 at the right end.
   :width: 80%
   :align: center

   Tag 1: the PDDL planner (gray: code). Tag 2: the LLM agent (blue: a
   model). A marker shows which end a system is on, not a measured distance.

The planner is at the better end of four axes; the agent is at the better end
of one, cases outside the domain.


The Normal Task 1 Flow: Feed, Inspect, Test, Place, Ship
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Cost:** the PDDL planner runs on your machine with no fee per call. Every
  LLM call costs tokens (hosted) or GPU time (local).
- **Determinism:** the same PDDL problem gives the same plan. The same prompt
  can give different plans on different runs.
- **Auditability:** a PDDL plan follows from a domain file anyone can read. An
  LLM plan follows from weights nobody can read.
- **Latency:** an LLM call adds network and generation time to every
  decision. GP4 measures both systems.

.. important::

   For a fully specified task such as the normal Task 1 flow, PDDL is the
   better tool.


Where the Agent Earns Its Place, and Hybrid Designs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Three kinds of situation:**

1. **Ambiguity:** the VLM says a cell "may be dented".
2. **Novelty:** a case the domain has no action for.
3. **Recovery the domain did not plan for:** the ARIAC challenges, which
   GP3's domain does not model.

**Hybrids are legitimate answers.**

- The LLM chooses the goal (which kit next, which tester) and PDDL plans the
  steps.
- Or PDDL runs the normal flow, and the LLM is called only when a replanning
  trigger fires.
- GP4 asks for an agent, but your team may defend a hybrid in its
  reflection.


Keep Numeric Work in Code
~~~~~~~~~~~~~~~~~~~~~~~~~

**The Li-Ion kit window** (``CellTypes.msg``: 3.6 V nominal, kit tolerance
0.15 V):

1. Four cells: :math:`4 \times 3.6 = 14.4` V.
2. The kit must be from :math:`14.4 - 0.15 = 14.25` V to
   :math:`14.4 + 0.15 = 14.55` V.
3. Choosing four cells that fit is arithmetic. LLMs make arithmetic slips,
   and ARIAC rejects the kit on any slip, so a function does it and the agent
   calls it as a tool. The demonstration checked 14.37 V in code
   (:math:`3.58 + 3.61 + 3.55 + 3.63 = 14.37` V).

**Class discussion (5 minutes).** For each of the four challenges, would your
GP3 domain have handled it with no change? Why or why not? The answers become
GP4's test cases.


.. _l9-gp4:

GP4: LLM Agent with VLM Grounding
---------------------------------

GP4 is posted today and is due in Week 13 (04/21). It is 10% of the course
grade.


Goal and Test Cases
~~~~~~~~~~~~~~~~~~~

**Goal:**

- Replace the PDDL planner with an LLM agent. It calls the robot skills as
  tools (through MCP if your team chooses) and returns output checked against
  a JSON schema.
- A VLM describes the cells for the agent. The GP3 executor runs the agent's
  decisions.

**Test cases, each shown on a trial:**

- A conveyor malfunction, a voltage tester malfunction, and high-priority
  orders. Set them in the trial configuration file (the ARIAC configuration
  page has an example).
- The vacuum tool malfunction affects only Task 2, so the final demo tests
  it, not GP4.


The Side-by-Side Comparison With GP3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80
   :class: compact-table

   * - **Measure**
     - **What you log**
   * - Validity
     - Did every action's preconditions hold when it ran, and was each kit
       accepted?
   * - Plan length
     - How many skill calls and service calls each system made for the same
       work.
   * - Cost
     - Tokens and dollars for the agent, or GPU time for a local model; the
       planner has no fee per call.
   * - Latency
     - Time from an observation to the decision, logged per decision.

- **Identical trials:** the same trial file (``SEED``, ``DEFECT_RATE``,
  ``CHALLENGES``) and the same team file (``SENSORS``, ``CONVEYOR_SPEED``,
  ``CELL_FEED_RATE``). Change only the planner.
- Log every decision with its inputs, outputs, time and token count from the
  first day. One run per system is not a comparison; L12 shows how many runs a
  claim needs.


Deliverables, Guard Rails and Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Deliverables:** the agent module, the VLM module, the executor changes, the
comparison with GP3, and a reflection on the agent's failure modes and how
they were caught.

**Guard rails to build from the start:**

1. A fixed list of allowed tools; reject any call to a tool not on it.
2. Schema validation with a bounded re-prompt, and a step limit per decision.
3. API keys in environment variables or a ``.env`` file listed in
   ``.gitignore``, never in the repository.

**Dependencies:** the course skills package moves the robots, so GP4 needs no
MoveIt 2 code. L10 opens the package.


.. _l9-next-class:

Next Class
----------

**L10: Frames, Transforms, and Motion Planning (Wednesday, April 7).** TF2 in
depth, the camera model (from a pixel to a pose), MoveIt 2, and the inside of
the course skills package.

**Quiz 5 (Wednesday, April 14, start of class)** covers L9 and L10.

**Before next class:**

- Submit GP3 and its peer-review form on ELMS-Canvas.
- Read the GP4 specification and agree on who owns the agent, the VLM module
  and the comparison.
- Set up LLM and VLM access (a hosted API key or a local model with Ollama)
  with the course :doc:`AI Access </ariac/ai_setup>` page.
- Run the L9 scripts (see :doc:`l9_code`) and compare your outputs with these
  notes.
