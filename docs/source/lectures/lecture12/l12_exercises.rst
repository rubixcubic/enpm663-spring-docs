====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 12: ROS 2
Communication Patterns (Services and Actions). Work through them in
order, as each exercise builds on the skills from the previous one.
Write, compile, and run each program to verify your understanding.

.. note::

   Build all packages with:

   .. code-block:: bash

      cd ~/ros2_ws && colcon build --packages-select <package_name>
      source install/setup.bash


----


.. dropdown:: Exercise 1 -- Custom Service Definition
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice defining a custom ``.srv`` file and building it as a ROS 2
    interface.

    **Specification**

    1. Create an interface package called ``robot_interfaces``:

       .. code-block:: bash

          ros2 pkg create --build-type ament_cmake robot_interfaces

    2. Inside the package, create a ``srv/`` directory and add a file
       ``RobotCommand.srv`` with the following definition:

       - **Request**: a ``string`` field ``command`` and a ``float64``
         field ``value``.
       - **Response**: a ``bool`` field ``success`` and a ``string``
         field ``message``.

    3. Update ``CMakeLists.txt`` and ``package.xml`` so the interface is
       generated.

    4. Build the package and verify the interface exists:

       .. code-block:: bash

          ros2 interface show robot_interfaces/srv/RobotCommand

    .. dropdown:: Solution
        :class-container: sd-border-success

        **srv/RobotCommand.srv**

        .. code-block:: text

           string command
           float64 value
           ---
           bool success
           string message

        **CMakeLists.txt** (relevant additions):

        .. code-block:: cmake

           find_package(rosidl_default_generators REQUIRED)

           rosidl_generate_interfaces(${PROJECT_NAME}
             "srv/RobotCommand.srv"
           )

        **package.xml** (relevant additions):

        .. code-block:: xml

           <buildtool_depend>rosidl_default_generators</buildtool_depend>
           <exec_depend>rosidl_default_runtime</exec_depend>
           <member_of_group>rosidl_interface_packages</member_of_group>

        **Verification:**

        .. code-block:: bash

           cd ~/ros2_ws && colcon build --packages-select robot_interfaces
           source install/setup.bash
           ros2 interface show robot_interfaces/srv/RobotCommand

        **Expected output:**

        .. code-block:: text

           string command
           float64 value
           ---
           bool success
           string message


.. dropdown:: Exercise 2 -- Service Server
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Implement a service server that processes robot commands.

    **Specification**

    1. Create a package ``robot_service`` that depends on ``rclcpp`` and
       ``robot_interfaces``.

    2. Write a node ``command_server`` that:

       - Advertises a service ``/robot_command`` of type
         ``robot_interfaces/srv/RobotCommand``.
       - Handles the following commands:

         - ``"move"``: responds with ``success = true`` and
           ``message = "Moving at <value> m/s"``.
         - ``"stop"``: responds with ``success = true`` and
           ``message = "Robot stopped"``.
         - Any other command: responds with ``success = false`` and
           ``message = "Unknown command: <command>"``.

    3. Build, run, and test with:

       .. code-block:: bash

          ros2 service call /robot_command robot_interfaces/srv/RobotCommand \
            "{command: 'move', value: 1.5}"

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <rclcpp/rclcpp.hpp>
           #include "robot_interfaces/srv/robot_command.hpp"

           class CommandServer : public rclcpp::Node {
            public:
             CommandServer() : Node{"command_server"} {
               service_ = create_service<robot_interfaces::srv::RobotCommand>(
                   "robot_command",
                   std::bind(&CommandServer::handle_command, this,
                             std::placeholders::_1, std::placeholders::_2));
               RCLCPP_INFO(get_logger(), "Command server ready.");
             }

            private:
             void handle_command(
                 const std::shared_ptr<robot_interfaces::srv::RobotCommand::Request>
                     request,
                 std::shared_ptr<robot_interfaces::srv::RobotCommand::Response>
                     response) {
               if (request->command == "move") {
                 response->success = true;
                 response->message =
                     "Moving at " + std::to_string(request->value) + " m/s";
               } else if (request->command == "stop") {
                 response->success = true;
                 response->message = "Robot stopped";
               } else {
                 response->success = false;
                 response->message = "Unknown command: " + request->command;
               }
               RCLCPP_INFO(get_logger(), "[%s] %s",
                           request->command.c_str(), response->message.c_str());
             }

             rclcpp::Service<robot_interfaces::srv::RobotCommand>::SharedPtr
                 service_;
           };

           int main(int argc, char* argv[]) {
             rclcpp::init(argc, argv);
             rclcpp::spin(std::make_shared<CommandServer>());
             rclcpp::shutdown();
             return 0;
           }


