====================================================
Lecture
====================================================

.. note::

   These notes follow the L3 slides shown in class, in the same order and
   with the same sections, so you can read them at home. Every program output
   below comes from running the three L3 programs, ``kit_views.py``,
   ``ontology_check.py`` and ``track_cell.py``, with Python 3.12.3 and
   ``jsonschema`` 4.10.3. The programs and how to run them are on the
   :doc:`code page <l3_code>`.

.. admonition:: Class logistics for this week
   :class: warning

   - **Team charters** were due before class.
   - **Quiz 1** is next week, at the start of class, on L1 to L3.


.. _l3-recap:

Recap
-----

**From L2.**

- Three layers: deliberative, executive, reactive.
- An LLM agent goes in the deliberative layer; a VLM goes in perception.
- Between the layers: ROS 2 actions, blackboard keys, and plans or agent
  decisions.

**This lecture.** What crosses those interfaces: a representation of the
world, the task and the robot.

**Team charters.** Charters were due before class. The ownership list in your
charter (a primary and a backup for each part) is what peer review is read
against.


.. _l3-why:

The Shared World Model
----------------------

This section covers a world model and the programs that read it.

Knowledge Representation and the World Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: knowledge representation and world model
   :class: note

   **Knowledge representation** is how a system writes down what it knows
   about the world, the task and itself, in a form programs can read and
   check. The written-down result is the system's **world model**: the facts
   it holds now, such as which cell sits in which tray slot.

**Where the facts come from in ARIAC.**

- ARIAC sends some facts on its topics: the AGV station, the four slot flags
  of each tray, each tester's voltage.
- Your system works out the rest: which cell is on which tester, which cells
  are good, which cells fit one kit.
- Both kinds go into one world model, and every part of your system reads
  that model.

The Readers of the World Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 22 56 22
   :class: compact-table

   * - **Reader**
     - **What it needs**
     - **Where**
   * - PDDL planner
     - Typed objects and true or false facts
     - GP3
   * - LLM agent
     - Text in; output that matches a JSON schema
     - GP4
   * - Executor
     - Typed action arguments: which robot, which tester, which AGV, which
       slot
     - GP1 on

- In this lecture, the **executor** is the part that runs actions: from GP1
  on, your behavior tree and the skills it calls.
- It is not a ROS 2 executor from L1, which runs a node's callbacks.
- **JSON** is a text format for data, and a **JSON schema** is a set of rules
  a JSON record must follow. View 2 of the example kit shows both.
- Each reader needs the same facts in a different form.

What Goes Wrong Without a Shared Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. The planner's copy says slot 2 of AGV 1 is empty, while
   ``/agv1/tray_status`` (``AgvTrayStatus.msg``) says it is full. The plan
   sends a cell to a full slot.
2. The agent names ``voltage_tester_3``. ARIAC 2025 has two testers, so the
   skill call names a tester that does not exist.
3. A cell's voltage is stored in one place and its inspection result in
   another, and the two disagree: one copy says a cell is good after the
   other copy recycled it.

.. important::

   Each case has two copies of one fact and nothing that keeps them equal.

Questions for the ARIAC World Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. What does it describe: objects, relations, events?
2. Who writes it, and who reads it?
3. How is it kept true as the factory changes?

Frames describe the objects, an ontology the relations, and a world model at
each layer who writes and reads each fact.


.. _l3-frames:

Frames
------

This section covers slots, fillers, defaults and inheritance, applied to
cells, kits, modules and AGVs.

What a Frame Is
~~~~~~~~~~~~~~~

.. admonition:: Definition: frame (Minsky, 1974)
   :class: note

   - A **frame** describes a kind of object as a set of named **slots**
     (Minsky calls them terminals).
   - Each slot holds a **filler**: a value, or a link to another frame.
   - A frame's slots start with **default** fillers, which new information
     can replace.

**Inheritance.** A more specific frame takes the slots of a general one. This
idea comes from the frame systems built after Minsky's memo; the memo itself
says the frames of a system share the same terminals.

Source: M. Minsky,
`A Framework for Representing Knowledge
<https://www.mit.edu/~dxh/marvin/web.media.mit.edu/~minsky/papers/Frames/frames.html>`_,
MIT AI Laboratory Memo 306, June 1974.


