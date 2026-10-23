====================================================
Code
====================================================

L4 has six Python scripts and one shell script. Four scripts use ``py_trees``
alone and tick a tree of stand-in leaves: no robot, no ROS 2 node and no
simulator. The fifth, ``ros_tree_demo.py``, runs a ``py_trees_ros`` tree as a
ROS 2 node against stand-ins for the ARIAC voltage tester, two course skills
and the kit check service, all in the same process. The sixth,
``kit_spread.py``, is plain Python: it computes the noise in a kit total built
from averaged readings. The outputs below come from running them on
ROS 2 Jazzy on 2026-10-12; ``kit_spread.py`` and the five sets of ten timeout
runs were added on 2026-10-18.

.. note::

   **What you need.** Ubuntu 24.04 with ROS 2 Jazzy, and the ``py_trees`` and
   ``py_trees_ros`` packages for Jazzy. The outputs come from these versions:

   .. literalinclude:: outputs/versions.txt
      :language: text

   If ``python3 -c "import py_trees_ros"`` fails after you source ROS 2,
   install the packages with
   ``sudo apt install ros-jazzy-py-trees ros-jazzy-py-trees-ros``.
   ``ros_tree_demo.py`` also uses ``control_msgs``, which an ARIAC install
   brings in; without ARIAC, install it with
   ``sudo apt install ros-jazzy-control-msgs``.

   Open a terminal, source ROS 2 once, and go to the folder that holds the
   scripts:

   .. code-block:: bash

      source /opt/ros/jazzy/setup.bash
      cd lecture4/code

   If an ARIAC simulation is running on the same machine, give
   ``ros_tree_demo.py`` a ROS domain of its own, for example
   ``export ROS_DOMAIN_ID=84``, so its topics do not mix with the
   simulation's.


.. list-table::
   :header-rows: 1
   :widths: 30 45 25
   :class: compact-table

   * - **Script**
     - **What it shows**
     - **Notes section**
   * - :download:`composite_status.py <code/composite_status.py>`
     - The status a sequence, a selector and three decorators return from
       their children's statuses.
     - :ref:`l4-primitives`
   * - :download:`parallel_watch.py <code/parallel_watch.py>`
     - A parallel that watches the tester while it waits for five readings,
       with ``synchronise`` True and False.
     - :ref:`l4-parallel`
   * - :download:`retry_demo.py <code/retry_demo.py>`
     - A ``Retry`` around a pick that fails once, in a sequence with memory
       and without memory.
     - :ref:`l4-memory`
   * - :download:`blackboard_demo.py <code/blackboard_demo.py>`
     - Blackboard keys for three cells, and a reader that tries to write.
     - :ref:`l4-blackboards`
   * - :download:`ros_tree_demo.py <code/ros_tree_demo.py>`
     - A ``py_trees_ros`` tree with subscriber, action and service leaves, in
       three runs.
     - :ref:`l4-py-trees-ros`
   * - :download:`kit_spread.py <code/kit_spread.py>`
     - How far the sum of four averaged voltages wanders, by formula and
       in 100,000 simulated kits.
     - :ref:`l4-patterns`
   * - :download:`run_all.sh <code/run_all.sh>`
     - Runs all six and writes their outputs to ``../outputs/``.
     - See the last section


Composites and Decorators: ``composite_status.py``
--------------------------------------------------

Each case builds a fresh composite or decorator over stand-in leaves
(``Fixed``) that each return one status, ticks it once, and prints each
child's status and then the parent's after the arrow. ``INVALID`` means the
child was not ticked. The last case ticks a ``Timeout`` of 0.2 s twice, 0.3 s
apart.

.. code-block:: bash

   python3 composite_status.py

.. literalinclude:: code/composite_status.py
   :language: python
   :caption: composite_status.py

.. literalinclude:: outputs/composite_status.txt
   :language: text


Parallel and ``synchronise``: ``parallel_watch.py``
---------------------------------------------------

A parallel ``wait_for_reading`` has two children: ``tester_ok`` (a condition)
and ``wait_for_voltage`` (one reading per tick, ``SUCCESS`` after five). The
policy is ``SuccessOnSelected([wait])``. The stand-in tester reads 3.61 V and
is ``OPERATIONAL`` on tick 1, then reads −1.0 V and is ``MALFUNCTIONING``
(values chosen for this example). The script runs the tree with
``synchronise=True`` (the ``py_trees`` default) and with ``False``.

.. code-block:: bash

   python3 parallel_watch.py

.. literalinclude:: code/parallel_watch.py
   :language: python
   :caption: parallel_watch.py

.. literalinclude:: outputs/parallel_watch.txt
   :language: text


Retry and Memory: ``retry_demo.py``
-----------------------------------

A sequence ``move_cell``: ``check_tester_ok``, then a ``Retry`` (up to 2
failures) around ``pick_from_tester``, then ``place_in_slot``. ``Step`` is a
stand-in leaf that returns ``RUNNING`` for ``run_ticks`` ticks, then the next
of its scripted results. The pick fails on its first attempt and succeeds on
its second. The script builds the tree with ``memory=True`` and with
``memory=False``, ticks each up to 14 times, and prints every leaf's status
after each tick.

.. code-block:: bash

   python3 retry_demo.py

