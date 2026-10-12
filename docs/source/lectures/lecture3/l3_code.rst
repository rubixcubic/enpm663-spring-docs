====================================================
Code
====================================================

L3 has one script, :download:`kit_views.py <code/kit_views.py>`. It writes
one kit state three ways (PDDL facts, text, and a JSON record checked against
a JSON schema), checks two invalid records, and computes the voltage range
for the kit's fourth cell. It needs no ROS and no simulator.

.. note::

   **What you need.** Python 3 and the ``jsonschema`` package. The outputs
   below come from Python 3.12.3 and ``jsonschema`` 4.10.3:

   .. literalinclude:: outputs/versions.txt
      :language: text

   On Ubuntu 24.04, ``sudo apt install python3-jsonschema`` installs the
   package for the system Python. In a virtual environment, use
   ``pip install jsonschema``.

Run it from the folder that holds it:

.. code-block:: bash

   python3 kit_views.py


The Script
----------

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
       ``(slot-empty ...)`` facts.
   * - ``text_view``
     - View 3: one paragraph of text. It assumes the filled slots come first
       and one slot is empty, as in the example.
   * - ``check``
     - Validates a record with ``Draft7Validator`` and prints every broken
       rule as ``path: rule value``.
   * - ``fourth_cell_range``
     - The range for the fourth cell: inside the kit window and inside the
       single-cell range. Its defaults are the Li-Ion values (nominal 3.6 V);
       pass ``nominal=1.2`` for a Ni-MH kit.
   * - ``main``
     - Prints the two views, checks the kit, an AGV 5 copy and a five-slot
       copy, and prints the fourth-cell range.

.. literalinclude:: code/kit_views.py
   :language: python
   :caption: kit_views.py


Output
------

.. literalinclude:: outputs/kit_views.txt
   :language: text

The :doc:`lecture notes <l3_lecture>` read this output section by section:
:ref:`l3-three-views` and :ref:`l3-fourth-cell`.
