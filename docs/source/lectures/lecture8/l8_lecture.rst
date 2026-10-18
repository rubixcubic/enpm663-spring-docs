====================================================
Lecture
====================================================

.. note::

   These notes follow the L8 slides shown in class, in the same order and
   with the same sections, so you can read them at home. Every program output
   below is copied from the files the L8 scripts wrote, the same files the
   slides show. The scripts and how to run them are on the
   :doc:`code page <l8_code>`.

.. important::

   **Two kinds of output.** Some demonstrations call a real model, Gemini
   (``gemini-3.5-flash-lite``), and drive ARIAC through the course skills. Each
   of those outputs says "Recorded once, on 2026-10-17, with
   gemini-3.5-flash-lite. A rerun gives different answers." The others use
   ``ScriptedModel``, a stand-in that returns fixed replies, one per call, to
   show a guard or a check. Each of those says "Scripted model: fixed
   replies." A scripted output repeats exactly; a real model's does not.


.. _l8-recap:

Recap
-----

From L7
~~~~~~~

- A plan-to-BT factory turns each plan step into a subtree: guard, act,
  verify, update.
- Retry and timeout decorators are always bounded.
- Replanning triggers stop a plan and ask the planner for a new one.

Today's Question
~~~~~~~~~~~~~~~~

GP4 replaces the PDDL planner with an LLM agent. **What must the code around
the LLM do so that the robots stay safe?**

.. admonition:: GP3
   :class: warning

   GP3 is due next week (Week 10, March 31). Bring your questions on the
   executor and the replanning demo.


.. _l8-where-the-llm-goes:

Where the LLM Goes
------------------

One part of the GP3 stack changes in GP4; the rest carries over. This section
also says where an agent helps, and where a classical planner is the better
tool.

The GP3 Stack and What GP4 Changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 38 42
   :class: compact-table

   * - **Part**
     - **GP3**
     - **GP4**
   * - State writer
     - Problem generator: a PDDL problem from the world model (L6)
     - The same world model, written as JSON for the agent
   * - Decision
     - PDDL planner (Fast Downward through UPF)
     - An LLM agent: an orchestrator runs a loop around the LLM
   * - Executor
     - Plan-to-BT executor with guards, retry and triggers (L7)
     - The same executor
   * - Skills and perception
     - Skills package; GP2 lidar detector
     - The same

The agent decides which skill runs next; classical code moves the robots.
This is the "orchestrate" part of NVIDIA's definition of physical AI from
:doc:`L1 </lectures/lecture1/l1_index>`: physical AI lets autonomous systems
"perceive, understand, reason, and perform or orchestrate complex actions in
the physical world."

Where an Agent Helps, and Where It Does Not
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**A PDDL domain covers only what its author modeled.** GP3's domain does not
model the four ARIAC challenges: conveyor malfunction, voltage tester
malfunction, vacuum tool malfunction and high-priority order. An LLM agent is
useful on ambiguity, new situations and recovery.

**On the routine path, the classical planner wins.** It is cheaper (no
tokens), deterministic (same problem, same plan) and easier to audit (every
step follows from the domain). This boundary is part of the course design.
L9 compares the planner and the agent on the same trial.


.. _l8-llm-as-function:

The LLM as a Function
---------------------

Messages In, Text Out, Nothing Kept
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: context
   :class: note

   A **large language model (LLM)** call takes a list of messages and returns
   text. Between calls it keeps nothing. Everything it knows about the factory
   must be in the messages of that call. These messages are its
   **context**.

The output is **sampled**: the model picks each piece of text with some
randomness, so the same messages can return different answers.

Anthropic's API reference describes the same thing: "Our models are trained
to operate on alternating ``user`` and ``assistant`` conversational turns.
When creating a new ``Message``, you specify the prior conversational turns
with the ``messages`` parameter, and the model then generates the next
``Message`` in the conversation."
(`Anthropic Messages API reference <https://platform.claude.com/docs/en/api/messages/create>`_,
read 2026-10-12)

So **the program, not the model, keeps the conversation.** It sends the
earlier turns again on every call.

Three Consequences for a Robot System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. The program sends the current state on every call, because the model
   keeps nothing.
2. The program checks every output before anything moves, because the output
   is sampled and can be wrong.
3. The program limits the cost, because every call is paid for in
   **tokens**: the pieces of text the model reads and writes.

.. tip::

   An agent's behavior comes from the loop around the model, not from the
   model alone. That loop is ordinary Python that your team writes and tests.

Some APIs offer settings, such as a **temperature**, that change how much the
answers vary. No setting makes the output safe to run without checks.


.. _l8-agent-loop:

The Agent Loop
--------------

This section covers the loop, its stop conditions and the orchestrator that
runs it. A live demonstration then runs an orchestrator with Gemini driving
the ARIAC inspection robots through the course skills.

Five Steps, Run by the Orchestrator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: orchestrator and agent loop
   :class: note

   The **orchestrator** is your team's code that runs the **agent loop**
   around the LLM. The loop has five steps:

   1. **Observe:** read the state from ROS and your team's records.
   2. **Reason:** send the LLM the goal, the state, the tools and the
      history.
   3. **Act:** the LLM returns a tool call; the orchestrator checks it and
      runs it through the executor.
   4. **Observe the result:** success, or a failure with its reason, joins
      the history.
   5. **Repeat** until a stop condition fires.

