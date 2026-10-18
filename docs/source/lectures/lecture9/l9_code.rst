====================================================
Code
====================================================

L9 has two Python scripts. They build on the L8 code, so keep the course
layout: ``lecture9/code/`` next to ``lecture8/code/``, with the outputs in
``lecture9/outputs/``. ``closed_loop.py`` and ``vlm_check.py`` import the L8
files from ``../../lecture8/code``.

- **Offline**, with the system Python and no ARIAC: the scripted VLM check,
  ``python3 vlm_check.py``. Its output repeats exactly.
- **Against ARIAC**, in the course container, with Gemini
  (``gemini-3.5-flash-lite``): the closed loop, with the replan policy and
  with the wait policy, and the live VLM check at the end of the replan run.
  These outputs were recorded once, on 2026-10-17. A rerun gives different
  answers.

Every output on this page is copied from the files the scripts wrote, the
same files the slides show.

.. important::

   **Two kinds of model.** ``stand_in_vlm()`` in ``vlm_check.py`` is a
   scripted stand-in that ignores the prompt and returns canned replies in a
   fixed order, written to hold the mistakes the checks must catch. Its
   ``TRAY_STATUS`` and ``RECORD`` are stand-in values, chosen for this
   example. The closed loop and the live VLM check call Gemini, a real
   model, on the real ARIAC camera image and topics.


.. list-table::
   :header-rows: 1
   :widths: 30 50 20
   :class: compact-table

   * - **File**
     - **What it does**
     - **Runs**
   * - :download:`vlm_check.py <code/vlm_check.py>`
     - The prompts, the schema, ``check()`` and ``cross_check()``. Run on its
       own, it plays the scripted run: a weak prompt, a structured prompt with
       one re-prompt, and a cross-check before a high-priority submit.
       ``live()`` is the live check that ``closed_loop.py`` calls.
     - offline; ``live()`` on ARIAC
   * - :download:`closed_loop.py <code/closed_loop.py>`
     - The L8 orchestrator with Gemini fills agv1's four slots while voltage
       tester 1 malfunctions, under a replan or a wait policy, then prints
       the kit total.
     - ARIAC
   * - :download:`run_sim_demo.sh <code/run_sim_demo.sh>`
     - The L8 ``run_sim_demo.sh`` with ``--lecture 9``. It refuses a trial
       file that still holds ``UNSET_`` placeholders.
     - host
   * - :download:`l9_trial.yaml <code/config/l9_trial.yaml>`,
       :download:`l9_trial_dry.yaml <code/config/l9_trial_dry.yaml>` and
       :download:`l9_user_config.yaml <code/config/l9_user_config.yaml>`
     - The trial file with the tester malfunction, the dry run's trial file
       with no challenge, and the team file with the camera over agv1's tray.
     - ARIAC
   * - :download:`run_all.sh <code/run_all.sh>`
     - Runs the scripted VLM check and writes its output to ``../outputs/``.
     - offline
   * - :download:`listings_l9.json <code/listings_l9.json>`
     - Which lines of each output the slides show (read by L8's
       ``listings.py``).
     - offline

The L8 files these scripts use (``orchestrator.py``, ``skill_tools.py``,
``gemini_model.py``, ``run_sim_demo.sh`` and the rest) are on the
:doc:`L8 code page </lectures/lecture8/l8_code>`, with the lecture's virtual
environment and where the API key goes.


The Scripted VLM Check: ``vlm_check.py``
----------------------------------------

.. note::

   **What you need.** Python 3 and the ``jsonschema`` package. On Ubuntu
   24.04: ``sudo apt install python3-jsonschema``. No ROS 2 setup is needed
   for the scripted run.

The scripted run plays one high-priority order check. The stand-in VLM
answers three times: a paragraph for the weak prompt, a reply that numbers
the slots 0 to 3, and a valid reply with two mistakes. ``TRAY_STATUS`` stands
in for one ``/agv1/tray_status`` message. ``RECORD`` stands in for the
orchestrator's own record: the voltage each cell read on a tester before it
was placed.

.. code-block:: bash

   cd lecture9/code
   python3 vlm_check.py

.. literalinclude:: code/vlm_check.py
   :language: python
   :caption: vlm_check.py

Output (scripted model: fixed replies):

.. literalinclude:: outputs/vlm_check.txt
   :language: text


The Closed Loop on ARIAC: ``closed_loop.py``
--------------------------------------------

