====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 9: OOP Advanced.
Work through them in order, as each exercise builds on the skills from the
previous one. Write, compile, and run each program to verify your understanding.

.. note::

   Compile all programs with warnings enabled:

   .. code-block:: bash

      g++ -std=c++17 -Wall -Wextra -o program program.cpp


----


.. dropdown:: Exercise 1 -- Basic Inheritance
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice creating a base class and a derived class using public
    inheritance, and understand how constructors are chained.

    **Specification**

    1. Create a ``Vehicle`` base class with:

       - A ``protected`` ``std::string`` attribute ``name_``.
       - A ``protected`` ``int`` attribute ``year_``.
       - A constructor that initializes both attributes.
       - A ``public`` method ``display_info()`` that prints the vehicle name and year.

    2. Create a ``Car`` derived class (public inheritance from ``Vehicle``) with:

       - A ``private`` ``int`` attribute ``num_doors_``.
       - A constructor that takes ``name``, ``year``, and ``num_doors``, and explicitly calls the ``Vehicle`` constructor.
       - A ``public`` method ``display_car_info()`` that calls ``display_info()`` and also prints the number of doors.

    3. In ``main()``, create a ``Car`` object and call ``display_car_info()``.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>
           #include <string>

           class Vehicle {
            protected:
             std::string name_;
             int year_;
            public:
             Vehicle(const std::string& name, int year)
                 : name_{name}, year_{year} {}

             void display_info() const {
                 std::cout << "Vehicle: " << name_ << " | Year: " << year_ << '\n';
             }
           };

           class Car : public Vehicle {
            private:
             int num_doors_;
            public:
             Car(const std::string& name, int year, int num_doors)
                 : Vehicle(name, year), num_doors_{num_doors} {}

             void display_car_info() const {
                 display_info();
                 std::cout << "Doors: " << num_doors_ << '\n';
             }
           };

           int main() {
               Car my_car{"Toyota Camry", 2024, 4};
               my_car.display_car_info();
               return 0;
           }

        **Expected output:**

        .. code-block:: text

           Vehicle: Toyota Camry | Year: 2024
           Doors: 4


.. dropdown:: Exercise 2 -- Method Overriding with ``virtual``
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Understand the difference between static binding (no ``virtual``) and
    dynamic binding (with ``virtual``), and practice using ``override``.

    **Specification**

    1. Create a ``Vehicle`` base class with:

       - A ``virtual`` method ``drive()`` that prints ``"Vehicle is driving"``.
       - A ``virtual`` destructor (``= default``).

    2. Create a ``RoboTaxi`` class (derived from ``Vehicle``) with:

       - An overridden ``drive()`` method that prints ``"RoboTaxi is driving autonomously"``.
       - Use the ``override`` keyword.

    3. Create a ``Taxi`` class (derived from ``Vehicle``) with:

       - An overridden ``drive()`` method that prints ``"Taxi is driving with a human driver"``.

    4. In ``main()``:

       a. Create a ``std::unique_ptr<Vehicle>`` pointing to a ``RoboTaxi``.
       b. Create a ``std::unique_ptr<Vehicle>`` pointing to a ``Taxi``.
       c. Call ``drive()`` on both pointers and observe runtime polymorphism.
       d. Create a ``std::vector<std::unique_ptr<Vehicle>>`` and iterate through it calling ``drive()`` on each element.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>
           #include <memory>
           #include <vector>

           class Vehicle {
            public:
             virtual ~Vehicle() = default;
             virtual void drive() const {
                 std::cout << "Vehicle is driving\n";
             }
           };

           class RoboTaxi : public Vehicle {
            public:
             void drive() const override {
                 std::cout << "RoboTaxi is driving autonomously\n";
             }
           };

           class Taxi : public Vehicle {
            public:
             void drive() const override {
                 std::cout << "Taxi is driving with a human driver\n";
             }
           };

           int main() {
               // Individual polymorphic pointers
               std::unique_ptr<Vehicle> rt = std::make_unique<RoboTaxi>();
               std::unique_ptr<Vehicle> tx = std::make_unique<Taxi>();

               rt->drive();  // RoboTaxi is driving autonomously
               tx->drive();  // Taxi is driving with a human driver

               // Polymorphic collection
               std::vector<std::unique_ptr<Vehicle>> fleet;
               fleet.push_back(std::make_unique<RoboTaxi>());
               fleet.push_back(std::make_unique<Taxi>());
               fleet.push_back(std::make_unique<RoboTaxi>());

               std::cout << "\nFleet dispatch:\n";
               for (const auto& v : fleet) {
                   v->drive();
               }

               return 0;
           }

        **Expected output:**

        .. code-block:: text

           RoboTaxi is driving autonomously
           Taxi is driving with a human driver

           Fleet dispatch:
           RoboTaxi is driving autonomously
           Taxi is driving with a human driver
           RoboTaxi is driving autonomously


