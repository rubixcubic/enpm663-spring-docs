====================================================
Lecture
====================================================




Course Introduction
====================================================


Course Overview
---------------

.. card::
    :class-card: sd-border-success sd-shadow-sm

    **Operating System**

    - Ubuntu Desktop 24.04 LTS: Noble Numbat (recommended)
    - Ubuntu Desktop 22.04 LTS: Jammy Jellyfish

.. card::
    :class-card: sd-border-success sd-shadow-sm

    **Software**

    - **Visual Studio Code** -- Code editor with rich extension support.
    - **ROS 2:**

      - Jazzy Jalisco (for Ubuntu 24.04)
      - Iron Irwini (for Ubuntu 22.04)

    - **Doxygen** -- Code documentation generator.
    - **Version Control:**

      - Git
      - GitHub (account required)

    - **Valgrind** -- Memory debugging and leak detection.
    - **CMake** -- Cross-platform build system.


Online Students
^^^^^^^^^^^^^^^

.. important::

   Online students participate asynchronously. They cannot be required to
   attend in-person for exams, presentations, or activities. Online
   students have at least 48 hours after the release of a recorded lecture
   to complete quizzes and assignments.


Linux Shell
====================================================


.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Definition**

    A :term:`shell <Shell>` is a program that provides a command-line
    interface (CLI) for users to interact with the operating system,
    allowing them to execute commands, run scripts, manage files, and
    control processes.


Common Shell Types
------------------

.. grid:: 1 2 2 3
    :gutter: 3

    .. grid-item-card:: Bash
        :class-card: sd-border-secondary

        `Bourne Again Shell <https://www.gnu.org/software/bash/>`_

        The default shell for most Linux distributions, known for its
        scripting capabilities.

    .. grid-item-card:: Zsh
        :class-card: sd-border-secondary

        `Z Shell <https://www.zsh.org/>`_

        Similar to Bash, with additional features like better
        autocompletion and customization options.

    .. grid-item-card:: Fish
        :class-card: sd-border-secondary

        `Friendly Interactive Shell <https://fishshell.com/>`_

        User-friendly and highly customizable, with a focus on simplicity.

    .. grid-item-card:: Csh / Tcsh
        :class-card: sd-border-secondary

        `C Shell / Tenex C Shell <https://www.tcsh.org/>`_

        Shells with syntax similar to the C programming language, often
        used in certain Unix environments.

    .. grid-item-card:: Ksh
        :class-card: sd-border-secondary

        `Korn Shell <http://www.kornshell.com/>`_

        A shell with advanced scripting features, sometimes used in
        enterprise environments.

.. tip::

   Check your current shell with:

   .. code-block:: bash

      ps -p $$


Configuration Files
-------------------

A :term:`shell configuration file <Configuration File (Shell)>` is a
script that runs each time a new shell session starts. It allows users to
customize their shell environment by defining settings, aliases,
functions, and environment variables.

.. list-table::
   :widths: 20 40 40
   :header-rows: 1
   :class: compact-table

   * - Shell
     - Config File
     - Location
   * - Bash
     - ``.bashrc``
     - Home directory (``~/``)
   * - Zsh
     - ``.zshrc``
     - Home directory (``~/``)
   * - Fish
     - ``config.fish``
     - ``~/.config/fish/``
   * - Csh / Tcsh
     - ``.cshrc``
     - Home directory (``~/``)
   * - Ksh
     - ``.kshrc``
     - Home directory (``~/``)

.. note::

   In most Unix-like operating systems (including Ubuntu), the tilde
   ``~`` symbol refers to the current user's home directory.
   ``cd ~`` takes you to your home directory.


Aliases
^^^^^^^

:term:`Aliases <Alias>` are shortcuts that save you from having to
remember or type long commands.

.. code-block:: bash

   alias identifier='value'

- An alias declaration starts with the ``alias`` keyword, followed by the
  alias name, an equal sign, and the command to be run.
- The command should be enclosed in quotes, with **no spaces around the
  equal sign**.
- Each alias should be declared on a separate line.

.. dropdown:: Examples
    :class-container: sd-border-secondary
    :open:

    .. code-block:: bash

       alias cdd='cd ~/Documents'
       alias meminfo='free -m -l -t'     # display memory usage
       alias weather='curl wttr.in'      # display weather information


Functions
^^^^^^^^^

:term:`Functions <Function (Shell)>` are reusable blocks of code that
allow you to group commands and execute them by calling the function's
name.

.. code-block:: bash

   # Method 1: Using the function keyword
   function function_name {
       commands
   }

   # Method 2: Without the function keyword
   function_name() {
       commands
   }

