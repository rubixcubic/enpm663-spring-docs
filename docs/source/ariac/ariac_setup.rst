====================================================
ARIAC and Robotics Tools
====================================================

This page covers ARIAC 2025 and the robotics tools used across the group
projects: MoveIt 2, ``py_trees_ros``, OpenCV, and a PDDL planner. Install
ROS 2 Jazzy and Gazebo Harmonic first (see :doc:`ros_setup`).

.. note::

   Always follow the official
   `ARIAC startup page <https://pages.nist.gov/ARIAC_docs/en/latest/pages/startup.html>`_
   for the exact commands, since they change with each release. The commands
   below are copied from it (checked 2026-10-11).


ARIAC 2025
----------

NIST describes two ways to run ARIAC. Both use the
`example team repository <https://github.com/usnistgov/ariac_example_team>`_,
which holds a team configuration and a sample trial.

.. tab-set::

   .. tab-item:: Docker (recommended by NIST)

      The image has every ARIAC dependency already installed:

      .. code-block:: bash

         docker pull nistariac/ariac2025:latest
         git clone https://github.com/usnistgov/ariac_example_team.git ~/ariac_example_team

   .. tab-item:: Native (Ubuntu 24.04)

      Clone both repositories into the ``src`` folder of a colcon
      workspace, then build it as the startup page describes:

      .. code-block:: bash

         git clone https://github.com/usnistgov/ARIAC.git src/ARIAC
         git clone https://github.com/usnistgov/ariac_example_team.git src/ariac_example_team

To start a trial in the native install, from the workspace:

.. code-block:: bash

   ros2 launch ariac_gz ariac.launch.py \
     trial_config:=src/ariac_example_team/example_team/config/trials/LHAF9835.yaml \
     user_config:=src/ariac_example_team/example_team/config/example_team_config.yaml

.. important::

   "The final evaluation will require teams to submit a Dockerfile for their
   solution" (ARIAC startup page). The final demo uses the same rule, so
   your team needs a working Dockerfile by then.


MoveIt 2 (Motion Planning)
--------------------------

MoveIt 2 plans the robot motions. The course skills package uses it for
picking and placing. Install the
Jazzy binaries:

.. code-block:: bash

   sudo apt install ros-jazzy-moveit


py_trees_ros (Behavior Trees)
-----------------------------

``py_trees_ros`` is the behavior-tree library used from GP1 onward:

.. code-block:: bash

   sudo apt install ros-jazzy-py-trees-ros ros-jazzy-py-trees-ros-interfaces

The `Groot2 <https://www.behaviortree.dev/groot/>`_ viewer is optional and is
useful for visualizing trees.


OpenCV (Perception)
-------------------

Classical perception in GP2 uses OpenCV with the ROS 2 ``cv_bridge``:

.. code-block:: bash

   sudo apt install ros-jazzy-cv-bridge
   pip install opencv-python


PDDL Planner
------------

GP3's classical baseline uses a PDDL planner. Two options are supported:

- **Unified Planning Framework** (Python-first, easiest to start with):

  .. code-block:: bash

     pip install unified-planning[engines]

- **Fast Downward** (research-grade), built from source per the
  `Fast Downward site <https://www.fast-downward.org/>`_.
