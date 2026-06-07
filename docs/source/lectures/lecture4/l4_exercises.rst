====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 4: STL
Containers. Work through them in order, as each exercise builds on
the skills from the previous one.

.. note::

   Compile all programs with warnings enabled:

   .. code-block:: bash

      g++ -std=c++17 -Wall -Wextra -o program program.cpp


----


.. dropdown:: Exercise 1 -- String Operations
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Demonstrate key ``std::string`` operations and observe Small String
    Optimization (SSO).

    **Specification**

    1. Create a short string (fewer than 15 characters) and a long string
       (more than 30 characters).
    2. Print the ``size()`` and ``capacity()`` of each string. Observe the
       difference caused by SSO.
    3. Use ``.insert()`` to insert ``"C++ "`` at the beginning of a string.
    4. Use ``.erase()`` to remove the first 4 characters from a string.
    5. Use ``.append()`` to add ``" is great!"`` to the end.
    6. Use ``.at()`` to access a character. Then try accessing an out-of-bounds
       index and observe the exception.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>
           #include <string>

           int main() {
               // Short string (likely uses SSO)
               std::string short_str{"Hello"};
               std::cout << "Short string: '" << short_str << "'\n";
               std::cout << "  Size: " << short_str.size() << '\n';
               std::cout << "  Capacity: " << short_str.capacity() << '\n';

               // Long string (likely uses heap allocation)
               std::string long_str{"This is a much longer string for testing"};
               std::cout << "Long string: '" << long_str << "'\n";
               std::cout << "  Size: " << long_str.size() << '\n';
               std::cout << "  Capacity: " << long_str.capacity() << '\n';

               // Insert
               std::string language{"rocks"};
               language.insert(0, "C++ ");
               std::cout << "After insert: " << language << '\n';

               // Erase
               std::string text{"Hello World"};
               text.erase(0, 6);
               std::cout << "After erase: " << text << '\n';

               // Append
               text.append(" is great!");
               std::cout << "After append: " << text << '\n';

               // Safe access with .at()
               std::cout << "Character at index 0: " << text.at(0) << '\n';

               return 0;
           }


.. dropdown:: Exercise 2 -- Array Manipulation
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Demonstrate both C-style arrays and ``std::array``.

    **Specification**

    1. Declare a C-style array of 5 integers and initialize it with values.
    2. Declare a ``std::array<int, 5>`` and initialize it with different values.
    3. Use ``.fill()`` to set all elements of the ``std::array`` to a single value.
    4. Access elements using ``[]`` and ``.at()``.
    5. Use a range-based for loop to print all elements.
    6. Print ``.size()`` and ``.empty()`` for the ``std::array``.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <array>
           #include <iostream>

           int main() {
               // C-style array
               int c_arr[5]{10, 20, 30, 40, 50};
               std::cout << "C-style array: ";
               for (int i{0}; i < 5; ++i) {
                   std::cout << c_arr[i] << ' ';
               }
               std::cout << '\n';

               // std::array
               std::array<int, 5> std_arr{100, 200, 300, 400, 500};
               std::cout << "std::array: ";
               for (const auto& val : std_arr) {
                   std::cout << val << ' ';
               }
               std::cout << '\n';

               // Fill
               std_arr.fill(42);
               std::cout << "After fill(42): ";
               for (const auto& val : std_arr) {
                   std::cout << val << ' ';
               }
               std::cout << '\n';

               // Access
               std_arr = {5, 10, 15, 20, 25};
               std::cout << "Element [2]: " << std_arr[2] << '\n';
               std::cout << "Element .at(2): " << std_arr.at(2) << '\n';
               std::cout << "Size: " << std_arr.size() << '\n';
               std::cout << "Empty: " << std_arr.empty() << '\n';

               return 0;
           }


.. dropdown:: Exercise 3 -- 2D Array
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create a 3x3 matrix using ``std::array``, fill it with values, and
    print it row by row.

    **Specification**

    1. Declare a 2D ``std::array`` of size 3x3.
    2. Fill the matrix with values 1 through 9
       (``row * 3 + col + 1``).
    3. Print the matrix in a grid format.
    4. Calculate and print the sum of each row.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <array>
           #include <iostream>

           int main() {
               std::array<std::array<int, 3>, 3> matrix{};

               // Fill with values 1-9
               int value{1};
               for (size_t row{0}; row < 3; ++row) {
                   for (size_t col{0}; col < 3; ++col) {
                       matrix.at(row).at(col) = value;
                       ++value;
                   }
               }

               // Print the matrix
               std::cout << "Matrix:\n";
               for (const auto& row : matrix) {
                   for (const auto& elem : row) {
                       std::cout << elem << '\t';
                   }
                   std::cout << '\n';
               }

               // Sum of each row
               for (size_t row{0}; row < 3; ++row) {
                   int row_sum{0};
                   for (const auto& elem : matrix.at(row)) {
                       row_sum += elem;
                   }
                   std::cout << "Sum of row " << row << ": " << row_sum << '\n';
               }

               return 0;
           }


