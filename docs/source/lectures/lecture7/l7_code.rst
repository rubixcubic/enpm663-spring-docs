====================================================
Code
====================================================

L7 has six Python scripts, one shared Python module, and one BehaviorTree.CPP
example in C++ and XML. None of them uses ROS communication or the ARIAC
simulation: the skills, the testers and the AGV are **mock** stand-ins written
in Python. The outputs below come from running ``run_all.sh`` on 2026-10-12:

.. literalinclude:: outputs/versions.txt
   :language: text
   :caption: outputs/versions.txt

.. note::

   **What you need.** Ubuntu 24.04 with ROS 2 Jazzy. The Python scripts need
   ``py_trees``, which comes from the Jazzy package ``ros-jazzy-py-trees``.
   The C++ example needs **BehaviorTree.CPP**, which comes from the Jazzy
   package ``ros-jazzy-behaviortree-cpp`` (version 4.10.0 on the course
   machine), and ``g++``. The ``ros-jazzy-desktop`` package does not bring
   in either library (checked with ``apt-cache depends`` on 2026-10-12), so
   install them with:

   .. code-block:: bash

      sudo apt install ros-jazzy-py-trees ros-jazzy-behaviortree-cpp g++

   Download the files below into one folder, ``code/``, with the two
   BehaviorTree.CPP files in ``code/btcpp/``. Open a terminal, source ROS 2
   once, and go to that folder:

   .. code-block:: bash

      source /opt/ros/jazzy/setup.bash
      cd lecture7/code

   Every command on this page runs from ``code/``.


.. list-table::
   :header-rows: 1
   :widths: 30 45 25
   :class: compact-table

   * - **File**
     - **What it is**
     - **Notes section**
   * - :download:`executor.py <code/executor.py>`
     - The plan-to-BT executor: the mock factory, the guard, act, verify and
       update leaves, the builders, the registry, ``build_tree`` and the tick
       logger. The demos import it.
     - :ref:`l7-factory`
   * - :download:`demo_factory.py <code/demo_factory.py>`
     - Demo 1: a five-step plan becomes a tree, and two bugs (no memory, no
       guards).
     - :ref:`l7-demo1`, :ref:`l7-debugging`
   * - :download:`demo_retry.py <code/demo_retry.py>`
     - Demo 2: Retry around a pick that fails.
     - :ref:`l7-retry`
   * - :download:`demo_timeout.py <code/demo_timeout.py>`
     - Demo 3: Timeout around a leaf that waits for valid voltage readings.
     - :ref:`l7-retry-timeout`
   * - :download:`demo_nesting.py <code/demo_nesting.py>`
     - Demo 4: ``Retry(Timeout(act))`` against ``Timeout(Retry(act))``.
     - :ref:`l7-nesting`
   * - :download:`demo_replan.py <code/demo_replan.py>`
     - Demo 5: the replanning loop on a cell with a bad voltage.
     - :ref:`l7-demo5`
   * - :download:`btcpp/place_cell.xml <code/btcpp/place_cell.xml>`
     - The BehaviorTree.CPP tree.
     - :ref:`l7-btcpp`
   * - :download:`btcpp/place_cell.cpp <code/btcpp/place_cell.cpp>`
     - The C++ nodes and the program that loads and ticks the XML tree.
     - :ref:`l7-btcpp`
   * - :download:`demo_place_cell.py <code/demo_place_cell.py>`
     - The same tree in ``py_trees``.
     - :ref:`l7-btcpp`
   * - :download:`run_all.sh <code/run_all.sh>`
     - Runs every example and writes its output to ``../outputs/``.
     - See the last section


The executor: ``executor.py``
-----------------------------

``executor.py`` is not run on its own. It holds everything the demos share:

- ``MockFactory``: what is really true in the mock factory (which cell is on
  each tester, what the robot holds, what is in each tray slot, where the AGV
  is). The skills are methods: ``pick_from_tester``, ``place_in_slot``,
  ``drop_in_recycling`` and ``move``. ``inject`` makes a skill fail a set
  number of times with ``GRASP_FAILED``.
- The four leaf types ``Guard``, ``Act``, ``Verify`` and ``Update``, and
  ``ReadAverage``, the act leaf of ``check-voltage``.
- One builder per action name, ``REGISTRY``, ``RETRIES`` and
  ``build_tree``, the plan-to-BT factory.
