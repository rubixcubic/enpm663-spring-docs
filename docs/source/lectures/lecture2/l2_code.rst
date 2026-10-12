====================================================
Code
====================================================

L2 has one program, the **toy factory** ``toy_factory.py``. It runs one short
Task 1 run under three architectures (plan only, react only, three layers)
while a voltage tester malfunctions. It is plain Python: no ROS, no ARIAC
simulation, no extra packages. The outputs below come from running it with
Python 3.12.3 on 2026-10-12.

.. note::

   **What you need.** Python 3 and nothing else: the script uses only the
   standard library (``argparse`` and ``random``). You do not need to source
   ROS 2. Open a terminal and go to the folder that holds the script:

   .. code-block:: bash

      cd lecture2/code
      python3 toy_factory.py --help

   Every run uses fixed seeds, so the same command gives the same output on
   your machine.

.. list-table::
   :header-rows: 1
   :widths: 30 45 25
   :class: compact-table

   * - **File**
     - **What it does**
     - **Notes section**
   * - :download:`toy_factory.py <code/toy_factory.py>`
     - The toy factory and its three architectures.
     - :ref:`l2-toy-factory`
   * - :download:`run_all.sh <code/run_all.sh>`
     - Runs the seven commands below and writes their outputs to
       ``../outputs/``.
     - See the last section


What the Toy Keeps from ARIAC
-----------------------------

Only these rules come from ARIAC 2025 (source, branch ``ariac2025``); the file
names are in the script's comments.

- Li-Ion cells: 3.6 V nominal, plus or minus 0.2 V per cell, plus or minus
  0.15 V per kit of four (``CellTypes.msg``). So a cell is good from 3.4 V to
  3.8 V, and a kit from 14.25 V to 14.55 V.
- Cell voltages spread with a standard deviation of 0.1 V
  (``cell_feed_plugin.hpp``).
- Tester noise with a standard deviation of 0.05 V
  (``voltage_tester/model.sdf``); a new reading every 0.1 s; an empty tester
  reads about 0 V.
- A malfunctioning tester reports −1 V with the status ``MALFUNCTIONING``
  (``voltage_tester_plugin.cpp``).

Everything else is chosen for this example: the step times, the grasp failure
rate and the number of cells. The step times, in seconds of the toy's clock,
are set at the top of the script:

.. list-table::
   :header-rows: 1
   :widths: 30 20 50
   :class: compact-table

   * - **Constant**
     - **Value**
     - **What takes that long**
   * - ``T_PICK``
     - 4 s
     - One pick from the conveyor, failed or not
   * - ``T_PLACE``
     - 3 s
     - Placing the held cell in a tester
   * - ``T_MOVE``
     - 4 s
     - Moving a cell from one tester to the other
   * - ``T_TRAY``
     - 6 s
     - Moving a cell from a tester to an AGV tray
   * - ``T_BIN``
     - 4 s
     - Moving a cell from a tester to the recycling bin
   * - ``T_SHIP``
     - 10 s
     - Shipping the kit
   * - ``T_READ``
     - 0.1 s
     - One tester reading (``N_READS`` = 10 readings are averaged per cell)


The Script: ``toy_factory.py``
------------------------------

.. literalinclude:: code/toy_factory.py
   :language: python
   :caption: toy_factory.py

The parts, in order:

- ``Factory`` is the world: the conveyor queue, the two testers, the three
  AGV trays, the recycling bin and a clock. Its skill methods
  (``pick_from_conveyor``, ``place_in_tester``, ``tester_to_tester``,
  ``tester_to_tray``, ``tester_to_bin``) stand in for the course skills
  package. Each one returns ``SUCCESS`` or a failure reason, and none of them
  retries. ``ship`` stands in for the AGV move and ARIAC's kit check.
- ``plan_only``, ``react_only`` and ``three_layers`` are the three
  architectures. ``three_layers`` uses a ``Planner`` (the deliberative layer)
  and an ``Executive`` (the executive layer) on top of the skills.
- ``sweep`` repeats each architecture over many seeds and counts the
  verdicts.


Options
-------

