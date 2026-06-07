====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 5: Functions --
Basics. Work through them in order, as each exercise builds on the
skills from the previous one.

.. note::

   Compile all programs with warnings enabled:

   .. code-block:: bash

      g++ -std=c++17 -Wall -Wextra -o program program.cpp


----


.. dropdown:: Exercise 1 -- Basic Function Declarations and Definitions
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write a program that demonstrates the complete function lifecycle: declaration, definition, and call.

   1. In a header file ``math_utils.hpp``, declare the following functions with Doxygen documentation:

      - ``int add(int a, int b);``
      - ``int subtract(int a, int b);``
      - ``double average(double a, double b);``
      - ``bool is_even(int number);``

   2. In a source file ``math_utils.cpp``, provide the definitions for all four functions.
   3. In ``main.cpp``, include the header, call each function, and print the results.
   4. Add ``#pragma once`` to the header file.
   5. Build using: ``g++ -std=c++17 main.cpp math_utils.cpp -o exercise1``

   .. dropdown:: Solution
      :class-container: sd-border-success

      **math_utils.hpp**

      .. code-block:: cpp

         #pragma once

         /**
          * @brief Adds two integers.
          * @param a The first integer.
          * @param b The second integer.
          * @return The sum of a and b.
          */
         int add(int a, int b);

         /**
          * @brief Subtracts the second integer from the first.
          * @param a The first integer.
          * @param b The second integer.
          * @return The result of a minus b.
          */
         int subtract(int a, int b);

         /**
          * @brief Calculates the average of two doubles.
          * @param a The first value.
          * @param b The second value.
          * @return The average of a and b.
          */
         double average(double a, double b);

         /**
          * @brief Checks whether a number is even.
          * @param number The number to check.
          * @return true if the number is even, false otherwise.
          */
         bool is_even(int number);

      **math_utils.cpp**

      .. code-block:: cpp

         #include "math_utils.hpp"

         int add(int a, int b) {
             return a + b;
         }

         int subtract(int a, int b) {
             return a - b;
         }

         double average(double a, double b) {
             return (a + b) / 2.0;
         }

         bool is_even(int number) {
             return number % 2 == 0;
         }

      **main.cpp**

      .. code-block:: cpp

         #include <iostream>
         #include "math_utils.hpp"

         int main() {
             std::cout << "add(3, 5) = " << add(3, 5) << '\n';
             std::cout << "subtract(10, 4) = " << subtract(10, 4) << '\n';
             std::cout << "average(7.5, 2.5) = " << average(7.5, 2.5) << '\n';
             std::cout << "is_even(42) = " << std::boolalpha << is_even(42) << '\n';
             std::cout << "is_even(7) = " << std::boolalpha << is_even(7) << '\n';
         }

.. dropdown:: Exercise 2 -- Pass-by-Value vs. Pass-by-Reference
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write a program that demonstrates the difference between pass-by-value, pass-by-reference, and pass-by-const-reference.

   1. Write a function ``void double_value(int x)`` that doubles its parameter (pass-by-value).
   2. Write a function ``void double_reference(int& x)`` that doubles its parameter (pass-by-reference).
   3. Write a function ``void print_vector(const std::vector<int>& v)`` that prints all elements (pass-by-const-reference).
   4. Write a function ``void add_element(std::vector<int>& v, int element)`` that adds an element to a vector (pass-by-reference).
   5. In ``main()``, demonstrate that pass-by-value does not modify the original, while pass-by-reference does.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: cpp

         #include <iostream>
         #include <vector>

         void double_value(int x) {
             x *= 2;
             std::cout << "Inside double_value: x = " << x << '\n';
         }

         void double_reference(int& x) {
             x *= 2;
             std::cout << "Inside double_reference: x = " << x << '\n';
         }

         void print_vector(const std::vector<int>& v) {
             std::cout << "Vector contents: ";
             for (const int& item : v) {
                 std::cout << item << " ";
             }
             std::cout << '\n';
         }

         void add_element(std::vector<int>& v, int element) {
             v.push_back(element);
         }

         int main() {
             // Pass-by-value: original is NOT modified
             int num{10};
             std::cout << "Before double_value: num = " << num << '\n';
             double_value(num);
             std::cout << "After double_value: num = " << num << '\n';

             std::cout << '\n';

             // Pass-by-reference: original IS modified
             std::cout << "Before double_reference: num = " << num << '\n';
             double_reference(num);
             std::cout << "After double_reference: num = " << num << '\n';

             std::cout << '\n';

             // Pass-by-const-reference: read-only, no copy
             std::vector<int> numbers{1, 2, 3, 4, 5};
             print_vector(numbers);

             // Pass-by-reference: modifying the vector
             add_element(numbers, 6);
             print_vector(numbers);
         }

