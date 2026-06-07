====================================================
Lecture
====================================================

``struct``
====================================================

In C, a ``struct`` is a **Plain Old Data** (POD) container. It is a simple, passive way to group related variables together. It has no methods, no privacy, and no complex behaviors.

When C++ was born, it took the C-style ``struct`` and gave it superpowers. In C++, a ``struct`` is, for all intents and purposes, a ``class``. The C heritage, however, still strongly influences how we use it.

In C++, ``struct`` and ``class`` are nearly identical. The **only** difference is the default access level: by default, members are **public** in ``struct`` and **private** in ``class``.

.. admonition:: Convention
   :class: tip

   Use ``struct`` for simple data containers (POD types). Use ``class`` when you need encapsulation and private data.


``struct`` vs ``class``
------------------------

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: struct (public by default)
      :class-card: sd-border-primary

      .. code-block:: cpp

         struct Robot {
             // PUBLIC by default
             std::string name;
             double speed;

             // Constructor
             Robot(std::string n, double s)
                 : name(n), speed(s) {}

             // Method
             void move(double distance) {
                 std::cout << name << " moving "
                     << distance << "m at "
                     << speed << " m/s\n";
             }
         };

         // Usage
         Robot r{"R2D2", 1.5};
         r.move(10.0);  // works
         std::cout << r.name;  // works

   .. grid-item-card:: class (private by default)
      :class-card: sd-border-secondary

      .. code-block:: cpp

         class Robot {
             // PRIVATE by default
             std::string name;
             double speed;

         public:  // Must explicitly say public!
             // Constructor
             Robot(std::string n, double s)
                 : name(n), speed(s) {}

             // Method
             void move(double distance) {
                 std::cout << name << " moving "
                           << distance << "m at "
                           << speed << " m/s\n";
             }
         };

         // Usage
         Robot r{"R2D2", 1.5};
         r.move(10.0);  // works
         // std::cout << r.name;  // ERROR: private!


Aggregate Initialization
--------------------------

The most "struct-like" feature is aggregate initialization. An "aggregate" is, broadly, a type (like a ``struct`` or array) with no user-defined constructors, no private or protected non-static data members, and no virtual functions.

.. code-block:: cpp

   struct Point {
       double x;
       double y;
       std::string label{"default"}; // C++11 default member initializer
   };

   int main() {
       // Aggregate Initialization
       Point p1 = {10.0, 20.0, "center"}; // Initializes x, y, label
       Point p2 = {10.0, 20.0};           // Initializes x, y. label uses its default.

       std::cout << p1.label << '\n'; // "center"
       std::cout << p2.label << '\n'; // "default"
   }


Structured Bindings
---------------------

Structured bindings allow you to decompose a ``struct``'s members into distinct local variables. It binds to the non-static data members of the ``struct`` in the order they are declared.

.. code-block:: cpp

   Point get_start_point() { return {1.0, 2.0}; }

   int main() {
       Point p = get_start_point();
       auto [x, y, label] = p; // Magic!

       // Variables x, y, and label are created and populated
       std::cout << "X: " << x << ", Y: " << y << ", Label: " << label << '\n';
   }

You can also bind by reference to modify the original ``struct``.

.. code-block:: cpp

   Point p = {10.0, 20.0};
   auto& [x_ref, y_ref, label_ref] = p;

   x_ref = 100.0; // This modifies p.x

   std::cout << p.x << '\n'; // Prints 100.0


Templates
====================================================

A template is a **blueprint** (generic programming) the compiler uses to generate concrete functions or types. You write with type parameters (e.g., ``T``); the compiler *instantiates* actual code for the types you use.

.. admonition:: Generic Programming Essentials
   :class: note

   1. **Separate algorithms from types**: write logic once.
   2. **Parameterize over types**: use placeholders (e.g., ``T``).
   3. **Enforce static correctness**: errors at compile time.
   4. **Zero-overhead**: optimal code for each instantiation.


Without Templates vs With Templates
--------------------------------------

**Without templates**, you must duplicate the same logic for each type:

.. code-block:: cpp

   int add(int a, int b) {
       return a + b;
   }

   double add(double a, double b) {
       return a + b;
   }

   std::string add(const std::string& a, const std::string& b) {
       return a + b;
   }

Same logic written three times. Any bug fix or improvement must be duplicated, violating **DRY**.

**With templates**, you write the logic once:

.. code-block:: cpp

   template<typename T>
   T add(T a, T b) {
       return a + b;
   }

When called, the compiler generates (instantiates) the needed concrete overloads, e.g., ``int add(int,int)``, ``double add(double,double)``, ``std::string add(const std::string&, const std::string&)``.


Syntax
--------

.. code-block:: cpp

   template<typename T>
   ReturnType function_name(T parameter) {
       // function body
   }

Or equivalently:

.. code-block:: cpp

   template<class T>
   ReturnType function_name(T parameter) {
       // function body
   }

- ``typename`` and ``class`` are interchangeable in parameter lists (historical difference only).

.. admonition:: Best Practice
   :class: tip

   Prefer ``typename`` for clarity in modern code.


Benefits
----------

1. **Maintainability**: fix once, apply everywhere.
2. **Consistency**: identical logic for all types.
3. **Flexibility**: support new types without new code.
4. **Less code**: fewer duplicates in sources.


Template vs Function Overloading
-----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 20 20

   * - Scenario
     - Use Overloading
     - Use Templates
   * - Same logic for all types
     - No
     - Yes
   * - Different logic per type
     - Yes
     - No
   * - Type-specific optimizations
     - Yes
     - Yes (specialize later)
   * - Simple, clear intent
     - Yes
     - Depends on complexity
   * - Avoiding code duplication
     - No
     - Yes


Instantiation
---------------

A template is stored as a blueprint; the compiler *instantiates* concrete functions only when used.

.. code-block:: cpp

   template<typename T>
   T multiply(T a, T b) {
       return a * b;
   }

   int main() {
       int result1{multiply(3, 4)};          // instantiates multiply<int>
       double result2{multiply(2.5, 4.0)};   // instantiates multiply<double>
       int result3{multiply(5, 6)};          // reuses multiply<int> (no new code)
   }


Definition
------------

Always define template functions and classes in header files (``.hpp``), **not** in separate ``.cpp`` files.

**Why?** Templates are **not compiled** until they are **instantiated**.

1. **Compilation happens when used**: The compiler generates actual code only when you call the template with specific types.
2. **Compiler needs full definition**: To instantiate, the compiler must see the complete template definition, not just a declaration.
3. **Separate compilation breaks**: If the definition is in a ``.cpp`` file, other translation units cannot see it and cannot instantiate.

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: Wrong: Separate Files
      :class-card: sd-border-danger

      .. code-block:: cpp

         // week6.hpp
         template<typename T>
         T add(T a, T b);  // Declaration only

         // week6.cpp
         template<typename T>
         T add(T a, T b) {  // Definition
             return a + b;
         }

         // main.cpp
         #include "week6.hpp"
         int main() {
             add(3, 4);  // Linker error!
                         // undefined reference ...
         }

   .. grid-item-card:: Correct: In Header
      :class-card: sd-border-success

      .. code-block:: cpp

         // week6.hpp
         template<typename T>
         // Definition in header
         T add(T a, T b) {
             return a + b;
         }

         // main.cpp
         #include "week6.hpp"
         int main() {
             add(3, 4);  // Works!
             // Compiler sees definition,
             // instantiates add<int>
         }

