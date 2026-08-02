====================================================
ARIAC and Robotics Tools
====================================================

This page covers the ARIAC testbed and the robotics tooling used across the
team projects: MoveIt2, ``py_trees_ros``, OpenCV, and a PDDL planner. Install
ROS 2 Jazzy and Gazebo Harmonic first (see :doc:`ros_setup`).

.. note::

   Always follow the official ARIAC installation guide for the exact,
   version-pinned commands, since they change with each release cycle:
   `ARIAC documentation <https://pages.nist.gov/ARIAC_docs/en/latest/>`_ and
   the `ARIAC GitHub repository <https://github.com/usnistgov/ARIAC>`_.


ARIAC 2025
----------

ARIAC is installed from source into a colcon workspace. The typical pattern is:

.. code-block:: bash

   mkdir -p ~/ariac_ws/src
   cd ~/ariac_ws/src
   git clone https://github.com/usnistgov/ARIAC.git
   cd ~/ariac_ws
   rosdep install --from-paths src -y --ignore-src
   colcon build
   source install/setup.bash

Refer to the official docs for the correct branch or tag for the ARIAC 2025
cycle and for any additional dependencies.


MoveIt2 (Motion Planning)
-------------------------

MoveIt2 provides motion planning and parameterized-grasp execution. Install the
Jazzy binaries:

.. code-block:: bash

   sudo apt install ros-jazzy-moveit


py_trees_ros (Behavior Trees)
-----------------------------

``py_trees_ros`` is the behavior-tree library used from PT1 onward:

.. code-block:: bash

   sudo apt install ros-jazzy-py-trees-ros ros-jazzy-py-trees-ros-interfaces

The `Groot2 <https://www.behaviortree.dev/groot/>`_ viewer is optional and is
useful for visualizing trees.


OpenCV (Perception)
-------------------

Classical perception in PT2 uses OpenCV with the ROS 2 ``cv_bridge``:

.. code-block:: bash

   sudo apt install ros-jazzy-cv-bridge
   pip install opencv-python


PDDL Planner
------------

PT3's classical baseline uses a PDDL planner. Two options are supported:

- **Unified Planning Framework** (Python-first, easiest to start with):

  .. code-block:: bash

     pip install unified-planning[engines]

- **Fast Downward** (research-grade), built from source per the
  `Fast Downward site <https://www.fast-downward.org/>`_.
