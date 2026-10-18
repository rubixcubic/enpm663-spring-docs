====================================================
Lecture
====================================================

.. note::

   These notes follow the L9 slides shown in class, in the same order and with
   the same sections, so you can read them at home. Every program output below
   is copied from the files the L9 scripts wrote, the same files the slides
   show. The scripts and how to run them are on the
   :doc:`code page <l9_code>`.

.. important::

   **Two kinds of output.** The closed loop and one VLM check call a real
   model, Gemini (``gemini-3.5-flash-lite``), on ARIAC 2025 through the course
   skills. Each of those outputs says "Recorded once, on 2026-10-17, with
   gemini-3.5-flash-lite. A rerun gives different answers." A second VLM
   check uses ``stand_in_vlm()``, a scripted stand-in whose canned replies
   hold the mistakes the checker must catch. Its outputs say "Scripted model:
   fixed replies."


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
   of agv1. The tray has four slots in two rows of two: slots 1 and 2 are the
   top row, left to right; slots 3 and 4 are the bottom row, left to right."
   The model cannot know the slot numbers unless you tell it. The order in
   the image depends on how the camera is mounted, so check it once against
   ``/agvN/tray_status``.
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
   :lines: 49-63
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

This section gives each field of the record a second source. The
demonstration has two runs: a real camera image and Gemini's answer, then a
scripted run with mistakes written in.


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


Demonstration Setup: One Camera Over agv1's Tray
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l9/vlm_tray.png
   :alt: Camera image, seen from above, of a gray kit tray with a round hole in the middle. Four blue battery cells lie left to right in four cavities, two in the top row and two in the bottom row. The top right cell shows printed text upside down: Li-Ion, 2000mAh, 3.7V. A black robot gripper covers the right edge of the image and the right end of the bottom right cell.
   :width: 60%
   :align: center

   The image Gemini saw, from sensor ``agv1_camera``
   (``config/l9_user_config.yaml``): 1280 × 720 pixels on
   ``/agv1_camera/image``. Slots 1 and 2 are the top row, 3 and 4 the bottom
   row, left to right. Taken at the end of the replan recording
   (:ref:`l9-demo`), after the fourth cell was placed.

The **record** (``record.json``) holds the voltage each cell read on a tester
before the agent placed it.

**Where the camera sits:**

1. The four slot centers, in the world frame (L8 smoke test): :math:`x` from
   2.085 to 2.215 m, :math:`y` from 1.450 to 1.550 m, :math:`z` 0.383 m. The
   camera sits above their center, (2.150, 1.500).
2. The field of view is 0.873 rad, ARIAC's default
   (``user_config_parser.py``). At a height :math:`h` above the slots, the
   image is :math:`2 \times \tan(0.873 / 2) = 0.933 \times h` wide. Chosen:
   twice the 0.130 m :math:`x` span of the slots, so
   :math:`h = 2 \times 0.130 / 0.933 = 0.279` m and
   :math:`z = 0.383 + 0.279 = 0.662` m.
3. Roll, pitch and yaw (0, :math:`\pi/2`, :math:`\pi/2`): the pitch points
   the camera down. The yaw puts slots 1 and 2 in the top row, as the prompt
   says: in the dry run's image with only slot 1 filled, that cell is top
   left.


Parse, Validate, Re-prompt Once
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/vlm_check.py
   :language: python
   :lines: 97-109
   :caption: lecture9/code/vlm_check.py (excerpt)

- The schema cannot say "each slot number once", so ``check()`` tests it in
  code.
- ``ask()`` sends the prompt, runs ``check()`` on the reply, and re-prompts
  once with the first error. The live prompt also carries the schema as
  text, since the model sees only the prompt.


The Cross-Check, Slot by Slot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/vlm_check.py
   :language: python
   :lines: 133-147
   :caption: lecture9/code/vlm_check.py (excerpt)

- ``type_from_volts()`` turns a recorded voltage into a type: 1.0 V to 1.4 V
  is ``NIMH``, 3.4 V to 3.8 V is ``LI_ION``. Each range is the nominal
  voltage plus or minus the 0.2 V cell tolerance in ``CellTypes.msg``: for
  NiMH, :math:`1.2 - 0.2 = 1.0` V and :math:`1.2 + 0.2 = 1.4` V. A slot with
  no record is checked for occupancy only.
- A slot whose verdict is not ``agree`` goes into ``flags``. ``decision()``
  then says submit only when ``flags`` is empty and all four slots are
  occupied, each with a record.

The checks run in order. Occupancy is compared first. Only if it agrees does
the code compare the type, and a VLM answer of ``UNKNOWN`` never counts as a
type disagreement.


Output: Gemini's Record, Cross-Checked
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/listings/vlm_live_attempts.txt
   :language: text