The script runs the L8 loop (``orchestrator.run``) with Gemini and the L9
tools: the ten L8 tools and ``wait``. ``--policy replan`` offers every tool
but ``wait``, so a run must replan around the broken tester to finish.
``--policy wait`` declares the tester argument as 1 only, adds one line to
the goal, and keeps a guard in code that refuses tester 2. The goal, checked
in code, is all four slots of agv1 filled, each cell with a recorded voltage
from 3.4 to 3.8 V. After the loop, the script prints the kit total against
14.25 to 14.55 V as a fact; it does not stop the run. ``--vlm-after`` then
runs the live VLM check on the camera image.

With no key file, the script runs the scripted model instead of Gemini and
skips the live VLM check. ``--scripted --image-only`` is the dry run that
timed the cycles.

.. literalinclude:: code/closed_loop.py
   :language: python
   :caption: closed_loop.py

The commands that made the L9 recordings, run on the host from
``lecture9/code`` (the steps before them, the virtual environment and the
key, are on the :doc:`L8 code page </lectures/lecture8/l8_code>`):

.. code-block:: bash

   # the dry run: scripted model, no challenge, one image with the first cell
   bash run_sim_demo.sh --name closed_loop_dry --sim config/l9_trial_dry.yaml \
       config/l9_user_config.yaml 3600 -- closed_loop.py --policy replan --scripted --image-only
   # the replan recording, then the live VLM check
   bash run_sim_demo.sh --name closed_loop_replan_rec1 --sim config/l9_trial.yaml \
       config/l9_user_config.yaml 3600 --key -- closed_loop.py --policy replan --vlm-after
   # the wait recording
   bash run_sim_demo.sh --name closed_loop_wait_rec1 --sim config/l9_trial.yaml \
       config/l9_user_config.yaml 3600 --key -- closed_loop.py --policy wait

.. literalinclude:: code/run_sim_demo.sh
   :language: bash
   :caption: run_sim_demo.sh

.. literalinclude:: code/config/l9_trial.yaml
   :language: yaml
   :caption: config/l9_trial.yaml

.. literalinclude:: code/config/l9_trial_dry.yaml
   :language: yaml
   :caption: config/l9_trial_dry.yaml

.. literalinclude:: code/config/l9_user_config.yaml
   :language: yaml
   :caption: config/l9_user_config.yaml

The Replan Recording
~~~~~~~~~~~~~~~~~~~~

Recorded once, on 2026-10-17, with gemini-3.5-flash-lite. A rerun gives
different answers. Recording 1 of 1.

.. note::

   The live check prints "Cross-check before /submit_high_priority_order",
   but this Li-Ion kit would go to ``/submit_kitting_order``. A comment in
   ``live()`` says so; the printed line stays as recorded.

.. literalinclude:: outputs/closed_loop_replan_rec1.txt
   :language: text

Tokens, latency and cost per call (written by L8's ``run_cost.py`` from the
raw API responses; call 27 is the VLM call):

.. literalinclude:: outputs/closed_loop_replan_rec1_cost.txt
   :language: text

The Wait Recording
~~~~~~~~~~~~~~~~~~

Recorded once, on 2026-10-17, with gemini-3.5-flash-lite. A rerun gives
different answers. Recording 1 of 1.

.. literalinclude:: outputs/closed_loop_wait_rec1.txt
   :language: text

.. literalinclude:: outputs/closed_loop_wait_rec1_cost.txt
   :language: text

The Dry Run
~~~~~~~~~~~

Scripted model: fixed replies, on ARIAC with no challenge. Its cycle times
set ``START_TIME`` and ``DURATION`` in ``l9_trial.yaml`` (see the comments
there).

.. literalinclude:: outputs/closed_loop_dry.txt
   :language: text


Running the Offline Part: ``run_all.sh``
----------------------------------------

``run_all.sh`` is the script that produced ``vlm_check.txt``. It runs the
script in a clean environment (``env -i``), so the system Python and its
``jsonschema`` are used even when a ROS 2 or virtual environment is active in
your shell. It also runs the lecture's tests and checks every slide listing
against its source in ``lecture9/outputs/``: ``closed_loop_replan_rec1.txt``,
``closed_loop_wait_rec1.txt`` or ``vlm_check.txt``. The tests and the slides
are in the course's slides repository, not on this page; ``python3
vlm_check.py`` gives the same output.

.. literalinclude:: code/run_all.sh
   :language: bash
   :caption: run_all.sh

.. literalinclude:: code/listings_l9.json
   :language: json
   :caption: listings_l9.json

Versions used for the outputs on this page:

.. literalinclude:: outputs/versions.txt
   :language: text