From a General Frame to a Cell
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l3/frames.svg
   :alt: Three columns of boxes. Tag 1, left, in teal: the general frame Cell with five empty slots: type, nominal_voltage, measured_voltage, inspection and location. Tag 2, middle, in teal: two more specific frames, LiIonCell with type = LI_ION and nominal_voltage = 3.6 V, and NiMHCell with type = NIMH and nominal_voltage = 1.2 V; a solid arrow goes from each to Cell. Tag 3, right, in magenta: the cell c1, with type = LI_ION, nominal_voltage = 3.6 V, measured_voltage = 3.55 V, inspection = passed and location = agv1, slot 1; a dashed arrow goes from c1 to LiIonCell.
   :width: 100%
   :align: center

   Tag 1: the general frame ``Cell``, slots empty. Tag 2: two more specific
   frames; each fills ``type`` and gives ``nominal_voltage`` its default.
   Tag 3: the cell ``c1`` from the example kit. Solid arrow: takes
   every slot of. Dashed arrow: is one instance of. Teal: a frame. Magenta:
   an instance.

``c1`` gets its first two fillers from ``LiIonCell``; your system fills the
last three.


A Cell Frame, Slot by Slot
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 44 36
   :class: compact-table

   * - **Slot**
     - **Filler**
     - **Who fills it**
   * - type
     - ``LI_ION`` or ``NIMH``
     - Your feed request (``ControlCellFeeder.srv``; values in
       ``CellTypes.msg``)
   * - nominal_voltage
     - Default from the type: 3.6 V or 1.2 V
     - ``CellTypes.msg``
   * - measured_voltage
     - Filled only after the tester readings are averaged
     - Your team
   * - inspection
     - Passed or not; each defect's type, angle θ around the cell and height
       z from its base
     - Your team (GP2, lidar); format: ``InspectionReport.msg``,
       ``CellDefect.msg``
   * - location
     - Conveyor, tester 1 or 2, gripper, tray slot, recycling bin or
       inspection bin
     - Your team

- ARIAC never sends your team an inspection result. Your team decides it
  from lidar and submits it with ``SubmitInspectionReport.srv``.
- The tolerances, plus or minus 0.2 V per cell and 0.15 V per kit
  (``CellTypes.msg``), are stored once, in the class.


Kit, Module, AGV and Order Frames
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80
   :class: compact-table

   * - **Frame**
     - **Slots**
   * - Kit
     - cell_type; agv (1 to 3); four slots, each a link to a cell frame;
       total_voltage (computed); window (4 × nominal plus or minus 0.15 V);
       status (building, checked, shipped, rejected)
   * - Module
     - bottom shell, top shell, four cells, welds (six: four on top, two on
       the bottom), flipped or not
   * - AGV
     - station (``INSPECTION``, ``ASSEMBLY``, ``SHIPPING``, ``RECYCLING``,
       or ``IN_TRANSIT`` while it moves; ``AgvStations.msg``); four slot
       occupancy flags (``AgvTrayStatus.msg``)
   * - High-priority order
     - an ID string (``HighPriorityOrder.msg``); the time it was announced;
       the fact that it needs a Ni-MH kit

.. tip::

   Many slots match ARIAC message fields: start from the message definitions
   when you list a frame's slots.


.. _l3-kit-frame:

Worked Example: Filling the Kit Frame
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Chosen for this example.** A Li-Ion kit on AGV 1. Slots 1 to 3 link to
cells ``c1``, ``c2`` and ``c3``, measured at 3.55 V, 3.62 V and 3.70 V. Slot 4
is empty.

**The other slots, step by step.**

1. ``total_voltage`` is computed from the linked cells:
   3.55 + 3.62 + 3.70 = 10.87 V.
2. ``window`` is computed from the class: 4 × 3.6 = 14.40 V, so
   14.40 − 0.15 = 14.25 V to 14.40 + 0.15 = 14.55 V.
3. ``status`` keeps its default, building, until the kit is checked.

.. important::

   Only the measured voltages are stored per cell. The total and the window
   are computed from them and from the class, so neither can disagree with
   the cells.


.. _l3-ontologies:

Ontologies
----------

