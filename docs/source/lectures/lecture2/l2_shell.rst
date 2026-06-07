====================================================
Shell Exercises
====================================================

These exercises build on the shell fundamentals from Lecture 1. You will
learn about environment variables, file permissions, finding files,
process management, command substitution, and basic shell scripting.

.. note::

   **Instructions:**

   - Open a terminal (``Ctrl + Alt + T``).
   - Try each exercise on your own before revealing the solution.
   - Exercises marked with a star (``*``) are more challenging.


----


Environment Variables
=====================

.. dropdown:: Exercise 1 -- Exploring and Setting Environment Variables
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Understand how environment variables work and how to create, modify,
    and inspect them.

    **Tasks**

    1. Print the values of ``$HOME``, ``$USER``, and ``$SHELL`` using ``echo``.
    2. Create a local variable called ``MY_PROJECT`` and set it to ``enpm702``. Print it.
    3. Open a new terminal tab and try to print ``MY_PROJECT``. What happens?
    4. Go back to the original tab and use ``export`` to make ``MY_PROJECT`` available to
       child processes. Verify by running ``bash -c 'echo $MY_PROJECT'``.
    5. Use ``env | grep MY_PROJECT`` to confirm the variable appears in the environment.
    6. Unset the variable with ``unset MY_PROJECT`` and verify it is gone.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: bash

           # Step 1: Print built-in environment variables
           echo "Home: $HOME"
           echo "User: $USER"
           echo "Shell: $SHELL"

           # Step 2: Create a local variable
           MY_PROJECT=enpm702
           echo $MY_PROJECT

           # Step 3: In a new tab, $MY_PROJECT is empty because
           # local variables are not inherited by other shells.

           # Step 4: Export the variable so child processes can see it
           export MY_PROJECT=enpm702
           bash -c 'echo $MY_PROJECT'
           # Output: enpm702

           # Step 5: Verify it is in the environment
           env | grep MY_PROJECT

           # Step 6: Unset the variable
           unset MY_PROJECT
           echo $MY_PROJECT
           # Output: (empty)


.. dropdown:: Exercise 2 -- Modifying the PATH Variable
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Understand how ``$PATH`` determines which commands the shell can find,
    and practice adding directories to it.

    **Tasks**

    1. Print the current value of ``$PATH``. Notice how directories are separated by colons.
    2. Create a directory ``~/bin`` if it does not already exist.
    3. Write a small script called ``greet`` inside ``~/bin`` that prints ``"Hello, $USER!"``.
       Make it executable.
    4. Try running ``greet`` from your home directory. It will likely fail with
       "command not found."
    5. Add ``~/bin`` to the **beginning** of your ``$PATH`` using ``export``.
    6. Run ``greet`` again -- it should work now.
    7. Use ``which greet`` to confirm the shell finds it in ``~/bin``.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: bash

           # Step 1: Print PATH
           echo $PATH

           # Step 2: Create ~/bin
           mkdir -p ~/bin

           # Step 3: Create the greet script
           echo '#!/bin/bash' > ~/bin/greet
           echo 'echo "Hello, $USER!"' >> ~/bin/greet
           chmod +x ~/bin/greet

           # Step 4: Try running it (will fail if ~/bin is not in PATH)
           greet
           # bash: greet: command not found

           # Step 5: Add ~/bin to the beginning of PATH
           export PATH="$HOME/bin:$PATH"

           # Step 6: Run it again
           greet
           # Output: Hello, <your-username>!

           # Step 7: Confirm location
           which greet
           # Output: /home/<your-username>/bin/greet


----


File Permissions
================