.. figure:: /_static/images/l8/agent_loop.svg
   :alt: The agent loop as five blocks. Tag 1, Read state (blue, the orchestrator), has an arrow to tag 2, Ask the LLM (orange). An arrow goes down to tag 3, Check and run (blue), which has an arrow to the Factory block (green) on the right. Tag 3 also has an arrow left to tag 4, Record result (blue), which leads up to tag 5, Stop? (blue). From Stop?, 'no' leads up to Read state and 'yes' leads left to End. A line from the Factory runs over the top of the figure into Read state.
   :width: 90%
   :align: center

   The agent loop. Tags 1 to 5 are the five steps above. The line from the
   Factory back to Read state is the next observation: the loop reads the
   state again after every action.

Colors in every L8 figure: **orange** is the LLM, **blue** is your team's code
(the orchestrator), **green** is the factory side (executor, skills, ARIAC
actions, robots).

Step 1: What the Orchestrator Reads
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From ARIAC (the ARIAC API page):

- ``/competition_status``: the competition state.
- ``/inspection_conveyor/status``: the conveyor's status.
- The voltage topics, such as ``/voltage_tester_1/voltage``: a reading and
  the tester's ``operation_status``.
- ``/{agv_name}/info``: the AGV's station; ``/{agv_name}/tray_status``: four
  slot occupied flags.

From your team's records:

- Each cell's inspection result and averaged voltage, the kit under way, and
  the steps already done.
- ARIAC publishes no topic for where each cell is (L3), so these records are
  the only source.

Step 5: Stop Conditions, Each Checked in Code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A **stop condition** ends the loop. Each one is checked in code:

1. The goal is reached: the kit was submitted.
2. A step limit is reached, for example 20 steps (chosen for this example).
3. Too many invalid outputs in a row.
4. The trial's time limit is near (``TIME_LIMIT`` in the trial file).
5. An operator stops the run.

.. warning::

   The model can say "done". Only the orchestrator decides that the goal is
   reached, by checking the state in code.

The Orchestrator Owns the Loop; the LLM Only Proposes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l8/orchestrator_checks.svg
   :alt: The orchestrator, a large blue frame, sits between an orange LLM block on the left and three green blocks on the right: Executor, then Skills, ARIAC, then Robots, linked top to bottom. Inside the frame are five checks in order: tag 1 Parse JSON, tag 2 Schema, tag 3 Semantic checks, tag 4 Executor guards, tag 5 Stop conditions. An arrow labeled call goes from the LLM into the frame and an arrow labeled error comes back. An arrow labeled run goes from the frame to the Executor, and an arrow labeled result comes back from the Robots block.
   :width: 90%
   :align: center

   The orchestrator between the LLM and the robots, with its five checks.

The five checks, in order:

1. The text parses as JSON.
2. It fits the tool's schema.
3. It makes sense in the factory now.
4. The executor's guards hold.
5. No stop condition has fired.

- The orchestrator owns the loop, the list of tools, the checks and the logs.
  **The LLM never sends a ROS goal itself.**
- Check 4 uses the same **guards** as L7's executor: the robot holds the
  right object, the AGV is at the right station, the slot is free.
- A call that fails checks 1 to 4 is not run. It goes back to the LLM as an
  error message, and the loop goes on.

Demonstration: The Setup
~~~~~~~~~~~~~~~~~~~~~~~~

- ARIAC 2025 and the course skills server run in the course container. Robot
  1 moves a cell from the conveyor to voltage tester 1 or 2; robot 2 moves it
  from a tester to an AGV tray slot or the recycling bin.
- **Ten tools:** the seven skill actions of the two robots, and three
  readings (testers, conveyor, one AGV).
- ``robot1_pick_from_conveyor`` also feeds the cell and submits a passing
  inspection report, since the skills do not wrap those ARIAC services. The
  report is correct: the trial file sets ``DEFECT_RATE`` to 0.0.
- The goal (``GOAL``): "Put one Li-Ion cell from the conveyor into agv1 slot
  1. Test its voltage on tester 1 first."
- **Run 1:** Gemini (``gemini-3.5-flash-lite``) chooses every call. **Run
  2:** a scripted model, to show the guard.

.. note::

   Every output in this section comes from ``lecture8/code/orchestrator.py``,
   recorded once on 2026-10-17 (``outputs/agent_rec1.txt``). The full
   recording, with its header, is on the :doc:`code page <l8_code>`.

Demonstration: The Tool List the Model Sees
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/skill_tools.py
   :language: python
   :lines: 84-93
   :caption: lecture8/code/skill_tools.py (excerpt)

- ``_int(1, 3, ...)`` writes an integer from 1 to 3 with a description.
  ``_args`` lists the arguments and the required ones, and allows no others.
  ``check_call()`` enforces that rule, because Gemini's ``parameters`` schema
  has no ``additionalProperties``
  (`Gemini API reference <https://ai.google.dev/api/generate-content>`_, read
  2026-10-17).
- The other skill tools: ``robot1_move_home``, ``robot1_pick_from_conveyor``,
  ``robot1_place_on_tester``, ``robot2_move_home``,
  ``robot2_pick_from_tester``, ``robot2_drop_in_recycling``. The readings:
  ``read_testers``, ``read_conveyor``, ``read_agv``.

A tool is a name, a description and an input schema (see
:ref:`l8-tool-calling`). The description says what the tool needs and what
each failure leaves behind, because that text is all the model knows about
the tool.

Demonstration: The Guard
~~~~~~~~~~~~~~~~~~~~~~~~

Two excerpts of ``guard()``:

