.. _l3-shell:

================
Shell Exercises
================

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
========

In Lecture 1, we covered basic navigation, file operations, aliases, functions, and pipes. In Lecture 2, we explored environment variables, permissions, ``find``/``grep``, process management, and shell scripting fundamentals.

In this lecture, we focus on **text processing tools**, **sed and awk basics**, **combining tools in pipelines**, and writing **shell scripts with arguments and loops**. We also write a script that integrates with Valgrind for memory leak detection.

Exercise 1: Text Processing with ``cut``
==========================================

The ``cut`` command extracts specific columns or fields from text.

Create a file called ``students.csv`` with the following content:

.. code-block:: text

   Name,Major,GPA
   Alice,ENPM,3.8
   Bob,ENSE,3.5
   Charlie,ENPM,3.9
   Diana,ENME,3.2
   Eve,ENPM,3.7

Perform the following tasks:

1. Extract only the **Name** column (field 1) using ``cut``:

   .. code-block:: bash

      cut -d',' -f1 students.csv

2. Extract the **Name** and **GPA** columns (fields 1 and 3):

   .. code-block:: bash

      cut -d',' -f1,3 students.csv

3. Extract everything **except** the Major column:

   .. code-block:: bash

      cut -d',' -f1,3 students.csv

Exercise 2: Sorting and Counting with ``sort``, ``uniq``, and ``wc``
======================================================================

Using the same ``students.csv`` file:

1. Extract the Major column and sort it alphabetically:

   .. code-block:: bash

      cut -d',' -f2 students.csv | tail -n +2 | sort

2. Count how many students are in each major:

   .. code-block:: bash

      cut -d',' -f2 students.csv | tail -n +2 | sort | uniq -c | sort -rn

3. Count the total number of students (excluding the header):

   .. code-block:: bash

      tail -n +2 students.csv | wc -l

4. Find the student with the highest GPA using ``sort``:

   .. code-block:: bash

      tail -n +2 students.csv | sort -t',' -k3 -rn | head -1

Exercise 3: Basic ``sed`` Usage
================================

``sed`` (stream editor) performs text transformations on input streams or files.

1. Replace all occurrences of ``ENPM`` with ``Engineering-PM`` in the file:

   .. code-block:: bash

      sed 's/ENPM/Engineering-PM/g' students.csv

2. Replace only the **first** occurrence of ``ENPM`` per line:

   .. code-block:: bash

      sed 's/ENPM/Engineering-PM/' students.csv

3. Delete the header line:

   .. code-block:: bash

      sed '1d' students.csv

4. Edit the file **in place** (modify the actual file) -- add a ``-i`` flag:

   .. code-block:: bash

      sed -i 's/ENME/Mechanical-E/g' students.csv

5. Insert a new line after the header:

   .. code-block:: bash

      sed '1a Frank,ENSE,3.6' students.csv

Exercise 4: Basic ``awk`` Usage
================================

``awk`` is a powerful text-processing language that works on columns (fields).

1. Print the Name and GPA columns (fields 1 and 3):

   .. code-block:: bash

      awk -F',' '{print $1, $3}' students.csv

2. Print only students with a GPA above 3.6 (skip the header):

   .. code-block:: bash

      awk -F',' 'NR > 1 && $3 > 3.6 {print $1, $3}' students.csv

3. Calculate the average GPA:

   .. code-block:: bash

      awk -F',' 'NR > 1 {sum += $3; count++} END {print "Average GPA:", sum/count}' students.csv

4. Print line numbers alongside each line:

   .. code-block:: bash

      awk '{print NR": "$0}' students.csv

Exercise 5: Combining Tools in Pipelines
==========================================

Pipelines chain multiple commands together. Each command's output becomes the next command's input.

1. Find all ENPM students and display only their names, sorted alphabetically:

   .. code-block:: bash

      grep 'ENPM' students.csv | cut -d',' -f1 | sort

2. Count how many unique majors exist:

   .. code-block:: bash

      tail -n +2 students.csv | cut -d',' -f2 | sort -u | wc -l

3. Find the names of students with GPA >= 3.7 and format the output:

   .. code-block:: bash

      awk -F',' 'NR > 1 && $3 >= 3.7 {print $1": "$3}' students.csv | sort -t':' -k2 -rn

4. Generate a summary report:

   .. code-block:: bash

      echo "=== Student Report ===" && \
      echo "Total students: $(tail -n +2 students.csv | wc -l)" && \
      echo "Unique majors: $(tail -n +2 students.csv | cut -d',' -f2 | sort -u | wc -l)" && \
      echo "Highest GPA: $(tail -n +2 students.csv | sort -t',' -k3 -rn | head -1 | cut -d',' -f1,3)"

