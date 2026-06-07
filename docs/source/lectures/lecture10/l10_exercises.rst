====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 10: ROS 2
Foundations. Work through them in order, as each exercise builds on the
skills from the previous one. Build and run each program in your ROS 2
workspace to verify your understanding.

.. note::

   Build all exercises with:

   .. code-block:: bash

      cd ~/ros2_ws
      colcon build --packages-select <package_name>
      source install/setup.bash


----


.. dropdown:: Exercise 1 -- Basic Node
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create a minimal ROS 2 node that logs a message when it starts.

    **Specification**

    1. Create a new ROS 2 package called ``basic_node_pkg`` with a dependency
       on ``rclcpp``.

    2. Write a node class ``BasicNode`` that inherits from ``rclcpp::Node``
       with:

       - Node name: ``"basic_node"``.
       - In the constructor, log an info message: ``"Basic node has been started"``.

    3. In ``main()``, initialize ROS 2, create the node, spin it, and shut down.

    4. Update ``CMakeLists.txt`` to build and install the executable.

    5. Build, source, and run the node.

    .. dropdown:: Solution
        :class-container: sd-border-success

        **Create the package:**

        .. code-block:: bash

           cd ~/ros2_ws/src
           ros2 pkg create --build-type ament_cmake \
               --node-name basic_node basic_node_pkg \
               --dependencies rclcpp

        **src/basic_node.cpp:**

        .. code-block:: cpp

           #include "rclcpp/rclcpp.hpp"

           class BasicNode : public rclcpp::Node {
            public:
             BasicNode() : Node("basic_node") {
                 RCLCPP_INFO(this->get_logger(), "Basic node has been started\n");
             }
           };

           int main(int argc, char* argv[]) {
               rclcpp::init(argc, argv);
               auto node{std::make_shared<BasicNode>()};
               rclcpp::spin(node);
               rclcpp::shutdown();
               return 0;
           }

        **CMakeLists.txt:**

        .. code-block:: cmake

           cmake_minimum_required(VERSION 3.8)
           project(basic_node_pkg)

           if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
             add_compile_options(-Wall -Wextra -Wpedantic)
           endif()

           find_package(ament_cmake REQUIRED)
           find_package(rclcpp REQUIRED)

           add_executable(basic_node src/basic_node.cpp)
           ament_target_dependencies(basic_node rclcpp)

           install(TARGETS
             basic_node
             DESTINATION lib/${PROJECT_NAME})

           ament_package()

        **Build and run:**

        .. code-block:: bash

           cd ~/ros2_ws
           colcon build --packages-select basic_node_pkg
           source install/setup.bash
           ros2 run basic_node_pkg basic_node

        **Expected output:**

        .. code-block:: text

           [INFO] [basic_node]: Basic node has been started


.. dropdown:: Exercise 2 -- Simple Publisher
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create a publisher node that publishes an incrementing counter on a
    topic every second.

    **Specification**

    1. Create a package ``counter_pub_pkg`` with dependencies on ``rclcpp``
       and ``std_msgs``.

    2. Write a node class ``CounterPublisher`` that:

       - Has node name ``"counter_publisher"``.
       - Publishes ``std_msgs::msg::Int32`` messages on the topic ``"counter"`` (queue size 10).
       - Uses a wall timer with a 1-second period.
       - Maintains a ``count_`` member variable (starting at 0) that increments each time.
       - Logs the published value using ``RCLCPP_INFO``.

    3. Build, source, and run. Verify with ``ros2 topic echo /counter``.

    .. dropdown:: Solution
        :class-container: sd-border-success

        **src/counter_publisher.cpp:**

        .. code-block:: cpp

           #include "rclcpp/rclcpp.hpp"
           #include "std_msgs/msg/int32.hpp"

           class CounterPublisher : public rclcpp::Node {
            public:
             CounterPublisher() : Node("counter_publisher"), count_{0} {
                 publisher_ = this->create_publisher<std_msgs::msg::Int32>("counter", 10);
                 timer_ = this->create_wall_timer(
                     std::chrono::seconds(1),
                     std::bind(&CounterPublisher::timer_callback, this));
             }

            private:
             void timer_callback() {
                 auto msg{std_msgs::msg::Int32()};
                 msg.data = count_;
                 RCLCPP_INFO(this->get_logger(), "Publishing: %d\n", msg.data);
                 publisher_->publish(msg);
                 count_++;
             }

             rclcpp::Publisher<std_msgs::msg::Int32>::SharedPtr publisher_;
             rclcpp::TimerBase::SharedPtr timer_;
             int count_;
           };

           int main(int argc, char* argv[]) {
               rclcpp::init(argc, argv);
               auto node{std::make_shared<CounterPublisher>()};
               rclcpp::spin(node);
               rclcpp::shutdown();
               return 0;
           }

        **Verify in a separate terminal:**

        .. code-block:: bash

           ros2 topic echo /counter


