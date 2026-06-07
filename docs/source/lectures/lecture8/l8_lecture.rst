====================================================
Lecture
====================================================


Core Principles of OOP
============================

Object-Oriented Programming organizes software around objects -- digital models of real-world things that hold data and perform actions. This approach helps make code more understandable, reusable, and easier to manage.

OOP is built around a set of fundamental principles that shape how code is structured, organized, and maintained. These concepts help developers build modular, scalable, and maintainable systems.

- **Encapsulation**: Groups data and the methods that operate on it into objects, shielding internal details from external access.
- **Abstraction**: Simplifies complexity by exposing only essential features while hiding the underlying implementation.
- **Inheritance**: Enables new classes to reuse and extend the functionality of existing ones, fostering code reuse and hierarchy.
- **Polymorphism**: Allows different objects to be treated uniformly through a common interface, supporting flexible and extensible code.

Advantages and Disadvantages
-----------------------------

.. grid:: 2

   .. grid-item-card:: Advantages
      :class-card: sd-border-success

      - **Modularity** -- Decomposes complex problems into manageable, self-contained components.
      - **Reusability** -- Promotes code reuse through inheritance and shared behaviors.
      - **Flexibility** -- Enables dynamic behavior via polymorphism and interchangeable interfaces.
      - **Maintainability** -- Facilitates localized changes and clearer code organization.

   .. grid-item-card:: Disadvantages
      :class-card: sd-border-warning

      - **Learning Curve** -- Requires mastery of abstract concepts and design patterns.
      - **Design Overhead** -- Often demands more upfront planning and structure.
      - **Code Size** -- Object-oriented programs can be more verbose than procedural ones.
      - **Performance Overhead** -- May incur runtime costs (e.g., due to dynamic dispatch).

.. warning::

   OOP is not a one-size-fits-all solution. Not all problems map naturally to objects and classes.


Classes and Objects
============================

Classes
--------

A class is a blueprint or template for creating objects.

.. figure:: /_static/images/l8/vehicle_blueprint.png
   :alt: Vehicle blueprint
   :align: center
   :width: 30%

   A class is a blueprint for creating objects.

A class bundles two main things: **attributes** and **methods**.

- **Attributes (Member Data):** These are the properties or characteristics of the object (data). They represent its state.

  - Blueprint (Class): ``Vehicle``
  - Attributes: ``color_``, ``model_``, ``is_running_``

- **Methods (Member Functions):** These are the functions or actions that an object can perform (behavior).

  - Blueprint (Class): ``Vehicle``
  - Methods: ``start_engine()``, ``stop_engine()``, ``drive()``

Defining a Class
^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // vehicle.hpp
   #include <string>

   class Vehicle {
   private:
       /* Attributes */
       std::string color_;
       std::string model_;
       bool is_running_{false};

   public:
       /* Constructor */
       Vehicle(const std::string& color, const std::string& model)
           : color_{color}, model_{model} {}
       /* Methods */
       void stop_engine();
       void start_engine();
       void drive();
       /* Accessors/Mutators */
       bool get_is_running() const { return is_running_; }
       std::string get_model() const { return model_; }
   }; // class Vehicle

Key conventions:

- Classes are defined in header files.
- File names use snake_case naming convention.
- Use the ``class`` keyword to define a class.
- Class names use PascalCase naming convention.
- Class definition ends with a semicolon (``;``).
- Add an end-of-class comment.
- Access specifiers control member visibility.
- Attributes are ``private`` with a trailing underscore (ROS naming convention).
- Attributes can be initialized in the class (e.g., ``bool is_running_{false}``).
- Each class should have at least one explicit constructor.
- Methods are declared in the class and implemented in source files (``.cpp``).
- Accessors and mutators can be implemented directly in the class.


Objects
--------

An object is a concrete instance of a class. You cannot drive a blueprint, but you can drive a physical vehicle that was built from the blueprint.

.. figure:: /_static/images/l8/vehicle_objects.png
   :alt: Vehicle objects
   :align: center
   :width: 30%

   Objects are instances of a class.

