====================================================
ROS 2 Refresher
====================================================

.. admonition:: Read this before Lecture 1
   :class: important

   This page is **pre-read material**, not lecture content. It covers the
   ROS 2 prerequisites in the :doc:`syllabus </syllabus/index>`: packages and
   workspaces, publishers, subscribers, services and actions in Python,
   parameters, launch files, the ``ros2`` command-line tools, and reading C++
   ROS 2 code. It ends with lifecycle nodes, for reference.

   Reading takes about 40 minutes. Running the examples yourself takes about
   an hour more, and it is the better preparation. L1 opens with an ungraded
   diagnostic quiz on this material.

   L1 does not repeat this page. It teaches four topics that build on it:
   QoS profiles, executors and callback groups, actions in depth (cancel and
   goal status), and TF2 (see :ref:`Where L1 Picks Up <preread-ros2-l1>`).


What You Need
-------------

- Ubuntu 24.04 with ROS 2 Jazzy (``ros-jazzy-desktop``) and the
  development tools (``ros-dev-tools``), installed as the
  :doc:`ROS 2 setup page </ariac/ros_setup>` shows.
- One terminal per running program. Run this line in every new terminal:

  .. code-block:: bash

     source /opt/ros/jazzy/setup.bash

Every output on this page was copied from a run on 2026-10-12, on Ubuntu
24.04 with Python 3.12.3, ``rclpy`` 7.1.12, ``rclcpp`` 28.1.22, ``ros2cli``
0.32.13, ``launch_ros`` 0.26.13, ``colcon-core`` 0.21.3 and g++ 13.3.0. The
numbers in square brackets in a log line are timestamps (seconds since 1
January 1970), so yours will differ.

.. tip::

   **Two people, one network.** ROS 2 programs on the same network find
   each other. The `ROS 2 documentation on the domain ID
   <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Domain-ID.html>`__
   says: "All ROS 2 nodes use domain ID 0 by default." If a classmate's
   nodes show up in your lists, pick a number "between 0 and 101,
   inclusive" (same page) and set it in every terminal, for example
   ``export ROS_DOMAIN_ID=42``. Only programs with the same domain ID see
   each other.


The Running Example
-------------------

Every example on this page belongs to one small package, ``preread_demo``.
Its nodes stand in for a battery-cell **voltage tester** and a **monitor**:

- ``tester`` publishes a voltage reading every 0.5 s.
- ``monitor`` listens to the readings, keeps the last few, and returns their
  average when asked.
- ``fibonacci_server`` is an action server, for the actions section.
- ``managed_tester`` is a lifecycle version of ``tester``, for the last
  section.

The readings are not random. ``tester`` adds four fixed offsets to a
nominal voltage, in turn: +0.02, -0.01, +0.03 and -0.02 V, so every run
prints the same numbers. These are stand-ins: the real ARIAC topics come in
L1.


Workspaces and Packages
-----------------------

A **package** is the unit ROS 2 builds and installs: a folder with a
``package.xml`` that names the package and what it depends on. A
**workspace** is a folder that holds packages in a ``src`` folder. **colcon**
is the tool that builds every package in a workspace.

Step 1: Create the Workspace and the Package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   mkdir -p ~/preread_ws/src
   cd ~/preread_ws/src
   ros2 pkg create preread_demo --build-type ament_python \
     --license Apache-2.0 --dependencies rclpy std_srvs example_interfaces

- ``--build-type ament_python`` makes a Python package. A C++ package uses
  ``ament_cmake`` (see :ref:`preread-ros2-cpp`).
- ``--dependencies`` writes one ``<depend>`` line per package into
  ``package.xml``. Here: ``rclpy`` (the Python client library),
  ``std_srvs`` and ``example_interfaces`` (message types used below).

After you add the node files and the launch file from the sections below,
the package looks like this (the generated ``test`` folder is left out):

.. code-block:: text

   preread_demo
   |-- LICENSE
   |-- launch
   |   `-- demo.launch.py
   |-- package.xml
   |-- preread_demo
   |   |-- __init__.py
   |   |-- ask_average.py
   |   |-- fibonacci_client.py
   |   |-- fibonacci_server.py
   |   |-- managed_tester.py
   |   |-- monitor.py
   |   `-- tester.py
   |-- resource
   |   `-- preread_demo
   |-- setup.cfg
   `-- setup.py

   4 directories, 13 files

Step 2: Register Each Node in ``setup.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ros2 run`` finds a Python node through an **entry point**: a line in
``setup.py`` that gives the node's command name and the function to call.
The second ``data_files`` line installs the launch file.

.. code-block:: python
   :caption: preread_demo/setup.py (excerpt)

   data_files=[
       ('share/ament_index/resource_index/packages',
           ['resource/' + package_name]),
       ('share/' + package_name, ['package.xml']),
       ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
   ],
   ...
   entry_points={
       'console_scripts': [
           'tester = preread_demo.tester:main',
           'monitor = preread_demo.monitor:main',
           'ask_average = preread_demo.ask_average:main',
           'fibonacci_server = preread_demo.fibonacci_server:main',
           'fibonacci_client = preread_demo.fibonacci_client:main',
           'managed_tester = preread_demo.managed_tester:main',
       ],
   },

``glob`` needs ``from glob import glob`` at the top of ``setup.py``. A node
file that has no entry point builds without error, but ``ros2 run`` cannot
find it.

Step 3: Build and Source
~~~~~~~~~~~~~~~~~~~~~~~~

Build from the workspace root, not from ``src``:

.. code-block:: bash

   cd ~/preread_ws
   colcon build