.. dropdown:: Exercise 3 -- Simple Subscriber
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create a subscriber node that listens to the counter topic from
    Exercise 2 and logs the received values.

    **Specification**

    1. Create a package ``counter_sub_pkg`` with dependencies on ``rclcpp``
       and ``std_msgs``.

    2. Write a node class ``CounterSubscriber`` that:

       - Has node name ``"counter_subscriber"``.
       - Subscribes to the ``"counter"`` topic (``std_msgs::msg::Int32``, queue size 10).
       - In the callback, logs the received value: ``"Received: <value>"``.

    3. Build, source, and run alongside the publisher from Exercise 2.

    .. dropdown:: Solution
        :class-container: sd-border-success

        **src/counter_subscriber.cpp:**

        .. code-block:: cpp

           #include "rclcpp/rclcpp.hpp"
           #include "std_msgs/msg/int32.hpp"

           class CounterSubscriber : public rclcpp::Node {
            public:
             CounterSubscriber() : Node("counter_subscriber") {
                 subscription_ = this->create_subscription<std_msgs::msg::Int32>(
                     "counter", 10,
                     std::bind(&CounterSubscriber::topic_callback, this,
                                std::placeholders::_1));
             }

            private:
             void topic_callback(const std_msgs::msg::Int32::SharedPtr msg) {
                 RCLCPP_INFO(this->get_logger(), "Received: %d\n", msg->data);
             }

             rclcpp::Subscription<std_msgs::msg::Int32>::SharedPtr subscription_;
           };

           int main(int argc, char* argv[]) {
               rclcpp::init(argc, argv);
               auto node{std::make_shared<CounterSubscriber>()};
               rclcpp::spin(node);
               rclcpp::shutdown();
               return 0;
           }

        **Run in two terminals:**

        .. code-block:: bash

           # Terminal 1
           ros2 run counter_pub_pkg counter_publisher

           # Terminal 2
           ros2 run counter_sub_pkg counter_subscriber

        **Expected output (Terminal 2):**

        .. code-block:: text

           [INFO] [counter_subscriber]: Received: 0
           [INFO] [counter_subscriber]: Received: 1
           [INFO] [counter_subscriber]: Received: 2
           ...


