.. _gp3:

===============================================
GP3: Coordinate Frames and Lifecycle Nodes
===============================================

Overview
--------

This is the final extension of the Group Project system. You will add coordinate frame management with **TF2** for spatial reasoning and **lifecycle nodes** for proper system startup and shutdown. These additions demonstrate production-quality ROS 2 development practices -- the kind of architecture used in real warehouse robotics systems. By the end of this assignment your team will have built a complete, multi-node ROS 2 system that spans publishers, subscribers, services, actions, coordinate frames, and lifecycle management.

-------------------
Learning Objectives
-------------------

By the end of this assignment you will be able to:

#. Broadcast static and dynamic transforms using TF2.
#. Listen for and use transforms between coordinate frames.
#. Implement lifecycle nodes for managed startup and shutdown.
#. Coordinate lifecycle transitions across multiple nodes.
#. Build a production-ready multi-node ROS 2 system.

------------
Requirements
------------

.. dropdown:: Static Transforms
   :open:
   :color: primary

   - Broadcast static transforms for fixed spatial relationships, for example:

     - ``base_link`` |rarr| ``camera_link``
     - ``base_link`` |rarr| ``lidar_link``

   - Use ``tf2_ros::StaticTransformBroadcaster``.

   .. code-block:: cpp
      :caption: Example static transform broadcast

      auto static_broadcaster_ =
          std::make_shared<tf2_ros::StaticTransformBroadcaster>(this);

      geometry_msgs::msg::TransformStamped t;
      t.header.stamp = this->get_clock()->now();
      t.header.frame_id = "base_link";
      t.child_frame_id = "camera_link";
      t.transform.translation.x = 0.1;
      t.transform.translation.y = 0.0;
      t.transform.translation.z = 0.3;

      static_broadcaster_->sendTransform(t);

.. dropdown:: Dynamic Transforms
   :open:
   :color: primary

   - Broadcast the robot's pose as a dynamic transform (e.g., ``world`` |rarr| ``robot_base_link``).
   - Update the transform based on odometry or commanded motion.
   - Use ``tf2_ros::TransformBroadcaster`` with a timer callback.

   .. code-block:: cpp
      :caption: Example dynamic transform broadcast

      auto tf_broadcaster_ =
          std::make_unique<tf2_ros::TransformBroadcaster>(*this);

      void odom_callback(const nav_msgs::msg::Odometry::SharedPtr msg)
      {
        geometry_msgs::msg::TransformStamped t;
        t.header.stamp = msg->header.stamp;
        t.header.frame_id = "world";
        t.child_frame_id = "robot_base_link";
        t.transform.translation.x = msg->pose.pose.position.x;
        t.transform.translation.y = msg->pose.pose.position.y;
        t.transform.translation.z = msg->pose.pose.position.z;
        t.transform.rotation = msg->pose.pose.orientation;

        tf_broadcaster_->sendTransform(t);
      }

.. dropdown:: Transform Listener
   :open:
   :color: primary

   - Create a node that listens for transforms between frames.
   - Use ``tf2_ros::Buffer`` and ``tf2_ros::TransformListener``.
   - Compute and display distances or spatial relationships between frames (e.g., distance from robot to a goal frame).
   - Handle transform exceptions gracefully (``tf2::TransformException``).

   .. code-block:: cpp
      :caption: Example transform lookup

      tf2_ros::Buffer tf_buffer_{this->get_clock()};
      tf2_ros::TransformListener tf_listener_{tf_buffer_};

      try {
        auto t = tf_buffer_.lookupTransform(
            "world", "robot_base_link", tf2::TimePointZero);
        RCLCPP_INFO(this->get_logger(),
            "Robot position: x=%.2f, y=%.2f\n",
            t.transform.translation.x,
            t.transform.translation.y);
      } catch (const tf2::TransformException& ex) {
        RCLCPP_WARN(this->get_logger(),
            "Could not get transform: %s\n", ex.what());
      }

