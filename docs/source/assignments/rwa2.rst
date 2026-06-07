====================================================
RWA2 -- STL Containers and Functions
====================================================

Overview
--------

In this assignment you **refactor RWA1** to replace raw arrays with STL
containers and extract repeated logic into well-designed functions. By
the end you will have a cleaner, safer codebase that no longer requires
manual ``new`` / ``delete`` calls --- demonstrating exactly *why* the
Standard Library exists.


Learning Objectives
-------------------

After completing this assignment you will be able to:

1. Use ``std::vector`` and ``std::array`` instead of raw C-style arrays.
2. Write functions with appropriate parameter passing (by value,
   by reference, by ``const`` reference).
3. Apply **function overloading** to provide multiple call signatures.
4. Use **iterators** and **range-based for loops** for container traversal.
5. Perform common ``std::string`` operations (``find``, ``substr``,
   ``insert``, ``erase``).
6. Document all functions with **Doxygen** comments.


Requirements
------------

.. dropdown:: R1 -- Replace Raw Arrays
   :open:

   Refactor every raw array from RWA1:

   * Convert the **part inventory** to ``std::vector<int>``.
   * Convert **sensor readings** to ``std::vector<double>``.
   * Use ``std::array`` for fixed-size data (e.g., a fixed number of
     aisles or a fixed set of robot IDs).
   * Demonstrate ``push_back``, ``emplace_back``, ``erase``, ``size``,
     and ``capacity``.

   .. code-block:: cpp

      std::vector<int> part_ids;
      part_ids.reserve(10);

      for (int i{0}; i < 10; ++i) {
          part_ids.push_back(1000 + i);
      }

      std::cout << "Size: " << part_ids.size()
                << "  Capacity: " << part_ids.capacity() << '\n';

      // Remove the third element
      part_ids.erase(part_ids.begin() + 2);

.. dropdown:: R2 -- Extract Functions
   :open:

   Move repeated or logically distinct blocks into functions:

   * ``print_warehouse_info()`` --- displays warehouse details.
   * ``add_robot()`` --- adds a robot to the collection.
   * ``remove_robot()`` --- removes a robot by ID.
   * ``update_robot_position()`` --- changes a robot's coordinates.

   Follow these parameter-passing guidelines:

   * **Pass by const reference** for read-only parameters.
   * **Pass by reference** for parameters that need modification.
   * **Return values** rather than modifying output parameters when
     practical.

   .. code-block:: cpp

      /**
       * @brief Print warehouse information to the console.
       * @param name  Warehouse name (read-only).
       * @param length  Warehouse length in meters.
       * @param width   Warehouse width in meters.
       * @param height  Warehouse height in meters.
       */
      void print_warehouse_info(const std::string& name,
                                double length,
                                double width,
                                double height) {
          std::cout << "Warehouse: " << name << '\n'
                    << "Dimensions: " << length << " x "
                    << width << " x " << height << '\n';
      }

.. dropdown:: R3 -- Function Overloading
   :open:

   Overload at least one function to accept different parameter types.
   A good candidate is ``find_robot``:

   * Find a robot **by ID** (``int``).
   * Find a robot **by name** (``const std::string&``).
   * Find a robot **by position** (``double x``, ``double y``).

   .. code-block:: cpp

      /**
       * @brief Find a robot by its unique ID.
       * @param robots  Vector of robots.
       * @param id      Robot ID to search for.
       * @return Index of the robot, or -1 if not found.
       */
      int find_robot(const std::vector<Robot>& robots, int id);

      /**
       * @brief Find a robot by its name.
       * @param robots  Vector of robots.
       * @param name    Robot name to search for.
       * @return Index of the robot, or -1 if not found.
       */
      int find_robot(const std::vector<Robot>& robots,
                     const std::string& name);

   .. note::

      At this stage ``Robot`` can be a simple ``struct`` --- full
      class design is deferred to RWA3.

.. dropdown:: R4 -- Iterators
   :open:

   * Use **iterators** (not index-based loops) to traverse containers
     in at least two places.
   * Use **range-based for loops** where appropriate.

   .. code-block:: cpp

      // Iterator-based traversal
      for (auto it{part_ids.begin()}; it != part_ids.end(); ++it) {
          std::cout << "Part: " << *it << '\n';
      }

      // Range-based for loop
      for (const auto& reading : temperature_readings) {
          std::cout << "Temp: " << reading << '\n';
      }

.. dropdown:: R5 -- String Operations
   :open:

   * Use ``std::string`` for robot names and part descriptions.
   * Demonstrate at least four of the following operations:
     ``insert``, ``erase``, ``find``, ``substr``, ``append``,
     ``replace``.

   .. code-block:: cpp

      std::string robot_name{"Scout_Alpha_01"};

      // find and substr
      auto pos{robot_name.find("Alpha")};
      if (pos != std::string::npos) {
          std::string model{robot_name.substr(pos, 5)};
          std::cout << "Model: " << model << '\n';
      }

      // insert
      robot_name.insert(0, "ENPM702_");

      // erase
      robot_name.erase(robot_name.size() - 3, 3);

.. dropdown:: R6 -- Documentation
   :open:

   Document **every** function with Doxygen-style comments:

   * ``@brief`` --- one-line summary.
   * ``@param`` --- description of each parameter.
   * ``@return`` --- description of the return value.

   .. code-block:: cpp

      /**
       * @brief Update the position of a robot.
       * @param x  Reference to the robot's x-coordinate.
       * @param y  Reference to the robot's y-coordinate.
       * @param dx Displacement in x.
       * @param dy Displacement in y.
       */
      void update_robot_position(double& x, double& y,
                                 double dx, double dy) {
          x += dx;
          y += dy;
      }


Deliverables
------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Item
     - Description
   * - Header files (``.hpp``)
     - Declarations for all functions and structs.
   * - Source files (``.cpp``)
     - Implementations and ``main.cpp``.
   * - ``CMakeLists.txt``
     - Build configuration targeting C++17 or later.
   * - Doxygen output
     - Generated HTML documentation (or a ``Doxyfile`` that produces it).


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Category
     - Weight
     - Criteria
   * - Correctness
     - 35 %
     - Program compiles, runs, and produces correct output.
   * - Function Design
     - 25 %
     - Proper parameter passing, clear interfaces, no unnecessary
       globals.
   * - STL Usage
     - 20 %
     - Effective use of ``std::vector``, ``std::array``, ``std::string``,
       and iterators.
   * - Documentation
     - 20 %
     - Complete Doxygen comments on every function; readable code.


Tips
----

.. admonition:: Refactor Incrementally
   :class: tip

   Start by copying your RWA1 code. Replace one raw array at a time
   and verify the output still matches before moving on.

.. admonition:: Compile Often
   :class: tip

   Each time you extract a function, compile and test immediately.
   Small, frequent compilations catch errors early.

.. admonition:: Parameter Passing Rule of Thumb
   :class: tip

   * **Cheap to copy** (``int``, ``double``, ``bool``) --- pass by value.
   * **Expensive to copy** and read-only --- pass by ``const`` reference.
   * **Needs modification** --- pass by reference.
