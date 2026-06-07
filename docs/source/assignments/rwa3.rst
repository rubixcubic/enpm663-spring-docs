====================================================
RWA3 -- Smart Pointers and OOP
====================================================

Overview
--------

In this assignment you **redesign** the warehouse system using
object-oriented principles. You will create a class hierarchy for
robots and sensors, manage object lifetimes with smart pointers, and
apply polymorphism so that different robot types exhibit distinct
behaviors --- all without a single raw ``new`` or ``delete``.


Learning Objectives
-------------------

After completing this assignment you will be able to:

1. Design class hierarchies with inheritance.
2. Apply encapsulation with proper access specifiers.
3. Use **virtual functions** for runtime polymorphism.
4. Manage object lifetimes with ``std::unique_ptr`` and
   ``std::shared_ptr``.
5. Implement proper constructors, destructors, and reason about
   the **Rule of Five**.
6. Apply ``const``-correctness throughout a multi-class project.


Requirements
------------

.. dropdown:: R1 -- Class Design
   :open:

   Create a ``Robot`` **base class** with:

   * **Attributes** (``private``): ``id_`` (``int``), ``name_``
     (``std::string``), ``x_position_``, ``y_position_``
     (``double``), ``battery_level_`` (``double``).
   * **Public interface**: ``move()``, ``report_status()``, getters,
     and setters where appropriate.
   * A **default constructor** and a **parameterized constructor**
     using a member initialization list.
   * A **virtual destructor**.

   .. code-block:: cpp

      class Robot {
       public:
          Robot() = default;

          Robot(int id, const std::string& name,
                double x, double y, double battery)
              : id_{id}, name_{name},
                x_position_{x}, y_position_{y},
                battery_level_{battery} {}

          virtual ~Robot() = default;

          virtual void move(double dx, double dy);
          virtual std::string report_status() const;

          // Getters
          int get_id() const { return id_; }
          const std::string& get_name() const { return name_; }

       private:
          int id_{0};
          std::string name_;
          double x_position_{0.0};
          double y_position_{0.0};
          double battery_level_{100.0};
      };

.. dropdown:: R2 -- Inheritance
   :open:

   Create three derived classes, each with distinct characteristics:

   .. grid:: 3
      :gutter: 3

      .. grid-item-card:: ScoutRobot
         :class-header: sd-bg-info sd-text-white

         * Fast movement speed.
         * Small payload capacity.
         * Overrides ``move()`` --- moves farther per call.
         * Overrides ``report_status()`` --- includes scouting range.

      .. grid-item-card:: CarrierRobot
         :class-header: sd-bg-success sd-text-white

         * Slow movement speed.
         * Large payload capacity.
         * Overrides ``move()`` --- moves less per call.
         * Overrides ``report_status()`` --- includes payload weight.

      .. grid-item-card:: DroneRobot
         :class-header: sd-bg-warning sd-text-white

         * Flies (ignores ground obstacles).
         * Limited battery drain per move.
         * Overrides ``move()`` --- drains battery faster.
         * Overrides ``report_status()`` --- includes altitude.

   .. code-block:: cpp

      class ScoutRobot : public Robot {
       public:
          ScoutRobot(int id, const std::string& name,
                     double x, double y, double battery,
                     double scouting_range)
              : Robot{id, name, x, y, battery},
                scouting_range_{scouting_range} {}

          void move(double dx, double dy) override;
          std::string report_status() const override;

       private:
          double scouting_range_{50.0};
      };

.. dropdown:: R3 -- Polymorphism
   :open:

   * Store all robots in a
     ``std::vector<std::unique_ptr<Robot>>``.
   * Call ``move()`` and ``report_status()`` through base-class
     pointers.
   * Demonstrate **runtime polymorphism**: each robot type produces
     different output from the same function call.

   .. code-block:: cpp

      std::vector<std::unique_ptr<Robot>> robots;

      robots.push_back(std::make_unique<ScoutRobot>(
          1, "Scout_A", 0.0, 0.0, 100.0, 50.0));
      robots.push_back(std::make_unique<CarrierRobot>(
          2, "Carrier_B", 10.0, 5.0, 95.0, 200.0));
      robots.push_back(std::make_unique<DroneRobot>(
          3, "Drone_C", 0.0, 0.0, 80.0, 25.0));

      for (const auto& robot : robots) {
          robot->move(5.0, 3.0);
          std::cout << robot->report_status() << '\n';
      }

