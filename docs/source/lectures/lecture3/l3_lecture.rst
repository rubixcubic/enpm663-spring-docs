====================================================
Lecture
====================================================

.. note::

   These notes follow the L3 slides shown in class, in the same order and
   with the same sections, so you can read them at home. Every program output
   below comes from running ``kit_views.py`` with Python 3.12.3 and
   ``jsonschema`` 4.10.3. The script and how to run it are on the
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
- Every boundary between layers is an interface.

**Today's question.** What exactly crosses those interfaces? A
representation of the world, the task and the robot.

**Team charters.** Charters were due before class. The ownership list in your
charter (a primary and a backup for each part) is what peer review is read
against.


.. _l3-why:

Why Representation Matters
--------------------------

.. admonition:: Definition: knowledge representation
   :class: note

   **Knowledge representation** is how a system writes down what it knows
   about the world, the task and itself, in a form programs can read and
   check. The written-down result is the system's **world model**.

The idea of this section: one world model, several programs that read it,
each in its own form.

Three Readers of One World Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

**What goes wrong without a shared model.**

- The planner believes slot 2 is empty while the tray status says it is full.
- The agent names a tester the skill does not accept.
- A cell's voltage is stored in one place and its inspection result in
  another, and the two drift apart.

Three Questions to Ask of Any Representation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. What does it describe: objects, relations, events?
2. Who writes it, and who reads it?
3. How is it kept true as the factory changes?

The rest of the lecture answers these questions for the ARIAC factory: frames
for the objects, an ontology for the relations, and a world model at each
layer.


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


A Cell Frame
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 22 52 26
   :class: compact-table

   * - **Slot**
     - **Filler**
     - **From**
   * - type
     - ``LI_ION`` or ``NIMH``
     - ``CellTypes.msg``
   * - nominal_voltage
     - Default from the type: 3.6 V or 1.2 V
     - ``CellTypes.msg``
   * - measured_voltage
     - Filled only after the tester readings are averaged
     - Your team
   * - inspection
     - Passed or not; each defect's type, angle θ around the cell and height
       z from its base
     - ``CellDefect.msg``
   * - location
     - Conveyor, tester 1 or 2, gripper, tray slot, recycling bin or
       inspection bin
     - Your team

**Inheritance in use.**

- ``Cell`` is the general frame; ``LiIonCell`` and ``NiMHCell`` take every
  slot and fill ``nominal_voltage`` with their own default.
- The tolerances (plus or minus 0.2 V per cell, 0.15 V per kit) are stored
  once for the class, not per cell.

The "From" column says who fills each slot: an ARIAC message definition, or
your team's own code. ``measured_voltage`` and ``location`` have no ARIAC
source, so your system must fill and update them itself.


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

   Many slots mirror ARIAC message fields. Reading the message definitions
   is the fastest way to find the slots a frame needs.


.. _l3-ontologies:

Ontologies
----------

This section covers classes, relations and instances: what can be said about
the factory, and what follows from it.

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
     - Robot (InspectionRobot, AssemblyRobot, GantryWelder), AGV, Station,
       Cell (LiIonCell, NiMHCell), Kit, Module, Shell, Tester, Sensor
       (BreakBeam, DistanceSensor, Camera, Lidar)
   * - **Relations**
     - inSlot(Cell, AGV, slot), atStation(AGV, Station), canReach(Robot,
       Place), testedBy(Cell, Tester), partOf(Cell, Kit)
   * - **Instances**
     - ``inspection_robot_1``, ``agv1``, ``voltage_tester_2``, and each cell
       as it arrives

Each relation names the classes it accepts. inSlot takes a Cell, an AGV and a
slot, so "agv2 is in a slot of agv1" cannot even be written: that is the check
the definition above describes.


From Perception to Planning
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Perception produces instances and facts: cell 7 has a dent at a given
   angle and height.
