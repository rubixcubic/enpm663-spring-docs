.. _gp1:

============================
GP1: ROS 2 Pub/Sub with Gazebo
============================

Overview
--------

In this first Group Project, your team will bring the warehouse robot concept into ROS 2. You will launch a mobile robot (e.g., TurtleBot3) in a Gazebo simulation, create publisher and subscriber nodes to control it, define custom interfaces for robot communication, and configure the system with parameters and launch files. This assignment bridges the gap between the C++ fundamentals you practiced in the RWAs and real robotic systems built on ROS 2.

-------------------
Learning Objectives
-------------------

By the end of this assignment you will be able to:

#. Launch a mobile robot in Gazebo simulation.
#. Create ROS 2 nodes that inherit from ``rclcpp::Node``.
#. Implement publishers and subscribers for robot control.
#. Define and use custom message types for inter-node communication.
#. Configure nodes with parameters and YAML files.
#. Orchestrate multi-node systems with Python launch files.
#. Select and justify an appropriate executor for the system.

------------
Requirements
------------

.. dropdown:: Gazebo Setup
   :open:
   :color: primary

   - Launch a mobile robot (TurtleBot3 or similar) in a Gazebo world.
   - The world should represent a simple warehouse environment. You may use a default world or create a simple custom one.
   - Verify that the robot spawns correctly and that topics are available (e.g., ``/cmd_vel``, ``/scan``, ``/odom``).

.. dropdown:: Publisher Node
   :open:
   :color: primary

   - Create a node that publishes velocity commands (``geometry_msgs::msg::Twist``) to control the robot.
   - The robot should follow a predefined path (e.g., navigate between waypoints).
   - Use a timer for periodic publishing.

   .. code-block:: cpp
      :caption: Example publisher snippet

      auto publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel", 10);

      auto timer_ = this->create_wall_timer(
          std::chrono::milliseconds{100},
          std::bind(&VelocityPublisher::timer_callback, this));

.. dropdown:: Subscriber Node
   :open:
   :color: primary

   - Create a node that subscribes to sensor data (e.g., ``sensor_msgs::msg::LaserScan``, ``nav_msgs::msg::Odometry``).
   - Process and log the received data.
   - Detect obstacles using laser scan data and log warnings when objects are within a configurable threshold.

.. dropdown:: Custom Interfaces
   :open:
   :color: primary

   - Define at least one custom message type.

   .. code-block:: text
      :caption: Example -- RobotStatus.msg

      string name
      float64 x
      float64 y
      float64 battery_level
      bool is_active

   - Publish robot status on a custom topic at a regular interval.
   - Create a subscriber in a separate node that receives and processes the custom message.

.. dropdown:: Parameters
   :open:
   :color: primary

   - Make key values configurable via ROS 2 parameters. At a minimum expose:

     - ``robot_name``
     - ``linear_speed``
     - ``angular_speed``
     - ``publish_rate``

   - Declare and use parameters in your nodes using ``this->declare_parameter()`` and ``this->get_parameter()``.
   - Provide a YAML configuration file that sets all parameters.

   .. code-block:: yaml
      :caption: Example -- params.yaml

      velocity_publisher:
        ros__parameters:
          robot_name: "warehouse_bot"
          linear_speed: 0.5
          angular_speed: 1.0
          publish_rate: 10.0

.. dropdown:: Launch File
   :open:
   :color: primary

   - Create a Python launch file that starts **all** nodes.
   - Pass parameters from the YAML configuration file.
   - Include the Gazebo launch with the robot model.

.. dropdown:: Executors
   :open:
   :color: primary

   - Use an appropriate executor (single-threaded or multi-threaded) for your system.
   - Provide a brief written justification in your README explaining **why** you chose the executor you did.

------------
Deliverables
------------

- ROS 2 package(s) with all source code.
- Custom interface definitions (``.msg`` files and ``CMakeLists.txt`` / ``package.xml`` changes).
- Launch file(s) and YAML configuration file.
- ``README.md`` with build and run instructions.
- Short video demo (1--2 minutes) showing the robot operating in Gazebo.

--------------
Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 50 15

   * - Criterion
     - Weight
   * - Functionality (robot moves, pub/sub works, obstacle detection)
     - 40%
   * - Custom Interfaces (message definition, publishing, subscribing)
     - 15%
   * - Parameters and Launch File (YAML config, launch orchestration)
     - 15%
   * - Code Quality (naming conventions, uniform initialization, ``'\n'`` usage, structure)
     - 15%
   * - Documentation and Demo (README clarity, video quality)
     - 15%