.. dropdown:: R4 -- Smart Pointers
   :open:

   * Use ``std::unique_ptr`` for **exclusive ownership** of robots
     (the ``Warehouse`` class owns each robot).
   * Use ``std::shared_ptr`` for **shared sensors** --- multiple
     robots may share the same physical sensor.
   * Use ``std::weak_ptr`` for **non-owning references** (e.g., a
     robot holds a weak reference to a sensor it does not own).
   * There must be **no** raw ``new`` or ``delete`` anywhere in
     your code.

   .. code-block:: cpp

      // Shared sensor
      auto temp_sensor{
          std::make_shared<TemperatureSensor>("Zone_A", 22.5)};

      // Multiple robots share the sensor
      scout->set_sensor(temp_sensor);   // stores shared_ptr
      carrier->set_sensor(temp_sensor); // same sensor

      // Weak reference example
      std::weak_ptr<TemperatureSensor> weak_ref{temp_sensor};
      if (auto locked{weak_ref.lock()}) {
          std::cout << "Sensor reading: "
                    << locked->read() << '\n';
      }

.. dropdown:: R5 -- Warehouse Class
   :open:

   Create a ``Warehouse`` class that manages the entire simulation:

   * Owns robots via ``std::vector<std::unique_ptr<Robot>>``.
   * Methods:

     - ``add_robot(std::unique_ptr<Robot> robot)``
     - ``remove_robot(int id)``
     - ``find_robot(int id) const``
     - ``print_all_robots() const``

   * Apply ``const``-correctness: mark every method and parameter
     that does not modify state as ``const``.

   .. code-block:: cpp

      class Warehouse {
       public:
          void add_robot(std::unique_ptr<Robot> robot);
          void remove_robot(int id);
          Robot* find_robot(int id) const;
          void print_all_robots() const;

       private:
          std::string name_{"Default Warehouse"};
          std::vector<std::unique_ptr<Robot>> robots_;
      };

.. dropdown:: R6 -- Sensor Hierarchy
   :open:

   Create a ``Sensor`` base class with derived types:

   * ``TemperatureSensor`` --- ``read()`` returns a temperature
     value.
   * ``HumiditySensor`` --- ``read()`` returns a humidity
     percentage.
   * ``read()`` is a **virtual** method that returns different data
     per sensor type.
   * Sensors are shared among robots via ``std::shared_ptr``.

   .. code-block:: cpp

      class Sensor {
       public:
          Sensor(const std::string& location)
              : location_{location} {}
          virtual ~Sensor() = default;

          virtual double read() const = 0;
          const std::string& get_location() const {
              return location_;
          }

       private:
          std::string location_;
      };

      class TemperatureSensor : public Sensor {
       public:
          TemperatureSensor(const std::string& location,
                           double baseline)
              : Sensor{location}, baseline_{baseline} {}

          double read() const override {
              // Simulate slight variation
              return baseline_ + (std::rand() % 10 - 5) * 0.1;
          }

       private:
          double baseline_{22.0};
      };


Deliverables
------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Item
     - Description
   * - Header files (``.hpp``)
     - One header per class (``robot.hpp``, ``scout_robot.hpp``,
       ``warehouse.hpp``, ``sensor.hpp``, etc.).
   * - Source files (``.cpp``)
     - Corresponding implementations and ``main.cpp``.
   * - ``CMakeLists.txt``
     - Build configuration targeting C++17 or later.
   * - UML class diagram
     - Shows the full class hierarchy and relationships.
   * - Valgrind output
     - Demonstrates zero memory leaks (even though you use smart
       pointers, this confirms correct usage).


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Category
     - Weight
     - Criteria
   * - OOP Design
     - 30 %
     - Proper class hierarchy, encapsulation, access specifiers,
       constructors with member initialization lists.
   * - Smart Pointer Usage
     - 25 %
     - Correct use of ``unique_ptr``, ``shared_ptr``, and
       ``weak_ptr``; no raw ``new`` / ``delete``.
   * - Polymorphism
     - 20 %
     - Virtual methods produce distinct behavior per derived class
       when called through base-class pointers.
   * - Code Quality
     - 15 %
     - ``const``-correctness, ``snake_case`` naming, uniform
       initialization, ``'\n'`` usage.
   * - Documentation
     - 10 %
     - Doxygen comments, UML diagram, inline comments for
       non-obvious logic.


Tips
----

.. admonition:: Design Before You Code
   :class: tip

   Sketch your UML class diagram first. Deciding which class owns
   which resource *before* writing code prevents painful refactors
   later.

.. admonition:: One Class at a Time
   :class: tip

   Implement and test the ``Robot`` base class before creating any
   derived classes. Then add one derived class, test polymorphism,
   and repeat.

.. admonition:: Smart Pointer Cheat Sheet
   :class: tip

   * **unique_ptr** --- sole owner, cannot be copied, can be moved.
   * **shared_ptr** --- reference-counted, multiple owners.
   * **weak_ptr** --- observes a ``shared_ptr`` without affecting
     its reference count.
