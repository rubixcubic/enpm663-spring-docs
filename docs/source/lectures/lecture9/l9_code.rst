====================================================
Code
====================================================

L9 has two short Python scripts. Neither one needs ROS, a simulator or a
model: both run in plain Python and print a trace. The outputs below come from
running them with Python 3.12.3 and jsonschema 4.10.3.

.. important::

   **Both scripts use scripted stand-ins.** ``stand_in_vlm()`` in
   ``vlm_check.py`` and ``stand_in_model()`` in ``closed_loop.py`` ignore the
   prompt and return canned replies in a fixed order. The replies were written
   to contain the mistakes the checks must catch. A real model's answers vary.
   The ``Factory`` class in ``closed_loop.py`` stands in for the ARIAC topics
   and the robot skills. Its payloads copy ARIAC 2025, but nothing moves.

.. note::

   **What you need.** Python 3 and the ``jsonschema`` package. On Ubuntu 24.04:
   ``sudo apt install python3-jsonschema``. No ROS 2 setup is needed for these
   two scripts. Go to the folder that holds them:

   .. code-block:: bash

      cd lecture9/code


.. list-table::
   :header-rows: 1
   :widths: 30 45 25
   :class: compact-table

   * - **Script**
     - **What it shows**
     - **Notes section**
   * - :download:`vlm_check.py <code/vlm_check.py>`
     - A weak prompt, a structured prompt with a schema and one re-prompt, and
       a slot-by-slot cross-check of the VLM's record before a high-priority
       submit.
     - :ref:`l9-checking`
   * - :download:`closed_loop.py <code/closed_loop.py>`
     - A closed agent loop that waits through a conveyor malfunction, replans
       around a broken tester and retries a lost grasp. ``--wait`` waits for
       the tester instead.
     - :ref:`l9-demo`
   * - :download:`run_all.sh <code/run_all.sh>`
     - Runs both scripts and writes their outputs to ``../outputs/``.
     - See the last section


Checking a VLM's Record: ``vlm_check.py``
-----------------------------------------

The script plays one high-priority order check. The stand-in VLM answers three
times: a paragraph for the weak prompt, a reply that numbers the slots 0 to 3,
and a valid reply with two mistakes. ``TRAY_STATUS`` stands in for one
``/agv1/tray_status`` message. ``RECORD`` stands in for the orchestrator's own
record: the voltage each cell read on a tester before it was placed. These
values are chosen for this example.

.. code-block:: bash

   python3 vlm_check.py

.. literalinclude:: code/vlm_check.py
   :language: python
   :caption: vlm_check.py

Output:

.. literalinclude:: outputs/vlm_check.txt
   :language: text


The Closed Loop: ``closed_loop.py``
-----------------------------------

The script builds one Li-Ion kit on agv1. The conveyor malfunction, the tester
malfunction, the action times, the cell voltages and the lost grasp are chosen
for this example; the malfunction keys (``START_TIME``, ``DURATION``,
``TESTER``) are those of an ARIAC trial file. You can change them at the top of
the script: Exercise 3 on the :doc:`exercises page <l9_exercises>` does.

.. note::

   **The action names are stand-ins.** ``load_tester`` and
   ``unload_to_tray`` are names made up for this demonstration, not the names
   of the course skills package's skills. ``move_agv`` stands in for ARIAC's
   own ``/{agv_name}/move`` action. ``Factory.run()`` only advances a clock and
   updates a few Python variables.

.. code-block:: bash

   python3 closed_loop.py           # replan around a broken tester
   python3 closed_loop.py --wait    # wait for a broken tester instead

.. literalinclude:: code/closed_loop.py
   :language: python
   :caption: closed_loop.py

Output without ``--wait``:

.. literalinclude:: outputs/closed_loop.txt
   :language: text

Output with ``--wait``:

.. literalinclude:: outputs/closed_loop_wait.txt
   :language: text

The two runs are the same until t = 145 s. From there the first replans and
finishes at 245 s after 3 model calls; the second waits for tester 1 and
finishes at 285 s after 1 model call. The stand-in model's calls take 0 s, so
the times count only the actions and the waiting.


Running Both: ``run_all.sh``
----------------------------

``run_all.sh`` is the script that produced the outputs above. It runs each
example in a clean environment (``env -i``), so the system Python and its
``jsonschema`` are used even when a ROS 2 or virtual environment is active in
your shell. It writes the Python and jsonschema versions to
``../outputs/versions.txt``. You do not need it: the commands in the sections
above give the same results.

.. literalinclude:: code/run_all.sh
   :language: bash
   :caption: run_all.sh

Versions used for the outputs on this page:

.. literalinclude:: outputs/versions.txt
   :language: text
