====================================================
Lecture
====================================================


What Are Exceptions?
====================================================

An **exception** is a runtime event that disrupts the normal flow of a
program. When something goes wrong during execution -- such as dividing
by zero, accessing an invalid index, failing to open a file, or
encountering a network timeout -- the program cannot continue normally.

Without exception handling, these errors typically crash the program
with little useful information. C++ provides a structured mechanism to
**detect**, **signal**, and **recover** from such errors using
exceptions.

Common situations that produce exceptions:

- Dividing by zero
- Accessing an out-of-bounds index in a container
- Failing to open a file
- Running out of memory during allocation
- Receiving invalid input from a sensor or user


``try``, ``catch``, and ``throw``
====================================================

C++ uses three keywords for exception handling:

- ``throw`` -- raises (throws) an exception.
- ``try`` -- wraps a block of code that might throw an exception.
- ``catch`` -- handles the exception if one is thrown.

.. card::
   :class-header: sd-bg-info sd-text-white
   :class-body: sd-bg-light

   Basic Syntax
   ^^^

   .. code-block:: cpp

      try {
          // code that might throw
          throw std::runtime_error("something went wrong");
      } catch (const std::runtime_error& e) {
          std::cout << "Error: " << e.what() << '\n';
      }

Key points:

- ``throw`` creates an exception object and immediately exits the
  current scope.
- The ``try`` block marks the region where exceptions might occur.
- The ``catch`` block receives the exception and handles it.
- **Execution flow**: any code after the ``throw`` statement inside the
  ``try`` block is **skipped**. Control transfers directly to the
  matching ``catch`` block.

You can have **multiple catch blocks** to handle different exception
types:

.. code-block:: cpp

   try {
       // code that might throw different exceptions
   } catch (const std::out_of_range& e) {
       std::cout << "Out of range: " << e.what() << '\n';
   } catch (const std::runtime_error& e) {
       std::cout << "Runtime error: " << e.what() << '\n';
   } catch (...) {
       std::cout << "Unknown exception caught\n";
   }

The **catch-all** handler ``catch (...)`` catches any exception type.
It is typically placed last as a safety net.


Standard Exception Hierarchy
====================================================

C++ provides a hierarchy of exception classes in the ``<stdexcept>``
header. All standard exception classes derive from ``std::exception``,
which provides a virtual ``what()`` method that returns a description
of the error.

.. list-table:: Standard Exception Classes
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - **Class**
     - **Description**
   * - ``std::exception``
     - Base class for all standard exceptions. Provides ``what()``.
   * - ``std::runtime_error``
     - Errors detectable only at runtime (e.g., file not found).
   * - ``std::logic_error``
     - Errors resulting from flawed program logic (e.g., precondition
       violation).
   * - ``std::out_of_range``
     - Thrown by ``.at()`` when an index is out of bounds.
   * - ``std::invalid_argument``
     - Thrown when a function receives an invalid argument.
   * - ``std::bad_alloc``
     - Thrown by ``new`` when memory allocation fails.

.. admonition:: Header
   :class: tip

   Include ``<stdexcept>`` to use ``std::runtime_error``,
   ``std::logic_error``, ``std::out_of_range``, and
   ``std::invalid_argument``. The ``std::bad_alloc`` class is declared
   in ``<new>``.

The hierarchy (simplified):

.. code-block:: text

   std::exception
   +-- std::logic_error
   |   +-- std::invalid_argument
   |   +-- std::out_of_range
   +-- std::runtime_error
   +-- std::bad_alloc


Catching Exceptions
====================================================

Best Practices for Catching
----------------------------------------------------

**Always catch by const reference.** This avoids slicing (losing
derived-class information) and avoids unnecessary copies.

.. code-block:: cpp

   catch (const std::exception& e) {  // good: by const reference
       std::cout << e.what() << '\n';
   }

**Catch order matters.** Place more-derived exception types before
their base classes. If you catch ``std::exception`` first, it will
match all derived types, and more specific handlers will never
execute.

.. code-block:: cpp

   try {
       std::vector<int> vec{1, 2, 3};
       std::cout << vec.at(10) << '\n';  // throws std::out_of_range
   } catch (const std::out_of_range& e) {
       std::cout << "Out of range: " << e.what() << '\n';
   } catch (const std::exception& e) {
       std::cout << "Exception: " << e.what() << '\n';
   }

Re-throwing Exceptions
----------------------------------------------------

Inside a catch block, you can re-throw the current exception using
``throw;`` (with no argument). This is useful when you want to log an
error but let a higher-level handler deal with it.

.. code-block:: cpp

   try {
       process_data();
   } catch (const std::exception& e) {
       std::cout << "Logging error: " << e.what() << '\n';
       throw;  // re-throw the same exception
   }


Throwing Exceptions
====================================================

