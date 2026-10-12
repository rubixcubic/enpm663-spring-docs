====================================================
References
====================================================

These are the sources the L2 slides cite or take their facts from, in the
order of the slides, grouped by section. Every link was checked on
2026-10-12.


.. dropdown:: Classical Robot Architectures
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Subsumption
         :link: https://doi.org/10.1109/JRA.1986.1087032
         :class-card: sd-border-secondary

         **R. A. Brooks (1986)**

         *A robust layered control system for a mobile robot.* IEEE Journal
         of Robotics and Automation, vol. 2, no. 1, pp. 14 to 23.

         The subsumption architecture: layers of behaviors running in
         parallel, suppression and inhibition.

      .. grid-item-card:: No explicit world model
         :link: https://doi.org/10.1016/0004-3702(91)90053-M
         :class-card: sd-border-secondary

         **R. A. Brooks (1991)**

         *Intelligence without representation.* Artificial Intelligence,
         vol. 47, pp. 139 to 159.

         Brooks's stronger claim, that a robot can work with no explicit
         world model.

      .. grid-item-card:: The three-layer architecture
         :link: https://flownet.com/gat/papers/tla.pdf
         :class-card: sd-border-secondary

         **E. Gat (1998)**

         *On three-layer architectures.* In D. Kortenkamp, R. P. Bonasso and
         R. Murphy (eds.), Artificial Intelligence and Mobile Robots, AAAI
         Press.

         The link is the author's preprint. The deliberator, the sequencer
         and the controller.


.. dropdown:: A Toy Factory, Three Ways
   :class-container: sd-border-secondary
   :open:

   The rules the toy keeps from ARIAC 2025 (branch ``ariac2025``).

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Cell types and tolerances
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/msg/CellTypes.msg
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_interfaces/msg/CellTypes.msg``

         Li-Ion 3.6 V nominal, 0.2 V per cell, 0.15 V per kit.

      .. grid-item-card:: Cell voltage spread
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/include/ariac_plugins/cell_feed_plugin.hpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/include/ariac_plugins/cell_feed_plugin.hpp``

         ``voltage_std_dev = 0.1``: cell voltages spread with a standard
         deviation of 0.1 V.

      .. grid-item-card:: Tester noise
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_gz/models/voltage_tester/model.sdf
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_gz/models/voltage_tester/model.sdf``

         ``noise_std_dev`` 0.05: each reading has noise with a standard
         deviation of 0.05 V.

      .. grid-item-card:: The tester malfunction in code
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/voltage_tester_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/src/voltage_tester_plugin.cpp``

         Publishes every 0.1 s; during a malfunction it keeps publishing,
         with a voltage of −1 and the status ``MALFUNCTIONING``.

      .. grid-item-card:: The tester malfunction in the docs
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/challenges.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Challenges**

         ``START_TIME``, ``DURATION`` and ``TESTER``. The page says a
         malfunctioning tester stops publishing and asks teams to watch the
         tester topics; the code above shows what it does.

      .. grid-item-card:: The 45 s example
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/config_files.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Configuration Files**

         The example trial configuration: tester 1 malfunctions with
         ``DURATION: 45``.


.. dropdown:: One Tester Malfunction, Layer by Layer
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: 4D/RCS
         :link: https://doi.org/10.6028/NIST.IR.6910
         :class-card: sd-border-secondary

         **J. Albus et al. (2002), NISTIR 6910**

         *4D/RCS: A Reference Model Architecture for Unmanned Vehicle
         Systems, Version 2.0.* NIST.

         The source of the rule "an error is handled where it is seen, and
         only the status moves up", which L3 covers.


