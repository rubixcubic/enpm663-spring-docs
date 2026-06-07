====================================================
C++ Exercises
====================================================


.. dropdown:: Exercise 1 -- Basic Try-Catch
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write a program that creates a ``std::vector<int>`` with 5 elements
   and attempts to access an out-of-bounds index using ``.at()``. Catch
   the resulting ``std::out_of_range`` exception and print the error
   message from ``what()``.

   Expected output (approximately):

   .. code-block:: text

      Caught out_of_range: vector::_M_range_check: __n (which is 10) >= this->size() (which is 5)

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: cpp

         #include <iostream>
         #include <vector>
         #include <stdexcept>

         int main() {
             std::vector<int> data{10, 20, 30, 40, 50};

             try {
                 std::cout << data.at(10) << '\n';
             } catch (const std::out_of_range& e) {
                 std::cout << "Caught out_of_range: " << e.what() << '\n';
             }

             return 0;
         }


.. dropdown:: Exercise 2 -- Throwing Exceptions
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write a function ``validate_speed(double speed)`` that checks whether
   a robot's speed is valid. The function should:

   - Throw ``std::invalid_argument`` if ``speed`` is negative.
   - Throw ``std::out_of_range`` if ``speed`` exceeds 10.0 (the
     maximum allowed speed).
   - Print ``"Speed OK: <speed>"`` if the speed is valid.

   In ``main()``, call ``validate_speed`` with values ``5.0``, ``-1.0``,
   and ``15.0``, catching and printing each exception.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: cpp

         #include <iostream>
         #include <stdexcept>

         void validate_speed(double speed) {
             if (speed < 0.0) {
                 throw std::invalid_argument("speed cannot be negative");
             }
             if (speed > 10.0) {
                 throw std::out_of_range("speed exceeds maximum of 10.0");
             }
             std::cout << "Speed OK: " << speed << '\n';
         }

         int main() {
             double test_speeds[]{5.0, -1.0, 15.0};

             for (double speed : test_speeds) {
                 try {
                     validate_speed(speed);
                 } catch (const std::invalid_argument& e) {
                     std::cout << "Invalid argument: " << e.what() << '\n';
                 } catch (const std::out_of_range& e) {
                     std::cout << "Out of range: " << e.what() << '\n';
                 }
             }

             return 0;
         }


.. dropdown:: Exercise 3 -- Multiple Catch Blocks
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write a function ``process_command(int code)`` that:

   - Throws ``std::invalid_argument`` if ``code`` is negative.
   - Throws ``std::out_of_range`` if ``code`` is greater than 100.
   - Throws ``std::runtime_error`` if ``code`` equals 42 (a simulated
     hardware fault).
   - Prints ``"Executing command <code>"`` otherwise.

   In ``main()``, test with values ``10``, ``-5``, ``42``, and ``200``.
   Use separate ``catch`` blocks for each exception type, plus a
   catch-all ``catch (...)`` as a safety net.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: cpp

         #include <iostream>
         #include <stdexcept>

         void process_command(int code) {
             if (code < 0) {
                 throw std::invalid_argument("negative command code");
             }
             if (code > 100) {
                 throw std::out_of_range("command code exceeds maximum");
             }
             if (code == 42) {
                 throw std::runtime_error("hardware fault on command 42");
             }
             std::cout << "Executing command " << code << '\n';
         }

         int main() {
             int test_codes[]{10, -5, 42, 200};

             for (int code : test_codes) {
                 try {
                     process_command(code);
                 } catch (const std::invalid_argument& e) {
                     std::cout << "Invalid argument: " << e.what() << '\n';
                 } catch (const std::out_of_range& e) {
                     std::cout << "Out of range: " << e.what() << '\n';
                 } catch (const std::runtime_error& e) {
                     std::cout << "Runtime error: " << e.what() << '\n';
                 } catch (...) {
                     std::cout << "Unknown exception caught\n";
                 }
             }

             return 0;
         }