This section covers classes, relations and instances, and which statements
about the factory they accept.

An ARIAC Ontology Sketch
~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: ontology
   :class: note

   An **ontology** defines

   - the **classes** in a domain, the **relations** between them, and the
     **instances** that exist now;
   - so software can check that a statement makes sense: a cell can be in a
     slot; an AGV cannot.

.. list-table::
   :widths: 16 84
   :class: compact-table

   * - **Classes**
     - Robot (InspectionRobot, AssemblyRobot, GantryWelder), AGV, Slot,
       Station, Cell (LiIonCell, NiMHCell), Kit, Module, Shell, Tester,
       Sensor (BreakBeam, DistanceSensor, Camera, Lidar)
   * - **Relations**
     - inSlot(Cell, AGV, Slot), atStation(AGV, Station), canReach(Robot,
       Place), testedBy(Cell, Tester), partOf(Cell, Kit)
   * - **Instances**
     - ``inspection_robot_1``, ``agv1``, ``voltage_tester_2``, and each cell
       as it arrives

A name in brackets is a kind of the class before it: a LiIonCell is a Cell.


Part of the Sketch as a Graph
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l3/ontology.svg
   :alt: A graph of the ARIAC ontology sketch. Teal class boxes: LiIonCell and NiMHCell on the left, each with a solid arrow to Cell in the middle. A magenta instance box, c1, sits between them, with a dashed arrow up to LiIonCell. Three gray relation boxes leave Cell: inSlot, with arrows to AGV and to Slot; testedBy, with an arrow to Tester; and partOf, with an arrow to Kit. At the top right, AGV connects to a gray relation box, atStation, with an arrow down to Station. A magenta instance box, inspection, has a dashed arrow up to Station.
   :width: 100%
   :align: center

   Teal: a class. Gray: a relation; its line starts at its first argument and
   its arrows point to the others, in order. Magenta: an instance. Solid
   arrow between classes: is a kind of. Dashed arrow: is one instance of.
   Same colors and arrows as the frame figure.


.. _l3-ontology-check:

Worked Example: Checking Six Statements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ontology_check.py`` holds the sketch as three Python dictionaries (classes
and their parents, relations and the class of each argument, instances and
their class) and checks six statements. The cells and the kit are named for
this example; the robot, AGV and tester names are ARIAC's.

.. literalinclude:: outputs/ontology_check.txt
   :language: text
   :caption: lecture3/outputs/ontology_check.txt

1. ``c1`` is a LiIonCell, and a LiIonCell is a kind of Cell, so inSlot
   accepts it. The ontology uses inheritance, as frames do.
2. Each rejection names the argument and the class the relation needed.


From Perception to Planning: One Dented Cell
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Perception** produces instances and facts: your GP2 lidar detector finds
   a dent on cell ``c7`` at an angle θ and a height z.
2. **The ontology's rule**: a cell with a defect fails inspection, so it must
   not go in a kit.
3. **Your system acts on it**: it submits an ``InspectionReport.msg`` with
   ``passed`` false and the dent in ``defects``. The inspection door stays
   closed for ``c7``, and the cell goes into the inspection bin.
4. **The planner** uses the result: ``c7`` never reaches a tray, so the kit
   needs another cell.

ARIAC's reply to a failing report: "Failing inspection report received. Door
will remain closed for cell." (``physical_inspection_plugin.cpp``, branch
``ariac2025``).


Where Ontologies Are Standardized
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- IEEE 1872-2015, *IEEE Standard Ontologies for Robotics and Automation*,
  defines a core ontology called **CORA**. IEEE made it inactive (reserved)
  on 2026-03-26 and is drafting a revision, P1872.
- The W3C Web Ontology Language (`OWL <https://www.w3.org/OWL/>`_) is a
  standard language for writing ontologies.
- The course does not require either.

.. important::

   In this course, your ontology is written in code: the message types, the
   PDDL types of GP3, and the JSON schema of GP4 each define which values and
   statements are valid.


.. _l3-world-model:

A World Model at Each Layer
---------------------------

This section takes two ideas from NIST's 4D/RCS reference model and uses
them inside the three-layer architecture from L2.

