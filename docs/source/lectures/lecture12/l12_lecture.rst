====================================================
Lecture
====================================================


Communication Patterns Overview
====================================================

ROS 2 provides three built-in communication patterns. Each pattern
addresses a different category of inter-node interaction.

.. list-table:: Communication Pattern Comparison
   :header-rows: 1
   :widths: 18 28 28 26

   * - Feature
     - Topics (Pub/Sub)
     - Services
     - Actions
   * - Direction
     - Many-to-many
     - One-to-one (client to server)
     - One-to-one (client to server)
   * - Style
     - Asynchronous, continuous
     - Synchronous request-response
     - Asynchronous goal-feedback-result
   * - Use case
     - Streaming sensor data, commands
     - Quick queries, configuration
     - Long-running tasks with progress
   * - Feedback
     - No built-in feedback
     - Single response
     - Periodic feedback during execution
   * - Preemptable
     - N/A
     - No
     - Yes (goals can be canceled)
   * - Example
     - ``/scan``, ``/cmd_vel``
     - ``/spawn``, ``/set_parameters``
     - ``/navigate_to_pose``

Topics (Publish-Subscribe)
--------------------------

Topics use the **publish-subscribe** pattern covered in L10. Publishers
send messages to a named topic; any number of subscribers can receive
them. Communication is decoupled -- publishers and subscribers do not
know about each other.

- **Many-to-many**: multiple publishers and subscribers per topic.
- **Continuous**: data streams at a configured rate.
- **Asynchronous**: publishers do not wait for subscribers.

Services (Request-Response)
---------------------------

A **service** is a synchronous exchange between exactly one client and
one server. The client sends a **request**, the server processes it and
returns a **response**. The interaction is complete in a single
round-trip.

- **One-to-one**: one server per service name, clients take turns.
- **Synchronous from the client's perspective**: the client waits for
  the response (though the underlying call is async in ``rclcpp``).
- **Short-lived**: the callback should return quickly.

Actions (Goal-Feedback-Result)
------------------------------

An **action** models a long-running task. The client sends a **goal**;
the server may accept or reject it. While executing, the server
publishes **feedback** messages to report progress. When done, the
server returns a **result**. The client can also **cancel** a goal.

- **One-to-one**: one server, one or more clients.
- **Asynchronous**: the client does not block while the goal executes.
- **Preemptable**: goals can be canceled mid-execution.


Services
====================================================

What Is a Service?
------------------

A ROS 2 service implements the **request-response** pattern. A single
node advertises a service under a name (e.g., ``/add_two_ints``). Any
node can create a client, send a request, and receive a response.

.. code-block:: text

   Client ── Request ──> Server
   Client <── Response ── Server

Unlike topics, the communication is **bidirectional** and
**transactional**: the client expects exactly one response per request.

Service Definition (``.srv`` Files)
-----------------------------------

A ``.srv`` file defines the request and response types, separated by
``---``:

.. code-block:: text

   # AddTwoInts.srv
   int64 a
   int64 b
   ---
   int64 sum

- Fields above ``---`` form the **request**.
- Fields below ``---`` form the **response**.

Standard Service Types
~~~~~~~~~~~~~~~~~~~~~~

ROS 2 ships several service types in ``std_srvs`` and ``example_interfaces``:

- ``std_srvs/srv/Trigger`` -- empty request, bool success + string message.
- ``std_srvs/srv/SetBool`` -- bool request, bool success + string message.
- ``example_interfaces/srv/AddTwoInts`` -- two int64 fields, one int64 sum.

Creating a Custom ``.srv``
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Create an interface package (or reuse an existing one):

   .. code-block:: bash

      ros2 pkg create --build-type ament_cmake my_interfaces

2. Create the ``srv/`` directory and the ``.srv`` file:

   .. code-block:: bash

      mkdir -p my_interfaces/srv

3. Add the ``.srv`` file, e.g., ``srv/ComputeSum.srv``:

   .. code-block:: text

      int64 a
      int64 b
      ---
      int64 sum