.. dropdown:: Exercise 4 -- Custom Exception Class
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Create a small exception hierarchy for a robot system:

   1. ``RobotError`` -- base class inheriting from ``std::runtime_error``.
      Stores a ``robot_id`` (``std::string``).
   2. ``MotorError`` -- derived from ``RobotError``. Stores which motor
      failed (``std::string motor_name``).
   3. ``SensorError`` -- derived from ``RobotError``. Stores which
      sensor failed (``std::string sensor_name``).

   Write a function ``run_diagnostics(int test_case)`` that throws
   ``MotorError`` when ``test_case == 1`` and ``SensorError`` when
   ``test_case == 2``. In ``main()``, catch each type separately and
   print the details.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: cpp

         #include <iostream>
         #include <stdexcept>
         #include <string>

         class RobotError : public std::runtime_error {
         public:
             RobotError(const std::string& robot_id, const std::string& message)
                 : std::runtime_error("Robot '" + robot_id + "': " + message),
                   robot_id_{robot_id} {}

             const std::string& robot_id() const { return robot_id_; }

         private:
             std::string robot_id_;
         };

         class MotorError : public RobotError {
         public:
             MotorError(const std::string& robot_id,
                        const std::string& motor_name,
                        const std::string& message)
                 : RobotError(robot_id, "Motor '" + motor_name + "' -- " + message),
                   motor_name_{motor_name} {}

             const std::string& motor_name() const { return motor_name_; }

         private:
             std::string motor_name_;
         };

         class SensorError : public RobotError {
         public:
             SensorError(const std::string& robot_id,
                         const std::string& sensor_name,
                         const std::string& message)
                 : RobotError(robot_id, "Sensor '" + sensor_name + "' -- " + message),
                   sensor_name_{sensor_name} {}

             const std::string& sensor_name() const { return sensor_name_; }

         private:
             std::string sensor_name_;
         };

         void run_diagnostics(int test_case) {
             if (test_case == 1) {
                 throw MotorError("robot_01", "left_wheel", "stall detected");
             }
             if (test_case == 2) {
                 throw SensorError("robot_01", "lidar_front", "no data received");
             }
             std::cout << "Diagnostics passed for test case " << test_case << '\n';
         }

         int main() {
             for (int tc{0}; tc <= 2; ++tc) {
                 try {
                     run_diagnostics(tc);
                 } catch (const MotorError& e) {
                     std::cout << "Motor failure: " << e.what() << '\n';
                     std::cout << "  Motor: " << e.motor_name() << '\n';
                 } catch (const SensorError& e) {
                     std::cout << "Sensor failure: " << e.what() << '\n';
                     std::cout << "  Sensor: " << e.sensor_name() << '\n';
                 } catch (const RobotError& e) {
                     std::cout << "Robot error: " << e.what() << '\n';
                 }
             }

             return 0;
         }


.. dropdown:: Exercise 5 -- Exception-Safe Resource Management
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write two functions that allocate an ``int`` array and then throw an
   exception:

   1. ``unsafe_allocation()`` -- Uses ``new`` to allocate an array,
      throws an exception **before** calling ``delete[]``. This leaks
      memory.
   2. ``safe_allocation()`` -- Uses ``std::unique_ptr`` to manage the
      array. Even when an exception is thrown, the memory is
      automatically released.

   Call both from ``main()`` inside try-catch blocks. Add print
   statements in appropriate places to show when memory is (or is not)
   cleaned up.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: cpp

         #include <iostream>
         #include <memory>
         #include <stdexcept>

         void unsafe_allocation() {
             int* data{new int[100]};
             std::cout << "  Allocated raw array\n";

             // Simulate an error before cleanup
             throw std::runtime_error("error in unsafe_allocation");

             // This line is never reached -- memory is leaked
             delete[] data;
             std::cout << "  Deleted raw array\n";
         }

         void safe_allocation() {
             auto data{std::make_unique<int[]>(100)};
             std::cout << "  Allocated managed array\n";

             // Simulate an error
             throw std::runtime_error("error in safe_allocation");

             // unique_ptr automatically deletes the array during
             // stack unwinding -- no leak
         }

         int main() {
             std::cout << "--- Unsafe (raw pointer) ---\n";
             try {
                 unsafe_allocation();
             } catch (const std::runtime_error& e) {
                 std::cout << "  Caught: " << e.what() << '\n';
                 std::cout << "  Memory was LEAKED\n";
             }

             std::cout << "\n--- Safe (unique_ptr) ---\n";
             try {
                 safe_allocation();
             } catch (const std::runtime_error& e) {
                 std::cout << "  Caught: " << e.what() << '\n';
                 std::cout << "  Memory was automatically freed\n";
             }

             return 0;
         }


