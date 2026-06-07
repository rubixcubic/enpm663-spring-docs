.. _l8_shell:

================
Shell Exercises
================

.. contents:: Table of Contents
   :depth: 2
   :local:

These exercises build on the shell skills from Lectures 1--7 and introduce advanced scripting techniques including command-line argument parsing with ``getopts``, associative arrays, JSON processing with ``jq``, signal handling, and process substitution.


.. dropdown:: Exercise 1 -- getopts: Basic Option Parsing
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Learn to parse command-line options using the built-in ``getopts`` command.

    **Background**

    ``getopts`` is a built-in Bash command for parsing single-character command-line options. It handles flags (``-v``) and options with arguments (``-n Alice``).

    .. code-block:: bash

       #!/bin/bash
       # script: greet.sh

       verbose=false
       name="World"

       while getopts "vn:" opt; do
           case $opt in
               v) verbose=true ;;
               n) name="$OPTARG" ;;
               \?) echo "Invalid option: -$OPTARG" >&2; exit 1 ;;
           esac
       done

       if $verbose; then
           echo "Running in verbose mode..."
       fi
       echo "Hello, $name!"

    **Tasks**

    1. Create the script above and run it with various combinations: ``./greet.sh``, ``./greet.sh -v``, ``./greet.sh -n Alice``, ``./greet.sh -v -n Bob``.
    2. Add a ``-h`` option that prints a usage message and exits.
    3. Add a ``-c`` option that takes a count argument and prints the greeting that many times.


.. dropdown:: Exercise 2 -- getopts: Build Script
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write a script ``build.sh`` that simulates a build system using ``getopts`` with required options, defaults, and error handling.

    **Starter Code**

    .. code-block:: bash

       #!/bin/bash
       # script: build.sh
       # Usage: ./build.sh -t <target> [-c] [-o <output_dir>] [-j <jobs>]

       target=""
       clean=false
       output_dir="./build"
       jobs=4

       while getopts "t:co:j:h" opt; do
           case $opt in
               t) target="$OPTARG" ;;
               c) clean=true ;;
               o) output_dir="$OPTARG" ;;
               j) jobs="$OPTARG" ;;
               h) echo "Usage: $0 -t <target> [-c] [-o <output_dir>] [-j <jobs>]"; exit 0 ;;
               \?) echo "Error: Invalid option -$OPTARG" >&2; exit 1 ;;
               :) echo "Error: Option -$OPTARG requires an argument" >&2; exit 1 ;;
           esac
       done

       if [[ -z "$target" ]]; then
           echo "Error: -t <target> is required" >&2
           exit 1
       fi

       echo "Target: $target"
       echo "Clean: $clean"
       echo "Output: $output_dir"
       echo "Jobs: $jobs"

    **Tasks**

    1. Create the script and test it with: ``./build.sh -t release -c -j 8 -o /tmp/build``.
    2. Test error handling: run without ``-t``, with an invalid option, and with a missing argument.
    3. Add validation: ensure ``-j`` is a positive integer and ``-t`` is one of ``debug``, ``release``, or ``test``.


.. dropdown:: Exercise 3 -- Associative Arrays
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Learn to use Bash associative arrays (dictionaries/hash maps) with ``declare -A``.

    **Background**

    .. code-block:: bash

       #!/bin/bash

       # Declare an associative array
       declare -A robot_speeds

       # Add entries
       robot_speeds[waffle]=0.26
       robot_speeds[burger]=0.22
       robot_speeds[create3]=0.31

       # Access a value
       echo "Waffle max speed: ${robot_speeds[waffle]} m/s"

       # Iterate over keys
       for robot in "${!robot_speeds[@]}"; do
           echo "$robot -> ${robot_speeds[$robot]} m/s"
       done

       # Check if key exists
       if [[ -v robot_speeds[waffle] ]]; then
           echo "Waffle is in the list"
       fi

       # Count entries
       echo "Total robots: ${#robot_speeds[@]}"

    **Tasks**

    1. Create an associative array mapping programming language names to their file extensions (e.g., ``cpp`` -> ``.cpp``, ``python`` -> ``.py``, ``rust`` -> ``.rs``).
    2. Write a script that reads a file extension from the user and looks up the language name.
    3. Write a script that counts the number of files by extension in a given directory, storing results in an associative array and printing a summary.