Our run, with the C++ package of :ref:`preread-ros2-cpp` in the same
workspace (times differ from machine to machine):

.. code-block:: text

   Starting >>> preread_demo
   Starting >>> preread_demo_cpp
   Finished <<< preread_demo [1.06s]
   Finished <<< preread_demo_cpp [4.05s]

   Summary: 2 packages finished [4.17s]

colcon creates three folders next to ``src``: ``build`` (intermediate
files), ``install`` (what the build produced) and ``log`` (build logs).
Then, **in a new terminal**:

.. code-block:: bash

   source /opt/ros/jazzy/setup.bash
   source ~/preread_ws/install/setup.bash

The `workspace tutorial
<https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html>`__
names the two layers. Your workspace is an **overlay**, "a secondary
workspace where you can add new packages without interfering with the
existing ROS 2 workspace that you're extending, or 'underlay'". Here the
underlay is ``/opt/ros/jazzy``. The same page warns that "Sourcing an
overlay in the same terminal where you built, or likewise building where an
overlay is sourced, may create complex issues": build in one terminal, run
in another.

.. tip::

   Rebuild after every change. For Python packages, ``colcon build
   --symlink-install`` "saves you from having to rebuild every time you
   tweak python scripts" (same tutorial). You still rebuild after you change
   ``setup.py`` or add a file.


Nodes and Topics
----------------

A **node** is one program that takes part in the ROS 2 graph. A **topic**
is a named channel: **publishers** send messages on it and **subscribers**
receive them, with no reply. Each topic carries one **message type**, an
interface defined in a ``.msg`` file.

A Publisher
~~~~~~~~~~~

.. code-block:: python
   :caption: preread_demo/preread_demo/tester.py
   :linenos:

   """Publish stand-in voltage readings on the voltage topic."""
   import rclpy
   from rclpy.executors import ExternalShutdownException
   from rclpy.node import Node
   from example_interfaces.msg import Float64

   OFFSETS = [0.02, -0.01, 0.03, -0.02]  # fixed, so every run prints the same


   class Tester(Node):
       def __init__(self):
           super().__init__('tester')
           self.declare_parameter('nominal', 3.6)
           self.declare_parameter('period', 0.5)
           self.nominal = self.get_parameter('nominal').value
           period = self.get_parameter('period').value
           self.pub = self.create_publisher(Float64, 'voltage', 10)
           self.timer = self.create_timer(period, self.publish_reading)
           self.count = 0

       def publish_reading(self):
           msg = Float64()
           msg.data = self.nominal + OFFSETS[self.count % len(OFFSETS)]
           self.pub.publish(msg)
           self.get_logger().info(f'published {msg.data:.2f} V')
           self.count += 1


   def main():
       rclpy.init()
       node = Tester()
       try:
           rclpy.spin(node)
       except (KeyboardInterrupt, ExternalShutdownException):
           pass  # Ctrl+C ends spin(); rclpy shuts itself down

Reading it from the bottom up:

1. ``main`` starts ROS 2 (``rclpy.init``), creates the node, and **spins**
   it: ``rclpy.spin`` waits for events and runs the matching
   **callbacks** (the functions you handed to ROS 2) until you press Ctrl+C.
2. The constructor names the node ``tester``, declares two **parameters**
   (see :ref:`preread-ros2-params`), creates a publisher on the topic
   ``voltage``, and creates a **timer** that calls ``publish_reading`` every
   ``period`` seconds.
3. The ``10`` in ``create_publisher`` is the queue depth. L1 shows what else
   a publisher's QoS profile sets, and why it matters.
4. ``publish_reading`` fills one message and publishes it.

Run it:

.. code-block:: bash

   ros2 run preread_demo tester

.. code-block:: text

   [INFO] [1791857535.230498063] [tester]: published 3.62 V
   [INFO] [1791857535.710914591] [tester]: published 3.59 V
   [INFO] [1791857536.210843354] [tester]: published 3.63 V
   [INFO] [1791857536.710606936] [tester]: published 3.58 V

3.62 is 3.6 + 0.02, 3.59 is 3.6 - 0.01, and so on through the four offsets.

.. note::

   **Why** ``example_interfaces/msg/Float64``. Its own definition says it is
   for tests: "if you are deploying it into a system you should create a
   semantically meaningful message type" (see the ``ros2 interface show``
   output below). Real systems define their own messages: ARIAC's voltage
   testers publish ``ariac_interfaces/msg/VoltageReading`` (L5).
   ``std_msgs/msg/Float64`` says in its definition that it "is deprecated as
   of Foxy".

A Subscriber
~~~~~~~~~~~~

``monitor`` subscribes to ``voltage``. It also offers a service, which the
:ref:`services section <preread-ros2-services>` explains.

.. code-block:: python
   :caption: preread_demo/preread_demo/monitor.py
   :linenos:

   """Average the last readings and serve the average on request."""
   from collections import deque

   import rclpy
   from rclpy.executors import ExternalShutdownException
   from rclpy.node import Node
   from example_interfaces.msg import Float64
   from std_srvs.srv import Trigger


   class Monitor(Node):
       def __init__(self):
           super().__init__('monitor')
           self.declare_parameter('window', 4)
           self.readings = deque(maxlen=self.get_parameter('window').value)
           self.sub = self.create_subscription(
               Float64, 'voltage', self.on_reading, 10)
           self.srv = self.create_service(
               Trigger, 'get_average', self.on_get_average)

       def on_reading(self, msg):
           self.readings.append(msg.data)
           self.get_logger().info(f'heard {msg.data:.2f} V')

       def on_get_average(self, request, response):
           if not self.readings:
               response.success = False
               response.message = 'no readings yet'
           else:
               avg = sum(self.readings) / len(self.readings)
               response.success = True
               response.message = (
                   f'average of {len(self.readings)} readings: {avg:.3f} V')
           return response


   def main():
       rclpy.init()
       node = Monitor()
       try:
           rclpy.spin(node)
       except (KeyboardInterrupt, ExternalShutdownException):
           pass  # Ctrl+C ends spin(); rclpy shuts itself down