.. dropdown:: Exercise 4 -- Vector Basics
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Demonstrate basic ``std::vector`` operations.

    **Specification**

    1. Create a vector of integers with initial values ``{10, 20, 30}``.
    2. Use ``push_back()`` to add 40 and 50. Print size and capacity
       after each ``push_back()``.
    3. Use ``pop_back()`` to remove the last element.
    4. Use ``front()``, ``back()``, ``[]``, and ``.at()`` to access elements.
    5. Use a range-based for loop to print all elements.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>
           #include <vector>

           int main() {
               std::vector<int> vec{10, 20, 30};
               std::cout << "Initial - Size: " << vec.size()
                         << ", Capacity: " << vec.capacity() << '\n';

               vec.push_back(40);
               std::cout << "After push_back(40) - Size: " << vec.size()
                         << ", Capacity: " << vec.capacity() << '\n';

               vec.push_back(50);
               std::cout << "After push_back(50) - Size: " << vec.size()
                         << ", Capacity: " << vec.capacity() << '\n';

               vec.pop_back();
               std::cout << "After pop_back() - Size: " << vec.size()
                         << ", Capacity: " << vec.capacity() << '\n';

               std::cout << "Front: " << vec.front() << '\n';
               std::cout << "Back: " << vec.back() << '\n';
               std::cout << "vec[1]: " << vec[1] << '\n';
               std::cout << "vec.at(2): " << vec.at(2) << '\n';

               std::cout << "All elements: ";
               for (const auto& val : vec) {
                   std::cout << val << ' ';
               }
               std::cout << '\n';

               return 0;
           }


.. dropdown:: Exercise 5 -- Vector Memory
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Demonstrate how vector capacity grows dynamically and how to manage
    memory with ``reserve()``, ``resize()``, and ``shrink_to_fit()``.

    **Specification**

    1. Start with an empty vector.
    2. In a loop, ``push_back()`` integers from 0 to 31. Print size and
       capacity each time the capacity changes.
    3. After the loop, use ``reserve(100)`` and print size and capacity.
    4. Use ``shrink_to_fit()`` and print size and capacity.
    5. Use ``resize(10)`` then ``shrink_to_fit()`` again.
    6. Observe the pattern of capacity growth (typically doubles).

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>
           #include <vector>

           int main() {
               std::vector<int> vec{};

               std::cout << "=== Capacity Growth ===\n";
               std::cout << "Initial - Size: " << vec.size()
                         << ", Capacity: " << vec.capacity() << '\n';

               for (int i{0}; i < 32; ++i) {
                   size_t old_capacity{vec.capacity()};
                   vec.push_back(i);
                   if (vec.capacity() != old_capacity) {
                       std::cout << "Size: " << vec.size()
                                 << ", Capacity changed: " << old_capacity
                                 << " -> " << vec.capacity() << '\n';
                   }
               }

               std::cout << "\nFinal - Size: " << vec.size()
                         << ", Capacity: " << vec.capacity() << '\n';

               vec.reserve(100);
               std::cout << "\nAfter reserve(100) - Size: " << vec.size()
                         << ", Capacity: " << vec.capacity() << '\n';

               vec.shrink_to_fit();
               std::cout << "After shrink_to_fit() - Size: " << vec.size()
                         << ", Capacity: " << vec.capacity() << '\n';

               vec.resize(10);
               std::cout << "After resize(10) - Size: " << vec.size()
                         << ", Capacity: " << vec.capacity() << '\n';

               vec.shrink_to_fit();
               std::cout << "After shrink_to_fit() - Size: " << vec.size()
                         << ", Capacity: " << vec.capacity() << '\n';

               return 0;
           }


.. dropdown:: Exercise 6 -- Simple Gradebook (Challenge)
    :icon: gear
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Implement a simple gradebook using vectors and strings with iterator
    traversal.

    **Specification**

    1. Store student names in a ``std::vector<std::string>``.
    2. Store each student's grades in a ``std::vector<std::vector<int>>``.
    3. Add at least 3 students with 4 grades each.
    4. Calculate and display the average grade for each student.
    5. Use iterators (not index-based loops) to traverse the containers.
    6. Find and display the student with the highest average.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>
           #include <string>
           #include <vector>

           int main() {
               std::vector<std::string> names{"Alice", "Bob", "Charlie"};

               std::vector<std::vector<int>> grades{
                   {92, 85, 88, 95},
                   {78, 82, 90, 73},
                   {95, 98, 92, 97}
               };

               std::cout << "=== Gradebook ===\n";
               std::vector<double> averages{};

               auto name_it = names.begin();
               auto grade_it = grades.begin();

               while (name_it != names.end()) {
                   int sum{0};
                   for (auto it = grade_it->begin(); it != grade_it->end(); ++it) {
                       sum += *it;
                   }
                   double avg{static_cast<double>(sum) / static_cast<double>(grade_it->size())};
                   averages.push_back(avg);

                   std::cout << *name_it << ": ";
                   for (auto it = grade_it->begin(); it != grade_it->end(); ++it) {
                       std::cout << *it << ' ';
                   }
                   std::cout << "-> Average: " << avg << '\n';

                   ++name_it;
                   ++grade_it;
               }

               double highest_avg{0.0};
               std::string top_student{};
               auto avg_it = averages.begin();
               auto n_it = names.begin();
               while (avg_it != averages.end()) {
                   if (*avg_it > highest_avg) {
                       highest_avg = *avg_it;
                       top_student = *n_it;
                   }
                   ++avg_it;
                   ++n_it;
               }

               std::cout << "\nTop student: " << top_student
                         << " with average " << highest_avg << '\n';

               return 0;
           }
