References
==========


.. dropdown:: Lecture 10
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM702 -- L10: ROS 2 Foundations**

        Covers the fundamentals of ROS 2: architecture (nodes, topics,
        messages, computation graph), workspace and package creation with
        ``colcon``, writing publisher and subscriber nodes in C++ using
        ``rclcpp::Node`` inheritance, standard message types, custom
        interface definitions (``.msg`` files), and essential CLI tools
        (``ros2 run``, ``ros2 topic list``, ``ros2 topic echo``,
        ``ros2 interface show``).

        **Before next class**: complete the C++ exercises on publishers,
        subscribers, and custom interfaces, and the quiz. Ensure you can
        build and run a publisher/subscriber pair in your workspace.


.. dropdown:: ROS 2 Official Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: ROS 2 Tutorials
            :link: https://docs.ros.org/en/jazzy/Tutorials.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy -- Tutorials**

            Official ROS 2 tutorials covering installation, workspace
            setup, package creation, nodes, topics, services, actions,
            and more.

            +++

            - Beginner: CLI Tools
            - Beginner: Client Libraries
            - Intermediate and Advanced topics

        .. grid-item-card:: rclcpp API Reference
            :link: https://docs.ros.org/en/jazzy/p/rclcpp/
            :class-card: sd-border-secondary

            **rclcpp -- ROS 2 C++ Client Library**

            API reference for the ``rclcpp`` library, including
            ``Node``, ``Publisher``, ``Subscription``, ``Timer``,
            ``Service``, and other core classes.

            +++

            - ``rclcpp::Node`` class
            - Publisher and Subscription creation
            - Timer and callback management
            - QoS configuration

        .. grid-item-card:: Common Message Types
            :link: https://docs.ros.org/en/jazzy/p/std_msgs/
            :class-card: sd-border-secondary

            **std_msgs -- Standard Messages**

            Reference for standard ROS 2 message types including
            ``String``, ``Int32``, ``Float64``, ``Bool``, ``Header``,
            and other primitive wrappers.

            +++

            - ``std_msgs/msg/String``
            - ``std_msgs/msg/Int32``
            - ``geometry_msgs/msg/Twist``
            - ``sensor_msgs/msg/LaserScan``

        .. grid-item-card:: Custom Interfaces
            :link: https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html
            :class-card: sd-border-secondary

            **Creating Custom msg and srv Files**

            Official tutorial for defining custom message and service
            types, building interface packages with
            ``rosidl_default_generators``, and using custom interfaces
            in C++ and Python nodes.

            +++

            - ``.msg`` file syntax
            - ``rosidl_generate_interfaces`` CMake macro
            - ``package.xml`` dependencies
            - Using generated headers in C++


.. dropdown:: colcon Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: colcon User Documentation
            :link: https://colcon.readthedocs.io/en/released/user/quick-start.html
            :class-card: sd-border-secondary

            **colcon -- Quick Start**

            Guide to using ``colcon`` for building ROS 2 workspaces,
            including ``colcon build``, ``--packages-select``,
            ``--packages-up-to``, ``--symlink-install``, and sourcing
            the install space.

            +++

            - ``colcon build`` usage
            - Package selection flags
            - Sourcing the workspace overlay
            - Build configuration options

        .. grid-item-card:: ament_cmake Documentation
            :link: https://docs.ros.org/en/jazzy/How-To-Guides/Ament-CMake-Documentation.html
            :class-card: sd-border-secondary

            **ament_cmake -- Build System**

            Reference for the ``ament_cmake`` build system used in
            ROS 2 C++ packages, covering ``CMakeLists.txt`` structure,
            ``find_package``, ``ament_target_dependencies``, and
            executable installation.

            +++

            - ``CMakeLists.txt`` structure
            - ``find_package`` and dependencies
            - ``ament_target_dependencies``
            - Installing executables and libraries
