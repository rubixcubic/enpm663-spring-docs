====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 13: ROS 2
Advanced Topics (TF2 and Lifecycle Nodes). Work through them in order,
as each exercise builds on the skills from the previous one. Build and
run each program in a ROS 2 workspace to verify your understanding.

.. note::

   All exercises require a ROS 2 Jazzy workspace. Build with:

   .. code-block:: bash

      cd ~/ros2_ws
      colcon build --packages-select my_package
      source install/setup.bash


----


.. dropdown:: Exercise 1 -- Static Transform Broadcaster
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Broadcast a static transform from ``base_link`` to ``camera_link``.

    **Specification**

    1. Create a ROS 2 node called ``static_camera_broadcaster``.
    2. Use ``tf2_ros::StaticTransformBroadcaster`` to publish a static
       transform from ``base_link`` to ``camera_link``.
    3. The camera is positioned 0.2 m forward (x), 0.0 m to the side (y),
       and 0.5 m above (z) the base_link.
    4. The camera has no rotation relative to base_link (identity
       quaternion).
    5. Log a message confirming the transform was published.
    6. Verify with: ``ros2 run tf2_ros tf2_echo base_link camera_link``

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <rclcpp/rclcpp.hpp>
           #include <tf2_ros/static_transform_broadcaster.h>
           #include <geometry_msgs/msg/transform_stamped.hpp>

           class StaticCameraBroadcaster : public rclcpp::Node {
            public:
             StaticCameraBroadcaster()
                 : Node{"static_camera_broadcaster"} {
               static_broadcaster_ =
                   std::make_shared<tf2_ros::StaticTransformBroadcaster>(this);

               geometry_msgs::msg::TransformStamped t;
               t.header.stamp = this->get_clock()->now();
               t.header.frame_id = "base_link";
               t.child_frame_id = "camera_link";

               t.transform.translation.x = 0.2;
               t.transform.translation.y = 0.0;
               t.transform.translation.z = 0.5;

               t.transform.rotation.x = 0.0;
               t.transform.rotation.y = 0.0;
               t.transform.rotation.z = 0.0;
               t.transform.rotation.w = 1.0;

               static_broadcaster_->sendTransform(t);
               RCLCPP_INFO(this->get_logger(),
                           "Published static transform: base_link -> camera_link");
             }

            private:
             std::shared_ptr<tf2_ros::StaticTransformBroadcaster> static_broadcaster_;
           };

           int main(int argc, char* argv[]) {
             rclcpp::init(argc, argv);
             rclcpp::spin(std::make_shared<StaticCameraBroadcaster>());
             rclcpp::shutdown();
             return 0;
           }


.. dropdown:: Exercise 2 -- Dynamic Transform Broadcaster (Circular Path)
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Broadcast a dynamic transform that moves a robot in a circular path
    in the world frame.

    **Specification**

    1. Create a ROS 2 node called ``circular_motion_broadcaster``.
    2. Use ``tf2_ros::TransformBroadcaster`` to publish the transform
       from ``world`` to ``base_link`` at 10 Hz.
    3. The robot should move in a circle of radius 2.0 m centered at the
       origin:

       - ``x = 2.0 * cos(angle)``
       - ``y = 2.0 * sin(angle)``
       - ``z = 0.0``

    4. Increment the angle by 0.05 radians each timer callback.
    5. Set the rotation quaternion to represent the robot facing the
       direction of travel (yaw = angle + pi/2). For simplicity, you may
       use an identity quaternion.
    6. Verify with: ``ros2 run tf2_ros tf2_echo world base_link``

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <rclcpp/rclcpp.hpp>
           #include <tf2_ros/transform_broadcaster.h>
           #include <geometry_msgs/msg/transform_stamped.hpp>
           #include <cmath>

           class CircularMotionBroadcaster : public rclcpp::Node {
            public:
             CircularMotionBroadcaster()
                 : Node{"circular_motion_broadcaster"}, angle_{0.0} {
               tf_broadcaster_ =
                   std::make_unique<tf2_ros::TransformBroadcaster>(this);

               timer_ = this->create_wall_timer(
                   std::chrono::milliseconds{100},
                   std::bind(&CircularMotionBroadcaster::broadcast_transform,
                             this));
             }

            private:
             void broadcast_transform() {
               geometry_msgs::msg::TransformStamped t;
               t.header.stamp = this->get_clock()->now();
               t.header.frame_id = "world";
               t.child_frame_id = "base_link";

               double radius{2.0};
               t.transform.translation.x = radius * std::cos(angle_);
               t.transform.translation.y = radius * std::sin(angle_);
               t.transform.translation.z = 0.0;

               // Identity quaternion for simplicity
               t.transform.rotation.x = 0.0;
               t.transform.rotation.y = 0.0;
               t.transform.rotation.z = 0.0;
               t.transform.rotation.w = 1.0;

               tf_broadcaster_->sendTransform(t);

               RCLCPP_INFO(this->get_logger(),
                           "Robot at (%.2f, %.2f)",
                           t.transform.translation.x,
                           t.transform.translation.y);

               angle_ += 0.05;
             }

             std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
             rclcpp::TimerBase::SharedPtr timer_;
             double angle_;
           };

           int main(int argc, char* argv[]) {
             rclcpp::init(argc, argv);
             rclcpp::spin(std::make_shared<CircularMotionBroadcaster>());
             rclcpp::shutdown();
             return 0;
           }


