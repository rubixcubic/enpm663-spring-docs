====================================================
C++ Exercises
====================================================


.. dropdown:: Exercise 1 -- If/Else Basics
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write a program that reads a robot sensor reading (an integer) from
   the user and categorizes it as follows:

   - If the reading is less than 0, print ``"Error: negative reading"``
   - If the reading is between 0 and 50 (inclusive), print ``"Low"``
   - If the reading is between 51 and 200 (inclusive), print ``"Normal"``
   - If the reading is greater than 200, print ``"High"``

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: cpp

         #include <iostream>

         int main() {
             std::cout << "Enter sensor reading: ";
             int reading{};
             std::cin >> reading;

             if (reading < 0) {
                 std::cout << "Error: negative reading\n";
             } else if (reading <= 50) {
                 std::cout << "Low\n";
             } else if (reading <= 200) {
                 std::cout << "Normal\n";
             } else {
                 std::cout << "High\n";
             }

             return 0;
         }


.. dropdown:: Exercise 2 -- Switch Statement
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write a program that reads a single character representing a robot
   command and uses a ``switch`` statement to print the corresponding
   action:

   - ``'f'`` -- ``"Moving forward"``
   - ``'b'`` -- ``"Moving backward"``
   - ``'l'`` -- ``"Turning left"``
   - ``'r'`` -- ``"Turning right"``
   - ``'s'`` -- ``"Stopping"``
   - Any other character -- ``"Unknown command"``

   Accept both uppercase and lowercase letters (e.g., ``'f'`` and ``'F'``
   should both print ``"Moving forward"``).

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: cpp

         #include <iostream>

         int main() {
             std::cout << "Enter robot command (f/b/l/r/s): ";
             char command{};
             std::cin >> command;

             switch (command) {
             case 'f':
             case 'F':
                 std::cout << "Moving forward\n";
                 break;
             case 'b':
             case 'B':
                 std::cout << "Moving backward\n";
                 break;
             case 'l':
             case 'L':
                 std::cout << "Turning left\n";
                 break;
             case 'r':
             case 'R':
                 std::cout << "Turning right\n";
                 break;
             case 's':
             case 'S':
                 std::cout << "Stopping\n";
                 break;
             default:
                 std::cout << "Unknown command\n";
                 break;
             }

             return 0;
         }


.. dropdown:: Exercise 3 -- For Loop
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   A robot has 8 distance sensors. The readings (in centimeters) are
   stored in an array:

   .. code-block:: cpp

      int readings[]{12, 45, 7, 89, 34, 56, 3, 22};

   Write a program that uses a ``for`` loop to:

   1. Calculate the sum of all sensor readings.
   2. Find the minimum reading and its index.
   3. Print the sum, the minimum value, and its index.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: cpp

         #include <iostream>

         int main() {
             int readings[]{12, 45, 7, 89, 34, 56, 3, 22};
             int size{8};

             int sum{0};
             int min_value{readings[0]};
             int min_index{0};

             for (int i{0}; i < size; ++i) {
                 sum += readings[i];
                 if (readings[i] < min_value) {
                     min_value = readings[i];
                     min_index = i;
                 }
             }

             std::cout << "Sum: " << sum << '\n';
             std::cout << "Min value: " << min_value << '\n';
             std::cout << "Min index: " << min_index << '\n';

             return 0;
         }


.. dropdown:: Exercise 4 -- While and Do-While
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write two small programs that ask the user to enter a valid motor
   speed (an integer between 0 and 100 inclusive).

   **Part A** -- Use a ``while`` loop. If the initial input is valid, the
   loop should not execute at all.

   **Part B** -- Use a ``do-while`` loop. The prompt should always appear
   at least once.

   For both parts, once a valid speed is entered, print
   ``"Motor speed set to: <speed>"``.

   .. dropdown:: Solution
      :class-container: sd-border-success

      **Part A -- while loop:**

      .. code-block:: cpp

         #include <iostream>

         int main() {
             int speed{-1};

             std::cout << "Enter motor speed (0-100): ";
             std::cin >> speed;

             while (speed < 0 || speed > 100) {
                 std::cout << "Invalid. Enter motor speed (0-100): ";
                 std::cin >> speed;
             }

             std::cout << "Motor speed set to: " << speed << '\n';

             return 0;
         }

      **Part B -- do-while loop:**

      .. code-block:: cpp

         #include <iostream>

         int main() {
             int speed{};

             do {
                 std::cout << "Enter motor speed (0-100): ";
                 std::cin >> speed;
             } while (speed < 0 || speed > 100);

             std::cout << "Motor speed set to: " << speed << '\n';

             return 0;
         }


.. dropdown:: Exercise 5 -- Nested Loops
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write a program that uses nested ``for`` loops to print the following
   right-triangle pattern. The user enters the number of rows.

   Example output for 5 rows:

   .. code-block:: text

      *
      **
      ***
      ****
      *****

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: cpp

         #include <iostream>

         int main() {
             std::cout << "Enter number of rows: ";
             int rows{};
             std::cin >> rows;

             for (int i{1}; i <= rows; ++i) {
                 for (int j{0}; j < i; ++j) {
                     std::cout << '*';
                 }
                 std::cout << '\n';
             }

             return 0;
         }


.. dropdown:: Exercise 6 -- Challenge: Menu-Driven Robot Controller
   :icon: gear
   :class-container: sd-border-warning
   :class-title: sd-font-weight-bold

   Build a simple menu-driven robot controller that combines ``switch``,
   loops, and input validation. The program should:

   1. Display a menu with options:

      - ``1) Move forward``
      - ``2) Move backward``
      - ``3) Turn left``
      - ``4) Turn right``
      - ``5) Set speed``
      - ``6) Quit``

   2. Use a ``do-while`` loop to keep the menu running until the user
      selects ``6) Quit``.
   3. Use a ``switch`` statement to handle each menu option.
   4. For ``5) Set speed``, use input validation (``while`` loop) to
      ensure the speed is between 0 and 100.
   5. After each action, print the current robot state (direction and
      speed).

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: cpp

         #include <iostream>

         int main() {
             int choice{};
             int speed{0};
             char direction{'S'};  // S=stopped, F=forward, B=backward, L=left, R=right

             do {
                 std::cout << "\n--- Robot Controller ---\n";
                 std::cout << "1) Move forward\n";
                 std::cout << "2) Move backward\n";
                 std::cout << "3) Turn left\n";
                 std::cout << "4) Turn right\n";
                 std::cout << "5) Set speed\n";
                 std::cout << "6) Quit\n";
                 std::cout << "Select option: ";
                 std::cin >> choice;

                 switch (choice) {
                 case 1:
                     direction = 'F';
                     std::cout << "Moving forward\n";
                     break;
                 case 2:
                     direction = 'B';
                     std::cout << "Moving backward\n";
                     break;
                 case 3:
                     direction = 'L';
                     std::cout << "Turning left\n";
                     break;
                 case 4:
                     direction = 'R';
                     std::cout << "Turning right\n";
                     break;
                 case 5: {
                     int new_speed{-1};
                     do {
                         std::cout << "Enter speed (0-100): ";
                         std::cin >> new_speed;
                     } while (new_speed < 0 || new_speed > 100);
                     speed = new_speed;
                     std::cout << "Speed updated\n";
                     break;
                 }
                 case 6:
                     std::cout << "Shutting down robot\n";
                     break;
                 default:
                     std::cout << "Invalid option\n";
                     break;
                 }

                 if (choice != 6) {
                     std::cout << "State: direction=" << direction
                               << " speed=" << speed << '\n';
                 }

             } while (choice != 6);

             return 0;
         }
