====================================================
Code
====================================================

L6 has two PDDL domains, three PDDL problems, seven Python scripts and one
shell script that runs them all. None of them uses ROS 2 or the ARIAC
simulation: the planner works on PDDL files, and the factory state is a
Python dictionary with values chosen for the examples. The outputs below come
from running ``run_all.sh`` on 2026-10-12:

.. literalinclude:: outputs/versions.txt
   :language: text
   :caption: outputs/versions.txt

.. note::

   **What you need.** Ubuntu 24.04 with its Python 3 (3.12.3 on the course
   machine), and a virtual environment with the Unified Planning Framework
   and its Fast Downward engine:

   .. code-block:: bash

      python3 -m venv ~/venvs/planning
      ~/venvs/planning/bin/pip install unified-planning up-fast-downward

   This installs ``unified-planning`` 1.3.0 and ``up-fast-downward`` 1.0.0
   (checked on 2026-10-12). The up-fast-downward package ships a built Fast
   Downward, so there is nothing to compile. Two things to know:

   - The UPF installation page lists Python 3.8 to 3.11; every demo here ran
     on Python 3.12.3.
   - ``pip install unified-planning[fast-downward]``, the form on the
     up-fast-downward page, installed up-fast-downward 0.5.2 instead. Use
     the command above.

   Download the files below into one folder, ``code/``, and make an empty
   ``outputs/`` folder next to it: the scripts read and write
   ``../outputs/``. Then activate the venv and go to ``code/``:

   .. code-block:: bash

      mkdir -p lecture6/outputs
      source ~/venvs/planning/bin/activate
      cd lecture6/code

   Every command on this page runs from ``code/``, with the venv active.
   ``select_cells.py`` needs nothing but Python, so it also runs with
   ``/usr/bin/python3``.


.. list-table::
   :header-rows: 1
   :widths: 32 43 25
   :class: compact-table

   * - **File**
     - **What it is**
     - **Notes section**
   * - :download:`domain.pddl <code/domain.pddl>`
     - The Task 1 domain: 6 types, 16 predicates, 8 actions.
     - :ref:`l6-domain`
   * - :download:`problem.pddl <code/problem.pddl>`
     - Four cells for one kit on agv1.
     - :ref:`l6-problem`
   * - :download:`plan_kit.py <code/plan_kit.py>`
     - Demo 1: load the domain and problem, plan, print the plan, write
       ``../outputs/plan.txt``.
     - :ref:`l6-planner`
   * - :download:`validate_plan.py <code/validate_plan.py>`
     - Demo 2: validate ``plan.txt`` and a copy with steps 6 and 7 swapped.
     - :ref:`l6-checking`
   * - :download:`gen_problem.py <code/gen_problem.py>`
     - Demo 3: write a problem from a stand-in factory state, then plan.
       Also defines ``make_problem()``.
     - :ref:`l6-generator`
   * - :download:`compare_planners.py <code/compare_planners.py>`
     - Demo 4: satisficing against optimal, on 4 cells and on 8 cells.
     - :ref:`l6-compare`
   * - :download:`mistakes.py <code/mistakes.py>`
     - Demo 5: two modeling mistakes and the plans they produce.
     - :ref:`l6-mistakes`
   * - :download:`select_cells.py <code/select_cells.py>`
     - Demo 6: the kit voltage window and the selection step, without and
       with look-ahead.
     - :ref:`l6-selection`
   * - :download:`numeric_try.py <code/numeric_try.py>`
     - Demo 7: give Fast Downward the kit window as numeric PDDL.
     - :ref:`l6-strains`
   * - :download:`kit_numeric.pddl <code/kit_numeric.pddl>`,
       :download:`kit_numeric_problem.pddl <code/kit_numeric_problem.pddl>`
     - The numeric domain and problem that ``numeric_try.py`` loads.
     - :ref:`l6-strains`
   * - :download:`run_all.sh <code/run_all.sh>`
     - Runs every example, and Fast Downward from the command line, and
       writes the outputs to ``../outputs/``.
     - See the last section


The domain and the problem
--------------------------

.. literalinclude:: code/domain.pddl
   :language: lisp
   :caption: domain.pddl

.. literalinclude:: code/problem.pddl
   :language: lisp
   :caption: problem.pddl


Demo 1: ``plan_kit.py``
-----------------------

Loads ``domain.pddl`` and ``problem.pddl`` with UPF, plans with Fast Downward
(``lama-first``), prints the plan and writes it in PDDL form to
``../outputs/plan.txt``. Run it before ``validate_plan.py``, which reads that
file.

.. code-block:: bash

   python plan_kit.py

.. literalinclude:: code/plan_kit.py
   :language: python
   :caption: plan_kit.py

.. literalinclude:: outputs/plan_kit.txt
   :language: text
   :caption: outputs/plan_kit.txt

.. literalinclude:: outputs/plan.txt
   :language: text
   :caption: outputs/plan.txt


Demo 2: ``validate_plan.py``
----------------------------

Writes ``../outputs/plan_swapped.txt``, a copy of ``plan.txt`` with steps 6
and 7 swapped, then validates both plans with UPF's ``PlanValidator``.

.. code-block:: bash

   python validate_plan.py

