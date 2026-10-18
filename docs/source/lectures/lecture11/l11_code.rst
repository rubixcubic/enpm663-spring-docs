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
     - L8's ``check_call()`` (tool, schema, guard) on scripted replies that
       use the L8 agent's tools, and the re-prompt once, then fall back
       policy through L8's ``run()``.
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

``run()`` ticks the tree up to 6 times (5 in Run D) with ``tick_once()``
and stops when the root is no longer ``RUNNING``. Each ``StubSkill`` follows
its script: ``"fail"`` fails on the first tick, and a number ``n`` runs for
``n`` ticks, then succeeds. ``Robot`` stands for robot 1's action server and
follows two rules of the course skills (README of v0.2.0, "One goal per arm"
and "Cancel stops the arm and retreats"): one goal at a time across all of
robot 1's skills, and a cancel that parks the arm before ``CANCELED`` comes
back, here after ``CANCEL_TICKS = 1`` tick (chosen). A stub sends its goal
only when robot 1 is free, and waits (``RUNNING``) until then.

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

The script imports L8's ``orchestrator``, ``skill_tools`` and
``fake_tools`` from ``lecture8/code`` (see the :doc:`L8 code page
</lectures/lecture8/l8_code>`), so run it from this folder with that folder
next to it, as in the course repository. ``make_state()`` runs eight calls
through L8's ``FakeTools`` (no ARIAC) to build the state, and checks each one
with ``check_call()`` first. The script then checks six separate replies with
``check_call()``, runs none of them, and plays two runs of the policy with
L8's ``run()`` and ``ScriptedModel``: a refused call goes back to the model as
its result, and two refusals in a row end the run (``MAX_INVALID = 2``). The
cell voltages and the tester 1 malfunction are chosen for this example.

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