.. admonition:: Remember
   :class: note

   Template code is like a blueprint -- the compiler needs to see the entire blueprint to build the actual function for each type you use.


Template Documentation
------------------------

Essential Doxygen tags for templates:

- ``@tparam T`` for each template parameter
- ``@param``, ``@return`` as usual
- ``@brief``, ``@details`` for summaries
- ``@note``, ``@warning`` for constraints
- ``@ingroup``, ``@file``, ``@namespace`` for organization

.. code-block:: cpp

   /// @file math_utils.hpp
   /// @brief Small numeric utilities.

   #pragma once

   /**
    * @brief Returns the greater of two values.
    *
    * @tparam T A totally ordered type (requires operator>).
    * @param a First value.
    * @param b Second value.
    * @return The larger of @p a and @p b.
    * @note Use explicit template arguments if deduction is ambiguous.
    * @code
    * auto m{max_value<int>(3, 4)};
    * @endcode
    */
   template<typename T>
   T max_value(T a, T b)
   {
       return (a > b) ? a : b;
   }


Multiple Template Parameters
-------------------------------

A template can have multiple independent type parameters.

.. code-block:: cpp

   template<typename T, typename U>
   auto add_different(T a, U b) {
       return a + b;  // deduce from operator+
   }

   int main() {
       int r1{add_different(3, 4)};        // int
       double r2{add_different(3, 4.5)};   // double
       double r3{add_different(3.5, 4)};   // double
   }

Using ``auto`` as the return type lets the compiler automatically deduce the result type from the ``return`` statement.


Explicit Template Arguments
------------------------------

If deduction fails or you want a different type than deduction would choose, specify template arguments explicitly.

.. code-block:: cpp

   function_name<type1, type2, ...>(arguments);

- Each type in ``<...>`` binds to a template parameter.
- When you specify them, the compiler skips deduction for those parameters.

.. code-block:: cpp

   template<typename T>
   void print_twice(T value) {
       std::cout << value << " " << value << '\n';
   }

   int main() {
       print_twice(10);        // T deduced as int
       print_twice<int>(10);   // explicitly T = int (same result)
   }

**Partial explicit specification:**

.. code-block:: cpp

   template<typename T, typename U>
   void display_pair(T a, U b) {
       std::cout << a << ", " << b << '\n';
   }

   int main() {
       display_pair<int>(5, 3.14); // T fixed to int, U deduced as double
   }


Template Type Deduction
-------------------------

The compiler deduces template parameters from the function arguments you pass.

.. code-block:: cpp

   template<typename T>
   T add(T a, T b) {
       return a + b;
   }

   int main() {
       int result{add(3, 5)};  // deduces T = int
   }

- Arguments ``3`` and ``5`` are ``int`` => ``T`` is ``int``.
- Compiler instantiates ``int add(int, int)``.

**Deduction with References**

.. code-block:: cpp

   template<typename T>
   void modify(T& value) {
       value *= 2;
   }

   int main() {
       int x{10};
       modify(x);  // T deduced as int; x becomes 20
   }

The reference is part of the template parameter list (``T&``); the deduced ``T`` is ``int``, not ``int&``.

**Deduction with** ``const``

.. code-block:: cpp

   template<typename T>
   void print(const T& value) {
       std::cout << value << '\n';
   }

   int main() {
       int x{42};
       print(x);   // T deduced as int

       const int y{99};
       print(y);   // T deduced as int (const is applied by the parameter type)
   }

**Override the Deduced Type**

.. code-block:: cpp

   template<typename T>
   void process(T value) {
       std::cout << typeid(T).name() << '\n';
   }

   int main() {
       short s{42};
       process(s);        // T is short
       process<int>(s);   // force T = int (converts before call)
   }


Deduction Failures
--------------------

**When Deduction Fails**

.. code-block:: cpp

   template<typename T>
   T create_value() { return T{}; }

   int main() {
       // create_value();           // ERROR: cannot deduce T
       auto v{create_value<int>()}; // OK
   }

**Ambiguity**

.. code-block:: cpp

   template<typename T>
   T get_value(T a, T b) {
       return a;
   }

   int main() {
       int result{get_value(3, 4.5)}; // ERROR: T = int or T = double?
   }

During deduction, one consistent ``T`` must satisfy all parameters. Here it cannot.

**Impossibility**

.. code-block:: cpp

   template<typename T>
   T create_value() {
       return T{};
   }

   int main() {
       auto result{create_value()};  // ERROR: cannot deduce T
       // Even: int r{create_value()}; // still ERROR
   }

Deduction uses only function *parameters*. Return types and assignment targets are *not* used for deduction.

**Type Mismatch**

.. code-block:: cpp

   template<typename T>
   void process(T* ptr) { /* expects a pointer */ }

   int main() {
       int x{42};
       process(x);  // ERROR: x is not a pointer
   }


Template Specialization
--------------------------

Templates are generic by default, but some types need different behavior. Specialization customizes a template for specific types.

**Full Specialization**

A full specialization provides a complete, alternative definition for a specific type or type combination.

.. code-block:: cpp

   template<>
   ReturnType function_name<SpecificType>(parameter_list) {
       // specialized implementation
   }

**Special Handling for Strings**

.. code-block:: cpp

   template<typename T> // generic
   T get_max(T a, T b) {
       return (a > b) ? a : b;
   }

   template<> // full specialization for std::string
   std::string get_max<std::string>(std::string a, std::string b) {
       std::cout << "Using string specialization!\n";
       return (a.length() > b.length()) ? a : b;
   }

   int main() {
       int max_int{get_max(3, 5)};                               // generic
       std::string max_str{get_max<std::string>("hi", "hello")}; // specialized
   }

**Optimized Version for** ``bool``

.. code-block:: cpp

   template<typename T>
   void process(T value) {
       std::cout << "Processing generic value: " << value << '\n';
   }

   template<> // full specialization
   void process<bool>(bool value) {
       std::cout << "Processing bool: " << (value ? "true" : "false") << '\n';
   }

   int main() {
       process(42);    // generic
       process(true);  // specialized
   }

**When to specialize?**

- **Performance**: a type admits a faster implementation.
- **Semantics**: a type needs different behavior.
- **Integration**: adapt external/library types.


Function Operators, Specifiers, and Attributes
====================================================

Beyond the function signature, C++ provides several mechanisms to convey extra information about a function's *behavior*, *usage*, and *constraints*.

- **Operators** perform actions or evaluations (e.g., ``+``, ``!``). They produce a result or effect at compile time or runtime.
- **Specifiers** modify how the compiler interprets a declaration. They affect linkage, optimization, or exception guarantees.
- **Attributes** provide metadata or hints to the compiler. They do not alter semantics but influence diagnostics and intent.