.. dropdown:: Exercise 4 -- Custom Message
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Define a custom message type and use it in a publisher/subscriber
    pair.

    **Specification**

    1. Create an interface package ``sensor_interfaces`` with:

       - A custom message ``msg/SensorReading.msg`` with fields:

         - ``string sensor_id``
         - ``float64 temperature``
         - ``float64 humidity``
         - ``uint32 timestamp``

    2. Create a node package ``sensor_pub_sub_pkg`` that depends on
       ``rclcpp`` and ``sensor_interfaces``.

    3. Write a publisher node ``SensorPublisher`` that:

       - Publishes ``sensor_interfaces::msg::SensorReading`` on the topic ``"sensor_data"`` every 2 seconds.
       - Populates each field with sample values.

    4. Write a subscriber node ``SensorSubscriber`` that:

       - Subscribes to ``"sensor_data"`` and logs all fields.

    5. Build both packages, source, and run.

    .. dropdown:: Solution
        :class-container: sd-border-success

        **Create the interface package:**

        .. code-block:: bash

           cd ~/ros2_ws/src
           ros2 pkg create --build-type ament_cmake sensor_interfaces
           mkdir -p sensor_interfaces/msg

        **sensor_interfaces/msg/SensorReading.msg:**

        .. code-block:: text

           string sensor_id
           float64 temperature
           float64 humidity
           uint32 timestamp

        **sensor_interfaces/CMakeLists.txt:**

        .. code-block:: cmake

           cmake_minimum_required(VERSION 3.8)
           project(sensor_interfaces)

           if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
             add_compile_options(-Wall -Wextra -Wpedantic)
           endif()

           find_package(ament_cmake REQUIRED)
           find_package(rosidl_default_generators REQUIRED)

           rosidl_generate_interfaces(${PROJECT_NAME}
             "msg/SensorReading.msg"
           )

           ament_package()

        **sensor_interfaces/package.xml** (add these lines):

        .. code-block:: xml

           <buildtool_depend>rosidl_default_generators</buildtool_depend>
           <exec_depend>rosidl_default_runtime</exec_depend>
           <member_of_group>rosidl_interface_packages</member_of_group>

        **sensor_pub_sub_pkg/src/sensor_publisher.cpp:**

        .. code-block:: cpp

           #include "rclcpp/rclcpp.hpp"
           #include "sensor_interfaces/msg/sensor_reading.hpp"

           class SensorPublisher : public rclcpp::Node {
            public:
             SensorPublisher() : Node("sensor_publisher") {
                 publisher_ = this->create_publisher<sensor_interfaces::msg::SensorReading>(
                     "sensor_data", 10);
                 timer_ = this->create_wall_timer(
                     std::chrono::seconds(2),
                     std::bind(&SensorPublisher::publish_reading, this));
             }

            private:
             void publish_reading() {
                 auto msg{sensor_interfaces::msg::SensorReading()};
                 msg.sensor_id = "sensor_01";
                 msg.temperature = 23.5;
                 msg.humidity = 45.2;
                 msg.timestamp = static_cast<uint32_t>(this->now().seconds());

                 RCLCPP_INFO(this->get_logger(),
                             "Publishing: id=%s, temp=%.1f, hum=%.1f\n",
                             msg.sensor_id.c_str(), msg.temperature, msg.humidity);
                 publisher_->publish(msg);
             }

             rclcpp::Publisher<sensor_interfaces::msg::SensorReading>::SharedPtr publisher_;
             rclcpp::TimerBase::SharedPtr timer_;
           };

           int main(int argc, char* argv[]) {
               rclcpp::init(argc, argv);
               auto node{std::make_shared<SensorPublisher>()};
               rclcpp::spin(node);
               rclcpp::shutdown();
               return 0;
           }

        **sensor_pub_sub_pkg/src/sensor_subscriber.cpp:**

        .. code-block:: cpp

           #include "rclcpp/rclcpp.hpp"
           #include "sensor_interfaces/msg/sensor_reading.hpp"

           class SensorSubscriber : public rclcpp::Node {
            public:
             SensorSubscriber() : Node("sensor_subscriber") {
                 subscription_ = this->create_subscription<sensor_interfaces::msg::SensorReading>(
                     "sensor_data", 10,
                     std::bind(&SensorSubscriber::reading_callback, this,
                                std::placeholders::_1));
             }

            private:
             void reading_callback(
                 const sensor_interfaces::msg::SensorReading::SharedPtr msg) {
                 RCLCPP_INFO(this->get_logger(),
                             "Sensor '%s': temp=%.1f, humidity=%.1f, time=%u\n",
                             msg->sensor_id.c_str(), msg->temperature,
                             msg->humidity, msg->timestamp);
             }

             rclcpp::Subscription<sensor_interfaces::msg::SensorReading>::SharedPtr
                 subscription_;
           };

           int main(int argc, char* argv[]) {
               rclcpp::init(argc, argv);
               auto node{std::make_shared<SensorSubscriber>()};
               rclcpp::spin(node);
               rclcpp::shutdown();
               return 0;
           }