- ``create_subscription`` takes the message type, the topic name, the
  callback and the queue depth. Every message that arrives calls
  ``on_reading``.
- ``deque(maxlen=4)`` keeps only the last ``window`` readings: a fifth one
  pushes out the oldest.

Run ``tester`` in one terminal and ``monitor`` in another. The first 8
lines from ``monitor``:

.. code-block:: text

   [INFO] [1791857538.236996603] [monitor]: heard 3.62 V
   [INFO] [1791857538.724975398] [monitor]: heard 3.59 V
   [INFO] [1791857539.225441438] [monitor]: heard 3.63 V
   [INFO] [1791857539.725151215] [monitor]: heard 3.58 V
   [INFO] [1791857540.224992041] [monitor]: heard 3.62 V
   [INFO] [1791857540.723961163] [monitor]: heard 3.59 V
   [INFO] [1791857541.225324784] [monitor]: heard 3.63 V
   [INFO] [1791857541.724020672] [monitor]: heard 3.58 V


The ``ros2`` Command-Line Tools
-------------------------------

While ``tester`` and ``monitor`` run, a third terminal can look at the
graph. These are the outputs of our run:

.. code-block:: text

   $ ros2 node list
   /monitor
   /tester

   $ ros2 topic list
   /parameter_events
   /rosout
   /voltage

   $ ros2 topic info /voltage
   Type: example_interfaces/msg/Float64
   Publisher count: 1
   Subscription count: 1

   $ ros2 topic echo /voltage --once
   data: 3.63
   ---

   $ ros2 interface show example_interfaces/msg/Float64
   # This is an example message of using a primitive datatype, float64.
   # If you want to test with this that's fine, but if you are deploying
   # it into a system you should create a semantically meaningful message type.
   # If you want to embed it in another message, use the primitive data type instead.
   float64 data

- ``/parameter_events`` and ``/rosout`` are created by every node: one
  announces parameter changes, the other collects log messages.
- ``ros2 topic info`` is the first check when a subscriber receives
  nothing: is there a publisher at all, and is the type the one you expect?

``ros2 node info`` lists everything one node offers:

.. code-block:: text

   $ ros2 node info /monitor
   /monitor
     Subscribers:
       /voltage: example_interfaces/msg/Float64
     Publishers:
       /parameter_events: rcl_interfaces/msg/ParameterEvent
       /rosout: rcl_interfaces/msg/Log
     Service Servers:
       /get_average: std_srvs/srv/Trigger
       /monitor/describe_parameters: rcl_interfaces/srv/DescribeParameters
       /monitor/get_parameter_types: rcl_interfaces/srv/GetParameterTypes
       /monitor/get_parameters: rcl_interfaces/srv/GetParameters
       /monitor/get_type_description: type_description_interfaces/srv/GetTypeDescription
       /monitor/list_parameters: rcl_interfaces/srv/ListParameters
       /monitor/set_parameters: rcl_interfaces/srv/SetParameters
       /monitor/set_parameters_atomically: rcl_interfaces/srv/SetParametersAtomically
     Service Clients:

     Action Servers:

     Action Clients:

The six ``/monitor/..._parameters`` services exist in every node: the
``ros2 param`` commands below call them.

.. list-table:: The commands used on this page
   :header-rows: 1
   :widths: 40 60
   :class: compact-table

   * - **Command**
     - **What it does**
   * - ``ros2 run <pkg> <executable>``
     - Starts one node.
   * - ``ros2 launch <pkg> <file>``
     - Starts the nodes a launch file lists.
   * - ``ros2 node list`` / ``info``
     - Lists the nodes; shows one node's topics, services and actions.
   * - ``ros2 topic list`` / ``info`` / ``echo``
     - Lists topics; shows a topic's type and counts; prints its messages.
   * - ``ros2 interface show <type>``
     - Prints a message, service or action definition.
   * - ``ros2 param list`` / ``get`` / ``set``
     - Lists, reads and changes a node's parameters.
   * - ``ros2 service type`` / ``call``
     - Shows a service's type; sends one request.
   * - ``ros2 action list`` / ``send_goal``
     - Lists actions; sends one goal.
   * - ``ros2 lifecycle get`` / ``list`` / ``set``
     - Reads and changes a lifecycle node's state.

Every command has ``-h`` for its options.


.. _preread-ros2-params:

Parameters
----------

A **parameter** is a named setting of one node, such as ``nominal`` or
``window``, that you can choose at start-up without changing the code. A
node must **declare** each parameter, with a default value, before it can
use it (``declare_parameter`` in ``tester.py``, lines 13 and 14).

Reading them while the two nodes run:

.. code-block:: text

   $ ros2 param list /tester
     nominal
     period
     start_type_description_service
     use_sim_time

   $ ros2 param get /tester nominal
   Double value is: 3.6

   $ ros2 param get /monitor window
   Integer value is: 4

``use_sim_time`` and ``start_type_description_service`` exist in every
node. ``use_sim_time`` matters with a simulator such as Gazebo: when it is
true, the node takes its clock from the simulator.