``decltype`` Operator
-----------------------

The ``decltype`` operator inspects the *type* of an expression at compile time **without evaluating it**. It allows developers to deduce types automatically based on expressions, ensuring type consistency in templates and generic code.

**Basic Usage**

.. code-block:: cpp

   double average(double a, double b) {
       return (a + b) / 2.0;
   }

   int main() {
       int x{42};
       decltype(x) y{10}; // y has same type as x (int)
       decltype(average(1.0, 2.0)) result{0.0}; // deduces double
   }

``decltype(expr)`` inspects the type of ``expr`` at compile time and returns it as a type. Unlike ``auto``, it does **not evaluate** the expression (only analyzes its declared type).

**Reference and Const Deduction**

.. code-block:: cpp

   int n{10};
   int& ref{n};
   const int c{5};

   decltype(n)   a{0};   // int
   decltype(ref) b{n};   // int&   (reference preserved)
   decltype(c)   d{7};   // const int (const preserved)
   decltype((n)) e{n};   // int&   (parentheses -> lvalue expression)

Parentheses are important! ``decltype(expr)`` preserves ``const`` and reference qualifiers depending on the expression form. If ``expr`` is an lvalue, ``decltype(expr)`` yields a ``T&`` type.

**Understanding Value Categories**

Expressions in C++ are classified into three **value categories**:

- **lvalue** ("locator value"): Has an identifiable memory address. Can appear on the left side of ``=``. Examples: variables, array elements, dereferenced pointers, string literals.
- **prvalue** ("pure rvalue"): Temporary or computed value with no persistent address. It **cannot appear on the left-hand side of** ``=``. Examples: literals (e.g., ``42``, ``3.14``), results of expressions like ``x + y``.
- **xvalue** ("expiring value"): Represents a resource that can be reused or moved from. Example: ``std::move(x)``.

.. code-block:: cpp

   int x{42};
   int* ptr{&x};   // OK: x is an lvalue
   // int* p{&42}; // ERROR: 42 is a prvalue (no address)

   int y{x + 5};   // (x + 5) is a prvalue (temporary)

**decltype and Expression Categories**

The type produced by ``decltype(expr)`` depends on whether ``expr`` is an **identifier**, an **lvalue expression**, or a **prvalue**.

.. code-block:: cpp

   int x{10};

   // decltype with identifiers (no parentheses)
   decltype(x)     a{0};    // int       (x's declared type)

   // decltype with expressions (parentheses or operations)
   decltype((x))   b{x};    // int&      (x is an lvalue expression)
   decltype(x + 0) c{0};    // int       (x + 0 is a prvalue)
   decltype(*(&x)) d{x};    // int&      (*(&x) is an lvalue)

.. admonition:: Rule of Thumb
   :class: tip

   - ``decltype(id)`` -> declared type
   - ``decltype(lvalue-expr)`` -> ``T&``
   - ``decltype(prvalue-expr)`` -> ``T``

**Practical Examples**

.. code-block:: cpp

   int arr[5]{1, 2, 3, 4, 5};
   const int c{100};

   decltype(arr[0])     v1{arr[1]};   // int&       (arr[0] is lvalue)
   decltype(arr[0] + 1) v2{0};        // int        (arithmetic -> prvalue)
   decltype(c)          v3{50};       // const int  (const preserved)
   decltype((c))        v4{c};        // const int& (lvalue expression)

   int get_value() { return 42; }
   decltype(get_value()) v5{0};  // int (function call -> prvalue)

In template or generic code, ``decltype`` allows perfect type deduction -- preserving references, constness, and distinguishing between lvalues and prvalues.

**Difference Between** ``auto`` **and** ``decltype``

.. list-table::
   :header-rows: 1
   :widths: 25 35 35

   * - Feature
     - ``auto``
     - ``decltype``
   * - Evaluates expression
     - Yes (value-based deduction)
     - No (type-only inspection)
   * - Preserves references
     - Drops them
     - Preserves them
   * - Preserves const qualifiers
     - Removes them
     - Keeps them
   * - Common usage
     - Variable initialization
     - Type extraction and template return types

``decltype`` provides exact compile-time type information. ``auto`` deduces from evaluated expressions, sometimes dropping qualifiers.

**Using decltype with Variables**

.. code-block:: cpp

   int x{10};
   int y{20};

   // Declare a variable with the same type as an expression
   decltype(x + y) sum{x + y};  // sum is int

   // With function calls
   double calculate(double a, double b) { return a * b; }
   decltype(calculate(2.0, 3.0)) result{calculate(2.5, 4.0)}; // double

**Common Pitfalls**

.. code-block:: cpp

   // Parentheses change meaning
   int x{5};
   decltype(x) a{0};   // int        (declared type)
   decltype((x)) b{x}; // int&       (lvalue expression)

   // decltype of a temporary
   decltype(x + 1) c{42}; // int (prvalue expression)

Be mindful of parentheses and expression category. ``decltype((x))`` yields a reference type since ``(x)`` is an lvalue, while ``decltype(x)`` gives the declared type directly.

.. admonition:: Best Practices for ``decltype``
   :class: tip

   - Use ``decltype`` to replicate another variable's type or an expression's result.
   - Combine with ``auto`` in templates for precise return-type deduction.
   - Avoid unnecessary usage when the type is obvious -- clarity comes first.
   - Remember: ``decltype`` never evaluates expressions; it only inspects their static type.


Trailing Return Type
----------------------

Introduced in C++11, the **trailing return type** syntax allows the return type to appear *after* the parameter list.

.. code-block:: cpp

   auto add(int a, int b) -> int {
       return a + b;
   }

This syntax is an alternative way to declare return types. It is particularly useful when the function's return type depends on its parameter types, which the compiler only knows after parsing the parameter list.

**Purpose and Motivation**

Traditional function declarations place the return type before the function name:

.. code-block:: cpp

   int add(int a, int b);

However, this becomes problematic in *templates* or complex C++ constructs where the return type depends on the parameter types.

.. code-block:: cpp

   template <typename T, typename U>
   ??? multiply(const T& a, const U& b) {  // What type goes here?
       return a * b;
   }

The compiler needs to know ``T`` and ``U`` before deducing the return type, but in traditional syntax, the return type comes *first*!

**Solution**: use ``auto`` or trailing return type ``-> decltype()``.

**Perfect Return Type Deduction**

.. code-block:: cpp

   template <typename T, typename U>
   auto multiply(const T& a, const U& b) -> decltype(a * b) {
       return a * b;
   }

   int main() {
       std::cout << multiply(2, 3.5) << '\n';     // 7.0 (double)
       std::cout << multiply(2.5, 3) << '\n';     // 7.5 (double)
       std::cout << multiply(2, 3) << '\n';       // 6 (int)
   }

The trailing return type ``-> decltype(a * b)`` ensures the return type exactly matches the result of the expression, regardless of operand types.

**Generic Arithmetic Operations**

.. code-block:: cpp

   template <typename T>
   auto square(const T& value) -> decltype(value * value) {
       return value * value;
   }

   template <typename T, typename U>
   auto add(const T& a, const U& b) -> decltype(a + b) {
       return a + b;
   }