.. dropdown:: Exercise 3 -- Understanding and Changing File Permissions
    :icon: lock
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Learn to read permission strings from ``ls -l`` and modify them with
    ``chmod`` using both symbolic and octal notation.

    **Tasks**

    1. Create a directory called ``permissions_lab`` in ``/tmp`` and ``cd`` into it.
    2. Create three files: ``public.txt``, ``private.txt``, and ``script.sh``.
    3. Run ``ls -l`` and examine the permission strings (e.g., ``-rw-r--r--``).
    4. Using **symbolic notation**, remove all permissions for "group" and "others"
       on ``private.txt`` so only the owner can read and write it.
    5. Using **octal notation**, set ``script.sh`` to be readable, writable, and
       executable by the owner, readable and executable by the group, and
       have no permissions for others (i.e., ``rwxr-x---``).
    6. Using **octal notation**, set ``public.txt`` so that everyone can read it
       but only the owner can write it.
    7. Try running ``./script.sh`` -- it should succeed (the file is empty, so
       nothing happens, but no "Permission denied" error).
    8. Remove execute permission from ``script.sh`` using symbolic notation and
       try ``./script.sh`` again to see the error.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: bash

           # Step 1: Create the directory
           mkdir -p /tmp/permissions_lab
           cd /tmp/permissions_lab

           # Step 2: Create files
           touch public.txt private.txt script.sh

           # Step 3: Inspect permissions
           ls -l
           # Default is typically -rw-r--r-- (644)

           # Step 4: Restrict private.txt (symbolic)
           chmod go-rwx private.txt
           ls -l private.txt
           # -rw------- 1 user user 0 ... private.txt

           # Step 5: Set script.sh to rwxr-x--- (octal 750)
           chmod 750 script.sh
           ls -l script.sh
           # -rwxr-x--- 1 user user 0 ... script.sh

           # Step 6: Set public.txt to rw-r--r-- (octal 644)
           chmod 644 public.txt
           ls -l public.txt
           # -rw-r--r-- 1 user user 0 ... public.txt

           # Step 7: Run script.sh (owner has execute permission)
           ./script.sh
           # (no output, but no error either)

           # Step 8: Remove execute permission and try again
           chmod u-x script.sh
           ./script.sh
           # bash: ./script.sh: Permission denied


----


Finding Files and Content
=========================

