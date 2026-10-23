====================================================
References
====================================================

These are the sources the L1 slides cite or take their facts from, in the
order of the slides, grouped by topic. A last dropdown lists the ROS 2 documentation pages for the
four refresher topics, which no slide cites but which go deeper than the
lecture. Every link was checked on 2026-10-12.


.. dropdown:: Course Introduction
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Robot agility
         :link: https://standards.ieee.org/ieee/2940/10411/
         :class-card: sd-border-secondary

         **IEEE P2940**

         *Standard for Measuring Robot Agility.* IEEE Standards
         Association, active project (PAR).

         One outcome of the instructor's robot agility research, named on
         the Research slide.

      .. grid-item-card:: ARIAC documentation
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/index.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation**

         The testbed of the course. Its Scenario, Sensors, Challenges and
         Scoring pages are the source of the factory section of the
         lecture.

         +++

         Read the Scenario, Sensors, Challenges and Scoring pages before L2.


.. dropdown:: Physical AI and Agents
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Physical AI
         :link: https://www.nvidia.com/en-us/glossary/generative-physical-ai/
         :class-card: sd-border-secondary

         **NVIDIA Glossary: "What is Physical AI?"**

         The definition quoted on the Two Definitions slide: physical AI
         lets autonomous systems "perceive, understand, reason, and perform
         or orchestrate complex actions in the physical world."


.. dropdown:: The ARIAC 2025 Factory
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The factory figures
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/scenario.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Scenario**

         The source of the module, Task 1 and Task 2 figures, and of the
         steps 1a to 1e. The factory floor figure is on the documentation's
         `home page <https://pages.nist.gov/ARIAC_docs/en/latest/index.html>`_.

      .. grid-item-card:: Cell types and tolerances
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_interfaces/msg/CellTypes.msg
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_interfaces/msg/CellTypes.msg``

         The nominal voltages (Li-Ion 3.6 V, Ni-MH 1.2 V) and the
         tolerances (0.2 V per cell, 0.15 V per kit) used in the kit voltage
         window.

      .. grid-item-card:: What ARIAC gives each robot
         :link: https://github.com/usnistgov/ARIAC/tree/ariac2025/ariac_description/config
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_description/config`` and ``ariac_plugins/src``

         Each robot's controller file: a joint trajectory controller for
         every robot, and a gripper controller only for the inspection robots
         and assembly robot 1. ``tool_changer_plugin.cpp``,
         ``vacuum_tool_plugin.cpp`` and ``welder_plugin.cpp`` create the
         tool, grasp and weld services.

      .. grid-item-card:: Sensors and their costs
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/sensors.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Sensors**

         The sensor grades and costs, and the three lidar bounding boxes
         around the inspection conveyor.

      .. grid-item-card:: The sensor budget
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_db/config/scoring_weights.yaml
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_db/config/scoring_weights.yaml``

         ``SENSOR_BUDGET: 9600``, and the scoring weights and penalties that
         L12 teaches.

      .. grid-item-card:: The four challenges
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/challenges.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Challenges**

         Conveyor, voltage tester and vacuum tool malfunctions, and the
         high-priority order. The page says a malfunctioning tester stops
         publishing; the source below shows what the 2025 code does.

      .. grid-item-card:: The voltage tester malfunction in code
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/voltage_tester_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/src/voltage_tester_plugin.cpp``

         During a malfunction the tester keeps publishing, with a voltage of
         −1 and the status ``MALFUNCTIONING``.

      .. grid-item-card:: How ARIAC scores a run
         :link: https://pages.nist.gov/ARIAC_docs/en/latest/pages/scoring.html
         :class-card: sd-border-secondary

         **NIST, ARIAC 2025 documentation: Scoring**

         The base score, the bonuses and the penalties. The formula is L12's
         topic.


.. dropdown:: ROS 2 Refresher
   :class-container: sd-border-secondary
   :open:

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: The break beam's QoS
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/ray_sensor_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/src/ray_sensor_plugin.cpp``

         Lines 51 and 52 create the break beam's status and change
         publishers with ``rclcpp::SensorDataQoS()``, which is best effort.

      .. grid-item-card:: The gripper action type
         :link: https://github.com/ros-controls/control_msgs
         :class-card: sd-border-secondary

         **ros-controls:** ``control_msgs``

         The package that defines ``control_msgs/GripperCommand``, the action
         type of the demonstration's server. ARIAC 2025 brings it in.

      .. grid-item-card:: AGV frame names
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_plugins/src/tf_publisher_plugin.cpp
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_plugins/src/tf_publisher_plugin.cpp``

         Names each frame after its model, which gives ``agv1_frame``,
         ``agv1_tray_frame`` and ``agv1_slot1_frame``.

      .. grid-item-card:: AGV tray and slot offsets
         :link: https://github.com/usnistgov/ARIAC/blob/ariac2025/ariac_gz/models/agv/model.sdf
         :class-card: sd-border-secondary

         **ARIAC source:** ``ariac_gz/models/agv/model.sdf``

         The tray 0.35 m above the base, turned −1.57 rad about z, and the
         four slots at plus or minus 0.065 m and plus or minus 0.05 m, 0.032 m
         above the tray.


.. dropdown:: Further Reading: ROS 2 Jazzy Concepts
   :class-container: sd-border-secondary

   The ROS 2 Jazzy documentation explains each refresher topic in more depth
   than the lecture.

   - `Quality of Service settings
     <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html>`_:
     the policies, the compatibility rules and the predefined profiles.
   - `Executors
     <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Executors.html>`_:
     executor types and callback groups.
   - `Actions <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Actions.html>`_:
     goals, feedback, results and cancellation.
   - `tf2 <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Tf2.html>`_:
     frames, transforms and lookups.
   - `ROS 2 Jazzy documentation <https://docs.ros.org/en/jazzy/>`_: the
     starting page.
