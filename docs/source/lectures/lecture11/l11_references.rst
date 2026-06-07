References
==========


.. dropdown:: Lecture 11
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM702 -- L11: ROS 2 Configuration and Orchestration**

        Covers ROS 2 parameters (declaring, getting, setting, parameter
        types, parameter callbacks, command-line overrides), launch files
        (Python launch files, ``Node`` action, passing parameters, remapping
        topics, launch arguments with ``DeclareLaunchArgument`` and
        ``LaunchConfiguration``, including other launch files, grouping with
        namespaces), executors (single-threaded, multi-threaded, callback
        groups -- mutually exclusive and reentrant), YAML configuration files
        (structure, loading from launch files and CLI), composable nodes, and
        ROS 2 CLI tools for parameter introspection (``list``, ``get``,
        ``set``, ``describe``, ``dump``).

        **Before next class**: complete the C++ exercises on parameters,
        launch files, and executors, and take the quiz.


.. dropdown:: ROS 2 Documentation -- Parameters
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Using Parameters in a Class (C++)
            :link: https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-CPP.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy Tutorial**

            Step-by-step tutorial for declaring and using parameters in a
            C++ ROS 2 node, including parameter declaration, retrieval,
            and command-line overrides.

            +++

            - ``declare_parameter()`` and ``get_parameter()``
            - Running with ``--ros-args -p``
            - Parameter types and defaults

        .. grid-item-card:: Monitoring Parameter Changes (C++)
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Monitoring-For-Parameter-Changes-CPP.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy Tutorial**

            Tutorial for setting up parameter change callbacks to
            dynamically respond when parameters are modified at runtime.

            +++

            - ``add_on_set_parameters_callback``
            - ``SetParametersResult``
            - Runtime parameter validation


.. dropdown:: ROS 2 Documentation -- Launch Files
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Creating a Launch File
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy Tutorial**

            Introduction to Python launch files, the
            ``generate_launch_description()`` function, and starting
            multiple nodes from a single command.

            +++

            - ``LaunchDescription`` and ``Node`` action
            - ``output='screen'``
            - ``ros2 launch`` command

        .. grid-item-card:: Using Substitutions in Launch Files
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Using-Substitutions.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy Tutorial**

            Covers launch arguments, ``DeclareLaunchArgument``,
            ``LaunchConfiguration``, and other substitution types for
            creating flexible, reusable launch files.

            +++

            - ``DeclareLaunchArgument``
            - ``LaunchConfiguration``
            - Command-line argument overrides
            - Composing launch files with ``IncludeLaunchDescription``

        .. grid-item-card:: Large Projects with Launch Files
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Using-ROS2-Launch-For-Large-Projects.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy Tutorial**

            Best practices for organizing launch files in large projects
            including namespacing, grouping, parameter files, and
            modular composition.

            +++

            - ``GroupAction`` and ``PushRosNamespace``
            - Including other launch files
            - Passing launch arguments between files


.. dropdown:: ROS 2 Documentation -- Executors
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Executors
            :link: https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Executors.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy Concepts**

            Conceptual overview of executors in ROS 2, including
            single-threaded and multi-threaded executors, callback
            groups, and their role in scheduling callbacks.

            +++

            - ``SingleThreadedExecutor``
            - ``MultiThreadedExecutor``
            - Callback group types
            - Choosing the right executor

        .. grid-item-card:: Composing Multiple Nodes in a Single Process
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Composition.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy Tutorial**

            Tutorial on composable nodes (components) that can be loaded
            into a single process for reduced overhead and intra-process
            communication.

            +++

            - Component nodes vs. standalone executables
            - Component containers
            - Intra-process communication
            - Runtime composition with ``ros2 component``
