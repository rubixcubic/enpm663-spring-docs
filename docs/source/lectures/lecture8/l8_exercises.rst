====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 8: OOP Basics.
Work through them in order, as each exercise builds on the skills from
the previous one.

.. note::

   Compile all programs with warnings enabled:

   .. code-block:: bash

      g++ -std=c++17 -Wall -Wextra -o program program.cpp


----


.. dropdown:: Exercise 1 -- Define a Simple Class
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Define a ``Robot`` class that models a basic robot with attributes and methods.

    **Specification**

    1. Create a header file ``robot.hpp`` with a ``Robot`` class.
    2. The class should have the following ``private`` attributes:

       - ``std::string name_`` -- the robot's name
       - ``std::string model_`` -- the robot's model
       - ``double battery_level_`` -- battery percentage (0.0 to 100.0), initialized to 100.0
       - ``bool is_active_`` -- whether the robot is active, initialized to ``false``

    3. Declare the following ``public`` methods (implement in ``robot.cpp``):

       - ``void activate()`` -- sets ``is_active_`` to ``true`` and prints a message
       - ``void deactivate()`` -- sets ``is_active_`` to ``false`` and prints a message
       - ``void move(double distance)`` -- prints a message and reduces ``battery_level_`` by ``distance * 0.5`` (only if active and battery > 0)

    4. Add a parameterized constructor that takes ``name`` and ``model``.
    5. Write a ``main.cpp`` that creates two ``Robot`` objects, activates them, moves them, and prints their status.

    **Starter Code**

    .. code-block:: cpp

       // robot.hpp
       #pragma once
       #include <string>

       class Robot {
       private:
           std::string name_;
           std::string model_;
           double battery_level_{100.0};
           bool is_active_{false};

       public:
           Robot(const std::string& name, const std::string& model);

           void activate();
           void deactivate();
           void move(double distance);
       }; // class Robot

    .. code-block:: cpp

       // main.cpp
       #include <iostream>
       #include "robot.hpp"

       int main() {
           Robot r1{"Atlas", "Humanoid"};
           Robot r2{"Spot", "Quadruped"};

           r1.activate();
           r1.move(10.0);

           r2.activate();
           r2.move(25.0);

           r1.deactivate();
       }

    **Deliverables**

    - ``robot.hpp`` with class definition
    - ``robot.cpp`` with method implementations
    - ``main.cpp`` that demonstrates creating and using objects


.. dropdown:: Exercise 2 -- Add Accessors and Mutators
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Extend the ``Robot`` class from Exercise 1 with proper accessors and mutators.

    **Specification**

    1. Add the following **accessors** (getters):

       - ``[[nodiscard]] const std::string& get_name() const noexcept``
       - ``[[nodiscard]] const std::string& get_model() const noexcept``
       - ``[[nodiscard]] double get_battery_level() const noexcept``
       - ``[[nodiscard]] bool is_active() const noexcept``

    2. Add the following **mutators** (setters):

       - ``void set_name(const std::string& name)`` -- validate that the name is not empty
       - ``void set_battery_level(double level)`` -- validate that level is between 0.0 and 100.0

    3. Update ``main.cpp`` to use the accessors and mutators.

    **Expected Output**

    .. code-block:: text

       Robot: Atlas (Humanoid), Battery: 100%
       Robot: Atlas (Humanoid), Battery: 95%
       Setting battery to 50%...
       Robot: Atlas (Humanoid), Battery: 50%

    .. dropdown:: Solution
       :class-container: sd-border-success

       .. code-block:: cpp

          [[nodiscard]] const std::string& get_name() const noexcept {
              return name_;
          }

          void set_name(const std::string& name) {
              if (name.empty()) {
                  throw std::invalid_argument("Name cannot be empty");
              }
              name_ = name;
          }

          void set_battery_level(double level) {
              if (level < 0.0 || level > 100.0) {
                  throw std::invalid_argument("Battery level must be between 0 and 100");
              }
              battery_level_ = level;
          }


