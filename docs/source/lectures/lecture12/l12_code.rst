====================================================
Code
====================================================

L12 has four short Python scripts. None of them uses ROS 2 or the ARIAC
simulation: they read small data files that sit next to them, or need none,
and print their results. The outputs below come from running them with
Python 3.12.3, numpy 1.26.4 and PyYAML 6.0.1 (on 2026-10-12, and on
2026-10-18 for ``batch_bar.py``).

.. note::

   **What you need.** Python 3 with ``numpy`` (for ``success_spread.py``
   and ``batch_bar.py``) and ``PyYAML`` (for ``score_calculator.py``). On Ubuntu 24.04 both come
   from apt:

   .. code-block:: bash

      sudo apt install python3-numpy python3-yaml

   Download the scripts and data files below into one folder, ``code/``,
   and create an ``outputs/`` folder next to it: two of the scripts write a
   JSON file to ``../outputs/``. Then run each script from ``code/``:

   .. code-block:: bash

      mkdir -p outputs
      cd code
      python3 perception_metrics.py


.. list-table::
   :header-rows: 1
   :widths: 30 45 25
   :class: compact-table

   * - **File**
     - **What it is**
     - **Notes section**
   * - :download:`perception_metrics.py <code/perception_metrics.py>`
     - Precision and recall from a labeled set of 20 cells, and the
       position error of 8 top shell spawns.
     - :ref:`l12-perception-metrics`
   * - :download:`cells.csv <code/cells.csv>`
     - 20 cells: the true label and the detector's flag.
     - :ref:`l12-perception-metrics`
   * - :download:`shell_poses.csv <code/shell_poses.csv>`
     - 8 top shell spawns: true and estimated position, in meters.
     - :ref:`l12-perception-metrics`
   * - :download:`success_spread.py <code/success_spread.py>`
     - How far chance moves a success rate measured over :math:`n` runs.
     - :ref:`l12-how-many-runs`
   * - :download:`batch_bar.py <code/batch_bar.py>`
     - How often a 20-run batch passes a bar of 19 of 20, for four true
       success rates.
     - :ref:`l12-runs-a-claim-needs`
   * - :download:`score_calculator.py <code/score_calculator.py>`
     - The ARIAC 2025 run score of the two worked-example runs, computed
       the way ``scoring.py`` does.
     - :ref:`l12-worked-example`
   * - :download:`scoring_weights.yaml <code/scoring_weights.yaml>`
     - The ARIAC 2025 weights, penalties and nominal times (branch
       ariac2025, commit 0c3e722).
     - :ref:`l12-scoring`
   * - :download:`run_all.sh <code/run_all.sh>`
     - Runs all four scripts and writes their outputs to ``../outputs/``.
     - See the last section


Perception metrics: ``perception_metrics.py``
---------------------------------------------

The script reads ``cells.csv``, counts the four outcomes (true positive, false
positive, false negative, true negative), and prints precision and recall.
Then it reads ``shell_poses.csv`` and prints each spawn's position error in
millimeters, with their mean, sample standard deviation and largest value.
Every value in both files is chosen for this example.

.. code-block:: bash

   python3 perception_metrics.py

.. literalinclude:: code/perception_metrics.py
   :language: python
   :caption: perception_metrics.py

The two data files:

.. literalinclude:: code/cells.csv
   :language: text
   :caption: cells.csv

.. literalinclude:: code/shell_poses.csv
   :language: text
   :caption: shell_poses.csv

Output:

.. literalinclude:: outputs/perception.txt
   :language: text


Success rate spread: ``success_spread.py``
------------------------------------------

A system that completes the trial with true probability 0.80 (``P_TRUE``,
chosen for this example) is tested :math:`n` times, for :math:`n` = 5, 10, 20,
50 and 100, and each test is repeated 10000 times (``REPEATS``). For each
:math:`n` the script prints the middle 95% of the measured rates, their
standard deviation and the standard error formula. The second part compares
two systems with the same true rate, 20 runs each, and prints how often chance
alone makes them look 0.10 or more apart. The seed is fixed (12), so every run
prints the same numbers. The script also writes ``../outputs/success_spread.json``,
which the plot in the notes reads.

.. code-block:: bash

   python3 success_spread.py

.. literalinclude:: code/success_spread.py
   :language: python
   :caption: success_spread.py

Output:

.. literalinclude:: outputs/success_spread.txt
   :language: text


Batch pass rate: ``batch_bar.py``
---------------------------------

The course skills package tests its skills in batches of 20 runs, and a skill
passes at 19 of 20 or better. For each true success rate :math:`p` (0.80,
0.90, 0.95 and 0.99, chosen for this example) the script prints the chance
that all 20 runs succeed, :math:`p^{20}`, the chance that exactly one fails,
:math:`20 \times p^{19} \times (1 - p)`, and their sum: the chance that the
batch passes. A simulation of 1000000 batches with a fixed seed (19) checks
each sum.

.. code-block:: bash

   python3 batch_bar.py

.. literalinclude:: code/batch_bar.py
   :language: python
   :caption: batch_bar.py

Output:

.. literalinclude:: outputs/batch_bar.txt
   :language: text


Score calculator: ``score_calculator.py``
-----------------------------------------

The script reads ``scoring_weights.yaml`` and computes the base score, the
five bonuses (with every bonus set to 0 when an order is missing, and the same clamping as ``scoring.py``),
the penalties and the run score for the two runs of the worked example. The
sensor prices come from the ARIAC sensors page; the choice of sensors and
every run measurement are chosen for the example. Its last line checks the
over-budget penalty for a $10400 sensor setup. It also writes
``../outputs/score_runs.json``, which the bar chart in the notes reads.

To score a run of your own, change the ``SENSORS`` list and the ``run_1``
dictionary: ``kits_wanted`` and ``kits_done``, ``modules_wanted`` and
``modules_done``, ``tm`` and ``te`` in seconds, ``report_s`` (the average
report time, in seconds), ``hp_s`` (one entry per high-priority order, in
seconds from announcement to submission; an empty list if there is none),
``defective`` and ``correct`` (defective cells, and correct reports), and
``events`` (penalty name and number of occurrences). Set ``kits_wanted`` or
``modules_wanted`` to 0 for a trial without kits or modules: that part of the
base score is then 0, as in ``scoring.py``.

.. code-block:: bash

   python3 score_calculator.py

.. literalinclude:: code/score_calculator.py
   :language: python
   :caption: score_calculator.py

.. literalinclude:: code/scoring_weights.yaml
   :language: yaml
   :caption: scoring_weights.yaml

Output:

.. literalinclude:: outputs/score_runs.txt
   :language: text

The JSON file the script writes:

.. literalinclude:: outputs/score_runs.json
   :language: json
   :caption: outputs/score_runs.json


Run everything: ``run_all.sh``
------------------------------

``run_all.sh`` runs the four scripts in turn, writes each output to
``../outputs/``, and records the Python, numpy and PyYAML versions in
``versions.txt``. It clears the environment (``env -i``) and calls
``/usr/bin/python3``, so it uses the system Python even when a ROS 2 setup or
a virtual environment is sourced in your shell.

.. code-block:: bash

   bash run_all.sh

.. literalinclude:: code/run_all.sh
   :language: bash
   :caption: run_all.sh

The versions it recorded:

.. literalinclude:: outputs/versions.txt
   :language: text
