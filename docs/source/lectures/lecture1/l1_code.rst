====================================================
Code
====================================================

L1 has four short ROS 2 Python scripts, one for each refresher topic. Each one
runs on its own, with no ARIAC simulation: the scripts use stand-in messages
(``std_msgs/Bool``, ``control_msgs/GripperCommand``) and static transforms
with ARIAC's own frame names and offsets. The outputs below come from running
them on ROS 2 Jazzy on 2026-10-12.

.. note::

   **What you need.** Ubuntu 24.04 with ROS 2 Jazzy. Every script uses
   ``rclpy``; ``tf_slot_lookup.py`` also uses ``tf2_ros`` and
   ``geometry_msgs``, which come with a desktop install. ``action_gripper.py``
   uses ``control_msgs``, which an ARIAC install brings in; without ARIAC,
   install it with ``sudo apt install ros-jazzy-control-msgs``.

   Open a terminal, source ROS 2 once, and go to the folder that holds the
   scripts:

   .. code-block:: bash

      source /opt/ros/jazzy/setup.bash
      cd lecture1/code

   If an ARIAC simulation is running on the same machine, give the scripts a
   ROS domain of their own, for example ``export ROS_DOMAIN_ID=77``, so their
   topics do not mix with the simulation's.


.. list-table::
   :header-rows: 1
   :widths: 30 45 25
   :class: compact-table

   * - **Script**
     - **What it shows**
     - **Notes section**
   * - :download:`qos_mismatch.py <code/qos_mismatch.py>`
     - A best-effort publisher and a reliable subscriber never connect.
     - :ref:`l1-qos`
   * - :download:`executor_blocking.py <code/executor_blocking.py>`
     - A slow callback blocks a fast one unless the executor and callback
       groups allow both to run.
     - :ref:`l1-executors`
   * - :download:`action_gripper.py <code/action_gripper.py>`
     - An action goal that runs to the end, and one cancelled partway.
     - :ref:`l1-actions`
   * - :download:`tf_slot_lookup.py <code/tf_slot_lookup.py>`
     - A TF2 lookup of AGV 1's tray slot 1, seen from the AGV's base.
     - :ref:`l1-tf2`
   * - :download:`run_all.sh <code/run_all.sh>`
     - Runs all four and writes their outputs to ``../outputs/``.
     - See the last section


QoS: ``qos_mismatch.py``
------------------------

One node publishes a ``Bool`` on ``beam/change`` every 0.1 s for 2 s with the
sensor data profile (best effort), the profile ARIAC's break beam uses. The
same node subscribes to the topic. Without ``--match`` the subscriber uses
the default profile (reliable, depth 10); with it, the sensor data profile.

.. code-block:: bash

   python3 qos_mismatch.py           # subscriber uses the default QoS
   python3 qos_mismatch.py --match   # subscriber uses the sensor data QoS

.. literalinclude:: code/qos_mismatch.py
   :language: python
   :caption: qos_mismatch.py

Output without ``--match``:

.. literalinclude:: outputs/qos_default.txt
   :language: text

Output with ``--match``:

.. literalinclude:: outputs/qos_match.txt
   :language: text

The two warning lines carry a time stamp, so yours will show different
numbers there.


Executors: ``executor_blocking.py``
-----------------------------------

A node has two timers: one fires once a second and sleeps for 1 s (a stand-in
for waiting on a skill), the other fires at 10 Hz and counts status reads. The
script spins the node for 5 s and prints the count.

.. code-block:: bash

   python3 executor_blocking.py single   # single-threaded executor, one group
   python3 executor_blocking.py multi    # multi-threaded executor, two groups

.. literalinclude:: code/executor_blocking.py
   :language: python
   :caption: executor_blocking.py

Output of ``single``:

.. literalinclude:: outputs/executor_single.txt
   :language: text

Output of ``multi``:

.. literalinclude:: outputs/executor_multi.txt
   :language: text

The count for ``single`` gave 11 in each of three reruns on the course machine
on 2026-10-12. It comes from timing, not from a formula, so on your machine
check that it is far below 50 rather than exactly 11.


Actions: ``action_gripper.py``
------------------------------

One process holds both sides. The server stands in for a robot skill: it
closes a gripper from 0.085 m in 0.0085 m steps, one step every 0.2 s, and
sends feedback after each step. The client sends two goals: it lets the first
run to the end and cancels the second after 0.5 s. Both nodes spin on one
multi-threaded executor, and the server's callbacks are in a reentrant group,
so the server can take the cancel request while a goal runs.

.. code-block:: bash

   python3 action_gripper.py

.. literalinclude:: code/action_gripper.py
   :language: python
   :caption: action_gripper.py

Output:

.. literalinclude:: outputs/action_gripper.txt
   :language: text


TF2: ``tf_slot_lookup.py``
--------------------------

The script publishes two static transforms with ARIAC's offsets from
``ariac_gz/models/agv/model.sdf`` (the tray 0.35 m above the AGV base, turned
−1.57 rad about z; slot 1 at (−0.065, 0.05, 0.032) m in the tray frame). It
then asks TF2 where slot 1 is in ``agv1_frame``.

.. code-block:: bash

   python3 tf_slot_lookup.py

.. literalinclude:: code/tf_slot_lookup.py
   :language: python
   :caption: tf_slot_lookup.py

Output:

.. literalinclude:: outputs/tf_slot.txt
   :language: text


Running all four: ``run_all.sh``
--------------------------------

``run_all.sh`` is the script that produced the outputs above. It runs each
example in a clean environment (``env -i``) on ROS domain 77, which kept the
examples away from a simulation running on the default domain 0, and writes
each output to ``../outputs/``. You do not need it: the commands in the
sections above give the same results.

.. literalinclude:: code/run_all.sh
   :language: bash
   :caption: run_all.sh