.. dropdown:: Lifecycle Nodes
   :open:
   :color: primary

   - Convert **at least 2** existing nodes to lifecycle nodes (``rclcpp_lifecycle::LifecycleNode``).
   - Implement the following transition callbacks:

     - ``on_configure`` -- set up publishers, subscribers, parameters.
     - ``on_activate`` -- start publishing, enable processing.
     - ``on_deactivate`` -- stop publishing, pause processing.
     - ``on_cleanup`` -- release resources.
     - ``on_shutdown`` -- final cleanup.

   - Sensors should **only** publish data when the node is in the **Active** state.
   - Demonstrate proper state transitions through logging and behavior changes.

   .. code-block:: cpp
      :caption: Example lifecycle node

      class SensorNode : public rclcpp_lifecycle::LifecycleNode {
       public:
        SensorNode(const rclcpp::NodeOptions& options)
            : rclcpp_lifecycle::LifecycleNode{"sensor_node", options} {}

        CallbackReturn on_configure(const rclcpp_lifecycle::State&) override
        {
          RCLCPP_INFO(this->get_logger(), "Configuring sensor node\n");
          scan_pub_ = this->create_publisher<sensor_msgs::msg::LaserScan>(
              "scan_filtered", 10);
          return CallbackReturn::SUCCESS;
        }

        CallbackReturn on_activate(const rclcpp_lifecycle::State&) override
        {
          RCLCPP_INFO(this->get_logger(), "Activating sensor node\n");
          scan_pub_->on_activate();
          return CallbackReturn::SUCCESS;
        }

        CallbackReturn on_deactivate(const rclcpp_lifecycle::State&) override
        {
          RCLCPP_INFO(this->get_logger(), "Deactivating sensor node\n");
          scan_pub_->on_deactivate();
          return CallbackReturn::SUCCESS;
        }

       private:
        rclcpp_lifecycle::LifecyclePublisher<sensor_msgs::msg::LaserScan>::SharedPtr scan_pub_;
      };

.. dropdown:: System Coordination
   :open:
   :color: primary

   - Create a launch file that manages lifecycle transitions.
   - Demonstrate orderly startup:

     #. Configure all nodes.
     #. Activate sensor nodes.
     #. Activate controller nodes.

   - Demonstrate orderly shutdown in reverse order.

.. dropdown:: Integration
   :open:
   :color: primary

   - All components from GP1 and GP2 must remain fully functional.
   - TF frames must be visible in RViz2. Verify with:

     .. code-block:: bash

        ros2 run tf2_tools view_frames

   - Lifecycle states must be manageable via the CLI:

     .. code-block:: bash

        ros2 lifecycle list /sensor_node
        ros2 lifecycle set /sensor_node activate

------------
Deliverables
------------

- Final ROS 2 package(s) with all features from GP1, GP2, and GP3.
- TF2 frame tree diagram (generated via ``view_frames``).
- Updated launch file with lifecycle management.
- Final ``README.md`` with complete build, run, and usage documentation.
- Video demo (2--3 minutes) showing the full system in operation.

--------------
Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 50 15

   * - Criterion
     - Weight
   * - TF2 Frames (static broadcasts, dynamic broadcasts, transform listener)
     - 30%
   * - Lifecycle Nodes (transition callbacks, state-dependent behavior, coordination)
     - 30%
   * - Integration (GP1 + GP2 features functional, RViz2 visualization, CLI management)
     - 20%
   * - Code Quality (naming conventions, uniform initialization, ``'\n'`` usage, structure)
     - 10%
   * - Documentation and Demo (README, video, frame tree diagram)
     - 10%

----------
Final Note
----------

.. admonition:: Congratulations
   :class: tip

   This assignment is the culmination of the entire ENPM702 course -- from basic C++ variables and control flow in RWA1 to a full ROS 2 robotic system with coordinate frames and lifecycle management. Your final submission should demonstrate mastery of modern C++ programming, object-oriented design, and the ROS 2 framework for building real robotic systems.
