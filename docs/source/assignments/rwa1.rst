====================================================
RWA1 -- C++ Fundamentals
====================================================

Overview
--------

In this assignment you build a simple **warehouse robot environment
simulator** in pure C++. This first version uses basic types, pointers,
and references to model robots, parts, and sensor readings inside a
warehouse setting. There is no object-oriented design yet --- the goal
is to practise foundational C++ constructs before refactoring in later
assignments.


Learning Objectives
-------------------

After completing this assignment you will be able to:

1. Apply variables, types, and constants in a practical context.
2. Use pointers and references to manage relationships between objects.
3. Practice dynamic memory allocation with ``new`` / ``delete``.
4. Use **Valgrind** to verify that your program has no memory leaks.
5. Follow ``snake_case`` naming and uniform initialization conventions.
6. Produce formatted console output with ``'\n'`` (not ``std::endl``).


Requirements
------------

.. dropdown:: R1 -- Warehouse Environment
   :open:

   Create variables that represent a warehouse:

   * ``length``, ``width``, ``height`` --- ``double`` values for dimensions.
   * ``warehouse_name`` --- ``std::string``.
   * ``num_aisles`` --- ``int``.
   * Use ``constexpr`` for fixed values such as maximum capacity.

   .. code-block:: cpp

      constexpr int max_capacity{500};
      std::string warehouse_name{"Main Distribution Center"};
      double length{120.0};
      double width{80.0};
      double height{12.5};
      int num_aisles{10};

.. dropdown:: R2 -- Robot Representation
   :open:

   Model a robot using individual variables:

   * ``robot_id`` (``int``)
   * ``x_position``, ``y_position`` (``double``)
   * ``battery_level`` (``double``, range 0--100)
   * ``is_active`` (``bool``)

   Create **at least three** robots with distinct values.

   .. code-block:: cpp

      // Robot 1
      int robot1_id{1};
      double robot1_x{0.0};
      double robot1_y{0.0};
      double robot1_battery{100.0};
      bool robot1_active{true};

.. dropdown:: R3 -- Sensor Data
   :open:

   * Create C-style arrays of sensor readings for **temperature** and
     **humidity** (at least 5 elements each).
   * Use **pointers** to access and modify sensor data.
   * Demonstrate **pointer arithmetic** to traverse the array.

   .. code-block:: cpp

      double temperature_readings[5]{22.1, 23.4, 21.8, 24.0, 22.5};
      double* temp_ptr{temperature_readings};

      // Traverse with pointer arithmetic
      for (int i{0}; i < 5; ++i) {
          std::cout << "Sensor " << i << ": " << *(temp_ptr + i) << '\n';
      }

.. dropdown:: R4 -- Part Inventory
   :open:

   * Dynamically allocate an array of part IDs (``int``) using ``new``.
   * Fill the array with sequential IDs.
   * Print all parts.
   * **Resize** the array: allocate a larger array, copy existing data,
     delete the old array, and reassign the pointer.
   * Free **all** dynamically allocated memory before the program ends.

   .. code-block:: cpp

      int initial_size{5};
      int* part_ids{new int[initial_size]};

      // Fill with sequential IDs
      for (int i{0}; i < initial_size; ++i) {
          part_ids[i] = 1000 + i;
      }

      // Resize to a larger array
      int new_size{10};
      int* new_part_ids{new int[new_size]};
      for (int i{0}; i < initial_size; ++i) {
          new_part_ids[i] = part_ids[i];
      }
      delete[] part_ids;
      part_ids = new_part_ids;

      // ... use part_ids ...
      delete[] part_ids;

.. dropdown:: R5 -- References
   :open:

   * Create **reference variables** to robot positions.
   * Modify robot positions through references.
   * Demonstrate that changes through references affect the original
     variables.

   .. code-block:: cpp

      double& ref_x{robot1_x};
      double& ref_y{robot1_y};

      ref_x = 15.5;
      ref_y = 30.2;

      // robot1_x is now 15.5, robot1_y is now 30.2
      std::cout << "Robot 1 position: ("
                << robot1_x << ", " << robot1_y << ")\n";

.. dropdown:: R6 -- Output
   :open:

   Print a **formatted report** to the console that includes:

   * Warehouse information (name, dimensions, aisles, capacity).
   * All robot statuses (ID, position, battery, active/inactive).
   * All sensor readings (temperature and humidity).
   * Full part inventory.

   Use ``'\n'`` for newlines --- do **not** use ``std::endl``.


Deliverables
------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Item
     - Description
   * - ``main.cpp``
     - Single source file containing all code.
   * - ``CMakeLists.txt``
     - Build configuration targeting C++17 or later.
   * - Valgrind output
     - Screenshot or text showing **no memory leaks**.
   * - ``README.md``
     - Build and run instructions.


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Category
     - Weight
     - Criteria
   * - Correctness
     - 40 %
     - Program compiles, runs, and produces the required output.
   * - Memory Management
     - 25 %
     - All dynamic memory is properly freed; Valgrind reports zero leaks.
   * - Code Quality
     - 20 %
     - Uniform initialization, ``snake_case`` naming, ``'\n'`` usage, clear
       variable names.
   * - Documentation
     - 15 %
     - README with build instructions; inline comments explaining
       pointer/reference usage.


Tips
----

.. admonition:: Start Early
   :class: tip

   Begin with the warehouse variables and robot representations.
   Add dynamic allocation last so you can focus on getting Valgrind
   clean before the deadline.

.. admonition:: Use Valgrind Frequently
   :class: tip

   Run ``valgrind --leak-check=full ./your_program`` after every
   change that involves ``new`` or ``delete``. Fixing leaks early is
   far easier than debugging them the night before the deadline.

.. admonition:: Follow the Conventions
   :class: tip

   * Use **uniform initialization**: ``int a{1};`` not ``int a = 1;``
   * Use **snake_case**: ``battery_level`` not ``batteryLevel``
   * Use ``'\n'`` instead of ``std::endl``
