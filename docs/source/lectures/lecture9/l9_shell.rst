================
Shell Exercises
================

.. contents:: Table of Contents
   :depth: 2
   :local:

These exercises build on the shell skills from Lectures 1--8 and represent
the **final shell exercise set** before we transition to ROS 2. The focus
is on shell libraries, building CLI tools, systemd basics, cron jobs, and a
comprehensive review that ties together everything covered so far.


.. dropdown:: Exercise 1 -- Creating a Shell Library
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    A shell library is a file containing reusable functions that can be sourced
    by other scripts. This is how you avoid duplicating utility code across
    multiple scripts.

    .. code-block:: bash

       # Create a library file: utils.sh
       #!/bin/bash

       # Color codes
       RED='\033[0;31m'
       GREEN='\033[0;32m'
       YELLOW='\033[1;33m'
       NC='\033[0m'  # No color

       log_info() {
           echo -e "${GREEN}[INFO]${NC} $1"
       }

       log_warn() {
           echo -e "${YELLOW}[WARN]${NC} $1"
       }

       log_error() {
           echo -e "${RED}[ERROR]${NC} $1"
       }

       check_command() {
           if command -v "$1" &> /dev/null; then
               log_info "$1 is installed"
               return 0
           else
               log_error "$1 is not installed"
               return 1
           fi
       }

    .. code-block:: bash

       # Source and use the library in another script: main.sh
       #!/bin/bash
       source ./utils.sh

       log_info "Starting deployment..."
       check_command "g++"
       check_command "cmake"
       log_warn "Checking optional dependencies..."
       check_command "valgrind"

    **Tasks:**

    1. Create ``utils.sh`` with the functions shown above. Make sure it is **not** executable on its own (it is a library, not a standalone script).
    2. Create ``main.sh`` that sources ``utils.sh`` and calls each function.
    3. Add a function ``confirm_action()`` to ``utils.sh`` that prompts the user with a yes/no question and returns 0 for yes, 1 for no.
    4. Add a function ``require_root()`` that checks if the script is running as root and exits with an error if not.


.. dropdown:: Exercise 2 -- Using ``source`` vs. Subshells
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    Understanding the difference between ``source`` (or ``.``) and running a
    script in a subshell is critical for writing shell libraries.

    .. code-block:: bash

       # set_var.sh
       #!/bin/bash
       MY_VAR="hello from set_var.sh"

    .. code-block:: bash

       # Test 1: Run in subshell
       bash set_var.sh
       echo "$MY_VAR"    # Empty! Variable was set in child process

       # Test 2: Source the file
       source set_var.sh
       echo "$MY_VAR"    # "hello from set_var.sh" -- variable is in current shell

    **Tasks:**

    1. Create ``set_var.sh`` as shown above. Run it with ``bash set_var.sh`` and then try ``echo "$MY_VAR"``. Explain why the variable is empty.
    2. Now run ``source set_var.sh`` and try ``echo "$MY_VAR"`` again. Explain the difference.
    3. Create a script ``setup_env.sh`` that exports ``PROJECT_ROOT``, ``BUILD_DIR``, and ``LOG_DIR`` variables. Source it and verify the variables are set in your current shell.
    4. What happens if you source a file that contains an ``exit`` command? Test it and explain.