.. dropdown:: Exercise 3 -- Function Overloading
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write a program that demonstrates function overloading by creating multiple versions of an ``area`` function.

   1. ``double area(double radius)`` -- calculates the area of a circle.
   2. ``double area(double length, double width)`` -- calculates the area of a rectangle.
   3. ``double area(double base, double height, bool is_triangle)`` -- calculates the area of a triangle (when ``is_triangle`` is true).
   4. Call each overloaded function from ``main()`` and print the results.
   5. Observe which version the compiler selects for each call.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: cpp

         #include <cmath>
         #include <iostream>

         // Area of a circle
         double area(double radius) {
             return M_PI * radius * radius;
         }

         // Area of a rectangle
         double area(double length, double width) {
             return length * width;
         }

         // Area of a triangle
         double area(double base, double height, bool is_triangle) {
             if (is_triangle) {
                 return 0.5 * base * height;
             }
             return base * height; // Fallback to rectangle
         }

         int main() {
             std::cout << "Circle area (r=5): " << area(5.0) << '\n';
             std::cout << "Rectangle area (4x6): " << area(4.0, 6.0) << '\n';
             std::cout << "Triangle area (b=3, h=8): " << area(3.0, 8.0, true) << '\n';
         }

.. dropdown:: Exercise 4 -- Recursive Functions
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write a program that implements the following recursive functions.

   1. ``int fibonacci(int n)`` -- returns the nth Fibonacci number. ``fibonacci(0) = 0``, ``fibonacci(1) = 1``, ``fibonacci(n) = fibonacci(n-1) + fibonacci(n-2)``.
   2. ``int sum_digits(int n)`` -- returns the sum of all digits in a non-negative integer. For example, ``sum_digits(1234)`` returns ``10``.
   3. ``void print_reverse(const std::string& str, int index)`` -- prints a string in reverse, character by character, using recursion.
   4. For each function, identify the **base case** and the **recursive step** in a comment.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: cpp

         #include <iostream>
         #include <string>

         // Base case: n <= 1
         // Recursive step: fib(n) = fib(n-1) + fib(n-2)
         int fibonacci(int n) {
             if (n <= 0) {
                 return 0;
             }
             if (n == 1) {
                 return 1;
             }
             return fibonacci(n - 1) + fibonacci(n - 2);
         }

         // Base case: n < 10 (single digit)
         // Recursive step: last digit + sum_digits(remaining digits)
         int sum_digits(int n) {
             if (n < 10) {
                 return n;
             }
             return (n % 10) + sum_digits(n / 10);
         }

         // Base case: index < 0
         // Recursive step: print current character, recurse with index - 1
         void print_reverse(const std::string& str, int index) {
             if (index < 0) {
                 return;
             }
             std::cout << str.at(index);
             print_reverse(str, index - 1);
         }

         int main() {
             // Fibonacci
             for (int i{0}; i <= 10; ++i) {
                 std::cout << "fibonacci(" << i << ") = " << fibonacci(i) << '\n';
             }

             std::cout << '\n';

             // Sum of digits
             std::cout << "sum_digits(1234) = " << sum_digits(1234) << '\n';
             std::cout << "sum_digits(9999) = " << sum_digits(9999) << '\n';

             std::cout << '\n';

             // Print reverse
             std::string msg{"Hello, World!"};
             std::cout << "Reverse of \"" << msg << "\": ";
             print_reverse(msg, static_cast<int>(msg.size()) - 1);
             std::cout << '\n';
         }

