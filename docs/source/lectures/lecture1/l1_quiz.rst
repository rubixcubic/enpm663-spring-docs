====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 1: Linux Shell, Shell
Configuration, Visual Studio Code, and CMake.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice
===============

.. admonition:: Question 1
   :class: hint

   What is a **shell** in the context of a Linux operating system?

   A. A graphical desktop environment for managing files.

   B. A program that provides a command-line interface to interact with the operating system.

   C. A type of programming language used to write C++ code.

   D. A hardware component that processes user input.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A program that provides a command-line interface to interact with the operating system.

   *Explanation:* A shell is a program that interprets commands and allows users to execute them, run scripts, manage files, and control processes through a CLI.


.. admonition:: Question 2
   :class: hint

   Which shell is the **default** for most Linux distributions?

   A. Zsh

   B. Fish

   C. Bash

   D. Ksh

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Bash (Bourne Again Shell)

   *Explanation:* Bash is the default shell for most Linux distributions and is widely used for scripting and interactive command-line use.


.. admonition:: Question 3
   :class: hint

   What is the correct syntax for creating a shell alias?

   A. ``alias identifier = 'value'``

   B. ``alias identifier='value'``

   C. ``set alias identifier 'value'``

   D. ``define identifier='value'``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``alias identifier='value'``

   *Explanation:* The alias command requires no spaces around the equal sign. The value should be enclosed in quotes.


.. admonition:: Question 4
   :class: hint

   Which configuration file does **Zsh** use?

   A. ``.bashrc``

   B. ``.zshrc``

   C. ``config.fish``

   D. ``.kshrc``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``.zshrc``

   *Explanation:* Zsh uses ``.zshrc``, located in the user's home directory. Each shell type has its own configuration file.


.. admonition:: Question 5
   :class: hint

   What does the ``~`` (tilde) symbol represent in a Linux terminal?

   A. The root directory.

   B. The previous directory.

   C. The current user's home directory.

   D. The temporary files directory.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- The current user's home directory.

   *Explanation:* In Unix-like operating systems, the tilde ``~`` is a shorthand for the current user's home directory (e.g., ``/home/username``).


.. admonition:: Question 6
   :class: hint

   What is the **Command Palette** in VSCode?

   A. A panel that shows compiler errors and warnings.

   B. A searchable list of all available commands in VSCode.

   C. A tool for managing Git repositories.

   D. A color picker for themes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A searchable list of all available commands in VSCode.

   *Explanation:* The Command Palette (``Ctrl + Shift + P``) is a universal search box for actions, including built-in commands and those from installed extensions.


.. admonition:: Question 7
   :class: hint

   What is the purpose of the ``CMakeLists.txt`` file?

   A. It stores VSCode workspace settings.

   B. It defines the build configuration for a C++ project.

   C. It lists all installed Linux packages.

   D. It contains shell aliases and functions.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It defines the build configuration for a C++ project.

   *Explanation:* ``CMakeLists.txt`` is used by CMake to specify which source files to compile, which libraries to link against, and other build-related settings.


.. admonition:: Question 8
   :class: hint

   Which file inside the ``.vscode`` folder stores **debug configurations**?

   A. ``settings.json``

   B. ``extensions.json``

   C. ``launch.json``

   D. ``tasks.json``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``launch.json``

   *Explanation:* ``launch.json`` contains debug configurations for the project. ``settings.json`` stores workspace settings, ``tasks.json`` automates workflows, and ``extensions.json`` lists recommended extensions.


----


True / False
============

.. admonition:: Question 9
   :class: hint

   **True or False:** Workspace ``settings.json`` takes precedence over
   user ``settings.json`` in VSCode.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   *Explanation:* Workspace settings override user settings, allowing project-specific configuration without affecting global preferences.


.. admonition:: Question 10
   :class: hint

   **True or False:** Shell aliases persist across terminal sessions
   without being added to a configuration file.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* Aliases defined directly in a terminal session are temporary. To persist them across sessions, they must be added to a shell configuration file (e.g., ``.bashrc`` or ``.zshrc``).


.. admonition:: Question 11
   :class: hint

   **True or False:** The ``ps -p $$`` command displays the current
   shell being used.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   *Explanation:* ``$$`` is a special variable that holds the PID of the current shell process. ``ps -p $$`` displays information about that process, including the shell name.


.. admonition:: Question 12
   :class: hint

   **True or False:** Fish shell uses ``.bashrc`` as its configuration
   file.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* Fish uses ``config.fish``, located in ``~/.config/fish/``. ``.bashrc`` is used by Bash.
