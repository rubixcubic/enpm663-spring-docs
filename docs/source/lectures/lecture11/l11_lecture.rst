====================================================
Lecture
====================================================


ROS 2 Configuration and Orchestration
====================================================

This lecture covers the tools for configuring and orchestrating ROS 2 systems:

- Parameters: node-specific configuration values
- Launch files: starting and configuring multi-node systems
- Executors: controlling callback dispatch and concurrency
- YAML configuration files: externalizing parameters
- ROS 2 CLI tools for parameter introspection


----


Parameters
====================================================

Parameters are node-specific configuration values that allow you to change a
node's behavior without modifying and recompiling code. They are ideal for
values that may vary between deployments -- such as sensor thresholds, timer
periods, topic names, or robot dimensions.

.. admonition:: Key Concept
   :class: note

   Parameters in ROS 2 are associated with individual nodes, not shared
   globally. Each node declares, owns, and manages its own parameters.


Declaring Parameters
----------------------------------------------------

A node must **declare** a parameter before using it. Declaring a parameter
registers its name, type, and an optional default value with the node.

.. code-block:: cpp

   // In your node's constructor
   this->declare_parameter<std::string>("robot_name", "default_robot");
   this->declare_parameter<double>("max_speed", 1.5);
   this->declare_parameter<int>("num_sensors", 4);
   this->declare_parameter<bool>("verbose", false);

If a parameter is not declared before it is accessed, ROS 2 throws an
``rclcpp::exceptions::ParameterNotDeclaredException``.


Getting Parameters
----------------------------------------------------

After declaring a parameter, retrieve its current value with
``get_parameter()``.

.. code-block:: cpp

   // Retrieve individual parameters
   std::string robot_name = this->get_parameter("robot_name").as_string();
   double max_speed = this->get_parameter("max_speed").as_double();
   int num_sensors = this->get_parameter("num_sensors").as_integer();
   bool verbose = this->get_parameter("verbose").as_bool();

You can also retrieve the value directly during declaration:

.. code-block:: cpp

   auto robot_name = this->declare_parameter<std::string>("robot_name", "default_robot");


Parameter Types
----------------------------------------------------

ROS 2 supports the following parameter types:

.. list-table::
   :widths: 30 30 40
   :header-rows: 1

   * - Type
     - C++ Type
     - Accessor Method
   * - Boolean
     - ``bool``
     - ``as_bool()``
   * - Integer
     - ``int64_t``
     - ``as_integer()``
   * - Double
     - ``double``
     - ``as_double()``
   * - String
     - ``std::string``
     - ``as_string()``
   * - Byte Array
     - ``std::vector<uint8_t>``
     - ``as_byte_array()``
   * - Bool Array
     - ``std::vector<bool>``
     - ``as_bool_array()``
   * - Integer Array
     - ``std::vector<int64_t>``
     - ``as_integer_array()``
   * - Double Array
     - ``std::vector<double>``
     - ``as_double_array()``
   * - String Array
     - ``std::vector<std::string>``
     - ``as_string_array()``


Parameter Callbacks
----------------------------------------------------

You can register a callback that is invoked whenever a parameter is set or
changed. This is useful for validating new values or reacting to
configuration changes at runtime.

.. code-block:: cpp

   // In your node's constructor
   param_callback_handle_ = this->add_on_set_parameters_callback(
       std::bind(&MyNode::param_callback, this, std::placeholders::_1));

The callback function receives a vector of parameters that are about to be
set and returns a ``SetParametersResult`` indicating whether the change is
accepted or rejected.

.. code-block:: cpp

   rcl_interfaces::msg::SetParametersResult MyNode::param_callback(
       const std::vector<rclcpp::Parameter>& parameters) {
       rcl_interfaces::msg::SetParametersResult result;
       result.successful = true;

       for (const auto& param : parameters) {
           if (param.get_name() == "max_speed") {
               double value{param.as_double()};
               if (value < 0.0 || value > 10.0) {
                   result.successful = false;
                   result.reason = "max_speed must be between 0.0 and 10.0";
                   return result;
               }
               RCLCPP_INFO(this->get_logger(), "max_speed updated to: %f", value);
           }
       }
       return result;
   }