.. dropdown:: Exercise 4 -- Using find and grep
    :icon: search
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Use ``find`` to locate files by name, type, and modification time,
    and use ``grep`` to search for patterns inside files.

    **Tasks**

    1. Create the following directory structure under ``/tmp/search_lab``:

       .. code-block:: text

          search_lab/
          ├── src/
          │   ├── main.cpp
          │   ├── utils.cpp
          │   └── utils.h
          ├── docs/
          │   ├── readme.txt
          │   └── notes.txt
          └── build/
              └── output.log

    2. Put the text ``#include <iostream>`` in both ``.cpp`` files and
       ``#pragma once`` in ``utils.h``.
    3. Use ``find`` to locate all ``.cpp`` files under ``/tmp/search_lab``.
    4. Use ``find`` to locate all files modified in the last 5 minutes.
    5. Use ``grep`` to search for the word ``include`` in all files under ``src/``.
    6. Use ``grep -r`` to recursively search the entire ``search_lab`` directory
       for the word ``pragma``.
    7. Combine ``find`` and ``grep`` using a pipe or ``-exec`` to find all ``.cpp``
       files that contain the word ``iostream``.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: bash

           # Step 1: Create directory structure
           mkdir -p /tmp/search_lab/{src,docs,build}

           # Step 2: Add content to files
           echo '#include <iostream>' > /tmp/search_lab/src/main.cpp
           echo '#include <iostream>' > /tmp/search_lab/src/utils.cpp
           echo '#pragma once' > /tmp/search_lab/src/utils.h
           echo 'Project readme' > /tmp/search_lab/docs/readme.txt
           echo 'Some notes' > /tmp/search_lab/docs/notes.txt
           echo 'Build output log' > /tmp/search_lab/build/output.log

           # Step 3: Find all .cpp files
           find /tmp/search_lab -name "*.cpp"
           # /tmp/search_lab/src/main.cpp
           # /tmp/search_lab/src/utils.cpp

           # Step 4: Find files modified in the last 5 minutes
           find /tmp/search_lab -type f -mmin -5

           # Step 5: Search for "include" in src/
           grep "include" /tmp/search_lab/src/*

           # Step 6: Recursive search for "pragma"
           grep -r "pragma" /tmp/search_lab/

           # Step 7: Find .cpp files containing "iostream" (two approaches)
           # Approach A: find with -exec
           find /tmp/search_lab -name "*.cpp" -exec grep -l "iostream" {} \;

           # Approach B: find piped to xargs
           find /tmp/search_lab -name "*.cpp" | xargs grep -l "iostream"


----


Process Management
==================

.. dropdown:: Exercise 5 -- Managing Background and Foreground Processes
    :icon: iterations
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Learn to run commands in the background, inspect running processes,
    and manage them with job control.

    **Tasks**

    1. Start a long-running command in the background:
       ``sleep 300 &``
    2. List your current jobs using ``jobs``.
    3. Use ``ps aux | grep sleep`` to find the process ID (PID) of the
       sleeping process.
    4. Bring the background job to the foreground using ``fg``.
    5. Suspend it with ``Ctrl + Z`` and confirm it is stopped with ``jobs``.
    6. Resume it in the background using ``bg``.
    7. Kill the process using ``kill`` and the PID you found earlier.
       Verify it is gone with ``jobs``.
    8. Start another ``sleep 120 &`` and kill it using ``kill %1``
       (job number syntax).

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: bash

           # Step 1: Start a background process
           sleep 300 &
           # [1] 12345   (PID will vary)

           # Step 2: List jobs
           jobs
           # [1]+  Running    sleep 300 &

           # Step 3: Find the PID
           ps aux | grep sleep
           # user  12345  ...  sleep 300

           # Step 4: Bring to foreground
           fg %1

           # Step 5: Suspend with Ctrl+Z
           # Press Ctrl+Z
           jobs
           # [1]+  Stopped    sleep 300

           # Step 6: Resume in background
           bg %1
           jobs
           # [1]+  Running    sleep 300 &

           # Step 7: Kill by PID
           kill 12345    # use the actual PID from step 3
           jobs
           # [1]+  Terminated  sleep 300

           # Step 8: Kill by job number
           sleep 120 &
           kill %1
           jobs


----


Command Substitution
====================

.. dropdown:: Exercise 6 -- Using Command Substitution (``*``)
    :icon: code-square
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Use ``$()`` to capture the output of one command and use it inside
    another command or assignment.

    **Tasks**

    1. Store today's date in a variable called ``TODAY`` using command substitution
       with ``date +%Y-%m-%d``.
    2. Print: ``"Today is: <date>"`` using the variable.
    3. Create a directory whose name includes the date:
       ``mkdir "backup_$(date +%Y-%m-%d)"``
    4. Count the number of files in ``/etc`` and store the result in a variable
       called ``FILE_COUNT``. Print: ``"There are <count> files in /etc."``.
    5. Use command substitution to find your current username (via ``whoami``)
       and create a file called ``<username>_log.txt``.
    6. Use **nested** command substitution to print the number of lines in
       the file ``/etc/passwd``:
       ``echo "Lines: $(wc -l < /etc/passwd)"``

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: bash

           # Step 1: Store today's date
           TODAY=$(date +%Y-%m-%d)

           # Step 2: Print it
           echo "Today is: $TODAY"

           # Step 3: Create a directory with the date in its name
           mkdir "backup_$(date +%Y-%m-%d)"

           # Step 4: Count files in /etc
           FILE_COUNT=$(ls /etc | wc -l)
           echo "There are $FILE_COUNT files in /etc."

           # Step 5: Create a file named after the current user
           touch "$(whoami)_log.txt"

           # Step 6: Nested command substitution
           echo "Lines: $(wc -l < /etc/passwd)"


----


Shell Scripting Basics
======================

.. dropdown:: Exercise 7 -- Writing Your First Shell Script
    :icon: file-code
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write a shell script that uses variables, conditionals, and command-line
    arguments.

    **Tasks**

    1. Create a file called ``sysinfo.sh`` in your home directory.
    2. Add the shebang line ``#!/bin/bash`` at the top.
    3. The script should:

       a. Print the current user, hostname, and date.
       b. Accept an optional command-line argument: a directory path.
       c. If no argument is given, default to the current directory.
       d. Check whether the directory exists. If it does, print how many
          files and subdirectories it contains. If not, print an error.

    4. Make the script executable and run it with:

       - No arguments (should use current directory).
       - ``/etc`` as an argument.
       - A non-existent path like ``/fake/path``.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: bash

           #!/bin/bash
           # sysinfo.sh -- Display system info and directory contents

           echo "============================="
           echo " System Information"
           echo "============================="
           echo "User:     $USER"
           echo "Hostname: $(hostname)"
           echo "Date:     $(date)"
           echo ""

           # Use argument or default to current directory
           TARGET_DIR="${1:-.}"

           if [ -d "$TARGET_DIR" ]; then
               FILE_COUNT=$(find "$TARGET_DIR" -maxdepth 1 -type f | wc -l)
               DIR_COUNT=$(find "$TARGET_DIR" -maxdepth 1 -type d | wc -l)
               # Subtract 1 from DIR_COUNT because find includes the directory itself
               DIR_COUNT=$((DIR_COUNT - 1))

               echo "Directory: $TARGET_DIR"
               echo "  Files:         $FILE_COUNT"
               echo "  Subdirectories: $DIR_COUNT"
           else
               echo "Error: '$TARGET_DIR' is not a valid directory."
               exit 1
           fi

        To create, make executable, and test:

        .. code-block:: bash

           # Create the script (copy the code above into the file)
           nano ~/sysinfo.sh

           # Make it executable
           chmod +x ~/sysinfo.sh

           # Test with no arguments
           ~/sysinfo.sh

           # Test with /etc
           ~/sysinfo.sh /etc

           # Test with a non-existent path
           ~/sysinfo.sh /fake/path
           # Error: '/fake/path' is not a valid directory.


.. dropdown:: Exercise 8 -- Build and Run a C++ Program with a Shell Script (``*``)
    :icon: rocket
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write a shell script that automates compiling and running a C++ source
    file with ``g++``. This exercise ties together environment variables,
    conditionals, command substitution, file permissions, and process management.

    **Tasks**

    1. Create a directory ``~/cpp_lab`` and write a simple C++ file called
       ``hello.cpp`` that prints ``"Hello from ENPM702!"`` to the console.
    2. Create a shell script called ``build_and_run.sh`` in ``~/cpp_lab`` that does
       the following:

       a. Accepts a ``.cpp`` file as a command-line argument.
       b. Validates that the argument was provided and that the file exists.
       c. Validates that the file has a ``.cpp`` extension.
       d. Uses ``g++`` to compile the file. The output binary should be named
          after the source file but without the ``.cpp`` extension
          (e.g., ``hello.cpp`` produces ``hello``).
       e. Checks whether compilation succeeded (using ``$?``).
       f. If compilation succeeded, runs the resulting binary and prints
          the exit code.
       g. If compilation failed, prints an error message and exits.

    3. Make the script executable and test it with ``hello.cpp``.
    4. Test it with a file that has a syntax error to verify the error handling.
    5. Test it with a non-existent file to verify the argument validation.

    .. dropdown:: Solution
        :class-container: sd-border-success

        First, create the C++ source file:

        .. code-block:: bash

           mkdir -p ~/cpp_lab
           cat > ~/cpp_lab/hello.cpp << 'CPPEOF'
           #include <iostream>

           int main() {
               std::cout << "Hello from ENPM702!" << '\n';
               return 0;
           }
           CPPEOF

        Now, create the build script:

        .. code-block:: bash

           #!/bin/bash
           # build_and_run.sh -- Compile and run a C++ source file

           # -- Validate arguments --
           if [ $# -eq 0 ]; then
               echo "Usage: $0 <source_file.cpp>"
               exit 1
           fi

           SOURCE_FILE="$1"

           # Check that the file exists
           if [ ! -f "$SOURCE_FILE" ]; then
               echo "Error: File '$SOURCE_FILE' not found."
               exit 1
           fi

           # Check the extension
           if [[ "$SOURCE_FILE" != *.cpp ]]; then
               echo "Error: '$SOURCE_FILE' is not a .cpp file."
               exit 1
           fi

           # -- Derive the output binary name --
           # Remove the .cpp extension using parameter expansion
           BINARY_NAME="${SOURCE_FILE%.cpp}"

           echo "Compiling '$SOURCE_FILE' -> '$BINARY_NAME' ..."

           # -- Compile --
           g++ -std=c++17 -Wall -Wextra -o "$BINARY_NAME" "$SOURCE_FILE"

           if [ $? -ne 0 ]; then
               echo "============================================"
               echo "  COMPILATION FAILED"
               echo "============================================"
               exit 1
           fi

           echo "Compilation successful."
           echo ""
           echo "============================================"
           echo "  Running ./$BINARY_NAME"
           echo "============================================"

           # -- Run the binary --
           ./"$BINARY_NAME"
           EXIT_CODE=$?

           echo ""
           echo "Program exited with code: $EXIT_CODE"

        To create, make executable, and test:

        .. code-block:: bash

           # Create the script (copy the code above into the file)
           nano ~/cpp_lab/build_and_run.sh

           # Make it executable
           chmod +x ~/cpp_lab/build_and_run.sh

           # Navigate to the project directory
           cd ~/cpp_lab

           # Test with hello.cpp
           ./build_and_run.sh hello.cpp
           # Compiling 'hello.cpp' -> 'hello' ...
           # Compilation successful.
           # ============================================
           #   Running ./hello
           # ============================================
           # Hello from ENPM702!
           #
           # Program exited with code: 0

           # Test with a non-existent file
           ./build_and_run.sh missing.cpp
           # Error: File 'missing.cpp' not found.

           # Create a file with a syntax error to test failure handling
           echo 'int main() { bad syntax }' > broken.cpp
           ./build_and_run.sh broken.cpp
           # Compiling 'broken.cpp' -> 'broken' ...
           # ... g++ error messages ...
           # ============================================
           #   COMPILATION FAILED
           # ============================================