.. dropdown:: Three Layers in Real Robot Software
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Nav2: Behavior Trees
         :link: https://docs.nav2.org/jazzy/getting_started/navigation_concepts/behavior_trees/
         :class-card: sd-border-secondary

         **Nav2 documentation (Jazzy)**

         "For this project, we use BehaviorTree CPP V4 as the behavior tree
         library."

      .. grid-item-card:: Nav2: Navigation Servers
         :link: https://docs.nav2.org/jazzy/getting_started/navigation_concepts/navigation_servers/
         :class-card: sd-border-secondary

         **Nav2 documentation (Jazzy)**

         "When the behavior tree ticks the corresponding BT node, it will call
         the action server to process its task."

      .. grid-item-card:: Nav2: Behavior-Tree Navigator
         :link: https://docs.nav2.org/jazzy/configuration_and_development/configuration_guide/core_servers/configuring_bt_navigator/
         :class-card: sd-border-secondary

         **Nav2 documentation (Jazzy)**

         The BT Navigator's configuration, including the ``NavigateToPose``
         action that a client application sends.

      .. grid-item-card:: Nav2: Detailed Behavior Tree Walkthrough
         :link: https://docs.nav2.org/jazzy/getting_started/nav2_behavior_trees/detailed_behavior_tree_walkthrough/detailed_behavior_tree_walkthrough/
         :class-card: sd-border-secondary

         **Nav2 documentation (Jazzy)**

         The default tree: replanning at 1 Hz, contextual recoveries, then
         the Recovery subtree, up to 6 retries.

      .. grid-item-card:: MoveIt: the move_group node
         :link: https://moveit.picknik.ai/main/doc/concepts/move_group.html
         :class-card: sd-border-secondary

         **MoveIt documentation (Rolling)**

         ``move_group`` as an integrator, and the FollowJointTrajectoryAction
         server that it does not provide.

      .. grid-item-card:: MoveIt: Motion Planning
         :link: https://moveit.picknik.ai/main/doc/concepts/motion_planning.html
         :class-card: sd-border-secondary

         **MoveIt documentation (Rolling)**

         "The result coming out of move_group is a trajectory and not just a
         path."

      .. grid-item-card:: ARIAC robot interfaces
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/api.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: API**

         Each robot's ``joint_trajectory_controller/follow_joint_trajectory``
         action, the gripper controller, the vacuum tools' grasp and release
         services, and the voltage tester topics.


.. dropdown:: The End-to-End Alternative
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: OpenVLA
         :link: https://openvla.github.io/
         :class-card: sd-border-secondary

         **OpenVLA: An Open-Source Vision-Language-Action Model**

         "a 7B parameter open-source vision-language-action model (VLA)". A
         single model.

      .. grid-item-card:: pi-0
         :link: https://arxiv.org/abs/2410.24164
         :class-card: sd-border-secondary

         **K. Black et al. (2024), Physical Intelligence**

         *π0: A Vision-Language-Action Flow Model for General Robot
         Control.* arXiv 2410.24164. A single model.

      .. grid-item-card:: Gemini Robotics
         :link: https://deepmind.google/models/gemini-robotics/
         :class-card: sd-border-secondary

         **Google DeepMind: Gemini Robotics**

         A VLA model that acts and an embodied-reasoning (ER) model that
         plans, working together.

      .. grid-item-card:: Helix
         :link: https://www.figure.ai/news/helix
         :class-card: sd-border-secondary

         **Figure: Helix**

         The source of the two-system numbers: a 7B-parameter VLM at 7 to
         9 Hz above an 80M-parameter policy at 200 Hz.


.. dropdown:: Multi-Robot Coordination
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Collision penalty
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/scoring.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Scoring**

         A penalty for every 5 s a robot is in collision, counted twice for a
         collision with another robot. The value may change.

      .. grid-item-card:: The 100 points
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_db/config/scoring_weights.yaml
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_db/config/scoring_weights.yaml``

         ``ROBOT_COLLISION: 100``.

      .. grid-item-card:: Positions in the tester area
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_gz/world/ariac.world
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_gz/world/ariac.world``

         The positions of the conveyor, testers, robots, bin and AGVs in the
         tester area figure.

      .. grid-item-card:: The robot descriptions
         :link: https://github.com/usnistgov/ARIAC/tree/ariac2025/ariac_description/urdf
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_description/urdf``

         The URDFs of inspection robot 1 (UR3e) and inspection robot 2
         (UR5e).