Source: J. Albus et al., *4D/RCS: A Reference Model Architecture for Unmanned
Vehicle Systems, Version 2.0*, NISTIR 6910, 2002
(`doi.org/10.6028/NIST.IR.6910 <https://doi.org/10.6028/NIST.IR.6910>`_).

What 4D/RCS Is
~~~~~~~~~~~~~~

.. admonition:: From NISTIR 6910
   :class: note

   "4D/RCS is a methodology for conceptualizing, designing, engineering,
   integrating, and testing intelligent systems software for vehicle systems
   with any degree of autonomy" (p. 9). "The 4D/RCS is a hybrid
   architecture, with both deliberative (reasoning and planning) and reactive
   (rapid response to exigencies) capabilities" (p. 16).

- NIST prepared it for the Army Research Laboratory's Demo III program
  (title page). It is derived from NIST's earlier RCS architecture (p. 12).
- It is a hierarchy of levels. "At every level, sensory processing and
  behavior generation processes have access to a model of the world that is
  resident in a knowledge database" (p. 16).
- The course keeps L2's three layers and takes two ideas from 4D/RCS.

Idea 1: Each Layer Keeps Only the Detail It Decides With
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: From NISTIR 6910
   :class: note

   "At no level does a node have to cope with both broad scope and high level
   of detail" (p. 31). "The world model in any node is rich and detailed
   within the region of attention, but contains only the amount of
   resolution in space and time required for making decisions in that node"
   (p. 55).

- A **node** is one unit of the 4D/RCS hierarchy, at one level, with its own
  world model. In this course, read it as one layer.
- At the top, the planner sees the whole order but no single tester reading.
- At the bottom, a controller sees joint positions but not the order.


.. _l3-layer-models:

Idea 1 in ARIAC: Each Layer's Model at One Moment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l3/layer_models.svg
   :alt: Three rows, one per layer, each a colored label on the left and a panel on the right. Blue, Deliberative (planner, agent): kit on agv1: c1, c2, c3 placed; slot 4 open; c4 is good; agv1 is at INSPECTION; no poses, no single readings. Amber, Executive (GP1 tree): /tester1/cell = c4, /tester1/voltage = 3.599, /kit/slots_filled = 3, /kit/total = 10.87. Green, Reactive (skills, ARIAC): joint positions of inspection robot 2, gripper width, TF2 frame of agv1's tray slot 4.
   :width: 100%
   :align: center

   The moment: ``c1`` to ``c3`` are on the tray (10.87 V), and ``c4`` has just
   been averaged on tester 1 at 3.599 V (the :ref:`GP1 worked example
   <l3-track-cell>`). Blue, amber and green: the layers, as in L2.

.. admonition:: Definition: blackboard
   :class: note

   The executive's model is the **blackboard**: a shared key-value store
   that every leaf of a ``py_trees`` behavior tree can read and write (L4).
   The key names in the figure follow L4.


Idea 2: Handle Errors Where They Are Seen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: From NISTIR 6910
   :class: note

   Commands flow down the hierarchy, and status feedback flows up (p. 19,
   Figure 1). An executor that "senses an error between its output
   CommandGoal and the predicted state … may react by modifying the
   commanded action so as to cope with that error" (p. 45).

**In ARIAC, in order.**

1. A skill that loses a grasp stops and returns a failure reason. It never
   retries the task itself: the skill's part is to stop safely and report.
2. The behavior tree reads that reason, then retries the skill or tries
   another branch.
3. Only when the tree cannot finish the kit, or the status shows that the plan
   assumes something false (tester 1 down), does the planner or the agent make
   a new plan.

- L2's toy factory showed this order: the executive moved cell 3 from tester
  1 to tester 2 by itself. Only the status moved up to the planner (cell 3
  reads 3.60 V; tester 1 is down); the −1 V readings stayed in the executive.
- L11 builds recovery on this order: local recovery first, then global.


The Design Rule, and What We Leave Out
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. important::

   **Design rule for the projects.**

   - Put each fact in the lowest layer that needs it.
   - Pass up only what the layer above decides with.
   - L8 uses the same rule for what goes into an LLM agent's context.