.. dropdown:: Exercise 5 -- Multi-topic Publisher
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create a single node that publishes on two different topics
    simultaneously.

    **Specification**

    1. Create a package ``multi_topic_pkg`` with dependencies on ``rclcpp``
       and ``std_msgs``.

    2. Write a node class ``MultiTopicPublisher`` that:

       - Has node name ``"multi_topic_publisher"``.
       - Publishes ``std_msgs::msg::String`` on the topic ``"status"`` every 1 second.
       - Publishes ``std_msgs::msg::Float64`` on the topic ``"temperature"`` every 2 seconds.
       - Uses two separate timers and two separate publishers.
       - Logs each published message.

    3. Build, source, and run. Verify both topics with ``ros2 topic list``
       and ``ros2 topic echo``.

    .. dropdown:: Solution
        :class-container: sd-border-success

        **src/multi_topic_publisher.cpp:**

        .. code-block:: cpp

           #include "rclcpp/rclcpp.hpp"
           #include "std_msgs/msg/string.hpp"
           #include "std_msgs/msg/float64.hpp"

           class MultiTopicPublisher : public rclcpp::Node {
            public:
             MultiTopicPublisher()
                 : Node("multi_topic_publisher"), count_{0}, temp_{20.0} {
                 status_pub_ = this->create_publisher<std_msgs::msg::String>("status", 10);
                 temp_pub_ = this->create_publisher<std_msgs::msg::Float64>("temperature", 10);

                 status_timer_ = this->create_wall_timer(
                     std::chrono::seconds(1),
                     std::bind(&MultiTopicPublisher::publish_status, this));

                 temp_timer_ = this->create_wall_timer(
                     std::chrono::seconds(2),
                     std::bind(&MultiTopicPublisher::publish_temperature, this));
             }

            private:
             void publish_status() {
                 auto msg{std_msgs::msg::String()};
                 msg.data = "Status update #" + std::to_string(count_);
                 RCLCPP_INFO(this->get_logger(), "Status: '%s'\n", msg.data.c_str());
                 status_pub_->publish(msg);
                 count_++;
             }

             void publish_temperature() {
                 auto msg{std_msgs::msg::Float64()};
                 msg.data = temp_;
                 RCLCPP_INFO(this->get_logger(), "Temperature: %.1f\n", msg.data);
                 temp_pub_->publish(msg);
                 temp_ += 0.5;
             }

             rclcpp::Publisher<std_msgs::msg::String>::SharedPtr status_pub_;
             rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr temp_pub_;
             rclcpp::TimerBase::SharedPtr status_timer_;
             rclcpp::TimerBase::SharedPtr temp_timer_;
             int count_;
             double temp_;
           };

           int main(int argc, char* argv[]) {
               rclcpp::init(argc, argv);
               auto node{std::make_shared<MultiTopicPublisher>()};
               rclcpp::spin(node);
               rclcpp::shutdown();
               return 0;
           }

        **Verify:**

        .. code-block:: bash

           ros2 topic list
           ros2 topic echo /status
           ros2 topic echo /temperature


