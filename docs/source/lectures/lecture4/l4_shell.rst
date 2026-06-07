.. _l4_shell:

================
Shell Exercises
================

.. contents:: Table of Contents
   :depth: 2
   :local:

These exercises build on the shell skills from Lectures 1--3 and introduce new tools for text processing, file comparison, archiving, and shell scripting.

Exercise 1: xargs
-------------------

``xargs`` reads items from standard input and passes them as arguments to a specified command. This is useful when you need to pass the output of one command as arguments (not input) to another.

.. code-block:: bash

   # Find all .cpp files and count lines in each
   find . -name "*.cpp" | xargs wc -l

   # Remove all .o files found by find
   find . -name "*.o" | xargs rm -f

   # Using -I {} to place the argument at a specific position
   find . -name "*.txt" | xargs -I {} cp {} /tmp/backup/

**Tasks:**

1. Use ``find`` and ``xargs`` to list all ``.rst`` files in your home directory and print the first 3 lines of each file.
2. Create 5 files named ``file1.txt`` through ``file5.txt``. Use ``ls`` and ``xargs`` to print their sizes with ``du -h``.
3. Use ``echo`` with ``xargs -n 1`` to print each word on a separate line: ``echo "alpha beta gamma delta" | xargs -n 1``.

Exercise 2: tee
-----------------

``tee`` reads from standard input and writes to both standard output **and** one or more files simultaneously. This is useful for logging output while still seeing it in the terminal.

.. code-block:: bash

   # Write output to file and display it
   echo "Build started" | tee build.log

   # Append to file instead of overwriting
   echo "Step 2 complete" | tee -a build.log

   # Write to multiple files
   ls -la | tee listing1.txt listing2.txt

**Tasks:**

1. Run ``date`` and use ``tee`` to save the output to ``timestamp.txt`` while also displaying it.
2. Run ``ls -la /usr/bin`` piped through ``tee`` to save the full listing to ``usr_bin.txt``, then pipe the tee output to ``wc -l`` to count the lines.
3. Create a simple build script that runs ``g++ main.cpp -o main 2>&1 | tee build.log`` and captures both stdout and stderr.

Exercise 3: diff and comm
---------------------------

``diff`` compares two files line by line and shows the differences. ``comm`` compares two **sorted** files and shows lines unique to each file and lines common to both.

.. code-block:: bash

   # diff -- shows what changed between two files
   diff file1.txt file2.txt

   # Unified format (more readable)
   diff -u file1.txt file2.txt

   # comm -- requires sorted input
   # Column 1: lines only in file1
   # Column 2: lines only in file2
   # Column 3: lines in both
   comm <(sort file1.txt) <(sort file2.txt)

   # Show only common lines
   comm -12 <(sort file1.txt) <(sort file2.txt)

**Tasks:**

1. Create two files with overlapping content. Use ``diff`` and ``diff -u`` to compare them.
2. Use ``comm`` to find lines that are common to both files and lines unique to each.
3. Compare the output of ``ls /usr/bin`` and ``ls /usr/local/bin`` using ``comm`` to find commands available in both locations.

Exercise 4: tar and zip
-------------------------

``tar`` bundles multiple files into a single archive. Combined with compression (``gzip``, ``bzip2``), it creates compressed archives. ``zip`` creates compressed archives compatible with most operating systems.

.. code-block:: bash

   # Create a tar archive
   tar -cf archive.tar file1.txt file2.txt dir/

   # Create a compressed tar.gz archive
   tar -czf archive.tar.gz file1.txt file2.txt dir/

   # Extract a tar.gz archive
   tar -xzf archive.tar.gz

   # List contents of an archive
   tar -tzf archive.tar.gz

   # zip and unzip
   zip archive.zip file1.txt file2.txt
   zip -r archive.zip directory/
   unzip archive.zip

**Tasks:**

1. Create a directory with several files. Archive it using ``tar -czf`` and verify the contents with ``tar -tzf``.
2. Extract the archive to a different directory using ``tar -xzf -C /path/to/dest``.
3. Create a ``zip`` archive containing all ``.cpp`` files in a directory. Unzip it to a new location and verify.