.. literalinclude:: outputs/listings/vlm_live_cross.txt
   :language: text

Recorded once, on 2026-10-17, with gemini-3.5-flash-lite. A rerun gives
different answers. Recording 1 of 1. ``call``: the VLM call's tokens and
time. ``record``: the voltage in ``record.json``, rounded to 0.01 V.

1. Gemini's first reply passed ``check()``, so no re-prompt was sent. It
   called all four slots occupied and ``LI_ION``; the topic and the records
   agree on every slot.
2. The NiMH running example used ``/submit_high_priority_order``. This Li-Ion
   kit goes to ``/submit_kitting_order``, which ARIAC refuses unless an AGV
   is at shipping: ``competition_manager_plugin.cpp``:249 checks first, then
   ``agv_tray_interface_plugin.cpp``:357.
3. ``decision()`` compares occupancy, type and the record of each slot. The
   next part shows a check it leaves out.


.. _l9-kit-total:

The Decision Leaves Out the Kit Total
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/listings/vlm_live_kit.txt
   :language: text

Recorded once, on 2026-10-17, with gemini-3.5-flash-lite. A rerun gives
different answers. Recording 1 of 1.

**The kit total, from** ``record.json``:

1. Sum: 3.540 + 3.444 = 6.984; + 3.645 = 10.629; + 3.465 = 14.094 V, about
   14.09 V.
2. ARIAC's window (``CellTypes.msg`` lines 7 and 11):
   :math:`4 \times 3.6 \pm 0.15` = 14.25 to 14.55 V. The sum is
   14.25 − 14.094 = 0.156 V short.
3. Chance: ARIAC adds the cells' own voltages
   (``agv_tray_interface_plugin.cpp``:416), not the tester readings. Each
   record is the mean of 10 readings (``skill_tools.py``), each with noise of
   standard deviation 0.05 V (``voltage_tester/model.sdf``). So chance moves
   one record by about :math:`0.05 / \sqrt{10} = 0.016` V, and the sum of
   four by about :math:`\sqrt{4} \times 0.016 = 0.03` V, a fifth of the
   0.156 V.

.. important::

   The run reached the lecture's goal: four cells, each read at 3.4 to
   3.8 V. The readings add to about 14.09 V, under ARIAC's 14.25 V minimum,
   so ARIAC would refuse this kit at ``/submit_kitting_order``
   (``agv_tray_interface_plugin.cpp``:437). The VLM "submit" compares only
   occupancy, type and the per-slot record. The kit total is a separate
   check, and it fails here.


The Scripted Run: Mistakes Written In
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::

   ``stand_in_vlm()`` is a scripted stand-in for the model: it returns canned
   replies, written to hold mistakes for the checker to find.

.. literalinclude:: outputs/listings/vlm_weak.txt
   :language: text

.. literalinclude:: outputs/listings/vlm_attempts.txt
   :language: text

Scripted model: fixed replies. Run: ``lecture9/code/run_all.sh`` (Python
3.12.3, jsonschema 4.10.3). To run it, see :doc:`l9_code`.

``json.loads`` rejects the paragraph; its hint, "one near the right", names
no slot. The first structured reply numbered the slots 0 to 3; the schema's
``minimum`` of 1 caught it, and the second reply passed.


Output: Two Disagreements Before the Submit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/listings/vlm_cross.txt
   :language: text

Scripted model: fixed replies. The tray status and the recorded voltages are
stand-in values for the NiMH example, chosen for this example.

1. **Slot 3:** the VLM says ``LI_ION``, but the cell read 1.24 V, inside the
   NiMH range of :math:`1.2 \pm 0.2` V (1.0 V to 1.4 V).
2. **Slot 4:** the VLM says empty, but ``/agv1/tray_status`` says occupied.
   The topic is ARIAC's own signal, so the VLM is wrong here, and its other
   answers from the same image are now in doubt.
3. The agent does **not submit**. It takes a new image and asks again, and
   the slot 3 question stays open until a third check settles it.


What the Demonstration Shows, and What a Live Call Adds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The two runs:**

- The scripted replies were written to get slot 3's type and slot 4's
  occupancy wrong, at confidences 0.6 and 0.7. The cross-check caught both.
- Gemini, on the real image, got occupancy and type right on all four slots.
  Its "damage ``NONE``" has no second source to check it against.
- Robot 2's gripper hides the right end of slot 4's cell. The model still
  gave slot 4 the same 0.95 as the fully visible slots, so its "no damage"
  answer covers a part the camera could not see. A confidence is the
  model's own number, not a check.

**What the live call cost.** Recorded once, on 2026-10-17, with
gemini-3.5-flash-lite. A rerun gives different answers. Recording 1 of 1.