Exercise 6: Shell Script with Arguments and Loops
===================================================

Create a script called ``process_csv.sh`` that accepts a CSV filename as an argument and performs basic analysis.

.. code-block:: bash

   #!/bin/bash

   # Check if a filename was provided
   if [ $# -ne 1 ]; then
       echo "Usage: $0 <csv_file>"
       exit 1
   fi

   file="$1"

   # Check if the file exists
   if [ ! -f "$file" ]; then
       echo "Error: File '$file' not found."
       exit 1
   fi

   echo "=== Processing: $file ==="
   echo ""

   # Count total records (excluding header)
   total=$(tail -n +2 "$file" | wc -l)
   echo "Total records: $total"

   # Get column headers
   headers=$(head -1 "$file")
   echo "Columns: $headers"
   echo ""

   # Loop through each unique value in column 2
   echo "--- Breakdown by Column 2 ---"
   tail -n +2 "$file" | cut -d',' -f2 | sort -u | while read -r category; do
       count=$(grep -c ",$category," "$file")
       echo "  $category: $count"
   done

Tasks:

1. Make the script executable: ``chmod +x process_csv.sh``
2. Run it: ``./process_csv.sh students.csv``
3. Test error handling by running it without arguments or with a non-existent file.

Exercise 7: Looping Over Files
================================

Create a script called ``batch_process.sh`` that processes all ``.csv`` files in a directory:

.. code-block:: bash

   #!/bin/bash

   target_dir="${1:-.}"  # default to current directory

   csv_count=0

   for file in "$target_dir"/*.csv; do
       # Check if the glob matched any files
       if [ ! -f "$file" ]; then
           echo "No CSV files found in $target_dir"
           exit 0
       fi

       csv_count=$((csv_count + 1))
       echo "=== File: $(basename "$file") ==="
       echo "  Lines: $(wc -l < "$file")"
       echo "  Size:  $(du -h "$file" | cut -f1)"
       echo "  First line: $(head -1 "$file")"
       echo ""
   done

   echo "Total CSV files processed: $csv_count"

Tasks:

1. Create several sample CSV files in a directory.
2. Run the script on that directory.
3. Modify the script to also show the last line of each file.

Exercise 8: Valgrind Memory Leak Checker Script (Challenge)
=============================================================

Write a shell script called ``check_leaks.sh`` that compiles and runs a C++ program through Valgrind, then reports whether memory leaks were found.

.. code-block:: bash

   #!/bin/bash

   # Usage: ./check_leaks.sh <source_file.cpp>

   if [ $# -ne 1 ]; then
       echo "Usage: $0 <source_file.cpp>"
       exit 1
   fi

   source_file="$1"
   executable="${source_file%.cpp}"

   # Check if source file exists
   if [ ! -f "$source_file" ]; then
       echo "Error: Source file '$source_file' not found."
       exit 1
   fi

   # Check if Valgrind is installed
   if ! command -v valgrind &> /dev/null; then
       echo "Error: Valgrind is not installed. Install with: sudo apt install valgrind"
       exit 1
   fi

   # Compile with debug symbols
   echo "Compiling $source_file..."
   g++ -g -std=c++17 -o "$executable" "$source_file"

   if [ $? -ne 0 ]; then
       echo "Compilation failed."
       exit 1
   fi

   echo "Running Valgrind..."
   echo ""

   # Run Valgrind and capture output
   valgrind_output=$(valgrind --leak-check=full --error-exitcode=1 "./$executable" 2>&1)
   valgrind_exit=$?

   echo "$valgrind_output"
   echo ""
   echo "==============================="

   # Check for leaks in the output
   if echo "$valgrind_output" | grep -q "no leaks are possible"; then
       echo "RESULT: No memory leaks detected."
   elif echo "$valgrind_output" | grep -q "definitely lost: 0 bytes"; then
       echo "RESULT: No definite memory leaks detected."
   else
       echo "RESULT: Memory leaks detected! Review the Valgrind output above."
   fi

   # Cleanup
   rm -f "$executable"

Tasks:

1. Create a C++ file with a deliberate memory leak (e.g., ``new`` without ``delete``).
2. Run ``./check_leaks.sh leaky_program.cpp`` and verify it detects the leak.
3. Fix the leak and re-run to confirm no leaks.
4. Modify the script to also detect **invalid memory access** errors.
