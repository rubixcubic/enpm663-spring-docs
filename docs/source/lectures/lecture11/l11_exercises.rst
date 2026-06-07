====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 11: ROS 2
Configuration and Orchestration. Work through them in order, as each exercise
builds on the skills from the previous one. Build and run each program in a
ROS 2 workspace to verify your understanding.

.. note::

   Build all ROS 2 packages with:

   .. code-block:: bash

      cd ~/ros2_ws && colcon build --packages-select my_package
      source install/setup.bash


----


.. dropdown:: Exercise 1 -- Parameterized Node
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice declaring and retrieving parameters on a ROS 2 node.

    **Specification**

    1. Create a node called ``param_demo_node`` that inherits from ``rclcpp::Node``.

    2. In the constructor, declare the following parameters with default values:

       - ``robot_name`` (string): ``"default_robot"``
       - ``max_speed`` (double): ``1.0``
       - ``num_sensors`` (int): ``3``
       - ``verbose`` (bool): ``false``

    3. Retrieve each parameter value using ``get_parameter()`` and log them
       with ``RCLCPP_INFO``.

    4. Create a timer (1-second period) that logs the robot name and speed
       each tick.

    5. Test by running:

       .. code-block:: bash

          ros2 run my_package param_demo_node --ros-args -p robot_name:=atlas -p max_speed:=2.5

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <rclcpp/rclcpp.hpp>
           #include <string>

           class ParamDemoNode : public rclcpp::Node {
            public:
             ParamDemoNode() : Node("param_demo_node") {
                 this->declare_parameter<std::string>("robot_name", "default_robot");
                 this->declare_parameter<double>("max_speed", 1.0);
                 this->declare_parameter<int>("num_sensors", 3);
                 this->declare_parameter<bool>("verbose", false);

                 robot_name_ = this->get_parameter("robot_name").as_string();
                 max_speed_ = this->get_parameter("max_speed").as_double();
                 int num_sensors{static_cast<int>(
                     this->get_parameter("num_sensors").as_integer())};
                 bool verbose{this->get_parameter("verbose").as_bool()};

                 RCLCPP_INFO(this->get_logger(),
                             "Robot: %s, Speed: %.2f, Sensors: %d, Verbose: %s",
                             robot_name_.c_str(), max_speed_, num_sensors,
                             verbose ? "true" : "false");

                 timer_ = this->create_wall_timer(
                     std::chrono::seconds(1),
                     std::bind(&ParamDemoNode::timer_callback, this));
             }

            private:
             void timer_callback() {
                 RCLCPP_INFO(this->get_logger(), "[%s] Speed: %.2f",
                             robot_name_.c_str(), max_speed_);
             }

             std::string robot_name_;
             double max_speed_;
             rclcpp::TimerBase::SharedPtr timer_;
           };

           int main(int argc, char* argv[]) {
               rclcpp::init(argc, argv);
               rclcpp::spin(std::make_shared<ParamDemoNode>());
               rclcpp::shutdown();
               return 0;
           }