.. literalinclude:: code/orchestrator.py
   :language: python
   :lines: 110-116
   :caption: lecture8/code/orchestrator.py, guard() (excerpt 1)

.. literalinclude:: code/orchestrator.py
   :language: python
   :lines: 130-131
   :caption: lecture8/code/orchestrator.py, guard() (excerpt 2)

- ``rec`` is the orchestrator's **record** of what each robot holds. ARIAC
  publishes none (L3). A pick needs ``NOTHING``, a place needs ``CELL``.
- ``n`` is the tester argument, and ``t`` is that tester's reading in
  ``snap``, the observation before the call. Empty means below 0.5 V
  (``EMPTY_TESTER_V``, chosen in the skills tests).
- The guard also refuses an occupied slot, an AGV not at ``INSPECTION``, or a
  cell outside 3.4 to 3.8 V.

The guard returns an error text, or ``None`` when the call may run.

Demonstration: The Loop, Part 1 (Send and Receive)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/orchestrator.py
   :language: python
   :lines: 208-219
   :caption: lecture8/code/orchestrator.py, run() (excerpt)

- ``snap`` is the first **observation** and ``rec`` the record. Each call
  sends ``SYSTEM``, the ten tool declarations and every message so far.
- ``max_steps`` is ``MAX_STEPS`` = 15, the step limit (chosen for this
  example).

Demonstration: The Loop, Part 2 (Check, Run, Record)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/orchestrator.py
   :language: python
   :lines: 241-254
   :caption: lecture8/code/orchestrator.py, run() (excerpt)

- ``error`` comes from ``check_call()``: an unknown tool, then the schema,
  then ``guard()``.
- ``max_invalid`` is ``MAX_INVALID`` = 2 invalid outputs in a row (chosen
  for this example). The result, the new observation and the record go back
  to the model.

Run 1: Gemini Fills agv1 Slot 1 in Five Calls
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/listings/run1_calls.txt
   :language: text

Recorded once, on 2026-10-17, with gemini-3.5-flash-lite. A rerun gives
different answers. Recording 1 of 1. Run 2 ran first in the same session
(``--runs 2,1``).

``model`` is Gemini's call and ``result`` the skill's answer, cut at the
slide's width. The next listing shows two of the observations.

Reading Run 1
~~~~~~~~~~~~~

.. literalinclude:: outputs/listings/run1_obs24.txt
   :language: text

Recorded once, on 2026-10-17, with gemini-3.5-flash-lite. A rerun gives
different answers. ``obs k`` is read after call :math:`k`; ``slots 1---``
means slot 1 is occupied.

1. Calls 1 and 2: robot 1 catches a cell and places it on tester 1. ``obs 2``
   reads 3.54 V on tester 1, inside 3.4 to 3.8 V.
2. Calls 3 and 4: robot 2 moves the cell from tester 1 to agv1 slot 1.
   ``obs 4`` shows ``slots 1---``.
3. Call 5: Gemini replies "done". The orchestrator checks in code that slot
   1 is occupied and that the record holds a voltage from 3.4 to 3.8 V, then
   stops: goal reached.
4. The input grows on every call: 1535 − 1264 = 271, 1788 − 1535 = 253,
   2045 − 1788 = 257 and 2309 − 2045 = 264 tokens more, because each call
   sends the whole history again.

Run 2: The Scripted Model Repeats a Refused Call
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/listings/run2.txt
   :language: text

Scripted model: fixed replies. The replies ran against ARIAC, so the
readings are real.

**Reading Run 2:**

1. Twice the model asks robot 2 to pick from tester 1. Tester 1 reads
   0.00 V, then 0.04 V: below 0.5 V, so the guard refuses. No robot moves.
2. Two invalid outputs in a row reach ``MAX_INVALID``, so the orchestrator
   stops. In GP4 it would then stop safely or hand the decision to the GP3
   planner.


.. _l8-plan-and-react:

Plan-and-Execute and ReAct
--------------------------

There are two ways to place the LLM calls in a run. This section says which
one fits which ARIAC situation, and what time allows.

Two Timelines
~~~~~~~~~~~~~

.. figure:: /_static/images/l8/plan_vs_react.svg
   :alt: Two timelines, time running to the right, not to scale. Plan-and-execute: one orange LLM block labeled Plan, then three green executor steps, then a dashed line marked tag 1, then an orange block labeled Replan, then four green steps. ReAct: six pairs of a small orange LLM block followed by a green step.
   :width: 90%
   :align: center

   Orange: one LLM call. Green: one executor step. Tag 1: a replanning
   trigger fires (L7).

The timeline is not a picture of space. It shows only the order of calls and
steps.

The Two Patterns
~~~~~~~~~~~~~~~~

.. admonition:: Definition: plan-and-execute
   :class: note

   The LLM writes a full plan once. The executor runs it, and asks for a new
   plan only when a trigger fires (L7). This means few calls, low cost, and
   the whole plan can be checked before any robot moves.

.. admonition:: Definition: ReAct (Reason and Act)
   :class: note

   Each iteration is one reasoning step and one tool call; the model sees
   each result before it chooses the next. This means more calls, more cost
   and more delay, but the agent adapts at every step.

The ReAct paper describes it this way: "we explore the use of LLMs to
generate both reasoning traces and task-specific actions in an interleaved
manner" (S. Yao et al.,
`ReAct: Synergizing Reasoning and Acting in Language Models <https://arxiv.org/abs/2210.03629>`_,
ICLR 2023; arXiv preprint 2022).

