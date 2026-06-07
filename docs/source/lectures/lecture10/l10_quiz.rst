====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 10: ROS 2 Foundations.
Topics include ROS 2 architecture, nodes, topics, publishers,
subscribers, message types, QoS, CLI tools, package creation,
``colcon`` build, and custom interfaces.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1--10)
====================================================

.. admonition:: Question 1
   :class: hint

   What is the middleware layer used by ROS 2 for communication?

   A. TCPROS

   B. ZeroMQ

   C. DDS (Data Distribution Service)

   D. gRPC

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- DDS (Data Distribution Service)

   ROS 2 uses DDS as its middleware layer for publish-subscribe
   communication. DDS provides features like configurable QoS,
   security, and real-time support. The default implementation in
   ROS 2 Jazzy is Fast DDS by eProsima.


.. admonition:: Question 2
   :class: hint

   Which command creates a new ROS 2 C++ package named ``my_pkg``
   with a dependency on ``rclcpp``?

   A. ``ros2 create pkg my_pkg --type cmake --dep rclcpp``

   B. ``ros2 pkg create --build-type ament_cmake my_pkg --dependencies rclcpp``

   C. ``colcon create my_pkg --depends rclcpp``

   D. ``catkin_create_pkg my_pkg rclcpp``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``ros2 pkg create --build-type ament_cmake my_pkg --dependencies rclcpp``

   The ``ros2 pkg create`` command is the standard way to create
   packages. ``--build-type ament_cmake`` specifies a C++ package,
   and ``--dependencies`` lists the required packages.


.. admonition:: Question 3
   :class: hint

   In the following code, what does the argument ``10`` represent?

   .. code-block:: cpp

      publisher_ = this->create_publisher<std_msgs::msg::String>("chatter", 10);

   A. The maximum message size in bytes

   B. The timer period in milliseconds

   C. The QoS history depth (queue size)

   D. The number of subscribers allowed

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- The QoS history depth (queue size)

   The second argument to ``create_publisher`` is the QoS depth,
   which specifies how many messages to queue if the subscriber is
   not consuming them fast enough. With ``KEEP_LAST`` history (the
   default), the system keeps the last 10 messages.


.. admonition:: Question 4
   :class: hint

   Which function keeps a ROS 2 node alive and processes callbacks?

   A. ``rclcpp::loop(node)``

   B. ``rclcpp::run(node)``

   C. ``rclcpp::spin(node)``

   D. ``rclcpp::execute(node)``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``rclcpp::spin(node)``

   ``rclcpp::spin()`` blocks and processes incoming callbacks (timer
   callbacks, subscription callbacks, etc.) until the node is shut
   down or the context is cancelled.


.. admonition:: Question 5
   :class: hint

   What is the purpose of ``std::placeholders::_1`` when creating a
   subscription with ``std::bind``?

   A. It specifies the topic name

   B. It is a placeholder for the first argument of the callback (the incoming message)

   C. It sets the QoS depth to 1

   D. It binds the node name to the callback

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It is a placeholder for the first argument of the callback
   (the incoming message)

   When using ``std::bind`` to bind a member function,
   ``std::placeholders::_1`` reserves a slot for the first argument
   that will be provided at call time -- in this case, the received
   message.


.. admonition:: Question 6
   :class: hint

   Where should custom ``.msg`` files be placed in a ROS 2 package?

   A. In the ``src/`` directory

   B. In the ``include/`` directory

   C. In a ``msg/`` directory within the interface package

   D. In the ``config/`` directory

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- In a ``msg/`` directory within the interface package

   Custom message definitions are placed in a ``msg/`` directory
   inside a dedicated interface package. The
   ``rosidl_generate_interfaces`` CMake macro generates the C++
   headers from these ``.msg`` files.


.. admonition:: Question 7
   :class: hint

   Which command shows all currently active topics and their message
   types?

   A. ``ros2 topic list -t``

   B. ``ros2 topic info --all``

   C. ``ros2 topic show``

   D. ``ros2 msg list``