**What the course does not take from 4D/RCS.** Its eight levels (servo,
primitive, subsystem, vehicle, section, platoon, company, battalion; Table 1,
p. 55) are sized for a military vehicle hierarchy, with plans from 50 ms at
the servo level to 24 h at the battalion level. ARIAC needs no platoon or
battalion levels, so the course keeps L2's three layers.


.. _l3-three-views:

Three Views of a Kit
--------------------

One kit state, written for the planner, for the agent, and for a prompt. It
is the kit from the kit frame example:

- AGV 1 at the inspection station;
- a Li-Ion kit;
- slots 1 to 3 holding cells measured at 3.55 V, 3.62 V and 3.70 V;
- slot 4 empty.

The outputs in this section come from ``kit_views.py``. In the
script the kit is one Python dictionary:

.. literalinclude:: code/kit_views.py
   :language: python
   :lines: 19-29
   :caption: lecture3/code/kit_views.py (excerpt)

The Three Views and Their Readers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l3/three_views.svg
   :alt: Left, a gray box: one kit state, agv1 at INSPECTION, Li-Ion, drawn as four slots holding 3.55 V, 3.62 V, 3.70 V and empty. Three arrows lead from it to three gray boxes in the middle, each with one sample line. Tag 1: PDDL facts, sample line (in-slot c1 agv1 s1). Tag 2: JSON record, sample line with "agv": 1. Tag 3: Text, sample line AGV 1 is at the .... An arrow leads from each to a blue box on the right: GP3 planner, GP4 agent and LLM prompt.
   :width: 100%
   :align: center

   Tags 1 to 3: the three views ``kit_views.py`` prints, each with one sample
   line. Blue: the deliberative layer, as in L2.

One program writes all three views from one Python dictionary, so the three
views hold the same facts.


View 1: PDDL Facts for the GP3 Planner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: PDDL fact
   :class: note

   PDDL (the Planning Domain Definition Language, L6) writes a state as a
   list of facts. A **fact** is a predicate and its objects:
   ``(in-slot c1 agv1 s1)`` says that cell ``c1`` is in slot ``s1`` of
   ``agv1``. A fact that is not listed is false.

.. literalinclude:: outputs/kit_views.txt
   :language: text
   :lines: 2-9

- ``(passed cN)`` is inferred: a cell on the tray got through the inspection door, so its report passed.
- The names are examples; your team chooses its own in GP3.


.. _l3-json-record:

View 2: The JSON Record for the GP4 Agent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: JSON and a JSON record
   :class: note

   **JSON** (JavaScript Object Notation) is a text format for data: objects
   in braces with named fields, lists in brackets, numbers, strings,
   ``true``, ``false`` and ``null``. A **JSON record** here is one object that
   holds the whole kit state.

``kit_views.py`` writes the record to ``kit_record.json``, reads it back and
checks it:

.. literalinclude:: outputs/kit_record.json
   :language: json
   :caption: lecture3/outputs/kit_record.json

- ``json.dumps`` writes 3.70 as 3.7: a number keeps no trailing zero.
- ``null``: slot 4 holds no cell.


View 2: A JSON Schema Says Which Records Are Valid
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: JSON schema and validator
   :class: note

   A **JSON schema** is a JSON document that states the rules a record must
   follow: the fields it needs, the type of each, the allowed values. A
   **validator** checks a record against the schema and lists every rule the
   record breaks.

.. literalinclude:: code/kit_views.py
   :language: python
   :lines: 31-64
   :caption: lecture3/code/kit_views.py (excerpt)

- ``IN_TRANSIT`` is left out of ``station`` on purpose: a record for a moving
  AGV is rejected.
- Each of the four slot items needs a ``slot`` number from 1 to 4 and a
  ``cell``. ``CELL`` allows an object with an ``id`` and a ``voltage``, or
  ``null``.
- Keywords used: ``type``, ``properties``, ``required``, ``enum``,
  ``minimum``, ``maximum``, ``minItems``, ``maxItems``.


Checking the Record and Two Bad Copies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The script checks three records: the record read back from
``kit_record.json``, a copy that names AGV 5, and a copy with a fifth slot
added.

.. literalinclude:: code/kit_views.py
   :language: python
   :lines: 108-117
   :caption: lecture3/code/kit_views.py (excerpt)

.. literalinclude:: outputs/kit_views.txt
   :language: text
   :lines: 16-21