4. Update ``CMakeLists.txt``:

   .. code-block:: cmake

      find_package(rosidl_default_generators REQUIRED)

      rosidl_generate_interfaces(${PROJECT_NAME}
        "srv/ComputeSum.srv"
      )

5. Update ``package.xml``:

   .. code-block:: xml

      <buildtool_depend>rosidl_default_generators</buildtool_depend>
      <exec_depend>rosidl_default_runtime</exec_depend>
      <member_of_group>rosidl_interface_packages</member_of_group>

6. Build with ``colcon build``.

Service Server
--------------

A service server is created with ``create_service``. The template
parameter is the service type. The callback receives the request and
must populate the response.

.. code-block:: cpp

   #include <rclcpp/rclcpp.hpp>
   #include "my_interfaces/srv/compute_sum.hpp"

   class SumServer : public rclcpp::Node {
    public:
     SumServer() : Node{"sum_server"} {
       service_ = create_service<my_interfaces::srv::ComputeSum>(
         "compute_sum",
         std::bind(&SumServer::handle_request, this,
                   std::placeholders::_1, std::placeholders::_2));
       RCLCPP_INFO(get_logger(), "Service server ready.");
     }

    private:
     void handle_request(
         const std::shared_ptr<my_interfaces::srv::ComputeSum::Request> request,
         std::shared_ptr<my_interfaces::srv::ComputeSum::Response> response) {
       response->sum = request->a + request->b;
       RCLCPP_INFO(get_logger(), "Request: %ld + %ld = %ld",
                   request->a, request->b, response->sum);
     }

     rclcpp::Service<my_interfaces::srv::ComputeSum>::SharedPtr service_;
   };

   int main(int argc, char* argv[]) {
     rclcpp::init(argc, argv);
     rclcpp::spin(std::make_shared<SumServer>());
     rclcpp::shutdown();
     return 0;
   }

Key points:

- ``create_service<SrvType>(name, callback)`` advertises the service.
- The callback signature takes a ``shared_ptr`` to the request and a
  ``shared_ptr`` to the response.
- The response is populated in-place; no return value is needed.

Service Client
--------------

A service client calls the service asynchronously with
``async_send_request``.

.. code-block:: cpp

   #include <rclcpp/rclcpp.hpp>
   #include "my_interfaces/srv/compute_sum.hpp"

   class SumClient : public rclcpp::Node {
    public:
     SumClient() : Node{"sum_client"} {
       client_ = create_client<my_interfaces::srv::ComputeSum>("compute_sum");
     }

     void send_request(int64_t a, int64_t b) {
       // Wait for the service to become available
       while (!client_->wait_for_service(std::chrono::seconds{1})) {
         if (!rclcpp::ok()) {
           RCLCPP_ERROR(get_logger(), "Interrupted while waiting.");
           return;
         }
         RCLCPP_INFO(get_logger(), "Waiting for service...");
       }

       auto request =
           std::make_shared<my_interfaces::srv::ComputeSum::Request>();
       request->a = a;
       request->b = b;

       auto future = client_->async_send_request(
           request,
           std::bind(&SumClient::response_callback, this,
                     std::placeholders::_1));
     }

    private:
     void response_callback(
         rclcpp::Client<my_interfaces::srv::ComputeSum>::SharedFuture future) {
       auto response = future.get();
       RCLCPP_INFO(get_logger(), "Result: %ld", response->sum);
     }

     rclcpp::Client<my_interfaces::srv::ComputeSum>::SharedPtr client_;
   };

   int main(int argc, char* argv[]) {
     rclcpp::init(argc, argv);
     auto node = std::make_shared<SumClient>();
     node->send_request(3, 5);
     rclcpp::spin(node);
     rclcpp::shutdown();
     return 0;
   }

Key points:

- ``create_client<SrvType>(name)`` creates the client.
- ``wait_for_service`` blocks until the server is available.
- ``async_send_request`` returns a ``SharedFuture``. A callback can be
  attached or you can call ``future.get()`` (blocking).

CMakeLists.txt for a Service Node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the package that contains the server/client nodes:

.. code-block:: cmake

   find_package(rclcpp REQUIRED)
   find_package(my_interfaces REQUIRED)

   add_executable(sum_server src/sum_server.cpp)
   ament_target_dependencies(sum_server rclcpp my_interfaces)

   add_executable(sum_client src/sum_client.cpp)
   ament_target_dependencies(sum_client rclcpp my_interfaces)

   install(TARGETS sum_server sum_client
     DESTINATION lib/${PROJECT_NAME})

Service CLI Tools
-----------------

.. code-block:: bash

   # List all active services
   ros2 service list

   # Show the type of a service
   ros2 service type /compute_sum

   # Call a service from the command line
   ros2 service call /compute_sum my_interfaces/srv/ComputeSum "{a: 3, b: 5}"


Actions
====================================================

What Is an Action?
------------------

An action models a **long-running task** with three phases:

1. **Goal**: the client sends a goal to the server.
2. **Feedback**: while executing, the server publishes progress updates.
3. **Result**: when complete, the server returns the final result.

.. code-block:: text

   Client ── Goal ──────> Server
   Client <── Feedback ── Server   (periodic)
   Client <── Result ──── Server   (once, at completion)

Actions are built on top of topics and services internally, but
``rclcpp_action`` provides a clean high-level API.

Action Definition (``.action`` Files)
--------------------------------------

An ``.action`` file has three sections separated by ``---``:

.. code-block:: text

   # Countdown.action
   int32 target_number
   ---
   bool success
   string message
   ---
   int32 current_number

- **Goal** (above first ``---``): what the client requests.
- **Result** (between the two ``---``): what the server returns on completion.
- **Feedback** (below second ``---``): progress updates during execution.

Creating a Custom ``.action``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. In the interface package, create an ``action/`` directory:

   .. code-block:: bash

      mkdir -p my_interfaces/action

2. Add the ``.action`` file, e.g., ``action/Countdown.action``:

   .. code-block:: text

      int32 target_number
      ---
      bool success
      string message
      ---
      int32 current_number

3. Update ``CMakeLists.txt``:

   .. code-block:: cmake

      rosidl_generate_interfaces(${PROJECT_NAME}
        "srv/ComputeSum.srv"
        "action/Countdown.action"
      )

4. Build with ``colcon build``.

Action Server
-------------

An action server uses the ``rclcpp_action`` library. You must provide
callbacks for handling goals, cancellation, and execution.

.. code-block:: cpp

   #include <rclcpp/rclcpp.hpp>
   #include <rclcpp_action/rclcpp_action.hpp>
   #include "my_interfaces/action/countdown.hpp"

   using Countdown = my_interfaces::action::Countdown;
   using GoalHandleCountdown = rclcpp_action::ServerGoalHandle<Countdown>;

   class CountdownServer : public rclcpp::Node {
    public:
     CountdownServer() : Node{"countdown_server"} {
       action_server_ = rclcpp_action::create_server<Countdown>(
           this,
           "countdown",
           std::bind(&CountdownServer::handle_goal, this,
                     std::placeholders::_1, std::placeholders::_2),
           std::bind(&CountdownServer::handle_cancel, this,
                     std::placeholders::_1),
           std::bind(&CountdownServer::handle_accepted, this,
                     std::placeholders::_1));
       RCLCPP_INFO(get_logger(), "Action server ready.");
     }

    private:
     // Decide whether to accept or reject a goal
     rclcpp_action::GoalResponse handle_goal(
         const rclcpp_action::GoalUUID& /*uuid*/,
         std::shared_ptr<const Countdown::Goal> goal) {
       RCLCPP_INFO(get_logger(), "Received goal: count down to %d",
                   goal->target_number);
       if (goal->target_number < 0) {
         return rclcpp_action::GoalResponse::REJECT;
       }
       return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
     }

     // Decide whether to accept a cancel request
     rclcpp_action::CancelResponse handle_cancel(
         const std::shared_ptr<GoalHandleCountdown> /*goal_handle*/) {
       RCLCPP_INFO(get_logger(), "Cancel request received.");
       return rclcpp_action::CancelResponse::ACCEPT;
     }

     // Called when a goal is accepted -- start execution in a thread
     void handle_accepted(
         const std::shared_ptr<GoalHandleCountdown> goal_handle) {
       std::thread{
           std::bind(&CountdownServer::execute, this, std::placeholders::_1),
           goal_handle}
           .detach();
     }

     // Execute the goal
     void execute(const std::shared_ptr<GoalHandleCountdown> goal_handle) {
       RCLCPP_INFO(get_logger(), "Executing goal...");
       auto feedback = std::make_shared<Countdown::Feedback>();
       auto result = std::make_shared<Countdown::Result>();
       const auto goal = goal_handle->get_goal();
       rclcpp::Rate rate{1.0};  // 1 Hz

       int current{10};
       while (current > goal->target_number && rclcpp::ok()) {
         // Check for cancellation
         if (goal_handle->is_canceling()) {
           result->success = false;
           result->message = "Countdown canceled.";
           goal_handle->canceled(result);
           RCLCPP_INFO(get_logger(), "Goal canceled.");
           return;
         }

         // Publish feedback
         feedback->current_number = current;
         goal_handle->publish_feedback(feedback);
         RCLCPP_INFO(get_logger(), "Feedback: %d", current);
         --current;
         rate.sleep();
       }

       // Send result
       result->success = true;
       result->message = "Countdown complete!";
       goal_handle->succeed(result);
       RCLCPP_INFO(get_logger(), "Goal succeeded.");
     }

     rclcpp_action::Server<Countdown>::SharedPtr action_server_;
   };

   int main(int argc, char* argv[]) {
     rclcpp::init(argc, argv);
     rclcpp::spin(std::make_shared<CountdownServer>());
     rclcpp::shutdown();
     return 0;
   }