- ``run``, which ticks a tree and logs each step's status changes (the tick
  trace).

The blackboard holds two entries: ``/facts``, the executor's facts as a set of
tuples such as ``("on-tester", "c3", "tester1")``, and ``/volts``, the
averaged voltage of each measured cell.

.. literalinclude:: code/executor.py
   :language: python
   :caption: executor.py


Demo 1: ``demo_factory.py``
---------------------------

A five-step plan (two picks, two places, one AGV move) built into a tree and
ticked. The argument picks what the script does.

.. code-block:: bash

   python3 demo_factory.py build      # print the plan and the tree's size
   python3 demo_factory.py tick       # print the tree after two ticks
   python3 demo_factory.py trace      # tick to the end, log each change
   python3 demo_factory.py unknown    # step 5 misspelled: move-avg
   python3 demo_factory.py nomemory   # the root without memory
   python3 demo_factory.py noguard    # no memory, and guards that always pass

.. literalinclude:: code/demo_factory.py
   :language: python
   :caption: demo_factory.py

.. literalinclude:: outputs/factory_build.txt
   :language: text
   :caption: build

.. literalinclude:: outputs/factory_tick.txt
   :language: text
   :caption: tick

.. literalinclude:: outputs/factory_trace.txt
   :language: text
   :caption: trace

.. literalinclude:: outputs/factory_unknown.txt
   :language: text
   :caption: unknown

.. literalinclude:: outputs/factory_nomemory.txt
   :language: text
   :caption: nomemory

.. literalinclude:: outputs/factory_noguard.txt
   :language: text
   :caption: noguard

These outputs count ticks, not seconds, so yours should match them exactly.


Demo 2: ``demo_retry.py``
-------------------------

A two-step plan (pick ``c3`` from ``tester1``, place it in ``s3``) with
``RETRIES["pick-from-tester"] = 3``. The argument is how many times the mock
pick fails before it succeeds.

.. code-block:: bash

   python3 demo_retry.py 2
   python3 demo_retry.py 3

.. literalinclude:: code/demo_retry.py
   :language: python
   :caption: demo_retry.py

.. literalinclude:: outputs/retry_2.txt
   :language: text
   :caption: demo_retry.py 2

.. literalinclude:: outputs/retry_3.txt
   :language: text
   :caption: demo_retry.py 3


Demo 3: ``demo_timeout.py``
---------------------------

A leaf that needs 10 valid readings from a mock tester that publishes every
0.1 s, inside ``Timeout(duration=2.0)``, ticked every 0.05 s. The argument
picks the tester's behavior: ``normal`` sends 3.62 V with ``OPERATIONAL``,
``silent`` sends nothing (as the ARIAC docs describe the malfunction), and
``malfunction`` sends −1 with ``MALFUNCTIONING`` (as the ARIAC 2025 code
does).

.. code-block:: bash

   python3 demo_timeout.py normal
   python3 demo_timeout.py silent
   python3 demo_timeout.py malfunction

.. literalinclude:: code/demo_timeout.py
   :language: python
   :caption: demo_timeout.py

.. literalinclude:: outputs/timeout_normal.txt
   :language: text
   :caption: demo_timeout.py normal

.. literalinclude:: outputs/timeout_silent.txt
   :language: text
   :caption: demo_timeout.py silent

.. literalinclude:: outputs/timeout_malfunction.txt
   :language: text
   :caption: demo_timeout.py malfunction

The script measures real time, so the last digit can differ on your machine.
A rerun on the course machine on 2026-10-12 printed 2.01 s for
``malfunction`` instead of 2.00 s.


Demo 4: ``demo_nesting.py``
---------------------------

The two nesting orders of Retry and Timeout, five runs of each. The limit is
0.2 s, ``num_failures`` is 3 and the tick period is 0.02 s. ``hang`` gives an
act that never finishes; ``fail`` gives an act that fails after 0.15 s.
``--starts`` also prints when each attempt of run 1 started (the figure in the
notes uses these times).

.. code-block:: bash

   python3 demo_nesting.py hang --starts
   python3 demo_nesting.py fail

.. literalinclude:: code/demo_nesting.py
   :language: python
   :caption: demo_nesting.py