.. list-table::
   :header-rows: 1
   :widths: 28 14 58
   :class: compact-table

   * - **Option**
     - **Default**
     - **What it sets**
   * - ``--arch NAME``
     - all three
     - Run one architecture and print its full trace: ``"plan only"``,
       ``"react only"`` or ``"three layers"`` (keep the quotes).
   * - ``--seed N``
     - 1
     - The seed for the cell voltages, the reading noise and the grasp
       failures.
   * - ``--cells N``
     - 10
     - The number of cells on the conveyor.
   * - ``--pick-fail P``
     - 0.2
     - The probability that one pick fails with ``GRASP_FAILED``.
   * - ``--retries N``
     - 2
     - How many times the three-layer executive retries a failed pick (so
       ``1 + N`` attempts). Plan only and react only do not use it.
   * - ``--no-malfunction``
     - off
     - Switch the tester malfunction off.
   * - ``--tester N``
     - 1
     - Which tester malfunctions, 1 or 2.
   * - ``--start S``
     - 20.0
     - When the malfunction starts, in seconds of the toy's clock (ARIAC's
       ``START_TIME``).
   * - ``--duration S``
     - 45.0
     - How long the malfunction lasts (ARIAC's ``DURATION``).
   * - ``--limit S``
     - 300.0
     - The time limit for react only and three layers. Plan only ends when its
       plan ends.
   * - ``--sweep N``
     - 0 (off)
     - Run each architecture on ``N`` seeds, starting at ``--seed``, and print
       a table of how the runs ended.


Mode 1: All Three, One Line Each
--------------------------------

.. code-block:: bash

   python3 toy_factory.py

With no ``--arch``, the script prints the true voltage of each cell, then one
verdict per architecture: when it finished, whether ARIAC's kit check would
accept the kit, and which in-range cells it recycled.

.. literalinclude:: outputs/summary.txt
   :language: text
   :caption: outputs/summary.txt

Only the three layers ship a kit inside 14.25 V to 14.55 V. Plan only also
recycled two good cells (3 and 5). The lecture notes work through each total
in :ref:`l2-toy-result`.


Mode 2: One Architecture, Step by Step
--------------------------------------

.. code-block:: bash

   python3 toy_factory.py --arch "plan only"
   python3 toy_factory.py --arch "react only"
   python3 toy_factory.py --arch "three layers"

With ``--arch``, the script prints a trace: one line per step, with the toy's
clock in seconds, and the verdict as the last line. ``cell 3: tester 1 reads
-1.00 V -> bin`` means the cell 3 reading at tester 1 was −1.00 V and the cell
went to the recycling bin. ``no cell`` means a pick failed and the tester was
empty when it was read.

**Plan only.** The fixed plan reads the malfunctioning tester's −1 V as a
voltage, so cells 3 and 5 go to the bin. It never checks a pick, so it reads
an empty tester twice.

.. literalinclude:: outputs/plan_only.txt
   :language: text
   :caption: outputs/plan_only.txt

**React only.** Rule 2 moves cell 2 away from the malfunctioning tester, but
the rules keep no record of the tray, so the first four in-range cells ship.

.. literalinclude:: outputs/react_only.txt
   :language: text
   :caption: outputs/react_only.txt

**Three layers.** The executive sees the malfunction and moves cell 3, the
planner stops using tester 1 until a status check finds it working again, the
executive retries two failed grasps, and the planner sends cells that do not
fit (2 and 5) to AGV 2.

.. literalinclude:: outputs/three_layers.txt
   :language: text
   :caption: outputs/three_layers.txt


Mode 3: No Malfunction
----------------------

.. code-block:: bash

   python3 toy_factory.py --no-malfunction

.. literalinclude:: outputs/no_malfunction.txt
   :language: text
   :caption: outputs/no_malfunction.txt

Without the malfunction, plan only no longer recycles good cells, but its kit
(cells 1 to 4, the same as react only's) is still 14.60 V, too high. The
malfunction was not the reason plan only failed: nobody chose the cells.


Mode 4: A Sweep over 1000 Seeds
-------------------------------

.. code-block:: bash

   python3 toy_factory.py --sweep 1000
   python3 toy_factory.py --sweep 1000 --no-malfunction

Each row is one architecture run on seeds 1 to 1000. The columns count how
the runs ended:

- ``accepted``: the kit passed;
- ``total``: rejected because the kit total was outside 14.25 V to 14.55 V;
- ``bad cell``: rejected because a cell was outside 3.4 V to 3.8 V;
- ``short``: rejected because the tray had fewer than four cells;
- ``stopped``: the three-layer run stopped cleanly (a grasp failed on every
  attempt, or the cells ran out);
- ``binned``: in-range cells sent to the recycling bin, over all 1000 runs.

A run that hits ``--limit`` counts as a timeout, which the table does not
print. In both sweeps below every row adds up to 1000 (for example
600 + 371 + 11 + 18 + 0 = 1000), so no run timed out.

.. literalinclude:: outputs/sweep.txt
   :language: text
   :caption: outputs/sweep.txt

.. literalinclude:: outputs/sweep_off.txt
   :language: text
   :caption: outputs/sweep_off.txt

What the table shows (the lecture notes give the chance check):

- Plan only and react only accept about the same number of kits with or
  without the malfunction (600 to 613), because neither chooses the cells.
- The malfunction shows in plan only's ``binned`` column: 1570 good cells
  recycled with it, 28 without.
- Three layers accepts 919 kits with the malfunction and 921 without.

A sweep runs 3000 toy runs (1000 per architecture). On the course machine it
took 0.23 s.


Running Everything: ``run_all.sh``
----------------------------------

``run_all.sh`` is the script that produced the outputs above. It runs the
seven commands of this page and writes each output to ``../outputs/``. It
calls Python through ``env -i``, which on the course machine kept another
project's Python setup out of the runs. You do not need it: the commands
above give the same results.

.. literalinclude:: code/run_all.sh
   :language: bash
   :caption: run_all.sh

The Python version it recorded:

.. literalinclude:: outputs/versions.txt
   :language: text
   :caption: outputs/versions.txt