Key points:

- ``rclcpp_action::create_server<ActionType>`` takes three callbacks:

  - **handle_goal**: accept or reject the incoming goal.
  - **handle_cancel**: accept or reject a cancel request.
  - **handle_accepted**: called when the goal is accepted; start
    execution (typically in a new thread).

- Inside ``execute``:

  - Use ``goal_handle->publish_feedback(feedback)`` to send progress.
  - Use ``goal_handle->is_canceling()`` to check for cancellation.
  - Call ``goal_handle->succeed(result)`` or ``goal_handle->canceled(result)``
    to finish.

Action Client
-------------

An action client sends goals and registers callbacks for the response,
feedback, and result.

.. code-block:: cpp

   #include <rclcpp/rclcpp.hpp>
   #include <rclcpp_action/rclcpp_action.hpp>
   #include "my_interfaces/action/countdown.hpp"

   using Countdown = my_interfaces::action::Countdown;
   using GoalHandleCountdown = rclcpp_action::ClientGoalHandle<Countdown>;

   class CountdownClient : public rclcpp::Node {
    public:
     CountdownClient() : Node{"countdown_client"} {
       client_ = rclcpp_action::create_client<Countdown>(this, "countdown");
     }

     void send_goal(int32_t target) {
       if (!client_->wait_for_action_server(std::chrono::seconds{5})) {
         RCLCPP_ERROR(get_logger(), "Action server not available.");
         return;
       }

       auto goal = Countdown::Goal{};
       goal.target_number = target;

       auto send_goal_options =
           rclcpp_action::Client<Countdown>::SendGoalOptions{};
       send_goal_options.goal_response_callback =
           std::bind(&CountdownClient::goal_response_callback, this,
                     std::placeholders::_1);
       send_goal_options.feedback_callback =
           std::bind(&CountdownClient::feedback_callback, this,
                     std::placeholders::_1, std::placeholders::_2);
       send_goal_options.result_callback =
           std::bind(&CountdownClient::result_callback, this,
                     std::placeholders::_1);

       client_->async_send_goal(goal, send_goal_options);
       RCLCPP_INFO(get_logger(), "Goal sent.");
     }

    private:
     void goal_response_callback(
         const GoalHandleCountdown::SharedPtr& goal_handle) {
       if (!goal_handle) {
         RCLCPP_ERROR(get_logger(), "Goal was rejected by server.");
       } else {
         RCLCPP_INFO(get_logger(), "Goal accepted by server.");
       }
     }

     void feedback_callback(
         GoalHandleCountdown::SharedPtr /*goal_handle*/,
         const std::shared_ptr<const Countdown::Feedback> feedback) {
       RCLCPP_INFO(get_logger(), "Feedback: %d", feedback->current_number);
     }

     void result_callback(
         const GoalHandleCountdown::WrappedResult& result) {
       switch (result.code) {
         case rclcpp_action::ResultCode::SUCCEEDED:
           RCLCPP_INFO(get_logger(), "Result: %s",
                       result.result->message.c_str());
           break;
         case rclcpp_action::ResultCode::ABORTED:
           RCLCPP_ERROR(get_logger(), "Goal was aborted.");
           break;
         case rclcpp_action::ResultCode::CANCELED:
           RCLCPP_WARN(get_logger(), "Goal was canceled.");
           break;
         default:
           RCLCPP_ERROR(get_logger(), "Unknown result code.");
           break;
       }
       rclcpp::shutdown();
     }

     rclcpp_action::Client<Countdown>::SharedPtr client_;
   };

   int main(int argc, char* argv[]) {
     rclcpp::init(argc, argv);
     auto node = std::make_shared<CountdownClient>();
     node->send_goal(0);
     rclcpp::spin(node);
     return 0;
   }

