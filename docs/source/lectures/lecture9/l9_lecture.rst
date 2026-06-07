====================================================
Lecture
====================================================


OOP Advanced Topics
====================================================

This lecture covers advanced object-oriented programming in C++:

- Class relationships: association, aggregation, composition, inheritance
- Polymorphism: compile-time and runtime
- Virtual destructors and the ``= default`` keyword
- Abstraction with pure virtual methods and abstract classes
- Concrete classes and the ``final`` keyword


----


Class Relationships
====================================================

Class relationships describe how classes interact and depend on each other.
They represent real-world connections between objects and define the structure
of your program. They are how you model the real world and, more importantly,
how you create code that is reusable, maintainable, and flexible.


Association
----------------------------------------------------

Association is a loose relationship where objects exist independently. One
object uses or interacts with another, but neither owns the other. If one
object is destroyed, the other can continue existing.

**Example**: A ``Teacher`` and a ``Student`` have an association. If the
teacher leaves, students still exist. If a student graduates, the teacher
remains.

.. figure:: /_static/images/l9/association.png
   :align: center

   UML diagram showing an association relationship.

.. admonition:: Multiplicity
   :class: note

   Multiplicity can be:

   - **n** = exactly **n**
   - **0..1** = zero or one
   - **\*** or **0..\*** = zero or more
   - **1..\*** = one or more


Aggregation
----------------------------------------------------

Aggregation is a type of association and represents a "has-a" relationship
where the container has a weak ownership of the contained objects. The
contained objects can exist independently of the container. When the
container is destroyed, the contained objects continue to exist.

**Example**: A ``Fleet`` "contains" ``Vehicles``. If the fleet is dissolved,
the vehicles still exist and can be transferred to another fleet or operate
independently.


Composition
----------------------------------------------------

Composition is a strong "has-a" relationship with exclusive ownership. The
contained object is an integral part of the container and cannot exist
independently. When the container is destroyed, all its parts are destroyed
as well.

**Example**: A ``Vehicle`` has ``Sensors``. The sensors are integral parts of
the vehicle. If the vehicle is destroyed (scrapped), its sensors are
destroyed with it.

.. admonition:: Aggregation vs. Composition
   :class: tip

   .. list-table::
      :widths: 20 40 40
      :header-rows: 1

      * - Aspect
        - Aggregation
        - Composition
      * - Ownership
        - Weak (shared)
        - Strong (exclusive)
      * - Lifetime
        - Independent
        - Dependent on container
      * - Destruction
        - Parts survive
        - Parts destroyed with container
      * - UML Symbol
        - Open diamond
        - Filled diamond


Inheritance (Generalization)
----------------------------------------------------

Inheritance represents an "is-a" relationship where a derived class inherits
attributes and behaviors from a base class. The derived class specializes or
extends the base class, providing specific implementations while maintaining
the common interface.

**Example**: ``RoboTaxi`` "is-a" ``Vehicle``. ``Taxi`` "is-a" ``Vehicle``.
Both inherit common vehicle behavior but add their own specific features.


Types of Inheritance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Single Inheritance**

Single inheritance: a class inherits from exactly one base class.

.. figure:: /_static/images/l9/single_inheritance.png
   :align: center
   :width: 60%

   Single inheritance -- ``Bird`` and ``Elephant`` inherit from ``Animal``.

- ``Bird`` and ``Elephant`` inherit ``Animal``'s ``public`` and ``protected`` members.

.. note::

   UML diagrams typically do not show inherited members.

.. figure:: /_static/images/l9/elephant-bird.png
   :align: center
   :width: 30%

**Multiple Inheritance**

Multiple inheritance occurs when a class inherits from more than one base
class. The derived class gains access to all ``public`` and ``protected``
members from all parent classes.

.. figure:: /_static/images/l9/mythicalcreature.png
   :align: center
   :width: 60%

   Multiple inheritance -- ``MythicalCreature`` inherits from both ``Animal`` and ``Human``.

- ``MythicalCreature`` inherits all ``protected`` and ``public`` attributes from ``Animal`` and ``Human``.

.. figure:: /_static/images/l9/Sphinx.jpg
   :align: center
   :width: 50%