.. dropdown:: Examples
    :class-container: sd-border-secondary
    :open:

    .. code-block:: bash

       function greeting {
           echo "Hello $1 $2"
       }

    Call the function: ``greeting John Doe``

    .. code-block:: bash

       print_arguments() {
           echo "Function or script name: $0"
           echo "Number of arguments: $#"
           echo "All arguments (\$*): $*"
           echo "Each argument separately:"
           for arg in "$@"; do
               echo "$arg"
           done
       }

    Call the function: ``print_arguments 1 2 hello world``


Visual Studio Code (VSCode)
====================================================


.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Definition**

    :term:`Visual Studio Code` (VSCode) is a free code editor that works
    on Windows, Mac, and Linux. It is consistently ranked as the most
    popular code editor in developer surveys worldwide.

    - Used by development teams at major tech companies including Google
      and Netflix.
    - Supports virtually every programming language.
    - Makes coding faster and less error-prone with helpful features.
    - Thousands of extensions for languages, snippets, formatters,
      linters, debuggers, and themes.


Installation
------------

1. Download the ``.deb`` file from
   `code.visualstudio.com/download <https://code.visualstudio.com/download>`_.

2. Install:

   .. code-block:: bash

      sudo apt install ./code_<version>_amd64.deb

3. Run: ``code`` from the terminal or launch from Ubuntu Applications.

**Essential Interface:**

- **Activity Bar** (left side): File explorer, search, source control,
  extensions.
- **Editor**: Where you write code.
- **Terminal**: For running commands and programs.
- **Status Bar**: Shows file info and problems.


Workspace
---------

A :term:`workspace <Workspace>` is a container that holds a set of
related projects or code files. In this course we use the following
structure for C++ lectures:

.. code-block:: text

   enpm702_fall2026_cpp/
       lectureX/
           src/
               *.cpp
           include/
               *.hpp

.. admonition:: Task
   :class: tip

   1. Create the folder structure for ``lecture1``.
   2. Place ``lecture1.cpp`` in ``lecture1/src/``.
   3. Open the workspace in VSCode:

      .. code-block:: bash

         cd <workspace>
         code .


Configuration
-------------

- Open settings: **File** > **Preferences** > **Settings** or
  ``Ctrl + ,``
- Changes are stored in:

  - Workspace ``settings.json`` (in the ``.vscode`` folder), or
  - User ``settings.json``

- Workspace settings take precedence over user settings.


The .vscode Folder
^^^^^^^^^^^^^^^^^^

The ``.vscode`` folder is a special directory that VSCode creates to
store workspace-specific configuration.

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - File
     - Purpose
   * - ``settings.json``
     - Workspace-specific settings that override user settings.
   * - ``launch.json``
     - Debug configurations for your project.
   * - ``tasks.json``
     - Automates common development workflows.
   * - ``extensions.json``
     - Recommended extensions for the workspace.

.. admonition:: Task
   :class: tip

   1. Place ``extensions.json`` in the ``.vscode`` folder.
   2. ``Ctrl + Shift + P`` > **Extensions: Show Recommended Extensions**
      > Click the cloud icon to install all recommended extensions.


The Command Palette
^^^^^^^^^^^^^^^^^^^

The :term:`command palette <Command Palette>` displays a searchable list
of all available commands in VSCode, including those from installed
extensions. It is one of VSCode's most powerful features.

.. code-block:: text

   Ctrl + Shift + P


CMake
-----

:term:`CMake` is an open-source, cross-platform family of tools designed
to build, test, and package software.

.. code-block:: bash

   sudo apt install cmake
   cmake --version

A ``CMakeLists.txt`` file defines the build configuration for a project.
It specifies which source files to compile, which libraries to link
against, and other build-related settings.

.. admonition:: Task
   :class: tip

   1. Install build tools:

      .. code-block:: bash

         sudo apt install build-essential gdb cmake

   2. Place ``CMakeLists.txt`` in your workspace.
   3. ``Ctrl + Shift + P`` > **CMake: Set Build Target**
   4. ``Ctrl + Shift + P`` > **Developer: Reload Window**
   5. Ensure **CMake** appears in the side bar.
   6. Click **Configure** (do this only once).
   7. Click **Build** (do this only once).
   8. From now on, clicking the play button at the bottom of the window
      will build and run the executable.


Course Conventions
====================================================


``'\n'`` vs ``std::endl``
-------------------------

In this course, always use ``'\n'`` to insert a newline character. Do
**not** use ``std::endl`` unless you have a specific reason to flush the
output buffer.

.. code-block:: cpp

   std::cout << "Hello, World!" << '\n';    // correct
   std::cout << "Hello, World!" << std::endl; // avoid

.. warning::

   ``std::endl`` inserts a newline **and** flushes the output buffer.
   Flushing forces the program to write all buffered output to the
   console immediately, which is significantly slower than simply
   writing a newline character. In most situations, flushing is
   unnecessary — the buffer is automatically flushed when it is full,
   when the program ends, or when ``std::cin`` is used.

   Using ``std::endl`` in loops or high-frequency output can cause
   noticeable performance degradation. Use ``'\n'`` by default.