.. dropdown:: Exercise 6 -- Simulated Robot Pub/Sub System
    :icon: gear
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal** *(Challenge)*

    Build a complete publisher/subscriber system for a simulated robot.
    The robot publishes its position using a custom message and
    subscribes to velocity commands.

    **Specification**

    1. Create an interface package ``robot_interfaces`` with two custom
       messages:

       - ``msg/RobotPose.msg``:

         - ``string robot_name``
         - ``float64 x``
         - ``float64 y``
         - ``float64 theta``

       - ``msg/VelocityCommand.msg``:

         - ``float64 linear_velocity``
         - ``float64 angular_velocity``

    2. Create a node package ``robot_sim_pkg`` with two nodes:

       **RobotNode** (``robot_node.cpp``):

       - Publishes ``RobotPose`` on ``"robot_pose"`` every 100ms.
       - Subscribes to ``VelocityCommand`` on ``"cmd_vel"``.
       - Maintains internal state (``x_``, ``y_``, ``theta_``), all
         initialized to ``0.0``.
       - When a velocity command is received, updates the pose:

         - ``theta_ += msg->angular_velocity * 0.1``
         - ``x_ += msg->linear_velocity * cos(theta_) * 0.1``
         - ``y_ += msg->linear_velocity * sin(theta_) * 0.1``

       **ControllerNode** (``controller_node.cpp``):

       - Publishes ``VelocityCommand`` on ``"cmd_vel"`` every 500ms.
       - Subscribes to ``RobotPose`` on ``"robot_pose"``.
       - Publishes a constant forward velocity (``linear_velocity = 1.0``,
         ``angular_velocity = 0.1``).
       - Logs the latest received robot pose.

    3. Build all packages, run both nodes, and verify with CLI tools.

    .. dropdown:: Solution
        :class-container: sd-border-success

        **robot_interfaces/msg/RobotPose.msg:**

        .. code-block:: text

           string robot_name
           float64 x
           float64 y
           float64 theta

        **robot_interfaces/msg/VelocityCommand.msg:**

        .. code-block:: text

           float64 linear_velocity
           float64 angular_velocity

        **robot_interfaces/CMakeLists.txt:**

        .. code-block:: cmake

           cmake_minimum_required(VERSION 3.8)
           project(robot_interfaces)

           if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
             add_compile_options(-Wall -Wextra -Wpedantic)
           endif()

           find_package(ament_cmake REQUIRED)
           find_package(rosidl_default_generators REQUIRED)

           rosidl_generate_interfaces(${PROJECT_NAME}
             "msg/RobotPose.msg"
             "msg/VelocityCommand.msg"
           )

           ament_package()

        **robot_sim_pkg/src/robot_node.cpp:**

        .. code-block:: cpp

           #include <cmath>

           #include "rclcpp/rclcpp.hpp"
           #include "robot_interfaces/msg/robot_pose.hpp"
           #include "robot_interfaces/msg/velocity_command.hpp"

           class RobotNode : public rclcpp::Node {
            public:
             RobotNode()
                 : Node("robot_node"), x_{0.0}, y_{0.0}, theta_{0.0} {
                 pose_pub_ = this->create_publisher<robot_interfaces::msg::RobotPose>(
                     "robot_pose", 10);

                 vel_sub_ = this->create_subscription<robot_interfaces::msg::VelocityCommand>(
                     "cmd_vel", 10,
                     std::bind(&RobotNode::velocity_callback, this,
                                std::placeholders::_1));

                 timer_ = this->create_wall_timer(
                     std::chrono::milliseconds(100),
                     std::bind(&RobotNode::publish_pose, this));

                 RCLCPP_INFO(this->get_logger(), "Robot node started\n");
             }

            private:
             void velocity_callback(
                 const robot_interfaces::msg::VelocityCommand::SharedPtr msg) {
                 theta_ += msg->angular_velocity * 0.1;
                 x_ += msg->linear_velocity * std::cos(theta_) * 0.1;
                 y_ += msg->linear_velocity * std::sin(theta_) * 0.1;
             }

             void publish_pose() {
                 auto msg{robot_interfaces::msg::RobotPose()};
                 msg.robot_name = "sim_robot";
                 msg.x = x_;
                 msg.y = y_;
                 msg.theta = theta_;

                 RCLCPP_INFO(this->get_logger(),
                             "Pose: x=%.3f, y=%.3f, theta=%.3f\n",
                             msg.x, msg.y, msg.theta);
                 pose_pub_->publish(msg);
             }

             rclcpp::Publisher<robot_interfaces::msg::RobotPose>::SharedPtr pose_pub_;
             rclcpp::Subscription<robot_interfaces::msg::VelocityCommand>::SharedPtr vel_sub_;
             rclcpp::TimerBase::SharedPtr timer_;
             double x_;
             double y_;
             double theta_;
           };

           int main(int argc, char* argv[]) {
               rclcpp::init(argc, argv);
               auto node{std::make_shared<RobotNode>()};
               rclcpp::spin(node);
               rclcpp::shutdown();
               return 0;
           }

        **robot_sim_pkg/src/controller_node.cpp:**

        .. code-block:: cpp

           #include "rclcpp/rclcpp.hpp"
           #include "robot_interfaces/msg/robot_pose.hpp"
           #include "robot_interfaces/msg/velocity_command.hpp"

           class ControllerNode : public rclcpp::Node {
            public:
             ControllerNode() : Node("controller_node") {
                 vel_pub_ = this->create_publisher<robot_interfaces::msg::VelocityCommand>(
                     "cmd_vel", 10);

                 pose_sub_ = this->create_subscription<robot_interfaces::msg::RobotPose>(
                     "robot_pose", 10,
                     std::bind(&ControllerNode::pose_callback, this,
                                std::placeholders::_1));

                 timer_ = this->create_wall_timer(
                     std::chrono::milliseconds(500),
                     std::bind(&ControllerNode::publish_command, this));

                 RCLCPP_INFO(this->get_logger(), "Controller node started\n");
             }

            private:
             void pose_callback(
                 const robot_interfaces::msg::RobotPose::SharedPtr msg) {
                 RCLCPP_INFO(this->get_logger(),
                             "Robot '%s' at (%.3f, %.3f), theta=%.3f\n",
                             msg->robot_name.c_str(), msg->x, msg->y, msg->theta);
             }

             void publish_command() {
                 auto msg{robot_interfaces::msg::VelocityCommand()};
                 msg.linear_velocity = 1.0;
                 msg.angular_velocity = 0.1;
                 vel_pub_->publish(msg);
             }

             rclcpp::Publisher<robot_interfaces::msg::VelocityCommand>::SharedPtr vel_pub_;
             rclcpp::Subscription<robot_interfaces::msg::RobotPose>::SharedPtr pose_sub_;
             rclcpp::TimerBase::SharedPtr timer_;
           };

           int main(int argc, char* argv[]) {
               rclcpp::init(argc, argv);
               auto node{std::make_shared<ControllerNode>()};
               rclcpp::spin(node);
               rclcpp::shutdown();
               return 0;
           }

        **robot_sim_pkg/CMakeLists.txt:**

        .. code-block:: cmake

           cmake_minimum_required(VERSION 3.8)
           project(robot_sim_pkg)

           if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
             add_compile_options(-Wall -Wextra -Wpedantic)
           endif()

           find_package(ament_cmake REQUIRED)
           find_package(rclcpp REQUIRED)
           find_package(robot_interfaces REQUIRED)

           add_executable(robot_node src/robot_node.cpp)
           ament_target_dependencies(robot_node rclcpp robot_interfaces)

           add_executable(controller_node src/controller_node.cpp)
           ament_target_dependencies(controller_node rclcpp robot_interfaces)

           install(TARGETS
             robot_node
             controller_node
             DESTINATION lib/${PROJECT_NAME})

           ament_package()

        **Run in two terminals:**

        .. code-block:: bash

           # Terminal 1
           ros2 run robot_sim_pkg robot_node

           # Terminal 2
           ros2 run robot_sim_pkg controller_node

        **Inspect with CLI tools:**

        .. code-block:: bash

           ros2 topic list -t
           ros2 topic echo /robot_pose
           ros2 topic echo /cmd_vel