State and Behavior
^^^^^^^^^^^^^^^^^^^

.. grid:: 2

   .. grid-item-card:: State (Attributes)
      :class-card: sd-border-info

      This is the object's unique data. While the class defines which attributes an object should have, the object itself holds the specific values.

      - ``blue_car.color_ = "blue"``
      - ``blue_car.model_ = "Wraith"``
      - ``blue_car.is_running_ = false``

   .. grid-item-card:: Behavior (Methods)
      :class-card: sd-border-info

      These are the actions the object can perform. When you call a method, you are doing it on that specific object, and it may change that object's state.

      - ``blue_car.start_engine()``
      - ``blue_car.stop_engine()``
      - ``blue_car.drive()``

.. admonition:: Key Insight
   :class: tip

   Each object is unique: if ``blue_car1`` is destroyed, ``blue_car2`` remains unaffected. Each object has its own set of attributes.

.. figure:: /_static/images/l8/objects_attributes.png
   :alt: Objects have their own attributes
   :align: center
   :width: 50%

   Each object has its own copy of the attributes.

.. admonition:: Shared Methods
   :class: tip

   All objects share the same methods. For example, the same ``start_engine()`` is used by all vehicles.

.. figure:: /_static/images/l8/objects_methods.png
   :alt: Objects share methods
   :align: center
   :width: 60%

   All objects of a class share the same method code.


Instantiation
--------------

Instantiation is the process of creating a new, specific object (an "instance") from a class (the "blueprint").

.. figure:: /_static/images/l8/instantiation.png
   :alt: Instantiation process
   :align: center
   :width: 60%

   Instantiation creates objects from a class.

.. code-block:: cpp

   #include <memory>
   #include <iostream>
   #include "vehicle.hpp"

   int main() {
       // Stack allocation
       Vehicle stack_car{"gray", "civic"};
       stack_car.start_engine();
       std::cout << stack_car.get_model() << " is "
                 << (stack_car.is_running() ? "running" : "stopped") << '\n';

       // Dynamic allocation with smart pointers
       auto heap_car = std::make_unique<Vehicle>("gray", "civic");
       heap_car->start_engine();
       std::cout << heap_car->get_model() << " is "
                 << (heap_car->is_running() ? "running" : "stopped") << '\n';
   }


Design Phase
============================

The design phase in OOP is crucial as it establishes the blueprint for the application. It involves transforming the requirements into a workable structure that serves as a foundation for further software development.

- The **Requirement Analysis** clearly describes what the system is supposed to achieve.
- The **Modeling Phase** represents and visualizes the system's structure and behavior through diagrams.

Requirement Analysis
---------------------

The requirement analysis defines *what* the system must do before designing *how* it will work.

1. **Functional Requirements** -- Define what the system must do and which specific capabilities it must provide.
2. **Non-Functional Requirements** -- Specify how well the system must perform in terms of quality attributes like performance, reliability, and safety.
3. **Technical Constraints** -- Establish design limitations and architectural principles that restrict implementation choices.
4. **Success Criteria** -- Set measurable outcomes that determine whether the project has achieved its goals.


Modeling Phase
---------------

The modeling phase defines *how* the system will be structured and designed to meet the requirements.

1. **Static Structure**

   - **Class Design** -- Define the system's static structure by identifying classes, their attributes, methods, and the relationships among them (such as association, aggregation, composition, and inheritance).

2. **Dynamic Behavior**

   - **Sequence Diagrams** -- Illustrate how objects collaborate and exchange messages over time to achieve specific functionalities.

Modeling Languages -- UML
^^^^^^^^^^^^^^^^^^^^^^^^^^

`UML (Unified Modeling Language) <https://www.uml.org/>`_ was designed specifically for software system design and documentation, particularly in object-oriented programming.

- **Focus**: It emphasizes classes, objects, methods, inheritance, and associations.
- **Common Diagrams:**

  - Class diagrams
  - Sequence diagrams
  - Use case diagrams
  - Activity diagrams
  - State machine diagrams

- **Use Case:** Ideal for designing and communicating software architecture, domain models, and system interactions.

