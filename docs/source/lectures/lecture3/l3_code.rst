====================================================
Code
====================================================

L3 has three programs. None needs ROS or a simulator.

.. list-table::
   :header-rows: 1
   :widths: 30 45 25
   :class: compact-table

   * - **File**
     - **What it does**
     - **Notes section**
   * - :download:`kit_views.py <code/kit_views.py>`
     - Writes one kit state three ways (PDDL facts, text, and a JSON record
       in ``kit_record.json``), checks the record and two bad copies
       against a JSON schema, and computes the voltage range for the kit's
       fourth cell, with and without margins for chance.
     - :ref:`l3-three-views`
   * - :download:`ontology_check.py <code/ontology_check.py>`
     - The lecture's ontology sketch as three dictionaries; checks six
       statements against it.
     - :ref:`l3-ontology-check`
   * - :download:`track_cell.py <code/track_cell.py>`
     - Tracks one cell from stand-in events and prints each world-model
       change.
     - :ref:`l3-track-cell`
   * - :download:`run_all.sh <code/run_all.sh>`
     - Runs the three programs with the system Python and writes their
       outputs to ``../outputs/``.
     - This page

.. note::

   **What you need.** Python 3. ``kit_views.py`` also needs the
   ``jsonschema`` package; the other two use only the standard library. The
   outputs below come from Python 3.12.3 and ``jsonschema`` 4.10.3:

   .. literalinclude:: outputs/versions.txt
      :language: text

   On Ubuntu 24.04, ``sudo apt install python3-jsonschema`` installs the
   package for the system Python. In a virtual environment, use
   ``pip install jsonschema``.

Run each program from the folder that holds it:

.. code-block:: bash

   python3 kit_views.py
   python3 ontology_check.py
   python3 track_cell.py

``kit_views.py`` writes ``kit_record.json`` in the folder it runs in.
``track_cell.py`` uses a fixed seed, so it prints the same lines on your
machine.


kit_views.py
------------

.. list-table::
   :header-rows: 1
   :widths: 30 70
   :class: compact-table

   * - **Part**
     - **What it does**
   * - ``KIT``
     - The example kit: AGV 1 at the inspection station, Li-Ion, cells of
       3.55 V, 3.62 V and 3.70 V in slots 1 to 3, slot 4 empty (values chosen
       for the example).
   * - ``CELL``, ``SCHEMA``
     - The JSON schema: AGV 1 to 3, one of four stations, ``LI_ION`` or
       ``NIMH``, exactly four slots, each with a slot number from 1 to 4 and
       a cell or ``null``.
   * - ``pddl_facts``
     - View 1: ``(at ...)``, ``(in-slot ...)``, ``(passed ...)`` and
       ``(slot-empty ...)`` facts. ``(passed ...)`` is inferred: a cell on
       the tray got through the inspection door.
   * - ``text_view``
     - View 3: three lines of text. It assumes the filled slots come first
       and one slot is empty, as in the example.
   * - ``record_text``
     - View 2: the kit as JSON text, one slot per line. ``main`` writes it to
       ``kit_record.json`` and reads it back.
   * - ``check``
     - Validates a record with ``Draft7Validator`` and prints every broken
       rule as ``path: rule value``.
   * - ``fourth_cell_range``
     - The range for the fourth cell: inside the kit window and inside the
       single-cell range, each narrowed by an optional margin. Its defaults
       are the Li-Ion values (nominal 3.6 V) with no margin; pass
       ``nominal=1.2`` for a Ni-MH kit.
   * - ``chance``
     - How far chance moves one average of 5 readings with 0.05 V noise,
       and sums of 3 and 4 averages. ``tail`` gives the chance that a
       normal value lands that many spreads or more above its mean.
   * - ``main``
     - Prints the views, writes and checks the record, checks an AGV 5 copy
       and a five-slot copy, and prints the fourth-cell range, the chance
       figures and the range with margins.

.. literalinclude:: code/kit_views.py
   :language: python
   :caption: kit_views.py

**Output.**

.. literalinclude:: outputs/kit_views.txt
   :language: text

.. literalinclude:: outputs/kit_record.json
   :language: json
   :caption: kit_record.json


ontology_check.py
-----------------

``PARENT`` maps each class to the class it is a kind of, ``RELATIONS`` maps
each relation to the class of each argument, and ``INSTANCES`` maps each
instance to its class. ``check`` accepts a statement when every argument is
of the class the relation needs, or of a kind of it.

.. literalinclude:: code/ontology_check.py
   :language: python
   :caption: ontology_check.py

**Output.**

.. literalinclude:: outputs/ontology_check.txt
   :language: text


track_cell.py
-------------

The events are stand-ins, not ARIAC messages. The five tester readings are
drawn around a true voltage of 3.58 V with ARIAC's 0.05 V noise (seed 91).
The program then checks the average against the range with margins that
``kit_views.py`` prints, 3.47 V to 3.59 V, and the kit total against the
0.09 V kit margin. As GP1 Task 4 says, it places the cell in slot 4 of
``agv1`` only if the kit can still land in the window; otherwise it
recycles the cell.

.. literalinclude:: code/track_cell.py
   :language: python
   :caption: track_cell.py

**Output.**

.. literalinclude:: outputs/track_cell.txt
   :language: text

The :doc:`lecture notes <l3_lecture>` read these outputs section by section.