``decltype`` ensures template functions adapt to any operand type -- from built-ins to user-defined types -- by deducing the expression's true return type.

**Why This Matters**

- **Type Safety**: Return type automatically matches the actual operation result.
- **Flexibility**: Works with custom types that overload operators.
- **Precision**: Preserves const, references, and value categories.
- **Future-Proof**: Code adapts automatically when types change.

**C++14 Simplification**

In C++14 and later, **simple cases** can use plain ``auto``:

.. code-block:: cpp

   // C++11: Explicit trailing return type
   template <typename T, typename U>
   auto add(T a, U b) -> decltype(a + b) {
       return a + b;
   }

   // C++14: Automatic deduction (simpler)
   template <typename T, typename U>
   auto add(T a, U b) {
       return a + b;  // compiler figures it out
   }

**When Are They Different?**

*Case 1: Returning References*

.. code-block:: cpp

   // Plain auto
   template <typename T>
   auto get_auto(T& ref) {
       return ref;  // Returns int (COPY!)
   }

   // With decltype
   template <typename T>
   auto get_decltype(T& ref) -> decltype(ref) {
       return ref;  // Returns int& (REFERENCE)
   }

   int main() {
       int x{42};
       get_auto(x) = 99;      // ERROR: can't assign to temporary
       get_decltype(x) = 99;  // OK: x becomes 99
   }

*Case 2: Returning const-ref*

.. code-block:: cpp

   const int global_value{3};
   const int& get_const_ref() { return global_value; }

   int main() {
       auto result1 = get_const_ref();         // int (copy; const & dropped)
       decltype(get_const_ref()) result2 = get_const_ref(); // const int&
       decltype(auto) result3 = get_const_ref();            // const int&
   }

**Takeaway**: ``auto`` copies and drops top-level ``const``/``&``. ``decltype(expr)`` and ``decltype(auto)`` reproduce the exact type of ``expr``.

.. admonition:: Best Practices
   :class: tip

   1. Use ``auto`` return type for simple template functions (C++14+).
   2. Use ``-> decltype(expr)`` when you need precise control over return type qualifiers, explicit documentation of the return type, or compatibility with C++11.
   3. Test template functions with various types, including user-defined types.


``constexpr`` Specifier
-------------------------

The ``constexpr`` specifier marks an expression or function as **potentially evaluable at compile time**. When called with constant arguments, the compiler computes the result **during compilation**. When called with runtime values, it executes like a normal function.

**Compile-Time Function Evaluation**

.. code-block:: cpp

   constexpr int square(int x) {
       return x * x;
   }

   int main() {
       constexpr int n{square(5)}; // evaluated at compile time
       int m{7};
       int result = square(m);      // evaluated at runtime
   }

``constexpr`` ensures a function **can** be evaluated at compile time, but does not require it to be. If all arguments are constant expressions, the compiler computes the result during compilation. If any argument is not constant, evaluation occurs at runtime.

**What Happens When Evaluated at Compile Time?**

When a ``constexpr`` function is evaluated at compile time:

- The compiler replaces the call with its computed result, as if it were a literal constant.
- No machine instructions are generated for that call.
- The value becomes part of the program's static data segment.

.. code-block:: cpp

   constexpr int cube(int n) { return n * n * n; }

   constexpr int volume{cube(4)}; // compiler computes 64 here
   int array[volume];              // valid: array size known at compile time

**Compile-time evaluation benefits:**

- Eliminates runtime computation -- improves performance.
- Enables use of results in contexts that require compile-time constants (e.g., array sizes, template arguments, ``switch`` cases).
- Detects logic errors early -- during compilation.

**Requirements for constexpr Functions**

A ``constexpr`` function must:

- Have a definition visible to the compiler (typically in a header file).
- Contain a single ``return`` statement before C++14 (relaxed in later standards).
- Operate only on arguments and expressions that can be constant at compile time.
- Avoid inherently runtime operations (I/O, dynamic memory, exceptions, etc.).

From C++14 onward, ``constexpr`` functions may include variables, loops, and conditionals, as long as their evaluation is deterministic and can be resolved by the compiler.

.. admonition:: Best Practices for ``constexpr``
   :class: tip

   - Use ``constexpr`` for lightweight, deterministic, side-effect-free computations.
   - Prefer ``constexpr`` when a result can safely be computed once at compile time.
   - Combine with ``constexpr`` variables or ``std::array`` bounds for extra safety.
   - Remember: ``constexpr`` shifts computation from runtime to compile time, improving both *performance* and *reliability*.


``inline`` Specifier
-----------------------

An ``inline`` function requests that the compiler perform an optimization known as **inlining**. **Inlining** is the process of replacing the function call with the actual body of the function at the spot where it was called (the "call site").

**The Problem with Functions**

Every function call involves several hidden steps. Together, these steps contribute to what is known as **function call overhead**.

- **Save the Context**: The program records its current state by pushing the return address onto the stack.
- **Push the Arguments**: All function parameters and local variables are placed onto the stack.
- **Transfer Control**: The instruction pointer moves to a new memory location.
- **Execute the Function**: The processor carries out the operations.
- **Store the Return Value**: The result is placed in a designated CPU register.
- **Restore the Stack**: The function's stack frame is removed.
- **Return Control**: The program retrieves the saved return address and resumes.

.. code-block:: cpp

   int add(int a, int b) {
       return a + b;
   }

   // Called in a loop...
   int total{0};
   for (int i{0}; i < 1000000; ++i) {
       total = add(total, i); // A million function calls!
   }

In this case, the overhead of calling the function millions of times may exceed the cost of performing the addition itself.

.. code-block:: cpp

   inline int add(int a, int b) { // inline
       return a + b;
   }

   // Called in a loop...
   int total{0};
   for (int i{0}; i < 1000000; ++i) {
       total = total + i; // Compiler may use the function body directly
   }

The output is identical, but the compiler may replace the function call with the function's body, eliminating the call overhead entirely.

**The inline Keyword Is Only a Hint**

``inline`` is a suggestion, not a command. The compiler is free to ignore the request. The compiler typically avoids inlining when a function is:

- **Large**: Expanding a long function would bloat the code.
- **Recursive**: Fully inlining a self-calling function is not feasible.
- **Loop-heavy**: Functions containing loops are usually poor inlining candidates.
- **Virtual**: Because ``virtual`` calls are resolved at runtime, the compiler generally cannot inline them.

Modern compilers may choose to ``inline`` a function even if you never mark it with the ``inline`` keyword.

**The One Definition Rule (ODR)**

If modern compilers can decide on their own when to inline, why does C++ still have the ``inline`` keyword? Because of the **One Definition Rule (ODR)**, not for performance, but for *linkage and consistency across translation units*.