Choosing a Pattern for an ARIAC Situation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 36 22 42
   :class: compact-table

   * - **Situation**
     - **Pattern**
     - **Reason**
   * - Build the next Li-Ion kit with both testers working
     - Plan-and-execute
     - The steps are known; check the whole plan once
   * - A voltage tester reports ``MALFUNCTIONING`` in the middle of a kit
     - ReAct-style steps, then a new plan
     - What still works is unclear until a few results come back
   * - A high-priority order arrives
     - Plan-and-execute
     - A known sequence: switch the cell feed to Ni-MH, build, submit with
       the order ID, switch back

.. tip::

   A common hybrid is plan-and-execute with ReAct-style recovery when a
   trigger fires. It matches the L7 executor directly.

Time Limits the Agent's Reach
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Two factory clocks:

- The conveyor moves at up to 0.1 m/s (the ``CONVEYOR_SPEED`` maximum in
  ``user_config_schema.json``).
- ARIAC's target for an inspection report is 4 s
  (``NOMINAL_INSPECTION_TIME`` in ``ariac_db/config/scoring_weights.yaml``).
  The report must arrive before the cell reaches the door (L5).

What 4 s means at top speed:

1. At 0.1 m/s a cell moves 0.1 × 4 = 0.4 m in 4 s.
2. Every second spent waiting for a model moves the cell another 0.1 m toward
   the door.

.. important::

   Loops tied to the moving conveyor stay classical: inspection, and picking
   a cell after the door. The agent decides at a slower level: which cells go
   in which kit, when to switch the feed, how to respond to a challenge.

Class Discussion: What Should the Agent Own?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Discussion question:** which ARIAC decisions should the agent own, and
which must stay classical because of time or safety?

Argue from:

- The factory's clocks above, and the trial's ``TIME_LIMIT``.
- The L7 triggers: which of them need a new plan, and which only a retry or a
  wait?
- What happens when the model is slow or wrong at that point.

The same question is on the ELMS discussion board for the online section.


.. _l8-prompt-structure:

Prompt Structure for a Planner
------------------------------

The system message holds what stays fixed during a run. The user message
holds the state and the goal, as compact JSON. Arithmetic stays in code.

The System Message: Four Parts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: system message and user message
   :class: note

   The **system message** holds what stays the same on every call of a run.
   The **user message** holds what changes: the current state and the goal.

The system message has four parts:

1. **Role:** the agent plans the next actions for the inspection and kitting
   cell.
2. **Facts it can rely on:** the robots and what each can reach, the four
   stations, and the kit rule.
3. **Rules:** use only the listed tools; never invent a cell ID; stop and
   report when no action is safe.
4. **Output format:** the JSON schema of the next section.

The Li-Ion kit rule, from ``CellTypes.msg``:

1. Nominal cell voltage 3.6 V, so a kit of 4 is 4 × 3.6 = 14.4 V.
2. Kit tolerance 0.15 V: 14.4 − 0.15 = 14.25 V to 14.4 + 0.15 = 14.55 V.
3. Cell tolerance 0.2 V: each cell 3.6 − 0.2 = 3.4 V to 3.6 + 0.2 = 3.8 V.

An Example System Message, and the User Message
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

System message (written for this lecture; tested once in the
:ref:`Structured Output <l8-structured-live>` section):

.. literalinclude:: outputs/listings/system_message.txt
   :language: text

- The system message is the same on every call of a run. The facts match the
  ARIAC sources: three AGVs (``ariac.world``), four stations
  (``AgvStations.msg``).
- The user message holds the current state and the goal, as compact JSON from
  the same world model the L6 problem generator reads. GP3 and GP4 then read
  one model (L3).
- **Few-shot examples:** one or two short worked decisions in the prompt show
  the expected format. Each one costs tokens on every call, so keep them
  short.

Arithmetic Stays in Code
~~~~~~~~~~~~~~~~~~~~~~~~

LLMs make arithmetic slips. The orchestrator computes voltage sums and the
remaining window, and gives the model the results.

The L3 kit, computed by the orchestrator:

1. Three cells on the tray (values chosen for the L3 example):
   3.55 + 3.62 + 3.70 = 10.87 V.
2. Lowest fourth cell: 14.25 − 10.87 = 3.38 V, raised to the cell minimum of
   3.40 V.
3. Highest fourth cell: 14.55 − 10.87 = 3.68 V.

.. tip::

   The prompt says "the fourth cell must be from 3.40 V to 3.68 V", not the
   three voltages. The model chooses among cells; code does the sums. A tool
   that computes the window is the other option.


.. _l8-structured-output:

Structured Output
-----------------

This section covers JSON Schema and how ARIAC itself uses it, then validation
in five steps with semantic checks and a bounded retry. A demonstration runs a
validator on seven scripted outputs, two retry runs and one real model
output.

JSON Schema, and ARIAC Uses It Too
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: JSON Schema
   :class: note

   **JSON Schema** is a JSON document that describes the allowed shape of
   other JSON documents: ``type``, ``required`` fields, ``enum`` (a list of
   allowed values), ``minimum`` and ``maximum``, and ``additionalProperties``
   (whether extra fields are allowed).

ARIAC's team configuration check:

- ARIAC checks each team configuration file (a YAML file) against
  ``ariac_setup/config/user_config_schema.json`` (draft-07), with the Python
  ``jsonschema`` package.
