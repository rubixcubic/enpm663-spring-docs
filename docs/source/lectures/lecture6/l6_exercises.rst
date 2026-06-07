====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 6: Functions --
Advanced. Work through them in order, as each exercise builds on the
skills from the previous one.

.. note::

   Compile all programs with warnings enabled:

   .. code-block:: bash

      g++ -std=c++17 -Wall -Wextra -o program program.cpp


----


.. dropdown:: Exercise 1 -- Struct Usage
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Demonstrate ``struct`` with aggregate initialization and structured bindings.

   **Specification**

   1. Define a ``struct Sensor`` with fields: ``std::string name``, ``double reading``, and ``bool is_active`` (with a default value of ``true``).
   2. Create three ``Sensor`` instances using aggregate initialization.
   3. Write a function ``print_sensor`` that takes a ``const Sensor&`` and prints all fields.
   4. Use structured bindings (``auto [name, reading, active] = ...``) to decompose one sensor and print its fields individually.
   5. Use a reference structured binding (``auto& [...]``) to modify a sensor's reading and verify the change.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: cpp

         #include <iostream>
         #include <string>

         struct Sensor {
             std::string name;
             double reading;
             bool is_active{true};
         };

         void print_sensor(const Sensor& s) {
             std::cout << "Name: " << s.name
                       << ", Reading: " << s.reading
                       << ", Active: " << (s.is_active ? "yes" : "no") << '\n';
         }

         int main() {
             // Aggregate initialization
             Sensor s1{"Lidar", 42.5, true};
             Sensor s2{"Camera", 30.0};       // is_active defaults to true
             Sensor s3{"IMU", 9.81, false};

             print_sensor(s1);
             print_sensor(s2);
             print_sensor(s3);

             // Structured bindings (by value)
             auto [name, reading, active] = s1;
             std::cout << "Decomposed: " << name << " " << reading << " " << active << '\n';

             // Structured bindings (by reference)
             auto& [name_ref, reading_ref, active_ref] = s2;
             reading_ref = 55.0;
             std::cout << "Modified s2 reading: " << s2.reading << '\n'; // 55.0

             return 0;
         }


.. dropdown:: Exercise 2 -- Function Templates
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Write a set of function templates that perform common operations.

   **Specification**

   1. Write a function template ``clamp(T value, T low, T high)`` that returns ``value`` constrained to the range ``[low, high]``.
   2. Write a function template ``swap_values(T& a, T& b)`` that swaps two values using a temporary.
   3. Write a function template with two type parameters ``auto convert_and_add(T a, U b)`` that adds two values of possibly different types.
   4. Test all three templates with ``int``, ``double``, and (for ``clamp`` and ``swap_values``) ``char``.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: cpp

         #include <iostream>
         #include <string>

         template<typename T>
         T clamp(T value, T low, T high) {
             if (value < low) return low;
             if (value > high) return high;
             return value;
         }

         template<typename T>
         void swap_values(T& a, T& b) {
             T temp{a};
             a = b;
             b = temp;
         }

         template<typename T, typename U>
         auto convert_and_add(T a, U b) {
             return a + b;
         }

         int main() {
             // clamp
             std::cout << clamp(15, 0, 10) << '\n';       // 10
             std::cout << clamp(3.14, 0.0, 2.0) << '\n';  // 2.0
             std::cout << clamp('z', 'a', 'm') << '\n';   // m

             // swap_values
             int x{10}, y{20};
             swap_values(x, y);
             std::cout << "x=" << x << " y=" << y << '\n'; // x=20 y=10

             double a{1.1}, b{2.2};
             swap_values(a, b);
             std::cout << "a=" << a << " b=" << b << '\n'; // a=2.2 b=1.1

             // convert_and_add
             std::cout << convert_and_add(3, 4.5) << '\n';    // 7.5
             std::cout << convert_and_add(2.5, 3) << '\n';    // 5.5

             return 0;
         }


