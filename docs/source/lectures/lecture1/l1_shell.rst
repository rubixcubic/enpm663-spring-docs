====================================================
Shell Exercises
====================================================

These exercises introduce fundamental Linux shell commands and concepts.
Difficulty increases with each lecture. Complete these exercises in a
terminal on your Ubuntu machine.

.. note::

   **Instructions:**

   - Open a terminal (``Ctrl + Alt + T``).
   - Try each exercise on your own before revealing the solution.
   - Exercises marked with a star are more challenging.


----


Navigating the File System
==========================

.. dropdown:: Exercise 1 -- Where Am I?
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Learn to identify your current location in the file system.

    **Tasks**

    1. Print the full path of your current working directory.
    2. List all files and folders in the current directory.
    3. List all files and folders, including hidden ones (files starting
       with ``.``).
    4. Navigate to your home directory using the tilde shortcut.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: bash

           # 1. Print current directory
           pwd

           # 2. List files and folders
           ls

           # 3. List all files, including hidden
           ls -a

           # 4. Navigate to home directory
           cd ~


.. dropdown:: Exercise 2 -- Creating and Moving Around
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice creating directories and navigating between them.

    **Tasks**

    1. In your home directory, create a folder called ``shell_practice``.
    2. Inside ``shell_practice``, create three subfolders: ``dir_a``,
       ``dir_b``, and ``dir_c``.
    3. Navigate into ``dir_a``.
    4. Go back to ``shell_practice`` using a relative path.
    5. Go directly to ``dir_c`` from ``shell_practice``.
    6. Return to your home directory using ``cd`` with no arguments.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: bash

           # 1. Create shell_practice
           mkdir ~/shell_practice

           # 2. Create subfolders
           mkdir ~/shell_practice/dir_a ~/shell_practice/dir_b ~/shell_practice/dir_c

           # 3. Navigate into dir_a
           cd ~/shell_practice/dir_a

           # 4. Go back to shell_practice
           cd ..

           # 5. Go to dir_c
           cd dir_c

           # 6. Return to home directory
           cd


.. dropdown:: Exercise 3 -- Absolute vs. Relative Paths
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Understand the difference between absolute and relative paths.

    **Tasks**

    1. From anywhere in the file system, navigate to ``/tmp`` using an
       absolute path.
    2. From ``/tmp``, navigate to your home directory using an absolute
       path.
    3. Create a folder ``~/shell_practice/dir_a/nested`` using an
       absolute path.
    4. Navigate to ``nested`` from your home directory using a relative
       path.
    5. From ``nested``, navigate to ``dir_b`` using a relative path.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: bash

           # 1. Navigate to /tmp (absolute)
           cd /tmp

           # 2. Navigate to home (absolute)
           cd /home/$USER
           # or: cd ~

           # 3. Create nested folder (absolute)
           mkdir ~/shell_practice/dir_a/nested

           # 4. Navigate to nested (relative)
           cd shell_practice/dir_a/nested

           # 5. Navigate to dir_b (relative)
           cd ../../dir_b


----


Working with Files
==================

.. dropdown:: Exercise 4 -- Creating and Viewing Files
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create files and view their contents from the terminal.

    **Tasks**

    1. Navigate to ``~/shell_practice/dir_a``.
    2. Create an empty file called ``notes.txt`` using ``touch``.
    3. Write "Hello, ENPM702!" into ``notes.txt`` using ``echo`` and
       output redirection (``>``).
    4. Display the contents of ``notes.txt`` using ``cat``.
    5. Append "This is my first shell exercise." to ``notes.txt`` using
       ``>>`` (append redirection).
    6. Display the updated contents.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: bash

           # 1. Navigate
           cd ~/shell_practice/dir_a

           # 2. Create empty file
           touch notes.txt

           # 3. Write to file (overwrites)
           echo "Hello, ENPM702!" > notes.txt

           # 4. Display contents
           cat notes.txt

           # 5. Append to file
           echo "This is my first shell exercise." >> notes.txt

           # 6. Display updated contents
           cat notes.txt

        .. warning::

           ``>`` **overwrites** the file. ``>>`` **appends** to the file.
           Using ``>`` on an existing file will erase its contents.


.. dropdown:: Exercise 5 -- Copying, Moving, and Removing
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Learn to copy, move, and delete files and directories.

    **Tasks**

    1. Copy ``notes.txt`` from ``dir_a`` to ``dir_b``.
    2. Rename the copy in ``dir_b`` to ``notes_backup.txt``.
    3. Move ``notes_backup.txt`` from ``dir_b`` to ``dir_c``.
    4. Delete ``notes.txt`` from ``dir_a``.
    5. Create a folder ``dir_a/temp`` with a file ``temp.txt`` inside it.
    6. Delete ``dir_a/temp`` and its contents in a single command.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: bash

           # 1. Copy file
           cp ~/shell_practice/dir_a/notes.txt ~/shell_practice/dir_b/

           # 2. Rename file
           mv ~/shell_practice/dir_b/notes.txt ~/shell_practice/dir_b/notes_backup.txt

           # 3. Move file
           mv ~/shell_practice/dir_b/notes_backup.txt ~/shell_practice/dir_c/

           # 4. Delete file
           rm ~/shell_practice/dir_a/notes.txt

           # 5. Create folder and file
           mkdir ~/shell_practice/dir_a/temp
           touch ~/shell_practice/dir_a/temp/temp.txt

           # 6. Delete folder and contents
           rm -r ~/shell_practice/dir_a/temp

        .. warning::

           ``rm -r`` removes directories and all their contents
           recursively. Use with caution -- there is no undo.