.. admonition:: Course Scope
   :class: note

   We focus exclusively on single inheritance in this course. For
   assignments and projects, you are welcome to use any inheritance approach.


Generalization and Specialization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. card::

   **Generalization**

   Bottom-up approach which should be used every time classes have specific
   differences and common similarities, so that the similarities can be
   grouped in a superclass and the differences maintained in subclasses.

   ---

   **Specialization**

   Top-down approach which creates new classes from an existing class. If
   certain properties only apply to some of the classes, subclasses can be
   created for these specific properties.

.. figure:: /_static/images/l9/general_special.png
   :align: center
   :width: 50%

   Generalization (bottom-up) vs. Specialization (top-down).


UML Representation
""""""""""""""""""""""""""""""""""""""""""""""""""""

The ``protected`` specifier is denoted with a ``#`` symbol in UML.

.. figure:: /_static/images/l9/base_derived.png
   :align: center
   :width: 60%

   UML representation of a base class and derived class.


Inheritance Access Types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Base Class Member
     - ``public`` inheritance
     - ``protected`` inheritance
     - ``private`` inheritance
   * - ``public``
     - ``public``
     - ``protected``
     - ``private``
   * - ``protected``
     - ``protected``
     - ``protected``
     - ``private``
   * - ``private``
     - not accessible (hidden)
     - not accessible (hidden)
     - not accessible (hidden)

.. admonition:: Important
   :class: warning

   - ``private`` members are inherited but hidden from derived classes.
   - Default inheritance in C++ is ``private``.


Constructors in Inheritance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Key Rule
   :class: warning

   The constructors of a class must address the attributes specific to
   that class.

Consider the following base and derived classes:

.. code-block:: cpp

   class Base {
    public:
     Base(int base_value = 50) :
       base_member_{base_value} {}
    protected:
     int base_member_;
   };  // class Base

   class Derived : public Base {
    public:
     Derived(double derived_value)
       : derived_member_{derived_value} {}
    private:
     double derived_member_;
   };  // class Derived

.. code-block:: cpp

   int main() {
       Derived derived(20.5);
   }

- Before a derived class is initialized, the base class portion must be initialized.
- When ``Derived derived(20.5)`` executes, ``Base(50)`` is first executed: ``base_member_`` is initialized to ``50``.
- ``Derived(20.5)`` is then executed: ``derived_member_`` is initialized to ``20.5``.
- Control returns to ``main()`` and the program exits.

.. warning::

   With the way this program is written, ``base_member_`` is *always*
   initialized to the default value ``50``.


**Approach 1 -- Member Initializer List (Does Not Work)**

Add another parameter to the constructor for ``Derived`` and use it to
initialize the attribute ``base_member_`` with the member initializer list.

.. code-block:: cpp

   class Derived : public Base {
    public:
     Derived(double derived_value, int base_value)
         : derived_member_{derived_value}, base_member_{base_value} {
           /*empty body*/
     }
    private:
     double derived_member_;
   };  // class Derived

.. warning::

   C++ prevents classes from initializing inherited attributes in the
   member initializer list of a constructor.


**Approach 2 -- Assignment in Constructor Body (Works, But Not Ideal)**

Since we cannot use the member initializer list, can we assign
``base_member_`` in the body of the constructor?

.. code-block:: cpp

   class Derived : public Base {
    public:
     Derived(double derived_value, int base_value)
         : derived_member_{derived_value} {
            base_member_ = base_value;
     }
    private:
     double derived_member_;
   };  // class Derived

.. warning::

   Yes this works. However, this approach is performed in two steps and
   will not work if the attribute is a ``const`` or a reference.


**Approach 3 -- Explicit Base Class Constructor Call (Recommended)**

Explicit call of the base class constructor. Constructors have to worry
about their own attributes.

.. code-block:: cpp

   class Derived : public Base {
    public:
     Derived(double derived_value, int base_value)
         : Base(base_value), derived_member_{derived_value} {
            /*empty body*/
     }
    private:
     double derived_member_;
   };  // class Derived

.. code-block:: cpp

   int main() {
       Derived derived(20.5, 10);
   }

.. admonition:: Best Practice
   :class: tip

   - Add parameters for base class attributes in the derived class constructor.
   - Explicitly call the base class constructor.


----


Polymorphism
====================================================

**Polymorphism** (Greek: *poly* = many, *morph* = form) is a core OOP
principle. Polymorphism allows objects of different classes to be treated
uniformly through a common interface. C++ supports two types:

- **Compile-time polymorphism** -- resolved at compile time
- **Runtime polymorphism** -- resolved at runtime


Compile-Time Polymorphism
----------------------------------------------------

*Compile-time polymorphism* (also called *static polymorphism* or *early
binding*) is resolved during compilation. The compiler determines which
function to call based on the **static type** at compile time.

**Examples**: *function overloading*, *operator overloading*, and *method
redefinition*.

.. note::

   The function resolution happens at compile time based on the declared
   type of the variable, not the actual object it contains.


Method Order Check
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   int main() {
       Derived derived(20.5, 10);
       derived.test(); // Base::test() called
   }

When a method is called on a derived class object:

1. The compiler first checks if the method exists in the derived class.
2. If not found, it searches up the inheritance hierarchy through base classes.
3. The compiler uses the first matching method it finds.

In the example, ``Base::test()`` is used since we did not provide a version
for ``Derived::test()``.


Method Redefinition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Method redefinition allows a derived class to provide its own implementation
of a base class method when the base class version is too general or needs
specialization.

.. code-block:: cpp

   // polymorphism_demo.cpp
   int main() {
       Derived derived(20.5, 10);
       derived.test(); // Derived::test() called
   }

.. note::

   Method redefinition is compile-time polymorphism because the method
   selection is based on the static type known at compile time.


Runtime Polymorphism
----------------------------------------------------

*Runtime polymorphism* (*dynamic polymorphism* or *late binding*) decides
which ``virtual`` method implementation runs based on the *dynamic type*
(actual object type) at runtime, not the static type of the pointer/reference.

.. admonition:: Key Requirement
   :class: note

   Runtime polymorphism in C++ requires a ``virtual`` method in a base class
   and a call through a *base* reference or *base* pointer to a *derived*
   object. The actual method called depends on the real object type at runtime.


The ``virtual`` Keyword
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``virtual`` keyword tells the compiler to use **dynamic dispatch** for
a method. This means:

1. The method call is resolved at **runtime**, not compile time.
2. The **actual object type** determines which method runs, not the pointer/reference type.

   - **Actual object:** ``RoboTaxi``
   - **Pointer type:** ``Vehicle``

3. The compiler creates a **vtable** (virtual method table) to track which implementation to call.

.. code-block:: cpp

   // in class Vehicle (vehicle.hpp)
   // virtual -> can be overridden in derived classes
   virtual void drive(); // can be overridden in derived classes
   void update_location(const Location &location); // cannot be overridden (static binding)

.. code-block:: cpp

   int main() {
       using transportation::Vehicle;
       using transportation::RoboTaxi;
       std::unique_ptr<Vehicle> rt = std::make_unique<RoboTaxi>("ROBOTAXI-001", 4);
       rt->drive();   // Calls RoboTaxi::drive() - dynamic dispatch
       rt->update_location(loc);  // Calls Vehicle::update_location() - static binding
   }


.. admonition:: Important
   :class: warning

   - Without ``virtual``, C++ uses static binding based on the pointer type, not the actual object.
   - Note that we wrote: ``std::unique_ptr<Vehicle> rt = ...`` and not ``auto rt = ...`` which is equivalent to ``std::unique_ptr<RoboTaxi> rt``. *We want a base class pointer (or reference) to a derived object.*


Non-Polymorphic Overloads (Not Scalable)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // Overloads choose at compile time based on the static type.
   void run_shift(transportation::RoboTaxi& v) { v.drive(); }
   void run_shift(transportation::Taxi&     v) { v.drive(); }

   int main() {
       transportation::RoboTaxi rt{"ROBOTAXI-001", 4};
       transportation::Taxi     tx{"TAXI-001", 4};
       run_shift(rt);  // Calls RoboTaxi version
       run_shift(tx);  // Calls Taxi version
   }

.. warning::

   Overload resolution is a compile-time choice. Each new derived type
   requires another overload. Bodies tend to duplicate (*violates DRY
   principle*). Does not support heterogeneous collections.


Polymorphic Solution (Scalable)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // Base interface with virtual method
   class Vehicle {
   public:
       virtual ~Vehicle() = default; // essential for polymorphic bases
       virtual void drive(); // virtual (can be overridden)
   };

.. code-block:: cpp

   // One function works for ALL current and future derived vehicle types
   void run_shift(transportation::Vehicle& v) {
       v.drive();  // Runtime dispatch - calls the actual object's drive()
   }
   // Pointer variant (e.g., ownership with unique_ptr)
   void run_shift(std::unique_ptr<transportation::Vehicle> v) {
       v->drive(); // Runtime dispatch
   }

   int main() {
       auto rt = std::make_unique<transportation::RoboTaxi>("ROBOTAXI-001", 4);
       auto tx = std::make_unique<transportation::Taxi>("TAXI-001", 4);
       run_shift(*rt);                // Calls RoboTaxi::drive()
       run_shift(std::move(tx));      // Calls Taxi::drive()
   }

.. note::

   Only one ``run_shift()`` is needed. The call *site* uses a base reference
   or pointer. The *target* method is determined at runtime based on the
   actual object type (the most-derived override).


When to Use ``auto`` vs. Explicit Base Type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The choice depends on **where polymorphism needs to happen**.

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item-card:: Explicit Base Type
      :class-card: sd-border-secondary

      .. code-block:: cpp

         unique_ptr<Vehicle> rt =
             make_unique<RoboTaxi>(...);

         // Polymorphic calls
         rt->drive();

      **Polymorphism in** ``main()``: Multiple polymorphic calls locally.

   .. grid-item-card:: Using ``auto``
      :class-card: sd-border-secondary

      .. code-block:: cpp

         auto rt = make_unique<RoboTaxi>(...);

         // Direct calls to RoboTaxi
         rt->drive();

         // Pass to polymorphic function
         run_shift(std::move(rt));

      **Polymorphism delegated**: Concrete type until passed to function.


The Container Problem with ``auto``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // This WORKS - function parameter accepts conversion
   auto rt = std::make_unique<RoboTaxi>(...);  // unique_ptr<RoboTaxi>
   run_shift(std::move(rt));  // Converts to unique_ptr<Vehicle> at call

.. code-block:: cpp

   // This FAILS - container requires exact type match
   auto rt = std::make_unique<RoboTaxi>(...);  // unique_ptr<RoboTaxi>
   std::vector<std::unique_ptr<Vehicle>> fleet;
   fleet.push_back(std::move(rt));     // ERROR: Type mismatch!
   fleet.emplace_back(std::move(rt));  // ERROR: Still doesn't work!

.. warning::

   Function parameters allow implicit conversions at the call site.
   Container storage requires **exact type matches**:
   ``unique_ptr<RoboTaxi>`` is not ``unique_ptr<Vehicle>``. This applies to
   **ALL** containers (``vector``, ``deque``, ``list``, ``set``, ``map``, etc.).


Complete Comparison Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 50 25 25
   :header-rows: 1

   * - Operation
     - Explicit Base Type
     - Using ``auto``
   * - Pass to function with base parameter
     - Yes
     - Yes
   * - Store in ANY container of base pointers
     - Yes
     - No
   * - Use ``push_back`` / ``emplace_back`` / ``insert`` with variable
     - Yes
     - No
   * - Direct insertion (no variable): ``vec.push_back(make_unique<...>())``
     - Yes
     - N/A [#f1]_
   * - Call derived-specific methods
     - No
     - Yes
   * - Polymorphic calls at point of use
     - Yes
     - No

.. [#f1] No ``auto`` variable involved -- temporary converts at insertion point.


Why This Happens: Type System Rules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Function Parameters:**

.. code-block:: cpp

   void run_shift(std::unique_ptr<Vehicle> v);  // Accepts base type

   auto rt = std::make_unique<RoboTaxi>(...);   // unique_ptr<RoboTaxi>
   run_shift(std::move(rt));  // Compiler converts RoboTaxi* -> Vehicle*
                              // Conversion happens at call boundary

**Container Storage:**

.. code-block:: cpp

   std::vector<std::unique_ptr<Vehicle>> fleet;  // Template parameter is FIXED

   auto rt = std::make_unique<RoboTaxi>(...);    // unique_ptr<RoboTaxi>
   fleet.push_back(std::move(rt));  // Template types don't convert!
                                    // unique_ptr<RoboTaxi> != unique_ptr<Vehicle>

.. warning::

   **Key insight:** ``unique_ptr<Derived>`` is NOT a subtype of
   ``unique_ptr<Base>``, even though ``Derived*`` converts to ``Base*``.
   Template instantiations do not inherit type relationships.


Solutions for Polymorphic Collections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Option 1: Direct construction (BEST)**

.. code-block:: cpp

   std::vector<std::unique_ptr<Vehicle>> fleet;
   fleet.push_back(std::make_unique<RoboTaxi>(...));  // Implicit conversion
   fleet.push_back(std::make_unique<Taxi>(...));       // Implicit conversion

**Option 2: Use base type from the start**

.. code-block:: cpp

   std::unique_ptr<Vehicle> rt = std::make_unique<RoboTaxi>(...);
   rt->drive();  // Polymorphic call
   fleet.push_back(std::move(rt));  // Types match exactly

**Option 3: Explicit cast (AVOID -- verbose and error-prone)**

.. code-block:: cpp

   auto rt = std::make_unique<RoboTaxi>(...);
   fleet.push_back(std::unique_ptr<Vehicle>(std::move(rt)));  // But ugly


Decision Framework
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **Need to store in a base-type container?**

   - Use **explicit base type** OR **direct insertion**.

2. **Need polymorphic calls at point of use?**

   - Use **explicit base type**.

3. **Need derived-specific methods before passing to functions?**

   - Use ``auto``, then pass to functions.

4. **Only passing to functions, no container storage?**

   - Either works; ``auto`` is more flexible.

.. admonition:: Best Practice
   :class: tip

   **Rule of thumb:** If you are building polymorphic collections, use
   explicit base type or direct insertion. If you are only calling
   functions, ``auto`` is fine.


The ``override`` Keyword
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``override`` keyword is a **safety feature** that tells the compiler
"I intend this method to override a base class virtual method".

- **Catches typos**: If signatures do not match, compilation fails.
- **Documents intent**: Makes it clear this overrides a base method.
- **Prevents accidental hiding**: Detects when you think you are overriding but are not.

.. code-block:: cpp

   class Vehicle {
   public:
       virtual void drive();
   };

   class RoboTaxi : public Vehicle {
   public:
       void drive() override;        // OK - matches base signature
       // void drive(int) override;  // ERROR - no matching virtual in base
       // void driev() override;     // ERROR - typo caught!
   };

.. admonition:: Best Practice
   :class: tip

   Always use ``override`` when overriding virtual methods. It is free safety.


Avoid Slicing and Embrace Polymorphic Collections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<std::unique_ptr<transportation::Vehicle>> fleet;
   fleet.emplace_back(std::make_unique<transportation::RoboTaxi>("ROBOTAXI-001", 4));
   fleet.emplace_back(std::make_unique<transportation::Taxi>("TAXI-001", 4));

   for (auto& v : fleet) {
       v->drive();   // Runtime dispatch for each element's actual type
   }

.. warning::

   Do not store derived objects by value in a ``std::vector<Vehicle>``.
   This causes *object slicing* where derived class data is lost and
   polymorphism does not work. Use owning pointers (``unique_ptr``,
   ``shared_ptr``), or non-owning pointers/references with external
   lifetime management.


Requirements for Runtime Polymorphism
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **Inheritance relationship** -- Derived classes inherit from a common base (``Vehicle``).
2. **Base handle to derived object** -- Use ``Vehicle&``, ``Vehicle*``, ``std::unique_ptr<Vehicle>``, or ``std::shared_ptr<Vehicle>``.
3. **virtual method in the base** -- Mark the interface ``virtual``; override it in derived classes.

.. note::

   The call target depends on the **dynamic type** of the object (what it
   actually is at runtime), not the **static type** of the handle (how the
   pointer/reference was declared). This is *late binding*.


----


Destructors
====================================================

A **destructor** is a special member function that cleans up an object's
resources when it goes out of scope or is explicitly deleted. The
destructor is automatically called: you do not invoke it manually.

**Key Characteristics:**

- **Naming**: ``~ClassName()`` (e.g., ``~Vehicle()``)
- **No parameters**, **no return type**
- **One per class** -- cannot be overloaded
- **Automatic invocation** at scope exit or ``delete``


What Does a Destructor Do?
----------------------------------------------------

A destructor performs **cleanup operations** before an object is destroyed:

- **Release dynamically allocated memory** (``delete``, ``delete[]``)
- **Close file handles, network connections, database connections**
- **Release mutexes or other synchronization primitives**
- **Decrement reference counts** in shared ownership schemes
- **Any other resource cleanup** needed for proper RAII

.. code-block:: cpp

   class FileHandler {
   private:
       FILE* file_;
   public:
       FileHandler(const char* filename) : file_(fopen(filename, "r")) {}
       ~FileHandler() {  // Destructor ensures file is closed
           if (file_) fclose(file_);
       }
   };
   // file_ is automatically closed when FileHandler goes out of scope


Virtual Destructors and Inheritance
----------------------------------------------------

.. admonition:: Critical
   :class: danger

   When deleting through a base pointer, a ``virtual`` destructor ensures
   the derived class destructor runs first. Without it, only the base
   destructor runs, causing **resource leaks** and **undefined behavior**.

.. code-block:: cpp

   class Base {
   public:
       ~Base() { std::cout << "~Base()\n"; }  // NOT virtual!
   };

   class Derived : public Base {
   private:
       int* data_;
   public:
       Derived() : data_(new int[1000]) {}
       ~Derived() { delete[] data_; std::cout << "~Derived()\n"; }
   };

   Base* ptr = new Derived();
   delete ptr;  // UNDEFINED BEHAVIOR! Only ~Base() called, not ~Derived()
                // Leaks memory from data_!

.. warning::

   Without ``virtual``, the destructor is selected at compile time based on
   the pointer type (``Base*``), not the actual object type (``Derived``).
   The derived destructor never runs.


The ``= default`` Keyword
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``= default`` keyword requests the compiler generate the default
implementation of a special member function (constructor, destructor,
copy/move operations).

**Why use it?**

- **Explicit intent**: Shows you deliberately want the default behavior.
- **Enables special rules**: Compiler-generated functions can be trivial/constexpr.
- **Rule of Zero compliance**: Do not write what the compiler can generate.
- **Better optimization**: Compiler-generated code is often optimal.

.. code-block:: cpp

   class Vehicle {
   public:
       virtual ~Vehicle() = default;  // Compiler generates virtual destructor body
       Vehicle() = default;           // Compiler generates default constructor
       Vehicle(const Vehicle&) = default;      // Compiler generates copy constructor
   };

.. note::

   ``= default`` is particularly important for ``virtual`` destructors in
   abstract base classes where you do not need custom cleanup logic but must
   ensure the destructor is ``virtual``.


----


Abstraction
====================================================

Abstraction exposes a **stable interface** and hides **implementation
details**. Users depend on **what** the type does (the contract), not
**how** it does it (the implementation).

**Key Benefits:**

- **Simplicity**: Small public surface with clear semantics
- **Modularity**: Independent evolution of internals without breaking clients
- **Maintainability**: Fewer ripple effects across codebase
- **Testability**: Mock the interface, validate behavior independently
- **Flexibility**: Swap implementations without changing client code


When to Use Abstract Classes
----------------------------------------------------

Create abstract classes when you want to:

1. **Define a contract** that multiple concrete types must follow.
2. **Enable polymorphic behavior** across different implementations.
3. **Prevent direct instantiation** of incomplete/conceptual types.
4. **Share common behavior** while requiring specialization.
5. **Design plugin architectures** where clients provide implementations.

.. note::

   **Example scenarios:** Device drivers (implement ``Device`` interface),
   geometric shapes (implement ``Shape`` interface), data sources (implement
   ``DataSource`` interface), UI widgets (implement ``Widget`` interface).


How is Abstraction Implemented in C++?
----------------------------------------------------

- **Abstract Classes**: Define behavior as a contract using pure ``virtual`` methods.
- **Pure virtual Methods**: Enforce implementation in derived types (``= 0``).
- **Encapsulation**: Keep data private or protected; expose intent through methods.

.. code-block:: cpp

   class Vehicle {
   public:
       virtual ~Vehicle() = default;
       // pure virtual - must be implemented in derived classes
       virtual void drive() = 0;
       // pure virtual - must be implemented in derived classes
       virtual void update_location(const Location &location) = 0;
   };


Pure Virtual Methods (``= 0``)
----------------------------------------------------

A **pure virtual method** is declared with ``= 0`` and:

- **Makes the class abstract** -- cannot be instantiated.
- **Requires derived classes to implement** the method.
- **Defines a contract** that concrete classes must fulfill.
- Can optionally provide a default implementation (rare).

.. code-block:: cpp

   class Vehicle {
   public:
       virtual void drive() = 0;
   };

   // transportation::Vehicle v;  // ERROR: cannot instantiate abstract class

   class RoboTaxi : public Vehicle {
   public:
       void drive() override { /* implementation required */ }
   };

   RoboTaxi rt;  // OK - RoboTaxi has overridden drive()


----


Concrete Classes
====================================================

A **concrete class** is a class that can be instantiated. It provides
complete implementations for all inherited pure ``virtual`` methods.

**Key Characteristics:**

- **Fully defined**: Implements all inherited pure ``virtual`` methods.
- **Instantiable**: Can create objects directly.
- **Observable behavior**: Provides complete, working functionality.
- **Safe to use**: All methods have defined behavior.

**Example -- Complete Concrete Class:**

.. code-block:: cpp

   // Abstract base - defines interface contract
   class Vehicle {
   public:
       virtual ~Vehicle() = default;
       virtual void drive() = 0;
       virtual void stop() = 0;
   };

   // Concrete derived class - implements all pure virtuals
   class RoboTaxi : public Vehicle {
   public:
       ~RoboTaxi() override = default;
       void drive() override { /* RoboTaxi-specific driving logic */ }
       void stop() override  { /* RoboTaxi-specific stopping logic */ }
   };

   // Usage
   transportation::RoboTaxi robo_taxi{"ROBOT001", 6}; // OK - fully concrete
   robo_taxi.drive(); // OK
   // transportation::Vehicle v; // ERROR - abstract class

**Example -- Incomplete Concrete Class:**

.. code-block:: cpp

   // Abstract base - defines interface contract
   class Vehicle {
   public:
       virtual ~Vehicle() = default;
       virtual void drive() = 0;
       virtual void stop() = 0;
   };

   // Concrete derived class - implements all pure virtuals
   class Taxi : public Vehicle {
   public:
       ~Taxi() override = default;
       void drive() override { /* Taxi-specific driving logic */ }
       // void stop() override  { /* Taxi-specific stopping logic */ }
   };

   // Usage
   transportation::Taxi taxi{"TAXI001", 6}; // ERROR - abstract class

.. warning::

   A derived class has to implement **ALL** pure ``virtual`` methods from
   the base class to become a concrete class. We forgot to implement
   ``stop()`` and therefore, ``Taxi`` is also an abstract class.


----


The ``final`` Keyword
====================================================

``final`` prevents further derivation or further overriding. Use it to lock
a design decision and communicate that a hierarchy is closed.


Prevent Class Inheritance
----------------------------------------------------

.. code-block:: cpp

   class RoboTaxi final : public Vehicle { /* ... */ };
   // class SuperRoboTaxi : public RoboTaxi {};  // ERROR: cannot inherit


Prevent Method Overriding
----------------------------------------------------

.. code-block:: cpp

   class Vehicle {
   public:
       virtual void drive() = 0;
       virtual void move() final { /* fixed behavior - cannot override */ }
   };

   class RoboTaxi : public Vehicle {
   public:
       void drive() override { /* OK */ }
       // void move() override { }  // ERROR: move() is final
   };


----


Next Class
====================================================

- **L10:** ROS 2 -- Introduction.