.. dropdown:: Exercise 3 -- Template Specialization
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Write a function template ``to_string_pretty(T value)`` that converts a value to a formatted string, with specializations for ``bool`` and ``double``.

   **Specification**

   1. Write the **generic** version that uses ``std::to_string``.
   2. Write a **full specialization** for ``bool`` that returns ``"true"`` or ``"false"`` (instead of ``"1"`` or ``"0"``).
   3. Write a **full specialization** for ``double`` that formats the number to exactly 2 decimal places using ``std::ostringstream`` with ``std::fixed`` and ``std::setprecision(2)``.
   4. Test with ``int``, ``bool``, and ``double`` values.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: cpp

         #include <iostream>
         #include <string>
         #include <sstream>
         #include <iomanip>

         // Generic version
         template<typename T>
         std::string to_string_pretty(T value) {
             return std::to_string(value);
         }

         // Specialization for bool
         template<>
         std::string to_string_pretty<bool>(bool value) {
             return value ? "true" : "false";
         }

         // Specialization for double
         template<>
         std::string to_string_pretty<double>(double value) {
             std::ostringstream oss;
             oss << std::fixed << std::setprecision(2) << value;
             return oss.str();
         }

         int main() {
             std::cout << to_string_pretty(42) << '\n';        // "42"
             std::cout << to_string_pretty(true) << '\n';      // "true"
             std::cout << to_string_pretty(false) << '\n';     // "false"
             std::cout << to_string_pretty(3.14159) << '\n';   // "3.14"

             return 0;
         }


.. dropdown:: Exercise 4 -- Lambda Expressions
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Use lambda expressions with STL algorithms.

   **Specification**

   1. Create a ``std::vector<int>`` with values ``{5, -3, 8, -1, 7, 2, -4, 6}``.
   2. Use ``std::sort`` with a lambda to sort the vector by **absolute value** (ascending).
   3. Use ``std::count_if`` with a lambda to count negative numbers.
   4. Use ``std::transform`` with a lambda to create a new vector where each element is squared.
   5. Use ``std::for_each`` with a lambda that captures a running total by reference to compute the sum.
   6. Use a lambda with the ``mutable`` keyword that captures a counter by value and increments it on each call. Call it 3 times and verify the original variable is unchanged.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: cpp

         #include <iostream>
         #include <vector>
         #include <algorithm>
         #include <numeric>
         #include <cmath>

         int main() {
             std::vector<int> values{5, -3, 8, -1, 7, 2, -4, 6};

             // 1. Sort by absolute value
             std::sort(values.begin(), values.end(), [](int a, int b) {
                 return std::abs(a) < std::abs(b);
             });
             std::cout << "Sorted by abs: ";
             for (int v : values) std::cout << v << " ";
             std::cout << '\n';

             // Reset for remaining exercises
             values = {5, -3, 8, -1, 7, 2, -4, 6};

             // 2. Count negatives
             int neg_count{static_cast<int>(std::count_if(values.begin(), values.end(),
                 [](int x) { return x < 0; }))};
             std::cout << "Negative count: " << neg_count << '\n';

             // 3. Transform: square each element
             std::vector<int> squared(values.size());
             std::transform(values.begin(), values.end(), squared.begin(),
                 [](int x) { return x * x; });
             std::cout << "Squared: ";
             for (int v : squared) std::cout << v << " ";
             std::cout << '\n';

             // 4. Sum using for_each with capture by reference
             int total{0};
             std::for_each(values.begin(), values.end(), [&total](int x) {
                 total += x;
             });
             std::cout << "Sum: " << total << '\n';

             // 5. Mutable lambda
             int counter{0};
             auto incrementer = [counter]() mutable {
                 counter++;
                 return counter;
             };
             std::cout << incrementer() << '\n'; // 1
             std::cout << incrementer() << '\n'; // 2
             std::cout << incrementer() << '\n'; // 3
             std::cout << "Original counter: " << counter << '\n'; // 0

             return 0;
         }


