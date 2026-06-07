.. _l7_shell:

================
Shell Exercises
================

.. contents:: Table of Contents
   :depth: 2
   :local:

These exercises build on the shell skills from Lectures 1--6 and introduce tools
for remote access, file transfer, terminal multiplexing, build automation, and
environment setup.

Exercise 1: SSH Basics
-----------------------

``ssh`` (Secure Shell) allows you to connect to remote machines over an encrypted
connection. This is essential for working with robots, servers, and cloud
instances.

.. code-block:: bash

   # Basic connection (you will be prompted for a password)
   ssh username@hostname

   # Connect to a specific port
   ssh -p 2222 username@hostname

   # Run a single command on the remote machine
   ssh username@hostname "ls -la /home/username"

   # Generate an SSH key pair (if you don't have one)
   ssh-keygen -t ed25519 -C "your_email@example.com"

   # Copy your public key to a remote machine for passwordless login
   ssh-copy-id username@hostname

**Tasks:**

1. Generate an SSH key pair using ``ssh-keygen -t ed25519``. Examine the files created in ``~/.ssh/``.
2. View the contents of your public key with ``cat ~/.ssh/id_ed25519.pub``.
3. Connect to ``localhost`` using ``ssh localhost`` to test your SSH setup (you may need to install ``openssh-server``).
4. Run ``uname -a`` on the remote machine using a single ``ssh`` command without opening an interactive session.

Exercise 2: SCP and rsync
---------------------------

``scp`` copies files securely between hosts. ``rsync`` is a more powerful
alternative that only transfers changed portions of files and supports
resumable transfers.

.. code-block:: bash

   # scp: Copy a file to a remote machine
   scp local_file.txt username@hostname:/remote/path/

   # scp: Copy a file from a remote machine
   scp username@hostname:/remote/path/file.txt ./local_dir/

   # scp: Copy a directory recursively
   scp -r local_dir/ username@hostname:/remote/path/

   # rsync: Sync a directory (archive mode, verbose, progress)
   rsync -avz --progress local_dir/ username@hostname:/remote/path/

   # rsync: Dry run (show what would be transferred)
   rsync -avzn local_dir/ username@hostname:/remote/path/

**Tasks:**

1. Create a directory ``~/test_transfer/`` with three small text files. Use ``scp -r`` to copy it to ``/tmp/`` on the same machine (use ``localhost``).
2. Modify one of the files in the original directory. Use ``rsync -avz`` to sync the changes to ``/tmp/test_transfer/``. Observe that only the changed file is transferred.
3. Use ``rsync -avzn`` (dry run) to preview a transfer before actually executing it.

Exercise 3: tmux Basics -- Sessions
--------------------------------------

``tmux`` is a terminal multiplexer that lets you create multiple terminal
sessions, detach from them (they keep running in the background), and
reattach later. This is essential for long-running processes on remote machines.

.. code-block:: bash

   # Start a new tmux session
   tmux

   # Start a named session
   tmux new -s my_session

   # Detach from a session (session keeps running)
   # Press: Ctrl+b, then d

   # List all sessions
   tmux ls

   # Reattach to a session
   tmux attach -t my_session

   # Kill a session
   tmux kill-session -t my_session

**Tasks:**

1. Start a new named tmux session called ``build``. Run ``top`` inside it.
2. Detach from the session using ``Ctrl+b``, then ``d``.
3. List all tmux sessions using ``tmux ls`` to verify the session is still running.
4. Reattach to the ``build`` session and confirm ``top`` is still running.
5. Kill the session with ``tmux kill-session -t build``.

Exercise 4: tmux -- Windows and Panes
----------------------------------------

Within a single tmux session, you can create multiple **windows** (like tabs)
and split windows into **panes** (side-by-side terminals).

.. code-block:: bash

   # Create a new window:         Ctrl+b, then c
   # Switch to next window:       Ctrl+b, then n
   # Switch to previous window:   Ctrl+b, then p
   # Switch to window by number:  Ctrl+b, then 0-9

   # Split horizontally:          Ctrl+b, then "
   # Split vertically:            Ctrl+b, then %
   # Move between panes:          Ctrl+b, then arrow keys
   # Close a pane:                exit  (or Ctrl+d)

**Tasks:**