.. dropdown:: Exercise 3 -- Abstract Class with Pure Virtual Methods
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice defining an abstract base class with pure virtual methods and
    implementing concrete derived classes.

    **Specification**

    1. Create an abstract ``Sensor`` class with:

       - A ``protected`` ``std::string`` attribute ``sensor_id_``.
       - A constructor that initializes ``sensor_id_``.
       - A ``virtual`` destructor (``= default``).
       - A pure virtual method ``double read_value() const = 0``.
       - A pure virtual method ``std::string get_type() const = 0``.
       - A non-virtual method ``void display() const`` that prints the sensor ID, type, and current reading.

    2. Create a ``TemperatureSensor`` class that:

       - Inherits from ``Sensor``.
       - Has a ``private`` ``double`` attribute ``temperature_``.
       - Implements ``read_value()`` to return ``temperature_``.
       - Implements ``get_type()`` to return ``"Temperature"``.

    3. Create a ``DistanceSensor`` class that:

       - Inherits from ``Sensor``.
       - Has a ``private`` ``double`` attribute ``distance_``.
       - Implements ``read_value()`` to return ``distance_``.
       - Implements ``get_type()`` to return ``"Distance"``.

    4. In ``main()``, create a vector of ``unique_ptr<Sensor>`` and add both sensor types. Iterate and call ``display()`` on each.

    5. Verify that attempting to instantiate ``Sensor`` directly causes a compile error.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>
           #include <memory>
           #include <string>
           #include <vector>

           class Sensor {
            protected:
             std::string sensor_id_;
            public:
             Sensor(const std::string& id) : sensor_id_{id} {}
             virtual ~Sensor() = default;

             virtual double read_value() const = 0;
             virtual std::string get_type() const = 0;

             void display() const {
                 std::cout << "[" << get_type() << "] "
                           << sensor_id_ << ": " << read_value() << '\n';
             }
           };

           class TemperatureSensor : public Sensor {
            private:
             double temperature_;
            public:
             TemperatureSensor(const std::string& id, double temp)
                 : Sensor(id), temperature_{temp} {}

             double read_value() const override { return temperature_; }
             std::string get_type() const override { return "Temperature"; }
           };

           class DistanceSensor : public Sensor {
            private:
             double distance_;
            public:
             DistanceSensor(const std::string& id, double dist)
                 : Sensor(id), distance_{dist} {}

             double read_value() const override { return distance_; }
             std::string get_type() const override { return "Distance"; }
           };

           int main() {
               std::vector<std::unique_ptr<Sensor>> sensors;
               sensors.push_back(std::make_unique<TemperatureSensor>("TEMP-01", 23.5));
               sensors.push_back(std::make_unique<DistanceSensor>("DIST-01", 1.75));
               sensors.push_back(std::make_unique<TemperatureSensor>("TEMP-02", 19.8));

               for (const auto& s : sensors) {
                   s->display();
               }

               // Sensor s{"test"};  // ERROR: cannot instantiate abstract class

               return 0;
           }

        **Expected output:**

        .. code-block:: text

           [Temperature] TEMP-01: 23.5
           [Distance] DIST-01: 1.75
           [Temperature] TEMP-02: 19.8