Modeling Tools
^^^^^^^^^^^^^^^

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - **Tool**
     - **Type**
     - **Description**
   * - PlantUML
     - Free/Open Source
     - Text-based UML modeling tool supporting class, sequence, and state diagrams.
   * - Mermaid
     - Free/Open Source
     - Lightweight diagramming syntax integrated into Markdown and documentation tools (e.g., GitHub, Obsidian, MkDocs).
   * - Diagrams.net (Draw.io)
     - Free/Open Source
     - Browser and desktop-based visual diagram editor for UML, ERD, and system design.
   * - Modelio
     - Free/Open Source
     - Comprehensive modeling environment supporting UML, BPMN, and SysML. Provides code generation and reverse engineering.
   * - Software Ideas Modeler
     - Free (Non-commercial)
     - Feature-rich UML tool with templates, validation, and code generation. Free for educational and personal use.
   * - StarUML
     - Paid (Free Trial)
     - Professional UML and SysML modeling platform supporting class, sequence, and component diagrams.
   * - Visual Paradigm
     - Freemium/Paid
     - Full-featured modeling suite with UML, BPMN, and SysML support.
   * - Lucidchart
     - Freemium/Paid
     - Web-based collaborative diagramming tool with UML templates.
   * - MagicDraw
     - Paid (Enterprise)
     - Advanced modeling tool used in industry for UML and SysML. Supports simulation, code generation, and model validation.


Implementation Phase
============================

The Implementation Phase follows the Design Phase and focuses on translating the system design into executable code. During this stage, the diagrams created earlier serve as blueprints for constructing the actual software components that realize the intended functionality.

Project Structure
-------------------

We propose the following project structure: a ``src`` folder for implementation files, an ``include`` folder for header files, and a ``CMakeLists.txt`` file for building the project. This structure follows C++ best practices by separating interface declarations (header files) from their implementations (source files).

.. code-block:: text

   week8/
   +-- src/
   |   +-- main.cpp
   |   +-- vehicle.cpp
   |   +-- driver.cpp
   |   +-- engine.cpp
   +-- include/
   |   +-- vehicle.hpp
   |   +-- driver.hpp
   |   +-- engine.hpp
   +-- CMakeLists.txt

In this lecture, we will focus exclusively on the ``Vehicle`` class and its implementation; the other classes (``Driver``, ``Engine``, ``Car``, ``Truck``, ``Train``, and ``Route``) and their relationships will be covered in the next class.

.. figure:: /_static/images/l8/vehicle_class.png
   :alt: Vehicle class UML
   :align: center
   :width: 30%

   UML class diagram for the Vehicle class.


Modern C++ Approaches
----------------------

Object-Oriented Programming is an ideal context for exploring modern C++ features and best practices. In this lecture, we will integrate contemporary idioms directly into our class design:

- ``[[nodiscard]]`` (covered previously)
- ``noexcept`` (covered previously)
- Move semantics (covered previously)
- Smart pointers (covered previously)
- ``std::string_view`` -- this lecture
- ``std::optional`` -- this lecture

std::string_view
^^^^^^^^^^^^^^^^^^

A ``std::string_view`` (header ``<string_view>``) is a lightweight, non-owning view into a string. It is essentially a pointer and size that lets you work with string data without copying or owning it.

.. admonition:: What is inside a std::string_view?
   :class: note

   A ``std::string_view`` contains just:

   - A pointer to the beginning of the data.
   - A size indicating how much data to view.

**Key Characteristics:**

- **Non-owning**: Does not manage memory.
- **Lightweight**: Usually 16 bytes (pointer + size).
- **Read-only**: Provides ``const`` access.
- **Efficient**: No copying or allocation.
- **View**: Since it is a view into existing data, the underlying string must remain valid for as long as the ``std::string_view`` is being used.

**Problem with Traditional Approaches:**