.. dropdown:: Exercise 3 -- Service Client
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write a service client node that sends commands to the server from
    Exercise 2.

    **Specification**

    1. In the same ``robot_service`` package, write a node
       ``command_client`` that:

       - Creates a client for ``/robot_command``.
       - Waits for the service to become available.
       - Sends a ``"move"`` command with ``value = 2.0``.
       - Prints the response ``success`` and ``message`` fields.

    2. Run the server in one terminal and the client in another.
       Verify the output.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <rclcpp/rclcpp.hpp>
           #include "robot_interfaces/srv/robot_command.hpp"

           class CommandClient : public rclcpp::Node {
            public:
             CommandClient() : Node{"command_client"} {
               client_ = create_client<robot_interfaces::srv::RobotCommand>(
                   "robot_command");
             }

             void send_command(const std::string& command, double value) {
               while (!client_->wait_for_service(std::chrono::seconds{1})) {
                 if (!rclcpp::ok()) {
                   RCLCPP_ERROR(get_logger(), "Interrupted while waiting.");
                   return;
                 }
                 RCLCPP_INFO(get_logger(), "Waiting for service...");
               }

               auto request =
                   std::make_shared<robot_interfaces::srv::RobotCommand::Request>();
               request->command = command;
               request->value = value;

               auto future = client_->async_send_request(
                   request,
                   std::bind(&CommandClient::response_callback, this,
                             std::placeholders::_1));
             }

            private:
             void response_callback(
                 rclcpp::Client<robot_interfaces::srv::RobotCommand>::SharedFuture
                     future) {
               auto response = future.get();
               RCLCPP_INFO(get_logger(), "Success: %s | Message: %s",
                           response->success ? "true" : "false",
                           response->message.c_str());
             }

             rclcpp::Client<robot_interfaces::srv::RobotCommand>::SharedPtr
                 client_;
           };

           int main(int argc, char* argv[]) {
             rclcpp::init(argc, argv);
             auto node = std::make_shared<CommandClient>();
             node->send_command("move", 2.0);
             rclcpp::spin(node);
             rclcpp::shutdown();
             return 0;
           }

        **Expected output (client terminal):**

        .. code-block:: text

           [INFO] [command_client]: Success: true | Message: Moving at 2.000000 m/s


.. dropdown:: Exercise 4 -- Custom Action Definition
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Define a custom ``.action`` file for a robot patrol task.

    **Specification**

    1. In the ``robot_interfaces`` package, create an ``action/``
       directory and add ``Patrol.action``:

       - **Goal**: ``int32 num_waypoints`` -- how many waypoints to visit.
       - **Result**: ``bool success`` and ``string message``.
       - **Feedback**: ``int32 current_waypoint`` -- the waypoint
         currently being visited.

    2. Update ``CMakeLists.txt`` to generate the action interface.

    3. Build and verify:

       .. code-block:: bash

          ros2 interface show robot_interfaces/action/Patrol

    .. dropdown:: Solution
        :class-container: sd-border-success

        **action/Patrol.action**

        .. code-block:: text

           int32 num_waypoints
           ---
           bool success
           string message
           ---
           int32 current_waypoint

        **CMakeLists.txt** (updated generation call):

        .. code-block:: cmake

           rosidl_generate_interfaces(${PROJECT_NAME}
             "srv/RobotCommand.srv"
             "action/Patrol.action"
           )

        **Verification:**

        .. code-block:: bash

           cd ~/ros2_ws && colcon build --packages-select robot_interfaces
           source install/setup.bash
           ros2 interface show robot_interfaces/action/Patrol

        **Expected output:**

        .. code-block:: text

           int32 num_waypoints
           ---
           bool success
           string message
           ---
           int32 current_waypoint


