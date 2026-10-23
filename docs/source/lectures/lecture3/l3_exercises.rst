====================================================
Exercises
====================================================

.. important::

   **These exercises are not submitted and they are not graded.** Nothing on
   this page goes to ELMS-Canvas.

   They exist so you can check your own understanding before the graded
   work, which is the five in-class quizzes, the four group projects and
   the final demo listed in the :doc:`syllabus </syllabus/index>`.

Seven take-home exercises on the L3 slides and programs. Exercises 1 to 3
are on paper: a frame, the observed, inferred and unknown facts of Task 1,
and an ontology check. Exercises 4 to 7 change ``kit_views.py``: more invalid
records, new schema rules, a Ni-MH kit, and more tester readings. For those,
predict the output first, write it down, then run the script.

.. note::

   The script is on the :doc:`code page <l3_code>`. Work on a copy, so the
   original still gives the output in the notes. To check a new record, build
   it in ``main`` (``copy.deepcopy(KIT)``, then change one field, as the script
   does for AGV 5) and call ``check("a name", record)``. Every output below
   was measured with Python 3.12.3 and ``jsonschema`` 4.10.3, last rerun on
   2026-10-18 with the current script.


.. dropdown:: Exercise 1. A Voltage Tester Frame
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Build a frame for an object the lecture did not cover, and fill a cell
   frame for one real moment of Task 1.

   .. raw:: html

      <hr>

   **Part A. The tester frame**

   L1 said: a tester publishes a voltage reading with a small amount of
   noise, so your team averages readings over a short window; during a
   malfunction, the ARIAC 2025 code keeps publishing, with a voltage of −1
   and the status ``MALFUNCTIONING``.

   1. Write a ``VoltageTester`` frame: its slots, a filler or default for
      each, and where each filler comes from (an ARIAC topic, or your team).
   2. Which slot links to another frame?

   .. raw:: html

      <hr>

   **Part B. One cell, one moment**

   A Ni-MH cell, ``c12``, passed lidar inspection with no defect. It now
   sits in tester 2, and your node has averaged its readings to 1.25 V.

   3. Fill every slot of its cell frame (the slots from the lecture's cell
      frame table). Mark which filler is a default inherited from
      ``NiMHCell``.
   4. Which two slots will change next, and what event changes each?

   .. dropdown:: Solution
      :color: success

      **Question 1.** One reasonable frame (your names may differ):

      .. list-table::
         :header-rows: 1
         :widths: 22 48 30
         :class: compact-table

         * - **Slot**
           - **Filler**
           - **From**
         * - id
           - 1 or 2
           - Your team (from the topic name, ``/voltage_tester_1/voltage``)
         * - status
           - Default: operational. ``MALFUNCTIONING`` when the tester says so
           - The tester's voltage topic
         * - last_reading
           - The newest voltage, or −1 during a malfunction
           - The tester's voltage topic
         * - cell
           - A link to the cell frame of the cell inside, or empty
           - Your team
         * - readings
           - The readings since the cell arrived, to average
           - Your team

      **Question 2.** ``cell`` links to a cell frame. That link is how the
      tester's averaged voltage reaches the right cell's
      ``measured_voltage`` slot.

      A frame that keeps only ``last_reading`` and drops ``status`` would
      average −1 into a cell during a malfunction. The status slot is what
      lets your tree tell a bad reading from a bad cell.

      **Question 3.**

      - type: ``NIMH``.
      - nominal_voltage: 1.2 V, the **default inherited** from ``NiMHCell``.
      - measured_voltage: 1.25 V.
      - inspection: passed, no defects.
      - location: tester 2.

      **Question 4.** ``location`` changes when inspection robot 2's place
      skill returns its result: to a tray slot (1.25 V is inside 1.0 V to
      1.4 V, so the cell is good). Once the cell is in a kit, the kit
      frame's slot links to ``c12``, and the kit's ``total_voltage`` changes.