C++ enforces the **One Definition Rule (ODR)**, which states:

   *A function may be declared multiple times (for example, in several header files), but it must be defined exactly once in the entire program.*

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: Without ``inline`` -- ODR Violation
      :class-card: sd-border-danger

      .. code-block:: cpp

         // utils.hpp
         #pragma once

         // A non-inline function DEFINITION
         int add(int a, int b) {
             return a + b;
         }

      .. code-block:: cpp

         // main.cpp
         #include "utils.hpp"
         #include <iostream>

         int main() {
             std::cout << add(5, 10) << '\n';
         }

      .. code-block:: cpp

         // other.cpp
         #include "utils.hpp"

      Compiling produces a linker error: *multiple definition of 'add(int, int)'*.

   .. grid-item-card:: With ``inline`` -- Legal
      :class-card: sd-border-success

      .. code-block:: cpp

         // utils.hpp
         #pragma once

         // This is now perfectly legal!
         inline int add(int a, int b) {
             return a + b;
         }

      Using the ``inline`` specifier relaxes the ODR. It informs the linker that identical definitions across translation units refer to the same function (keep one and discard the duplicates).

.. admonition:: Best Practices for ``inline``
   :class: tip

   - The definitions of ``inline`` functions must be placed in header files (``.hpp``).
   - When a method (class member function) is **defined inside** a class body, it is implicitly ``inline``, so defining it in a header file is perfectly valid.
   - If you define a function **outside** the class and mark it as ``inline``, that single definition must be visible to every translation unit. Place the definition in the header file, not in the source file.


``noexcept`` Specifier/Operator
---------------------------------

The ``noexcept`` specifier is a **compile-time promise** that a function will not throw an exception. The compiler can make aggressive optimizations based on this guarantee.

.. code-block:: cpp

   void safe_operation() noexcept {
       // This function guarantees it won't throw
   }

   void risky_operation() {
       // This function might throw
   }

If an exception is thrown from a ``noexcept`` function, ``std::terminate()`` is called.

**Exceptions vs Errors**

- **Exceptions** represent *recoverable, unexpected conditions* detected at runtime. They signal that something went wrong, but the program can often handle it and continue safely.
- **Errors** represent *unrecoverable situations* where program execution cannot proceed safely. They often indicate logic faults, contract violations, or conditions outside the program's control.

**Why noexcept?**

Exceptions introduce runtime overhead and complicate optimization.

- When the compiler cannot guarantee that a function will not throw, it must generate extra code to handle stack unwinding and clean-up.
- Marking a function ``noexcept`` lets the compiler skip this extra code and optimize more aggressively.
- It also conveys intent to other developers: "this function is safe and predictable."

Use ``noexcept`` for small, low-level, or performance-critical functions that are not expected to throw.

**The noexcept Operator**

``noexcept`` is also an **operator** that checks whether an expression is ``noexcept`` at compile time.

.. code-block:: cpp

   void might_throw();
   void never_throw() noexcept;

   bool check1{noexcept(never_throw())};   // true
   bool check2{noexcept(might_throw())};   // false
   bool check3{noexcept(1 + 2)};           // true

The ``noexcept(...)`` operator:

- Returns ``true`` if the expression inside is guaranteed not to throw.
- Returns ``false`` if the expression might throw.
- Evaluation happens at **compile-time**.

**Dynamic noexcept Conditions**

The ``noexcept`` specifier can take a Boolean expression evaluated at compile time.

.. code-block:: cpp

   void never_throw() noexcept;

   void demo() noexcept(noexcept(never_throw())) {
               // |     // |- Inner noexcept(...):  OPERATOR
               // |     // '- "Is never_throw() noexcept?"
               // |
               // |- Outer noexcept(...):  SPECIFICATION
               // '- "Make demo() noexcept IF the condition is true"
   }

- **Inner**: Evaluates to a boolean at compile time.
- **Outer**: Specifies whether ``demo()`` should be marked ``noexcept``.

**Practical Example**

.. code-block:: cpp

   void might_throw();
   void never_throw() noexcept;

   // Will NOT be noexcept
   void demo1() noexcept(noexcept(might_throw())) {
       might_throw();  // Might throw
   }

   // WILL be noexcept
   void demo2() noexcept(noexcept(never_throw())) {
       never_throw();  // Never throws
   }

- ``demo1()`` inherits the exception risk from ``might_throw()``.
- ``demo2()`` is safe because ``never_throw()`` is safe.

**When NOT to Use noexcept**

- When a function may legitimately throw and the caller should handle it.
- When working with third-party or legacy functions not marked ``noexcept``.
- When you are uncertain about whether the function is truly exception-safe.

.. code-block:: cpp

   // GOOD: Clearly might fail
   int parse_number(const std::string& s) {
       return std::stoi(s);  // May throw
   }

   // GOOD: Simple operation
   void reset_counter() noexcept {
       counter = 0;  // Can't fail
   }

.. admonition:: Best Practices for ``noexcept``
   :class: tip

   - Mark simple, guaranteed-safe operations as ``noexcept``.
   - Don't lie: if a function might throw, don't mark it ``noexcept``.
   - Document exception guarantees in comments or with ``noexcept``.
   - ``noexcept`` expresses **intent** and enables compiler optimizations.


Function Attributes
---------------------

Attributes provide the compiler with additional information about functions or variables, influencing warnings, optimizations, or behavior without changing the program's semantics.


``[[nodiscard]]``
^^^^^^^^^^^^^^^^^^^

The ``[[nodiscard]]`` attribute warns if a function's return value is ignored. It encourages safer, more intentional code by catching overlooked results.

.. code-block:: cpp

   [[nodiscard]] int compute_total(int x, int y) {
       return x + y;
   }

   int main() {
       compute_total(2, 3); // Warning: result of 'compute_total' is discarded
   }

Use ``[[nodiscard]]`` for functions whose result is important and should not be silently ignored.

**Custom Message**

You can provide a message to clarify why ignoring the return value is risky.

.. code-block:: cpp

   [[nodiscard("You should check for success before continuing")]]
   bool process_data(int id);

   int main() {
       process_data(42); // Compiler warning with custom message
   }

.. admonition:: Best Practices for ``[[nodiscard]]``
   :class: tip

   - Apply to functions returning critical status codes, error flags, or computed values.
   - Avoid excessive use (reserve it for meaningful results). Some functions return a value for convenience, but their main purpose is to perform an action.
   - Can also be applied to classes, marking all constructors' return values as significant.


``[[maybe_unused]]``
^^^^^^^^^^^^^^^^^^^^^^

The ``[[maybe_unused]]`` attribute tells the compiler that a variable, parameter, function, or type **might be intentionally unused**. It prevents warnings such as *"unused variable"* or *"unused parameter"*.

.. code-block:: cpp

   // Compile with: -Wall -Wextra -Werror
   [[maybe_unused]] void debug_print(const std::string& msg) {
       std::cerr << msg << '\n';
   }

   int main() {
       [[maybe_unused]] int temp_value{42};   // No warning even with -Wextra -Werror

       bool debug_mode = false;
       if (debug_mode)
           debug_print("Diagnostics enabled.");
   }

Without ``[[maybe_unused]]``, the compiler may emit an error under ``-Wextra -Werror``, which treats all warnings as errors. This attribute explicitly documents that the unused state is intentional.

**Common Use Cases**

