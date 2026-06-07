References
==========


.. dropdown:: Lecture 13
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM702 -- L13: ROS 2 Advanced Topics**

        Covers coordinate frame management with TF2 and managed lifecycle
        nodes in ROS 2. TF2 topics include the frame tree concept, static
        and dynamic transform broadcasting, transform listening with
        ``lookupTransform()``, the ``TransformStamped`` message, and
        debugging tools (``view_frames``, ``tf2_echo``, RViz2). Lifecycle
        node topics include the state machine (Unconfigured, Inactive,
        Active, Finalized), transition callbacks (``on_configure``,
        ``on_activate``, ``on_deactivate``, ``on_cleanup``,
        ``on_shutdown``), ``CallbackReturn`` values, ``LifecyclePublisher``
        behavior, and managing lifecycle nodes via CLI and programmatic
        interfaces.

        **This is the final lecture.** Complete the C++ exercises on TF2
        and lifecycle nodes, and take the quiz before starting GP3.


.. dropdown:: ROS 2 TF2 Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: TF2 Tutorials
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Tf2-Main.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy -- TF2 Tutorials**

            Official ROS 2 tutorials for the TF2 library, covering
            static and dynamic broadcasters, transform listeners,
            frame debugging, and time travel.

            +++

            - Introduction to TF2
            - Writing a static broadcaster (C++)
            - Writing a broadcaster (C++)
            - Writing a listener (C++)
            - Adding a frame
            - Using time with TF2

        .. grid-item-card:: TF2 API Reference
            :link: https://docs.ros.org/en/jazzy/p/tf2_ros/
            :class-card: sd-border-secondary

            **tf2_ros API Reference**

            API documentation for the ``tf2_ros`` package including
            ``TransformBroadcaster``, ``StaticTransformBroadcaster``,
            ``TransformListener``, and ``Buffer``.

            +++

            - ``tf2_ros::TransformBroadcaster``
            - ``tf2_ros::StaticTransformBroadcaster``
            - ``tf2_ros::TransformListener``
            - ``tf2_ros::Buffer``

        .. grid-item-card:: geometry_msgs
            :link: https://docs.ros.org/en/jazzy/p/geometry_msgs/
            :class-card: sd-border-secondary

            **geometry_msgs Message Reference**

            Documentation for geometry message types used with TF2,
            including ``TransformStamped``, ``Transform``, ``Vector3``,
            and ``Quaternion``.

            +++

            - ``TransformStamped``
            - ``Transform``
            - ``Vector3``
            - ``Quaternion``
            - ``Pose`` and ``PoseStamped``

        .. grid-item-card:: REP 105 -- Coordinate Frames
            :link: https://www.ros.org/reps/rep-0105.html
            :class-card: sd-border-secondary

            **REP 105 -- Coordinate Frames for Mobile Platforms**

            The ROS Enhancement Proposal that defines standard coordinate
            frame conventions for mobile robots, including ``map``,
            ``odom``, ``base_link``, and ``base_footprint``.

            +++

            - Standard frame names
            - Frame relationships
            - Conventions for mobile robots


.. dropdown:: ROS 2 Lifecycle Node Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Managed Nodes Tutorial
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Managing-Nodes-Lifecycle.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy -- Managing Nodes with Lifecycle**

            Official tutorial on lifecycle (managed) nodes, covering the
            state machine, transition callbacks, and CLI management.

            +++

            - Lifecycle state machine overview
            - Implementing transition callbacks
            - CLI commands for lifecycle management
            - Coordinated system bringup

        .. grid-item-card:: rclcpp_lifecycle API
            :link: https://docs.ros.org/en/jazzy/p/rclcpp_lifecycle/
            :class-card: sd-border-secondary

            **rclcpp_lifecycle API Reference**

            API documentation for the ``rclcpp_lifecycle`` package
            including ``LifecycleNode``, ``LifecyclePublisher``, and
            transition callback types.

            +++

            - ``rclcpp_lifecycle::LifecycleNode``
            - ``rclcpp_lifecycle::LifecyclePublisher``
            - ``CallbackReturn`` enum
            - State and transition types

        .. grid-item-card:: lifecycle_msgs
            :link: https://docs.ros.org/en/jazzy/p/lifecycle_msgs/
            :class-card: sd-border-secondary

            **lifecycle_msgs Message/Service Reference**

            Documentation for lifecycle message and service types
            including ``State``, ``Transition``, ``ChangeState``, and
            ``GetState``.

            +++

            - ``lifecycle_msgs::msg::State``
            - ``lifecycle_msgs::msg::Transition``
            - ``lifecycle_msgs::srv::ChangeState``
            - ``lifecycle_msgs::srv::GetState``

        .. grid-item-card:: Lifecycle Node Design Document
            :link: https://design.ros2.org/articles/node_lifecycle.html
            :class-card: sd-border-secondary

            **ROS 2 Design -- Managed Nodes**

            The original design document for the ROS 2 lifecycle node
            concept, explaining the motivation, state machine design,
            and intended usage patterns.

            +++

            - Design rationale
            - State machine specification
            - Transition callbacks
            - Error handling model