.. dropdown:: Exercise 3 -- Implement Constructors
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice writing different constructor types for the ``Robot`` class.

    **Specification**

    1. Implement a **default constructor** that initializes the robot with name ``"Unknown"``, model ``"Generic"``, battery at ``100.0``, and inactive.
    2. Implement a **parameterized constructor** that takes ``name`` and ``model``.
    3. Implement a **fully parameterized constructor** that takes ``name``, ``model``, and ``battery_level``.
    4. **All constructors must use member initializer lists** -- do not use assignment in the constructor body.
    5. Add a ``print_status()`` method that prints the robot's state.

    **Starter Code**

    .. code-block:: cpp

       // robot.hpp
       #pragma once
       #include <iostream>
       #include <string>

       class Robot {
       private:
           std::string name_;
           std::string model_;
           double battery_level_{100.0};
           bool is_active_{false};

       public:
           // Default constructor
           Robot();

           // Two-parameter constructor
           Robot(const std::string& name, const std::string& model);

           // Three-parameter constructor
           Robot(const std::string& name, const std::string& model, double battery_level);

           void print_status() const;
       }; // class Robot

    .. code-block:: cpp

       // main.cpp
       #include "robot.hpp"

       int main() {
           Robot r1;
           r1.print_status();
           // Expected: Robot: Unknown (Generic), Battery: 100%, Active: No

           Robot r2{"Atlas", "Humanoid"};
           r2.print_status();
           // Expected: Robot: Atlas (Humanoid), Battery: 100%, Active: No

           Robot r3{"Spot", "Quadruped", 75.0};
           r3.print_status();
           // Expected: Robot: Spot (Quadruped), Battery: 75%, Active: No
       }

    .. dropdown:: Solution
       :class-container: sd-border-success

       .. code-block:: cpp

          Robot::Robot()
              : name_{"Unknown"}, model_{"Generic"} {}

          Robot::Robot(const std::string& name, const std::string& model)
              : name_{name}, model_{model} {}

          Robot::Robot(const std::string& name, const std::string& model, double battery_level)
              : name_{name}, model_{model}, battery_level_{battery_level} {}

          void Robot::print_status() const {
              std::cout << "Robot: " << name_ << " (" << model_
                        << "), Battery: " << battery_level_
                        << "%, Active: " << (is_active_ ? "Yes" : "No") << '\n';
          }


.. dropdown:: Exercise 4 -- Static Member Counter
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Add a ``static`` member to track the total number of ``Robot`` objects created.

    **Specification**

    1. Add a ``private`` ``static`` attribute ``inline static int robot_count_{0}`` to the ``Robot`` class.
    2. Increment ``robot_count_`` in every constructor.
    3. Add a ``static`` method ``[[nodiscard]] static int get_robot_count() noexcept`` that returns the count.
    4. Demonstrate in ``main.cpp`` that the count updates correctly as robots are created.

    **Test Code**

    .. code-block:: cpp

       // main.cpp
       #include <iostream>
       #include <memory>
       #include "robot.hpp"

       int main() {
           std::cout << "Robots: " << Robot::get_robot_count() << '\n'; // 0

           Robot r1{"Atlas", "Humanoid"};
           std::cout << "Robots: " << Robot::get_robot_count() << '\n'; // 1

           Robot r2{"Spot", "Quadruped"};
           std::cout << "Robots: " << Robot::get_robot_count() << '\n'; // 2

           {
               Robot r3{"Pepper", "Service"};
               std::cout << "Robots: " << Robot::get_robot_count() << '\n'; // 3
           }
           // r3 is destroyed here, but the count remains 3
           // (we are only counting creations, not tracking live objects)
           std::cout << "Robots: " << Robot::get_robot_count() << '\n'; // 3

           auto r4 = std::make_unique<Robot>("Create3", "Differential");
           std::cout << "Robots: " << Robot::get_robot_count() << '\n'; // 4
       }

    **Deliverables**

    - Updated ``robot.hpp`` with ``static`` member and method
    - Updated constructors that increment the counter
    - ``main.cpp`` demonstrating the counter


.. dropdown:: Exercise 5 -- const Correctness in Classes
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice ``const``-correctness by implementing a ``Waypoint`` class.

    **Specification**

    1. Define a ``Waypoint`` class with:

       - ``private`` attributes: ``double x_``, ``double y_``, ``const std::string label_``

    2. Implement a parameterized constructor using a member initializer list (required because ``label_`` is ``const``).

    3. Implement these methods with correct ``const`` qualifiers:

       - ``[[nodiscard]] double get_x() const noexcept``
       - ``[[nodiscard]] double get_y() const noexcept``
       - ``[[nodiscard]] const std::string& get_label() const noexcept``
       - ``void set_x(double x) noexcept``
       - ``void set_y(double y) noexcept``
       - ``[[nodiscard]] double distance_to(const Waypoint& other) const noexcept`` -- compute Euclidean distance
       - ``void print() const``

    4. In ``main.cpp``, create both a ``const`` and non-``const`` ``Waypoint``. Demonstrate which methods can be called on each.

    **Test Code**

    .. code-block:: cpp

       #include <cmath>
       #include <iostream>
       #include "waypoint.hpp"

       int main() {
           Waypoint wp1{3.0, 4.0, "start"};
           const Waypoint wp2{6.0, 8.0, "goal"};

           // Both work: get_x() is const
           std::cout << "wp1.x = " << wp1.get_x() << '\n';
           std::cout << "wp2.x = " << wp2.get_x() << '\n';

           // Only works on non-const object
           wp1.set_x(0.0);
           // wp2.set_x(0.0);  // Error: wp2 is const

           // distance_to is const, so both work
           std::cout << "Distance: " << wp1.distance_to(wp2) << '\n';
           std::cout << "Distance: " << wp2.distance_to(wp1) << '\n';
       }

    **Deliverables**

    - ``waypoint.hpp`` and ``waypoint.cpp`` with proper ``const``-correctness
    - ``main.cpp`` demonstrating ``const`` vs non-``const`` object behavior