You can technically throw any type in C++ (an ``int``, a ``std::string``,
a custom object), but **best practice is to throw objects derived from
std::exception**. This ensures that all catch handlers can rely on the
``what()`` method.

.. code-block:: cpp

   double divide(double a, double b) {
       if (b == 0.0) {
           throw std::invalid_argument("division by zero");
       }
       return a / b;
   }

   int main() {
       try {
           double result{divide(10.0, 0.0)};
           std::cout << "Result: " << result << '\n';
       } catch (const std::invalid_argument& e) {
           std::cout << "Error: " << e.what() << '\n';
       }
       return 0;
   }

.. admonition:: Guideline
   :class: tip

   Always throw by value and catch by const reference.


Custom Exception Classes
====================================================

When standard exception types do not provide enough context, you can
create your own exception classes. Inherit from ``std::exception`` or
one of its derived classes (such as ``std::runtime_error``).

.. code-block:: cpp

   #include <stdexcept>
   #include <string>

   class SensorError : public std::runtime_error {
   public:
       SensorError(const std::string& sensor_name, const std::string& message)
           : std::runtime_error("Sensor '" + sensor_name + "': " + message),
             sensor_name_{sensor_name} {}

       const std::string& sensor_name() const { return sensor_name_; }

   private:
       std::string sensor_name_;
   };

Usage:

.. code-block:: cpp

   void read_sensor(const std::string& name, double value) {
       if (value < 0.0) {
           throw SensorError(name, "negative reading");
       }
       std::cout << name << ": " << value << '\n';
   }

   int main() {
       try {
           read_sensor("lidar_front", -1.5);
       } catch (const SensorError& e) {
           std::cout << "Sensor failure on " << e.sensor_name()
                     << ": " << e.what() << '\n';
       }
       return 0;
   }

By deriving from ``std::runtime_error``, your custom class
automatically inherits ``what()`` and can be caught by any handler
that catches ``std::runtime_error`` or ``std::exception``.


``noexcept`` and Exception Safety
====================================================

The ``noexcept`` specifier (introduced in Lecture 6) tells the
compiler that a function will not throw exceptions. If a ``noexcept``
function does throw, the program calls ``std::terminate``.

.. code-block:: cpp

   int safe_add(int a, int b) noexcept {
       return a + b;
   }

Exception Safety Guarantees
----------------------------------------------------

C++ recognizes three levels of exception safety:

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **Guarantee**
     - **Description**
   * - **Nothrow**
     - The function never throws. Destructors and ``swap`` should
       provide this guarantee.
   * - **Strong**
     - If the function throws, the program state is rolled back to
       the state before the call (commit-or-rollback semantics).
   * - **Basic**
     - If the function throws, the program is in a valid (but
       possibly changed) state. No resources are leaked.

RAII and Exception Safety
----------------------------------------------------

**RAII** (Resource Acquisition Is Initialization) ensures that
resources are released when an object goes out of scope, even if an
exception is thrown. Smart pointers (``std::unique_ptr``,
``std::shared_ptr``) and standard containers follow RAII, making
exception-safe code much easier to write.

.. code-block:: cpp

   #include <memory>
   #include <stdexcept>

   void process() {
       auto ptr{std::make_unique<int>(42)};
       // ... code that might throw ...
       throw std::runtime_error("something failed");
       // ptr is automatically deleted when the stack unwinds
   }

.. admonition:: Key Insight
   :class: important

   Destructors run during stack unwinding, so RAII objects clean up
   their resources even when exceptions propagate. This is why smart
   pointers are preferred over raw ``new``/``delete``.


When to Use Exceptions
====================================================

**Use exceptions for:**

- Truly exceptional conditions that cannot be handled locally.
- Errors that cross function boundaries (the caller needs to decide
  how to handle them).
- Constructor failures (constructors have no return value).

**Do not use exceptions for:**

- Normal control flow (e.g., ending a loop).
- Expected conditions (e.g., user entering invalid input in a menu).
  Use ``std::optional`` or return codes instead.
- Performance-critical inner loops.

.. admonition:: Performance Note
   :class: note

   Modern C++ implementations use **zero-cost exception handling**:
   there is no runtime overhead when exceptions are *not* thrown. The
   cost is incurred only when an exception is actually thrown, which
   involves stack unwinding and is relatively expensive.


Best Practices
====================================================

.. admonition:: Do
   :class: tip

   - Always catch by ``const`` reference.
   - Prefer standard exception types (``std::runtime_error``,
     ``std::invalid_argument``, etc.).
   - Use RAII for exception-safe resource management.
   - Throw by value, catch by const reference.
   - Provide meaningful error messages in ``what()``.

.. admonition:: Do Not
   :class: warning

   - Never throw in destructors (can cause ``std::terminate`` during
     stack unwinding).
   - Do not use exceptions for normal control flow.
   - Do not catch exceptions you cannot handle -- let them propagate
     to a handler that can.
   - Do not catch by value (causes slicing).