- **Template Parameters**: Some template parameters may not be used in every specialization.

  .. code-block:: cpp

     template <typename T, typename U>
     void process(const T& a, [[maybe_unused]] const U& b) {
         std::cout << a << '\n'; // OK: 'b' may not be used
     }

- **Platform or Context Variants**: Functions may include parameters required on some systems but not others.

  .. code-block:: cpp

     void initialize([[maybe_unused]] int device_id) {
         std::cout << "Initialization complete.\n";
         // Some environments do not need 'device_id'
     }

- **Debug or Logging Helpers**: Useful when diagnostic code can be toggled on/off without changing function signatures.

  .. code-block:: cpp

     void log_info([[maybe_unused]] const std::string& message) {
         // Logging disabled in production builds
     }

**When to Use vs When to Avoid**

Use ``[[maybe_unused]]`` when a variable, parameter, or function exists for clarity, documentation, or future expansion, and might not be referenced in every configuration.

Avoid using it to silence warnings created by actual mistakes.

.. code-block:: cpp

   // Misuse: hides a bug under -Wextra -Werror
   int compute_sum(int a, int b) {
       [[maybe_unused]] int result = a + b; // Suppresses warning
       return 0; // Bug: forgot to return result
   }

.. admonition:: Best Practices for ``[[maybe_unused]]``
   :class: tip

   - Use when a symbol may legitimately remain unused in certain builds or code paths.
   - Combine with compiler flags such as ``-Wall -Wextra -Werror`` to maintain strict code hygiene.
   - Document why it is unused -- e.g., performance testing, logging, or template flexibility.
   - Do **not** use as a blanket fix for warnings; prefer removing unnecessary variables.


``[[deprecated]]``
^^^^^^^^^^^^^^^^^^^^^

The ``[[deprecated]]`` attribute marks a function, variable, or type as obsolete. It triggers a compiler warning when used, signaling that newer alternatives exist.

.. code-block:: cpp

   [[deprecated("Use compute_area() instead")]]
   double calc_area(double r) {
       return 3.14159 * r * r;
   }

   double compute_area(double r) { return 3.14159 * r * r; }

   int main() {
       double a = calc_area(2.0); // Warning: 'calc_area' is deprecated
   }

.. admonition:: Best Practices for ``[[deprecated]]``
   :class: tip

   - Use when phasing out old APIs, functions, or constants.
   - Always include a message pointing to the preferred alternative.
   - Avoid removing deprecated code abruptly; deprecation helps maintain backward compatibility.

**Summary**: Attributes like ``[[nodiscard]]``, ``[[maybe_unused]]``, and ``[[deprecated]]`` improve code safety, clarity, and maintainability. They do not change program semantics -- they help the compiler help you.


Callables
====================================================

The term **callable** is a broad concept that refers to anything that can be invoked using the function-call syntax. If you can write ``f(arg1, arg2)``, then ``f`` is a callable.

There are six main "things" in C++ that satisfy this definition:

1. Functions (and Function Pointers)
2. Functors (Function Objects)
3. Lambdas
4. Member Functions (and Pointers to Member Functions)
5. Bound Functions (from ``std::bind``)
6. Standard Tools: ``std::function`` and ``std::invoke``


Function Pointers
-------------------

A function pointer is a variable that stores the address of a function, allowing you to call that function indirectly through the pointer. It behaves similarly to pointers to data, except that it points to code rather than data.

**Syntax**

Given a function ``int add(int a, int b);``, a pointer to this function would be declared as: ``int (*ptr)(int, int);``

Where:

- ``int``: the return type of the function that ``ptr`` can point to.
- ``(*ptr)``: the pointer variable itself. The parentheses are mandatory. They bind ``*`` to the name ``ptr``, signifying "``ptr`` is a pointer."
- ``(int, int)``: the parameter list of the function that ``ptr`` can point to.

.. admonition:: Important
   :class: warning

   If you write ``int *ptr(int, int)`` instead of ``int (*ptr)(int, int)``, you are declaring a function named ``ptr`` that takes two ``int``\s and returns an ``int*`` (a pointer to an integer). The parentheses make all the difference.

**Declaring and Initializing**

You initialize a function pointer by assigning it the name of a **compatible function**. The ``&`` (address-of) operator is optional, as the name of a function automatically *decays* to a pointer to that function.

.. code-block:: cpp

   // 1. A compatible function we want to point to
   int multiply(int a, int b) { return a * b; }
   // Another compatible function
   int add(int a, int b) { return a + b; }

   int main() {
       // 2. Declare a function pointer
       int (*func_ptr)(int, int);
       // 3. Initialize it (the & is optional)
       func_ptr = &multiply; // or func_ptr = multiply;
       // It's a variable, so it can be changed
       func_ptr = add;
   }

**Calling Through a Function Pointer**

Once you have a pointer, you can use it to call the function it points to. C and C++ provide two syntaxes:

- **Explicit Dereference (C-style):** ``(*func_ptr)(arg1, arg2)``
- **Implicit Dereference (C++ style):** ``func_ptr(arg1, arg2)``

We can call a function through a pointer because a function pointer is a **callable**.

.. code-block:: cpp

   int multiply(int a, int b) { return a * b; }

   int main() {
       int (*func_ptr)(int, int){&multiply};

       // Call using explicit dereference
       int result1{(*func_ptr)(5, 10)}; // result1 is 50
       std::cout << "Result 1: " << result1 << '\n';

       // Change what it points to
       func_ptr = &add; // or func_ptr = add;

       // Call using implicit dereference
       int result2{func_ptr(5, 10)}; // result2 is 15
       std::cout << "Result 2: " << result2 << '\n';
   }

**Use Cases**

Function pointers allow you to pass behavior as an argument.

- **State Machines**: An array of function pointers where each function implements the logic for a different state.
- **Plugin Systems**: A main application loads a dynamic library, finds a function by name, stores its address in a function pointer, and calls it.
- **Callbacks**: A function you pass to another function, which the receiving function "calls back" at an appropriate time.

.. code-block:: cpp

   // This function takes a callback: void (*operation)(int)
   void process_list(int* arr, int size, void (*operation)(int)) {
       for (int i{0}; i < size; ++i) {
           operation(arr[i]); // "Calling back" the operation
       }
   }

   void print_number(int n) { std::cout << "Value: " << n << '\n'; }
   void double_number(int n) { std::cout << "Double: " << n * 2 << '\n'; }

   int main() {
       constexpr size_t array_size{3};
       int my_list[array_size] = {1, 2, 3};
       std::cout << "--- Printing ---\n";
       process_list(my_list, array_size, print_number);

       std::cout << "--- Doubling ---\n";
       process_list(my_list, array_size, double_number);
   }

In C++, the name of a function **automatically decays** to a *function pointer* when passed as an argument -- just like an array name decays to a pointer to its first element.

**Dangers and Limitations**