.. dropdown:: Exercise 4 -- JSON Processing with jq: Basics
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Learn basic JSON processing from the command line using ``jq``. Install it with ``sudo apt install jq``.

    **Background**

    .. code-block:: bash

       # Create a sample JSON file
       cat << 'EOF' > robots.json
       {
         "robots": [
           {"name": "turtlebot3", "type": "differential", "max_speed": 0.26},
           {"name": "create3", "type": "differential", "max_speed": 0.31},
           {"name": "spot", "type": "quadruped", "max_speed": 1.6}
         ]
       }
       EOF

       # Extract all robot names
       jq '.robots[].name' robots.json

       # Get the first robot
       jq '.robots[0]' robots.json

       # Filter robots by type
       jq '.robots[] | select(.type == "differential")' robots.json

       # Extract specific fields
       jq '.robots[] | {name, max_speed}' robots.json

    **Tasks**

    1. Create the JSON file above and run each ``jq`` command to understand the output.
    2. Write a ``jq`` command that finds the robot with the highest ``max_speed``.
    3. Write a ``jq`` command that outputs a formatted table: ``Name: <name>, Speed: <speed> m/s`` for each robot.
    4. Add a new robot to the JSON using ``jq`` and save the result to a new file.


.. dropdown:: Exercise 5 -- JSON Processing with jq: Advanced
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice advanced ``jq`` queries including grouping, filtering, and aggregation.

    **Background**

    .. code-block:: bash

       # Create a more complex JSON file
       cat << 'EOF' > sensor_data.json
       {
         "timestamp": "2026-10-15T10:30:00Z",
         "sensors": [
           {"id": "lidar_front", "type": "lidar", "range": 12.0, "status": "active"},
           {"id": "camera_rgb", "type": "camera", "resolution": "1920x1080", "status": "active"},
           {"id": "imu_center", "type": "imu", "frequency": 200, "status": "active"},
           {"id": "lidar_rear", "type": "lidar", "range": 10.0, "status": "error"},
           {"id": "camera_depth", "type": "camera", "resolution": "640x480", "status": "inactive"}
         ]
       }
       EOF

       # Count sensors by status
       jq '[.sensors[] | .status] | group_by(.) | map({status: .[0], count: length})' sensor_data.json

       # Get only active sensors
       jq '.sensors | map(select(.status == "active"))' sensor_data.json

    **Tasks**

    1. Write a ``jq`` expression that returns only the ``id`` and ``status`` of sensors that are not ``"active"``.
    2. Write a ``jq`` expression that groups sensors by ``type`` and counts how many of each type exist.
    3. Write a shell script that reads the JSON, checks for any sensor with ``"error"`` status, and prints a warning message with the sensor ID.


.. dropdown:: Exercise 6 -- Signal Handling
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Learn to handle signals in Bash scripts using ``trap``.

    **Background**

    Signals are software interrupts sent to a process. ``trap`` lets you catch signals and execute custom code.

    .. code-block:: bash

       #!/bin/bash
       # script: monitor.sh

       cleanup() {
           echo -e "\nCleaning up temporary files..."
           rm -f /tmp/monitor_*.tmp
           echo "Goodbye!"
           exit 0
       }

       # Trap SIGINT (Ctrl+C) and SIGTERM
       trap cleanup SIGINT SIGTERM

       # Trap EXIT for guaranteed cleanup
       trap 'echo "Script exiting..."' EXIT

       echo "Monitoring system (PID: $$). Press Ctrl+C to stop."
       counter=0

       while true; do
           echo "Heartbeat #$((++counter)) at $(date +%T)" > /tmp/monitor_$$.tmp
           echo "Heartbeat #$counter"
           sleep 2
       done

    **Tasks**

    1. Run the script and press ``Ctrl+C``. Observe the cleanup behavior.
    2. Open a second terminal and send ``SIGTERM`` using ``kill <PID>``. Verify cleanup runs.
    3. Modify the script to count the number of times ``Ctrl+C`` is pressed. On the first press, print "Press Ctrl+C again to quit." On the second press, actually exit.