Key points:

- ``rclcpp_action::create_client<ActionType>`` creates the client.
- ``SendGoalOptions`` lets you attach three callbacks:

  - **goal_response_callback**: called when the server accepts or
    rejects the goal.
  - **feedback_callback**: called each time the server publishes
    feedback.
  - **result_callback**: called once when the action completes (or is
    canceled/aborted).

- ``async_send_goal(goal, options)`` sends the goal without blocking.

CMakeLists.txt for an Action Node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cmake

   find_package(rclcpp REQUIRED)
   find_package(rclcpp_action REQUIRED)
   find_package(my_interfaces REQUIRED)

   add_executable(countdown_server src/countdown_server.cpp)
   ament_target_dependencies(countdown_server
     rclcpp rclcpp_action my_interfaces)

   add_executable(countdown_client src/countdown_client.cpp)
   ament_target_dependencies(countdown_client
     rclcpp rclcpp_action my_interfaces)

   install(TARGETS countdown_server countdown_client
     DESTINATION lib/${PROJECT_NAME})

Remember to add ``<depend>rclcpp_action</depend>`` to ``package.xml``.

Action CLI Tools
----------------

.. code-block:: bash

   # List all active actions
   ros2 action list

   # Show information about an action
   ros2 action info /countdown

   # Send a goal from the command line (with feedback)
   ros2 action send_goal /countdown my_interfaces/action/Countdown \
     "{target_number: 0}" --feedback


When to Use What
====================================================

Choosing the right communication pattern depends on the nature of the
interaction.

.. list-table:: Decision Guide
   :header-rows: 1
   :widths: 30 70

   * - Scenario
     - Recommended Pattern
   * - Continuous sensor data (LiDAR, IMU, camera)
     - **Topic** -- publisher streams data; subscribers process it.
   * - Periodic velocity commands
     - **Topic** -- ``/cmd_vel`` published at a fixed rate.
   * - Quick computation (e.g., add two numbers)
     - **Service** -- send request, get immediate response.
   * - Configuration query (e.g., get/set a parameter)
     - **Service** -- one-off request-response.
   * - Spawning/deleting an entity
     - **Service** -- short-lived, immediate result.
   * - Navigation to a waypoint
     - **Action** -- long-running, needs progress feedback.
   * - Robot arm trajectory execution
     - **Action** -- takes time, client needs to monitor progress.
   * - Any task the operator may want to cancel
     - **Action** -- supports goal cancellation.

**Rules of thumb:**

1. Use a **topic** when data flows continuously and you do not need a
   response.
2. Use a **service** when you need a response and the server can reply
   quickly (a few milliseconds).
3. Use an **action** when the task takes a noticeable amount of time,
   you want feedback, or you need the ability to cancel.

.. warning::

   Never perform long-running work inside a service callback. The
   client will block waiting for the response, and the server's
   executor thread is occupied. Use an action for anything that takes
   more than a trivial amount of time.