**Setting a parameter at start-up.** ``--ros-args -p name:=value`` sets it
for one run:

.. code-block:: bash

   ros2 run preread_demo tester --ros-args -p nominal:=1.2

.. code-block:: text

   [INFO] [1791857551.478343779] [tester]: published 1.22 V
   [INFO] [1791857551.958421117] [tester]: published 1.19 V

**Setting a parameter while the node runs.** ``ros2 param set`` changes the
stored value, but ``tester`` read ``nominal`` once, in its constructor. In
this run we set ``nominal`` to 1.2 while ``tester`` was running:

.. code-block:: text

   $ ros2 param set /tester nominal 1.2
   Set parameter successful

   $ ros2 param get /tester nominal
   Double value is: 1.2

and ``tester`` kept publishing around 3.6 V to the end (last 3 of its 11
lines):

.. code-block:: text

   [INFO] [1791857518.455766307] [tester]: published 3.62 V
   [INFO] [1791857518.954742122] [tester]: published 3.59 V
   [INFO] [1791857519.455932478] [tester]: published 3.63 V

A node that must react to a change registers a callback for it (see the
parameter tutorial in :ref:`preread-ros2-reading`).


.. _preread-ros2-services:

Services
--------

A **service** is one request and one reply, between a **client** and a
**server**. A **service type** (a ``.srv`` file) defines both parts, split
by ``---``. ``std_srvs/srv/Trigger`` has an empty request:

.. code-block:: text

   $ ros2 service type /get_average
   std_srvs/srv/Trigger

   $ ros2 interface show std_srvs/srv/Trigger
   ---
   bool success   # indicate successful run of triggered service
   string message # informational, e.g. for error messages

The Server
~~~~~~~~~~

In ``monitor.py``, ``create_service(Trigger, 'get_average',
self.on_get_average)`` (lines 18 and 19) makes the node a server.
``on_get_average`` receives the request and an empty response, fills the
response, and returns it.

Calling it from the command line, with ``tester`` and ``monitor`` running:

.. code-block:: text

   $ ros2 service call /get_average std_srvs/srv/Trigger
   waiting for service to become available...
   requester: making request: std_srvs.srv.Trigger_Request()

   response:
   std_srvs.srv.Trigger_Response(success=True, message='average of 4 readings: 3.605 V')

The 4 readings in the window are the four offsets once each, so the
average is:

1. 3.62 + 3.59 + 3.63 + 3.58 = 14.42 V.
2. 14.42 / 4 = 3.605 V.

A Client in Python
~~~~~~~~~~~~~~~~~~

.. code-block:: python
   :caption: preread_demo/preread_demo/ask_average.py
   :linenos:

   """Call the get_average service once and print the reply."""
   import rclpy
   from rclpy.node import Node
   from std_srvs.srv import Trigger


   def main():
       rclpy.init()
       node = Node('ask_average')
       client = node.create_client(Trigger, 'get_average')
       if not client.wait_for_service(timeout_sec=5.0):
           node.get_logger().error('get_average is not available')
       else:
           future = client.call_async(Trigger.Request())
           rclpy.spin_until_future_complete(node, future)
           reply = future.result()
           node.get_logger().info(
               f'success={reply.success}, message="{reply.message}"')
       node.destroy_node()
       rclpy.shutdown()

.. code-block:: text

   $ ros2 run preread_demo ask_average
   [INFO] [1791857549.348944677] [ask_average]: success=True, message="average of 4 readings: 3.605 V"

- ``wait_for_service`` waits until a server exists, up to 5 s here.
- ``call_async`` sends the request and returns a **future**: an object that
  holds the reply once it arrives.
- ``spin_until_future_complete`` spins the node until the reply is in.

This client is a short script, so it may spin in ``main``. A client inside
a running node's callback cannot wait this way: L1's executor section shows
why.


Actions
-------

An **action** runs a long task: the client sends a **goal**, the server
sends **feedback** while it works, and the goal ends with a **result**. The
`ROS 2 concepts page on actions
<https://docs.ros.org/en/jazzy/Concepts/Basic/About-Actions.html>`__
describes it as "a long-running remote procedure call with feedback and the
ability to cancel or preempt the goal". An **action type** (an ``.action``
file) has three parts, split by ``---``:

.. code-block:: text

   $ ros2 interface show example_interfaces/action/Fibonacci
   # Goal
   int32 order
   ---
   # Result
   int32[] sequence
   ---
   # Feedback
   int32[] sequence

The Fibonacci action is the one the ROS 2 tutorials use: the goal is an
``order``, and the server builds the Fibonacci sequence (each number is the
sum of the two before it) one number per step.

The Server
~~~~~~~~~~

.. code-block:: python
   :caption: preread_demo/preread_demo/fibonacci_server.py
   :linenos:

   """An action server: build a Fibonacci sequence, one term per step."""
   import time

   import rclpy
   from rclpy.executors import ExternalShutdownException
   from rclpy.action import ActionServer
   from rclpy.node import Node
   from example_interfaces.action import Fibonacci


   class FibonacciServer(Node):
       def __init__(self):
           super().__init__('fibonacci_server')
           self.server = ActionServer(
               self, Fibonacci, 'fibonacci', self.execute)

       def execute(self, goal_handle):
           order = goal_handle.request.order
           self.get_logger().info(f'goal received: order {order}')
           feedback = Fibonacci.Feedback()
           feedback.sequence = [0, 1]
           for _ in range(1, order):
               feedback.sequence.append(
                   feedback.sequence[-1] + feedback.sequence[-2])
               goal_handle.publish_feedback(feedback)
               time.sleep(0.5)
           goal_handle.succeed()
           result = Fibonacci.Result()
           result.sequence = feedback.sequence
           return result


   def main():
       rclpy.init()
       node = FibonacciServer()
       try:
           rclpy.spin(node)
       except (KeyboardInterrupt, ExternalShutdownException):
           pass  # Ctrl+C ends spin(); rclpy shuts itself down

