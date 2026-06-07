References
==========


.. dropdown:: Lecture 12
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM702 -- L12: ROS 2 Communication Patterns**

        Covers the three core ROS 2 communication patterns: topics
        (publish-subscribe), services (request-response), and actions
        (goal-feedback-result). The lecture explains when to use each
        pattern, how to define custom ``.srv`` and ``.action``
        interfaces, and how to implement service servers/clients and
        action servers/clients in C++ using ``rclcpp`` and
        ``rclcpp_action``. CLI tools for inspecting and calling
        services and actions are also covered.

        **Before next class**: complete the C++ exercises on services
        and actions, and the quiz. Prepare your workspace with the
        ``robot_interfaces`` package built and ready.


.. dropdown:: ROS 2 Documentation -- Services
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Understanding Services
            :link: https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy -- Understanding Services**

            Beginner tutorial introducing the service concept, CLI
            tools for listing, calling, and inspecting services.

            +++

            - ``ros2 service list``
            - ``ros2 service type``
            - ``ros2 service call``

        .. grid-item-card:: Writing a Service and Client (C++)
            :link: https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Service-And-Client.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy -- Writing a Simple Service and Client (C++)**

            Step-by-step tutorial for implementing a service server and
            client using ``rclcpp``.

            +++

            - ``create_service`` API
            - ``create_client`` and ``async_send_request``
            - Request/response callback patterns

        .. grid-item-card:: Custom Interfaces
            :link: https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy -- Custom Interfaces**

            Tutorial on creating custom ``.msg``, ``.srv``, and
            ``.action`` files in a dedicated interface package.

            +++

            - ``rosidl_generate_interfaces``
            - Package.xml dependencies
            - Building and verifying interfaces


.. dropdown:: ROS 2 Documentation -- Actions
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Understanding Actions
            :link: https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy -- Understanding Actions**

            Beginner tutorial covering the action concept, the
            goal-feedback-result lifecycle, and CLI tools for
            interacting with actions.

            +++

            - ``ros2 action list``
            - ``ros2 action info``
            - ``ros2 action send_goal --feedback``

        .. grid-item-card:: Writing an Action Server and Client (C++)
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Writing-an-Action-Server-Client/Cpp.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy -- Writing an Action Server and Client (C++)**

            Intermediate tutorial for implementing an action server
            (with goal handling, feedback, and cancellation) and an
            action client using ``rclcpp_action``.

            +++

            - ``rclcpp_action::create_server``
            - ``rclcpp_action::create_client``
            - Goal, cancel, and accepted callbacks
            - ``SendGoalOptions`` and result handling

        .. grid-item-card:: ROS 2 Design -- Actions
            :link: https://design.ros2.org/articles/actions.html
            :class-card: sd-border-secondary

            **ROS 2 Design -- Actions**

            Design article explaining the architecture of actions,
            their internal implementation using topics and services,
            and the rationale behind the goal-feedback-result pattern.

            +++

            - Internal topic/service structure
            - Goal state machine
            - Preemption and cancellation semantics

        .. grid-item-card:: ``rclcpp_action`` API Reference
            :link: https://docs.ros.org/en/jazzy/p/rclcpp_action/
            :class-card: sd-border-secondary

            **ROS 2 Jazzy -- rclcpp_action API**

            API documentation for the ``rclcpp_action`` library
            including server, client, and goal handle classes.

            +++

            - ``Server`` and ``Client`` class templates
            - ``ServerGoalHandle`` and ``ClientGoalHandle``
            - ``GoalResponse`` and ``CancelResponse`` enums