Exercise 5: Here Documents (Heredoc)
--------------------------------------

A **here document** (heredoc) allows you to pass multiple lines of input to a command. The syntax uses ``<<DELIMITER`` to start and ``DELIMITER`` on its own line to end.

.. code-block:: bash

   # Write multiple lines to a file
   cat << 'EOF' > config.txt
   hostname=myserver
   port=8080
   debug=false
   EOF

   # Pass multi-line input to a command
   grep "port" << EOF
   hostname=myserver
   port=8080
   debug=false
   EOF

   # Use with variable expansion (no quotes around delimiter)
   NAME="Alice"
   cat << EOF
   Hello, $NAME!
   Today is $(date).
   EOF

**Tasks:**

1. Use a heredoc to write a 5-line poem to a file called ``poem.txt``.
2. Use a heredoc with variable expansion to generate a personalized greeting (define a ``NAME`` variable and reference it).
3. Use a heredoc to create a simple HTML file with a title and body paragraph.

Exercise 6: Shell Arrays and Loops
------------------------------------

Bash supports one-dimensional indexed arrays. You can iterate over arrays using ``for`` loops.

.. code-block:: bash

   # Declare an array
   fruits=("apple" "banana" "cherry" "date")

   # Access elements (0-indexed)
   echo "${fruits[0]}"   # apple
   echo "${fruits[2]}"   # cherry

   # All elements
   echo "${fruits[@]}"

   # Number of elements
   echo "${#fruits[@]}"  # 4

   # Loop over array elements
   for fruit in "${fruits[@]}"; do
       echo "Fruit: $fruit"
   done

   # Loop with index
   for i in "${!fruits[@]}"; do
       echo "Index $i: ${fruits[$i]}"
   done

   # Add an element
   fruits+=("elderberry")

**Tasks:**

1. Create an array of 5 programming languages. Print each language with its index.
2. Write a script that takes directory names as array elements and creates each directory if it does not already exist.
3. Create an array of filenames. Loop through the array and report whether each file exists (``-f``) or not.

Exercise 7: Combining Tools
-----------------------------

Combine the tools from this lecture to solve more complex tasks.

**Tasks:**

1. Find all ``.cpp`` files in a project directory, use ``xargs`` to run ``wc -l`` on each, and use ``tee`` to save the results to ``line_counts.txt`` while displaying them.
2. Create two directories with some overlapping files. Use ``diff -rq`` to compare the directories and save the report using ``tee``.
3. Write a script that archives all ``.log`` files older than 7 days into a dated ``tar.gz`` file, then deletes the originals.

Exercise 8: Challenge -- C++ Project Scaffold
-----------------------------------------------

Write a shell script called ``create_project.sh`` that creates a complete C++ project scaffold. The script should:

1. Accept a project name as a command-line argument.
2. Create the following directory structure:

   .. code-block:: text

      project_name/
      ├── CMakeLists.txt
      ├── src/
      │   └── main.cpp
      ├── include/
      │   └── project_name/
      ├── tests/
      └── build/

3. Use a heredoc to generate a ``CMakeLists.txt`` with:

   .. code-block:: cmake

      cmake_minimum_required(VERSION 3.16)
      project(PROJECT_NAME)

      set(CMAKE_CXX_STANDARD 17)
      set(CMAKE_CXX_STANDARD_REQUIRED ON)

      add_executable(PROJECT_NAME src/main.cpp)
      target_include_directories(PROJECT_NAME PRIVATE include)

   Replace ``PROJECT_NAME`` with the actual project name.

4. Use a heredoc to generate a ``main.cpp``:

   .. code-block:: cpp

      #include <iostream>

      int main() {
          std::cout << "Hello from PROJECT_NAME!\n";
          return 0;
      }

5. Print a summary of created files using ``find`` and ``tee``.

**Hints:**

- Use ``$1`` to access the first command-line argument.
- Use ``mkdir -p`` to create nested directories.
- Use ``sed`` or variable substitution to replace ``PROJECT_NAME`` in the heredoc output.
