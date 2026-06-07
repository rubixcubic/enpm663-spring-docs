====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 11: ROS 2 Configuration and
Orchestration. Topics include parameters (declaring, getting, setting,
callbacks), launch files (Python launch files, launch arguments, remappings,
namespaces), executors (single-threaded, multi-threaded, callback groups),
YAML configuration files, and ROS 2 CLI tools for parameters.

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

   What must a ROS 2 node do before accessing a parameter's value?

   A. Subscribe to the ``/parameter_events`` topic.

   B. Declare the parameter using ``declare_parameter()``.

   C. Call ``rclcpp::init()`` with the parameter name.

   D. Load a YAML configuration file.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Declare the parameter using ``declare_parameter()``.

   In ROS 2, every parameter must be declared before it can be used. If a
   node tries to get an undeclared parameter, an
   ``rclcpp::exceptions::ParameterNotDeclaredException`` is thrown.


.. admonition:: Question 2
   :class: hint

   Which command correctly sets a parameter when launching a node from the
   command line?

   A. ``ros2 run my_pkg my_node -p max_speed 2.5``

   B. ``ros2 run my_pkg my_node --ros-args -p max_speed:=2.5``

   C. ``ros2 run my_pkg my_node --param max_speed=2.5``

   D. ``ros2 run my_pkg my_node max_speed:=2.5``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``ros2 run my_pkg my_node --ros-args -p max_speed:=2.5``

   The ``--ros-args`` flag tells the ROS 2 argument parser that the
   following arguments are ROS-specific. The ``-p`` flag sets a parameter
   using the ``name:=value`` syntax.


.. admonition:: Question 3
   :class: hint

   In a Python launch file, which class is used to define a launch argument
   that can be overridden from the command line?

   A. ``LaunchConfiguration``

   B. ``Node``

   C. ``DeclareLaunchArgument``

   D. ``SetParameter``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``DeclareLaunchArgument``

   ``DeclareLaunchArgument`` defines a launch-time argument with a name,
   default value, and description. ``LaunchConfiguration`` is then used
   to *read* the value of a declared argument inside the launch file.


.. admonition:: Question 4
   :class: hint

   What is the correct YAML structure for setting a parameter ``max_speed``
   to ``2.5`` on a node named ``robot_node``?

   A.

   .. code-block:: yaml

      max_speed: 2.5

   B.

   .. code-block:: yaml

      robot_node:
        max_speed: 2.5

   C.

   .. code-block:: yaml

      robot_node:
        ros__parameters:
          max_speed: 2.5

   D.

   .. code-block:: yaml

      parameters:
        robot_node:
          max_speed: 2.5

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**

   .. code-block:: yaml

      robot_node:
        ros__parameters:
          max_speed: 2.5

   ROS 2 YAML parameter files require the node name as a top-level key,
   followed by the special ``ros__parameters`` key (with double underscores),
   under which the actual parameters are listed.


.. admonition:: Question 5
   :class: hint

   What does the ``add_on_set_parameters_callback`` method return?

   A. A ``bool`` indicating whether the callback was registered.

   B. A ``SharedPtr`` to a callback handle that must be stored as a member
      variable.

   C. A ``SetParametersResult`` message.

   D. Nothing (``void``).

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A ``SharedPtr`` to a callback handle that must be stored as a
   member variable.

   The returned handle must remain in scope for the callback to stay active.
   If the handle goes out of scope (e.g., stored in a local variable), the
   callback is automatically unregistered.


.. admonition:: Question 6
   :class: hint

   What is the default executor used by ``rclcpp::spin()``?

   A. ``MultiThreadedExecutor``

   B. ``SingleThreadedExecutor``

   C. ``StaticSingleThreadedExecutor``

   D. ``EventsExecutor``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``SingleThreadedExecutor``

   When you call ``rclcpp::spin(node)``, ROS 2 creates a
   ``SingleThreadedExecutor`` behind the scenes and spins the node on a
   single thread. All callbacks are processed sequentially.