**How to read an error line.** Each line is ``path: rule value``. The path
names the field from the top of the record; list items count from 0. So
``slots.4.slot`` is the ``slot`` field of the fifth item of ``slots``.

**The three records.**

1. The record read back from ``kit_record.json`` passes every rule.
2. AGV 5 breaks one rule: ``agv`` must be at most 3, because ARIAC 2025 has
   three AGVs.
3. A fifth slot breaks two rules at once: the list has more than 4 items
   (``maxItems``), and the new item's ``slot`` number is above 4.

.. important::

   An LLM agent can return a record like the last two. Your code checks each
   record against the schema before any robot moves (L8).


View 3: Text for a Prompt
~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: outputs/kit_views.txt
   :language: text
   :lines: 11-13

- An LLM reads text, so the agent's prompt describes the kit in words.
- In GP4, a VLM also describes a camera image in words. Your code checks that
  description against this text (L9).
- The text drops the cell IDs, so your code checks the record of View 2
  instead.


.. _l3-fourth-cell:

Worked Example: The Voltage Range for the Fourth Cell
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. The three cells total 3.55 + 3.62 + 3.70 = 10.87 V.
2. The Li-Ion kit window is 14.25 V to 14.55 V (the kit frame's ``window``,
   from L1).
3. The fourth cell must be between 14.25 − 10.87 = 3.38 V and
   14.55 − 10.87 = 3.68 V.
4. A single cell must be 3.6 V plus or minus 0.2 V (``CellTypes.msg``):
   3.40 V to 3.80 V. So the fourth cell must be from 3.40 V to 3.68 V.
5. A cell at 3.75 V passes on its own, but it would put the kit at
   10.87 + 3.75 = 14.62 V, outside the window.

**The program's output.**

.. literalinclude:: outputs/kit_views.txt
   :language: text
   :lines: 22-23

.. important::

   This decision uses each cell's measured voltage, so the representation
   must keep it. PDDL facts are true or false (View 1), so GP3 picks the cells
   in a separate step (L6).


.. _l3-chance:

Worked Example: How Far Chance Moves the Answer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ARIAC checks the kit with the true voltage stored with each cell
  (``validate_kit()`` in ``agv_tray_interface_plugin.cpp``). Your team knows
  only averages of tester readings.
- Each reading has noise with a standard deviation of 0.05 V
  (``voltage_tester/model.sdf``). Each average uses five readings, as L4's
  ``wait_for_voltage`` collects.

1. One average wanders by about 0.05 / √5 = 0.0224 V.
2. A sum of n averages wanders by √n times that: about √3 × 0.0224 = 0.039 V
   for the three placed cells, and √4 × 0.0224 = 0.045 V for a full kit.

.. literalinclude:: outputs/kit_views.txt
   :language: text
   :lines: 24-27

**The verdicts, checked against chance.**

3. With a 3.75 V cell, the averages total 14.62 V: 14.62 − 14.55 = 0.07 V over
   the window. A **spread** here is how far chance moves the number:
   0.0447 V for a full kit. So 0.07 / 0.0447 = 1.57, about 1.6 spreads.
4. If the true total were exactly 14.55 V, the averages would still read
   14.62 V or more about 6 times in 100 (5.9% by the normal formula). So a
   failed kit is likely but not certain. Keep the 3.75 V cell out of this
   kit.
5. A fourth cell that reads 3.68 V puts the averages at exactly 14.55 V. For
   a total within about 2 × 0.045 = 0.09 V of an edge, chance alone can put
   the true total on either side (L4).

.. literalinclude:: outputs/kit_views.txt
   :language: text
   :lines: 28-29

**Keep a margin inside the window.** The margins are twice what chance moves
each number; the factor 2 is chosen for this example.

1. Kit margin: 2 × 0.045 = 0.09 V. Cell margin: 2 × 0.0224 = 0.04 V
   (rounded).
2. Low end: the larger of 14.25 + 0.09 − 10.87 = 3.47 V and
   3.40 + 0.04 = 3.44 V, so 3.47 V.
3. High end: the smaller of 14.55 − 0.09 − 10.87 = 3.59 V and
   3.80 − 0.04 = 3.76 V, so 3.59 V.