.. dropdown:: Exercise 3 -- Transform Listener (Distance Computation)
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Listen for transforms and compute the distance between two frames.

    **Specification**

    1. Create a ROS 2 node called ``distance_calculator``.
    2. Use ``tf2_ros::Buffer`` and ``tf2_ros::TransformListener`` to
       listen for transforms.
    3. Every second, look up the transform from ``world`` to
       ``camera_link``.
    4. Compute the Euclidean distance from the world origin to the
       camera_link frame:

       - ``distance = sqrt(x^2 + y^2 + z^2)``

    5. Log the distance.
    6. Handle ``tf2::TransformException`` with a warning message.
    7. Test by running the circular motion broadcaster (Exercise 2) and
       the static camera broadcaster (Exercise 1) simultaneously.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <rclcpp/rclcpp.hpp>
           #include <tf2_ros/buffer.h>
           #include <tf2_ros/transform_listener.h>
           #include <geometry_msgs/msg/transform_stamped.hpp>
           #include <tf2/exceptions.h>
           #include <cmath>

           class DistanceCalculator : public rclcpp::Node {
            public:
             DistanceCalculator()
                 : Node{"distance_calculator"} {
               tf_buffer_ =
                   std::make_unique<tf2_ros::Buffer>(this->get_clock());
               tf_listener_ =
                   std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);

               timer_ = this->create_wall_timer(
                   std::chrono::seconds{1},
                   std::bind(&DistanceCalculator::compute_distance, this));
             }

            private:
             void compute_distance() {
               try {
                 auto t = tf_buffer_->lookupTransform(
                     "world", "camera_link", tf2::TimePointZero);

                 double x{t.transform.translation.x};
                 double y{t.transform.translation.y};
                 double z{t.transform.translation.z};
                 double distance{std::sqrt(x * x + y * y + z * z)};

                 RCLCPP_INFO(this->get_logger(),
                             "Distance from world to camera_link: %.3f m",
                             distance);

               } catch (const tf2::TransformException& ex) {
                 RCLCPP_WARN(this->get_logger(),
                             "Could not get transform: %s", ex.what());
               }
             }

             std::unique_ptr<tf2_ros::Buffer> tf_buffer_;
             std::shared_ptr<tf2_ros::TransformListener> tf_listener_;
             rclcpp::TimerBase::SharedPtr timer_;
           };

           int main(int argc, char* argv[]) {
             rclcpp::init(argc, argv);
             rclcpp::spin(std::make_shared<DistanceCalculator>());
             rclcpp::shutdown();
             return 0;
           }


