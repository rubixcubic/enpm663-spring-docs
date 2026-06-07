====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 2: Introduction to C++.
Work through them in order, as each exercise builds on the skills from the previous one.
Write, compile, and run each program to verify your understanding.

.. note::

   Compile all programs with warnings enabled:

   .. code-block:: bash

      g++ -std=c++17 -Wall -Wextra -o program program.cpp


----


.. dropdown:: Exercise 1 -- Variable Declarations and Initialization
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice declaring and initializing variables of different types using
    uniform (brace) initialization and explore the ``sizeof`` operator.

    **Specification**

    1. Create a file called ``variables.cpp``.
    2. Declare and initialize the following variables using uniform initialization (``{}``):

       - An ``int`` for a robot's ID (e.g., 42).
       - A ``double`` for a sensor reading (e.g., 3.14159).
       - A ``float`` for a motor speed (e.g., 1.5f).
       - A ``char`` for a status code (e.g., 'A').
       - A ``bool`` for whether a sensor is active (e.g., true).
       - A ``short`` for a small counter (e.g., 100).
       - An ``unsigned int`` for a part number (e.g., 50000).

    3. Print each variable's value and its size using ``sizeof``.
    4. Use ``std::boolalpha`` to print the ``bool`` as ``true``/``false`` instead of ``1``/``0``.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>

           int main() {
               // Uniform initialization
               int robot_id{42};
               double sensor_reading{3.14159};
               float motor_speed{1.5f};
               char status_code{'A'};
               bool sensor_active{true};
               short counter{100};
               unsigned int part_number{50000};

               // Print values and sizes
               std::cout << "robot_id: " << robot_id
                         << " | size: " << sizeof(robot_id) << " bytes\n";
               std::cout << "sensor_reading: " << sensor_reading
                         << " | size: " << sizeof(sensor_reading) << " bytes\n";
               std::cout << "motor_speed: " << motor_speed
                         << " | size: " << sizeof(motor_speed) << " bytes\n";
               std::cout << "status_code: " << status_code
                         << " | size: " << sizeof(status_code) << " bytes\n";
               std::cout << "sensor_active: " << std::boolalpha << sensor_active
                         << " | size: " << sizeof(sensor_active) << " bytes\n";
               std::cout << "counter: " << counter
                         << " | size: " << sizeof(counter) << " bytes\n";
               std::cout << "part_number: " << part_number
                         << " | size: " << sizeof(part_number) << " bytes\n";

               return 0;
           }


----


.. dropdown:: Exercise 2 -- Type Conversion Explorer
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Understand implicit type conversions, narrowing conversions, and
    arithmetic conversions in C++.

    **Specification**

    1. Create a file called ``conversions.cpp``.
    2. Include ``<iostream>`` and ``<typeinfo>``.
    3. Demonstrate the following conversions and print results with ``typeid().name()``:

       - **Implicit widening:** Assign an ``int`` to a ``double`` and print both values and types.
       - **Narrowing with static_cast:** Assign a ``double`` to an ``int`` using ``static_cast<int>()`` and observe truncation.
       - **Bool to int:** Add ``true`` and ``false`` to an integer and print the result.
       - **Arithmetic conversion:** Add an ``int`` and a ``double`` and show the resulting type.
       - **Char to int:** Print a ``char`` variable as both a character and its integer (ASCII) value.

    4. For each conversion, print a descriptive label explaining what is happening.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>
           #include <typeinfo>

           int main() {
               // 1. Implicit widening: int -> double
               int int_val{42};
               double widened{int_val};
               std::cout << "=== Implicit Widening ===\n";
               std::cout << "int_val: " << int_val
                         << " (type: " << typeid(int_val).name() << ")\n";
               std::cout << "widened: " << widened
                         << " (type: " << typeid(widened).name() << ")\n\n";

               // 2. Narrowing with static_cast: double -> int
               double pi{3.14159};
               int truncated{static_cast<int>(pi)};
               std::cout << "=== Narrowing with static_cast ===\n";
               std::cout << "pi: " << pi << "\n";
               std::cout << "truncated: " << truncated
                         << " (fractional part lost)\n\n";

               // 3. Bool to int
               int bool_sum{5 + true + false};
               std::cout << "=== Bool to Int ===\n";
               std::cout << "5 + true + false = " << bool_sum
                         << " (true=1, false=0)\n\n";

               // 4. Arithmetic conversion: int + double -> double
               int a{10};
               double b{3.5};
               auto result = a + b;
               std::cout << "=== Arithmetic Conversion ===\n";
               std::cout << "int(10) + double(3.5) = " << result
                         << " (type: " << typeid(result).name() << ")\n\n";

               // 5. Char to int
               char letter{'Z'};
               std::cout << "=== Char to Int ===\n";
               std::cout << "letter as char: " << letter << "\n";
               std::cout << "letter as int: " << static_cast<int>(letter) << "\n";

               return 0;
           }