- ``execute`` runs once per accepted goal. ``goal_handle.request`` is the
  goal.
- ``publish_feedback`` sends feedback to the client. The sleep stands in for
  slow work.
- ``succeed()`` marks the goal done, and the returned object is the result.

Sending a Goal from the Command Line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With ``fibonacci_server`` running:

.. code-block:: text

   $ ros2 action send_goal --feedback /fibonacci example_interfaces/action/Fibonacci "{order: 5}"
   Waiting for an action server to become available...
   Sending goal:
        order: 5

   Goal accepted with ID: b3e044d798d74ad79521caa78f185c01

   Feedback:
       sequence:
   - 0
   - 1
   - 1

   Feedback:
       sequence:
   - 0
   - 1
   - 1
   - 2

   Feedback:
       sequence:
   - 0
   - 1
   - 1
   - 2
   - 3

   Feedback:
       sequence:
   - 0
   - 1
   - 1
   - 2
   - 3
   - 5

   Result:
       sequence:
   - 0
   - 1
   - 1
   - 2
   - 3
   - 5

   Goal finished with status: SUCCEEDED

Order 5 gives 4 feedback messages: the loop runs for ``range(1, 5)``, that
is 1, 2, 3 and 4, and adds one number each time to the starting ``[0, 1]``.

A Client in Python
~~~~~~~~~~~~~~~~~~

.. code-block:: python
   :caption: preread_demo/preread_demo/fibonacci_client.py
   :linenos:

   """An action client: send one goal, print feedback and the result."""
   import rclpy
   from rclpy.action import ActionClient
   from rclpy.node import Node
   from example_interfaces.action import Fibonacci


   def main():
       rclpy.init()
       node = Node('fibonacci_client')
       client = ActionClient(node, Fibonacci, 'fibonacci')
       client.wait_for_server()

       goal = Fibonacci.Goal()
       goal.order = 5

       def on_feedback(msg):
           node.get_logger().info(f'feedback: {list(msg.feedback.sequence)}')

       send_future = client.send_goal_async(goal, feedback_callback=on_feedback)
       rclpy.spin_until_future_complete(node, send_future)
       goal_handle = send_future.result()
       if not goal_handle.accepted:
           node.get_logger().info('goal rejected')
       else:
           result_future = goal_handle.get_result_async()
           rclpy.spin_until_future_complete(node, result_future)
           result = result_future.result().result
           node.get_logger().info(f'result: {list(result.sequence)}')
       node.destroy_node()
       rclpy.shutdown()

.. code-block:: text

   $ ros2 run preread_demo fibonacci_client
   [INFO] [1791857562.275336344] [fibonacci_client]: feedback: [0, 1, 1]
   [INFO] [1791857562.761744197] [fibonacci_client]: feedback: [0, 1, 1, 2]
   [INFO] [1791857563.262007701] [fibonacci_client]: feedback: [0, 1, 1, 2, 3]
   [INFO] [1791857563.761202819] [fibonacci_client]: feedback: [0, 1, 1, 2, 3, 5]
   [INFO] [1791857564.264828672] [fibonacci_client]: result: [0, 1, 1, 2, 3, 5]

The client waits twice, on two futures:

1. ``send_goal_async`` returns a future for the **goal handle**: the server's
   answer, accepted or rejected.
2. ``get_result_async`` returns a future for the result.

Feedback arrives through ``on_feedback`` in between. L1 adds what this page
leaves out: cancelling a goal, the final status (``SUCCEEDED``,
``CANCELED`` or ``ABORTED``), and why a server needs the right executor to
accept a cancel request while it works.


Launch Files
------------

A **launch file** starts several nodes at once, each with its own
parameters. In ROS 2 Jazzy it is often a Python file with a function
``generate_launch_description``.

.. code-block:: python
   :caption: preread_demo/launch/demo.launch.py
   :linenos:

   """Start the tester and the monitor with chosen parameters."""
   from launch import LaunchDescription
   from launch_ros.actions import Node


   def generate_launch_description():
       return LaunchDescription([
           Node(
               package='preread_demo',
               executable='tester',
               parameters=[{'nominal': 1.2, 'period': 1.0}],
           ),
           Node(
               package='preread_demo',
               executable='monitor',
               parameters=[{'window': 3}],
           ),
       ])

- ``executable`` is the entry point name from ``setup.py``.
- The launch file must be installed (the ``data_files`` line in Step 2),
  and the package needs ``<exec_depend>launch_ros</exec_depend>`` in
  ``package.xml``. Rebuild after adding it.

.. code-block:: bash

   ros2 launch preread_demo demo.launch.py

The first 13 lines of our run, which end with Ctrl+C:

.. code-block:: text

   [INFO] [launch]: All log files can be found below /home/zeidk/.ros/log/2026-10-12-22-12-32-751647-zeidk-Legion-7-16IRX9-3261323
   [INFO] [launch]: Default logging verbosity is set to INFO
   [INFO] [tester-1]: process started with pid [3261326]
   [INFO] [monitor-2]: process started with pid [3261327]
   [tester-1] [INFO] [1791857554.099752173] [tester]: published 1.22 V
   [monitor-2] [INFO] [1791857554.099981288] [monitor]: heard 1.22 V
   [tester-1] [INFO] [1791857555.079399056] [tester]: published 1.19 V
   [monitor-2] [INFO] [1791857555.079970678] [monitor]: heard 1.19 V
   [tester-1] [INFO] [1791857556.079165320] [tester]: published 1.23 V
   [monitor-2] [INFO] [1791857556.079754464] [monitor]: heard 1.23 V
   [WARNING] [launch]: user interrupted with ctrl-c (SIGINT)
   [INFO] [monitor-2]: sending signal 'SIGINT' to process[monitor-2]
   [INFO] [tester-1]: sending signal 'SIGINT' to process[tester-1]

- Each line from a node starts with its process name, ``tester-1`` or
  ``monitor-2``, so the two outputs can be told apart.
- ``period`` 1.0 gives one reading per second; ``nominal`` 1.2 gives
  1.22, 1.19 and 1.23 V (1.2 + 0.02, 1.2 - 0.01, 1.2 + 0.03).
- After these lines, our run printed ``[ERROR] [tester-1]: process has died
  [pid 3261326, exit code -2, ...]``, and the same for ``monitor-2``. Exit
  code -2 means the process ended on signal 2, SIGINT: the Ctrl+C you
  pressed, not a crash.


.. _preread-ros2-cpp:

Reading C++ ROS 2 Code
----------------------

You will not write C++ in this course, but you will read it: ARIAC's
Gazebo plugins are written in C++, and so are many ROS 2 packages. Here is ``tester`` again,
in C++, in a second package of the same workspace. It was made with
``ros2 pkg create preread_demo_cpp --build-type ament_cmake --license
Apache-2.0 --dependencies rclcpp example_interfaces``.

.. code-block:: cpp
   :caption: preread_demo_cpp/src/tester.cpp
   :linenos:

   // Publish stand-in voltage readings on the voltage topic (C++ version).
   #include <chrono>
   #include <memory>
   #include <vector>

   #include "rclcpp/rclcpp.hpp"
   #include "example_interfaces/msg/float64.hpp"

   class Tester : public rclcpp::Node
   {
   public:
     Tester()
     : Node("tester")
     {
       nominal_ = this->declare_parameter("nominal", 3.6);
       const double period = this->declare_parameter("period", 0.5);
       pub_ = this->create_publisher<example_interfaces::msg::Float64>(
         "voltage", 10);
       timer_ = this->create_wall_timer(
         std::chrono::duration<double>(period),
         std::bind(&Tester::publish_reading, this));
     }

   private:
     void publish_reading()
     {
       example_interfaces::msg::Float64 msg;
       msg.data = nominal_ + offsets_[count_ % offsets_.size()];
       pub_->publish(msg);
       RCLCPP_INFO(this->get_logger(), "published %.2f V", msg.data);
       ++count_;
     }

     const std::vector<double> offsets_{0.02, -0.01, 0.03, -0.02};
     double nominal_{};
     std::size_t count_{0};
     rclcpp::Publisher<example_interfaces::msg::Float64>::SharedPtr pub_;
     rclcpp::TimerBase::SharedPtr timer_;
   };

   int main(int argc, char * argv[])
   {
     rclcpp::init(argc, argv);
     rclcpp::spin(std::make_shared<Tester>());
     rclcpp::shutdown();
     return 0;
   }

.. list-table:: The same steps in Python and in C++
   :header-rows: 1
   :widths: 24 34 42
   :class: compact-table

   * - **Step**
     - **Python (rclpy)**
     - **C++ (rclcpp)**
   * - Message header
     - ``from example_interfaces.msg import Float64``
     - ``#include "example_interfaces/msg/float64.hpp"``; the type is
       ``example_interfaces::msg::Float64``
   * - Node class
     - ``class Tester(Node)``, ``super().__init__('tester')``
     - ``class Tester : public rclcpp::Node``, ``: Node("tester")``
   * - Parameter
     - ``declare_parameter``, then ``get_parameter(...).value``
     - ``declare_parameter`` returns the value at once
   * - Publisher
     - ``create_publisher(Float64, 'voltage', 10)``
     - ``create_publisher<Float64>("voltage", 10)``: the type goes in
       angle brackets
   * - Timer
     - ``create_timer(period, self.publish_reading)``
     - ``create_wall_timer(duration, std::bind(...))``
   * - Log
     - ``self.get_logger().info(f'...')``
     - ``RCLCPP_INFO(get_logger(), "...", args)``, printf-style
   * - Start and spin
     - ``rclpy.init()``, ``rclpy.spin(node)``
     - ``rclcpp::init(argc, argv)``, ``rclcpp::spin(node)``

Four C++ habits that ROS 2 code uses everywhere:

- ``this->`` calls a member of the class, like ``self.`` in Python.
- A name ending in ``_`` (``pub_``, ``timer_``) is a member variable, by
  convention. Python uses ``self.pub`` instead.
- ``SharedPtr`` is a pointer that deletes the object when nobody uses it any
  more. ``pub_->publish(msg)`` calls a method through it.
- ``std::bind(&Tester::publish_reading, this)`` makes a callable that runs
  ``publish_reading`` on this object: the C++ way to pass
  ``self.publish_reading``.

A C++ package builds through ``CMakeLists.txt``. These lines, added to the
generated file, build the node and install it where ``ros2 run`` finds it:

.. code-block:: cmake
   :caption: preread_demo_cpp/CMakeLists.txt (excerpt)

   find_package(ament_cmake REQUIRED)
   find_package(rclcpp REQUIRED)
   find_package(example_interfaces REQUIRED)

   add_executable(tester src/tester.cpp)
   ament_target_dependencies(tester rclcpp example_interfaces)
   install(TARGETS tester DESTINATION lib/${PROJECT_NAME})

It prints the same readings as the Python node:

.. code-block:: text

   $ ros2 run preread_demo_cpp tester
   [INFO] [1791857566.137010873] [tester]: published 3.62 V
   [INFO] [1791857566.637028502] [tester]: published 3.59 V
   [INFO] [1791857567.137105537] [tester]: published 3.63 V
   [INFO] [1791857567.637067507] [tester]: published 3.58 V
   [INFO] [1791857568.137029728] [tester]: published 3.62 V
   [INFO] [1791857568.246409203] [rclcpp]: signal_handler(SIGINT/SIGTERM)

The last line is rclcpp reporting the Ctrl+C.


Lifecycle Nodes (for Reference)
-------------------------------

.. note::

   This section is for reference. The course skills package has no
   lifecycle nodes, and no group project asks you to write one. You meet
   them when you read other ROS 2 packages.

A **lifecycle node** (also called a **managed node**) has states, and
another program moves it from state to state. It can start up in steps: set
itself up first, then start working when told to. The `ROS 2 design article
on managed nodes <https://design.ros2.org/articles/node_lifecycle.html>`__
says: "There are 4 primary states: Unconfigured Inactive Active Finalized".

.. list-table:: The four primary states, in the design article's words
   :header-rows: 1
   :widths: 20 80
   :class: compact-table

   * - **State**
     - **What the node does**
   * - Unconfigured
     - "the node is in immediately after being instantiated"
   * - Inactive
     - "a node that is not currently performing any processing"; it can be
       configured again without running
   * - Active
     - "the node performs any processing, responds to service requests,
       reads and processes data, produces output, etc."
   * - Finalized
     - "the state in which the node ends immediately before being
       destroyed"

A **transition** moves the node between states: ``configure``
(unconfigured to inactive), ``activate`` (inactive to active),
``deactivate`` (active to inactive), ``cleanup`` (inactive to
unconfigured) and ``shutdown`` (to finalized). Each transition calls a
callback in your node, such as ``on_configure``.

.. code-block:: python
   :caption: preread_demo/preread_demo/managed_tester.py
   :linenos:

   """A lifecycle (managed) version of the tester."""
   import rclpy
   from rclpy.executors import ExternalShutdownException
   from rclpy.lifecycle import Node, State, TransitionCallbackReturn
   from example_interfaces.msg import Float64


   class ManagedTester(Node):
       def __init__(self):
           super().__init__('managed_tester')
           self.pub = None
           self.timer = None

       def on_configure(self, state: State) -> TransitionCallbackReturn:
           self.pub = self.create_lifecycle_publisher(Float64, 'voltage', 10)
           self.get_logger().info('configured: publisher created')
           return TransitionCallbackReturn.SUCCESS

       def on_activate(self, state: State) -> TransitionCallbackReturn:
           self.timer = self.create_timer(0.5, self.publish_reading)
           self.get_logger().info('activated: publishing')
           return super().on_activate(state)

       def on_deactivate(self, state: State) -> TransitionCallbackReturn:
           self.destroy_timer(self.timer)
           self.get_logger().info('deactivated: stopped publishing')
           return super().on_deactivate(state)

       def on_cleanup(self, state: State) -> TransitionCallbackReturn:
           self.destroy_publisher(self.pub)
           self.get_logger().info('cleaned up: publisher destroyed')
           return TransitionCallbackReturn.SUCCESS

       def publish_reading(self):
           msg = Float64()
           msg.data = 3.6
           self.pub.publish(msg)


   def main():
       rclpy.init()
       node = ManagedTester()
       try:
           rclpy.spin(node)
       except (KeyboardInterrupt, ExternalShutdownException):
           pass  # Ctrl+C ends spin(); rclpy shuts itself down

- ``Node`` here comes from ``rclpy.lifecycle``, not ``rclpy.node``.
- A **lifecycle publisher** sends messages only while the node is active.
  ``super().on_activate`` and ``super().on_deactivate`` switch it on and
  off.
- Returning ``TransitionCallbackReturn.SUCCESS`` lets the transition finish.

Driving it from the command line while ``managed_tester`` runs:

.. code-block:: text

   $ ros2 lifecycle get /managed_tester
   unconfigured [1]

   $ ros2 lifecycle list /managed_tester
   - configure [1]
   	Start: unconfigured
   	Goal: configuring
   - shutdown [5]
   	Start: unconfigured
   	Goal: shuttingdown

   $ ros2 lifecycle set /managed_tester configure
   Transitioning successful

   $ ros2 lifecycle get /managed_tester
   inactive [2]

   $ ros2 lifecycle set /managed_tester activate
   Transitioning successful

   $ ros2 topic echo /voltage --once
   data: 3.6
   ---

   $ ros2 lifecycle set /managed_tester deactivate
   Transitioning successful

   $ ros2 lifecycle get /managed_tester
   inactive [2]

   $ ros2 lifecycle set /managed_tester cleanup
   Transitioning successful

   $ ros2 lifecycle get /managed_tester
   unconfigured [1]

The node's own log from the same run, one line per callback:

.. code-block:: text

   [INFO] [1791857598.267626156] [managed_tester]: configured: publisher created
   [INFO] [1791857600.361049681] [managed_tester]: activated: publishing
   [INFO] [1791857602.991913328] [managed_tester]: deactivated: stopped publishing
   [INFO] [1791857605.047632965] [managed_tester]: cleaned up: publisher destroyed

``ros2 lifecycle list`` shows only the transitions allowed from the current
state: from unconfigured, a node can only be configured or shut down.
``configured`` comes in the log before ``activated``: the node does not
publish until something activates it.


.. _preread-ros2-l1:

Where L1 Picks Up
-----------------

L1 assumes everything above and teaches four topics on top of it, each with
a short script and its measured output:

- :ref:`QoS profiles <l1-qos>`: what the ``10`` in ``create_publisher``
  leaves out, and why a subscriber can receive nothing without an error.
- :ref:`Executors and callback groups <l1-executors>`: who runs the
  callbacks, and why a slow callback can make a node miss messages.
- :ref:`Actions in depth <l1-actions>`: cancelling a goal, and the final
  status.
- :ref:`TF2 <l1-tf2>`: coordinate frames, and where a point in one frame is
  in another.


Check Yourself
--------------

Answer each question before you open its answer.

.. dropdown:: 1. You built your workspace, opened a new terminal and ran ``ros2 run preread_demo tester``. ROS 2 answers "Package 'preread_demo' not found". What is missing?
   :class-container: sd-border-secondary

   The new terminal has not sourced the overlay. Run
   ``source /opt/ros/jazzy/setup.bash`` and then
   ``source ~/preread_ws/install/setup.bash``. If the package is still not
   found, check that ``colcon build`` finished it without errors.

.. dropdown:: 2. You added a new node file to ``preread_demo/preread_demo/`` and rebuilt, but ``ros2 run`` cannot find it. Why?
   :class-container: sd-border-secondary

   It has no entry point. ``ros2 run`` finds a Python node through the
   ``console_scripts`` list in ``setup.py``. Add a line such as
   ``'my_node = preread_demo.my_node:main'``, then rebuild and source again.

.. dropdown:: 3. The monitor's window is 4. ``tester`` has published 6 readings. What does ``get_average`` return?
   :class-container: sd-border-secondary

   The deque keeps the last 4 readings: numbers 3 to 6, which are 3.63,
   3.58, 3.62 and 3.59 V (the offsets repeat after 4 readings).

   1. 3.63 + 3.58 + 3.62 + 3.59 = 14.42 V.
   2. 14.42 / 4 = 3.605 V.

   The message is ``average of 4 readings: 3.605 V``. Any 4 readings in a
   row hold each offset once, so the average stays 3.605 V.

.. dropdown:: 4. You want a 2 s period for one run without editing the code. Which command, and why does ``ros2 param set /tester period 2.0`` on a running node not do the job?
   :class-container: sd-border-secondary

   ``ros2 run preread_demo tester --ros-args -p period:=2.0``. On a running
   node, ``ros2 param set`` changes the stored value, but ``tester`` read
   ``period`` once, in its constructor, to create the timer. The timer keeps
   its 0.5 s period, as the ``nominal`` example in
   :ref:`preread-ros2-params` showed.

.. dropdown:: 5. Topic, service or action? (a) a battery reading every 0.5 s; (b) "what is the average now?"; (c) "move the arm to this pose and tell me how far along you are".
   :class-container: sd-border-secondary

   (a) A topic: a stream with no reply. (b) A service: one request, one
   reply. (c) An action: a long task with feedback and a result.

.. dropdown:: 6. In a C++ node you read ``sub_ = this->create_subscription<sensor_msgs::msg::Image>("camera", 10, std::bind(&Viewer::on_image, this, std::placeholders::_1));``. Say it in Python terms.
   :class-container: sd-border-secondary

   The node subscribes to the topic ``camera``, of type
   ``sensor_msgs/msg/Image``, with queue depth 10. Every message calls the
   member function ``on_image``, which takes the message as its one
   argument (``_1``). In Python:
   ``self.sub = self.create_subscription(Image, 'camera', self.on_image, 10)``.


.. _preread-ros2-reading:

Further Reading
---------------

- `ROS 2 Jazzy tutorials <https://docs.ros.org/en/jazzy/Tutorials.html>`__:
  the "Beginner: CLI tools" and "Beginner: Client libraries" tutorials cover
  this page in more depth. "Monitoring for parameter changes (Python)", in
  the intermediate tutorials, shows how a node reacts to ``ros2 param set``.
- `Creating a workspace
  <https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html>`__
  and `Creating a package
  <https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html>`__:
  overlays, underlays and ``ros2 pkg create``.
- `Writing a simple publisher and subscriber (Python)
  <https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html>`__.
- `Creating a launch file
  <https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html>`__.
- `Parameters <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Parameters.html>`__,
  `Interfaces <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Interfaces.html>`__,
  `Actions <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Actions.html>`__
  and `Introspection with command line tools
  <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Command-Line-Tools.html>`__:
  the concept pages behind each section.
- `The ROS_DOMAIN_ID
  <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Domain-ID.html>`__.
- `Managed nodes <https://design.ros2.org/articles/node_lifecycle.html>`__
  (the design article) and `Managing node lifecycles
  <https://docs.ros.org/en/jazzy/Tutorials/Demos/Managed-Nodes.html>`__
  (a C++ talker and listener as managed nodes).
- `ros2/examples, Jazzy branch <https://github.com/ros2/examples/tree/jazzy>`__:
  minimal publishers, subscribers, services and actions in Python and C++,
  side by side.
- `colcon documentation <https://colcon.readthedocs.io/en/released/>`__.