.. code-block:: cpp

   // Using const std::string& - less flexible
   void process_name(const std::string& name) { /* ... */ }

   int main() {
       std::string john{"John Smith"};
       const char* jane{"Jane Doe"};

       process_name(john);          // OK
       process_name(jane);          // Creates temporary std::string -> expensive!
       process_name("Bob Johnson"); // Creates temporary std::string -> expensive!

       // Want substring? Need to create new string:
       process_name(john.substr(0, 4)); // Allocates memory for "John"
   }

**Solution with std::string_view:**

.. code-block:: cpp

   void process_name(std::string_view name) { /* ... */ }

   int main() {
       std::string john{"John Smith"};
       const char* jane{"Jane Doe"};

       process_name(john);          // OK - no conversion
       process_name(jane);          // OK - no conversion
       process_name("Bob Johnson"); // OK - no conversion

       // Substrings are free:
       process_name(john.substr(0, 4)); // No allocation
                                        // Just adjusts pointer and size
   }

**Dangling View Warning:**

.. warning::

   .. code-block:: cpp

      std::string_view dangerous_function() {
          std::string temp{"temporary"};
          return temp;  // DANGER: returning view to destroyed object
      }

   .. code-block:: cpp

      std::string_view safe_function() {
          static auto permanent{"permanent"};
          return permanent;  // OK: string literal has static storage
      }

**When to Use Each:**

.. grid:: 2

   .. grid-item-card:: Use std::string_view when:
      :class-card: sd-border-success

      - Function only reads the string data.
      - You want to accept any string-like input.
      - Performance is critical.
      - Working with substrings frequently.

   .. grid-item-card:: Use const std::string& when:
      :class-card: sd-border-warning

      - You specifically need ``std::string`` features not in ``string_view``.
      - The function is part of an older API that expects ``std::string``.
      - You need to store the reference long-term (be careful with ``string_view`` lifetime).

.. admonition:: Summary
   :class: tip

   ``std::string_view`` is generally the better choice for read-only string parameters because it is more flexible, faster, and provides a cleaner interface while maintaining the same safety as ``const std::string&`` for temporary string objects.


std::optional
^^^^^^^^^^^^^^

``std::optional`` (header ``<optional>``) represents a value that may or may not exist (``std::nullopt``). It provides a type-safe way to handle operations that might fail, eliminating the need for "magic values" or error-prone null pointer patterns.

**Exercise:** Write the function ``int find_index(const std::vector<int>& vec, int target)`` that searches for the first occurrence of a target value in a vector and returns its index if found.

.. code-block:: cpp

   int main() {
       std::vector<int> numbers{10, 20, 30, 40, 30};
       auto result{find_index(numbers, 30)};
       std::cout << "Index: " << result << '\n'; // 2
   }

**Checking Value:**

There are different ways to check whether an ``std::optional`` contains a value.

.. code-block:: cpp

   int main() {
       std::optional<int> index{find_index(numbers, 30)};
       // auto index{find_index(numbers, 30)};

       if (index) {/*do something*/}
       if (index.has_value()) {/*do something*/}
       if (index != std::nullopt) {/*do something*/}
   }

.. admonition:: std::nullopt
   :class: note

   ``std::nullopt`` is a constant used with ``std::optional`` to represent an empty or uninitialized optional value.

**Accessing Value:**

1. **Dereference the Result:**

   .. code-block:: cpp

      std::cout << "Found at index: " << *index << '\n';

   .. note::

      ``std::optional<int>`` is not a pointer. The ``*`` operator is overloaded to provide pointer-like syntax, making ``std::optional`` intuitive if you are familiar with pointers.

2. **value():**

   .. code-block:: cpp

      std::cout << "Found at index: " << index.value() << '\n';

3. **value_or():** Retrieve the value inside an ``std::optional`` or provide a default if it is empty.

   .. code-block:: cpp

      std::optional<int> x{10};
      std::optional<int> y{std::nullopt};

      std::cout << "x: " << x.value_or(-1) << '\n'; // 10
      std::cout << "y: " << y.value_or(-1) << '\n'; // -1

.. warning::

   Always check that the ``std::optional`` contains a value before accessing it (unless you use ``value_or()``).

   .. code-block:: cpp

      std::optional<int> x{std::nullopt};
      // Unsafe: throws std::bad_optional_access
      std::cout << "x: " << x.value() << '\n';
      // Safe: check before accessing
      if (x) {
          std::cout << "x: " << x.value() << '\n';
      }