.. dropdown:: Answer
   :class-container: sd-border-success

   **A** -- ``ros2 topic list -t``

   The ``-t`` flag adds the message type next to each topic name.
   Without ``-t``, only topic names are listed.


.. admonition:: Question 8
   :class: hint

   What is the correct way to source a ROS 2 workspace overlay after
   building?

   A. ``source ~/ros2_ws/build/setup.bash``

   B. ``source ~/ros2_ws/install/setup.bash``

   C. ``source ~/ros2_ws/src/setup.bash``

   D. ``source ~/ros2_ws/devel/setup.bash``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``source ~/ros2_ws/install/setup.bash``

   The ``install/`` directory contains the built artifacts and the
   ``setup.bash`` script that adds them to your environment. The
   ``devel/`` directory is a ROS 1 concept and does not exist in
   ROS 2.


.. admonition:: Question 9
   :class: hint

   Which CMake macro is used to generate C++ code from custom ``.msg``
   files?

   A. ``ament_generate_messages()``

   B. ``rosidl_generate_interfaces()``

   C. ``add_message_files()``

   D. ``generate_messages()``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``rosidl_generate_interfaces()``

   ``rosidl_generate_interfaces()`` is the ROS 2 CMake macro that
   invokes the ``rosidl`` toolchain to generate C++, Python, and
   other language bindings from ``.msg``, ``.srv``, and ``.action``
   files. Options C and D are ROS 1 macros.


.. admonition:: Question 10
   :class: hint

   What is the key advantage of ROS 2 over ROS 1 regarding the
   ``roscore`` process?

   A. ROS 2 requires ``roscore`` but it starts automatically

   B. ROS 2 replaces ``roscore`` with ``ros2core``

   C. ROS 2 does not require a central master -- nodes discover each
      other through DDS

   D. ROS 2 uses multiple ``roscore`` instances for redundancy

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ROS 2 does not require a central master -- nodes discover
   each other through DDS

   ROS 2 uses DDS discovery, which is fully distributed. There is no
   single point of failure like the ROS 1 master (``roscore``). Nodes
   automatically discover each other on the network.


----


True or False (Questions 11--15)
====================================================

.. admonition:: Question 11
   :class: hint

   **True or False:** A ROS 2 topic can have multiple publishers and
   multiple subscribers at the same time.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Topics support many-to-many communication. Any number of nodes can
   publish to a topic, and any number of nodes can subscribe to it.


.. admonition:: Question 12
   :class: hint

   **True or False:** In ROS 2, you must call ``rclcpp::init()``
   before creating any nodes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   ``rclcpp::init()`` initializes the ROS 2 runtime context. It must
   be called before creating nodes, publishers, subscribers, or any
   other ROS 2 entities.


.. admonition:: Question 13
   :class: hint

   **True or False:** Custom message types in ROS 2 can only contain
   primitive types (``int32``, ``float64``, ``string``, etc.) and
   cannot include other message types as fields.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Custom messages can contain other message types as fields. For
   example, a custom message can include a ``geometry_msgs/msg/Point``
   field or another custom message type. This allows building complex,
   nested data structures.


.. admonition:: Question 14
   :class: hint

   **True or False:** The command ``colcon build --packages-select
   my_package`` builds only the specified package and its
   dependencies.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``--packages-select`` builds **only** the specified package(s), not
   their dependencies. To build a package along with its dependencies,
   use ``--packages-up-to my_package`` instead.


.. admonition:: Question 15
   :class: hint

   **True or False:** The ``RCLCPP_INFO`` macro in ROS 2 supports
   ``printf``-style format strings.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   ``RCLCPP_INFO`` and other ROS 2 logging macros accept
   ``printf``-style format strings. For example:
   ``RCLCPP_INFO(this->get_logger(), "Count: %d\n", count);``
