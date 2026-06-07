.. _l6_shell:

================
Shell Exercises
================

.. contents:: Table of Contents
   :depth: 2
   :local:

These exercises build on the shell skills from Lectures 1--5 and introduce **regular expressions**, **stream editing with sed**, and **awk programming**. By the end, you will be able to combine these tools in powerful text-processing pipelines.


.. dropdown:: Exercise 1 -- Regular Expressions with ``grep -E``
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   ``grep -E`` (extended grep) supports full regular expression syntax without requiring backslash escapes for metacharacters like ``+``, ``?``, ``|``, ``{}``, and ``()``.

   Create a file called ``robots.log`` with the following content:

   .. code-block:: text

      [INFO] Robot R2D2 speed: 1.5 m/s
      [WARN] Robot BB8 battery: 20%
      [ERROR] Robot C3PO collision detected
      [INFO] Robot R2D2 speed: 2.0 m/s
      [DEBUG] Sensor calibration started
      [WARN] Robot BB8 battery: 10%
      [ERROR] Robot R2D2 motor fault
      [INFO] Robot C3PO speed: 0.5 m/s

   **Basic Patterns:**

   .. code-block:: bash

      # Match lines containing "ERROR"
      grep -E "ERROR" robots.log

      # Match lines containing "R2D2" or "BB8"
      grep -E "R2D2|BB8" robots.log

      # Match lines starting with "[WARN]" or "[ERROR]"
      grep -E "^\[(WARN|ERROR)\]" robots.log

      # Match lines containing a decimal number (e.g., 1.5, 2.0)
      grep -E "[0-9]+\.[0-9]+" robots.log

      # Match lines where battery percentage is one or two digits
      grep -E "battery: [0-9]{1,2}%" robots.log

   **Tasks:**

   1. Find all lines that contain either ``WARN`` or ``ERROR`` log levels.
   2. Find all lines that mention a robot name (any word starting with an uppercase letter followed by digits: e.g., ``R2D2``, ``BB8``, ``C3PO``). Hint: use ``[A-Z]+[A-Z0-9]*``.
   3. Find all lines that contain a speed measurement (a number followed by ``m/s``).
   4. Count how many lines match each log level (``INFO``, ``WARN``, ``ERROR``, ``DEBUG``) using ``grep -c``.
   5. Find lines that do **not** contain ``Robot`` using ``grep -Ev``.


.. dropdown:: Exercise 2 -- More ``grep -E`` Patterns
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Create a file ``code_samples.txt``:

   .. code-block:: text

      int count{0};
      double speed{1.5};
      std::string name{"R2D2"};
      int* ptr{nullptr};
      const int MAX_SPEED{100};
      auto result{compute(x, y)};
      std::vector<int> values{1, 2, 3};

   **Tasks:**

   1. Find all lines that use uniform initialization (contain ``{`` and ``}``).

      .. code-block:: bash

         grep -E "\{.*\}" code_samples.txt

   2. Find all lines that declare a pointer (contain ``*``).
   3. Find all lines that use ``const`` or ``auto``.
   4. Find all lines where a variable name is in ``snake_case`` (lowercase letters and underscores): hint ``[a-z_]+``.
   5. Find all lines containing ``std::`` followed by any identifier.

      .. code-block:: bash

         grep -E "std::[a-z_]+" code_samples.txt


.. dropdown:: Exercise 3 -- Stream Editing with ``sed`` (Substitution)
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   ``sed`` (stream editor) processes text line by line. The most common operation is substitution: ``s/pattern/replacement/flags``.

   .. code-block:: bash

      # Replace first occurrence of "Robot" with "Unit" on each line
      sed 's/Robot/Unit/' robots.log

      # Replace ALL occurrences on each line (global flag)
      sed 's/Robot/Unit/g' robots.log

      # Case-insensitive replacement (GNU sed)
      sed 's/robot/Unit/Ig' robots.log

      # Replace only on lines matching a pattern
      sed '/ERROR/s/Robot/FAULTY_UNIT/g' robots.log

   **Tasks:**

   1. Replace all occurrences of ``m/s`` with ``meters per second`` in ``robots.log``.
   2. Replace ``[INFO]`` with ``[LOG]`` only on lines that contain ``speed``.
   3. Add a prefix ``>> `` to every line: ``sed 's/^/>> /' robots.log``.
   4. Remove all text inside square brackets (the log level): ``sed 's/\[.*\] //' robots.log``.


.. dropdown:: Exercise 4 -- ``sed`` (Deletion and In-Place Editing)
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   ``sed`` can also delete lines and edit files in place.

   .. code-block:: bash

      # Delete lines matching a pattern
      sed '/DEBUG/d' robots.log

      # Delete the first 2 lines
      sed '1,2d' robots.log

      # Delete empty lines
      sed '/^$/d' robots.log

      # In-place editing (modifies the file directly)
      sed -i 's/old/new/g' filename.txt

      # In-place with backup
      sed -i.bak 's/old/new/g' filename.txt

   **Tasks:**

   1. Delete all ``DEBUG`` lines from ``robots.log`` and save to a new file.
   2. Delete lines 3 through 5 from ``robots.log`` (pipe to a new file; do not modify the original).
   3. Create a copy of ``robots.log`` and use ``sed -i`` to replace all robot names with ``UNIT_X``.
   4. Use ``sed`` to print only lines 2 through 4: ``sed -n '2,4p' robots.log``.