**When to Use std::optional:**

- Functions that might fail (parsing, division by zero).
- Search operations (may not find target).
- Configuration values (may be unset).
- Database queries (may return no results).

**Benefits:**

- **Type-safe**: Compiler forces handling of "no value" case.
- **Expressive**: Code clearly shows when something might be missing.
- **No magic values**: Eliminates sentinel value confusion.
- **Exception safety**: ``value_or()`` provides safe defaults.


Encapsulation
--------------

Encapsulation (or data hiding) is one of the core principles of OOP. The main purpose of encapsulation is to provide security to the data by restricting its access to the public (the end users).

- In C++, encapsulation is performed via the access specifier ``private``.
- As a developer, you *must encapsulate* all attributes to protect them.
- If you want the user to access and/or modify some attributes, then provide *accessors (getters)* and *mutators (setters)*.
- The C++ Standard Library encapsulates all their attributes. This is why you cannot access them directly.

.. warning::

   All class attributes must be encapsulated using ``private`` or ``protected`` access specifiers. Failure to encapsulate attributes = **automatic 0** on the assignment. This is non-negotiable.

   If unsure about access specifiers, ask during office hours before submission.

Access Specifiers
^^^^^^^^^^^^^^^^^^

Access specifiers determine the accessibility of the members (attributes and methods) of a ``class``. They play a crucial role in *encapsulation*. There are three primary access specifiers in C++.

- ``public`` -- Members declared under the ``public`` specifier can be accessed from outside the class and by derived classes.
- ``private`` -- Members declared as ``private`` are restricted to the class in which they are declared. They cannot be accessed from outside the class or by derived classes.
- ``protected`` -- ``protected`` members are somewhere between ``public`` and ``private``. They cannot be accessed from outside the class, but they can be accessed by derived classes. We see this in detail in the *inheritance* section.

.. warning::

   If you do not provide any access specifier, C++ will make all your members ``private``.


Accessors/Mutators
--------------------

Accessors (getters) and mutators (setters) are ``public`` methods that provide controlled access to ``private`` and ``protected`` attributes, enabling encapsulation by allowing you to validate data, enforce invariants, and modify internal implementation without breaking client code.

Accessors (Getters)
^^^^^^^^^^^^^^^^^^^^

An accessor (or getter) is a ``public`` method that provides controlled, read-only access to ``private`` and ``protected`` attributes while maintaining encapsulation.

**Key Points:**

- **Return type:** Matches the attribute being accessed (by value for small types like ``int``, ``bool``, ``char``; by ``const`` reference for large types like ``std::string``, containers, custom objects).
- **Parameters:** Accessors typically have no parameters.
- **Read-only access:** Return by value or by ``const`` reference. *Never* return by non-``const`` reference, as this would allow external code to modify the ``private`` attribute, breaking encapsulation.
- **const correctness:** Must be declared ``const`` to guarantee no modification of object state and to allow calling on ``const`` objects.
- **[[nodiscard]]** (C++17): Should be used to prevent accidentally ignoring the return value, which is almost always a programming error.
- **noexcept:** Consider adding when the accessor cannot throw exceptions (e.g., returning primitives or ``const`` references).
- **inline:** Accessors defined inside the class definition are automatically inline, eliminating function call overhead for these trivial operations.

**Return by Value (Primitives):**

.. code-block:: cpp

   [[nodiscard]] bool is_running() const noexcept {
       return is_running_;
   }

- Efficient for small types
- No risk of external modification
- ``noexcept`` safe (no allocation)

**Return by const Reference (Large Types):**

.. code-block:: cpp

   [[nodiscard]] const std::string& get_color() const noexcept {
       return color_;
   }

- Avoids expensive copying
- ``const`` prevents modification
- ``noexcept`` safe (no copy)

**const-Correctness with Accessors:**

When a method is declared ``const``, it creates a compile-time contract guaranteeing the method will not modify the object's state. This prevents accidental modification of member variables and enables the method to be called on ``const`` objects.