.. dropdown:: Exercise 4 -- Composition vs. Inheritance
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Understand the difference between "has-a" (composition) and "is-a"
    (inheritance) relationships by implementing both.

    **Specification**

    1. Create an ``Engine`` class with:

       - A ``private`` ``int`` attribute ``horsepower_``.
       - A ``public`` method ``start()`` that prints ``"Engine started (<hp> HP)"``.
       - A ``public`` method ``stop()`` that prints ``"Engine stopped"``.

    2. Create a ``GPS`` class with:

       - A ``private`` ``std::string`` attribute ``model_``.
       - A ``public`` method ``get_location()`` that prints ``"GPS (<model>): Location acquired"``.

    3. Create a ``Vehicle`` base class with:

       - **Composition**: An ``Engine`` member and a ``GPS`` member (has-a relationships).
       - A ``virtual`` destructor (``= default``).
       - A ``virtual`` method ``describe()`` that prints the vehicle type.

    4. Create a ``Truck`` class (derived from ``Vehicle``) that:

       - Has an additional ``private`` ``double`` attribute ``payload_capacity_``.
       - Overrides ``describe()`` to include payload capacity.

    5. In ``main()``, create a ``Truck``, start its engine, get its GPS location, and call ``describe()``.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>
           #include <string>

           class Engine {
            private:
             int horsepower_;
            public:
             Engine(int hp) : horsepower_{hp} {}
             void start() const {
                 std::cout << "Engine started (" << horsepower_ << " HP)\n";
             }
             void stop() const {
                 std::cout << "Engine stopped\n";
             }
           };

           class GPS {
            private:
             std::string model_;
            public:
             GPS(const std::string& model) : model_{model} {}
             void get_location() const {
                 std::cout << "GPS (" << model_ << "): Location acquired\n";
             }
           };

           class Vehicle {
            protected:
             Engine engine_;   // Composition: Vehicle "has-a" Engine
             GPS gps_;         // Composition: Vehicle "has-a" GPS
             std::string name_;
            public:
             Vehicle(const std::string& name, int hp, const std::string& gps_model)
                 : engine_{hp}, gps_{gps_model}, name_{name} {}
             virtual ~Vehicle() = default;

             void start() const { engine_.start(); }
             void stop() const { engine_.stop(); }
             void locate() const { gps_.get_location(); }

             virtual void describe() const {
                 std::cout << "Vehicle: " << name_ << '\n';
             }
           };

           // Inheritance: Truck "is-a" Vehicle
           class Truck : public Vehicle {
            private:
             double payload_capacity_;
            public:
             Truck(const std::string& name, int hp, const std::string& gps_model,
                   double payload)
                 : Vehicle(name, hp, gps_model), payload_capacity_{payload} {}

             void describe() const override {
                 std::cout << "Truck: " << name_
                           << " | Payload: " << payload_capacity_ << " tons\n";
             }
           };

           int main() {
               Truck my_truck{"Ford F-150", 400, "Garmin DriveTrack", 1.5};
               my_truck.start();
               my_truck.locate();
               my_truck.describe();
               my_truck.stop();
               return 0;
           }

        **Expected output:**

        .. code-block:: text

           Engine started (400 HP)
           GPS (Garmin DriveTrack): Location acquired
           Truck: Ford F-150 | Payload: 1.5 tons
           Engine stopped


.. dropdown:: Exercise 5 -- Virtual Destructors
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Understand why virtual destructors are essential in polymorphic
    hierarchies and observe the difference between virtual and non-virtual
    destructors.

    **Specification**

    1. Create a ``Base`` class with:

       - A **non-virtual** destructor that prints ``"~Base()"``.

    2. Create a ``Derived`` class (derived from ``Base``) with:

       - A ``private`` ``int*`` attribute ``data_`` allocated with ``new int[100]``.
       - A destructor that ``delete[]``'s ``data_`` and prints ``"~Derived()"``.

    3. In ``main()``:

       a. Create a ``Derived`` object on the stack and observe both destructors run.
       b. Create a ``Base*`` pointer to a ``new Derived()`` object, then ``delete`` it. Observe that only ``~Base()`` runs (resource leak).

    4. Now fix the problem by making the ``Base`` destructor ``virtual``. Re-run step 3b and confirm both destructors run.

    5. Run the fixed and unfixed versions through Valgrind and compare the memory leak reports.

    .. dropdown:: Solution
        :class-container: sd-border-success

        **Part 1 -- Non-virtual destructor (BROKEN):**

        .. code-block:: cpp

           #include <iostream>

           class Base {
            public:
             ~Base() { std::cout << "~Base()\n"; }  // NOT virtual
           };

           class Derived : public Base {
            private:
             int* data_;
            public:
             Derived() : data_{new int[100]} {
                 std::cout << "Derived() allocated 100 ints\n";
             }
             ~Derived() {
                 delete[] data_;
                 std::cout << "~Derived() freed memory\n";
             }
           };

           int main() {
               std::cout << "--- Stack object (both dtors run) ---\n";
               { Derived d; }

               std::cout << "\n--- Heap via Base* (LEAK!) ---\n";
               Base* ptr = new Derived();
               delete ptr;  // Only ~Base() runs!

               return 0;
           }

        **Part 2 -- Virtual destructor (FIXED):**

        .. code-block:: cpp

           class Base {
            public:
             virtual ~Base() { std::cout << "~Base()\n"; }  // NOW virtual
           };

           // Derived class stays the same

        With ``virtual``, ``delete ptr`` correctly calls ``~Derived()`` first,
        then ``~Base()``.


