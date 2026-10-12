====================================================
Code
====================================================

L11 has four short Python scripts. None of them needs a simulator or a
model: each runs in plain Python and prints a trace. The outputs below come
from running them with Python 3.12.3, ``py_trees`` 2.6.0 and ``jsonschema``
4.10.3.

.. important::

   **All four scripts use stand-ins.** The skills in ``recovery_tree.py``
   and ``timeout_demo.py`` are stubs that follow a script of outcomes. The
   LLM in ``llm_output_checker.py`` is a fixed list of replies; a real
   model's answers vary. The readings in ``tester_watcher.py`` are
   synthetic. The values each script uses are labeled in its docstring.

.. note::

   **What you need.** Python 3, ``py_trees`` and ``jsonschema``.
   ``py_trees`` is the ROS 2 Jazzy package ``ros-jazzy-py-trees``, and it is
   found only after you source ROS 2. ``jsonschema`` is an Ubuntu 24.04
   package. Install whichever is missing, source ROS 2, then go to the folder
   that holds the scripts:

   .. code-block:: bash

      sudo apt install ros-jazzy-py-trees python3-jsonschema
      source /opt/ros/jazzy/setup.bash
      cd lecture11/code

   ``tester_watcher.py`` needs neither package and runs in any Python 3.


.. list-table::
   :header-rows: 1
   :widths: 30 45 25
   :class: compact-table

   * - **Script**
     - **What it shows**
     - **Notes section**
   * - :download:`recovery_tree.py <code/recovery_tree.py>`
     - A selector, a Retry decorator and a guard, in four separate runs with
       injected failures.
     - :ref:`l11-bt-recovery`
   * - :download:`timeout_demo.py <code/timeout_demo.py>`
     - Timeout turns a skill that hangs into a failure the tree can react
       to.
     - :ref:`l11-bt-recovery`
   * - :download:`llm_output_checker.py <code/llm_output_checker.py>`
     - Five layers of checks on scripted LLM replies, and the re-prompt
       once, then fall back policy.
     - :ref:`l11-llm-checks`
   * - :download:`tester_watcher.py <code/tester_watcher.py>`
     - A voltage tester watcher that treats a ``MALFUNCTIONING`` status and
       silence both as failure, and the averaging worked example.
     - :ref:`l11-equipment`
   * - :download:`run_all.sh <code/run_all.sh>`
     - Runs all four scripts and writes their outputs to ``../outputs/``.
     - See the last section


The Recovery Tree: ``recovery_tree.py``
---------------------------------------

Inspection robot 1 must place a cell on a voltage tester. The tree is a
selector with memory on and three children: a guard on tester 1's status
around a Retry that allows 3 failures around ``place_on_tester_1``; then
``place_on_tester_2``; then ``hold_cell``, which is always ``RUNNING``. The
same tree runs four separate times, each with its own injected failure:

- **A:** the place on tester 1 fails once; Retry runs it again.
- **B:** it fails three times; the selector falls back to tester 2.
- **C:** tester 1 reports ``MALFUNCTIONING`` while the place is running; the
  guard stops that branch.
- **D:** as B, but with selector memory off.

``run()`` ticks the tree up to 5 times (4 in Run D) with ``tick_once()``
and stops when
the root is no longer ``RUNNING``. Each ``StubSkill`` follows its script:
``"fail"`` fails on the first tick, and a number ``n`` runs for ``n`` ticks,
then succeeds.

.. code-block:: bash

   python3 recovery_tree.py

.. literalinclude:: code/recovery_tree.py
   :language: python
   :caption: recovery_tree.py

Output:

.. literalinclude:: outputs/recovery_tree.txt
   :language: text


Timeout: ``timeout_demo.py``
----------------------------

A stand-in pick skill returns ``RUNNING`` forever. Timeout fails it after
0.5 s, and the selector moves on to ``report_to_planner``. The tree is ticked
every 0.2 s. Both durations are chosen for this example. This script reads
the wall clock, so on a busy machine a printed time can differ from the
output below.

.. code-block:: bash

   python3 timeout_demo.py

.. literalinclude:: code/timeout_demo.py
   :language: python
   :caption: timeout_demo.py

Output:

.. literalinclude:: outputs/timeout_demo.txt
   :language: text


Checking LLM Output: ``llm_output_checker.py``
----------------------------------------------

``check()`` runs the five layers in order and returns the first failure as
``(layer, message)``, or ``None`` if the reply passes. ``decide()`` plays the
policy: ask, check, re-prompt once with the error, then fall back. The tool
names, the cell IDs and the world state are chosen for this example; the
three AGVs and the four tray slots come from ARIAC 2025.

.. code-block:: bash

   python3 llm_output_checker.py

.. literalinclude:: code/llm_output_checker.py
   :language: python
   :caption: llm_output_checker.py

Output:

.. literalinclude:: outputs/llm_output_checker.txt
   :language: text


The Voltage Tester Watcher: ``tester_watcher.py``
-------------------------------------------------

``TesterWatcher`` applies the four rules from the notes: status first, then
the value, a time limit checked from a timer, and a window of the last good
readings. ``run()`` feeds it 10 readings per second from t = 175.0 s to
230.0 s, with tester 1 failing from 180 s to 225 s. Run 1 sends voltage -1
with ``MALFUNCTIONING`` (the ARIAC code's behavior); Run 2 sends nothing
(the ARIAC docs' behavior). The random noise uses a fixed seed (11), so the
output is the same on every run. The last three lines are the averaging
worked example.

.. code-block:: bash

   python3 tester_watcher.py

.. literalinclude:: code/tester_watcher.py
   :language: python
   :caption: tester_watcher.py

Output:

.. literalinclude:: outputs/tester_watcher.txt
   :language: text


Running All Four: ``run_all.sh``
--------------------------------

``run_all.sh`` is the script that produced the outputs above. It runs each
example in a clean environment (``env -i``) with ROS 2 Jazzy sourced, so the
system Python, the system ``jsonschema`` and the ``py_trees`` from Jazzy are
used even when a virtual environment is active in your shell. It writes the Python, ``py_trees`` and
``jsonschema`` versions to ``../outputs/versions.txt``. You do not need it:
the commands in the sections above give the same results.

.. code-block:: bash

   bash run_all.sh

.. literalinclude:: code/run_all.sh
   :language: bash
   :caption: run_all.sh

Versions used for the outputs on this page:

.. literalinclude:: outputs/versions.txt
   :language: text