.. dropdown:: Exercise 2 -- Dynamic Parameter Update
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Add a parameter callback that logs and validates parameter changes at
    runtime.

    **Specification**

    1. Start from the node in Exercise 1.

    2. Add a parameter callback using ``add_on_set_parameters_callback`` that:

       - Logs the name and new value of every parameter that changes.
       - Rejects ``max_speed`` values that are negative or greater than ``10.0``.
       - Updates the member variables (``robot_name_``, ``max_speed_``) when
         the change is accepted.

    3. Store the callback handle as a class member.

    4. Test by running the node, then in another terminal:

       .. code-block:: bash

          ros2 param set /param_demo_node max_speed 5.0
          ros2 param set /param_demo_node max_speed -1.0
          ros2 param set /param_demo_node robot_name optimus

    5. Verify that the timer output reflects accepted changes and that the
       negative speed is rejected.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <rclcpp/rclcpp.hpp>
           #include <string>

           class ParamDemoNode : public rclcpp::Node {
            public:
             ParamDemoNode() : Node("param_demo_node") {
                 this->declare_parameter<std::string>("robot_name", "default_robot");
                 this->declare_parameter<double>("max_speed", 1.0);

                 robot_name_ = this->get_parameter("robot_name").as_string();
                 max_speed_ = this->get_parameter("max_speed").as_double();

                 param_cb_handle_ = this->add_on_set_parameters_callback(
                     std::bind(&ParamDemoNode::on_param_change, this,
                               std::placeholders::_1));

                 timer_ = this->create_wall_timer(
                     std::chrono::seconds(1),
                     std::bind(&ParamDemoNode::timer_callback, this));
             }

            private:
             void timer_callback() {
                 RCLCPP_INFO(this->get_logger(), "[%s] Speed: %.2f",
                             robot_name_.c_str(), max_speed_);
             }

             rcl_interfaces::msg::SetParametersResult on_param_change(
                 const std::vector<rclcpp::Parameter>& parameters) {
                 rcl_interfaces::msg::SetParametersResult result;
                 result.successful = true;

                 for (const auto& param : parameters) {
                     RCLCPP_INFO(this->get_logger(), "Parameter '%s' changing",
                                 param.get_name().c_str());

                     if (param.get_name() == "max_speed") {
                         double val{param.as_double()};
                         if (val < 0.0 || val > 10.0) {
                             result.successful = false;
                             result.reason = "max_speed must be in [0.0, 10.0]";
                             RCLCPP_WARN(this->get_logger(), "Rejected: %s",
                                         result.reason.c_str());
                             return result;
                         }
                         max_speed_ = val;
                     } else if (param.get_name() == "robot_name") {
                         robot_name_ = param.as_string();
                     }
                 }
                 return result;
             }

             std::string robot_name_;
             double max_speed_;
             rclcpp::TimerBase::SharedPtr timer_;
             rclcpp::node_interfaces::OnSetParametersCallbackHandle::SharedPtr
                 param_cb_handle_;
           };

           int main(int argc, char* argv[]) {
               rclcpp::init(argc, argv);
               rclcpp::spin(std::make_shared<ParamDemoNode>());
               rclcpp::shutdown();
               return 0;
           }


.. dropdown:: Exercise 3 -- Basic Launch File
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write a Python launch file that starts two nodes simultaneously.

    **Specification**

    1. Create a ``launch/`` directory in your package.

    2. Write a ``demo.launch.py`` file that starts two instances of your
       ``param_demo_node`` with different names:

       - Node 1: name ``robot_a``, parameter ``robot_name`` set to ``"alpha"``
       - Node 2: name ``robot_b``, parameter ``robot_name`` set to ``"beta"``

    3. Add the ``install(DIRECTORY launch/ ...)`` directive to your
       ``CMakeLists.txt``.

    4. Build and test:

       .. code-block:: bash

          colcon build --packages-select my_package
          source install/setup.bash
          ros2 launch my_package demo.launch.py

    5. In another terminal, verify both nodes are running:

       .. code-block:: bash

          ros2 node list

    .. dropdown:: Solution
        :class-container: sd-border-success

        **launch/demo.launch.py:**

        .. code-block:: python

           from launch import LaunchDescription
           from launch_ros.actions import Node

           def generate_launch_description():
               return LaunchDescription([
                   Node(
                       package='my_package',
                       executable='param_demo_node',
                       name='robot_a',
                       output='screen',
                       parameters=[{'robot_name': 'alpha'}],
                   ),
                   Node(
                       package='my_package',
                       executable='param_demo_node',
                       name='robot_b',
                       output='screen',
                       parameters=[{'robot_name': 'beta'}],
                   ),
               ])

        **CMakeLists.txt addition:**

        .. code-block:: cmake

           install(DIRECTORY launch/
             DESTINATION share/${PROJECT_NAME}/launch
           )