.. dropdown:: Exercise 6 -- Challenge: Shape Hierarchy with Polymorphic Area Calculation
    :icon: rocket
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Build a complete shape hierarchy using abstract classes, pure virtual
    methods, ``override``, ``final``, virtual destructors, and smart pointers.

    **Specification**

    1. Create an abstract ``Shape`` class with:

       - A ``virtual`` destructor (``= default``).
       - A pure virtual method ``double area() const = 0``.
       - A pure virtual method ``std::string name() const = 0``.
       - A non-virtual method ``void print() const`` that prints the shape name and area.

    2. Create the following concrete classes:

       - ``Circle`` with a ``double`` radius. ``area()`` returns pi * r * r.
       - ``Rectangle`` with ``double`` width and height. ``area()`` returns width * height.
       - ``Triangle`` with ``double`` base and height. ``area()`` returns 0.5 * base * height.
       - ``Square final`` that inherits from ``Rectangle``. Constructor takes a single side length. Mark the class ``final``.

    3. In ``main()``:

       a. Create a ``std::vector<std::unique_ptr<Shape>>`` containing one of each shape type.
       b. Iterate through the vector and call ``print()`` on each shape.
       c. Calculate and print the total area of all shapes.
       d. Find and print the shape with the largest area.

    4. Verify that attempting to derive from ``Square`` causes a compile error.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <cmath>
           #include <iostream>
           #include <memory>
           #include <string>
           #include <vector>

           class Shape {
            public:
             virtual ~Shape() = default;
             virtual double area() const = 0;
             virtual std::string name() const = 0;

             void print() const {
                 std::cout << name() << ": area = " << area() << '\n';
             }
           };

           class Circle : public Shape {
            private:
             double radius_;
            public:
             Circle(double radius) : radius_{radius} {}
             double area() const override { return M_PI * radius_ * radius_; }
             std::string name() const override { return "Circle"; }
           };

           class Rectangle : public Shape {
            protected:
             double width_;
             double height_;
            public:
             Rectangle(double width, double height)
                 : width_{width}, height_{height} {}
             double area() const override { return width_ * height_; }
             std::string name() const override { return "Rectangle"; }
           };

           class Triangle : public Shape {
            private:
             double base_;
             double height_;
            public:
             Triangle(double base, double height)
                 : base_{base}, height_{height} {}
             double area() const override { return 0.5 * base_ * height_; }
             std::string name() const override { return "Triangle"; }
           };

           class Square final : public Rectangle {
            public:
             Square(double side) : Rectangle(side, side) {}
             std::string name() const override { return "Square"; }
           };

           // class SpecialSquare : public Square {};  // ERROR: Square is final

           int main() {
               std::vector<std::unique_ptr<Shape>> shapes;
               shapes.push_back(std::make_unique<Circle>(5.0));
               shapes.push_back(std::make_unique<Rectangle>(4.0, 6.0));
               shapes.push_back(std::make_unique<Triangle>(3.0, 8.0));
               shapes.push_back(std::make_unique<Square>(5.0));

               std::cout << "--- All Shapes ---\n";
               double total_area{0.0};
               for (const auto& s : shapes) {
                   s->print();
                   total_area += s->area();
               }

               std::cout << "\nTotal area: " << total_area << '\n';

               // Find largest shape
               const Shape* largest{nullptr};
               double max_area{0.0};
               for (const auto& s : shapes) {
                   if (s->area() > max_area) {
                       max_area = s->area();
                       largest = s.get();
                   }
               }

               if (largest) {
                   std::cout << "Largest shape: ";
                   largest->print();
               }

               return 0;
           }

        **Expected output:**

        .. code-block:: text

           --- All Shapes ---
           Circle: area = 78.5398
           Rectangle: area = 24
           Triangle: area = 12
           Square: area = 25

           Total area: 139.54
           Largest shape: Circle: area = 78.5398