.. code-block:: cpp

   // With const (Correct)
   [[nodiscard]] bool is_running() const noexcept {
       is_running_ = true; // Compilation error: cannot modify in const method
       return is_running_;
   }

.. code-block:: cpp

   // Without const (Problematic)
   [[nodiscard]] bool is_running() noexcept {
       is_running_ = true; // Compiles but violates accessor semantics
       return is_running_;  // Accessor should not modify state!
   }

**Key Insight:** The ``const`` keyword enforces the read-only contract at compile time, catching bugs early and documenting intent. Without it, accessors can accidentally become mutators.


Mutators (Setters)
^^^^^^^^^^^^^^^^^^^

A mutator (or setter) is a ``public`` method that provides controlled modification of ``private`` and ``protected`` attributes while maintaining encapsulation and enforcing invariants.

**Key Points:**

- **Return type:** Typically ``void``, though sometimes returns a reference to the object (``*this``) to enable method chaining.
- **Parameters:** Takes one parameter matching the attribute type (by value for small types like ``int``, ``bool``; by ``const`` reference for large types like ``std::string``, containers).
- **Validation:** Should validate input to maintain class invariants (e.g., prevent negative values, check ranges, ensure non-empty strings).
- **const correctness:** Must *NOT* be declared ``const`` because mutators modify object state.
- **noexcept:** Use only if the setter cannot throw exceptions. Be cautious with types that may throw during assignment (e.g., ``std::string``).
- **Encapsulation benefit:** Allows internal representation changes without breaking client code, and enforces business rules at a single point.

**Simple Mutator (No Validation):**

.. code-block:: cpp

   void set_color(const std::string& color) noexcept {
       color_ = color;
   }

- Pass by ``const`` reference for large types
- Simple assignment, no validation needed
- ``noexcept`` if assignment cannot throw

**Mutator with Validation:**

.. code-block:: cpp

   void set_max_speed(int speed) {
       if (speed < 0) {
           throw std::invalid_argument("Max speed cannot be negative");
       }
       max_speed_ = speed;
   }

- Enforces class invariants
- Prevents invalid states
- Cannot be ``noexcept`` (may throw)

**Why Mutators Cannot Be const:**

Mutators modify object state, so they must *not* be declared ``const``. The ``const`` keyword would create a contract that the method does not modify the object, which directly contradicts the purpose of a mutator.

.. code-block:: cpp

   // Without const (Correct)
   void set_is_running(bool running) noexcept {
       is_running_ = running;  // OK: can modify member variable
   }

.. code-block:: cpp

   // With const (Wrong!)
   void set_is_running(bool running) const noexcept {
       is_running_ = running;  // Compilation error: cannot modify in const method
   }

**Key Insight:** Mutators inherently change object state. Marking them ``const`` creates a logical contradiction and will cause compilation errors when trying to modify member variables.


Constructors
--------------

A constructor is a special member function that initializes an object when it is created.

**Key characteristics:**

- Same name as the class
- No return type (not even ``void``)
- Automatically called when an object is instantiated
- Used to set up the initial state of an object (initialize its attributes)
- Can be overloaded

Default Constructor
^^^^^^^^^^^^^^^^^^^^

A default constructor is a constructor that takes no arguments. It is automatically called when an object is created without initialization parameters.

.. warning::

   If you do not define *any* constructor, the compiler generates a default constructor that:

   - Leaves built-in types (``int``, ``double``, etc.) uninitialized with garbage values
   - Calls the default constructor for user-defined type members
   - Uses in-class initializers if provided

.. code-block:: cpp

   class Vehicle {
   private:
       std::string color_;            // std::string's default constructor (empty string)
       std::string model_;            // std::string's default constructor (empty string)
       bool is_running_{false};       // Initialized to false
       int max_speed_;                // Uninitialized (garbage value)
   };

   int main() {
       Vehicle car; // Default constructor from compiler is called
   }

**User-Defined Default Constructor:**