.. admonition:: Important
   :class: warning

   The member variable that stores the callback handle
   (``param_callback_handle_``) must remain in scope for the callback to
   stay active. Declare it as a class member of type
   ``rclcpp::node_interfaces::OnSetParametersCallbackHandle::SharedPtr``.


Setting Parameters from the Command Line
----------------------------------------------------

You can set parameter values when launching a node from the command line
using the ``--ros-args -p`` syntax:

.. code-block:: bash

   ros2 run my_package my_node --ros-args -p robot_name:=atlas -p max_speed:=2.5

Multiple parameters can be set by repeating the ``-p`` flag.


Complete Node Example with Parameters
----------------------------------------------------

The following example demonstrates a complete node that declares parameters,
retrieves them, and responds to runtime changes.

.. code-block:: cpp

   #include <rclcpp/rclcpp.hpp>
   #include <string>

   class ConfigurableNode : public rclcpp::Node {
    public:
     ConfigurableNode() : Node("configurable_node") {
         // Declare parameters with default values
         this->declare_parameter<std::string>("robot_name", "default_robot");
         this->declare_parameter<double>("max_speed", 1.5);
         this->declare_parameter<int>("update_rate", 10);

         // Retrieve parameter values
         robot_name_ = this->get_parameter("robot_name").as_string();
         max_speed_ = this->get_parameter("max_speed").as_double();
         int update_rate{static_cast<int>(
             this->get_parameter("update_rate").as_integer())};

         RCLCPP_INFO(this->get_logger(), "Robot: %s, Max speed: %.2f, Rate: %d",
                     robot_name_.c_str(), max_speed_, update_rate);

         // Register parameter change callback
         param_callback_handle_ = this->add_on_set_parameters_callback(
             std::bind(&ConfigurableNode::on_parameter_change, this,
                       std::placeholders::_1));

         // Create a timer using the update_rate parameter
         timer_ = this->create_wall_timer(
             std::chrono::milliseconds(1000 / update_rate),
             std::bind(&ConfigurableNode::timer_callback, this));
     }

    private:
     void timer_callback() {
         RCLCPP_INFO(this->get_logger(), "[%s] Moving at max speed: %.2f",
                     robot_name_.c_str(), max_speed_);
     }

     rcl_interfaces::msg::SetParametersResult on_parameter_change(
         const std::vector<rclcpp::Parameter>& parameters) {
         rcl_interfaces::msg::SetParametersResult result;
         result.successful = true;

         for (const auto& param : parameters) {
             if (param.get_name() == "max_speed") {
                 double new_speed{param.as_double()};
                 if (new_speed < 0.0) {
                     result.successful = false;
                     result.reason = "max_speed cannot be negative";
                     return result;
                 }
                 max_speed_ = new_speed;
                 RCLCPP_INFO(this->get_logger(), "max_speed updated to %.2f",
                             max_speed_);
             } else if (param.get_name() == "robot_name") {
                 robot_name_ = param.as_string();
                 RCLCPP_INFO(this->get_logger(), "robot_name updated to %s",
                             robot_name_.c_str());
             }
         }
         return result;
     }

     std::string robot_name_;
     double max_speed_;
     rclcpp::TimerBase::SharedPtr timer_;
     rclcpp::node_interfaces::OnSetParametersCallbackHandle::SharedPtr
         param_callback_handle_;
   };

   int main(int argc, char* argv[]) {
       rclcpp::init(argc, argv);
       rclcpp::spin(std::make_shared<ConfigurableNode>());
       rclcpp::shutdown();
       return 0;
   }


----


Launch Files
====================================================

Launch files automate starting multiple nodes, passing parameters, remapping
topics, and configuring an entire ROS 2 system with a single command. Without
launch files, you would need a separate terminal for every node.


Why Launch Files?
----------------------------------------------------

- Start multiple nodes simultaneously from one command.
- Pass parameters and load YAML configuration files.
- Remap topic and service names.
- Set namespaces to avoid name collisions.
- Organize complex systems into modular, reusable components.
- Define launch arguments to make launch files configurable.


Python Launch Files vs. XML
----------------------------------------------------

ROS 2 supports launch files written in Python, XML, or YAML. **Python launch
files** are the most common because they offer the full power of Python for
conditional logic, loops, and dynamic configuration. This course uses Python
launch files exclusively.

