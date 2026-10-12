====================================================
References
====================================================

These are the sources the L4 slides cite or take their facts from, in the
order of the slides, grouped by topic. Every link was checked on 2026-10-12.


.. dropdown:: Trees and State Machines
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The book on behavior trees
         :link: https://arxiv.org/abs/1709.00084
         :class-card: sd-border-secondary

         **Colledanchise, M., and Ögren, P. (2018)**

         *Behavior Trees in Robotics and AI: An Introduction.* Chapman and
         Hall/CRC. Free preprint: arXiv 1709.00084.

         The lecture's "to read more" source on BTs and how they compare with
         state machines.

      .. grid-item-card:: Behavior trees in Nav2
         :link: https://docs.nav2.org/jazzy/getting_started/navigation_concepts/behavior_trees/
         :class-card: sd-border-secondary

         **Nav2 documentation (Jazzy): Behavior Trees**

         Nav2, the ROS 2 navigation stack, runs its navigation logic as
         behavior trees and says it uses BehaviorTree.CPP (version 4) as its
         behavior tree library.

      .. grid-item-card:: BehaviorTree.CPP
         :link: https://www.behaviortree.dev/
         :class-card: sd-border-secondary

         **BehaviorTree.CPP**

         The C++ behavior tree library Nav2 uses. L7 shows it so you can read
         that code.


.. dropdown:: BT Primitives
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Composites
         :link: https://py-trees.readthedocs.io/en/devel/composites.html
         :class-card: sd-border-secondary

         **py_trees 2.6.0 documentation: Composites**

         Sequence, selector and parallel, the memory flag, and the parallel
         policies with their ``synchronise`` flag.

      .. grid-item-card:: Decorators
         :link: https://py-trees.readthedocs.io/en/devel/decorators.html
         :class-card: sd-border-secondary

         **py_trees 2.6.0 documentation: Decorators**

         ``Retry``, ``Timeout``, ``Inverter``, ``FailureIsSuccess``,
         ``EternalGuard`` and the other decorators in
         ``py_trees.decorators``.


.. dropdown:: Ticks and Memory
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Behaviours and their methods
         :link: https://py-trees.readthedocs.io/en/devel/behaviours.html
         :class-card: sd-border-secondary

         **py_trees 2.6.0 documentation: Behaviours**

         The node life cycle: ``setup``, ``initialise``, ``update`` and
         ``terminate``.

      .. grid-item-card:: How an action leaf sends and cancels a goal
         :link: https://github.com/splintered-reality/py_trees_ros/blob/release/2.6.x/py_trees_ros/action_clients.py
         :class-card: sd-border-secondary

         **py_trees_ros source:** ``action_clients.py`` (release 2.6.x)

         ``FromConstant`` and ``FromBlackboard``: the goal is sent in
         ``initialise``, and the cancel only when the status goes from
         ``RUNNING`` to ``INVALID``.

      .. grid-item-card:: The AGV move rejects cancel requests
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/agv_motion_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/src/agv_motion_plugin.cpp``
         (branch ``ariac2025``)

         ``goal_cancel_cb`` returns ``CancelResponse::REJECT``: once the AGV
         leaves, it finishes its move.


.. dropdown:: Blackboards
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Blackboards
         :link: https://py-trees.readthedocs.io/en/devel/blackboards.html
         :class-card: sd-border-secondary

         **py_trees 2.6.0 documentation: Blackboards**

         Blackboard clients, ``register_key`` and read and write access.

      .. grid-item-card:: The watchers
         :link: https://py-trees-ros.readthedocs.io/en/devel/features.html
         :class-card: sd-border-secondary

         **py_trees_ros 2.6.0 documentation: Features**

         The ``py-trees-tree-watcher`` and ``py-trees-blackboard-watcher``
         command-line tools and their arguments.


.. dropdown:: py_trees_ros
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Module API
         :link: https://py-trees-ros.readthedocs.io/en/devel/modules.html
         :class-card: sd-border-secondary

         **py_trees_ros 2.6.0 documentation: Module API**

         ``trees.BehaviourTree`` (``setup``, ``tick_tock``),
         ``action_clients``, ``service_clients`` and
         ``subscribers.ToBlackboard``.

      .. grid-item-card:: The ARIAC interfaces
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/api.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: ROS API**

         The interfaces the demonstration's stand-ins replace:
         ``/voltage_tester_1/voltage``, ``/{agv_name}/check_kit_quality`` and
         ``/{agv_name}/move``.

      .. grid-item-card:: The kit check reply
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/srv/CheckKitQuality.srv
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_interfaces/srv/CheckKitQuality.srv``
         (branch ``ariac2025``)

         The reply has ``bool is_good`` and ``string message``: the field your
         condition after the service leaf must read.


.. dropdown:: Patterns for the GP1 Tree
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The kit voltage window
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/scenario.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Scenario**

         The Task 1 steps the starter tree follows, and the kit tolerance used
         in the fourth-cell example.

      .. grid-item-card:: ARIAC source
         :link: https://github.com/usnistgov/ARIAC/tree/ariac2025
         :class-card: sd-border-secondary

         **usnistgov/ARIAC, branch** ``ariac2025``

         The code to check against when a leaf depends on how ARIAC behaves,
         as the cancel and kit check facts above do.
