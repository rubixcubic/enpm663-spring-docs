.. _l5_shell:

================
Shell Exercises
================

.. contents:: Table of Contents
   :depth: 2
   :local:

These exercises build on the shell skills from Lectures 1--4 and introduce functions in bash scripts, file processing, string manipulation, and control flow constructs.

.. dropdown:: Exercise 1 -- Functions in Bash Scripts
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Bash supports user-defined functions that can be called by name. Functions help organize scripts into reusable, modular pieces -- just like functions in C++.

   .. code-block:: bash

      # Define a function
      greet() {
          echo "Hello, $1!"
      }

      # Call the function with an argument
      greet "Alice"   # Output: Hello, Alice!
      greet "Bob"     # Output: Hello, Bob!

      # Function with multiple parameters
      add_numbers() {
          local sum=$(( $1 + $2 ))
          echo "Sum of $1 and $2 is: $sum"
      }

      add_numbers 5 10   # Output: Sum of 5 and 10 is: 15

   **Tasks:**

   1. Write a function ``say_hello`` that takes a name as an argument and prints ``Hello, <name>! Welcome to ENPM702.``
   2. Write a function ``multiply`` that takes two numbers and prints their product.
   3. Write a function ``file_info`` that takes a filename as an argument and prints whether the file exists, its size (using ``stat`` or ``wc -c``), and the number of lines.

.. dropdown:: Exercise 2 -- Return Values and Local Variables
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Bash functions do not return values like C++ functions. Instead, they use ``return`` for exit codes (0--255) and ``echo`` to output values that can be captured.

   .. code-block:: bash

      # Using return for exit codes
      is_even() {
          if (( $1 % 2 == 0 )); then
              return 0   # Success (true)
          else
              return 1   # Failure (false)
          fi
      }

      if is_even 4; then
          echo "4 is even"
      fi

      # Using echo to "return" a value (captured with command substitution)
      get_square() {
          local num=$1
          local result=$(( num * num ))
          echo "$result"
      }

      square=$(get_square 7)
      echo "Square of 7 is: $square"   # Output: Square of 7 is: 49

      # Local variables are scoped to the function
      demo_scope() {
          local local_var="I am local"
          global_var="I am global"
          echo "Inside function: $local_var"
      }

      demo_scope
      echo "Outside function: $local_var"    # Empty -- local_var is not visible
      echo "Outside function: $global_var"   # Prints: I am global

   **Tasks:**

   1. Write a function ``is_positive`` that returns exit code 0 if a number is positive and 1 otherwise. Test it with ``if is_positive 5; then ...``.
   2. Write a function ``celsius_to_fahrenheit`` that takes a Celsius value, computes the Fahrenheit equivalent using ``bc`` (for floating point: ``echo "scale=2; ($1 * 9/5) + 32" | bc``), and echoes the result. Capture the result in a variable and print it.
   3. Write a function that demonstrates the difference between ``local`` and non-local variables.

.. dropdown:: Exercise 3 -- Reading Files Line by Line
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Bash can process text files line by line using a ``while read`` loop. This is essential for log processing, data parsing, and configuration reading.

   .. code-block:: bash

      # Read a file line by line
      while IFS= read -r line; do
          echo "Line: $line"
      done < "input.txt"

      # Process a CSV file
      while IFS=',' read -r name age city; do
          echo "Name: $name, Age: $age, City: $city"
      done < "people.csv"

      # Read with line numbers
      line_num=1
      while IFS= read -r line; do
          echo "$line_num: $line"
          line_num=$(( line_num + 1 ))
      done < "input.txt"

   **Tasks:**

   1. Create a file ``students.txt`` with 5 names (one per line). Write a script that reads the file and prints each name with a greeting.
   2. Create a CSV file ``scores.csv`` with columns ``name,score``. Write a script that reads each line, and prints whether each student passed (score >= 60) or failed.
   3. Write a script that reads ``/etc/passwd`` and prints only the usernames (the first field, delimited by ``:``) and their shells (the last field).

.. dropdown:: Exercise 4 -- String Manipulation in Bash
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Bash provides built-in string manipulation capabilities using parameter expansion.

   .. code-block:: bash

      str="Hello, World!"

      # String length
      echo "${#str}"           # 13

      # Substring extraction: ${string:position:length}
      echo "${str:0:5}"        # Hello
      echo "${str:7}"          # World!

      # Substring replacement: ${string/pattern/replacement}
      echo "${str/World/Bash}" # Hello, Bash!

      # Replace all occurrences: ${string//pattern/replacement}
      msg="foo-bar-baz"
      echo "${msg//-/_}"       # foo_bar_baz

      # Remove prefix: ${string#pattern} (shortest) ${string##pattern} (longest)
      path="/home/user/docs/file.txt"
      echo "${path##*/}"       # file.txt (remove everything up to last /)

      # Remove suffix: ${string%pattern} (shortest) ${string%%pattern} (longest)
      echo "${path%/*}"        # /home/user/docs (remove last / and everything after)

      # Case conversion (Bash 4+)
      name="hello world"
      echo "${name^^}"         # HELLO WORLD (uppercase)
      echo "${name^}"          # Hello world (capitalize first letter)

   **Tasks:**

   1. Given a variable ``filepath="/home/user/project/src/main.cpp"``, extract just the filename (``main.cpp``) and the extension (``cpp``) using parameter expansion.
   2. Write a function ``to_snake_case`` that takes a string like ``"HelloWorld"`` and converts it. (Hint: use ``sed`` for inserting underscores before capitals, then convert to lowercase.)
   3. Write a script that reads a list of filenames and replaces all spaces in filenames with underscores using parameter expansion.