----


.. dropdown:: Exercise 3 -- Constants and constexpr
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Understand the difference between ``const`` and ``constexpr`` and when
    to use each.

    **Specification**

    1. Create a file called ``constants.cpp``.
    2. Declare the following constants:

       - A ``constexpr double`` for pi (3.14159265358979).
       - A ``constexpr int`` for the maximum number of joints on a robot arm (6).
       - A ``const`` variable initialized from a computation (e.g., circumference = 2 * pi * radius, where radius is a ``constexpr``).

    3. Use the constants to compute and print:

       - The area of a circle with radius 5.0 (area = pi * r * r).
       - The circumference of that circle (circumference = 2 * pi * r).

    4. Show that ``constexpr`` cannot use runtime values:

       - Read an ``int`` from ``std::cin`` and store it in a ``const`` variable (this works).
       - Comment out a line that tries to store the same input in a ``constexpr`` variable, with a comment explaining why it fails.

    5. Print all results.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>

           int main() {
               // constexpr: evaluated at compile time
               constexpr double pi{3.14159265358979};
               constexpr int max_joints{6};
               constexpr double radius{5.0};

               // const: computed from constexpr values (also compile-time here)
               const double area{pi * radius * radius};
               const double circumference{2.0 * pi * radius};

               std::cout << "=== Compile-Time Constants ===\n";
               std::cout << "pi: " << pi << "\n";
               std::cout << "max_joints: " << max_joints << "\n";
               std::cout << "radius: " << radius << "\n";
               std::cout << "area: " << area << "\n";
               std::cout << "circumference: " << circumference << "\n\n";

               // const can use runtime values
               std::cout << "Enter a number: ";
               int user_input{};
               std::cin >> user_input;
               const int user_const{user_input};  // OK: const with runtime value

               std::cout << "Your const value: " << user_const << "\n";

               // constexpr CANNOT use runtime values (uncomment to see the error):
               // constexpr int user_constexpr{user_input};
               // Error: the value of 'user_input' is not usable in a constant expression

               return 0;
           }


----


.. dropdown:: Exercise 4 -- Scope Detective
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Understand variable scope, lifetime, and shadowing in C++.

    **Specification**

    1. Create a file called ``scopes.cpp``.
    2. **Part A -- Predict the output:** Before running the code below, predict
       what it will print. Then compile and run it to check your prediction.

       .. code-block:: cpp

          #include <iostream>

          int value{100};

          int main() {
              std::cout << value << "\n";
              int value{200};
              std::cout << value << "\n";
              {
                  int value{300};
                  std::cout << value << "\n";
                  {
                      std::cout << value << "\n";
                  }
              }
              std::cout << value << "\n";
              std::cout << ::value << "\n";
              return 0;
          }

    3. **Part B -- Write your own:** Write a program that:

       - Declares a global variable ``robot_name`` with value ``"GlobalBot"``.
       - In ``main()``, declares a local ``robot_name`` with value ``"LocalBot"``.
       - Inside a nested block, declares another ``robot_name`` with value ``"InnerBot"``.
       - Prints the innermost, local, and global versions (use ``::`` to access the global one).

    .. dropdown:: Solution
        :class-container: sd-border-success

        **Part A output:**

        .. code-block:: text

           100
           200
           300
           300
           200
           100

        The global ``value`` (100) is printed first. Then the local ``value`` (200) shadows it.
        Inside the nested block, another ``value`` (300) shadows the local one. The innermost
        block has no new ``value``, so it uses the nearest one (300). After the nested block
        ends, the local ``value`` (200) is back in scope. Finally, ``::value`` accesses the
        global ``value`` (100).

        **Part B solution:**

        .. code-block:: cpp

           #include <iostream>
           #include <string>

           std::string robot_name{"GlobalBot"};

           int main() {
               std::string robot_name{"LocalBot"};

               {
                   std::string robot_name{"InnerBot"};
                   std::cout << "Inner scope: " << robot_name << "\n";
               }

               std::cout << "Local scope: " << robot_name << "\n";
               std::cout << "Global scope: " << ::robot_name << "\n";

               return 0;
           }


----