From its ``call`` line: 1377 input tokens (277 text and 1100 image, in the
raw response) and 147 output tokens, in 2.02 s. At L8's prices, $0.30 and
$2.50 per million input and output tokens:
(1377 × 0.30 + 147 × 2.50) / 1,000,000 = $0.000781. These are the latency
and cost columns of the GP4 comparison.


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
  after ``robot1_place_on_tester``, the tester reads 3.4 V to 3.8 V for a
  good Li-Ion cell.
- In the demonstration, ``Record.after`` (``orchestrator.py`` lines 87 to
  101) updates the record from each skill result, ``guard()`` checks the
  next call against the record and a fresh observation, and the model judges
  what to do next.


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

This section covers what to do after a mismatch, applied to the four ARIAC
2025 challenges. In the demonstration, the model chooses, and code refuses a
call that breaks a rule.


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

**The replan recording shows the same:**

.. literalinclude:: outputs/listings/replan_tester1.txt
   :language: text

Recorded once, on 2026-10-17, with gemini-3.5-flash-lite. A rerun gives
different answers. Recording 1 of 1, from :ref:`l9-demo`.

- ``obs k`` is what the orchestrator read after the model's call :math:`k`;
  :math:`t` is the simulation time. Tester 1 read −1.00 V,
  ``MALFUNCTIONING``, from obs 3 to obs 10, and it kept publishing.
- With no cell on it, a working tester reads 0 V plus noise (same source
  file), so a reading near 0 V means the tester is empty.


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

- Gemini (``gemini-3.5-flash-lite``) fills agv1's four slots with Li-Ion
  cells in ARIAC, through the course skills, with the L8 orchestrator and its
  guard (``lecture9/code/closed_loop.py``). A **cycle** is four skill calls
  for one cell: pick from the conveyor, place on a tester, pick from the
  tester, place in a slot.
- Voltage tester 1 malfunctions at ``START_TIME`` 30 s for ``DURATION`` 70 s
  of simulation time (``config/l9_trial.yaml``), chosen from a scripted dry
  run (``outputs/closed_loop_dry.txt``):

  1. ``START_TIME``: cycle 1 ended at :math:`t` = 36.7 s; rounded down to
     10 s, that is 30 s. Cycle 1's reading came at :math:`t` = 23.8 s,
     before 30 s, so the first cell is tested before tester 1 breaks.
  2. ``DURATION``: cycles 2 and 3 took 71.2 − 36.7 = 34.5 s and
     105.1 − 71.2 = 33.9 s; 34.5 + 33.9 = 68.4 s, rounded up to 10 s, that
     is 70 s: about two cycles.

- Two recordings on the same trial file: one with a **replan** policy, one
  with a **wait** policy.

The full recordings and the commands that made them are on the
:doc:`code page <l9_code>`.


The Policy in Code
~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/closed_loop.py
   :language: python
   :lines: 110-114
   :caption: lecture9/code/closed_loop.py (excerpt)

.. literalinclude:: ../lecture8/code/orchestrator.py
   :language: python
   :lines: 119-125
   :caption: lecture8/code/orchestrator.py (excerpt)

- The first ``check`` is the one ``policy_guard(policy)`` returns, not
  ``vlm_check.check``. It never fired: the wait run never named tester 2.
- No code picks retry, wait or replan; the chart stays a concept. The model
  chooses, and two refused calls in a row end the run (L8's
  ``MAX_INVALID``).

The tool lists differ: the replan run offers no ``wait`` tool, so it must
replan to finish; the wait run offers ``wait`` and declares the tester
argument as 1 only.


Trace, Part 1: Tester 1 Breaks, Gemini Moves to Tester 2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/listings/replan_part1.txt
   :language: text

Recorded once, on 2026-10-17, with gemini-3.5-flash-lite. A rerun gives
different answers. Recording 1 of 1. ``model``: Gemini's call :math:`k`;
``obs k``: the observation after it, cut at the slide's width. Every skill
call succeeded on its first attempt; result lines and obs 0 are left out.

- Cell 1 read 3.54 V (obs 2). Tester 1 broke while robot 2 held cell 1
  (obs 3). Gemini put cell 2 on tester 2, which read 3.44 V (obs 6).


Trace, Part 2: Tester 1 Recovers, and the Guard Refuses a 3.39 V Cell
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/listings/replan_part2.txt
   :language: text

Recorded once, on 2026-10-17, with gemini-3.5-flash-lite. A rerun gives
different answers. Recording 1 of 1: calls 9 to 17; obs 9, 13, 15 and 16
left out. ``orch``: the orchestrator's refusal.

- Cell 3 read 3.65 V on tester 2 (obs 10). Tester 1 was back by obs 11, but
  Gemini kept using tester 2.
- Cell 4 read 3.39 V (obs 14), 0.01 V under the 3.4 V minimum. Gemini still
  asked to place it in slot 4; ``guard()`` refused, and Gemini dropped the
  cell in recycling.