.. dropdown:: Exercise 5 -- std::function Callbacks
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Demonstrate ``std::function`` as a flexible callback mechanism.

   **Specification**

   1. Write a function ``apply_operation(const std::vector<int>& data, std::function<int(int)> op)`` that applies an operation to each element and returns a new vector.
   2. Define a free function ``negate_value`` that negates an integer.
   3. Define a functor ``ScaleBy`` that multiplies by a configurable factor.
   4. Call ``apply_operation`` three times using: a lambda (double each value), the free function, and the functor.
   5. Demonstrate checking an empty ``std::function`` before calling it.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: cpp

         #include <iostream>
         #include <vector>
         #include <functional>

         // Apply an operation to each element
         std::vector<int> apply_operation(const std::vector<int>& data,
                                          std::function<int(int)> op) {
             std::vector<int> result;
             result.reserve(data.size());
             for (int val : data) {
                 result.push_back(op(val));
             }
             return result;
         }

         // Free function
         int negate_value(int x) { return -x; }

         // Functor
         struct ScaleBy {
             int factor;
             ScaleBy(int f) : factor(f) {}
             int operator()(int x) const { return x * factor; }
         };

         void print_vector(const std::vector<int>& v) {
             for (int val : v) std::cout << val << " ";
             std::cout << '\n';
         }

         int main() {
             std::vector<int> data{1, 2, 3, 4, 5};

             // 1. Lambda
             auto doubled = apply_operation(data, [](int x) { return x * 2; });
             std::cout << "Doubled: ";
             print_vector(doubled);

             // 2. Free function
             auto negated = apply_operation(data, negate_value);
             std::cout << "Negated: ";
             print_vector(negated);

             // 3. Functor
             ScaleBy times_10(10);
             auto scaled = apply_operation(data, times_10);
             std::cout << "Scaled x10: ";
             print_vector(scaled);

             // 4. Empty std::function check
             std::function<int(int)> empty_op;
             if (empty_op) {
                 std::cout << empty_op(5) << '\n';
             } else {
                 std::cout << "Operation is empty -- skipping call.\n";
             }

             return 0;
         }


.. dropdown:: Challenge -- Generic Sorting with Templates and Lambdas
   :icon: gear
   :class-container: sd-border-warning
   :class-title: sd-font-weight-bold

   **Goal**

   Write a generic sorting utility that combines templates and lambdas.

   **Specification**

   1. Write a function template ``sort_by(std::vector<T>& data, Comparator comp)`` where ``Comparator`` is also a template parameter. It should implement selection sort (do not use ``std::sort``).
   2. Define a ``struct Student`` with fields: ``std::string name``, ``double gpa``, ``int credits``.
   3. Create a vector of 5 students.
   4. Sort by GPA (descending) using a lambda comparator.
   5. Sort by name (alphabetical) using a lambda comparator.
   6. Sort by credits (ascending) using a lambda comparator.
   7. Print the sorted results after each sort.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: cpp

         #include <iostream>
         #include <vector>
         #include <string>

         struct Student {
             std::string name;
             double gpa;
             int credits;
         };

         // Generic selection sort with a comparator
         template<typename T, typename Comparator>
         void sort_by(std::vector<T>& data, Comparator comp) {
             for (size_t i{0}; i < data.size(); ++i) {
                 size_t best{i};
                 for (size_t j{i + 1}; j < data.size(); ++j) {
                     if (comp(data[j], data[best])) {
                         best = j;
                     }
                 }
                 if (best != i) {
                     T temp{data[i]};
                     data[i] = data[best];
                     data[best] = temp;
                 }
             }
         }

         void print_students(const std::vector<Student>& students) {
             for (const auto& s : students) {
                 std::cout << "  " << s.name
                           << " | GPA: " << s.gpa
                           << " | Credits: " << s.credits << '\n';
             }
         }

         int main() {
             std::vector<Student> students{
                 {"Alice", 3.8, 45},
                 {"Bob", 3.5, 60},
                 {"Charlie", 3.9, 30},
                 {"Diana", 3.2, 75},
                 {"Eve", 3.7, 50}
             };

             // Sort by GPA (descending)
             sort_by(students, [](const Student& a, const Student& b) {
                 return a.gpa > b.gpa;
             });
             std::cout << "Sorted by GPA (desc):\n";
             print_students(students);

             // Sort by name (alphabetical)
             sort_by(students, [](const Student& a, const Student& b) {
                 return a.name < b.name;
             });
             std::cout << "\nSorted by name (asc):\n";
             print_students(students);

             // Sort by credits (ascending)
             sort_by(students, [](const Student& a, const Student& b) {
                 return a.credits < b.credits;
             });
             std::cout << "\nSorted by credits (asc):\n";
             print_students(students);

             return 0;
         }