.. dropdown:: Exercise 5 -- ``awk`` (Fields and Patterns)
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   ``awk`` is a powerful pattern-scanning and processing language. It splits each line into fields (``$1``, ``$2``, ...) by whitespace by default.

   .. code-block:: bash

      # Print the entire line
      awk '{print $0}' robots.log

      # Print the first field (log level)
      awk '{print $1}' robots.log

      # Print the third field (robot name)
      awk '{print $3}' robots.log

      # Print lines where the second field is "Robot"
      awk '$2 == "Robot" {print $0}' robots.log

      # Print lines matching a regex
      awk '/ERROR/ {print $0}' robots.log

   **Tasks:**

   1. Print only the robot names (field 3) from lines containing ``Robot``.
   2. Print the log level (field 1) and robot name (field 3) separated by a tab.
   3. Print only lines where the last field is ``m/s``.
   4. Print the line number and the line content: ``awk '{print NR, $0}' robots.log``.


.. dropdown:: Exercise 6 -- ``awk`` (Actions and Built-in Variables)
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   ``awk`` has several built-in variables:

   - ``NR``: current line (record) number
   - ``NF``: number of fields in the current line
   - ``FS``: field separator (default: whitespace)
   - ``$NF``: the last field on the line

   .. code-block:: bash

      # Count the number of lines
      awk 'END {print NR}' robots.log

      # Print lines with more than 6 fields
      awk 'NF > 6 {print $0}' robots.log

      # Use a custom field separator
      awk -F':' '{print $1}' /etc/passwd

      # Sum up values (e.g., extract speeds and sum them)
      awk '/speed/ {sum += $5} END {print "Total speed:", sum}' robots.log

   **Tasks:**

   1. Count how many lines contain ``ERROR``.
   2. Print the last field of every line.
   3. Compute the average speed from lines containing ``speed:`` (extract the numeric value and compute the mean).
   4. Print lines where the number of fields (``NF``) is greater than 7.


.. dropdown:: Exercise 7 -- ``awk`` (Custom Field Separator and Formatting)
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Create a file called ``sensor_data.csv``:

   .. code-block:: text

      timestamp,sensor_id,temperature,humidity
      1001,S01,22.5,45.0
      1002,S02,23.1,44.2
      1003,S01,22.8,45.5
      1004,S03,25.0,40.1
      1005,S02,23.5,43.8

   .. code-block:: bash

      # Use comma as field separator
      awk -F',' '{print $2, $3}' sensor_data.csv

      # Formatted output with printf
      awk -F',' 'NR > 1 {printf "Sensor %s: Temp=%.1f, Humid=%.1f\n", $2, $3, $4}' sensor_data.csv

   **Tasks:**

   1. Print only the sensor IDs and temperatures (skip the header line).
   2. Calculate the average temperature across all data rows.
   3. Print only rows where the temperature is above 23.0.
   4. Count how many readings came from sensor ``S01``.
   5. Print the row with the highest temperature.


.. dropdown:: Exercise 8 -- Combining Tools in Pipelines
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   The real power comes from combining ``grep``, ``sed``, and ``awk`` in pipelines.

   .. code-block:: bash

      # Find ERROR lines, extract robot name, sort uniquely
      grep -E "ERROR" robots.log | awk '{print $3}' | sort -u

      # Replace robot names, then count lines per log level
      sed 's/Robot/Unit/g' robots.log | awk '{print $1}' | sort | uniq -c | sort -rn

      # Extract speeds, remove "m/s", compute average
      grep "speed:" robots.log | sed 's/ m\/s//' | awk '{sum += $NF; n++} END {print sum/n}'

   **Tasks:**

   1. Find all ``WARN`` lines, extract the battery percentage (just the number), and compute the average battery level.
   2. Extract all unique robot names mentioned in ``ERROR`` or ``WARN`` lines.
   3. Generate a summary report: for each robot name, count how many log entries it has.

      .. code-block:: bash

         awk '$2 == "Robot" {print $3}' robots.log | sort | uniq -c | sort -rn

   4. Create a pipeline that converts all log levels to lowercase and removes the square brackets.

      .. code-block:: bash

         sed 's/\[\(.*\)\]/\1/' robots.log | awk '{$1 = tolower($1); print}'


.. dropdown:: Challenge -- Log Analyzer Script
   :icon: gear
   :class-container: sd-border-warning
   :class-title: sd-font-weight-bold

   Write a shell script called ``log_analyzer.sh`` that takes a log file as an argument and produces a summary report:

   1. Total number of lines.
   2. Count of each log level (``INFO``, ``WARN``, ``ERROR``, ``DEBUG``).
   3. List of unique robot names.
   4. Average speed (from lines containing ``speed:``).
   5. Any robots that appear in ``ERROR`` lines.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         #!/bin/bash

         if [ $# -ne 1 ]; then
             echo "Usage: $0 <logfile>"
             exit 1
         fi

         logfile="$1"

         echo "=== Log Analysis Report ==="
         echo "File: $logfile"
         echo "Total lines: $(wc -l < "$logfile")"
         echo ""

         echo "--- Log Level Counts ---"
         for level in INFO WARN ERROR DEBUG; do
             count=$(grep -c "\[$level\]" "$logfile")
             echo "  $level: $count"
         done
         echo ""

         echo "--- Unique Robots ---"
         awk '$2 == "Robot" {print $3}' "$logfile" | sort -u
         echo ""

         echo "--- Average Speed ---"
         grep "speed:" "$logfile" | awk '{sum += $5; n++} END {if (n > 0) printf "%.2f m/s\n", sum/n; else print "N/A"}'
         echo ""

         echo "--- Robots with Errors ---"
         grep "ERROR" "$logfile" | awk '$2 == "Robot" {print $3}' | sort -u

      Make the script executable with ``chmod +x log_analyzer.sh`` and run it:

      .. code-block:: bash

         ./log_analyzer.sh robots.log