Trace, Part 3: One More Cell Recycled, Then Slot 4
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/listings/replan_part3.txt
   :language: text

Recorded once, on 2026-10-17, with gemini-3.5-flash-lite. A rerun gives
different answers. Recording 1 of 1: calls 18 to 26; obs 18, 20, 22 and 24
left out. ``text 'done'``: a reply with no tool call.

- The next cell read 3.36 V on tester 1 (obs 19). Gemini dropped it in
  recycling itself, with no refused call. The cell after it read 3.46 V
  (obs 23) and went to slot 4.
- The goal, checked in code, held at obs 25 (:math:`t` = 225.8 s), and
  Gemini said ``done`` at call 26. The camera check of
  :ref:`l9-checking` ran right after.


Replan or Wait: The Wait Recording
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/listings/wait_hold.txt
   :language: text

Recorded once, on 2026-10-17, with gemini-3.5-flash-lite. A rerun gives
different answers. Recording 1 of 1, wait policy, same trial file. Calls 5
to 13; obs 6 to 11 left out.

- The goal text said: use tester 1 only; while tester 1 is
  ``MALFUNCTIONING``, call ``wait``, then read it again.
- Robot 2 picked cell 1 from tester 1 (call 5), and tester 1 then read
  ``MALFUNCTIONING`` (obs 5). Gemini waited 5, 10, 20 and 30 s while robot 2
  held that tested cell: from obs 5 to obs 12, 112.6 − 38.2 = 74.4 s. The
  cell already had its reading (3.56 V, obs 3), so it could have gone to
  slot 1 at once; the goal text did not say so.


Replan or Wait: The Two Recordings Side by Side
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 22 39 39
   :class: compact-table

   * -
     - **Replan recording**
     - **Wait recording**
   * - Tools offered
     - 10: no ``wait``
     - 11: ``wait``; tester 1 only
   * - Model calls
     - 26: 24 skills, 1 refused, ``done``
     - 26: 16 skills, 4 ``wait``, 5 tester readings, ``done``
   * - Loop tokens
     - 122,861 in, 477 out
     - 116,624 in, 414 out
   * - Goal reached at
     - :math:`t` = 225.8 s (obs 25); kit 14.09 V
     - :math:`t` = 224.0 s (obs 25); kit 14.01 V
   * - Lost to the malfunction
     - almost none: slot 3 filled at :math:`t` = 108.8 s; dry run 105.1 s
     - 112.6 − 38.2 = 74.4 s (obs 5 to 12), holding a tested cell
   * - Lost to recycling
     - 39.7 s (obs 12 to 17) + 40.3 s (obs 17 to 21) = 80.0 s
     - none

.. important::

   Both recordings finished at about 225 s, and one run each cannot say
   which policy is faster. Here the fourth cell read 3.39 V, so the guard
   refused it. The same cell read 3.41 V in the dry run and in the wait run
   (``SEED`` 1 draws the same cells), and one record moves by about 0.016 V.
   So chance cost this run the 80 s.

- Recorded once, on 2026-10-17, with gemini-3.5-flash-lite. A rerun gives
  different answers. Recording 1 of 1 each; the dry run was scripted, with
  no challenge.
- Tokens: the two ``outputs/*_cost.txt`` files. Both recordings with the VLM
  call, at $0.30 and $2.50 per million input and output tokens:
  (240,862 × 0.30 + 1,038 × 2.50) / 1,000,000 = $0.074854.


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
   calls it as a tool. The demonstration had no kit tool, so no tool chose
   the cells: the model placed every cell that read 3.4 to 3.8 V, and the
   total came out 14.09 V, under the window (:ref:`l9-kit-total`).

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
- A VLM describes the cells for the agent. Each field with a second source
  (tray status, tester voltages) is checked against it before the agent acts.
  The GP3 executor runs the agent's decisions.

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

- Fill in the GP3 peer-review form on ELMS-Canvas (GP3 was due today).
- Read the GP4 specification and agree on who owns the agent, the VLM module
  and the comparison.
- Set up LLM and VLM access (a hosted API key or a local model with Ollama)
  with the course :doc:`AI Access </ariac/ai_setup>` page.
- Rerun the scripted VLM check: on your copy, ``python3 vlm_check.py`` in
  ``lecture9/code`` (see :doc:`l9_code`), and compare its output with these
  notes. In class, ``run_all.sh`` reran it and checked every slide listing
  against its source in ``lecture9/outputs/``: ``closed_loop_replan_rec1.txt``,
  ``closed_loop_wait_rec1.txt`` or ``vlm_check.txt``; it also needs the
  lecture's tests and the slides, which are not on this site. The Gemini runs
  need ARIAC and an API key.