.. dropdown:: Exercise 4 -- Basic Lifecycle Node
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create a lifecycle node with logging in each transition callback.

    **Specification**

    1. Create a lifecycle node called ``basic_lifecycle_node``.
    2. Inherit from ``rclcpp_lifecycle::LifecycleNode``.
    3. Implement all five transition callbacks:

       - ``on_configure`` -- log "Configuring..." and return SUCCESS.
       - ``on_activate`` -- log "Activating..." and return SUCCESS.
       - ``on_deactivate`` -- log "Deactivating..." and return SUCCESS.
       - ``on_cleanup`` -- log "Cleaning up..." and return SUCCESS.
       - ``on_shutdown`` -- log "Shutting down..." and return SUCCESS.

    4. Test using the CLI:

       .. code-block:: bash

          ros2 lifecycle set /basic_lifecycle_node configure
          ros2 lifecycle set /basic_lifecycle_node activate
          ros2 lifecycle set /basic_lifecycle_node deactivate
          ros2 lifecycle set /basic_lifecycle_node cleanup
          ros2 lifecycle set /basic_lifecycle_node shutdown

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <rclcpp/rclcpp.hpp>
           #include <rclcpp_lifecycle/lifecycle_node.hpp>

           using CallbackReturn =
               rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn;

           class BasicLifecycleNode
               : public rclcpp_lifecycle::LifecycleNode {
            public:
             BasicLifecycleNode()
                 : LifecycleNode{"basic_lifecycle_node"} {
               RCLCPP_INFO(this->get_logger(), "Node created (Unconfigured)");
             }

             CallbackReturn on_configure(
                 const rclcpp_lifecycle::State& /*previous_state*/) override {
               RCLCPP_INFO(this->get_logger(), "Configuring...");
               return CallbackReturn::SUCCESS;
             }

             CallbackReturn on_activate(
                 const rclcpp_lifecycle::State& /*previous_state*/) override {
               RCLCPP_INFO(this->get_logger(), "Activating...");
               return CallbackReturn::SUCCESS;
             }

             CallbackReturn on_deactivate(
                 const rclcpp_lifecycle::State& /*previous_state*/) override {
               RCLCPP_INFO(this->get_logger(), "Deactivating...");
               return CallbackReturn::SUCCESS;
             }

             CallbackReturn on_cleanup(
                 const rclcpp_lifecycle::State& /*previous_state*/) override {
               RCLCPP_INFO(this->get_logger(), "Cleaning up...");
               return CallbackReturn::SUCCESS;
             }

             CallbackReturn on_shutdown(
                 const rclcpp_lifecycle::State& /*previous_state*/) override {
               RCLCPP_INFO(this->get_logger(), "Shutting down...");
               return CallbackReturn::SUCCESS;
             }
           };

           int main(int argc, char* argv[]) {
             rclcpp::init(argc, argv);
             rclcpp::spin(
                 std::make_shared<BasicLifecycleNode>()
                     ->get_node_base_interface());
             rclcpp::shutdown();
             return 0;
           }


.. dropdown:: Exercise 5 -- Lifecycle Sensor Node
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create a lifecycle sensor node that only publishes data when in the
    Active state.

    **Specification**

    1. Create a lifecycle node called ``lifecycle_temperature_sensor``.
    2. In ``on_configure``:

       - Create a ``LifecyclePublisher`` for ``std_msgs::msg::Float64``
         on topic ``/temperature``.
       - Create a timer that fires every 1 second.
       - Initialize a temperature value to 20.0.

    3. In ``on_activate``:

       - Log that the sensor is active and publishing.

    4. In ``on_deactivate``:

       - Log that the sensor has stopped publishing.

    5. In ``on_cleanup``:

       - Reset the publisher and timer.

    6. In ``on_shutdown``:

       - Reset the publisher and timer.

    7. In the timer callback:

       - Check if the node is in the Active state before publishing.
       - Publish the temperature value with a small random fluctuation.
       - Log the published value.

    8. Test: configure, activate, observe data, deactivate, verify data
       stops, re-activate, observe data resumes.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <rclcpp/rclcpp.hpp>
           #include <rclcpp_lifecycle/lifecycle_node.hpp>
           #include <std_msgs/msg/float64.hpp>
           #include <lifecycle_msgs/msg/state.hpp>
           #include <random>

           using CallbackReturn =
               rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn;

           class LifecycleTemperatureSensor
               : public rclcpp_lifecycle::LifecycleNode {
            public:
             LifecycleTemperatureSensor()
                 : LifecycleNode{"lifecycle_temperature_sensor"},
                   temperature_{20.0},
                   gen_{rd_()},
                   dist_{-0.5, 0.5} {
               RCLCPP_INFO(this->get_logger(), "Node created (Unconfigured)");
             }

             CallbackReturn on_configure(
                 const rclcpp_lifecycle::State& /*previous_state*/) override {
               RCLCPP_INFO(this->get_logger(), "Configuring sensor...");
               publisher_ = this->create_publisher<std_msgs::msg::Float64>(
                   "/temperature", 10);
               timer_ = this->create_wall_timer(
                   std::chrono::seconds{1},
                   std::bind(&LifecycleTemperatureSensor::publish_temperature,
                             this));
               temperature_ = 20.0;
               return CallbackReturn::SUCCESS;
             }

             CallbackReturn on_activate(
                 const rclcpp_lifecycle::State& /*previous_state*/) override {
               RCLCPP_INFO(this->get_logger(),
                           "Sensor active -- publishing temperature data");
               return CallbackReturn::SUCCESS;
             }

             CallbackReturn on_deactivate(
                 const rclcpp_lifecycle::State& /*previous_state*/) override {
               RCLCPP_INFO(this->get_logger(),
                           "Sensor deactivated -- stopped publishing");
               return CallbackReturn::SUCCESS;
             }

             CallbackReturn on_cleanup(
                 const rclcpp_lifecycle::State& /*previous_state*/) override {
               RCLCPP_INFO(this->get_logger(), "Cleaning up sensor...");
               publisher_.reset();
               timer_.reset();
               return CallbackReturn::SUCCESS;
             }

             CallbackReturn on_shutdown(
                 const rclcpp_lifecycle::State& /*previous_state*/) override {
               RCLCPP_INFO(this->get_logger(), "Shutting down sensor...");
               publisher_.reset();
               timer_.reset();
               return CallbackReturn::SUCCESS;
             }

            private:
             void publish_temperature() {
               if (this->get_current_state().id() !=
                   lifecycle_msgs::msg::State::PRIMARY_STATE_ACTIVE) {
                 return;
               }
               temperature_ += dist_(gen_);
               auto msg = std_msgs::msg::Float64{};
               msg.data = temperature_;
               publisher_->publish(msg);
               RCLCPP_INFO(this->get_logger(),
                           "Temperature: %.2f C", temperature_);
             }

             rclcpp_lifecycle::LifecyclePublisher<std_msgs::msg::Float64>::SharedPtr
                 publisher_;
             rclcpp::TimerBase::SharedPtr timer_;
             double temperature_;
             std::random_device rd_;
             std::mt19937 gen_;
             std::uniform_real_distribution<double> dist_;
           };

           int main(int argc, char* argv[]) {
             rclcpp::init(argc, argv);
             rclcpp::spin(
                 std::make_shared<LifecycleTemperatureSensor>()
                     ->get_node_base_interface());
             rclcpp::shutdown();
             return 0;
           }