.. dropdown:: Exercise 5 -- Case Statements
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   The ``case`` statement is bash's version of a switch statement. It matches a value against patterns.

   .. code-block:: bash

      read -p "Enter a fruit: " fruit

      case "$fruit" in
          apple)
              echo "Apples are red or green."
              ;;
          banana)
              echo "Bananas are yellow."
              ;;
          orange | tangerine)
              echo "Citrus fruits!"
              ;;
          *)
              echo "Unknown fruit: $fruit"
              ;;
      esac

   **Tasks:**

   1. Write a script that takes a file extension as input and prints the type of file (e.g., ``.cpp`` -> "C++ source", ``.py`` -> "Python script", ``.sh`` -> "Shell script", etc.).
   2. Write a script that takes a single command-line argument (``start``, ``stop``, ``restart``, ``status``) and prints an appropriate message for each. Include a default case for invalid commands.
   3. Write a script that takes a month name and prints the number of days in that month.

.. dropdown:: Exercise 6 -- Select Menus
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   The ``select`` construct creates a numbered menu from a list and prompts the user to choose.

   .. code-block:: bash

      echo "Choose your editor:"
      select editor in vim nano emacs code "quit"; do
          case "$editor" in
              vim)
                  echo "You chose vim -- a classic!"
                  ;;
              nano)
                  echo "You chose nano -- beginner-friendly!"
                  ;;
              emacs)
                  echo "You chose emacs -- an operating system!"
                  ;;
              code)
                  echo "You chose VS Code -- modern and popular!"
                  ;;
              quit)
                  echo "Goodbye!"
                  break
                  ;;
              *)
                  echo "Invalid choice. Try again."
                  ;;
          esac
      done

   **Tasks:**

   1. Create a menu that lists 4 programming languages and prints a fun fact about the one selected.
   2. Create a file management menu with options: "Create file", "Delete file", "List files", "Quit". Implement each action (prompt for filenames where needed).
   3. Create a menu that lets users choose a build type (Debug, Release, RelWithDebInfo) and prints the corresponding ``cmake`` command.

.. dropdown:: Exercise 7 -- Trap for Cleanup
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   The ``trap`` command lets you run a function or command when a script receives a signal (e.g., ``EXIT``, ``INT`` for Ctrl+C, ``ERR``). This is essential for cleanup tasks.

   .. code-block:: bash

      # Cleanup function
      cleanup() {
          echo "Cleaning up temporary files..."
          rm -f /tmp/my_temp_file_$$
          echo "Done."
      }

      # Register the cleanup function to run on EXIT
      trap cleanup EXIT

      # Create a temp file
      echo "Working..." > /tmp/my_temp_file_$$

      # Simulate work
      echo "Processing..."
      sleep 2

      # Even if the script is interrupted (Ctrl+C), cleanup runs
      echo "Finished."
      # cleanup() runs automatically here because the script is exiting

   **Tasks:**

   1. Write a script that creates a temporary directory, does some work inside it, and uses ``trap`` to ensure the directory is deleted on exit (even if the script fails or is interrupted).
   2. Write a script that logs ``"Script started"`` to a log file at the beginning and ``"Script ended"`` at the end using ``trap EXIT``. Include a ``trap 'echo "Interrupted!"; exit 1' INT`` for Ctrl+C handling.
   3. Write a script with ``trap 'echo "Error on line $LINENO"; exit 1' ERR`` and ``set -e`` that runs several commands. Observe how the trap catches the error and reports the line number.

.. dropdown:: Exercise 8 -- Challenge: Build Automation Script
   :icon: gear
   :class-container: sd-border-warning
   :class-title: sd-font-weight-bold

   Write a comprehensive bash script called ``build_manager.sh`` that automates common C++ build tasks using functions, case statements, select menus, and trap. The script should:

   1. Define the following functions:

      - ``configure_project()``: Runs ``cmake`` with the selected build type (Debug/Release).
      - ``build_project()``: Runs ``cmake --build build``.
      - ``clean_project()``: Removes the ``build/`` directory.
      - ``run_project()``: Runs the built executable.
      - ``cleanup()``: A trap handler that reports elapsed time when the script exits.

   2. Use ``trap`` to register the cleanup function on ``EXIT``.

   3. Accept a command-line argument (``configure``, ``build``, ``clean``, ``run``, ``all``) using a ``case`` statement. If no argument is provided, display a ``select`` menu with these options.

   4. Use ``local`` variables inside functions for intermediate values.

   5. Read a simple config file (``build.conf``) line by line to get project settings (e.g., project name, build type, executable name).

   .. code-block:: bash

      # Example build.conf
      PROJECT_NAME=my_robot
      BUILD_TYPE=Release
      EXECUTABLE=robot_app

   .. code-block:: bash

      # Usage examples:
      ./build_manager.sh configure   # Configure with cmake
      ./build_manager.sh build       # Build the project
      ./build_manager.sh all         # Configure, build, and run
      ./build_manager.sh             # Show interactive menu