.. dropdown:: Exercise 5 -- Header File Organization
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Reorganize a monolithic program into properly separated files. Start with this single-file program and split it into a header, source, and main file.

   **Starting code (all in main.cpp):**

   .. code-block:: cpp

      #include <iostream>
      #include <string>
      #include <vector>

      void print_menu() {
          std::cout << "1. Add student\n";
          std::cout << "2. Print students\n";
          std::cout << "3. Quit\n";
      }

      void add_student(std::vector<std::string>& students, const std::string& name) {
          students.push_back(name);
          std::cout << "Added: " << name << '\n';
      }

      void print_students(const std::vector<std::string>& students) {
          if (students.empty()) {
              std::cout << "No students registered.\n";
              return;
          }
          std::cout << "Registered students:\n";
          for (const auto& student : students) {
              std::cout << "  - " << student << '\n';
          }
      }

      int main() {
          std::vector<std::string> students;
          int choice{0};
          while (choice != 3) {
              print_menu();
              std::cout << "Enter choice: ";
              std::cin >> choice;
              if (choice == 1) {
                  std::string name;
                  std::cout << "Enter student name: ";
                  std::cin >> std::ws;
                  std::getline(std::cin, name);
                  add_student(students, name);
              } else if (choice == 2) {
                  print_students(students);
              }
          }
      }

   **Tasks:**

   1. Create ``student_utils.hpp`` with declarations and Doxygen comments for ``print_menu``, ``add_student``, and ``print_students``.
   2. Create ``student_utils.cpp`` with the definitions.
   3. Simplify ``main.cpp`` to contain only the ``main`` function and the necessary ``#include``.
   4. Build with: ``g++ -std=c++17 main.cpp student_utils.cpp -o exercise5``

.. dropdown:: Exercise 6 -- Challenge: Calculator with Functions
   :icon: gear
   :class-container: sd-border-warning
   :class-title: sd-font-weight-bold

   Build a modular calculator program that uses functions for all operations. The program should:

   1. Define the following functions in ``calculator.hpp`` / ``calculator.cpp``:

      - ``double add(double a, double b);``
      - ``double subtract(double a, double b);``
      - ``double multiply(double a, double b);``
      - ``double divide(double a, double b);`` -- handle division by zero by printing an error message and returning ``0.0``.
      - ``double power(double base, int exponent);`` -- implement using a loop (not ``std::pow``). Handle negative exponents.
      - ``long long factorial(int n);`` -- implement recursively. Return ``1`` for ``n <= 1``.
      - ``void print_result(const std::string& operation, double result);`` -- format and display the result.
      - ``void print_menu();`` -- display available operations.

   2. Use **default parameters**: ``print_result`` should have a default precision parameter (``int precision = 2``).

   3. Use **function overloading**: Create an ``add`` function that works with both ``double`` and ``int`` arguments.

   4. In ``main()``, implement a loop that:

      - Displays the menu.
      - Reads the user's operation choice.
      - Reads the operands.
      - Calls the appropriate function and displays the result.
      - Exits when the user chooses "quit".

   5. Use proper header guards and Doxygen documentation for all functions.

   .. dropdown:: Starter Code
      :class-container: sd-border-success

      **calculator.hpp**

      .. code-block:: cpp

         #pragma once
         #include <string>

         /**
          * @brief Adds two double values.
          * @param a The first operand.
          * @param b The second operand.
          * @return The sum of a and b.
          */
         double add(double a, double b);

         /**
          * @brief Adds two integer values.
          * @param a The first operand.
          * @param b The second operand.
          * @return The sum of a and b.
          */
         int add(int a, int b);

         double subtract(double a, double b);
         double multiply(double a, double b);
         double divide(double a, double b);
         double power(double base, int exponent);
         long long factorial(int n);
         void print_result(const std::string& operation, double result, int precision = 2);
         void print_menu();

      **main.cpp**

      .. code-block:: cpp

         #include <iostream>
         #include <string>
         #include "calculator.hpp"

         int main() {
             int choice{0};
             while (true) {
                 print_menu();
                 std::cout << "Enter choice (0 to quit): ";
                 std::cin >> choice;

                 if (choice == 0) {
                     std::cout << "Goodbye!\n";
                     break;
                 }

                 // TODO: Read operands and call the appropriate function
                 // based on the user's choice.
             }
         }