- In that schema ``CONVEYOR_SPEED`` is above 0 and at most 0.1
  (``exclusiveMinimum`` 0, ``maximum`` 0.1), and a sensor's ``TYPE`` must be
  one of ``break_beam``, ``distance``, ``lidar`` or ``camera``.
- A bad file is refused before the simulation starts. Your orchestrator does
  the same with an LLM's output.

A Schema for One AGV Move
~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/validator.py
   :language: python
   :lines: 21-29
   :caption: lecture8/code/validator.py (excerpt)

- ``STATIONS`` lists ``INSPECTION``, ``ASSEMBLY``, ``SHIPPING`` and
  ``RECYCLING``. The field names are chosen for this example.
- The orchestrator maps a valid move to the ARIAC action ``/agv{N}/move`` with
  ``station_id`` 1 to 4 (``AgvStations.msg``).
- ``agv`` runs from 1 to 3 because ARIAC 2025 has three AGVs.

Validation in Five Steps
~~~~~~~~~~~~~~~~~~~~~~~~

1. **Parse** the text as JSON. A parse error is a failure.
2. **Validate against the schema**, for example with ``jsonschema`` or
   Pydantic. ``jsonschema.validate(instance, schema)`` raises
   ``ValidationError``. The package reads the draft from the schema's
   ``$schema`` field, and uses the newest draft, 2020-12, when that field is
   missing.
3. **Run the semantic checks** a schema cannot express: the cell ID exists,
   the AGV is where the action needs it, the kit total stays inside its
   window.
4. **On a failure, send the exact error message back** to the LLM and ask
   again.
5. **Cap the retries**, for example at 2 (chosen for this example). After the
   cap, fall back: stop safely, or hand the decision to the GP3 planner.

A **semantic check** is a check that needs the factory's current state; a
**bounded retry** is a retry with a fixed cap.

Demonstration: Steps 1 to 3 in One Function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/validator.py
   :language: python
   :pyobject: check
   :caption: lecture8/code/validator.py (excerpt)

``PATHS`` holds the seven AGV paths ARIAC accepts (``agv_motion_plugin.cpp``).
The factory is the stub of ``stub_agv.py``, chosen for this example.

The seven paths, from ``stub_agv.py``:

.. literalinclude:: code/stub_agv.py
   :language: python
   :lines: 11-19
   :caption: lecture8/code/stub_agv.py (excerpt)

Demonstration: Seven Outputs, One Check Each
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Output (system Python 3.12.3, ``jsonschema`` 4.10.3):

.. literalinclude:: outputs/listings/validator_seven.txt
   :language: text

Scripted model: fixed replies. The seven outputs are texts chosen for this
example.

**Reading the seven results:**

1. The valid move: ``agv1`` holds 4 cells and ``INSPECTION`` to ``SHIPPING``
   is an ARIAC path.
2. ``SHIPPING`` without quotes is not JSON, so step 1 fails.
3. AGV 4 breaks ``maximum``: ARIAC 2025 has three AGVs.
4. ``'SHIP'`` breaks ``enum``: no station has that name.
5. An extra ``speed`` field breaks ``additionalProperties``.
6. ``agv2`` passes the schema, but holds 3 of 4 cells: a semantic failure.
7. ``agv3`` passes the schema, but is at ``RECYCLING``, and ARIAC has no path
   from there to ``SHIPPING``.

.. important::

   The last two outputs are well formed and still wrong. Only code that knows
   the factory's state catches them.

Demonstration: Steps 4 and 5, the Bounded Retry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/validator.py
   :language: python
   :pyobject: ask
   :caption: lecture8/code/validator.py (excerpt)

``MAX_RETRIES`` = 2 gives 3 attempts in all (chosen for this example). The
model is ``ScriptedModel``, which returns fixed replies.

Retry Run 1: Accepted on the Third Attempt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Output of ``lecture8/code/validator.py``:

.. literalinclude:: outputs/listings/validator_retry1.txt
   :language: text

Scripted model: fixed replies.

1. Attempt 1 fails the schema; the exact error text goes back to the model.
2. Attempt 2 fails a semantic check; that error goes back too.
3. Attempt 3 passes all three steps and is accepted.

Retry Run 2: The Cap Is Reached
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Output of ``lecture8/code/validator.py``:

.. literalinclude:: outputs/listings/validator_retry2.txt
   :language: text

Scripted model: fixed replies.

1. Three attempts fail, each for a different reason.
2. After the third failure nothing is sent back: the cap is reached, and the
   orchestrator falls back.

.. _l8-structured-live:

One Real Output, Through the Same Check
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Output of ``lecture8/code/structured_live.py``:

.. literalinclude:: outputs/listings/structured_live.txt
   :language: text

Recorded once, on 2026-10-17, with gemini-3.5-flash-lite. A rerun gives
different answers.

**Reading the output:**

1. Gemini got the example system message of the
   :ref:`Prompt Structure <l8-prompt-structure>` section, the user message
   above (the state of the stub factory, chosen for this example), and one
   tool, ``move_agv``, whose parameters are ``SCHEMA``. It is L6's
   ``move-agv`` without the dash; :ref:`l8-what-a-tool-is` says why.
2. It called ``move_agv`` with ``agv`` 1 and ``SHIPPING``. The script turns
   the arguments back into JSON text, and ``check()`` runs steps 1 to 3 on
   it: valid.
3. One valid output says nothing about the next one, so the check runs on
   every output.