.. admonition:: Convention
   :class: tip

   Python launch files use the ``.launch.py`` extension (e.g.,
   ``robot.launch.py``) and are placed in a ``launch/`` directory inside your
   package.


Creating a Launch File
----------------------------------------------------

A Python launch file is a Python module that defines a ``generate_launch_description()``
function. This function returns a ``LaunchDescription`` object containing the
actions (nodes, arguments, includes) to execute.

.. code-block:: python

   # launch/simple.launch.py
   from launch import LaunchDescription
   from launch_ros.actions import Node

   def generate_launch_description():
       return LaunchDescription([
           Node(
               package='my_package',
               executable='talker_node',
               name='talker',
               output='screen',
           ),
           Node(
               package='my_package',
               executable='listener_node',
               name='listener',
               output='screen',
           ),
       ])

Run this launch file with:

.. code-block:: bash

   ros2 launch my_package simple.launch.py


The ``Node`` Action
----------------------------------------------------

The ``Node`` action is the most common action in a launch file. It starts a
single ROS 2 node and accepts the following key arguments:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Argument
     - Description
   * - ``package``
     - The package containing the executable.
   * - ``executable``
     - The name of the executable to run.
   * - ``name``
     - Override the node name (optional).
   * - ``namespace``
     - Set a namespace for the node (optional).
   * - ``output``
     - Where to send output: ``'screen'``, ``'log'``, or ``'both'``.
   * - ``parameters``
     - A list of parameter dictionaries or YAML file paths.
   * - ``remappings``
     - A list of ``(from, to)`` tuples for topic/service remapping.
   * - ``arguments``
     - Command-line arguments passed to the executable.


Passing Parameters in Launch Files
----------------------------------------------------

Parameters can be passed directly as dictionaries or loaded from a YAML file.

.. code-block:: python

   Node(
       package='my_package',
       executable='configurable_node',
       name='robot_node',
       output='screen',
       parameters=[
           {'robot_name': 'atlas', 'max_speed': 2.5, 'update_rate': 20}
       ],
   )

To load parameters from a YAML file:

.. code-block:: python

   import os
   from ament_index_python.packages import get_package_share_directory

   config_file = os.path.join(
       get_package_share_directory('my_package'), 'config', 'params.yaml'
   )

   Node(
       package='my_package',
       executable='configurable_node',
       name='robot_node',
       output='screen',
       parameters=[config_file],
   )


Remapping Topics
----------------------------------------------------

Use the ``remappings`` argument to redirect topic or service names:

.. code-block:: python

   Node(
       package='my_package',
       executable='listener_node',
       name='listener',
       output='screen',
       remappings=[
           ('/input_topic', '/sensor_data'),
           ('/output_topic', '/processed_data'),
       ],
   )


Launch Arguments
----------------------------------------------------

Launch arguments make launch files reusable by allowing values to be set at
the command line. Use ``DeclareLaunchArgument`` to define an argument and
``LaunchConfiguration`` to use its value.

.. code-block:: python

   from launch import LaunchDescription
   from launch.actions import DeclareLaunchArgument
   from launch.substitutions import LaunchConfiguration
   from launch_ros.actions import Node

   def generate_launch_description():
       # Declare a launch argument with a default value
       robot_name_arg = DeclareLaunchArgument(
           'robot_name',
           default_value='atlas',
           description='Name of the robot'
       )

       speed_arg = DeclareLaunchArgument(
           'max_speed',
           default_value='1.5',
           description='Maximum speed of the robot'
       )

       return LaunchDescription([
           robot_name_arg,
           speed_arg,
           Node(
               package='my_package',
               executable='configurable_node',
               name='robot_node',
               output='screen',
               parameters=[{
                   'robot_name': LaunchConfiguration('robot_name'),
                   'max_speed': LaunchConfiguration('max_speed'),
               }],
           ),
       ])

Override arguments from the command line:

.. code-block:: bash

   ros2 launch my_package robot.launch.py robot_name:=optimus max_speed:=3.0


Including Other Launch Files
----------------------------------------------------

You can compose launch files by including one launch file from another:

.. code-block:: python

   from launch import LaunchDescription
   from launch.actions import IncludeLaunchDescription
   from launch.launch_description_sources import PythonLaunchDescriptionSource
   from ament_index_python.packages import get_package_share_directory
   import os

   def generate_launch_description():
       other_launch = IncludeLaunchDescription(
           PythonLaunchDescriptionSource(
               os.path.join(
                   get_package_share_directory('other_package'),
                   'launch',
                   'other.launch.py'
               )
           ),
           launch_arguments={'robot_name': 'atlas'}.items(),
       )

       return LaunchDescription([other_launch])


Grouping with Namespaces
----------------------------------------------------

Use ``GroupAction`` with ``PushRosNamespace`` to apply a namespace to a set
of nodes:

.. code-block:: python

   from launch import LaunchDescription
   from launch.actions import GroupAction
   from launch_ros.actions import Node, PushRosNamespace

   def generate_launch_description():
       robot_group = GroupAction([
           PushRosNamespace('robot1'),
           Node(
               package='my_package',
               executable='sensor_node',
               name='lidar',
               output='screen',
           ),
           Node(
               package='my_package',
               executable='sensor_node',
               name='camera',
               output='screen',
           ),
       ])

       return LaunchDescription([robot_group])

This creates nodes ``/robot1/lidar`` and ``/robot1/camera``.


Complete Launch File Example
----------------------------------------------------

The following launch file starts a publisher and subscriber with parameters
and remappings:

.. code-block:: python

   # launch/system.launch.py
   import os
   from launch import LaunchDescription
   from launch.actions import DeclareLaunchArgument
   from launch.substitutions import LaunchConfiguration
   from launch_ros.actions import Node
   from ament_index_python.packages import get_package_share_directory

   def generate_launch_description():
       # Declare launch arguments
       rate_arg = DeclareLaunchArgument(
           'publish_rate', default_value='500',
           description='Timer period in milliseconds'
       )

       config_file = os.path.join(
           get_package_share_directory('my_package'), 'config', 'params.yaml'
       )

       publisher_node = Node(
           package='my_package',
           executable='publisher_node',
           name='data_publisher',
           output='screen',
           parameters=[
               config_file,
               {'publish_rate': LaunchConfiguration('publish_rate')},
           ],
       )

       subscriber_node = Node(
           package='my_package',
           executable='subscriber_node',
           name='data_subscriber',
           output='screen',
           parameters=[config_file],
           remappings=[
               ('/raw_data', '/sensor/data'),
           ],
       )

       return LaunchDescription([
           rate_arg,
           publisher_node,
           subscriber_node,
       ])


Installing Launch Files in CMakeLists.txt
----------------------------------------------------

To make launch files available after building, add the following to your
``CMakeLists.txt``:

.. code-block:: cmake

   # Install launch files
   install(DIRECTORY launch/
     DESTINATION share/${PROJECT_NAME}/launch
   )

If you also have a config directory for YAML files:

.. code-block:: cmake

   # Install launch and config files
   install(DIRECTORY launch/ config/
     DESTINATION share/${PROJECT_NAME}/
   )

.. admonition:: Common Pattern
   :class: tip

   A typical package directory structure with launch and config files:

   .. code-block:: text

      my_package/
      ├── CMakeLists.txt
      ├── package.xml
      ├── config/
      │   └── params.yaml
      ├── launch/
      │   └── system.launch.py
      ├── include/
      │   └── my_package/
      └── src/
          ├── publisher_node.cpp
          └── subscriber_node.cpp


----


Executors
====================================================

An **executor** is the mechanism that manages and dispatches callbacks in a
ROS 2 node. Every time a message arrives on a subscription, a timer fires,
or a service request is received, the executor is responsible for calling
the appropriate callback function.


What Is an Executor?
----------------------------------------------------

When you call ``rclcpp::spin(node)``, you are using the default
**single-threaded executor**. The executor enters a loop, waiting for work
(incoming messages, timer events, service requests) and dispatching callbacks
one at a time.

.. code-block:: cpp

   // Default: single-threaded executor
   rclcpp::spin(std::make_shared<MyNode>());

This is equivalent to:

.. code-block:: cpp

   auto node = std::make_shared<MyNode>();
   rclcpp::executors::SingleThreadedExecutor executor;
   executor.add_node(node);
   executor.spin();