- **Type mismatch risk** -- if the pointer's signature does not exactly match the function's, undefined behavior occurs.
- **No state retention** -- function pointers cannot capture variables or maintain context like lambdas or functors.
- **Null or invalid pointer calls** -- calling through an uninitialized or dangling pointer leads to crashes.
- **Poor readability and maintenance** -- the syntax is verbose and less intuitive for large systems.
- **Overload ambiguity** -- overloaded functions require explicit casting to resolve which overload to use.
- **No exception safety or lifetime management** -- no automatic handling of destroyed or unloaded code.
- **Incompatible with member functions** -- require special syntax and cannot be used directly with objects.
- **Obsolete for many tasks** -- modern alternatives like ``std::function``, lambdas, and ``std::invoke`` provide safer and more flexible mechanisms.


Functors
----------

A functor (or function object) is an object of a ``class`` or ``struct`` that overloads the function call operator (``operator()``). This allows you to create an object that can be called as if it were a regular function (callable), but with a key advantage: a functor can hold state.

**Why Not Just Use a Function?**

A regular C++ function does not typically maintain state between calls (unless you use ``static`` variables, which has different implications).

- A function takes inputs and produces an output. It is stateless.
- A functor is an object. It can have member variables (state) that persist across calls.

**A Simple Stateful Counter**

A "function" that counts how many times it has been called.

.. code-block:: cpp

   struct Counter {
       int count = 0; // 1. The State
       // 2. The Overloaded Call Operator
       // This is what makes it a functor.
       void operator()() {
           ++count;
           std::cout << "Called " << count << " times.\n";
       }
   };

   int main() {
       Counter my_counter; // Create an instance of our functor

       // Call the object as if it's a function
       my_counter(); // Output: Called 1 times.
       my_counter(); // Output: Called 2 times.

       // We can still access its state directly
       std::cout << "Final count: " << my_counter.count << '\n'; // Output: 2
   }

**STL Algorithms**

The most powerful and common use for functors is with C++ STL algorithms like ``std::transform``, ``std::for_each``, or ``std::count_if``. These algorithms often need a "predicate" or "operation" (a function to apply to each element in a container). A functor allows you to pass in an operation that is configurable.


Lambdas
---------

A lambda function (or lambda) is an anonymous, inline function defined right at the location where it is used.

- **Anonymous**: It does not have a name in the traditional sense.
- **Inline**: You define its body directly within another expression, such as a function call.

Think of it as a quick, throwaway function. You need a simple operation (like comparing two numbers or adding 1 to a value) for a single purpose, like sorting a vector. Instead of defining a whole separate function, you just write the operation right there.

.. admonition:: Under the Hood
   :class: note

   The compiler translates a lambda into a unique, unnamed functor (a ``struct`` or ``class`` with an overloaded ``operator()``). So, lambdas are mostly syntactic sugar for creating function objects, but they are incredibly convenient.

**Syntax**

.. code-block:: cpp

   [captures](parameters) mutable exception_spec -> return_type { body }

Don't be intimidated! We usually only use ``captures``, ``parameters``, and ``body``.

.. code-block:: cpp

   int main() {
       std::vector<int> numbers = {5, 2, 8, 3, 1};

       // Use a lambda for custom sorting
       std::sort(numbers.begin(), numbers.end(), [](int a, int b) {
           return a > b; // Sort in descending order
       });

       for (int n : numbers) {
           std::cout << n << " ";
       }
       // Output: 8 5 3 2 1
       std::cout << '\n';
   }

**Use Cases**

- **Algorithms**: As a comparator for ``std::sort``, ``std::stable_sort``, ``std::max_element``, etc.
- **Functional Programming**: With algorithms like ``std::transform`` (map), ``std::copy_if`` (filter), or ``std::accumulate`` (reduce).
- **Callbacks**: In asynchronous programming or GUI development, where you need to provide a function to be "called back" later.

**The Capture Clause [...]**

This is the most important part of a lambda. It defines how the lambda accesses variables from its surrounding scope.

- **No capture** ``[]``: The lambda cannot see or use any variables from the outside.
- **Capture by Value** ``[=]``: The lambda gets a copy of all outside variables it uses. These copies are ``const`` inside the lambda by default.
- **Capture by Reference** ``[&]``: The lambda gets a reference to all outside variables it uses. This is fast but can be dangerous.
- **Specific Capture (Value)** ``[x, y]``: Only captures ``x`` and ``y`` by value.
- **Specific Capture (Reference)** ``[&x, &y]``: Only captures ``x`` and ``y`` by reference.
- **Mixed Capture** ``[x, &y]``: Captures ``x`` by value and ``y`` by reference. You can mix ``[=]`` and ``[&]`` defaults with specific captures (e.g., ``[=, &y]`` captures ``y`` by reference and all other variables by value).

.. code-block:: cpp

   int x{10};
   int y{20};

   // Captures x by value (a copy) and y by reference (the original)
   auto my_lambda = [x, &y]() {
       // std::cout << "x = " << x << '\n'; // x is 10
       // x = 15; // ERROR! x is const (captured by value)
       y = 30; // OK! y is a reference
   };

   my_lambda();
   // std::cout << y << '\n'; // Output: 30

**The Parameter List**

The parameter list defines what arguments the lambda expects. It behaves exactly like a regular function's parameter list.

.. code-block:: cpp

   // No parameters
   [] { std::cout << "Hello!\n"; };

   // Single parameter
   [](int x) { std::cout << x << '\n'; };

   // Multiple parameters
   [](int a, int b) { return a + b; };

If your lambda takes no parameters, you may omit the parentheses ``()``.

**The Body**

The body defines the code executed when the lambda is invoked. It can contain a single expression or multiple statements enclosed in braces.

.. code-block:: cpp

   // Single-expression body
   [](int a, int b) { return a + b; };

   // Multi-statement body
   [](int x) {
       std::cout << "Value: " << x << '\n';
       return x * x;
   };

In C++11/C++14/C++17, lambdas must use ``return`` to produce a value explicitly.

**Return Type Deduction**

The compiler automatically deduces the lambda's return type from the return statements in its body (just like an ``auto`` function).

.. code-block:: cpp

   [](int x) { return x * 2.0; } // Return type is deduced as double

If the body is complex or you need to be explicit (e.g., returning an ``int`` from a ``double`` calculation), you can use the trailing return type syntax:

.. code-block:: cpp

   [](double d) -> int {
       if (d > 10.0) {
           return static_cast<int>(d);
       }
       return 0; // Multiple return statements might confuse the compiler
   };

**The mutable Keyword**

By default, variables captured by value are ``const``. You cannot modify your copy of them. The ``mutable`` keyword removes this restriction, allowing you to modify the copied data (which exists only inside the lambda).

.. code-block:: cpp

   int counter{0};

   auto my_counter = [counter]() mutable {
       counter++; // Modifies the lambda's internal copy
       return counter;
   };

   std::cout << my_counter() << '\n'; // Output: 1
   std::cout << my_counter() << '\n'; // Output: 2
   std::cout << counter << '\n';     // Output: 0 (original is unchanged)

The capture ``[counter]`` means capture by value. The lambda gets its own internal copy of ``counter``. Think of it as:

.. code-block:: cpp

   struct __Lambda {
       int counter;  // copy of outer counter
       int operator()() mutable {
           counter++;
           return counter;
       }
   };

**Functional Programming Patterns**

Lambdas are the key to using ``<algorithm>`` functions in a functional style.