.. code-block:: cpp

   class Vehicle {
   private:
       std::string color_;
       std::string model_;
       bool is_running_{false};
       int max_speed_;
   public:
       // User-defined default constructor
       Vehicle() {
           color_ = "White";
           model_ = "Unknown";
           max_speed_ = 0;
       }
   };

   int main() {
       Vehicle car; // User-defined default constructor is called
   }


Parameterized Constructors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A parameterized constructor takes one or more parameters, allowing you to initialize an object's attributes with specific values at the time of creation.

.. code-block:: cpp

   class Vehicle {
   /*other code*/
   public:
       Vehicle(const std::string& color, const std::string& model, int max_speed)
       {
           color_ = color;
           model_ = model;
           max_speed_ = max_speed;
       }
       Vehicle(int max_speed) { max_speed_ = max_speed; }
   };

.. code-block:: cpp

   int main() {
       Vehicle car(131);
       auto wraith = std::make_unique<Vehicle>("white", "Wraith", 131);
       Vehicle bus; // Error: no default constructor available
   }


Member Initialization List
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A constructor's **member initializer list** allows you to initialize an object's attributes directly when the object is created, before the constructor body executes.

.. code-block:: cpp

   class Vehicle {
   /*other code*/
   public:
       Vehicle(const std::string& color, const std::string& model, int max_speed)
           : color_{color}, model_{model}, max_speed_{max_speed} {
           /*body*/
       }
   };

**C++ Object Construction Order:**

When an object is created, C++ follows a strict initialization sequence:

1. **Base class constructors** -- If the class inherits from a base class, the base class constructor(s) execute first (in declaration order for multiple inheritance).
2. **Member attribute constructors** -- All member objects are constructed in the order they are *declared* in the class definition, regardless of the order in the member initializer list.
3. **Constructor body** -- Finally, the statements in the constructor body execute.

**Assignment in Body vs. Member Initializer List:**

.. code-block:: cpp

   class A {
   public:
       A() {
           std::cout << "A constructor\n";
           name_ = "Default"; // Assignment (two-step process)
       }
   private:
       std::string name_; // Constructed first with default constructor
   };

Before ``A`` can exist, the ``std::string name_`` attribute must be initialized. The ``std::string`` default constructor is called (creating an empty string), then ``A``'s constructor body runs and ``"Default"`` is assigned to ``name_``. This results in two operations instead of one.

.. admonition:: Best Practice
   :class: tip

   Use a member initializer list for direct initialization: ``A() : name_{"Default"}``

**Constant and Reference Members:**

.. code-block:: cpp

   class A {
   public:
       A(int x, int& y) {
           c_ = x;  // Wrong: const members cannot be assigned
           r_ = y;  // Wrong: references cannot be rebound
       }
   private:
       const int c_;
       int& r_;
   };

.. warning::

   - ``const`` members must be initialized before the constructor body executes.
   - References must be initialized when created (they cannot be left unbound).

.. admonition:: Best Practice
   :class: tip

   Use a member initializer list to initialize both the constant and reference members.

**Declaration Order Matters:**

Members are always initialized *in the order they are declared*, not in the order they appear in the initializer list.

.. code-block:: cpp

   class Rectangle {
   private:
       double area_;   // 1. initialized first
       double width_;  // 2. initialized second
       double height_; // 3. initialized third
   public:
       Rectangle(double w, double h)
           : width_{w}, height_{h}, area_{width_ * height_} {
           // area_ is computed using uninitialized width_ and height_
       }
   };

.. warning::

   Even though ``width_{w}`` and ``height_{h}`` appear before ``area_{width_ * height_}`` in the initializer list, ``area_`` is initialized first (with garbage ``width_`` and ``height_``) because of declaration order.

**Summary:**

- **Direct Initialization** -- Member initializer lists initialize attributes directly, avoiding the two-step process of default construction followed by assignment. This is more efficient, especially for complex types like ``std::string`` or ``std::vector``.
- **Required for Const and References** -- Attributes declared as ``const`` or references must be initialized using the initializer list, as they cannot be assigned after construction.


const Objects
^^^^^^^^^^^^^^