.. dropdown:: Exercise 6 (Challenge) -- Design a Sensor Class
    :icon: gear
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Design and implement a ``Sensor`` class that integrates all OOP concepts from this lecture, including ``std::optional`` and ``std::string_view``.

    **Specification**

    1. Define a ``Sensor`` class in ``sensor.hpp`` with:

       - ``private`` attributes:

         - ``std::string id_`` -- unique sensor identifier
         - ``std::string type_`` -- sensor type (e.g., "lidar", "camera", "imu")
         - ``bool is_calibrated_`` -- initialized to ``false``
         - ``double update_frequency_`` -- in Hz
         - ``inline static int sensor_count_{0}``

       - Constructors:

         - Default constructor
         - Parameterized constructor taking ``id``, ``type``, and ``update_frequency``
         - All using member initializer lists

       - Accessors for all attributes (with ``[[nodiscard]]``, ``const``, ``noexcept`` where appropriate)
       - Mutator for ``update_frequency_`` with validation (must be positive)
       - ``void calibrate()`` -- sets ``is_calibrated_`` to ``true``
       - ``void print_info() const`` -- prints all sensor information
       - ``static int get_sensor_count() noexcept``

    2. Use ``std::optional`` to add a method ``std::optional<double> get_reading() const`` that returns a reading only if the sensor is calibrated. If not calibrated, return ``std::nullopt``.

    3. Use ``std::string_view`` for constructor parameters that only need to read string data.

    4. Demonstrate with ``const`` and non-``const`` sensors.

    **Starter Code**

    .. code-block:: cpp

       // sensor.hpp
       #pragma once
       #include <iostream>
       #include <optional>
       #include <string>
       #include <string_view>

       class Sensor {
       private:
           std::string id_;
           std::string type_;
           bool is_calibrated_{false};
           double update_frequency_{0.0};
           inline static int sensor_count_{0};

       public:
           Sensor();
           Sensor(std::string_view id, std::string_view type, double update_frequency);

           // Accessors
           [[nodiscard]] const std::string& get_id() const noexcept;
           [[nodiscard]] const std::string& get_type() const noexcept;
           [[nodiscard]] bool is_calibrated() const noexcept;
           [[nodiscard]] double get_update_frequency() const noexcept;

           // Mutators
           void set_update_frequency(double frequency);

           // Methods
           void calibrate();
           void print_info() const;
           [[nodiscard]] std::optional<double> get_reading() const;

           // Static
           [[nodiscard]] static int get_sensor_count() noexcept;
       }; // class Sensor

    .. code-block:: cpp

       // main.cpp
       #include <iostream>
       #include "sensor.hpp"

       int main() {
           std::cout << "Sensors: " << Sensor::get_sensor_count() << '\n'; // 0

           Sensor lidar{"lidar_front", "lidar", 10.0};
           Sensor camera{"camera_rgb", "camera", 30.0};
           Sensor imu;

           std::cout << "Sensors: " << Sensor::get_sensor_count() << '\n'; // 3

           lidar.print_info();

           // Try reading before calibration
           auto reading = lidar.get_reading();
           if (!reading) {
               std::cout << "No reading: sensor not calibrated\n";
           }

           // Calibrate and try again
           lidar.calibrate();
           reading = lidar.get_reading();
           if (reading) {
               std::cout << "Reading: " << reading.value() << '\n';
           }

           // const sensor
           const Sensor const_sensor{"imu_center", "imu", 200.0};
           const_sensor.print_info();
           // const_sensor.calibrate();  // Error: cannot call non-const method
       }

    **Deliverables**

    - ``sensor.hpp`` with full class definition
    - ``sensor.cpp`` with all method implementations
    - ``main.cpp`` demonstrating all features
