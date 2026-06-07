====================================================
C++ Development Environment
====================================================

.. _setup-cpp:

Complete this setup before the first lecture. Make sure you have
:doc:`Ubuntu installed <ubuntu_setup>` first.


Build Tools
-----------

Install the essential build tools, debugger, CMake, and Valgrind:

.. code-block:: bash

   sudo apt update
   sudo apt install build-essential gdb cmake valgrind

Verify the installation:

.. code-block:: bash

   g++ --version
   cmake --version
   gdb --version
   valgrind --version

.. note::

   ``build-essential`` includes ``g++`` (the GNU C++ compiler),
   ``make``, and other libraries needed to compile C++ programs.
   ``valgrind`` is a memory debugging and leak detection tool used
   throughout the course.


Visual Studio Code
------------------

1. Download the ``.deb`` file from
   `code.visualstudio.com/download <https://code.visualstudio.com/download>`_.

2. Install from the terminal:

   .. code-block:: bash

      cd ~/Downloads
      sudo apt install ./code_*.deb

3. Launch VSCode:

   .. code-block:: bash

      code


Recommended Extensions
^^^^^^^^^^^^^^^^^^^^^^

Open the command palette (``Ctrl + Shift + P``) and select
**Extensions: Install Extension**, then install the following:

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - Extension
     - Purpose
   * - **C/C++** (Microsoft)
     - IntelliSense, debugging, and code browsing for C/C++.
   * - **CMake Tools** (Microsoft)
     - CMake integration for building and debugging.
   * - **CMake** (twxs)
     - Syntax highlighting for ``CMakeLists.txt`` files.
   * - **Doxygen Documentation Generator**
     - Generate Doxygen comment blocks with ``/**``.
   * - **Error Lens**
     - Display errors and warnings inline in the editor.
   * - **GitLens**
     - Enhanced Git integration and blame annotations.

.. tip::

   You can place an ``extensions.json`` file in your workspace's
   ``.vscode/`` folder to recommend extensions to all team members.
   See :doc:`Lecture 1 </lectures/lecture1/l1_lecture>` for details.


Workspace Structure
^^^^^^^^^^^^^^^^^^^

Create the following folder structure for your C++ lectures:

.. code-block:: text

   ~/enpm702_fall2026_cpp/
       lecture1/
           src/
               main.cpp
           include/
           CMakeLists.txt
       lecture2/
           src/
               main.cpp
           include/
           CMakeLists.txt
       ...

Open the workspace in VSCode:

.. code-block:: bash

   cd ~/enpm702_fall2026_cpp
   code .


Doxygen
-------

Doxygen generates documentation from annotated C++ source code.

.. code-block:: bash

   sudo apt install doxygen doxygen-gui


Git
---

Install Git and configure your identity:

.. code-block:: bash

   sudo apt install git
   git config --global user.name "Your Name"
   git config --global user.email "your_email@example.com"

Create a `GitHub <https://github.com>`_ account if you do not already
have one.

.. tip::

   Watch the **Version Control** pre-recorded video on Canvas for a
   full walkthrough of Git and GitHub workflows used in this course.