.. dropdown:: Exercise 5 -- Namespace Organizer
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create and use custom namespaces to organize code for different robot
    subsystems.

    **Specification**

    1. Create a file called ``namespaces.cpp``.
    2. Define a namespace ``sensors`` with:

       - A ``constexpr int max_range{100};`` (in centimeters).
       - A ``double current_reading{0.0};``
       - A ``const std::string type{"LIDAR"};``

    3. Define a namespace ``actuators`` with:

       - A ``constexpr int max_speed{255};`` (PWM value).
       - A ``double current_speed{0.0};``
       - A ``const std::string type{"DC_MOTOR"};``

    4. In ``main()``, demonstrate three different ways to access namespace members:

       - **Fully qualified:** Use ``sensors::max_range`` directly.
       - **Using declaration:** Use ``using sensors::current_reading;`` then access ``current_reading`` directly.
       - **Using directive:** Use ``using namespace actuators;`` in a limited block scope.

    5. Set some values and print them with labels showing which subsystem they belong to.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>
           #include <string>

           namespace sensors {
               constexpr int max_range{100};
               double current_reading{0.0};
               const std::string type{"LIDAR"};
           }

           namespace actuators {
               constexpr int max_speed{255};
               double current_speed{0.0};
               const std::string type{"DC_MOTOR"};
           }

           int main() {
               // Method 1: Fully qualified names
               std::cout << "=== Fully Qualified ===\n";
               std::cout << "Sensor type: " << sensors::type << "\n";
               std::cout << "Sensor max range: " << sensors::max_range << " cm\n";

               // Method 2: Using declaration (imports a single name)
               std::cout << "\n=== Using Declaration ===\n";
               using sensors::current_reading;
               current_reading = 42.5;
               std::cout << "Sensor reading: " << current_reading << " cm\n";

               // Method 3: Using directive (imports all names -- limited scope)
               std::cout << "\n=== Using Directive (block scope) ===\n";
               {
                   using namespace actuators;
                   current_speed = 128.0;
                   std::cout << "Actuator type: " << type << "\n";
                   std::cout << "Actuator max speed: " << max_speed << "\n";
                   std::cout << "Actuator current speed: " << current_speed << "\n";
               }

               // Summary
               std::cout << "\n=== Summary ===\n";
               std::cout << "Sensor reading: " << sensors::current_reading << " cm\n";
               std::cout << "Actuator speed: " << actuators::current_speed << "\n";

               return 0;
           }


----


.. dropdown:: Exercise 6 -- Challenge: Unit Converter
    :icon: rocket
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Build an interactive unit converter that uses constants, proper types,
    namespaces, and input/output.

    **Specification**

    1. Create a file called ``converter.cpp``.
    2. Define a namespace ``conversion`` with ``constexpr`` conversion factors:

       - ``meters_to_feet`` (1 meter = 3.28084 feet)
       - ``kg_to_pounds`` (1 kg = 2.20462 pounds)
       - ``celsius_to_fahrenheit_scale`` (9.0 / 5.0)
       - ``celsius_to_fahrenheit_offset`` (32.0)

    3. The program should:

       - Display a menu with options: (1) Meters to Feet, (2) Kilograms to Pounds, (3) Celsius to Fahrenheit, (4) Quit.
       - Read the user's choice using ``std::cin``.
       - For options 1--3, prompt for a value, perform the conversion, and print the result.
       - For option 4, print a goodbye message and exit.
       - For invalid choices, print an error message.

    4. Use ``const`` for the user's input value (it should not change after reading).
    5. Use appropriate types (``double`` for measurements, ``int`` for menu choice).

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>

           namespace conversion {
               constexpr double meters_to_feet{3.28084};
               constexpr double kg_to_pounds{2.20462};
               constexpr double celsius_to_fahrenheit_scale{9.0 / 5.0};
               constexpr double celsius_to_fahrenheit_offset{32.0};
           }

           int main() {
               bool running{true};

               while (running) {
                   std::cout << "\n=== Unit Converter ===\n";
                   std::cout << "1. Meters to Feet\n";
                   std::cout << "2. Kilograms to Pounds\n";
                   std::cout << "3. Celsius to Fahrenheit\n";
                   std::cout << "4. Quit\n";
                   std::cout << "Enter your choice: ";

                   int choice{};
                   std::cin >> choice;

                   if (choice == 4) {
                       std::cout << "Goodbye!\n";
                       running = false;
                   } else if (choice == 1) {
                       std::cout << "Enter value in meters: ";
                       double input{};
                       std::cin >> input;
                       const double meters{input};
                       const double feet{meters * conversion::meters_to_feet};
                       std::cout << meters << " m = " << feet << " ft\n";

                   } else if (choice == 2) {
                       std::cout << "Enter value in kilograms: ";
                       double input{};
                       std::cin >> input;
                       const double kg{input};
                       const double pounds{kg * conversion::kg_to_pounds};
                       std::cout << kg << " kg = " << pounds << " lbs\n";

                   } else if (choice == 3) {
                       std::cout << "Enter value in Celsius: ";
                       double input{};
                       std::cin >> input;
                       const double celsius{input};
                       const double fahrenheit{
                           celsius * conversion::celsius_to_fahrenheit_scale
                           + conversion::celsius_to_fahrenheit_offset};
                       std::cout << celsius << " C = " << fahrenheit << " F\n";

                   } else {
                       std::cout << "Invalid choice. Please try again.\n";
                   }
               }

               return 0;
           }