----


Aliases and Functions
=====================

.. dropdown:: Exercise 6 -- Creating Aliases
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create shell aliases to speed up common commands.

    **Tasks**

    1. Create an alias called ``ll`` that runs ``ls -la``.
    2. Test the alias by typing ``ll``.
    3. Create an alias called ``practice`` that navigates to your
       ``~/shell_practice`` folder.
    4. Test the alias.
    5. Add both aliases to your shell configuration file (``.bashrc``
       or ``.zshrc``).
    6. Open a new terminal and verify the aliases still work.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: bash

           # 1. Create alias (temporary -- current session only)
           alias ll='ls -la'

           # 2. Test
           ll

           # 3. Create navigation alias
           alias practice='cd ~/shell_practice'

           # 4. Test
           practice

           # 5. Add to config file (example for Bash)
           echo "alias ll='ls -la'" >> ~/.bashrc
           echo "alias practice='cd ~/shell_practice'" >> ~/.bashrc

           # 6. Reload the config file (or open new terminal)
           source ~/.bashrc


.. dropdown:: Exercise 7 -- Writing Shell Functions
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write shell functions that accept arguments.

    **Tasks**

    1. Write a function called ``mkcd`` that creates a directory and
       immediately navigates into it. It should accept the directory
       name as an argument.
    2. Test: ``mkcd test_folder`` should create ``test_folder`` and
       place you inside it.
    3. Write a function called ``backup`` that copies a file and appends
       ``.bak`` to the copy's name. It should accept a filename as an
       argument.
    4. Test: ``backup myfile.txt`` should create ``myfile.txt.bak`` in
       the same directory.
    5. Add both functions to your shell configuration file.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: bash

           # 1. mkcd function
           mkcd() {
               mkdir -p "$1" && cd "$1"
           }

           # 2. Test
           mkcd test_folder
           pwd  # should show .../test_folder

           # 3. backup function
           backup() {
               cp "$1" "$1.bak"
           }

           # 4. Test
           touch myfile.txt
           backup myfile.txt
           ls  # should show myfile.txt and myfile.txt.bak

        Add to ``~/.bashrc`` or ``~/.zshrc`` to persist across sessions.


----


Pipes and Redirection
=====================

.. dropdown:: Exercise 8 -- Combining Commands with Pipes
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Learn to chain commands using pipes (``|``).

    **Tasks**

    1. List all files in ``/usr/bin`` and pipe the output to ``wc -l``
       to count them.
    2. List all files in ``/usr/bin`` and pipe to ``grep python`` to
       find Python-related executables.
    3. Display the contents of ``/etc/passwd`` and pipe to ``head -5``
       to show only the first 5 lines.
    4. Run ``history`` and pipe to ``grep cd`` to find all your recent
       ``cd`` commands.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: bash

           # 1. Count files in /usr/bin
           ls /usr/bin | wc -l

           # 2. Find Python-related executables
           ls /usr/bin | grep python

           # 3. First 5 lines of /etc/passwd
           cat /etc/passwd | head -5

           # 4. Recent cd commands
           history | grep cd

        .. note::

           The pipe operator ``|`` takes the output of the command on the
           left and feeds it as input to the command on the right. You
           can chain multiple pipes together.


.. dropdown:: Exercise 9 -- Redirection Practice
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice redirecting command output to files.

    **Tasks**

    1. Save the output of ``ls -la ~`` to a file called
       ``~/shell_practice/home_listing.txt``.
    2. Save the output of ``date`` to ``~/shell_practice/log.txt``.
    3. Append the output of ``whoami`` to ``log.txt``.
    4. Append the output of ``uname -a`` to ``log.txt``.
    5. Display the contents of ``log.txt`` to verify all three entries.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: bash

           # 1. Save directory listing
           ls -la ~ > ~/shell_practice/home_listing.txt

           # 2. Save date
           date > ~/shell_practice/log.txt

           # 3. Append whoami
           whoami >> ~/shell_practice/log.txt

           # 4. Append system info
           uname -a >> ~/shell_practice/log.txt

           # 5. Verify
           cat ~/shell_practice/log.txt


----


Challenge
=========

.. dropdown:: Exercise 10 -- Build a Project Setup Script
    :icon: gear
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Write a shell function that automates the workspace structure
    described in the lecture.

    **Tasks**

    Write a function called ``new_lecture`` that:

    1. Accepts a lecture number as an argument (e.g., ``new_lecture 1``).
    2. Creates the folder structure:

       .. code-block:: text

          lectureN/
              src/
              include/

    3. Creates an empty ``main.cpp`` file in ``src/``.
    4. Prints a confirmation message: "Lecture N workspace created."
    5. Add this function to your shell configuration file.
    6. Test: ``new_lecture 2`` should create ``lecture2/src/main.cpp``
       and ``lecture2/include/``.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: bash

           new_lecture() {
               local num="$1"
               mkdir -p "lecture${num}/src" "lecture${num}/include"
               touch "lecture${num}/src/main.cpp"
               echo "Lecture ${num} workspace created."
           }

        Add to ``~/.bashrc`` or ``~/.zshrc``:

        .. code-block:: bash

           echo '
           new_lecture() {
               local num="$1"
               mkdir -p "lecture${num}/src" "lecture${num}/include"
               touch "lecture${num}/src/main.cpp"
               echo "Lecture ${num} workspace created."
           }' >> ~/.bashrc
           source ~/.bashrc

        Test:

        .. code-block:: bash

           cd ~/enpm702_fall2026_cpp
           new_lecture 2
           ls -R lecture2