To change the run, edit ``build``: ``num_failures`` in the ``Retry``, the list
of results given to the pick, or the ``memory`` values in the loop at the
bottom.

.. literalinclude:: code/retry_demo.py
   :language: python
   :caption: retry_demo.py

.. literalinclude:: outputs/retry_demo.txt
   :language: text


Blackboard: ``blackboard_demo.py``
----------------------------------

The tree ``handle_cell`` = ``average_voltage``, then the selector
``place_or_recycle`` (sequence ``place_if_good`` = ``voltage_in_range``, then
``place_in_slot``; else ``recycle_cell``). ``READINGS`` holds five tester
readings per cell, chosen to average 3.55 V, 3.85 V and 3.62 V. The script
ticks the tree once per cell, prints the keys, then makes the reader
``voltage_in_range`` try to write its key.

.. code-block:: bash

   python3 blackboard_demo.py

.. literalinclude:: code/blackboard_demo.py
   :language: python
   :caption: blackboard_demo.py

.. literalinclude:: outputs/blackboard_demo.txt
   :language: text


A Tree as a ROS 2 Node: ``ros_tree_demo.py``
--------------------------------------------

The tree ``move_cell`` (a sequence with memory): ``read_voltage`` (a subscriber
leaf), ``retry_pick`` around the action leaf ``pick_from_tester``,
``timeout_place`` (2.0 s) around the action leaf ``place_in_slot``, the service
leaf ``check_kit``, and the condition ``kit_is_good``. ``StandIns`` is a second
node in the same process: it publishes 3.62 V on ``tester1/voltage`` every
0.1 s, serves the two actions (``control_msgs/GripperCommand``) and the
``check_kit`` service (``std_srvs/Trigger``). The tree ticks every 100 ms. Each
line of the log shows the time since the first tick, the tick number, and a
node whose status changed on that tick; lines marked ``[server]`` come from the
stand-in action servers.

The script takes one argument, the run:

.. list-table::
   :header-rows: 1
   :widths: 20 80
   :class: compact-table

   * - **Argument**
     - **What changes**
   * - ``ok``
     - Nothing: the pick aborts once, then succeeds; the place takes 0.6 s;
       the kit check replies ``success=True``.
   * - ``timeout``
     - The place goal runs 5.0 s, longer than ``timeout_place`` allows.
   * - ``bad_kit``
     - The kit check replies ``success=False``.

.. code-block:: bash

   python3 ros_tree_demo.py ok
   python3 ros_tree_demo.py timeout
   python3 ros_tree_demo.py bad_kit

.. literalinclude:: code/ros_tree_demo.py
   :language: python
   :caption: ros_tree_demo.py

Output of ``ok``:

.. literalinclude:: outputs/ros_tree_ok.txt
   :language: text

Output of ``timeout``:

.. literalinclude:: outputs/ros_tree_timeout.txt
   :language: text

Output of ``bad_kit``:

.. literalinclude:: outputs/ros_tree_bad_kit.txt
   :language: text

Ten more runs of ``ok`` and ten of ``timeout``, last line only. The tick on
which the timeout fires moves between 33 and 34 (see :ref:`l4-run2`):

.. literalinclude:: outputs/ros_tree_repeats.txt
   :language: text

Five more sets of ten ``timeout`` runs, last line only. The number of runs that
end on tick 33 changes from set to set, from 3 to 6 of 10:

.. literalinclude:: outputs/ros_tree_repeat_sets.txt
   :language: text

The ``timeout`` run above heard 35 voltage messages in 34 ticks. In the 60
runs of these two files, the message count equals the tick count every time.

The time stamps in the ``[INFO]`` lines and the exact times in the log change
from run to run. On some runs, a line such as
``The following exception was never retrieved: cannot use Destroyable because
destruction was requested`` appears after the last line, while the nodes shut
down; it does not change the result.


Noise in the Kit Total: ``kit_spread.py``
-----------------------------------------

The tree adds four averaged voltages; ARIAC checks the cells' true voltages.
The ARIAC tester adds noise with a standard deviation of 0.05 V to each reading
(``noise_std_dev`` in ARIAC's ``voltage_tester/model.sdf``), and each average
here uses five readings, as ``wait_for_voltage`` collects. The script works out
the spread of one average and of the sum of four by formula, then simulates
100,000 kits whose true total sits on the window's upper edge, 14.55 V, and
counts how many read 14.62 V or more. It repeats both with 20 readings per
cell. It needs no ROS 2.

.. code-block:: bash

   python3 kit_spread.py

.. literalinclude:: code/kit_spread.py
   :language: python
   :caption: kit_spread.py

.. literalinclude:: outputs/kit_spread.txt
   :language: text

The formula assumes each reading carries its own noise. The tester draws new
noise 30 times per simulated second and publishes every 0.1 s, so readings
0.1 s apart carry different draws while the simulation runs at a third of real
time or faster.


Run Everything: ``run_all.sh``
------------------------------

``run_all.sh`` runs every script and writes each output to ``../outputs/``.
It is how the outputs on this page were made. It starts each script with
``env -i`` and ``ROS_DOMAIN_ID=84``, which keeps the course machine's other
ROS settings out; on your machine, the plain commands above do the same job.

.. literalinclude:: code/run_all.sh
   :language: bash
   :caption: run_all.sh
