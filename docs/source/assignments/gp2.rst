.. _gp2:

=============================================
GP2: Services, Actions, and Robot Inheritance
=============================================

Overview
--------

This assignment extends your GP1 system by adding request-response communication through **services** and long-running task management through **actions**. You will also introduce a robot type hierarchy using C++ inheritance -- a base ``RobotNode`` class with derived types that have different ROS parameters and behaviors. By the end, your warehouse simulation will support multiple robot types that can be commanded via services and actions alongside the existing pub/sub architecture.

-------------------
Learning Objectives
-------------------

By the end of this assignment you will be able to:

#. Implement ROS 2 services for synchronous request-response operations.
#. Implement ROS 2 actions for long-running tasks with periodic feedback.
#. Design a class hierarchy for robot nodes using C++ inheritance.
#. Apply polymorphism to differentiate robot behaviors at runtime.
#. Integrate services and actions with the existing pub/sub system from GP1.

------------
Requirements
------------

.. dropdown:: Robot Inheritance
   :open:
   :color: primary

   - Design a base ``RobotNode`` class that inherits from ``rclcpp::Node``. This class should contain common functionality shared by all robot types:

     - Publishers (e.g., velocity commands, robot status).
     - Subscribers (e.g., laser scan, odometry).
     - Common parameters (e.g., ``robot_name``, ``publish_rate``).

   - Create **at least 2** derived robot types, for example:

     - ``ScoutBot`` -- fast movement speed, equipped with cameras, used for exploration.
     - ``CarrierBot`` -- slow movement speed, large payload capacity, used for transport.

   - Each derived type must have:

     - Different default parameters (speed, sensor configuration).
     - Different behavior (movement patterns, task capabilities).

   - Demonstrate polymorphism through virtual methods.

   .. code-block:: cpp
      :caption: Example class hierarchy

      class RobotNode : public rclcpp::Node {
       public:
        RobotNode(const std::string& node_name, const rclcpp::NodeOptions& options);
        virtual ~RobotNode() = default;

       protected:
        virtual void execute_task() = 0;
        virtual void configure_sensors() = 0;

        rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_pub_;
        double linear_speed_{0.0};
        double angular_speed_{0.0};
      };

      class ScoutBot : public RobotNode {
       public:
        ScoutBot(const rclcpp::NodeOptions& options);

       protected:
        void execute_task() override;
        void configure_sensors() override;
      };

.. dropdown:: Custom Service
   :open:
   :color: primary

   - Define a custom ``.srv`` file.

   .. code-block:: text
      :caption: Example -- SpawnRobot.srv

      # Request
      string robot_type
      float64 x
      float64 y
      ---
      # Response
      bool success
      string message

   - Implement a **service server** that handles robot spawning or configuration requests.
   - Implement a **service client** that calls the service and processes the response.

.. dropdown:: Custom Action
   :open:
   :color: primary

   - Define a custom ``.action`` file.

   .. code-block:: text
      :caption: Example -- NavigateToGoal.action

      # Goal
      float64 x
      float64 y
      ---
      # Result
      bool success
      float64 time_elapsed
      ---
      # Feedback
      float64 distance_remaining

   - Implement an **action server** that navigates the robot to a goal position with periodic feedback.
   - Implement an **action client** that sends goals and processes feedback as it arrives.

   .. code-block:: cpp
      :caption: Example action server callback

      rclcpp_action::GoalResponse handle_goal(
          const rclcpp_action::GoalUUID& uuid,
          std::shared_ptr<const NavigateToGoal::Goal> goal)
      {
        RCLCPP_INFO(this->get_logger(),
            "Received goal: x=%.2f, y=%.2f\n", goal->x, goal->y);
        return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
      }

.. dropdown:: Integration
   :open:
   :color: primary

   - Services and actions must work **alongside** the existing pub/sub system from GP1.
   - Multiple robot types should be able to coexist in the same simulation.
   - The launch file must start all components (Gazebo, robot nodes, service/action servers).

------------
Deliverables
------------

- Updated ROS 2 package(s) with all source code.
- Custom service (``.srv``) and action (``.action``) definitions.
- Updated launch file that starts all components.
- ``README.md`` with build and run instructions.
- Short video demo showing services being called and actions executing with feedback.

--------------
Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 50 15

   * - Criterion
     - Weight
   * - Services (custom ``.srv``, server implementation, client implementation)
     - 25%
   * - Actions (custom ``.action``, server with feedback, client)
     - 25%
   * - Robot Inheritance (base class, derived types, polymorphism)
     - 25%
   * - Integration (pub/sub still functional, multi-robot, launch file)
     - 15%
   * - Documentation and Demo (README, video)
     - 10%