- **Map** (``std::transform``): Applies an operation to every element in a range and stores the result.
- **Filter** (``std::copy_if`` or ``std::remove_copy_if``): Copies elements that match a predicate.


``std::function`` and Type Erasure
-------------------------------------

We have a problem: all callables have **different, unique types**.

- A function pointer is ``int(*)(int)``.
- A functor is ``MyFunctor``.
- A lambda has an **unnamable type** generated by the compiler.

How can we store these different things in a single variable or pass them to a function that accepts *any* of them?

**The Solution: std::function**

``std::function`` (header ``<functional>``) is a general-purpose, polymorphic function wrapper. It can store, copy, and invoke **any** callable object (function pointer, lambda, functor) as long as it has a compatible function signature.

This is a powerful concept called **Type Erasure**. ``std::function`` "erases" the specific type of the callable and stores it behind a common interface.

**Syntax**

It is a template that takes the function *signature* as its parameter.

.. code-block:: cpp

   // A std::function that can hold any callable
   // that takes an int and a double, and returns a std::string
   std::function<std::string(int, double)> my_callable;

**Storing Different Callables**

.. code-block:: cpp

   // 1. A free function
   int double_value(int a) { return a * 2; }
   // 2. A functor
   struct Multiplier {
       int factor;
       Multiplier(int f) : factor(f) {}
       int operator()(int x) const { return x * factor; }
   };

   int main() {
       // A std::function that needs an "int(int)" signature
       std::function<int(int)> operation;
       // 1. Store a lambda
       operation = [](int x) { return x + 10; };
       std::cout << operation(5) << '\n'; // Output: 15
       // 2. Store a functor
       Multiplier times_5(5);
       operation = times_5;
       std::cout << operation(5) << '\n'; // Output: 25
       // 3. Store a (compatible) free function
       operation = double_value;  // assign the function itself
       std::cout << operation(5) << '\n'; // Output: 10
   }

**Gotchas and Performance**

``std::function`` is powerful, but not "free."

- **Performance Cost**: Type erasure has overhead. A ``std::function`` call can be slower than a direct lambda or function pointer call because it may involve virtual dispatch.
- **Heap Allocation**: If the callable is "small" (like a simple lambda with no captures), it may be stored inside the ``std::function`` object itself (Small Object Optimization). If the callable is "large," ``std::function`` may allocate memory on the heap.
- **Empty State**: A default-constructed ``std::function`` is "empty." Calling it will throw a ``std::bad_function_call`` exception.

.. code-block:: cpp

   std::function<void()> empty_func;

   // empty_func(); // CRASH: throws std::bad_function_call

   // Always check before calling if it might be empty
   if (empty_func) {
       empty_func(); // Safe
   }


``std::variant`` (C++17)
====================================================

``std::variant`` is a **type-safe union** introduced in C++17. It can hold a value of one of several alternative types at any given time, but unlike a C-style ``union``, it always knows which type it currently holds and enforces safe access.

.. code-block:: cpp

   #include <variant>

Why std::variant?
-------------------

C-style unions are **unsafe**: they do not track which member is active, and reading the wrong member is undefined behavior. ``std::variant`` eliminates this problem by tracking the active type at runtime and providing checked access.

.. admonition:: Convention
   :class: tip

   Use ``std::variant`` instead of C-style unions whenever you need a variable that can hold one of several types.


Declaration and Assignment
----------------------------

A ``std::variant`` is declared with its possible types as template arguments. You can assign any of those types to it at any time.

.. code-block:: cpp

   #include <variant>
   #include <string>

   std::variant<int, double, std::string> data;
   data = 42;          // holds int
   data = 3.14;        // now holds double
   data = "hello";     // now holds std::string


Accessing Values
------------------

There are several ways to retrieve the stored value:

.. code-block:: cpp

   std::variant<int, double, std::string> data{42};

   // std::get<type> -- throws std::bad_variant_access if wrong type
   int val = std::get<int>(data);

   // std::get<index> -- access by index (0-based)
   int val2 = std::get<0>(data);  // same as std::get<int>

   // std::holds_alternative<type> -- check which type is active
   if (std::holds_alternative<int>(data)) {
       std::cout << "Holds an int: " << std::get<int>(data) << '\n';
   }


``std::visit`` for Pattern Matching
--------------------------------------

``std::visit`` applies a callable (typically a lambda) to the value currently held by the variant. This is the idiomatic way to handle all possible types.

.. code-block:: cpp

   std::variant<int, double, std::string> sensor_value{42};

   std::visit([](auto&& val) {
       std::cout << "Value: " << val << '\n';
   }, sensor_value);

The ``auto&&`` parameter lets the lambda accept any of the variant's types. The compiler generates a separate instantiation for each possible type.

Use Cases in Robotics
-----------------------

``std::variant`` is useful in robotics for:

- **Heterogeneous sensor data**: A single variable that can hold an ``int`` error code, a ``double`` measurement, or a ``std::string`` status message.
- **Command variants**: Different command types (move, rotate, stop) stored in a single variant.
- **Configuration values**: Parameters that can be ``int``, ``double``, or ``std::string``.

Example: Sensor Data Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. dropdown:: Full Example
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   .. code-block:: cpp

      #include <variant>
      #include <string>
      #include <iostream>

      using SensorData = std::variant<int, double, std::string>;

      void process_reading(const SensorData& data) {
          std::visit([](const auto& val) {
              std::cout << "Reading: " << val << '\n';
          }, data);
      }

      int main() {
          SensorData temperature{23.5};
          SensorData error_code{404};
          SensorData status{std::string{"active"}};

          process_reading(temperature);
          process_reading(error_code);
          process_reading(status);

          // Check type
          if (std::holds_alternative<double>(temperature)) {
              std::cout << "Temperature is a double: "
                        << std::get<double>(temperature) << '\n';
          }

          return 0;
      }


``if constexpr`` (C++17)
====================================================

``if constexpr`` is a compile-time conditional introduced in C++17. Unlike a regular ``if`` statement, the condition is evaluated **at compile time**, and the branch that is not taken is **discarded entirely** -- it does not even need to compile for the given type.

.. code-block:: cpp

   #include <type_traits>

This feature is especially powerful in templates, where different branches may only be valid for certain types.

.. code-block:: cpp

   template<typename T>
   void process(T value) {
       if constexpr (std::is_integral_v<T>) {
           std::cout << "Integer: " << value << '\n';
       } else if constexpr (std::is_floating_point_v<T>) {
           std::cout << "Float: " << value << '\n';
       } else {
           std::cout << "Other: " << value << '\n';
       }
   }

When ``process<int>`` is instantiated, only the first branch is compiled. The ``else`` branches are completely discarded. This differs from a regular ``if``, where all branches must be valid C++ for the instantiated type.

.. admonition:: Key Point
   :class: note

   ``if constexpr`` requires ``<type_traits>`` for type-checking utilities like ``std::is_integral_v``, ``std::is_floating_point_v``, ``std::is_same_v``, etc. The discarded branches do not need to be valid for the given template parameter -- they are removed before semantic analysis.