.. dropdown:: Exercise 2. Observed, Inferred or Unknown
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Sort the facts a GP1 tree uses by where they come from, and place each in
   the layer that needs it.

   .. raw:: html

      <hr>

   **Specification**

   For each fact, say whether it is **observed** (read from an ARIAC topic
   or service reply), **inferred** (from your team's reasoning) or
   **unknown** (no ARIAC interface gives it). Then name the lowest layer
   that needs it: deliberative, executive or reactive.

   1. The competition state is ``STARTED``.
   2. The cell now in tester 1 is the one the break beam saw 4 s ago.
   3. Tester 2 reads 3.61 V.
   4. The averaged voltage of the cell in tester 2 is in range.
   5. Slot 2 of AGV 1 is occupied.
   6. Where on the conveyor the next cell is right now.
   7. The kit on AGV 1 will pass the check kit quality service.
   8. The joint positions of inspection robot 2.

   .. dropdown:: Solution
      :color: success

      .. list-table::
         :header-rows: 1
         :widths: 46 18 36
         :class: compact-table

         * - **Fact**
           - **Kind**
           - **Lowest layer that needs it**
         * - 1. Competition state ``STARTED``
           - Observed
           - Executive (the tree waits for ``READY`` and starts the run)
         * - 2. Tester 1 holds the cell the beam saw
           - Inferred
           - Executive
         * - 3. Tester 2 reads 3.61 V
           - Observed
           - Executive (it averages the readings)
         * - 4. The averaged voltage is in range
           - Inferred
           - Executive; the deliberative layer needs only "this cell is
             good"
         * - 5. Slot 2 of AGV 1 is occupied
           - Observed (``AgvTrayStatus.msg``)
           - Executive
         * - 6. Where the next cell is now
           - Unknown
           - None can read it; the executive layer tracks cells from events
         * - 7. The kit will pass the check
           - Inferred, until you call the service; the reply is observed
           - Deliberative (which cells go together)
         * - 8. Joint positions of inspection robot 2
           - Observed
           - Reactive

      Facts 2 and 4 are where a world model goes wrong without anyone
      noticing: if the tree matches a tester reading to the wrong cell, every
      later fact about that cell is wrong too, and ARIAC cannot correct it
      (fact 6). Fact 4 shows the design rule: the executive layer keeps the
      voltage, and passes up only what the layer above decides with.


.. dropdown:: Exercise 3. Check Statements Against the Ontology
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Use the lecture's ARIAC ontology to accept or reject statements, and to
   apply the ontology's rule to a perception result.

   .. raw:: html

      <hr>

   **Specification**

   Use the classes and relations from the ontology sketch in the notes:
   inSlot(Cell, AGV, Slot), atStation(AGV, Station), testedBy(Cell, Tester),
   partOf(Cell, Kit). ``s2`` and ``s3`` are Slots.

   1. Which of these statements make sense, and why not for the others?

      a. inSlot(c7, agv1, s2)
      b. inSlot(agv2, agv1, s3)
      c. atStation(agv1, shipping)
      d. testedBy(agv1, voltage_tester_1)
      e. partOf(c7, kit3)

   2. Perception reports that c7 has a dent. Statement (e) is in the world
      model. What does the ontology say follows, and what must the system do?

   To check Question 1 by machine, add the instances to ``INSTANCES`` in a
   copy of ``ontology_check.py`` and call ``check`` for each statement.

   .. dropdown:: Solution
      :color: success

      **Question 1.**

      a. Makes sense: a Cell, an AGV and a Slot.
      b. Rejected: inSlot needs a Cell first, and agv2 is an AGV. This is the
         lecture's example: a cell can be in a slot; an AGV cannot.
      c. Makes sense: an AGV and a Station.
      d. Rejected: testedBy needs a Cell first.
      e. Makes sense: a Cell and a Kit.

      **Question 2.** A cell with a defect fails inspection, so it must not
      go in a kit. The world model now holds two facts that cannot both
      stand: c7 has a dent, and c7 is part of kit3. In Task 1 your system
      submits a failing report for c7, the inspection door stays closed, c7
      drops into the inspection bin, and it never reaches a tray. Your system must remove
      partOf(c7, kit3) and plan another cell for that place in the kit.


.. dropdown:: Exercise 4. More Invalid Records
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Learn exactly what the schema catches and what it lets through, as an
   LLM agent's answers would test it.

   .. raw:: html

      <hr>

   **Specification**

   Make each record from ``KIT`` with one change, check it, and predict the
   printed lines first.

   1. ``station`` is ``"IN_TRANSIT"``.
   2. ``agv`` is the string ``"1"``.
   3. ``cell_type`` is missing.
   4. The cell in slot 1 has no ``voltage``.
   5. The voltage in slot 2 is the string ``"3.62"``.
   6. ``agv`` is 0.
   7. ``slots`` has only the first three items.
   8. The fourth item's ``slot`` number is 1 instead of 4.
   9. The voltage in slot 1 is −3.55.
   10. ``cell_type`` is ``"LI-ION"`` (a hyphen instead of an underscore).
   11. An extra field, ``agv_id``, set to 1.

   Then answer:

   12. Which records pass, and what is wrong with each of them?
   13. The lecture leaves ``IN_TRANSIT`` out of ``station`` on purpose. Give
       one case where your system would need a record for a moving AGV, and
       say what else must change if you add it.

   .. dropdown:: Solution
      :color: success

      Measured:

      .. code-block:: text

           in transit: rejected
             station: enum ['INSPECTION', 'ASSEMBLY', 'SHIPPING', 'RECYCLING']
           agv as text: rejected
             agv: type integer
           no cell type: rejected
             : required ['agv', 'station', 'cell_type', 'slots']
           no voltage: rejected
             slots.0.cell: required ['id', 'voltage']
           voltage as text: rejected
             slots.1.cell.voltage: type number
           agv 0: rejected
             agv: minimum 1
           three slots: rejected
             slots: minItems 4
           slot 1 twice: valid
           negative voltage: valid
           LI-ION: rejected
             cell_type: enum ['LI_ION', 'NIMH']
           extra field agv_id: valid

      Notes on the lines:

      - Record 3 has an empty path before the colon: the broken rule is on
        the top-level object, which must have all four fields.
      - Records 2 and 5 show that ``"1"`` and ``"3.62"`` are text, not
        numbers. An LLM often writes numbers as text, and the schema catches
        it.
      - Record 10 shows why the schema uses ``enum``: one wrong character is
        a different value.

      **Question 12.** Three records pass:

      - **Slot 1 twice** (record 8): two items claim slot 1 and none claims
        slot 4. No rule says the slot numbers must differ.
      - **Negative voltage** (record 9): the schema says only that a voltage
        is a number.
      - **Extra field** (record 11): by default JSON Schema allows fields
        the schema does not list, so ``agv_id`` passes unnoticed while the
        code reads ``agv``.

      Exercise 5 adds rules for all three.

      **Question 13.** One case: a high-priority order arrives while
      ``agv1`` drives to shipping, and the agent must decide now whether to
      start the Ni-MH kit on another AGV. It needs a record that says
      ``agv1`` is moving and what it carries. Adding ``IN_TRANSIT`` to the
      ``enum`` is the one-line part. The rest is in the code that reads the
      record: no skill may place a cell on a moving AGV, the planner must
      not treat ``IN_TRANSIT`` as a station it can send work to, and the
      record must be refreshed when the AGV arrives (``AgvStations.msg``
      gives ``IN_TRANSIT`` the value −1).


.. dropdown:: Exercise 5. Add Schema Rules
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Close the gaps Exercise 4 found, and find one rule JSON Schema cannot
   write the obvious way.

   .. raw:: html

      <hr>

   **Part A. Two one-line rules**

   1. In ``CELL``, change the voltage rule to
      ``{"type": "number", "exclusiveMinimum": 0}``. Check the kit and the
      negative-voltage record.
   2. Add ``"additionalProperties": False`` to the top level of ``SCHEMA``.
      Check the kit and the ``agv_id`` record.

   .. raw:: html

      <hr>

   **Part B. Different slot numbers**

   3. Add ``"uniqueItems": True`` to the ``slots`` rule. Predict, then check
      the "slot 1 twice" record. Also check a record whose fourth item is a
      full copy of the first item.
   4. ``uniqueItems`` compares whole items. Replace the ``items`` rule with a
      list of four rules, one per position, where item *i* must have
      ``"slot": {"const": i}``:

      .. code-block:: python

         "items": [
             {
                 "type": "object",
                 "required": ["slot", "cell"],
                 "properties": {"slot": {"const": i}, "cell": CELL},
             }
             for i in range(1, 5)
         ],

      Check the kit, "slot 1 twice" and the five-slot record from class.

   .. raw:: html

      <hr>

   **Part C. A voltage range per cell type (optional)**

   5. Draft 7 JSON Schema has ``if`` and ``then``. Add this to ``SCHEMA``:

      .. code-block:: python

         "allOf": [
             {"if": {"properties": {"cell_type": {"const": "LI_ION"}}},
              "then": {"properties": {"slots": {"items": {"properties": {
                  "cell": {"properties": {"voltage": {
                      "minimum": 3.4, "maximum": 3.8}}}}}}}}},
             {"if": {"properties": {"cell_type": {"const": "NIMH"}}},
              "then": {"properties": {"slots": {"items": {"properties": {
                  "cell": {"properties": {"voltage": {
                      "minimum": 1.0, "maximum": 1.4}}}}}}}}},
         ],

      Check the kit, a copy with the slot 3 voltage set to 3.85, and a copy
      with ``cell_type`` set to ``"NIMH"`` and the Li-Ion voltages left in
      place.
   6. Can the schema check the kit voltage window? Why or why not?

   .. dropdown:: Solution
      :color: success

      **Questions 1 and 2.** Measured:

      .. code-block:: text

           the kit: valid
           negative voltage: rejected
             slots.0.cell.voltage: exclusiveMinimum 0
           extra field agv_id: rejected
             : additionalProperties False

      **Question 3.** Measured:

      .. code-block:: text

           slot 1 twice: valid
           slot 1 copied: rejected
             slots: uniqueItems True

      "Slot 1 twice" still passes. Its two slot-1 items differ (one holds
      c1, the other ``null``), so they are not duplicates. ``uniqueItems``
      catches only an exact copy.

      **Question 4.** Measured:

      .. code-block:: text

           the kit: valid
           slot 1 twice: rejected
             slots.3.slot: const 4
           five slots: rejected
             slots: maxItems 4

      Fixing each position's slot number makes the numbers different by
      construction. It also means the agent must list the slots in order,
      1 to 4. The five-slot record now breaks one rule instead of two: the
      fifth item matches none of the four position rules, and in Draft 7 an
      item past the end of an ``items`` list is not checked.

      **Question 5.** Measured:

      .. code-block:: text

           the kit: valid
           cell at 3.85 V: rejected
             slots.2.cell.voltage: maximum 3.8
           Li-Ion voltages, NIMH type: rejected
             slots.0.cell.voltage: maximum 1.4
             slots.1.cell.voltage: maximum 1.4
             slots.2.cell.voltage: maximum 1.4

      The last record is the disagreement the lecture warned about: a type stored in
      one place and voltages in another that do not agree. The schema now
      catches it.

      **Question 6.** No, not with these keywords. Each rule checks one value
      against fixed limits; none adds the four voltages. The window needs a
      sum, so it stays in code: ``fourth_cell_range`` in the script, or your
      own check before the robot places a cell.


.. dropdown:: Exercise 6. Write the Ni-MH Kit
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Write the kit of a high-priority order in all three views, and catch a
   default that is wrong for Ni-MH.

   .. raw:: html

      <hr>

   **Specification**

   A high-priority order arrives. AGV 2 is at the inspection station. Its
   tray holds three Ni-MH cells, ``c11``, ``c12`` and ``c13``, measured at
   1.18 V, 1.25 V and 1.21 V in slots 1 to 3; slot 4 is empty (values chosen
   for this exercise).

   1. Write the record as a Python dictionary like ``KIT``, named
      ``NIMH_KIT``. Predict the PDDL facts and the text, then print them with
      ``pddl_facts`` and ``text_view``.
   2. Check it with ``check("the Ni-MH kit", NIMH_KIT)``.
   3. Call ``fourth_cell_range(NIMH_KIT)`` with no other argument and print
      the three numbers. What is wrong with the answer, and why?
   4. Call it again with ``nominal=1.2``. Check the result by hand.

   .. dropdown:: Solution
      :color: success

      **Question 1.**

      .. code-block:: python

         NIMH_KIT = {
             "agv": 2,
             "station": "INSPECTION",
             "cell_type": "NIMH",
             "slots": [
                 {"slot": 1, "cell": {"id": "c11", "voltage": 1.18}},
                 {"slot": 2, "cell": {"id": "c12", "voltage": 1.25}},
                 {"slot": 3, "cell": {"id": "c13", "voltage": 1.21}},
                 {"slot": 4, "cell": None},
             ],
         }

      Measured:

      .. code-block:: text

         PDDL facts:
           (at agv2 inspection)
           (in-slot c11 agv2 s1)
           (passed c11)
           (in-slot c12 agv2 s2)
           (passed c12)
           (in-slot c13 agv2 s3)
           (passed c13)
           (slot-empty agv2 s4)
         Text:
           AGV 2 is at the inspection station. Kit type Ni-MH.
           Slots 1 to 3 hold cells at 1.18 V, 1.25 V and 1.21 V.
           Slot 4 is empty.

      The PDDL facts do not say the cells are Ni-MH. If the planner must
      know (a high-priority order needs a Ni-MH kit), add a fact such as
      ``(kit-type agv2 nimh)``.

      **Question 2.** Measured:

      .. code-block:: text

         JSON schema checks:
           the Ni-MH kit: valid

      **Question 3.** Measured, printed as ``total, low, high``:

      .. code-block:: text

         3.64 V, 10.61 V to 3.80 V

      The low end is above the high end, so the range is empty. The
      function's defaults are the Li-Ion values: it compared a Ni-MH total of
      3.64 V with the Li-Ion window, 14.25 V to 14.55 V, which gives a low
      end of 14.25 − 3.64 = 10.61 V. The function does not read
      ``cell_type``: a fact stored in the record and a default stored in the
      code disagree.

      **Question 4.** Measured:

      .. code-block:: text

         Three cells total 3.64 V.
         The fourth cell must be from 1.01 V to 1.31 V.

      By hand:

      1. 1.18 + 1.25 + 1.21 = 3.64 V.
      2. The Ni-MH window is 4 × 1.2 = 4.8 V plus or minus 0.15 V: 4.65 V to
         4.95 V.
      3. The fourth cell must be between 4.65 − 3.64 = 1.01 V and
         4.95 − 3.64 = 1.31 V.
      4. A single Ni-MH cell may be 1.0 V to 1.4 V, so the answer stays
         1.01 V to 1.31 V.

      A safer function takes the nominal voltage from the record's
      ``cell_type``, so the two cannot disagree.


.. dropdown:: Exercise 7. Twenty Readings Instead of Five
   :icon: number
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   See how the number of readings behind each average changes the margins
   and the verdicts of the fourth-cell example.

   .. raw:: html

      <hr>

   **Specification**

   Your tree takes 20 readings per cell instead of the lecture's five. The
   kit is the lecture's example kit (10.87 V in slots 1 to 3), and the
   margins are still twice what chance moves each number.

   1. By hand: how far does one average wander, and how far does a sum of
      four averages wander?
   2. By hand: the kit margin, the cell margin (both rounded to 0.01 V), and
      the range for the fourth cell.
   3. Check your answers with ``chance(readings=20)`` and
      ``fourth_cell_range(KIT, margin=..., cell_margin=...)``.
   4. Cell ``c4`` averages 3.599 V, as in the lecture's ``track_cell.py``
      example. Does it go in slot 4 now?
   5. How many spreads over the edge is the 0.07 V overshoot of a 3.75 V
      cell now, and how often would a true 14.55 V kit read that high? Use
      ``tail`` from ``kit_views.py``.

   .. dropdown:: Solution
      :color: success

      **Question 1.**

      1. One average: 0.05 / √20 = 0.0112 V.
      2. Four averages: √4 × 0.0112 = 0.0224 V.

      **Question 2.**

      1. Kit margin: 2 × 0.0224 = 0.04 V. Cell margin: 2 × 0.0112 = 0.02 V.
      2. Low end: the larger of 14.25 + 0.04 − 10.87 = 3.42 V and
         3.40 + 0.02 = 3.42 V, so 3.42 V.
      3. High end: the smaller of 14.55 − 0.04 − 10.87 = 3.64 V and
         3.80 − 0.02 = 3.78 V, so 3.64 V.

      **Question 3.** Measured (printed with four and two decimals):

      .. code-block:: text

         0.0112 0.0194 0.0224
         0.04 0.02
         10.87 3.42 3.64

      The three numbers on the first line are one average, three averages
      and four averages. The range with margins is 3.42 V to 3.64 V, against
      3.47 V to 3.59 V with five readings.

      **Question 4.** Yes. 3.599 V is inside 3.42 V to 3.64 V, so ``c4`` goes
      in slot 4: 10.87 + 3.599 = 14.469 V is 0.081 V below the top edge,
      more than the 0.04 V kit margin, so chance alone does not put the true
      total on the other side. With five readings, the same total was inside
      the 0.09 V margin, and the tree recycled ``c4``.

      **Question 5.** Measured: 0.07 / 0.0224 = 3.13 spreads, and
      ``100 * tail(3.13)`` prints 0.1 (%). With five readings it was 1.57
      spreads and 5.9%. Four times as many readings halve every spread, so
      the 3.75 V verdict goes from likely to nearly certain, and the range
      for the fourth cell widens. The cost is time: with readings at a fixed
      rate, each cell sits on the tester four times as long.
