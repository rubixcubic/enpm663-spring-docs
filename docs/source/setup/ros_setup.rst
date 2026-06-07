====================================================
ROS 2 Development Environment
====================================================

.. _setup-ros:

ROS 2 is required starting in **Week 10**. The instructions below are
for **ROS 2 Jazzy Jalisco** on **Ubuntu 24.04**. If you are using
Ubuntu 22.04, install **ROS 2 Iron Irwini** instead.


Set Locale
----------

.. code-block:: bash

   locale  # check for UTF-8

   sudo apt update && sudo apt install locales
   sudo locale-gen en_US en_US.UTF-8
   sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
   export LANG=en_US.UTF-8

   locale  # verify settings


Add the ROS 2 Repository
-------------------------

.. code-block:: bash

   sudo apt install software-properties-common
   sudo add-apt-repository universe

   sudo apt update && sudo apt install curl -y
   sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
       -o /usr/share/keyrings/ros-archive-keyring.gpg

   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
       http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
       | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

   sudo apt update
   sudo apt upgrade


Install ROS 2 Jazzy
--------------------

.. code-block:: bash

   sudo apt install ros-jazzy-desktop

This installs ROS 2, RViz, demos, and tutorials.


Install Development Tools
-------------------------

.. code-block:: bash

   sudo apt install ros-dev-tools


Configure Your Shell
--------------------

Add the ROS 2 setup script to your shell configuration file so that
ROS 2 is available in every new terminal session.

**For Bash users** (``~/.bashrc``):

.. code-block:: bash

   echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
   source ~/.bashrc

**For Zsh users** (``~/.zshrc``):

.. code-block:: bash

   echo "source /opt/ros/jazzy/setup.zsh" >> ~/.zshrc
   source ~/.zshrc

Verify the installation:

.. code-block:: bash

   ros2 --help

.. warning::

   You must source the setup file in **every terminal** you use for
   ROS 2 development. Adding it to your shell configuration file
   automates this.


Configure colcon
^^^^^^^^^^^^^^^^

``colcon`` is the build tool used for ROS 2 workspaces. Add
autocompletion to your shell:

**For Bash users:**

.. code-block:: bash

   echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc

**For Zsh users:**

.. code-block:: bash

   echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.zsh" >> ~/.zshrc


ROS 2 Workspace
---------------

Create and build a ROS 2 workspace:

.. code-block:: bash

   mkdir -p ~/ros2_ws/src
   cd ~/ros2_ws
   colcon build
   source install/setup.bash

Add the workspace overlay to your shell configuration file:

**For Bash users:**

.. code-block:: bash

   echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc

**For Zsh users:**

.. code-block:: bash

   echo "source ~/ros2_ws/install/setup.zsh" >> ~/.zshrc

.. note::

   After making changes to your ``~/.bashrc`` or ``~/.zshrc``, either
   open a new terminal or run ``source ~/.bashrc`` (or ``source
   ~/.zshrc``) to apply the changes.


Verify ROS 2
------------

Open two terminals and run:

**Terminal 1 -- Talker:**

.. code-block:: bash

   ros2 run demo_nodes_cpp talker

**Terminal 2 -- Listener:**

.. code-block:: bash

   ros2 run demo_nodes_cpp listener

You should see the talker publishing messages and the listener
receiving them. Press ``Ctrl + C`` in both terminals to stop.


Gazebo (Simulation)
-------------------

Gazebo is required for the Group Projects (GP1--GP3). Install it with:

.. code-block:: bash

   sudo apt install ros-jazzy-ros-gz

Verify:

.. code-block:: bash

   gz sim --version


Summary of Shell Configuration
-------------------------------

After completing the setup, your ``~/.bashrc`` (or ``~/.zshrc``)
should contain these lines at the bottom:

.. code-block:: bash

   # ROS 2 Jazzy
   source /opt/ros/jazzy/setup.bash

   # colcon autocompletion
   source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash

   # ROS 2 workspace overlay
   source ~/ros2_ws/install/setup.bash

.. tip::

   You can add helpful aliases to your shell configuration file:

   .. code-block:: bash

      alias cb='cd ~/ros2_ws && colcon build'
      alias cbs='cd ~/ros2_ws && colcon build && source install/setup.bash'
      alias sw='source ~/ros2_ws/install/setup.bash'