.. dropdown:: Exercise 7 -- Subshells and Process Substitution
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Understand subshells and process substitution (``<(command)`` and ``>(command)``).

    **Background**

    A **subshell** runs commands in a child process. **Process substitution** treats command output as a file.

    .. code-block:: bash

       # Subshell: changes do not affect parent
       x=10
       (x=20; echo "Inside subshell: x=$x")
       echo "Outside subshell: x=$x"

       # Process substitution: compare two command outputs
       diff <(ls /usr/bin | sort) <(ls /usr/local/bin | sort)

       # Use process substitution to read from multiple sources
       paste <(cut -d: -f1 /etc/passwd) <(cut -d: -f7 /etc/passwd) | head -5

    **Tasks**

    1. Demonstrate that a variable modified inside a subshell does not affect the parent shell.
    2. Use process substitution with ``diff`` to compare the sorted output of ``apt list --installed`` on your system with a saved package list.
    3. Write a script that uses process substitution to merge two sorted lists of numbers from two files into a single sorted list without creating intermediate files.


.. dropdown:: Exercise 8 -- Putting It All Together
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write a script ``robot_config.sh`` that combines ``getopts``, associative arrays, ``jq``, and signal handling.

    **Requirements**

    - Accept command-line options using ``getopts``:

      - ``-r <robot_name>`` -- Robot name (required)
      - ``-c <config_file>`` -- JSON config file (default: ``robot_config.json``)
      - ``-v`` -- Verbose mode
      - ``-h`` -- Help message

    - Use an associative array to store supported robot types and their default speeds.
    - Read robot configuration from a JSON file using ``jq``.
    - Handle ``SIGINT`` with a cleanup function.
    - If verbose mode is enabled, use process substitution to log output to both the terminal and a log file.

    **Starter Code**

    .. code-block:: bash

       #!/bin/bash

       declare -A default_speeds
       default_speeds[turtlebot3]=0.26
       default_speeds[create3]=0.31
       default_speeds[custom]=0.0

       robot_name=""
       config_file="robot_config.json"
       verbose=false

       cleanup() {
           echo "Shutting down robot configuration..."
           exit 0
       }
       trap cleanup SIGINT SIGTERM

       while getopts "r:c:vh" opt; do
           case $opt in
               r) robot_name="$OPTARG" ;;
               c) config_file="$OPTARG" ;;
               v) verbose=true ;;
               h) echo "Usage: $0 -r <robot> [-c <config>] [-v]"; exit 0 ;;
               \?) exit 1 ;;
           esac
       done

       # Validate robot name
       if [[ -z "$robot_name" ]]; then
           echo "Error: -r <robot_name> is required" >&2
           exit 1
       fi

       # Check if robot type is supported
       if [[ -v default_speeds[$robot_name] ]]; then
           echo "Default speed for $robot_name: ${default_speeds[$robot_name]} m/s"
       else
           echo "Warning: Unknown robot type '$robot_name'"
       fi

       # Read config if file exists
       if [[ -f "$config_file" ]]; then
           echo "Reading configuration from $config_file..."
           jq '.' "$config_file"
       else
           echo "No config file found. Using defaults."
       fi

    **Tasks**

    1. Complete the script with full error handling and verbose logging.
    2. Create a sample ``robot_config.json`` file and test the script with various options.
    3. Add a feature that validates the JSON config file structure using ``jq`` before processing.


.. dropdown:: Challenge -- Automated Project Scaffolding
    :icon: gear
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Write a script ``scaffold.sh`` that creates a C++ project directory structure similar to what was discussed in the lecture.

    **Requirements**

    - Accept options: ``-p <project_name>`` (required), ``-c <class_name>`` (repeatable), ``-t`` (include test directory), ``-g`` (initialize git repo).
    - For each class name provided with ``-c``, generate a header file in ``include/`` and a source file in ``src/`` with boilerplate code.
    - Generate a ``CMakeLists.txt`` with the project name and source files.
    - Use associative arrays to track generated files.
    - Handle errors with ``trap`` and clean up partial directory structures on failure.

    **Example usage**

    .. code-block:: bash

       ./scaffold.sh -p week8 -c Vehicle -c Driver -c Engine -t -g