.. literalinclude:: outputs/kit_views.txt
   :language: text
   :lines: 30-31

.. important::

   To set a margin, the world model must keep each average and the number of
   readings behind it.


.. _l3-gp1:

What the GP1 Tree Must Know
---------------------------

Observed, Inferred and Unknown
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 16 84
   :class: compact-table

   * - **Kind**
     - **Examples in Task 1**
   * - Observed
     - From ARIAC topics and service replies: competition state, conveyor and
       tester status, tester voltage, AGV station, slot occupancy,
       high-priority order IDs
   * - Inferred
     - From your team's reasoning: this cell is the one the break beam saw at
       that time; its averaged voltage is in range; the kit total is in the
       window
   * - Unknown
     - Where each cell is: ARIAC publishes no frames or pose topics for
       individual cells or shells

.. admonition:: Track every cell yourself
   :class: warning

   Your system must track each cell itself, from events: the beam time, the
   tester reading, the skill result. If your system loses track of a cell, no
   ARIAC topic gives its position.


.. _l3-track-cell:

Worked Example: Tracking Cell c4 from Events
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``track_cell.py`` feeds stand-ins for ARIAC messages to a small world
model and prints each change. The step names follow L4's starter tree, and the
keys follow L4's blackboard table. Chosen for this example: ``c4`` at 3.58 V,
seed 91. Each average uses five readings, as L4's ``wait_for_voltage``
collects; the 0.05 V reading noise is ARIAC's. The kit is the example kit,
with ``c1`` to ``c3`` already placed.

.. literalinclude:: outputs/track_cell.txt
   :language: text
   :caption: lecture3/outputs/track_cell.txt

Only the readings and the beam event are observed; which cell each event
belongs to is inferred, and the inspection value is your team's own report.

**Applying GP1's rule to c4.** GP1, Task 4: "Before placing a cell inside that
range, check that the four-cell total can still land in 14.25 V to 14.55 V. If
it cannot, recycle the cell."

1. ``c4`` averages 3.599 V, inside 3.40 V to 3.80 V, so GP1's check applies.
2. On the averages, the total is 10.87 + 3.599 = 14.469 V, inside
   14.25 V to 14.55 V. It is 14.55 − 14.469 = 0.081 V below the top edge.
3. But 0.081 V is under the 0.09 V kit margin: chance alone can put a total
   that close to an edge on either side (L4). The same check on the cell:
   3.599 V is 0.009 V over the 3.59 V limit, less than one spread of a single
   average (0.0224 V).
4. So for ``c4``, chance alone could make GP1's check give the wrong answer.
   Cells lock to the tray once placed, so the tree recycles ``c4``, as L4
   does with the 3.75 V cell. Slot 4 stays open.

.. important::

   The cost: ``c4``'s true voltage, 3.58 V, would have fit
   (10.87 + 3.58 = 14.45 V, if ``c1`` to ``c3`` read true).


Where GP1 Stores Its World Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- On the ``py_trees`` blackboard (L4): a small set of named keys, such as the
  cell on each tester, the averaged voltages, the slots filled and the kit
  total so far.
- Decide the key names and types now, and give each key an owner in your
  charter.

**Later in the semester.**

- GP3's planner reads the same kit as facts.
- GP4's agent reads it as a record checked by a JSON schema.
- The final demo's recovery logic updates it when a cell fails inspection or
  a tester stops giving valid readings.


Next Class
----------

**Quiz 1** (Wednesday, February 17, start of class): closed notes, on
ELMS-Canvas or paper, covering L1 to L3. Review the ARIAC 2025 tasks,
challenges and how ARIAC scores a run; QoS, executors, actions and TF2 and
their demo results; the classical and three-layer architectures and AI in the
three layers; frames, ontologies, the two 4D/RCS ideas and the three views of a
kit.

**L4: Behavior Trees for Task Execution.** Behavior trees for the executive
layer, which read and write the blackboard. After L4, your team writes the GP1 tree.

**Before next class.**

- Run ``kit_views.py``, ``ontology_check.py`` and ``track_cell.py``, and
  compare your output with these notes.
- List the facts your GP1 tree must track, and agree on the blackboard key
  names and types.