.. dropdown:: Exercise 4 -- Launch with Parameters and YAML
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Pass parameters via a YAML configuration file and use launch arguments to
    make the launch file configurable.

    **Specification**

    1. Create a ``config/params.yaml`` file with the following content:

       .. code-block:: yaml

          robot_a:
            ros__parameters:
              robot_name: "alpha"
              max_speed: 2.0

          robot_b:
            ros__parameters:
              robot_name: "beta"
              max_speed: 3.5

    2. Write a ``system.launch.py`` that:

       - Declares a launch argument ``config_file`` with a default value
         pointing to your YAML file.
       - Starts ``robot_a`` and ``robot_b`` using parameters from the YAML
         file.

    3. Add the ``config/`` directory to your ``CMakeLists.txt`` install rules.

    4. Build and test:

       .. code-block:: bash

          ros2 launch my_package system.launch.py

    5. Override the config file from the command line:

       .. code-block:: bash

          ros2 launch my_package system.launch.py config_file:=/path/to/other.yaml

    .. dropdown:: Solution
        :class-container: sd-border-success

        **launch/system.launch.py:**

        .. code-block:: python

           import os
           from launch import LaunchDescription
           from launch.actions import DeclareLaunchArgument
           from launch.substitutions import LaunchConfiguration
           from launch_ros.actions import Node
           from ament_index_python.packages import get_package_share_directory

           def generate_launch_description():
               default_config = os.path.join(
                   get_package_share_directory('my_package'),
                   'config',
                   'params.yaml'
               )

               config_arg = DeclareLaunchArgument(
                   'config_file',
                   default_value=default_config,
                   description='Path to the parameter YAML file'
               )

               config = LaunchConfiguration('config_file')

               return LaunchDescription([
                   config_arg,
                   Node(
                       package='my_package',
                       executable='param_demo_node',
                       name='robot_a',
                       output='screen',
                       parameters=[config],
                   ),
                   Node(
                       package='my_package',
                       executable='param_demo_node',
                       name='robot_b',
                       output='screen',
                       parameters=[config],
                   ),
               ])

        **CMakeLists.txt addition:**

        .. code-block:: cmake

           install(DIRECTORY launch/ config/
             DESTINATION share/${PROJECT_NAME}/
           )


.. dropdown:: Exercise 5 -- Multi-Threaded Executor
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create a node that uses a ``MultiThreadedExecutor`` with callback groups
    to allow concurrent execution of a timer and a subscription.

    **Specification**

    1. Create a node called ``multi_executor_node``.

    2. Create two callback groups:

       - A **mutually exclusive** group for a timer.
       - A **reentrant** group for a subscription.

    3. Create a timer (1-second period) in the exclusive group that:

       - Simulates heavy work with ``std::this_thread::sleep_for(2s)``.
       - Logs the thread ID.

    4. Create a subscription to ``/chatter`` (``std_msgs::msg::String``) in
       the reentrant group that:

       - Logs the received message and thread ID.

    5. In ``main()``, use a ``MultiThreadedExecutor`` instead of
       ``rclcpp::spin()``.

    6. Test:

       - Run the node.
       - In another terminal: ``ros2 topic pub /chatter std_msgs/msg/String "{data: 'hello'}" -r 2``
       - Observe that subscription callbacks are not blocked by the
         long-running timer callback.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <chrono>
           #include <rclcpp/rclcpp.hpp>
           #include <std_msgs/msg/string.hpp>
           #include <thread>

           using namespace std::chrono_literals;

           class MultiExecutorNode : public rclcpp::Node {
            public:
             MultiExecutorNode() : Node("multi_executor_node") {
                 // Create callback groups
                 exclusive_group_ = this->create_callback_group(
                     rclcpp::CallbackGroupType::MutuallyExclusive);
                 reentrant_group_ = this->create_callback_group(
                     rclcpp::CallbackGroupType::Reentrant);

                 // Timer in the exclusive group (simulates heavy work)
                 timer_ = this->create_wall_timer(
                     1s,
                     std::bind(&MultiExecutorNode::timer_callback, this),
                     exclusive_group_);

                 // Subscription in the reentrant group
                 rclcpp::SubscriptionOptions sub_options;
                 sub_options.callback_group = reentrant_group_;

                 subscription_ = this->create_subscription<std_msgs::msg::String>(
                     "/chatter", 10,
                     std::bind(&MultiExecutorNode::topic_callback, this,
                               std::placeholders::_1),
                     sub_options);
             }

            private:
             void timer_callback() {
                 RCLCPP_INFO(this->get_logger(),
                             "Timer start (thread %ld) -- sleeping 2s...",
                             std::this_thread::get_id());
                 std::this_thread::sleep_for(2s);
                 RCLCPP_INFO(this->get_logger(), "Timer done");
             }

             void topic_callback(const std_msgs::msg::String::SharedPtr msg) {
                 RCLCPP_INFO(this->get_logger(),
                             "Received: '%s' (thread %ld)",
                             msg->data.c_str(), std::this_thread::get_id());
             }

             rclcpp::CallbackGroup::SharedPtr exclusive_group_;
             rclcpp::CallbackGroup::SharedPtr reentrant_group_;
             rclcpp::TimerBase::SharedPtr timer_;
             rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
           };

           int main(int argc, char* argv[]) {
               rclcpp::init(argc, argv);

               auto node = std::make_shared<MultiExecutorNode>();

               rclcpp::executors::MultiThreadedExecutor executor;
               executor.add_node(node);
               executor.spin();

               rclcpp::shutdown();
               return 0;
           }