.. dropdown:: Exercise 5 -- Action Server with Feedback
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Implement an action server that simulates visiting waypoints and
    publishes feedback.

    **Specification**

    1. Create a package ``robot_action`` that depends on ``rclcpp``,
       ``rclcpp_action``, and ``robot_interfaces``.

    2. Write a node ``patrol_server`` that:

       - Creates an action server for ``/patrol`` of type
         ``robot_interfaces/action/Patrol``.
       - Rejects goals where ``num_waypoints <= 0``.
       - Simulates visiting each waypoint with a 1-second delay.
       - Publishes feedback with the current waypoint number.
       - Handles cancellation: if canceled, returns
         ``success = false``.
       - On completion, returns ``success = true`` and
         ``message = "Patrol complete. Visited N waypoints."``.

    3. Test with:

       .. code-block:: bash

          ros2 action send_goal /patrol robot_interfaces/action/Patrol \
            "{num_waypoints: 5}" --feedback

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <rclcpp/rclcpp.hpp>
           #include <rclcpp_action/rclcpp_action.hpp>
           #include "robot_interfaces/action/patrol.hpp"

           using Patrol = robot_interfaces::action::Patrol;
           using GoalHandlePatrol = rclcpp_action::ServerGoalHandle<Patrol>;

           class PatrolServer : public rclcpp::Node {
            public:
             PatrolServer() : Node{"patrol_server"} {
               action_server_ = rclcpp_action::create_server<Patrol>(
                   this, "patrol",
                   std::bind(&PatrolServer::handle_goal, this,
                             std::placeholders::_1, std::placeholders::_2),
                   std::bind(&PatrolServer::handle_cancel, this,
                             std::placeholders::_1),
                   std::bind(&PatrolServer::handle_accepted, this,
                             std::placeholders::_1));
               RCLCPP_INFO(get_logger(), "Patrol action server ready.");
             }

            private:
             rclcpp_action::GoalResponse handle_goal(
                 const rclcpp_action::GoalUUID& /*uuid*/,
                 std::shared_ptr<const Patrol::Goal> goal) {
               if (goal->num_waypoints <= 0) {
                 RCLCPP_WARN(get_logger(), "Rejecting goal: invalid waypoint count.");
                 return rclcpp_action::GoalResponse::REJECT;
               }
               RCLCPP_INFO(get_logger(), "Accepting goal: %d waypoints.",
                           goal->num_waypoints);
               return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
             }

             rclcpp_action::CancelResponse handle_cancel(
                 const std::shared_ptr<GoalHandlePatrol> /*goal_handle*/) {
               RCLCPP_INFO(get_logger(), "Cancel request accepted.");
               return rclcpp_action::CancelResponse::ACCEPT;
             }

             void handle_accepted(
                 const std::shared_ptr<GoalHandlePatrol> goal_handle) {
               std::thread{
                   std::bind(&PatrolServer::execute, this,
                             std::placeholders::_1),
                   goal_handle}
                   .detach();
             }

             void execute(const std::shared_ptr<GoalHandlePatrol> goal_handle) {
               auto feedback = std::make_shared<Patrol::Feedback>();
               auto result = std::make_shared<Patrol::Result>();
               const auto goal = goal_handle->get_goal();
               rclcpp::Rate rate{1.0};

               for (int i{1}; i <= goal->num_waypoints; ++i) {
                 if (goal_handle->is_canceling()) {
                   result->success = false;
                   result->message = "Patrol canceled.";
                   goal_handle->canceled(result);
                   RCLCPP_INFO(get_logger(), "Patrol canceled.");
                   return;
                 }
                 feedback->current_waypoint = i;
                 goal_handle->publish_feedback(feedback);
                 RCLCPP_INFO(get_logger(), "Visiting waypoint %d/%d",
                             i, goal->num_waypoints);
                 rate.sleep();
               }

               result->success = true;
               result->message = "Patrol complete. Visited " +
                                 std::to_string(goal->num_waypoints) +
                                 " waypoints.";
               goal_handle->succeed(result);
               RCLCPP_INFO(get_logger(), "%s", result->message.c_str());
             }

             rclcpp_action::Server<Patrol>::SharedPtr action_server_;
           };

           int main(int argc, char* argv[]) {
             rclcpp::init(argc, argv);
             rclcpp::spin(std::make_shared<PatrolServer>());
             rclcpp::shutdown();
             return 0;
           }


.. dropdown:: Exercise 6 -- Challenge: Integrated Communication System
    :icon: gear
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Build a system that uses all three communication patterns working
    together.

    **Specification**

    Design and implement a multi-node system with the following
    components:

    1. **Sensor Publisher** (topic): a node that publishes simulated
       battery level (``std_msgs/msg/Float64``) on ``/battery_level``
       at 2 Hz. The level starts at 100.0 and decreases by 1.0 each
       publication.

    2. **Status Service** (service): a node that provides a
       ``/get_status`` service using ``std_srvs/srv/Trigger``. When
       called, it returns ``success = true`` and a message with the
       current system status (e.g., ``"System OK"``).

    3. **Patrol Action** (action): reuse or extend the patrol server
       from Exercise 5. Before starting the patrol, the server should
       call the ``/get_status`` service to check the system status. If
       the service returns ``success = false``, abort the goal.

    4. **Coordinator** (action client + subscriber): a node that:

       - Subscribes to ``/battery_level``.
       - When battery drops below 50.0, sends a patrol goal to
         ``/patrol`` with 3 waypoints.
       - Logs feedback as it arrives.
       - Logs the final result.

    5. Use a launch file to start all four nodes.

    .. dropdown:: Solution
        :class-container: sd-border-success

        This exercise is open-ended. A complete solution requires
        multiple files across two or more packages. Below is an outline
        of the key design decisions:

        - **Sensor publisher**: straightforward timer-based publisher.
          Use ``create_wall_timer`` at 500 ms.
        - **Status service**: a minimal service server with a
          ``Trigger`` callback.
        - **Patrol action server**: in ``handle_accepted``, before
          entering the waypoint loop, create a synchronous service
          client call to ``/get_status``. If the result is
          ``success = false``, call ``goal_handle->abort(result)``.
        - **Coordinator**: combine a subscription callback (for
          ``/battery_level``) with an action client. Use a flag to
          ensure the goal is sent only once.
        - **Launch file** (Python):

          .. code-block:: python

             from launch import LaunchDescription
             from launch_ros.actions import Node

             def generate_launch_description():
                 return LaunchDescription([
                     Node(package='robot_service', executable='status_server'),
                     Node(package='robot_action', executable='patrol_server'),
                     Node(package='robot_sensor', executable='battery_publisher'),
                     Node(package='robot_coordinator', executable='coordinator'),
                 ])

        Build all packages, source the workspace, and run:

        .. code-block:: bash

           ros2 launch robot_coordinator system_launch.py