2. The ontology says what follows: a cell with a defect fails inspection, so
   it must not go in a kit.
3. The planner uses the result.


Where Ontologies Are Standardized
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- IEEE 1872-2015, *IEEE Standard Ontologies for Robotics and Automation*,
  defines a core ontology called **CORA**. IEEE made it inactive (reserved)
  on 2026-03-26 and is drafting a revision, P1872.
- The W3C Web Ontology Language (`OWL <https://www.w3.org/OWL/>`_) is a
  standard language for writing ontologies.
- The course does not require either; they show that standards bodies define
  such ontologies.


.. _l3-world-model:

A World Model at Each Layer
---------------------------

This section takes two ideas from NIST's **4D/RCS** reference model and uses
them inside the three-layer architecture from L2. **4D/RCS** is a reference
model architecture NIST wrote for unmanned vehicle systems: a hierarchy of
levels, each of which plans over its own time span and keeps its own world
model.

Source: J. Albus et al., *4D/RCS: A Reference Model Architecture for Unmanned
Vehicle Systems, Version 2.0*, NISTIR 6910, 2002
(`doi.org/10.6028/NIST.IR.6910 <https://doi.org/10.6028/NIST.IR.6910>`_).

Idea 1: Each Layer Keeps Only the Detail It Decides With
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: From NISTIR 6910
   :class: note

   "At no level does a node have to cope with both broad scope and high level
   of detail" (p. 31). "The world model in any node is rich and detailed
   within the region of attention, but contains only the amount of
   resolution in space and time required for making decisions in that node"
   (p. 55).

.. list-table::
   :header-rows: 1
   :widths: 20 80
   :class: compact-table

   * - **Layer**
     - **Its world model in ARIAC**
   * - Deliberative
     - Orders, kits, which cells are good, AGV stations. No poses.
   * - Executive
     - The blackboard: the cell on each tester, its averaged voltage, the
       slots filled, the step under way
   * - Reactive
     - Joint positions, gripper width, tray slot frames from TF2

The **blackboard** is the shared key-value store a ``py_trees`` behavior tree
reads and writes; L4 covers it.


Idea 2: Errors Are Handled Where They Are Seen; Status Moves Up
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: From NISTIR 6910
   :class: note

   Commands flow down the hierarchy, and status feedback flows up (p. 19,
   Figure 1). An executor that "senses an error between its output
   CommandGoal and the predicted state … may react by modifying the
   commanded action so as to cope with that error" (p. 45).

**In ARIAC, in order.**

1. A skill that loses a grasp stops and returns a failure reason. It never
   retries the task itself.
2. The behavior tree reads that reason, then retries the skill or tries
   another branch.
3. Only when the tree cannot finish the kit does the planner or the agent
   make a new plan.

L11 builds recovery on this order: local recovery first, then global.


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
the servo level to 24 h at the battalion level. ARIAC's stack is shallow, so
the three layers are enough.


.. _l3-three-views:

One Kit, Three Views
--------------------

One kit state, written for the planner, for the agent, and for a prompt. The
values are chosen for this example:

- AGV 1 at the inspection station;
- a Li-Ion kit;
- slots 1 to 3 holding cells measured at 3.55 V, 3.62 V and 3.70 V;
- slot 4 empty.

In ``kit_views.py`` the kit is one Python dictionary:

.. literalinclude:: code/kit_views.py
   :language: python
   :lines: 15-25
   :caption: lecture3/code/kit_views.py (excerpt)


View 1 and View 3: PDDL Facts and Text
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**View 1: PDDL facts, for the GP3 planner.** PDDL (the Planning Domain
Definition Language) describes a state as a list of facts, each true or
false; L6 teaches it. A fact that is not listed is false.

.. literalinclude:: outputs/kit_views.txt
   :language: text
   :lines: 2-9

**View 3: text, for a prompt, next to a VLM description.**

.. literalinclude:: outputs/kit_views.txt
   :language: text
   :lines: 11