.. literalinclude:: outputs/nesting_hang.txt
   :language: text
   :caption: ``demo_nesting.py hang --starts``

.. literalinclude:: outputs/nesting_fail.txt
   :language: text
   :caption: demo_nesting.py fail

When the five runs differ, the script prints the range ("0.52 to 0.53 s").
A rerun on the course machine on 2026-10-12 printed that range for
``Retry(Timeout(act))`` in ``fail``, where the file above shows 0.52 s.


Demo 5: ``demo_replan.py``
--------------------------

The replanning loop: plan 1, a failed voltage check, a new problem, plan 2 and
the shipped kit. It takes no argument.

.. code-block:: bash

   python3 demo_replan.py

.. literalinclude:: code/demo_replan.py
   :language: python
   :caption: demo_replan.py

.. literalinclude:: outputs/replan.txt
   :language: text
   :caption: demo_replan.py


.. _l7-code-btcpp:

BehaviorTree.CPP: ``btcpp/place_cell.cpp`` and ``place_cell.xml``
-----------------------------------------------------------------

The ``PlaceCell`` tree: a pick with up to three attempts, then a place. The
program takes two arguments: the XML file and how many times the mock pick
fails before it succeeds.

.. literalinclude:: code/btcpp/place_cell.xml
   :language: xml
   :caption: btcpp/place_cell.xml

.. literalinclude:: code/btcpp/place_cell.cpp
   :language: cpp
   :caption: btcpp/place_cell.cpp

**Build it** with the same ``g++`` command that ``run_all.sh`` uses. The
headers and the library come from ``/opt/ros/jazzy``, which the
``ros-jazzy-behaviortree-cpp`` package installs. ``run_all.sh`` writes the
program to a temporary folder and deletes it at the end; here it goes in
``code/`` as ``place_cell``:

.. code-block:: bash

   g++ -std=c++17 btcpp/place_cell.cpp -I/opt/ros/jazzy/include \
     -L/opt/ros/jazzy/lib -lbehaviortree_cpp \
     -Wl,-rpath,/opt/ros/jazzy/lib -o place_cell

**Run it** in the terminal where you sourced ROS 2:

.. code-block:: bash

   ./place_cell btcpp/place_cell.xml 1
   ./place_cell btcpp/place_cell.xml 3

.. warning::

   Source ``/opt/ros/jazzy/setup.bash`` before you run the program, even
   though the ``g++`` line sets a library path. On the course machine
   (2026-10-12), in a shell that had not sourced ROS 2, the program stopped
   with ``error while loading shared libraries: libament_index_cpp.so``:
   ``libbehaviortree_cpp.so`` needs that library, and the ``-rpath`` setting
   covers only the libraries the program links to directly.

.. literalinclude:: outputs/btcpp_1.txt
   :language: text
   :caption: ./place_cell btcpp/place_cell.xml 1

.. literalinclude:: outputs/btcpp_3.txt
   :language: text
   :caption: ./place_cell btcpp/place_cell.xml 3

The program gives ``createTreeFromFile`` the full path of the XML file
(``std::filesystem::absolute``), so it also runs from another folder.


The same tree in ``py_trees``: ``demo_place_cell.py``
-----------------------------------------------------

.. code-block:: bash

   python3 demo_place_cell.py 1
   python3 demo_place_cell.py 3

.. literalinclude:: code/demo_place_cell.py
   :language: python
   :caption: demo_place_cell.py

.. literalinclude:: outputs/pytrees_1.txt
   :language: text
   :caption: demo_place_cell.py 1

.. literalinclude:: outputs/pytrees_3.txt
   :language: text
   :caption: demo_place_cell.py 3


Run everything: ``run_all.sh``
------------------------------

``run_all.sh`` runs every example above, writes each output to
``../outputs/`` (create that folder next to ``code/`` first), builds and runs
the C++ example, and writes ``versions.txt``.

.. code-block:: bash

   mkdir -p ../outputs
   bash run_all.sh

.. literalinclude:: code/run_all.sh
   :language: bash
   :caption: run_all.sh

The script runs each example in a clean shell (``env -i``) that sources
ROS 2 Jazzy, so the paths of the shell you start it from do not matter. It
also sets ``ROS_DOMAIN_ID`` to 87. No example sends ROS messages, so the
domain does not change any result; it is a habit of the course machine, which
runs a simulation on domain 0.