.. dropdown:: Exercise 6 -- Exception-Safe Config Parser (Challenge)
   :icon: gear
   :class-container: sd-border-warning
   :class-title: sd-font-weight-bold

   Write an exception-safe configuration file parser. The parser reads a
   text file containing key-value pairs (one per line, separated by
   ``=``) and stores them in a ``std::map<std::string, std::string>``.

   Requirements:

   1. Create three custom exception classes derived from
      ``std::runtime_error``:

      - ``FileError`` -- thrown when the file cannot be opened.
      - ``ParseError`` -- thrown when a line has invalid format (no ``=``
        sign). Store the line number.
      - ``MissingKeyError`` -- thrown when a required key is not found
        in the config. Store the key name.

   2. Write a function ``parse_config(const std::string& filename)``
      that returns a ``std::map<std::string, std::string>``.

   3. Write a function ``get_required(const std::map<...>& config,
      const std::string& key)`` that throws ``MissingKeyError`` if the
      key is absent.

   4. In ``main()``, parse a config file and retrieve required keys
      ``"robot_name"``, ``"max_speed"``, and ``"sensor_topic"``,
      handling each exception type.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: cpp

         #include <fstream>
         #include <iostream>
         #include <map>
         #include <sstream>
         #include <stdexcept>
         #include <string>

         // --- Custom Exception Classes ---

         class FileError : public std::runtime_error {
         public:
             explicit FileError(const std::string& filename)
                 : std::runtime_error("Cannot open file: " + filename),
                   filename_{filename} {}

             const std::string& filename() const { return filename_; }

         private:
             std::string filename_;
         };

         class ParseError : public std::runtime_error {
         public:
             ParseError(int line_number, const std::string& line_content)
                 : std::runtime_error("Parse error on line "
                       + std::to_string(line_number)
                       + ": missing '=' in '" + line_content + "'"),
                   line_number_{line_number} {}

             int line_number() const { return line_number_; }

         private:
             int line_number_;
         };

         class MissingKeyError : public std::runtime_error {
         public:
             explicit MissingKeyError(const std::string& key)
                 : std::runtime_error("Missing required key: " + key),
                   key_{key} {}

             const std::string& key() const { return key_; }

         private:
             std::string key_;
         };

         // --- Functions ---

         std::map<std::string, std::string> parse_config(
                 const std::string& filename) {
             std::ifstream file{filename};
             if (!file.is_open()) {
                 throw FileError(filename);
             }

             std::map<std::string, std::string> config;
             std::string line;
             int line_number{0};

             while (std::getline(file, line)) {
                 ++line_number;

                 // Skip empty lines and comments
                 if (line.empty() || line[0] == '#') {
                     continue;
                 }

                 auto pos{line.find('=')};
                 if (pos == std::string::npos) {
                     throw ParseError(line_number, line);
                 }

                 std::string key{line.substr(0, pos)};
                 std::string value{line.substr(pos + 1)};
                 config[key] = value;
             }

             return config;
         }

         const std::string& get_required(
                 const std::map<std::string, std::string>& config,
                 const std::string& key) {
             auto it{config.find(key)};
             if (it == config.end()) {
                 throw MissingKeyError(key);
             }
             return it->second;
         }

         int main() {
             try {
                 auto config{parse_config("robot_config.txt")};

                 std::string robot_name{get_required(config, "robot_name")};
                 std::string max_speed{get_required(config, "max_speed")};
                 std::string sensor_topic{get_required(config, "sensor_topic")};

                 std::cout << "Robot: " << robot_name << '\n';
                 std::cout << "Max speed: " << max_speed << '\n';
                 std::cout << "Sensor topic: " << sensor_topic << '\n';

             } catch (const FileError& e) {
                 std::cout << "File error: " << e.what() << '\n';
             } catch (const ParseError& e) {
                 std::cout << "Parse error: " << e.what() << '\n';
             } catch (const MissingKeyError& e) {
                 std::cout << "Config error: " << e.what() << '\n';
             } catch (const std::exception& e) {
                 std::cout << "Unexpected error: " << e.what() << '\n';
             }

             return 0;
         }