- The names are examples; your team chooses its own in GP3.
- A VLM's description of a camera image is checked against this text, not
  trusted on its own (L9).


View 2: A JSON Schema for the GP4 Agent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Definition: JSON schema
   :class: note

   A **JSON schema** is a JSON document that states the rules a JSON record
   must follow: which fields it needs, the type of each, and the allowed
   values. A **validator** checks a record against the schema and lists
   every rule the record breaks.

.. literalinclude:: code/kit_views.py
   :language: python
   :lines: 27-60
   :caption: lecture3/code/kit_views.py (excerpt)

- Each of the four slot items needs a ``slot`` number from 1 to 4 and a
  ``cell``: an object with an ID and a voltage, or ``null``.
- Keywords used: ``type``, ``properties``, ``required``, ``enum``,
  ``minimum``, ``maximum``, ``minItems``, ``maxItems``.


Checking Records Against the Schema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The script checks three records: the kit, a copy that names AGV 5, and a copy
with a fifth slot added.

.. literalinclude:: code/kit_views.py
   :language: python
   :lines: 89-98
   :caption: lecture3/code/kit_views.py (excerpt)

Each error line gives the path to the field that broke a rule, then the rule
and its value. The path counts list items from 0.

.. literalinclude:: outputs/kit_views.txt
   :language: text
   :lines: 13-18

**Reading the schema check.**

1. The example kit passes every rule.
2. AGV 5 breaks one rule: ``agv`` must be at most 3, because ARIAC 2025 has
   three AGVs.
3. A fifth slot breaks two rules at once: the list has more than 4 items
   (``maxItems``), and the new item's ``slot`` number is above 4
   (``slots.4.slot``, counting items from 0).

.. important::

   An LLM agent can return a record like the last two. The schema lets your
   code reject it before any robot moves (L8).


.. _l3-fourth-cell:

Worked Example: Which Fourth Cell Fits?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. The three cells total 3.55 + 3.62 + 3.70 = 10.87 V.
2. The Li-Ion kit window is 14.25 V to 14.55 V (L1).
3. The fourth cell must be between 14.25 − 10.87 = 3.38 V and
   14.55 − 10.87 = 3.68 V.
4. A single cell may only be 3.4 V to 3.8 V, so the fourth cell must be from
   3.40 V to 3.68 V.
5. A cell at 3.75 V passes on its own, but it would put the kit at
   10.87 + 3.75 = 14.62 V, outside the window.

**The program agrees.**

.. literalinclude:: outputs/kit_views.txt
   :language: text
   :lines: 19-20

.. important::

   The representation must keep each cell's measured voltage, not only pass
   or fail; otherwise this decision cannot be made. PDDL handles numbers
   poorly, so GP3 picks the cells in a separate step (L6).


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
   tester reading, the skill result. A world model that loses track of a cell
   cannot recover it by asking ARIAC.


Where the Model Lives in GP1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- On the ``py_trees`` blackboard (L4): a small set of named keys, such as the
  cell on each tester, the averaged voltages and the slots filled.
- Decide the key names and types now. They are interfaces, and your charter
  assigns who owns them.

**Later in the semester.**

- GP3's planner reads the same kit as facts.
- GP4's agent reads it as a record checked by a JSON schema.
- The final demo's recovery logic updates it when a cell fails inspection or
  a tester stops giving valid readings.


Next Class
----------

**Quiz 1** (Wednesday, February 17, start of class): closed notes, on
ELMS-Canvas or paper, covering L1 to L3. Review the ARIAC 2025 tasks,
challenges and what the score rewards; QoS, executors, actions and TF2 and
their demo results; the classical and three-layer architectures and where AI
plugs in; frames, ontologies, the two 4D/RCS ideas and the three views of a
kit.

**L4: Behavior Trees for Task Execution.** The executive layer that runs on
today's representation. After L4, your team writes the GP1 tree.
