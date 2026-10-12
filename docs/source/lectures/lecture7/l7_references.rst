====================================================
References
====================================================

These are the sources the L7 slides cite or take their facts from, in the
order of the slides, grouped by section. The slide deck has no bibliography:
the sources below are the documentation pages, ARIAC source files and ROS 2
packages that the slides name. Every link was checked on 2026-10-12.


.. dropdown:: The Plan-to-BT Factory
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The action names
         :link: /lectures/lecture6/l6_index
         :link-type: doc
         :class-card: sd-border-secondary

         **L6: the PDDL domain for Task 1**

         The action names the executor knows, and the preconditions and
         effects that each builder's guard and update use.

      .. grid-item-card:: Station numbers
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/msg/AgvStations.msg
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_interfaces/msg/AgvStations.msg``

         ``INSPECTION`` 1, ``ASSEMBLY`` 2, ``SHIPPING`` 3, ``RECYCLING`` 4:
         the ``station_id`` a builder sends for a PDDL station name.

      .. grid-item-card:: Sequence with memory
         :link: https://py-trees.readthedocs.io/en/devel/modules.html
         :class-card: sd-border-secondary

         **py_trees 2.6.0 API reference**

         ``py_trees.composites.Sequence(name, memory, children)``, and the
         ``Retry`` and ``Timeout`` decorators of the next section.
         ``py_trees.display.ascii_tree`` and ``unicode_tree`` print a tree
         with its statuses.

      .. grid-item-card:: The act leaf in GP3
         :link: https://py-trees-ros.readthedocs.io/en/devel/modules.html
         :class-card: sd-border-secondary

         **py_trees_ros API reference**

         ``py_trees_ros.action_clients.FromConstant`` and ``FromBlackboard``,
         the leaves that send an action goal and stay RUNNING until the
         result arrives.


.. dropdown:: Retry and Timeout
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The four challenges
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/challenges.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Challenges**

         The vacuum tool malfunction (detect, move away, grasp again), the
         voltage tester malfunction ("one or both voltage testers will stop
         publishing data"), the conveyor malfunction and the high-priority
         order.

      .. grid-item-card:: The vacuum tool malfunction in code
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/vacuum_tool_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/src/vacuum_tool_plugin.cpp``

         The failure clears only after every suction cup has lost contact, so
         a retry must move the gripper away first.

      .. grid-item-card:: The voltage tester malfunction in code
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/voltage_tester_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/src/voltage_tester_plugin.cpp``

         During a malfunction the tester keeps publishing every 0.1 s, with
         a voltage of −1 and the status ``MALFUNCTIONING``.

      .. grid-item-card:: Tester status values
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/msg/OperationStates.msg
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_interfaces/msg/OperationStates.msg``

         The ``OPERATIONAL`` and ``MALFUNCTIONING`` values that
         ``demo_timeout.py`` copies.


.. dropdown:: The Replanning Loop
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: AGV moves cannot be cancelled
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/agv_motion_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/src/agv_motion_plugin.cpp``

         The ``/agvN/move`` action rejects cancel requests, so the executor
         waits for a moving AGV before it replans.

      .. grid-item-card:: Cell and kit tolerances
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/msg/CellTypes.msg
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_interfaces/msg/CellTypes.msg``

         Li-Ion 3.6 V, plus or minus 0.2 V per cell and 0.15 V per kit: the
         check that fails ``c3`` at 3.86 V in Demo 5, and the 14.25 V to
         14.55 V kit window.


.. dropdown:: BehaviorTree.CPP
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: BehaviorTree.CPP documentation
         :link: https://www.behaviortree.dev/docs/intro/
         :class-card: sd-border-secondary

         **BehaviorTree.CPP 4**

         Trees in XML, nodes as C++ classes, ports and the blackboard. The
         `XML format page <https://www.behaviortree.dev/docs/learn-the-basics/xml_format/>`__
         and the `decorator nodes page <https://www.behaviortree.dev/docs/nodes-library/DecoratorNode/>`__
         cover ``RetryUntilSuccessful`` and ``Timeout``.

      .. grid-item-card:: The ROS 2 Jazzy package
         :link: https://index.ros.org/p/behaviortree_cpp/
         :class-card: sd-border-secondary

         **ROS Index:** ``behaviortree_cpp``

         Version 4.10.0 for Jazzy, installed with
         ``sudo apt install ros-jazzy-behaviortree-cpp``. The source is on
         `GitHub <https://github.com/BehaviorTree/BehaviorTree.CPP>`__.

      .. grid-item-card:: Nav2 builds on it
         :link: https://index.ros.org/p/nav2_behavior_tree/
         :class-card: sd-border-secondary

         **ROS Index:** ``nav2_behavior_tree``

         The Jazzy package ``ros-jazzy-nav2-behavior-tree`` depends on
         ``ros-jazzy-behaviortree-cpp``.


.. dropdown:: Debugging a Running Tree
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Snapshots and the tree watcher
         :link: https://py-trees-ros.readthedocs.io/en/devel/features.html
         :class-card: sd-border-secondary

         **py_trees_ros: features**

         ``py-trees-tree-watcher`` streams a running tree to the terminal.
         The ``default_snapshot_stream`` parameter and the
         ``~/snapshot_streams/open`` service are in the
         `API reference <https://py-trees-ros.readthedocs.io/en/devel/modules.html>`__.

      .. grid-item-card:: The tree viewer
         :link: https://github.com/splintered-reality/py_trees_ros_viewer
         :class-card: sd-border-secondary

         **py_trees_ros_viewer**

         Shows the snapshots in a window. Apt package
         ``ros-jazzy-py-trees-ros-viewer``.

      .. grid-item-card:: Groot2
         :link: https://www.behaviortree.dev/groot/
         :class-card: sd-border-secondary

         **Groot2**

         The editor and monitor for BehaviorTree.CPP: "Compatible with both
         BT.CPP 3 and 4." The free version monitors a running tree of up to
         20 nodes.