.. dropdown:: Exercise 6 -- Challenge: Configurable Robot System
    :icon: rocket
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Build a complete, configurable multi-node robot system that brings
    together parameters, YAML configuration, launch files, and executors.

    **Specification**

    1. Create two node types:

       **SensorNode** (``sensor_node.cpp``):

       - Declares parameters: ``sensor_name`` (string), ``publish_rate_ms`` (int),
         ``noise_level`` (double).
       - Publishes ``std_msgs::msg::Float64`` on a topic ``/<sensor_name>/data``
         at the configured rate.
       - The published value is a simulated reading: a base value plus random
         noise scaled by ``noise_level``.
       - Has a parameter callback that accepts runtime changes to
         ``noise_level`` (must be >= 0).

       **MonitorNode** (``monitor_node.cpp``):

       - Declares parameters: ``sensor_names`` (string array), ``threshold`` (double).
       - Subscribes to each sensor's topic.
       - Uses a ``MultiThreadedExecutor`` with a reentrant callback group
         for all subscriptions.
       - Logs a warning when any reading exceeds ``threshold``.

    2. Create a ``config/robot_system.yaml``:

       .. code-block:: yaml

          lidar_sensor:
            ros__parameters:
              sensor_name: "lidar"
              publish_rate_ms: 200
              noise_level: 0.5

          camera_sensor:
            ros__parameters:
              sensor_name: "camera"
              publish_rate_ms: 100
              noise_level: 0.3

          monitor:
            ros__parameters:
              sensor_names:
                - "lidar"
                - "camera"
              threshold: 8.0

    3. Create a ``launch/robot_system.launch.py`` that:

       - Declares a ``config_file`` launch argument.
       - Starts two ``SensorNode`` instances (``lidar_sensor`` and
         ``camera_sensor``) with parameters from the YAML file.
       - Starts one ``MonitorNode`` (``monitor``) with parameters from the
         YAML file.

    4. Build, launch, and verify:

       - Both sensors publish data.
       - The monitor subscribes and logs warnings when thresholds are
         exceeded.
       - Change ``noise_level`` at runtime:

         .. code-block:: bash

            ros2 param set /lidar_sensor noise_level 5.0

    .. dropdown:: Solution
        :class-container: sd-border-success

        **sensor_node.cpp:**

        .. code-block:: cpp

           #include <chrono>
           #include <random>
           #include <rclcpp/rclcpp.hpp>
           #include <std_msgs/msg/float64.hpp>
           #include <string>

           class SensorNode : public rclcpp::Node {
            public:
             SensorNode() : Node("sensor_node"), gen_{rd_()} {
                 this->declare_parameter<std::string>("sensor_name", "sensor");
                 this->declare_parameter<int>("publish_rate_ms", 500);
                 this->declare_parameter<double>("noise_level", 0.1);

                 sensor_name_ = this->get_parameter("sensor_name").as_string();
                 noise_level_ = this->get_parameter("noise_level").as_double();
                 int rate_ms{static_cast<int>(
                     this->get_parameter("publish_rate_ms").as_integer())};

                 std::string topic{"/" + sensor_name_ + "/data"};
                 publisher_ = this->create_publisher<std_msgs::msg::Float64>(topic, 10);

                 timer_ = this->create_wall_timer(
                     std::chrono::milliseconds(rate_ms),
                     std::bind(&SensorNode::publish_reading, this));

                 param_cb_ = this->add_on_set_parameters_callback(
                     std::bind(&SensorNode::on_param_change, this,
                               std::placeholders::_1));

                 RCLCPP_INFO(this->get_logger(),
                             "SensorNode '%s' publishing on %s every %d ms",
                             sensor_name_.c_str(), topic.c_str(), rate_ms);
             }

            private:
             void publish_reading() {
                 std::normal_distribution<double> dist{5.0, noise_level_};
                 auto msg = std_msgs::msg::Float64();
                 msg.data = dist(gen_);
                 publisher_->publish(msg);
             }

             rcl_interfaces::msg::SetParametersResult on_param_change(
                 const std::vector<rclcpp::Parameter>& parameters) {
                 rcl_interfaces::msg::SetParametersResult result;
                 result.successful = true;
                 for (const auto& p : parameters) {
                     if (p.get_name() == "noise_level") {
                         double val{p.as_double()};
                         if (val < 0.0) {
                             result.successful = false;
                             result.reason = "noise_level must be >= 0";
                             return result;
                         }
                         noise_level_ = val;
                         RCLCPP_INFO(this->get_logger(),
                                     "noise_level updated to %.2f", val);
                     }
                 }
                 return result;
             }

             std::string sensor_name_;
             double noise_level_;
             std::random_device rd_;
             std::mt19937 gen_;
             rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr publisher_;
             rclcpp::TimerBase::SharedPtr timer_;
             rclcpp::node_interfaces::OnSetParametersCallbackHandle::SharedPtr
                 param_cb_;
           };

           int main(int argc, char* argv[]) {
               rclcpp::init(argc, argv);
               rclcpp::spin(std::make_shared<SensorNode>());
               rclcpp::shutdown();
               return 0;
           }

        **monitor_node.cpp:**

        .. code-block:: cpp

           #include <functional>
           #include <rclcpp/rclcpp.hpp>
           #include <std_msgs/msg/float64.hpp>
           #include <string>
           #include <vector>

           class MonitorNode : public rclcpp::Node {
            public:
             MonitorNode() : Node("monitor_node") {
                 this->declare_parameter<std::vector<std::string>>(
                     "sensor_names", std::vector<std::string>{});
                 this->declare_parameter<double>("threshold", 10.0);

                 auto sensor_names =
                     this->get_parameter("sensor_names").as_string_array();
                 threshold_ = this->get_parameter("threshold").as_double();

                 reentrant_group_ = this->create_callback_group(
                     rclcpp::CallbackGroupType::Reentrant);
                 rclcpp::SubscriptionOptions sub_options;
                 sub_options.callback_group = reentrant_group_;

                 for (const auto& name : sensor_names) {
                     std::string topic{"/" + name + "/data"};
                     auto cb = [this, name](
                                   const std_msgs::msg::Float64::SharedPtr msg) {
                         if (msg->data > threshold_) {
                             RCLCPP_WARN(this->get_logger(),
                                         "[%s] Reading %.2f exceeds threshold %.2f",
                                         name.c_str(), msg->data, threshold_);
                         } else {
                             RCLCPP_INFO(this->get_logger(),
                                         "[%s] Reading: %.2f", name.c_str(),
                                         msg->data);
                         }
                     };
                     subscriptions_.push_back(
                         this->create_subscription<std_msgs::msg::Float64>(
                             topic, 10, cb, sub_options));
                     RCLCPP_INFO(this->get_logger(), "Subscribed to %s",
                                 topic.c_str());
                 }
             }

            private:
             double threshold_;
             rclcpp::CallbackGroup::SharedPtr reentrant_group_;
             std::vector<rclcpp::Subscription<std_msgs::msg::Float64>::SharedPtr>
                 subscriptions_;
           };

           int main(int argc, char* argv[]) {
               rclcpp::init(argc, argv);
               auto node = std::make_shared<MonitorNode>();
               rclcpp::executors::MultiThreadedExecutor executor;
               executor.add_node(node);
               executor.spin();
               rclcpp::shutdown();
               return 0;
           }

        **launch/robot_system.launch.py:**

        .. code-block:: python

           import os
           from launch import LaunchDescription
           from launch.actions import DeclareLaunchArgument
           from launch.substitutions import LaunchConfiguration
           from launch_ros.actions import Node
           from ament_index_python.packages import get_package_share_directory

           def generate_launch_description():
               default_config = os.path.join(
                   get_package_share_directory('my_package'),
                   'config',
                   'robot_system.yaml'
               )

               config_arg = DeclareLaunchArgument(
                   'config_file',
                   default_value=default_config,
                   description='Path to the parameter YAML file'
               )

               config = LaunchConfiguration('config_file')

               return LaunchDescription([
                   config_arg,
                   Node(
                       package='my_package',
                       executable='sensor_node',
                       name='lidar_sensor',
                       output='screen',
                       parameters=[config],
                   ),
                   Node(
                       package='my_package',
                       executable='sensor_node',
                       name='camera_sensor',
                       output='screen',
                       parameters=[config],
                   ),
                   Node(
                       package='my_package',
                       executable='monitor_node',
                       name='monitor',
                       output='screen',
                       parameters=[config],
                   ),
               ])