A ``const`` object is an instance of a class whose state cannot be modified after it is created.

.. warning::

   When you declare an object as ``const``, all its non-``const`` methods become inaccessible: only methods marked as ``const`` can be called.

   This enforces read-only access to the object's internal data and ensures ``const``-correctness.

.. code-block:: cpp

   int main() {
       const Vehicle camry("White", "Camry", 113);
       camry.print_status(); // Error: print_status() is not const
   }

.. note::

   Non-``const`` objects can access both ``const`` and non-``const`` methods.


The this Pointer
============================

In every *non-static method*, the compiler **implicitly** passes a hidden pointer named ``this`` that points to the current object -- the instance on which the function was called.

In other words:

.. code-block:: cpp

   object.method();

is equivalent to:

.. code-block:: cpp

   ClassName::method(&object);

So inside the method, ``this`` is a pointer to the object that invoked the function.

**Example:**

.. code-block:: cpp

   class Point {
   private:
       double x_;
       double y_;

   public:
       Point(double x, double y) : x_{x}, y_{y} { /*body*/ }

       void move(double dx, double dy) {
           this->x_ += dx; // same as x_ += dx;
           this->y_ += dy; // same as y_ += dy;
       }

       void print() const {
           std::cout << "(" << this->x_ << ", " << this->y_ << ")\n";
       }
   };

.. note::

   - Here, ``this`` has the type ``Point* const``
   - It refers to the current object (``p`` if you call ``p.move(2, 3)``)

**Type of the this Pointer:**

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - **Context**
     - **Type of this**
     - **Can modify object?**
     - **Can reassign this?**
   * - Non-``const`` method
     - ``A* const``
     - Yes
     - No
   * - ``const`` method
     - ``const A* const``
     - No
     - No

.. admonition:: Summary
   :class: tip

   The ``this`` pointer itself is always ``const`` (you cannot change what it points to), but whether you can modify the object depends on if the method is ``const``.

**When and Why We Use this:**

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - **Purpose**
     - **Description**
     - **Example**
   * - Disambiguation
     - When a parameter name shadows a member variable
     - ``this->x = x;``
   * - Chaining Calls
     - Returning ``*this`` allows method chaining
     - ``return *this;``
   * - Returning the Current Object
     - Often used in operators like assignment
     - ``return *this;``
   * - Obtaining Address
     - Sometimes used to get the current object's pointer
     - ``return this;``

**Method Chaining Example:**

.. code-block:: cpp

   class Counter {
   private:
       int value_;

   public:
       Counter(int v = 0) : value_{v} {}

       Counter& increment() {
           ++value_;
           return *this; // allows chaining
       }

       void print() const { std::cout << "Value: " << value_ << '\n'; }
   };

.. code-block:: cpp

   int main() {
       Counter c;
       c.increment().increment().increment().print();
   }


static Members
============================

static Attributes
------------------

A ``static`` attribute (or ``static`` data member) *belongs to the class itself*, not to any individual object.

- There is only one copy of the ``static`` attribute shared by all instances.
- It exists even if no objects of the class are created.
- It is often used for class-wide constants, counters, or shared resources.

static Methods
---------------

A ``static`` method (or ``static`` member function) *belongs to the class itself*, not to any individual object.

- It cannot access non-``static`` members (data or methods) because it does not have a ``this`` pointer.
- It can be called even if no objects of the class exist, using the class name (e.g., ``Vehicle::get_vehicle_count()``).
- It is often used for utility functions or to access/modify ``static`` data members.

**Example:**

.. code-block:: cpp

   class Vehicle {
   private:
       inline static int vehicle_count_{0}; // C++17 and later
       std::string model_;

   public:
       Vehicle(const std::string& model) : model_{model} { vehicle_count_++; }

       [[nodiscard]] static int get_vehicle_count() noexcept {
           return vehicle_count_;
       }
   };

.. code-block:: cpp

   int main() {
       std::cout << Vehicle::get_vehicle_count() << '\n'; // 0
       Vehicle vehicle("Sedan");
       std::cout << vehicle.get_vehicle_count() << '\n';  // 1
   }