.. literalinclude:: code/validate_plan.py
   :language: python
   :caption: validate_plan.py

.. literalinclude:: outputs/validate_plan.txt
   :language: text
   :caption: outputs/validate_plan.txt

.. literalinclude:: outputs/plan_swapped.txt
   :language: text
   :caption: outputs/plan_swapped.txt


Demo 3: ``gen_problem.py``
--------------------------

``make_problem(state)`` turns a factory state (a Python dictionary) into the
text of a PDDL problem. Run as a script, it writes the problem for ``STATE``
(four cells at the door, c5 on tester2 at 3.86 V) to
``../outputs/problem_generated.pddl`` and plans it.

.. code-block:: bash

   python gen_problem.py

.. literalinclude:: code/gen_problem.py
   :language: python
   :caption: gen_problem.py

.. literalinclude:: outputs/problem_generated.pddl
   :language: lisp
   :caption: outputs/problem_generated.pddl

.. literalinclude:: outputs/gen_problem.txt
   :language: text
   :caption: outputs/gen_problem.txt


Demo 4: ``compare_planners.py``
-------------------------------

Writes ``../outputs/problem_large.pddl`` (8 cells, 2 AGVs) with
``make_problem()``, then solves the small and the large problem with
``fast-downward`` (``lama-first``) and ``fast-downward-opt`` (A* with
LM-cut). It imports ``gen_problem.py``, so keep both in ``code/``. The large
optimal run takes about 15 s.

.. code-block:: bash

   python compare_planners.py

.. literalinclude:: code/compare_planners.py
   :language: python
   :caption: compare_planners.py

.. literalinclude:: outputs/compare_planners.txt
   :language: text
   :caption: outputs/compare_planners.txt

The times are wall-clock seconds for one run. A second run on the same
machine gave 0.14 s, 0.60 s and 13.98 s for the last three lines; the step
counts did not change.

.. dropdown:: outputs/problem_large.pddl
   :class-container: sd-border-secondary

   .. literalinclude:: outputs/problem_large.pddl
      :language: lisp


Demo 5: ``mistakes.py``
-----------------------

Removes one piece of ``domain.pddl`` in memory (the file is not changed),
plans ``problem.pddl`` with the changed domain, and prints the steps that
show the mistake. Each entry of ``MISTAKES`` is the text to find, its
replacement, and the step numbers to print.

.. code-block:: bash

   python mistakes.py

.. literalinclude:: code/mistakes.py
   :language: python
   :caption: mistakes.py

.. literalinclude:: outputs/mistakes.txt
   :language: text
   :caption: outputs/mistakes.txt


Demo 6: ``select_cells.py``
---------------------------

The kit voltage window in plain Python, with the Li-Ion limits from ARIAC's
``CellTypes.msg``. It needs no package.

.. code-block:: bash

   python select_cells.py

.. literalinclude:: code/select_cells.py
   :language: python
   :caption: select_cells.py

.. literalinclude:: outputs/select_cells.txt
   :language: text
   :caption: outputs/select_cells.txt


Demo 7: ``numeric_try.py``
--------------------------

Loads the numeric kit domain and problem and asks Fast Downward for a plan.
Fast Downward stops at ``:numeric-fluents``.

.. code-block:: bash

   python numeric_try.py

.. literalinclude:: code/kit_numeric.pddl
   :language: lisp
   :caption: kit_numeric.pddl

.. literalinclude:: code/kit_numeric_problem.pddl
   :language: lisp
   :caption: kit_numeric_problem.pddl

.. literalinclude:: code/numeric_try.py
   :language: python
   :caption: numeric_try.py

.. literalinclude:: outputs/numeric_try.txt
   :language: text
   :caption: outputs/numeric_try.txt


Run everything: ``run_all.sh``
------------------------------

``run_all.sh`` runs the seven demos in order, then runs Fast Downward from
the command line (A* with LM-cut) on the small and the large problem. Give it
the venv folder in ``VENV``:

.. code-block:: bash

   VENV=~/venvs/planning bash run_all.sh

.. literalinclude:: code/run_all.sh
   :language: bash
   :caption: run_all.sh

The script runs each program in a clean shell (``env -i``), so the paths of
the shell you start it from do not matter. It finds ``fast-downward.py`` in
the up-fast-downward package folder, under ``downward/``. It keeps Fast
Downward's translated task in a temporary folder, counts the ground actions
of each kind in it, and deletes the folder at the end.

Besides the outputs above, it writes:

.. literalinclude:: outputs/fd_summary.txt
   :language: text
   :caption: outputs/fd_summary.txt

.. literalinclude:: outputs/ground_actions.txt
   :language: text
   :caption: outputs/ground_actions.txt

.. literalinclude:: outputs/fd_small.plan
   :language: text
   :caption: outputs/fd_small.plan

.. dropdown:: outputs/fd_large.plan
   :class-container: sd-border-secondary

   .. literalinclude:: outputs/fd_large.plan
      :language: text

It also writes Fast Downward's full logs, ``fd_small.log`` and
``fd_large.log``. They are not on this page: the lines the notes use are
collected in ``fd_summary.txt``. The search times in ``fd_summary.txt``
change from run to run (a second run gave 0.013089 s and 14.419236 s); the
operator counts, plan lengths and expanded states did not.