Constrained Output Removes Some Errors, Not All
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some providers can hold the output to a schema while it is generated. This is
**constrained output**.

- OpenAI: "Structured Outputs is a feature that ensures the model will always
  generate responses that adhere to your supplied JSON Schema"
  (`structured outputs guide <https://developers.openai.com/api/docs/guides/structured-outputs>`_).
  The same page says "a refusal does not necessarily follow the schema you
  have supplied".
- Anthropic: add ``strict: true`` to a tool definition "to ensure Claude's
  tool calls always match your schema exactly"
  (`tool use overview <https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview>`_).

.. warning::

   A schema-perfect output can still ship a tray with 3 cells. Constrained
   output removes parse and schema errors (steps 1 and 2), not semantic
   errors, so steps 3 to 5 stay.


.. _l8-tool-calling:

Tool Calling and MCP
--------------------

This section says what a tool is and how to design tools for the factory,
then introduces the Model Context Protocol (MCP): hosts, clients and servers.
A demonstration serves ten tools (7 skills and 3 readings) from an MCP server, and a client
lists them and calls three against ARIAC.

.. _l8-what-a-tool-is:

What a Tool Is
~~~~~~~~~~~~~~

.. admonition:: Definition: tool and tool call
   :class: note

   1. A **tool** is a **name**, a **description** and an **input schema**. In
      the Gemini API it is a **function declaration** with ``name``,
      ``description`` and ``parameters``.
   2. The model returns a **tool call**: a ``function_call`` part with an
      ``id``, a ``name`` and ``args``, the arguments as JSON.
   3. The orchestrator runs the call and sends the result back as a function
      response part, with the call's ``name`` and ``id``.

The Gemini API reference describes the three fields of a declaration:
``name``: "The name of the function." ``description``: "A brief description
of the function." ``parameters``: "Describes the parameters to this
function."
(`Gemini API reference, generateContent <https://ai.google.dev/api/generate-content>`_,
read 2026-10-17)

- The name, the description and the schema are all the model knows about a
  tool. So the description states what the tool does, its preconditions and
  its failure results.
- The Gemini guide says to name functions "without spaces, periods, or
  dashes"
  (`function calling guide <https://ai.google.dev/gemini-api/docs/generate-content/function-calling>`_,
  read 2026-10-17). So the L6 action ``move-agv`` is the tool ``move_agv`` in
  this lecture.

Designing Tools for the Factory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. One tool per skill action, named for the robot and the action:
   ``robot2_place_in_slot``, ``robot1_place_on_tester``, ...
2. Narrow arguments: integer ranges, such as ``tester`` 1 to 2, ``agv`` 1 to
   3 and ``slot`` 1 to 4.
3. Structured results: the skill's result code, what the robot holds, and a
   message.
4. No catch-all tool that runs arbitrary commands.

.. tip::

   Each rule shrinks what a wrong answer can do. A model that can only call
   ``robot2_place_in_slot`` with ``agv`` 1 to 3 and ``slot`` 1 to 4 cannot
   send a joint command.

The result codes of ``SkillResult.msg``: ``SUCCESS``, ``PLANNING_FAILED``,
``EXECUTION_FAILED``, ``GRASP_FAILED``, ``PRECONDITION_FAILED``,
``PLACE_NOT_FOUND``, ``ZONE_BUSY_TIMEOUT`` and ``CANCELED``.

MCP: Hosts, Clients and Servers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: Model Context Protocol (MCP)
   :class: note

   The **Model Context Protocol (MCP)** is an open protocol between agent
   applications and the servers that provide tools.

.. figure:: /_static/images/l8/mcp_client_server.svg
   :alt: A dashed blue frame, tag 1, holds an orange LLM block, a blue Orchestrator block and, below them, a blue MCP client block, tag 2. Arrows labeled tools/list and tools/call go right from the client to an MCP server frame, tag 3, and an arrow labeled results comes back. The server holds three blocks: 10 tools: robot1_..., robot2_..., read_...; Resources; and Prompts. An arrow goes from the tools block to a green block, tag 4, labeled Skill actions, ARIAC topics.
   :width: 90%
   :align: center

   An MCP host, client and server, and the skill actions and ARIAC topics
   behind the tools.

The tags, with the definitions quoted from the
`MCP architecture overview <https://modelcontextprotocol.io/docs/learn/architecture>`_
(spec version 2026-07-28, read 2026-10-12):

1. **MCP host:** "The AI application that coordinates and manages one or
   multiple MCP clients".
2. **MCP client:** keeps a connection to one server.
3. **MCP server:** "A program that provides context to MCP clients".
4. The skill actions and ARIAC topics behind the tools.

What a Server Offers, and How a Client Asks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Three core primitives a server can expose:

- **Tools:** "Executable functions that AI applications can invoke to perform
  actions".
- **Resources:** "Data sources that provide contextual information to AI
  applications".
- **Prompts:** "Reusable templates that help structure interactions with
  language models".

Messages:

- MCP messages are **JSON-RPC 2.0** messages (a standard format for a request
  and its response in JSON). A client finds the tools with ``tools/list`` and
  runs one with ``tools/call``.
- Two transports: **stdio**, for a local server started as a process, and
  **Streamable HTTP**, for a remote one.
- Write the robot tools once as an MCP server, and any agent framework that
  speaks MCP can use them.

Demonstration: A Server for the Skill Tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/skills_mcp_server.py
   :language: python
   :lines: 10-21
   :caption: lecture8/code/skills_mcp_server.py (excerpt)