Single-Threaded Executor
----------------------------------------------------

The ``SingleThreadedExecutor`` processes all callbacks sequentially on a
single thread. This is the default behavior and is safe because no two
callbacks can run simultaneously.

**Advantages:**

- Simple and safe -- no data races or synchronization needed.
- Predictable execution order.

**Disadvantages:**

- A long-running callback blocks all other callbacks.
- Cannot take advantage of multi-core processors.

.. code-block:: cpp

   #include <rclcpp/rclcpp.hpp>

   int main(int argc, char* argv[]) {
       rclcpp::init(argc, argv);

       auto node = std::make_shared<MyNode>();

       rclcpp::executors::SingleThreadedExecutor executor;
       executor.add_node(node);
       executor.spin();

       rclcpp::shutdown();
       return 0;
   }


Multi-Threaded Executor
----------------------------------------------------

The ``MultiThreadedExecutor`` dispatches callbacks across multiple threads,
allowing concurrent execution. This is useful when you have long-running
callbacks that would otherwise block other processing.

.. code-block:: cpp

   #include <rclcpp/rclcpp.hpp>

   int main(int argc, char* argv[]) {
       rclcpp::init(argc, argv);

       auto node = std::make_shared<MyNode>();

       rclcpp::executors::MultiThreadedExecutor executor;
       executor.add_node(node);
       executor.spin();

       rclcpp::shutdown();
       return 0;
   }

.. admonition:: Important
   :class: warning

   When using a ``MultiThreadedExecutor``, you must consider thread safety.
   Multiple callbacks may access shared data simultaneously, which can lead
   to data races.


Callback Groups
----------------------------------------------------

**Callback groups** control which callbacks can run concurrently when using a
``MultiThreadedExecutor``. ROS 2 provides two types:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Callback Group Type
     - Behavior
   * - **Mutually Exclusive**
     - Only one callback in the group can execute at a time. Other callbacks
       in the group wait until the running callback finishes. This is the
       default behavior.
   * - **Reentrant**
     - Multiple callbacks in the group can execute concurrently on different
       threads. Use this only when callbacks are thread-safe.

.. code-block:: cpp

   class MultiCallbackNode : public rclcpp::Node {
    public:
     MultiCallbackNode() : Node("multi_callback_node") {
         // Create callback groups
         exclusive_group_ = this->create_callback_group(
             rclcpp::CallbackGroupType::MutuallyExclusive);
         reentrant_group_ = this->create_callback_group(
             rclcpp::CallbackGroupType::Reentrant);

         // Subscription options to assign callback groups
         rclcpp::SubscriptionOptions sub_options;
         sub_options.callback_group = reentrant_group_;

         // Timer with mutually exclusive group (default)
         timer_ = this->create_wall_timer(
             std::chrono::seconds(1),
             std::bind(&MultiCallbackNode::timer_callback, this),
             exclusive_group_);

         // Subscription with reentrant group
         subscription_ = this->create_subscription<std_msgs::msg::String>(
             "topic", 10,
             std::bind(&MultiCallbackNode::topic_callback, this,
                       std::placeholders::_1),
             sub_options);
     }

    private:
     void timer_callback() {
         RCLCPP_INFO(this->get_logger(), "Timer callback on thread: %ld",
                     std::this_thread::get_id());
     }

     void topic_callback(const std_msgs::msg::String::SharedPtr msg) {
         RCLCPP_INFO(this->get_logger(), "Received: '%s' on thread: %ld",
                     msg->data.c_str(), std::this_thread::get_id());
     }

     rclcpp::CallbackGroup::SharedPtr exclusive_group_;
     rclcpp::CallbackGroup::SharedPtr reentrant_group_;
     rclcpp::TimerBase::SharedPtr timer_;
     rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
   };


When to Use a Multi-Threaded Executor
----------------------------------------------------

Use a ``MultiThreadedExecutor`` when:

- You have long-running callbacks (e.g., heavy computation, blocking I/O)
  that would delay other callbacks.
- You need to process multiple subscriptions concurrently.
- You have a timer callback that must not be delayed by incoming messages.

Use the default ``SingleThreadedExecutor`` when:

- Your callbacks are short and fast.
- You want simplicity and do not need concurrency.
- You share data between callbacks and do not want to manage mutexes.


Component Nodes and Composition
----------------------------------------------------

ROS 2 supports **composable nodes** (also called "components") that can be
loaded into a single process at runtime. Instead of each node running in its
own process, multiple component nodes share a process, reducing inter-process
communication overhead.

.. admonition:: Brief Overview
   :class: note

   Component composition is an advanced topic. The key idea is:

   - Nodes can be written as **components** (shared libraries) rather than
     standalone executables.
   - A **component container** process loads multiple components into the
     same address space.
   - Intra-process communication between components in the same container
     avoids serialization overhead.

   This course introduces the concept here; you may encounter it in the
   group projects when optimizing performance.


----


YAML Configuration Files
====================================================

For systems with many parameters, it is impractical to set every value in the
launch file or on the command line. YAML configuration files provide a clean,
organized way to externalize all parameter values.


YAML File Structure
----------------------------------------------------

A ROS 2 YAML parameter file uses a specific structure. The top-level keys
are node names (with a ``ros__parameters`` key underneath):

.. code-block:: yaml

   # config/params.yaml
   /**:
     ros__parameters:
       # Parameters shared by all nodes
       use_sim_time: false

   data_publisher:
     ros__parameters:
       robot_name: "atlas"
       max_speed: 2.5
       publish_rate: 500
       sensor_topics:
         - "/lidar/scan"
         - "/camera/image"
         - "/imu/data"

   data_subscriber:
     ros__parameters:
       robot_name: "atlas"
       buffer_size: 100
       verbose: true

.. admonition:: Wildcard Namespace
   :class: tip

   The ``/**`` key applies parameters to **all nodes** loaded from the file.
   Node-specific keys override the wildcard values for that node.


Loading YAML from a Launch File
----------------------------------------------------

Use ``os.path.join`` and ``get_package_share_directory`` to locate the YAML
file, then pass it in the ``parameters`` list:

.. code-block:: python

   import os
   from ament_index_python.packages import get_package_share_directory
   from launch import LaunchDescription
   from launch_ros.actions import Node

   def generate_launch_description():
       config = os.path.join(
           get_package_share_directory('my_package'),
           'config',
           'params.yaml'
       )

       return LaunchDescription([
           Node(
               package='my_package',
               executable='publisher_node',
               name='data_publisher',
               output='screen',
               parameters=[config],
           ),
           Node(
               package='my_package',
               executable='subscriber_node',
               name='data_subscriber',
               output='screen',
               parameters=[config],
           ),
       ])

You can also combine YAML files with inline parameter overrides:

.. code-block:: python

   parameters=[config, {'max_speed': 3.0}],

The inline dictionary values override any matching keys from the YAML file.


Loading YAML from the Command Line
----------------------------------------------------

You can also pass a YAML file directly when running a node:

.. code-block:: bash

   ros2 run my_package publisher_node --ros-args --params-file config/params.yaml


----


ROS 2 CLI for Parameters
====================================================

ROS 2 provides several command-line tools for inspecting and modifying
parameters on running nodes.


``ros2 param list``
----------------------------------------------------

List all parameters declared by a node:

.. code-block:: bash

   ros2 param list /data_publisher

Example output:

.. code-block:: text

   max_speed
   publish_rate
   robot_name
   use_sim_time


``ros2 param get``
----------------------------------------------------

Get the current value of a parameter:

.. code-block:: bash

   ros2 param get /data_publisher max_speed

Example output:

.. code-block:: text

   Double value is: 2.5


``ros2 param set``
----------------------------------------------------

Set a parameter value at runtime:

.. code-block:: bash

   ros2 param set /data_publisher max_speed 3.0

If the node has a parameter callback, it will be invoked to validate the new
value.


``ros2 param describe``
----------------------------------------------------

Get information about a parameter including its type and description:

.. code-block:: bash

   ros2 param describe /data_publisher max_speed


``ros2 param dump``
----------------------------------------------------

Dump all of a node's current parameters to the terminal in YAML format:

.. code-block:: bash

   ros2 param dump /data_publisher

This is useful for capturing the current configuration to save as a YAML
file:

.. code-block:: bash

   ros2 param dump /data_publisher > saved_params.yaml