.. dropdown:: Exercise 6 -- Challenge: Multi-Frame Robot with Lifecycle Management
    :icon: gear
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Build a complete system that combines TF2 frame management with
    lifecycle node control. This exercise integrates all concepts from
    the lecture.

    **Specification**

    1. Create a **lifecycle node** called ``robot_system_node`` that
       manages a robot with sensors.

    2. In ``on_configure``:

       - Create a ``tf2_ros::StaticTransformBroadcaster`` and publish
         two static transforms:

         - ``base_link`` -> ``camera_link`` (0.15 m forward, 0.4 m up)
         - ``base_link`` -> ``lidar_link`` (0.0 m forward, 0.3 m up)

       - Create a ``tf2_ros::TransformBroadcaster`` for the robot's
         dynamic motion.
       - Create a ``LifecyclePublisher`` for ``std_msgs::msg::String``
         on topic ``/sensor_status``.
       - Create a timer at 10 Hz.

    3. In ``on_activate``:

       - Log that the robot system is active.
       - Set a flag ``active_`` to true.

    4. In ``on_deactivate``:

       - Set ``active_`` to false.
       - Log that the robot system is paused.

    5. In the timer callback:

       - If not active, return immediately.
       - Broadcast a dynamic transform from ``world`` to ``base_link``
         (robot moves in a figure-eight pattern):

         - ``x = 3.0 * sin(angle)``
         - ``y = 3.0 * sin(angle) * cos(angle)``

       - Publish a sensor status message with the current position.
       - Increment the angle.

    6. In ``on_cleanup`` and ``on_shutdown``:

       - Reset all publishers, broadcasters, and the timer.

    7. Test the full lifecycle: configure -> activate -> observe frames
       and messages -> deactivate -> verify publishing stops -> activate
       again -> shutdown.

    8. Use ``ros2 run tf2_tools view_frames`` to verify the frame tree.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <rclcpp/rclcpp.hpp>
           #include <rclcpp_lifecycle/lifecycle_node.hpp>
           #include <tf2_ros/static_transform_broadcaster.h>
           #include <tf2_ros/transform_broadcaster.h>
           #include <geometry_msgs/msg/transform_stamped.hpp>
           #include <std_msgs/msg/string.hpp>
           #include <lifecycle_msgs/msg/state.hpp>
           #include <cmath>
           #include <sstream>

           using CallbackReturn =
               rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn;

           class RobotSystemNode
               : public rclcpp_lifecycle::LifecycleNode {
            public:
             RobotSystemNode()
                 : LifecycleNode{"robot_system_node"},
                   angle_{0.0},
                   active_{false} {
               RCLCPP_INFO(this->get_logger(), "Robot system created (Unconfigured)");
             }

             CallbackReturn on_configure(
                 const rclcpp_lifecycle::State& /*previous_state*/) override {
               RCLCPP_INFO(this->get_logger(), "Configuring robot system...");

               // Static transforms for sensors
               static_broadcaster_ =
                   std::make_shared<tf2_ros::StaticTransformBroadcaster>(this);

               geometry_msgs::msg::TransformStamped camera_tf;
               camera_tf.header.stamp = this->get_clock()->now();
               camera_tf.header.frame_id = "base_link";
               camera_tf.child_frame_id = "camera_link";
               camera_tf.transform.translation.x = 0.15;
               camera_tf.transform.translation.y = 0.0;
               camera_tf.transform.translation.z = 0.4;
               camera_tf.transform.rotation.w = 1.0;

               geometry_msgs::msg::TransformStamped lidar_tf;
               lidar_tf.header.stamp = this->get_clock()->now();
               lidar_tf.header.frame_id = "base_link";
               lidar_tf.child_frame_id = "lidar_link";
               lidar_tf.transform.translation.x = 0.0;
               lidar_tf.transform.translation.y = 0.0;
               lidar_tf.transform.translation.z = 0.3;
               lidar_tf.transform.rotation.w = 1.0;

               static_broadcaster_->sendTransform(camera_tf);
               static_broadcaster_->sendTransform(lidar_tf);

               // Dynamic transform broadcaster
               tf_broadcaster_ =
                   std::make_unique<tf2_ros::TransformBroadcaster>(this);

               // Sensor status publisher
               status_publisher_ =
                   this->create_publisher<std_msgs::msg::String>(
                       "/sensor_status", 10);

               // Timer at 10 Hz
               timer_ = this->create_wall_timer(
                   std::chrono::milliseconds{100},
                   std::bind(&RobotSystemNode::update, this));

               angle_ = 0.0;
               active_ = false;

               RCLCPP_INFO(this->get_logger(), "Robot system configured");
               return CallbackReturn::SUCCESS;
             }

             CallbackReturn on_activate(
                 const rclcpp_lifecycle::State& /*previous_state*/) override {
               active_ = true;
               RCLCPP_INFO(this->get_logger(), "Robot system ACTIVE");
               return CallbackReturn::SUCCESS;
             }

             CallbackReturn on_deactivate(
                 const rclcpp_lifecycle::State& /*previous_state*/) override {
               active_ = false;
               RCLCPP_INFO(this->get_logger(), "Robot system PAUSED");
               return CallbackReturn::SUCCESS;
             }

             CallbackReturn on_cleanup(
                 const rclcpp_lifecycle::State& /*previous_state*/) override {
               RCLCPP_INFO(this->get_logger(), "Cleaning up robot system...");
               status_publisher_.reset();
               timer_.reset();
               return CallbackReturn::SUCCESS;
             }

             CallbackReturn on_shutdown(
                 const rclcpp_lifecycle::State& /*previous_state*/) override {
               RCLCPP_INFO(this->get_logger(), "Shutting down robot system...");
               status_publisher_.reset();
               timer_.reset();
               return CallbackReturn::SUCCESS;
             }

            private:
             void update() {
               if (!active_) {
                 return;
               }

               // Broadcast dynamic transform: world -> base_link
               geometry_msgs::msg::TransformStamped t;
               t.header.stamp = this->get_clock()->now();
               t.header.frame_id = "world";
               t.child_frame_id = "base_link";

               // Figure-eight path
               double x{3.0 * std::sin(angle_)};
               double y{3.0 * std::sin(angle_) * std::cos(angle_)};
               t.transform.translation.x = x;
               t.transform.translation.y = y;
               t.transform.translation.z = 0.0;
               t.transform.rotation.w = 1.0;

               tf_broadcaster_->sendTransform(t);

               // Publish sensor status
               auto msg = std_msgs::msg::String{};
               std::ostringstream oss;
               oss << "Robot at (" << x << ", " << y << ")";
               msg.data = oss.str();
               status_publisher_->publish(msg);

               angle_ += 0.02;
             }

             std::shared_ptr<tf2_ros::StaticTransformBroadcaster>
                 static_broadcaster_;
             std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
             rclcpp_lifecycle::LifecyclePublisher<std_msgs::msg::String>::SharedPtr
                 status_publisher_;
             rclcpp::TimerBase::SharedPtr timer_;
             double angle_;
             bool active_;
           };

           int main(int argc, char* argv[]) {
             rclcpp::init(argc, argv);
             rclcpp::spin(
                 std::make_shared<RobotSystemNode>()
                     ->get_node_base_interface());
             rclcpp::shutdown();
             return 0;
           }