- The loop serves each of the ten L8 tools: the name and the description
  from ``DECLARATIONS``, the function from ``SkillTools``. MCP writes each
  input schema from the function's type hints.
- The server uses the Python ``mcp`` package 2.3.0, in the lecture's virtual
  environment. ``MCPServer`` is the class that 1.x tutorials call
  ``FastMCP``. In 2.3.0, ``mcp/server/fastmcp.py`` holds only a message
  (read 2026-10-17): its docstring says "``FastMCP`` is now
  ``mcp.server.mcpserver.MCPServer``", and importing it raises
  ``ModuleNotFoundError``.

Demonstration: A Client That Calls Three Tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: code/skills_mcp_client.py
   :language: python
   :lines: 25-34
   :caption: lecture8/code/skills_mcp_client.py (excerpt)

- ``client`` is connected to ``skills_mcp_server.py``, which the client
  started as a process; they talk over stdio. Before this loop, the client
  lists the tools: each one's name, and one line per argument.
- ``CALLS`` holds three calls. No LLM is involved: the client makes the calls
  a model would ask for.

Output: The Tool List
~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/listings/mcp_tools.txt
   :language: text

A real run of the MCP client against ARIAC, on 2026-10-17. No model runs.
Recording 2 of 2; recording 1 used a client that printed 3 lines per result.

Output: Three Calls
~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/listings/mcp_calls.txt
   :language: text

A real run of the MCP client against ARIAC, on 2026-10-17. No model runs.
Recording 2 of 2; recording 1 used a client that printed 3 lines per result.

Reading the Tool List and the Calls
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. The server lists the ten L8 tools. A tool with arguments shows one line
   per argument.
2. MCP wrote each schema from the type hints: ``Literal[1, 2]`` became an
   integer ``enum``. The Gemini declarations use ``minimum`` and ``maximum``
   instead, because Gemini's ``parameters`` schema allows ``enum`` for strings
   only.
3. ``read_testers`` returns both testers: 0.024 V and −0.005 V, both
   ``OPERATIONAL``. Both are below 0.5 V, so both are empty.
4. ``robot2_move_home`` ran and parked robot 2: ``SUCCESS``, holding
   ``NOTHING``. The tool ran, so ``is_error`` is ``False``.
5. AGV 4 fails the server's own argument check ("Input should be 1, 2 or
   3"), so the tool never ran and ``is_error`` is ``True``.

Raw ROS Access, and the GP4 Choice
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`ros-mcp-server <https://github.com/robotmcp/ros-mcp-server>`_ connects to a
robot through rosbridge. It lets an LLM publish and subscribe to topics, call
services and actions, and set parameters. It gives an LLM wide access to the
robot system.

For GP4:

- Task-level tools behind the executor's guards are safer than raw publish
  access to ROS topics.
- Each team chooses whether to use MCP. The tool schemas are the same either
  way; MCP changes only how the tools reach the agent.


.. _l8-context-cost-latency:

Context, Cost and Latency
-------------------------

This section covers what goes in the agent's context, how input tokens and
cost grow with the number of loop steps, and latency against the factory's
clocks.

What Goes in the Agent's Context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

L3's idea 1 from 4D/RCS: each layer keeps only the detail it decides with. The
agent sits in the deliberative layer.

.. list-table::
   :header-rows: 1
   :widths: 50 50
   :class: compact-table

   * - **In the agent's context**
     - **Left out**
   * - Orders and the high-priority order ID
     - Joint positions and gripper width
   * - Kits: the cells in each slot and their voltages
     - Raw lidar points and camera images
   * - Cell results: passed or failed, in range or not
     - Tray slot frames from TF2
   * - Station states: AGV stations, tester and conveyor status
     - Tester readings before they are averaged

.. tip::

   A smaller context costs fewer tokens and gives the model less to misread.

Measuring F and h in Run 1
~~~~~~~~~~~~~~~~~~~~~~~~~~

Symbols:

- :math:`F`: the tokens sent on every call: the system message, the tool
  list, the goal, the first observation and the record. ``FIXED`` in
  ``token_growth.py``.
- :math:`h`: the tokens each earlier step adds: the model's call, then its
  result with the new observation and the record. ``PER_STEP`` in
  ``token_growth.py``.

The arithmetic, from Run 1's token counts:

1. Call 1 sends no history, so :math:`F` is call 1's input: :math:`F` = 1264
   tokens (``outputs/agent_run1_usage.json``).
2. Call 5 sent 2309 tokens: 2309 − 1264 = 1045 tokens more than call 1.
3. Call 5 carries 4 earlier steps: 1045 / 4 = 261.25, rounded to :math:`h` =
   261 tokens.
4. Output per call: 79 tokens over 5 calls is 15.8, rounded to 16 tokens
   (``OUT``).

Why the Input Grows with Each Step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Symbols:

- :math:`F` = 1264 and :math:`h` = 261 tokens, measured in Run 1 (above).
- :math:`n`: the number of steps in a ReAct run, one call per step.

The arithmetic:

1. Call :math:`k` sends :math:`F` plus the :math:`k - 1` earlier steps:
   :math:`F + (k - 1)\,h` tokens.
2. A call 20 would send 1264 + 19 × 261 = 1264 + 4959 = 6223 tokens.
3. Over :math:`n` calls: :math:`nF + h\,n(n - 1)/2`. For :math:`n` = 20:
   20 × 1264 + 261 × 20 × 19 / 2 = 25,280 + 49,590 = 74,870 tokens.