1. Create a tmux session with two windows. In the first window, run ``htop`` (or ``top``). In the second window, open a code file.
2. In the second window, split the pane vertically (``Ctrl+b``, ``%``). Run ``watch -n 1 date`` in one pane and use the other pane for shell commands.
3. Split a pane horizontally (``Ctrl+b``, ``"``). Practice navigating between panes with ``Ctrl+b`` + arrow keys.

Exercise 5: Makefile Basics -- Targets and Dependencies
---------------------------------------------------------

A ``Makefile`` automates the build process. Each rule has a **target**, optional
**dependencies**, and a **recipe** (commands to run). ``make`` only rebuilds
targets whose dependencies have changed.

.. code-block:: make

   # Basic Makefile structure
   # target: dependencies
   #     recipe (must be indented with a TAB, not spaces)

   all: main

   main: main.o utils.o
   	g++ -o main main.o utils.o

   main.o: main.cpp utils.h
   	g++ -c main.cpp

   utils.o: utils.cpp utils.h
   	g++ -c utils.cpp

   clean:
   	rm -f main *.o

.. code-block:: bash

   # Build the default target
   make

   # Build a specific target
   make clean

   # Build with verbose output
   make --debug

**Tasks:**

1. Create a simple C++ project with ``main.cpp`` and ``utils.cpp``/``utils.h``. Write the ``Makefile`` shown above.
2. Run ``make`` to build the project. Run it again and observe that nothing is rebuilt (no changes).
3. Modify ``utils.cpp`` and run ``make`` again. Observe that only ``utils.o`` and ``main`` are rebuilt.
4. Run ``make clean`` and verify all build artifacts are removed.

Exercise 6: Makefile Variables and Patterns
---------------------------------------------

Variables make Makefiles more maintainable. Pattern rules reduce repetition
when many files follow the same compilation pattern.

.. code-block:: make

   # Variables
   CXX      = g++
   CXXFLAGS = -std=c++17 -Wall -Wextra -g
   TARGET   = my_program
   SRCS     = main.cpp utils.cpp math_utils.cpp
   OBJS     = $(SRCS:.cpp=.o)

   # Default target
   all: $(TARGET)

   # Link
   $(TARGET): $(OBJS)
   	$(CXX) $(CXXFLAGS) -o $@ $^

   # Pattern rule: compile any .cpp to .o
   %.o: %.cpp
   	$(CXX) $(CXXFLAGS) -c $< -o $@

   # Clean
   clean:
   	rm -f $(TARGET) $(OBJS)

   .PHONY: all clean

**Tasks:**

1. Rewrite the Makefile from Exercise 5 using variables (``CXX``, ``CXXFLAGS``, ``TARGET``, ``SRCS``, ``OBJS``).
2. Add a pattern rule for compiling ``.cpp`` files to ``.o`` files.
3. Add the ``.PHONY`` declaration for ``all`` and ``clean``.
4. Test by building, modifying a source file, and rebuilding.

Exercise 7: Environment Setup Scripts
----------------------------------------

A setup script configures environment variables, paths, and aliases for a
development session. This is commonly used in robotics (e.g., sourcing a ROS 2
workspace).

.. code-block:: bash

   #!/bin/bash
   # setup_env.sh -- Source this file, don't execute it
   # Usage: source setup_env.sh

   # Set project root
   export PROJECT_ROOT="$HOME/enpm702_ws"

   # Add project binaries to PATH
   export PATH="$PROJECT_ROOT/build/bin:$PATH"

   # Set compiler flags
   export CXXFLAGS="-std=c++17 -Wall -Wextra"

   # Create useful aliases
   alias build="cd $PROJECT_ROOT && make -j$(nproc)"
   alias clean="cd $PROJECT_ROOT && make clean"

   echo "Environment configured for ENPM702 project"

**Tasks:**

1. Create a ``setup_env.sh`` file with the content above. Make it executable with ``chmod +x setup_env.sh``.
2. Source the script with ``source setup_env.sh`` and verify the environment variables are set using ``echo $PROJECT_ROOT``.
3. Add a check at the top of the script that verifies ``$PROJECT_ROOT`` exists and prints a warning if it does not.
4. Add a ``PS1`` override that changes your prompt to show the project name: ``export PS1="(enpm702) $PS1"``.

Exercise 8 (Challenge): Complete Build Environment
-----------------------------------------------------

Create a complete build environment that combines multiple shell skills.

**Requirements:**

1. Create a project directory with the following structure:

   .. code-block:: text

      my_project/
      ├── src/
      │   ├── main.cpp
      │   └── robot.cpp
      ├── include/
      │   └── robot.h
      ├── build/
      ├── Makefile
      └── setup_env.sh

2. Write a ``Makefile`` that:

   - Compiles ``.cpp`` files from ``src/`` with includes from ``include/``.
   - Places object files in ``build/``.
   - Supports ``make``, ``make clean``, and ``make rebuild`` (clean + build).

3. Write a ``setup_env.sh`` that:

   - Sets ``PROJECT_ROOT`` to the project directory.
   - Adds aliases for ``build``, ``clean``, and ``rebuild``.
   - Modifies the prompt.

4. Test the entire workflow in a tmux session with two panes: one for editing, one for building.

.. dropdown:: Hint
   :class-container: sd-border-warning

   For placing object files in ``build/``, use a pattern rule that maps
   ``build/%.o`` to ``src/%.cpp``:

   .. code-block:: make

      OBJDIR = build
      OBJS   = $(patsubst src/%.cpp,$(OBJDIR)/%.o,$(SRCS))

      $(OBJDIR)/%.o: src/%.cpp | $(OBJDIR)
      	$(CXX) $(CXXFLAGS) -I include -c $< -o $@

      $(OBJDIR):
      	mkdir -p $(OBJDIR)