.. admonition:: Question 7
   :class: hint

   In a ``MultiThreadedExecutor``, what is the behavior of a **mutually
   exclusive** callback group?

   A. All callbacks in the group run concurrently on separate threads.

   B. Only one callback in the group can execute at a time; others wait.

   C. Callbacks are distributed across executors in a round-robin fashion.

   D. Callbacks are queued and executed in FIFO order on a dedicated thread.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Only one callback in the group can execute at a time; others
   wait.

   A mutually exclusive callback group ensures that at most one callback
   from the group runs at any given time. This provides serialized access
   without requiring explicit mutexes, making it safe for callbacks that
   share state.


.. admonition:: Question 8
   :class: hint

   Which of the following correctly passes a YAML file as parameters in a
   Python launch file?

   A. ``parameters={'file': 'params.yaml'}``

   B. ``parameters=['/path/to/params.yaml']``

   C. ``parameters=LaunchConfiguration('params.yaml')``

   D. ``parameters=yaml.load('params.yaml')``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``parameters=['/path/to/params.yaml']``

   The ``parameters`` argument to the ``Node`` action accepts a list. Each
   element can be either a dictionary of parameter key-value pairs or a
   string path to a YAML file. ROS 2 automatically parses the YAML file
   and applies the parameters to the node.


.. admonition:: Question 9
   :class: hint

   You want to remap a node's subscription topic from ``/input`` to
   ``/sensor/data`` in a launch file. Which argument do you use?

   A. ``arguments=['--remap', '/input:=/sensor/data']``

   B. ``parameters=[{'input_topic': '/sensor/data'}]``

   C. ``remappings=[('/input', '/sensor/data')]``

   D. ``namespace='sensor'``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``remappings=[('/input', '/sensor/data')]``

   The ``remappings`` argument accepts a list of ``(from, to)`` tuples that
   redirect topic and service names. This is applied at the ROS 2 middleware
   level, so the node code does not need to change.


.. admonition:: Question 10
   :class: hint

   Which ROS 2 CLI command dumps all of a running node's parameters in YAML
   format?

   A. ``ros2 param list /my_node``

   B. ``ros2 param get /my_node --all``

   C. ``ros2 param dump /my_node``

   D. ``ros2 param describe /my_node``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``ros2 param dump /my_node``

   The ``ros2 param dump`` command outputs all of a node's current parameter
   names and values in YAML format. This can be redirected to a file to
   capture the running configuration.


----


True / False (Questions 11--15)
====================================================

.. admonition:: Question 11
   :class: hint

   **True or False:** ROS 2 parameters are globally shared between all nodes
   in the system.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   ROS 2 parameters are **node-specific**. Each node declares, owns, and
   manages its own parameters. Unlike ROS 1's parameter server, there is no
   global parameter store. To read another node's parameters, you must use
   a parameter client or the CLI tools.


.. admonition:: Question 12
   :class: hint

   **True or False:** A ``MultiThreadedExecutor`` can execute callbacks from
   the same mutually exclusive callback group concurrently.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   A mutually exclusive callback group guarantees that only one callback in
   the group executes at a time, even when using a ``MultiThreadedExecutor``.
   Concurrent execution is only possible for callbacks in a **reentrant**
   callback group or in separate mutually exclusive groups.


.. admonition:: Question 13
   :class: hint

   **True or False:** Python launch files must define a function called
   ``generate_launch_description()`` that returns a ``LaunchDescription``
   object.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   The ROS 2 launch system looks for the ``generate_launch_description()``
   function as the entry point of a Python launch file. This function must
   return a ``LaunchDescription`` containing the actions to execute.


.. admonition:: Question 14
   :class: hint

   **True or False:** The ``ros2 param set`` command can change a parameter
   on a running node even if the node does not have a parameter callback.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   Parameter callbacks are optional. If no callback is registered, the
   parameter value is simply updated. The callback is only needed if you want
   to validate, reject, or react to parameter changes.


.. admonition:: Question 15
   :class: hint

   **True or False:** In a ROS 2 YAML parameter file, the ``/**`` wildcard
   key applies parameters to all nodes that load that file.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   The ``/**`` wildcard namespace matches all nodes. Parameters defined
   under ``/**`` are applied to every node that loads the YAML file.
   Node-specific entries (e.g., ``my_node:``) override the wildcard values
   for that particular node.