4. The :math:`n(n - 1)/2` term grows with the square of :math:`n`: twice the
   steps gives about four times the history.

Input Tokens over a Run
~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l8/token_growth.svg
   :alt: A plot. The x axis is the number of steps in the run, 0 to 40; the y axis is the total input tokens over the run, in thousands, 0 to 300. A solid curve for ReAct rises faster and faster, with dots at 10 steps (24,385), 20 steps (74,870) and 40 steps (254,140). A dashed line for plan-and-execute with one replan stays flat near the x axis.
   :width: 80%
   :align: center

   Total input tokens over a run, against the number of steps, with
   :math:`F` and :math:`h` measured in Run 1.

- This is a graph of token counts, not a picture of the factory.
- ReAct: the formula above, with :math:`F` and :math:`h` from Run 1.
- Plan-and-execute: one plan and one replan, each sending :math:`F` = 1264
  tokens, so 2 × 1264 = 2528 tokens for any :math:`n`. A replan sends the
  current state, not the history. Its output, 40 tokens per plan step
  (``PLAN_OUT``), is chosen: no plan-and-execute run was recorded.
- The values come from ``lecture8/code/token_growth.py``.

The Cost of Run 1
~~~~~~~~~~~~~~~~~

Output of ``lecture8/code/run_cost.py``, from Run 1's raw API responses:

.. literalinclude:: outputs/listings/run1_cost.txt
   :language: text

Recorded once, on 2026-10-17, with gemini-3.5-flash-lite. A rerun gives
different answers. ``billed``: output plus thinking tokens (none in Run 1).
``wall s``: each call's time, measured by the client.

The arithmetic, at the prices of ``gemini_prices.py``:

1. Input: 8941 × 0.30 / 1,000,000 = $0.0026823.
2. Output: 79 × 2.50 / 1,000,000 = $0.0001975.
3. Run 1: $0.0026823 + $0.0001975 = $0.0028798, shown as 0.002880.

The Cost Table: A Straight-Line Model of Run 1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Output of ``lecture8/code/token_growth.py``:

.. literalinclude:: outputs/listings/token_growth.txt
   :language: text

Each row is computed from :math:`F`, :math:`h` and 16 output tokens per call,
not run. At 5 steps the model gives 8930 tokens in and 80 out; Run 1
measured 8941 in and 79 out. Where the 11 tokens come from:

1. Run 1's four steps added 271, 253, 257 and 264 tokens: 10 more, 8 less,
   4 less and 3 more than :math:`h` = 261.
2. Calls 2 to 5 send step 1 again 4 times, step 2 three times, step 3 twice,
   step 4 once.
3. 4 × 10 = 40 more, 3 × 8 = 24 less, 2 × 4 = 8 less, 1 × 3 = 3 more:
   40 − 24 − 8 + 3 = 11 tokens more than the model.

Reading the Cost Table, and Keeping the History Short
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. ReAct, 20 steps: 74,870 × 0.30 / 1,000,000 = $0.022461 for input, plus
   320 × 2.50 / 1,000,000 = $0.0008 for output: $0.023261, shown as 0.0233.
2. From 20 to 40 steps the ReAct cost goes from $0.0233 to $0.0778, about
   3.3 times, because the history term grows with the square of the steps.
3. Plan-and-execute stays under $0.01 at every length in the table.

Keeping the history short:

- Summarize old steps instead of sending each one again. The current state
  read from ROS is the truth, not the history.
- Memory across runs, such as "tester 2 often malfunctions in this trial",
  should be small, written by code, and checked against the current state.

**In GP4:** read token counts from the API's ``usage`` fields and prices from
the provider's page on the day. GP4 reports cost and latency per trial.

Latency Against the Factory's Clocks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Latency** is the time from sending a call to getting its answer.

ARIAC's clocks:

- The trial's time limit (``TIME_LIMIT`` in the trial file).
- A nominal 150 s for the high-priority order's speed bonus, and a nominal
  4 s for inspection reports (``NOMINAL_HIGH_PRIORITY_EXECUTION_DURATION``
  and ``NOMINAL_INSPECTION_TIME`` in ``scoring_weights.yaml``; the ARIAC
  scoring page says these targets can change).

Two kinds of time:

- ARIAC's clocks count simulation time; a model call takes wall-clock time.
  Gazebo ran at about 0.37 times real time in the course's skills container
  on the instructor's Lenovo (measured).
- So the same model latency costs a different amount of simulation time on
  each machine. Each team measures its own model's latency instead of
  assuming it.


.. _l8-next-class:

Next Class
----------

**L9: LLM Agents II: VLM Grounding and Agentic Replanning (Wednesday, March
31)**

- A VLM describes the camera images for the agent, the loop closes around
  feedback for replanning, and the class compares the PDDL planner and the
  agent on the same trial.
- Quiz 4 at the start of class covers L7 and L8. GP3 is due, and GP4 is
  posted.

**Before next class:**

- Set up LLM access (a free-tier Gemini API key or a local open-weight
  model, as the course's :doc:`AI Access </ariac/ai_setup>` page describes).
- Run the offline L8 scripts in ``lecture8/code/``: ``validator.py`` and
  ``token_growth.py`` print the tables above, and
  ``python3 orchestrator.py --fake --runs 2`` runs the loop without ARIAC.
  The ARIAC and Gemini demos need the course container (see the
  :doc:`code page <l8_code>`).
- Finish GP3: the executor and the replanning demo.