.. dropdown:: Exercise 3 -- Building a Complete CLI Tool
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    Build a multi-command CLI tool using ``case`` statements, functions, and a
    shell library. The tool manages a simple project directory structure.

    .. code-block:: bash

       #!/bin/bash
       # project_tool.sh -- A project management CLI

       source ./utils.sh  # From Exercise 1

       PROJ_DIR="$HOME/my_project"

       cmd_init() {
           log_info "Initializing project in $PROJ_DIR..."
           mkdir -p "$PROJ_DIR"/{src,include,build,tests,docs}
           echo "cmake_minimum_required(VERSION 3.16)" > "$PROJ_DIR/CMakeLists.txt"
           log_info "Project initialized."
       }

       cmd_build() {
           log_info "Building project..."
           cd "$PROJ_DIR/build" || { log_error "Build dir not found"; return 1; }
           cmake .. && make
       }

       cmd_clean() {
           log_warn "Cleaning build directory..."
           rm -rf "$PROJ_DIR/build"/*
           log_info "Build directory cleaned."
       }

       cmd_status() {
           echo "Project: $PROJ_DIR"
           echo "Source files: $(find "$PROJ_DIR/src" -name '*.cpp' 2>/dev/null | wc -l)"
           echo "Header files: $(find "$PROJ_DIR/include" -name '*.hpp' 2>/dev/null | wc -l)"
           echo "Build artifacts: $(find "$PROJ_DIR/build" -type f 2>/dev/null | wc -l)"
       }

       cmd_help() {
           echo "Usage: $0 {init|build|clean|status|help}"
           echo ""
           echo "Commands:"
           echo "  init    Create project directory structure"
           echo "  build   Build the project with cmake/make"
           echo "  clean   Remove build artifacts"
           echo "  status  Show project statistics"
           echo "  help    Show this help message"
       }

       case "${1:-help}" in
           init)   cmd_init ;;
           build)  cmd_build ;;
           clean)  cmd_clean ;;
           status) cmd_status ;;
           help)   cmd_help ;;
           *)      log_error "Unknown command: $1"; cmd_help; exit 1 ;;
       esac

    **Tasks:**

    1. Create ``project_tool.sh`` as shown above. Test each command: ``init``, ``status``, ``clean``, ``help``.
    2. Add a ``cmd_test`` command that runs all ``.cpp`` files in the ``tests/`` directory (compile and execute each one).
    3. Add a ``cmd_new`` command that takes a filename argument and creates a new ``.cpp`` file with a basic template (include guards, main function).
    4. Add argument validation: if ``cmd_new`` is called without a filename, print an error and show usage.


.. dropdown:: Exercise 4 -- systemd Basics
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    ``systemd`` is the init system on modern Linux distributions. A **service
    file** tells systemd how to start, stop, and manage a background process.

    .. code-block:: ini

       # ~/.config/systemd/user/hello.service
       [Unit]
       Description=Hello World Service
       After=default.target

       [Service]
       Type=simple
       ExecStart=/bin/bash -c 'while true; do echo "Hello at $(date)" >> /tmp/hello.log; sleep 10; done'
       Restart=on-failure

       [Install]
       WantedBy=default.target

    .. code-block:: bash

       # Manage user-level services (no root required)
       mkdir -p ~/.config/systemd/user

       # Copy the service file
       cp hello.service ~/.config/systemd/user/

       # Reload systemd to pick up new service
       systemctl --user daemon-reload

       # Start the service
       systemctl --user start hello

       # Check status
       systemctl --user status hello

       # View logs
       journalctl --user -u hello -f

       # Stop the service
       systemctl --user stop hello

    **Tasks:**

    1. Create the ``hello.service`` file shown above in ``~/.config/systemd/user/``.
    2. Start the service, verify it is running with ``systemctl --user status hello``, and check the log at ``/tmp/hello.log``.
    3. Stop the service and verify it has stopped.
    4. Modify the service to run a custom script instead of an inline command. Create ``~/bin/heartbeat.sh`` that logs the system uptime every 30 seconds, and update the service file to use it.

    .. admonition:: Important
       :class: warning

       User-level systemd services (``--user``) do not require root access.
       System-level services (in ``/etc/systemd/system/``) require ``sudo``.


.. dropdown:: Exercise 5 -- Cron Jobs
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    ``cron`` is a time-based job scheduler. You define scheduled tasks in a
    **crontab** file. Each line specifies when and what to run.

    .. code-block:: text

       # Crontab format:
       # minute  hour  day-of-month  month  day-of-week  command
       #  0-59   0-23     1-31       1-12     0-7(0,7=Sun)

       # Examples:
       # Run every minute
       * * * * * echo "tick" >> /tmp/cron.log

       # Run at 8:00 AM every day
       0 8 * * * /home/user/bin/daily_report.sh

       # Run every 5 minutes
       */5 * * * * /home/user/bin/check_health.sh

       # Run at midnight on Mondays
       0 0 * * 1 /home/user/bin/weekly_cleanup.sh

    .. code-block:: bash

       # Edit your crontab
       crontab -e

       # List current crontab entries
       crontab -l

       # Remove all crontab entries
       crontab -r

    **Tasks:**

    1. Use ``crontab -e`` to add a cron job that appends the current date and system load (use ``uptime``) to ``~/cron_log.txt`` every minute.
    2. Wait 3 minutes, then verify the log file contains 3 entries.
    3. Remove the every-minute job and replace it with one that runs every 5 minutes.
    4. Write a cron expression that runs a backup script at 2:30 AM on the first day of every month.
    5. Remove your test crontab entries when done (use ``crontab -e`` to delete the lines).


.. dropdown:: Exercise 6 -- Building a Log Rotation Script
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    Combine shell scripting skills to build a log rotation utility. This is a
    common sysadmin task that exercises file operations, conditionals, loops,
    and date handling.

    .. code-block:: bash

       #!/bin/bash
       # rotate_logs.sh -- Rotate log files in a given directory

       source ./utils.sh

       LOG_DIR="${1:?Usage: $0 <log_directory>}"
       MAX_SIZE_KB="${2:-1024}"  # Default: 1MB
       ARCHIVE_DIR="$LOG_DIR/archive"

       rotate() {
           local file="$1"
           local timestamp
           timestamp=$(date +%Y%m%d_%H%M%S)
           local basename
           basename=$(basename "$file")
           local archive_name="${basename%.log}_${timestamp}.log.gz"

           gzip -c "$file" > "$ARCHIVE_DIR/$archive_name"
           truncate -s 0 "$file"
           log_info "Rotated $basename -> $archive_name"
       }

       mkdir -p "$ARCHIVE_DIR"

       for log_file in "$LOG_DIR"/*.log; do
           [ -f "$log_file" ] || continue
           size_kb=$(du -k "$log_file" | cut -f1)
           if [ "$size_kb" -ge "$MAX_SIZE_KB" ]; then
               rotate "$log_file"
           else
               log_info "$(basename "$log_file"): ${size_kb}KB (below ${MAX_SIZE_KB}KB threshold)"
           fi
       done

       # Clean up archives older than 30 days
       find "$ARCHIVE_DIR" -name "*.log.gz" -mtime +30 -delete
       log_info "Cleanup complete."

    **Tasks:**

    1. Create ``rotate_logs.sh`` as shown above.
    2. Create a test directory with several ``.log`` files of varying sizes (use ``dd`` or ``yes | head -c 2000000 > big.log`` to create large files).
    3. Run the script and verify that large files are compressed and archived while small files are left alone.
    4. Add a ``--dry-run`` flag that shows what would be rotated without actually doing it.


.. dropdown:: Exercise 7 -- Environment Setup Script
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    Create a comprehensive environment setup script that verifies and configures
    a development environment. This exercise combines ``source``, functions,
    conditionals, and command checking.

    **Tasks:**

    1. Create ``dev_setup.sh`` that performs the following checks:

       - Verify ``g++`` is installed and print its version.
       - Verify ``cmake`` is installed and print its version.
       - Verify ``git`` is installed and print its version.
       - Check if ``valgrind`` is installed (optional dependency -- warn if missing).
       - Check if ``~/.bashrc`` contains a ``PROJECT_ROOT`` export; if not, offer to add it.

    2. The script should use your ``utils.sh`` library from Exercise 1.
    3. Print a summary at the end showing which tools are available and which are missing.
    4. Add a ``--fix`` flag that attempts to install missing required packages using ``sudo apt install``.


.. dropdown:: Exercise 8 -- Comprehensive Review
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    This exercise combines skills from all previous shell exercises (L1--L9).
    Build a project workspace manager that automates common development tasks.

    **Tasks:**

    1. Create a script ``workspace.sh`` with the following subcommands:

       - ``workspace.sh create <name>``: Create a new C++ project with ``src/``, ``include/``, ``build/``, ``tests/`` directories and a template ``CMakeLists.txt``.
       - ``workspace.sh list``: List all projects in ``~/workspaces/`` with file counts and sizes.
       - ``workspace.sh archive <name>``: Create a ``tar.gz`` archive of a project.
       - ``workspace.sh search <pattern>``: Search all projects for a pattern in ``.cpp`` and ``.hpp`` files (use ``grep`` or ``find``/``xargs``).
       - ``workspace.sh stats``: Show total disk usage, number of projects, and total source file count across all projects.

    2. Use your ``utils.sh`` library for logging.
    3. Add proper error handling (missing arguments, non-existent projects, etc.).
    4. Add a ``workspace.sh backup`` command that archives all projects, compresses them, and moves them to ``~/backups/`` with a timestamp.

    .. dropdown:: Challenge
        :icon: rocket
        :class-container: sd-border-warning
        :class-title: sd-font-weight-bold

        Extend ``workspace.sh`` with a ``monitor`` subcommand that watches a
        project directory for file changes using ``inotifywait`` (from the
        ``inotify-tools`` package). When a ``.cpp`` or ``.hpp`` file is saved,
        automatically run ``cmake --build build/`` and report success or failure.
        Use your logging library to colorize the output.

        .. code-block:: bash

           # Install inotify-tools if needed
           sudo apt install inotify-tools

           # Basic inotifywait usage
           inotifywait -m -r -e modify,create --include '\.(cpp|hpp)$' src/ include/
