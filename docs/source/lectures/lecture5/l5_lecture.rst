====================================================
Lecture
====================================================


Part I -- The Core Mechanics
-----------------------------

Introduction to Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^

A function is a named group of statements that can be executed as a unit. Functions are one of the most important concepts in C++ and form the foundation of modular programming.

.. seealso::

   `C++ Core Guidelines: F (Functions) <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-functions>`_

Code Reusability
""""""""""""""""

Functions eliminate the need to copy and paste code blocks (**DRY = Don't Repeat Yourself**). Create a function once and call it multiple times throughout your program.

.. code-block:: cpp

   constexpr unsigned int calculate_area(unsigned int length, unsigned int width) {
       return length * width;
   }

   int main() {
       // Use it anywhere:
       unsigned int room1_area{calculate_area(10, 12)};
       unsigned int room2_area{calculate_area(8, 15)};

       std::cout << "Room 1 Area: " << room1_area << '\n';
       std::cout << "Room 2 Area: " << room2_area << '\n';
   }

The DRY Principle: Don't Repeat Yourself
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The DRY principle states that every piece of logic should have a single, unambiguous representation within a system. In short: **avoid duplicating code**.

.. grid:: 2

   .. grid-item-card:: WET Code (Write Everything Twice)

      .. code-block:: cpp

         // --- In your shopping cart ---
         double price{100.0};
         double discount{price * 0.10}; // 10% discount
         double final_price1{price - discount};

         // --- In the checkout page ---
         double order_total{100.0};
         double final_discount{order_total * 0.10};
         double final_price2{order_total - final_discount};

      The discount logic is repeated. If you need to change the discount to 15%, you have to find and update it in **every location**, which is error-prone.

   .. grid-item-card:: DRY Code (Using a Function)

      .. code-block:: cpp

         double calculate_final_price(double price) {
             double discount{price * 0.10};
             return price - discount;
         }

         // --- In your shopping cart ---
         double final_price1{calculate_final_price(100.0)};

         // --- In the checkout page ---
         double final_price2{calculate_final_price(100.0)};

      The logic exists in **one place**. To change the discount, you only need to edit the function, guaranteeing consistency everywhere it's used.

Modularity and Organization
"""""""""""""""""""""""""""""

Functions help organize code logically, making it easier to understand and maintain large projects.

.. code-block:: cpp

   // Each function has a specific purpose
   void get_user_input();
   void process_data();
   void display_results();

   int main() {
       get_user_input();
       process_data();
       display_results();
   }

.. seealso::

   - `F.2: A function should perform a single logical operation <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#f2-a-function-should-perform-a-single-logical-operation>`_
   - `F.3: Keep functions short and simple <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#f3-keep-functions-short-and-simple>`_

Easier Debugging and Testing
""""""""""""""""""""""""""""""

When code is organized in functions, you can test and debug individual components separately, making bug fixing much more efficient.

.. code-block:: cpp

   // Test individual functions
   bool is_valid_email(std::string email) {
       // Validation logic here
       return email.find("@") != std::string::npos;
   }

   // Easy to test:
   is_valid_email("test@email.com");

Abstraction of Complex Operations
"""""""""""""""""""""""""""""""""""

Functions allow you to use complex operations without worrying about implementation details.

.. code-block:: cpp

   // Complex math hidden behind simple function
   double calculate_interest(double principal, double rate, int years) {
       // Complex formula abstracted away
       return principal * pow(1 + rate, years);
   }


The Function Lifecycle
^^^^^^^^^^^^^^^^^^^^^^

Function Declaration
""""""""""""""""""""

A function declaration (or prototype) consists of the **return type** + **identifier** + **parameters** (types and names). The body of the function is not part of the declaration.

.. code-block:: cpp

   type identifier(<parameters>); // e.g., int add_numbers(int a, int b);

- ``type`` -- What kind of value the function is expected to return to the calling function (the caller) or main program. When a function does not return anything, its type should be ``void``.
- ``identifier`` -- The name given to a function.

  .. note::

     - We use the same naming convention as for variables (``snake_case``).
     - A function does an action, therefore, the identifier should include a verb.

- ``<parameters>`` -- If the function takes parameters, the parameters are listed in the parentheses. Each parameter has the form ``type identifier``. If the function does not use any parameter, the parentheses are left empty.

.. seealso::

   - `NL.25: Don't use void as an argument type <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rl-void>`_
   - `F.1: "Package" meaningful operations as carefully named functions <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#f1-package-meaningful-operations-as-carefully-named-functions>`_

**The "Promise"**

- The function declaration provides a *promise* that the function will be implemented (defined) elsewhere in the code, either later in the same source file or in a different source file.
- *A function declaration allows you to use (call) that function before its actual definition in the code*. This is particularly useful in scenarios where multiple functions call each other.
- During compilation, the *linker* will look for the actual definition of the function.

Function Definition
""""""""""""""""""""

A function definition (often referred to as a function **implementation**) consists of the **declaration** + **body**.

.. code-block:: cpp

   type identifier(<parameters>) {
       // body of the function
   }

.. code-block:: cpp

   // declaration
   int add_numbers(int a, int b);

   // definition
   int add_numbers(int a, int b) {
       return a + b;
   }

   int main() {
       std::cout << add_numbers(3, 5) << '\n';
   }

Header Files and Source Files
""""""""""""""""""""""""""""""

Think of your code like a book:

- **Header File (.hpp)**: The **Table of Contents**. It tells you *what* functions are available (declarations) but not how they work. It is a public-facing menu or interface.
- **Source File (.cpp)**: The **Chapters**. It contains the actual story and details (definitions) of how each function works. This is the private implementation.

Separating code this way gives us three huge wins:

1. Faster Compilation
2. Code Reusability
3. Better Organization

Benefit 1: Faster Compilation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You only recompile what actually changes.

.. grid:: 2

   .. grid-item-card:: Without Headers

      .. code-block:: cpp

         // big_file.cpp - 10,000 lines
         void funcA() { /* ... */ }
         void funcB() { /* ... */ }
         int main()  { /* ... */ }

      Change one line in ``funcA()`` -- the **entire 10,000-line file** must be recompiled.

   .. grid-item-card:: With Headers

      .. code-block:: cpp

         // funcs.hpp
         void funcA();
         void funcB();

         // main.cpp
         #include "funcs.hpp"
         int main() { /* ... */ }

         // funcs.cpp
         #include "funcs.hpp"
         void funcA() { /* ... */ }

      Change ``funcA()`` -- only ``funcs.cpp`` recompiles. Fast!

Benefit 2: Code Reusability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Declare once, use everywhere. Headers are the single source of truth.

.. grid:: 2

   .. grid-item-card:: Without Headers

      .. code-block:: cpp

         // file1.cpp
         int add(int a, int b); // Declaration
         // ...
         // file2.cpp
         int add(int a, int b); // Repeated!
         // ...
         // file3.cpp
         int add(int a, int b); // Repeated again!

      Changing the function signature requires finding and updating it in **every single file**.

   .. grid-item-card:: With Headers

      .. code-block:: cpp

         // math.hpp
         #pragma once
         int add(int a, int b); // Declared ONCE

         // file1.cpp
         #include "math.hpp"

         // file2.cpp
         #include "math.hpp"

      Change the declaration in **one place**, and every file that uses it gets the update automatically.

Benefit 3: Better Organization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Headers group related functionality into logical modules.

.. grid:: 2

   .. grid-item-card:: Without Headers

      .. code-block:: cpp

         // mess.cpp - 5000 lines
         // --- Customer Logic ---
         struct Customer { /*...*/ };
         void save_customer() { /*...*/ }
         // --- Pricing Logic ---
         struct Product { /*...*/ };
         void calculate_price() { /*...*/ }
         // --- Utility Logic ---
         void send_email() { /*...*/ }

      Finding code is difficult, different logic is tangled together, and it is impossible for a team to work on the code without conflicts.

   .. grid-item-card:: With Headers

      .. code-block:: cpp

         // customer.hpp
         struct Customer;
         void save_customer();

         // pricing.hpp
         struct Product;
         void calculate_price();

         // main.cpp
         #include "customer.hpp"
         #include "pricing.hpp"

      The project is clean and self-documenting. Need to work on pricing? Open ``pricing.hpp`` and ``pricing.cpp``. Simple, modular, and scalable.

Include Guards
~~~~~~~~~~~~~~~

What if a file includes your header twice by accident? You will get "redefinition" errors. We solve this with **include guards**.

.. grid:: 2

   .. grid-item-card:: Old Way

      .. code-block:: cpp

         #ifndef MY_HEADER_HPP
         #define MY_HEADER_HPP

         // All your declarations go here...
         int add(int a, int b);

         #endif // MY_HEADER_HPP

   .. grid-item-card:: Modern Way

      .. code-block:: cpp

         #pragma once

         // All your declarations go here...
         int add(int a, int b);

      This is simpler, less error-prone, and supported by *most* modern compilers.

.. seealso::

   `Include Guards: #pragma once vs Header Guards <https://thamara.dev/posts/pragma-once-vs-header-guards/>`_

.. admonition:: To-Do
   :class: tip

   1. Move all function declarations to ``week5.hpp``
   2. Add include guards in ``week5.hpp``
   3. Move all function definitions to ``week5.cpp``
   4. Include ``week5.hpp`` at the top of your ``week5.cpp`` file
   5. Include ``week5.hpp`` at the top of your ``main.cpp`` file
   6. Update ``CMakeLists.txt`` to generate the executable from ``main.cpp`` and ``week5.cpp``
   7. Update ``CMakeLists.txt`` to tell the build system where to find your headers using ``target_include_directories(<target> <INTERFACE|PUBLIC|PRIVATE> [items...])``
   8. Build and run your program to confirm that it still works correctly

.. admonition:: Best Practice
   :class: important

   ``main.cpp`` should contain only one function: The ``main`` function!

.. warning::

   - ``.cpp`` files are compiled but not included.
   - ``.hpp`` files are included but not compiled.


Function Call
""""""""""""""

When a function is called, the execution of the program jumps to the function definition, runs the code inside the function, and then returns back to the point from where the function was called, continuing from the next statement.

**Why Defining Functions Is Not Enough**

The compiler reads your code from top to bottom. This can lead to two common problems if you are not careful.

.. grid:: 2

   .. grid-item-card:: Problem 1: Order of Definition
      :class-card: sd-border-danger

      .. code-block:: cpp

         void print_hello() {
             print_world(); // ERROR!
             // Compiler has not seen
             // print_world() yet.
         }
         void print_world() { /* ... */ }

         int main() { print_hello(); }

   .. grid-item-card:: Problem 2: Cyclic Dependency
      :class-card: sd-border-danger

      .. code-block:: cpp

         void prompt_user() {
             // ...
             print_number(num); // ERROR!
         }
         void print_number(int n) {
             if (n <= 0)
                 prompt_user(); // ERROR!
         }
         int main() { prompt_user(); }

**The Solution: Function Declarations**

Function declarations solve both of these problems.

.. grid:: 2

   .. grid-item-card:: Solution 1: Order Fixed
      :class-card: sd-border-success

      .. code-block:: cpp

         // "Promise" to the compiler
         void print_world();

         void print_hello() {
             print_world(); // OK!
         }
         void print_world() { /* ... */ }

         int main() { print_hello(); }

   .. grid-item-card:: Solution 2: Cycle Broken
      :class-card: sd-border-success

      .. code-block:: cpp

         // Make promises for both
         void print_number(int n);
         void prompt_user();

         void prompt_user() {
             print_number(0); // OK!
         }
         void print_number(int n) {
             prompt_user(); // OK!
         }
         int main() { prompt_user(); }

**Tracing the Flow of Control**

With declarations in place, the program executes by jumping between functions and always returning to where it was called.

.. code-block:: cpp

   // Declarations
   void print_world();
   void print_hello();

   void print_world() {
       std::cout << "world\n";
   }

   void print_hello() {
       std::cout << "hello, ";
       print_world();
   }

   int main() {
       print_hello();
       std::cout << "exit main\n";
   }

1. Execution starts in ``main()``.
2. ``main()`` calls ``print_hello()``.
3. Control jumps to ``print_hello()``.
4. ``hello,`` is printed.
5. ``print_hello()`` calls ``print_world()``.
6. Control jumps to ``print_world()``, prints ``world``, and returns.
7. Control returns to ``main()``, prints ``exit main``, and the program ends.

.. admonition:: Best Practice
   :class: important

   **The Golden Rule of Function Ordering**: Always provide function declarations (prototypes) for all non-trivial functions, typically in header (``.hpp``) files. This completely solves ordering and cyclic dependency issues. It allows you to organize your code based on logic, not compiler limitations.

The ``return`` Keyword
""""""""""""""""""""""

**Returning from void Functions**

In a ``void`` function, ``return;`` is used to **exit the function early**. No value can be returned. It is optional at the end of a ``void`` function, as it will return automatically when it reaches the closing brace.

.. code-block:: cpp

   void print_number(int number) {
       if (number < 0) {
           std::cout << "Error: Negative numbers not allowed.\n";
           return; // Exit the function immediately
       }
       std::cout << "The number is: " << number << "\n";
   }

   int main() {
       print_number(10);  // Prints "The number is: 10"
       print_number(-5);  // Prints error and returns
   }

**Returning Values from Functions**

For non-``void`` functions, the ``return`` statement sends a value back to the function's caller. The type of the value you return **must match** or be convertible to the function's declared return type.

.. code-block:: cpp

   int calculate_sum(int a, int b) {
       int result{a + b};
       return result; // Send the value of 'result' back
   }

   int main() {
       // The returned value is used
       // to initialize the 'sum' variable.
       int sum{calculate_sum(5, 3)};
       std::cout << sum << '\n'; // 8
   }

How it works:

1. ``main()`` calls ``calculate_sum(5, 3)``.
2. ``calculate_sum`` runs and computes ``result`` (8).
3. ``return result;`` makes a copy of ``result``'s value.
4. Control jumps back to ``main()``.
5. The returned copy of the value (8) is used to initialize ``sum``.

.. warning::

   **The Golden Rule of Returning Values**: Every possible execution path in a non-``void`` function **must** end with a ``return`` statement.

   .. code-block:: cpp

      // DANGEROUS: What if number is 0?
      int get_sign(int number) {
          if (number > 0) {
              return 1;
          } else if (number < 0) {
              return -1;
          }
          // No return here! If number is 0, this causes UNDEFINED BEHAVIOR.
      }

**Implicit Return Type Conversion**

If you return a value of a different type, the compiler will try to **implicitly convert** it. This can sometimes lead to a loss of data.

.. code-block:: cpp

   int truncate_double() {
       double value{99.99};
       return value; // The double 99.99 is converted to the int 99
   }

   int main() {
       int truncated{truncate_double()};
       std::cout << truncated << '\n'; // Prints 99
   }

.. admonition:: Best Practice
   :class: important

   Be explicit to avoid surprises. Prefer ``return static_cast<int>(value);`` to show you intended the conversion.

**Returning Multiple Values (Modern C++)**

You cannot use ``return`` twice, but you can return a single object that contains multiple values, like a ``std::pair``, a ``std::tuple``, or a ``struct``. Since C++17, **structured bindings** make this incredibly clean and easy to use.

.. seealso::

   `F.21: To return multiple "out" values, prefer returning a struct <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#f21-to-return-multiple-out-values-prefer-returning-a-struct>`_

Using ``std::pair``:

.. code-block:: cpp

   #include <utility> // For std::pair

   // This function returns both a bool and a string
   std::pair<bool, std::string> get_user_data() {
       // ... logic to get data ...
       bool success{true};
       std::string name{"Zayd"};
       return {success, name};
   }

   int main() {
       // The returned pair is automatically unpacked
       // into two new variables: 'success' and 'user_name'.
       auto [success, user_name] = get_user_data();

       if (success) {
           std::cout << "Welcome, " << user_name << "!\n";
       }
   }

Using ``std::tuple``:

.. code-block:: cpp

   #include <iostream>
   #include <string>
   #include <tuple> // Required for std::tuple

   // This function returns three values: status code, success flag, and content.
   std::tuple<int, bool, std::string> parse_http_response() {
       // ... imagine parsing a network response ...
       int status_code{200};
       bool is_success{true};
       std::string response_body{"{\"user\":\"Zayd\"}"};

       return {status_code, is_success, response_body};
   }

   int main() {
       // Structured bindings work perfectly with std::tuple,
       // unpacking the elements in the order they are defined.
       auto [code, success, body] = parse_http_response();

       if (success) {
           std::cout << "Response OK (Code " << code << "): " << body << '\n';
       }
   }

Using a ``struct``:

.. code-block:: cpp

   #include <iostream>
   #include <string>

   // Define a struct to hold the related data
   struct UserQueryResult {
       bool found;
       std::string user_name;
   };

   // The function now returns our custom struct
   UserQueryResult find_user() {
       // ... logic to find a user in a database ...
       return {true, "Zayd"}; // C++ aggregate initialization
   }

   int main() {
       // Structured bindings work seamlessly with structs.
       // The members are unpacked in the order they are defined.
       auto [user_found, name] = find_user();

       if (user_found) {
           std::cout << "User found: " << name << "!\n";
       }
   }

**Return Type Deduction with auto**

Since C++14, you can use the ``auto`` keyword as a function's return type. This instructs the compiler to automatically deduce the return type from the expression in the ``return`` statement.

.. code-block:: cpp

   // The compiler looks at `a + b` and sees that int + double = double.
   // It deduces that the return type of this function must be `double`.
   auto add(int a, double b) {
       return a + b;
   }

   int main() {
       // 'result' will correctly be of type 'double'.
       auto result{add(5, 3.14)};
   }

.. admonition:: Best Practice
   :class: important

   Prefer explicit return types for clarity. While powerful, ``auto`` can make code harder to read because the function's signature no longer states what it returns. Use it sparingly, mainly in generic programming (templates) where the return type can be complex.


The Function Interface
^^^^^^^^^^^^^^^^^^^^^^

A function's interface is its public-facing contract, defining how data flows into it (through parameters) and out of it (through return values).

Parameters vs. Arguments
""""""""""""""""""""""""""

**Parameter**: A placeholder in the function's definition. It defines what **type** of data the function expects.

.. code-block:: cpp

   void make_coffee(std::string cup_size, bool is_hot);

**Argument**: The actual value or variable you provide when you **call** the function.

.. code-block:: cpp

   int main() {
       make_coffee("large", true);
   }

Passing Arguments
""""""""""""""""""

When you pass data to a function, does it receive the **original item** or a **copy**? This is a crucial question in C++. The method you choose affects performance and whether the original data can be modified.

- Pass-by-value (a safe copy)
- Pass-by-reference (the modifiable original)
- Pass-by-const-reference (a safe, efficient view)
- Pass-by-pointer (an optional, modifiable original)

Pass-by-Value: Give a Copy
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the default method. The function receives a **brand new copy** of the argument.

.. warning::

   Changes made to the copy inside the function do not affect the original.

.. code-block:: cpp

   void add_ten(int x) {
       // int x{a};
       x += 10; // Modifies the copy
   }

   int main() {
       int a{5};
       add_ten(a); // A copy of 'a' is sent
       std::cout << a << '\n'; // 'a' is still 5
   }

.. figure:: /_static/images/l5/pass-by-value2.jpg
   :alt: Pass-by-value diagram
   :align: center
   :width: 50%

   Pass-by-value: the function works on a copy of the original.

.. admonition:: Best Practice
   :class: important

   **Use for:** Small data that is cheap to copy (like ``int``, ``double``, ``bool``).

Pass-by-Reference: Give the Original
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The function receives a direct link (an alias) to the original argument. No copy is made.

.. warning::

   Changes made to the parameter inside the function WILL affect the original.

.. code-block:: cpp

   void add_ten(int& x) {
       // int &x{a}
       x += 10; // Modifies the original 'a'
   }

   int main() {
       int a{5};
       add_ten(a); // 'a' itself is shared
       std::cout << a << '\n';  // 'a' is now 15
   }

.. figure:: /_static/images/l5/pass-by-reference2.jpg
   :alt: Pass-by-reference diagram
   :align: center
   :width: 50%

   Pass-by-reference: the function operates on the original variable.

.. admonition:: Best Practice
   :class: important

   **Use when:** You **want to modify** the original argument.

Pass-by-const-Reference: Read-Only Access
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method shares the original data (efficient, no copy) but makes it read-only (``const``), so the function is forbidden from changing it (safe).

.. code-block:: cpp

   void print_vector(const std::vector<int>& v) {
       // We get the efficiency of pass-by-reference without the risk.
       for (const int& item : v) {
           std::cout << item << " ";
       }
       // v.push_back(100); // COMPILER ERROR: v is const!
   }

   int main() {
       std::vector<int> num_vect{1, 2, 3};
       print_vector(num_vect); // No expensive copy is made.
   }

.. admonition:: Best Practice
   :class: important

   **This should be your default choice** for passing large, read-only objects like vectors or strings.

Pass-by-Pointer: Give an Address
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The function receives the memory address of the original argument. This allows modification (like a reference) but with a key difference: a pointer can be ``nullptr``.

.. code-block:: cpp

   void add_ten(int* p) {
       if (p != nullptr) {
           *p += 10; // Modifies original 'a'
       }
   }

   int main() {
       int a{5};
       add_ten(&a); // Pass the address of 'a'
       // 'a' is now 15
       std::cout << a << '\n';
   }

.. figure:: /_static/images/l5/pass-by-pointer2.jpg
   :alt: Pass-by-pointer diagram
   :align: center
   :width: 50%

   Pass-by-pointer: the function receives a memory address.

.. admonition:: Best Practice
   :class: important

   **Use when:** You want to modify the argument, AND the argument could be optional (``nullptr``). In modern C++, prefer references when possible.

How to Choose a Passing Method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l5/functionchart.pdf
   :alt: Flowchart for choosing a passing method
   :align: center
   :width: 80%

   Decision flowchart for choosing a parameter-passing method.

.. seealso::

   - `F.15: Prefer simple and conventional ways of passing information <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#f15-prefer-simple-and-conventional-ways-of-passing-information>`_
   - `F.16: For "in" parameters, pass cheaply-copied types by value and others by reference to const <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#f16-for-in-parameters-pass-cheaply-copied-types-by-value-and-others-by-reference-to-const>`_
   - `F.17: For "in-out" parameters, pass by reference to non-const <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#f17-for-in-out-parameters-pass-by-reference-to-non-const>`_

Returning Data from Functions
""""""""""""""""""""""""""""""

When a function gives a result, is the caller receiving a **brand-new object** or a **link to an existing one**? The return method impacts efficiency and can introduce critical bugs if used incorrectly.

- Return-by-Value (a new copy)
- Return-by-Reference (a link to an existing object)
- Return-by-Pointer (an address of an existing object)

Return-by-Value
~~~~~~~~~~~~~~~~

This is the most common way to return data. The function produces a result, and a **temporary copy** of that result is given back to the caller.

.. code-block:: cpp

   int add_numbers(int a, int b) {
       return a + b;
   }

   int main() {
       auto result{add_numbers(3, 4)};
   }

- The ``return`` statement's job is to get the value back to the caller (``main``). For an ``int``, the compiled code places the value 7 into a specific CPU register that, by convention, is designated for function return values (e.g., the **EAX** or **RAX** register on x86 processors).
- The function's memory (its stack frame) is cleaned up, and control returns to ``main``.
- The ``main`` function knows to look in that specific CPU register for the return value. It reads the value 7 from the register and uses it to initialize the new variable ``result``.

**But isn't copying slow?**

.. code-block:: cpp

   std::vector<int> create_large_vector() {
       std::vector<int> local_vec = { /* ... 1 million integers ... */ };
       return local_vec; // Oh no, are we copying 1 million ints?
   }

   int main() {
       std::vector<int> my_vec{create_large_vector()};
   }

In the past, this was a performance concern. But not anymore thanks to **copy elision**.

Copy Elision
~~~~~~~~~~~~~~

Copy elision is a compiler optimization that eliminates unnecessary copying or moving of objects. Instead of creating a temporary object and then transferring it to its final destination, the compiler constructs the object **directly where it is needed**.

.. grid:: 2

   .. grid-item-card:: Without Copy Elision

      1. Function creates a temporary object.
      2. The temporary is copied or moved.
      3. The temporary is destroyed.

   .. grid-item-card:: With Copy Elision

      1. Function constructs the object directly at the destination.
      2. Done.

**The Compiler's Strategy for Return Values**

A modern C++ compiler follows a hierarchy of strategies when a function returns an object, always choosing the most efficient option available:

1. **Copy Elision (RVO/NRVO):** The best-case scenario. The compiler avoids creating a temporary object altogether. This is a true "zero-cost abstraction".
2. **Implicit Move:** If elision is not possible, the compiler attempts to **move** the local object. This is highly efficient for objects that manage resources (e.g., ``std::vector``, ``std::unique_ptr``).
3. **Copy Construction:** The fallback option. If the object cannot be moved, it will be **copied**. This can be expensive for large objects.
4. **Compilation Error:** If an object is neither movable nor copyable, and copy elision cannot be performed, the code will fail to compile.

**Return Value Optimization (RVO)**

RVO is a form of copy elision that applies when a function returns a temporary, unnamed object (a **prvalue**). The compiler constructs this object directly in the memory of the variable that will receive it.

Since C++17, RVO for temporary return values is **guaranteed** by the language standard. You can rely on it.

.. code-block:: cpp

   std::string create_greeting() {
       // This temporary is a prvalue.
       // RVO is guaranteed here.
       return std::string("Hello");
   }

   int main() {
       // No temporary is created; "Hello"
       // is constructed directly inside `msg`.
       std::string msg{create_greeting()};
   }

- **How it works:** The compiler passes a hidden pointer to ``create_greeting``, telling it where ``msg``'s memory is. The ``std::string`` is then constructed at that location.
- **Key Benefit:** This process is so effective that it works even for objects that are non-copyable and non-movable.

.. admonition:: Definition
   :class: note

   A **prvalue**, or "pure rvalue", is a type of expression in C++ that represents a **temporary**, **unnamed object** or a value that is not associated with a specific memory location. Think of it as a transient value that exists only for the duration of a single expression.

   - **Literals**: ``42``, ``true``, ``"hello"``
   - The result of a function call that returns by value.
   - The result of an arithmetic operation: ``x + y``

**Named Return Value Optimization (NRVO)**

NRVO is a variation of RVO that applies when a function returns a **named local variable**. If certain conditions are met, the compiler can still elide the copy by constructing this named object in the caller's destination.

Unlike RVO, NRVO is **not guaranteed** by the C++ standard. It is a common but optional optimization that depends on the compiler and the function's complexity.

.. code-block:: cpp

   std::vector<int> generate_data() {
       std::vector<int> local_data;
       local_data.reserve(100);
       // ... operations on local_data ...
       for (int i{0}; i < 100; ++i) {
           local_data.push_back(i);
       }
       // Returning a named object.
       return local_data;
   }

   int main() {
       // NRVO may construct local_data
       // directly inside `my_data`.
       auto my_data{generate_data()};
   }

- **With NRVO:** The ``local_data`` vector is constructed directly in ``my_data``'s memory.
- **Without NRVO:** ``local_data`` is constructed, and then its contents are **moved** into ``my_data`` upon return.

**When Can NRVO Fail?**

.. grid:: 2

   .. grid-item-card:: Multiple Potential Return Objects

      .. code-block:: cpp

         std::string get_path(bool is_windows) {
             std::string win_path{"C:\\"};
             std::string nix_path{"/"};

             // Compiler can't know which
             // object to construct at the
             // destination. NRVO fails.
             // (A move will be used instead.)
             return is_windows ? win_path : nix_path;
         }

   .. grid-item-card:: Assignment vs. Initialization

      .. code-block:: cpp

         std::string create_greeting() {
             return "hello";
         }

         int main() {
             std::string msg; // Constructed here

             // Elision is impossible: msg
             // already exists. A move-assignment
             // will be used instead.
             msg = create_greeting();
         }

.. admonition:: Best Practice
   :class: important

   To enable copy elision, prefer initializing objects directly from function calls: ``auto result{my_func()};``

Return-by-Reference
~~~~~~~~~~~~~~~~~~~~

Return-by-reference allows a function to return a direct link to an **existing object**. This is useful for allowing chained function calls or modifying objects.

.. code-block:: cpp

   // This function returns a reference to an element in the vector
   int& get_element(std::vector<int>& vec, size_t index) {
       return vec.at(index);
   }

   int main() {
       std::vector<int> my_vec = {10, 20, 30};
       // get_element returns a reference to my_vec[1], not a copy of 20.
       get_element(my_vec, 1) = 99; // We are modifying the original vector directly!
       // my_vec is now {10, 99, 30}
   }

.. danger::

   **CRITICAL DANGER: Dangling References**

   NEVER return a reference to a local variable.

   .. code-block:: cpp

      int& get_value() {
          int local_value{10};
          return local_value; // DANGEROUS!
      } // 'local_value' is destroyed here.

      int main() {
          int& ref{get_value()};
          // 'ref' is now a "dangling reference". It refers to memory
          // that has been freed.
          std::cout << ref << '\n'; // UNDEFINED BEHAVIOR.
      }

.. seealso::

   `F.43: Never (directly or indirectly) return a pointer or a reference to a local object <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#f43-never-directly-or-indirectly-return-a-pointer-or-a-reference-to-a-local-object>`_

Return-by-Pointer
~~~~~~~~~~~~~~~~~~~

Return-by-pointer allows a function to return the memory address of an **existing object**. A key feature is the ability to return ``nullptr`` to indicate failure or that nothing was found.

.. code-block:: cpp

   // This function returns a pointer to the first element found, or nullptr.
   int* find_value(std::vector<int>& vec, int value) {
       for (int& element : vec) {
           if (element == value) {
               return &element; // Return the address of the element
           }
       }
       return nullptr; // Return nullptr if nothing was found
   }

   int main() {
       std::vector<int> my_vec = {10, 20, 30};
       int* ptr{find_value(my_vec, 20)};

       // ALWAYS check a returned pointer before using it!
       if (ptr != nullptr) {
           *ptr = 99; // Modify the original vector via the pointer
       }
       // my_vec is now {10, 99, 30}
   }

.. danger::

   **CRITICAL DANGER: Dangling Pointers**

   NEVER return a pointer to a local variable.

   .. code-block:: cpp

      int* get_value() {
          int local_value{10};
          return &local_value; // DANGEROUS!
      } // 'local_value' is destroyed here.

      int main() {
          int* ptr{get_value()};
          // 'ptr' is now a "dangling pointer". It points to memory
          // that has been freed.
          std::cout << *ptr << '\n'; // UNDEFINED BEHAVIOR.
      }

.. seealso::

   - `F.43: Never (directly or indirectly) return a pointer or a reference to a local object <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#f43-never-directly-or-indirectly-return-a-pointer-or-a-reference-to-a-local-object>`_
   - `F.60: Prefer T* over T& when "no argument" is a valid option <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#f60-prefer-t-over-t-when-no-argument-is-a-valid-option>`_


Part II -- Enhancing Functions
-------------------------------

.. seealso::

   `F.56: Avoid unnecessary condition nesting <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#f56-avoid-unnecessary-condition-nesting>`_

Static Variables in Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A ``static`` local variable is initialized **only once** and keeps its value between function calls. Think of it like a sticky note on the function's desk that it can read and update each time it is called.

.. grid:: 2

   .. grid-item-card:: Without ``static``

      .. code-block:: cpp

         void counter() {
             int count{0}; // Re-created every time
             count++;
             // Always prints 1
             std::cout << count << '\n';
         }

         int main() {
             counter(); // count is 1
             counter(); // count is 1
         }

   .. grid-item-card:: With ``static``

      .. code-block:: cpp

         void static_counter() {
             static int count{0}; // Created ONCE
             count++;
             // Prints 1, then 2
             std::cout << count << '\n';
         }

         int main() {
             static_counter(); // count becomes 1
             static_counter(); // count becomes 2
         }

Key Properties of Static Variables
""""""""""""""""""""""""""""""""""""

- **Single Initialization**: A ``static`` variable is initialized only the **first time** the code flows over its declaration. On all subsequent calls, the declaration is skipped.
- **Lifetime**: It exists for the **entire lifetime** of the program. It is created on the first call and destroyed only when the program terminates.
- **Scope**: It is still a **local variable**. Its visibility (scope) is limited to the function in which it is defined. You cannot access it from outside the function.
- **Storage**: It is stored in a separate memory area (the static or global data segment), not on the call stack like regular local variables.
- **Use Cases**: Perfect for things like function call counters, caching results of expensive calculations, or ensuring a resource is initialized only once.

Function Overloading
^^^^^^^^^^^^^^^^^^^^^

Function overloading lets you define multiple functions with the **same name**, as long as they have **different parameter lists**.

.. note::

   The compiler chooses the correct function at compile-time based on the **arguments** you provide.

.. code-block:: cpp

   // Three different functions, all named 'print'
   void print(const std::string& text) { /* ... */ } // Signature: print(string)
   void print(int number)               { /* ... */ } // Signature: print(int)
   void print(double value, int precision) { /* ... */ } // Signature: print(double, int)

   int main() {
       print("hello");     // Calls the string version
       print(42);          // Calls the int version
       print(3.14159, 2);  // Calls the double, int version
   }

What Makes a Function Unique?
"""""""""""""""""""""""""""""""

A function's signature is defined by its **name** and its sequence of **parameter types**. The parameter names and the return type are **NOT** part of the signature for overloading purposes.

.. grid:: 2

   .. grid-item-card:: VALID Overloads

      .. code-block:: cpp

         // Different number of parameters
         void func(int a);
         void func(int a, int b);

         // Different types of parameters
         void func(double a);

         // Different order of parameters
         void func(int a, double b);
         void func(double a, int b);

   .. grid-item-card:: INVALID Overload

      .. code-block:: cpp

         // The compiler can't distinguish
         // these based on return type alone.

         int get_value() {
             return 42;
         }

         double get_value() { // ERROR!
             return 3.14;
         }

Overload Resolution
""""""""""""""""""""

When you call an overloaded function, the compiler follows a strict hierarchy to find the best match. This process is called **overload resolution**.

1. **Exact Match**: The compiler first looks for a function where the argument types match the parameter types perfectly. (e.g., calling with an ``int`` finds a function expecting an ``int``).
2. **Match with Promotion**: If no exact match is found, the compiler tries to achieve a match by **promoting** the arguments. These are safe, non-narrowing conversions.

   - ``bool`` -> ``int``
   - ``char`` -> ``int``
   - ``float`` -> ``double``

3. **Match with Standard Conversion**: If promotion does not work, the compiler tries other built-in conversions, even if they might lose information (narrowing).

   - ``int`` -> ``float``
   - ``double`` -> ``int``

4. **Ambiguous or No Match**: If the compiler finds multiple equally good matches (ambiguous) or no match at all, it will issue a compilation error.

**Exercise: Predict the result.**

.. code-block:: cpp

   int add(int a, int b) { return a + b; }
   int add(int a, float b) { return a + b; }
   int add(int a, double b) { return a + b; }

   int main() {
       std::cout << add(2, 3) << '\n';         // ???
       std::cout << add(2.5, 3) << '\n';       // ???
       std::cout << add('h', false) << '\n';   // ???
       std::cout << add("hello", 3) << '\n';   // ???
   }


Default Parameters
^^^^^^^^^^^^^^^^^^^

Default parameters allow you to provide a **fallback** value for one or more **trailing parameters**, making arguments optional during a function call.

.. code-block:: cpp

   // 'width' and 'height' are given default values.
   void create_window(const std::string& title, int width = 800, int height = 600) {
       // ... function body ...
   }

   int main() {
       // All arguments provided.
       create_window("My App", 1920, 1080);
       // 'height' is omitted, uses default of 600.
       create_window("Another App", 1280);
       // 'width' and 'height' are omitted, use defaults.
       create_window("Default App");
   }

.. admonition:: Best Practice
   :class: important

   Default values should **only be specified in the function declaration** (usually in the ``.hpp`` file), not the definition.

**Exercise: Predict the result for each line.**

.. code-block:: cpp

   // Function with default parameters
   void print_config(int id, bool logging = false, const std::string& mode = "auto") {
       std::cout << "ID: " << id << ", Logging: " << std::boolalpha
                 << logging << ", Mode: " << mode << '\n';
   }

   int main() {
       print_config(1, true, "manual"); // ???
       print_config(2, true);           // ???
       print_config(3);                 // ???
       print_config();                  // ???
   }

Default Parameters vs. Overloading
""""""""""""""""""""""""""""""""""""

Often, you can achieve the same result with either overloading or default parameters. Which should you choose?

.. grid:: 2

   .. grid-item-card:: Overloading

      .. code-block:: cpp

         // Two separate functions
         void print(std::string s);
         void print(std::string s, int indent);

   .. grid-item-card:: Default Parameter

      .. code-block:: cpp

         // One flexible function
         void print(std::string s, int indent = 0);

.. seealso::

   `F.51: Where there is a choice, prefer default arguments over overloading <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#Rf-default-args>`_

Where to Specify Default Values
"""""""""""""""""""""""""""""""""

The compiler needs a single, authoritative source for a function's default arguments. This source should always be the function's public-facing "contract".

.. admonition:: Best Practice
   :class: important

   Default parameters belong in the function declaration, not the definition.

.. grid:: 2

   .. grid-item-card:: Correct
      :class-card: sd-border-success

      .. code-block:: cpp

         // --- In your header file (.hpp) ---
         // Default value is specified here
         void print(std::string s, int indent = 0);

         // --- In your source file (.cpp) ---
         // The definition does NOT repeat the default
         void print(std::string s, int indent) {
             // ... function implementation ...
         }

   .. grid-item-card:: Incorrect
      :class-card: sd-border-danger

      .. code-block:: cpp

         // --- In your header file (.hpp) ---
         void print(std::string s, int indent = 0);

         // --- In your source file (.cpp) ---
         // ERROR: Redefinition of default argument
         void print(std::string s, int indent = 0) {
             // ...
         }


Part III -- Under the Hood
---------------------------

The Call Stack
^^^^^^^^^^^^^^

The call stack organizes all active function calls. Think of it as a stack of books: the last book you put on is the first one you take off (**LIFO: Last-In, First-Out**).

.. figure:: /_static/images/l5/books.pdf
   :alt: Stack of books
   :align: center
   :width: 15%

   The call stack works like a stack of books: Last-In, First-Out.

The call stack is the **entire structure**, while a stack frame is just a **single book** in that stack. Each book represents one active function call.

When a function is called, its stack frame is **pushed** onto the top of the call stack. When the function returns, its stack frame is **popped off**.

Visualizing the Call Stack
"""""""""""""""""""""""""""

As functions call each other, the stack grows. As they return, it shrinks.

.. code-block:: cpp

   void C() { /*...*/ }

   void B() {
       C();
   }

   void A() {
       B();
   }

   int main() {
       A();
   }

.. figure:: /_static/images/l5/callstacks.pdf
   :alt: Call stack visualization
   :align: center
   :width: 70%

   Visualization of the call stack as functions are called and returned.

**Exercise: Trace the call stack activities for the following program (manual and debugger).**

.. code-block:: cpp

   void f(int& x, int y, int z) {
       x += y + z;
   }

   int g(int a, int b) {
       int result{};
       result = a + b;
       f(result, a, b);
       return result;
   }

   int main() {
       int x{10};
       int y{20};
       int z{};
       z = g(x, y);
       std::cout << z << '\n';
   }

Recursive Functions
^^^^^^^^^^^^^^^^^^^^

A recursive function is a function that **calls itself**. Understanding the call stack is the key to seeing how this works without getting lost.

Each recursive call gets its **own unique stack frame** with its own set of local variables.

.. warning::

   Every recursive function needs a **base case**: a condition that stops the recursion and prevents an infinite loop (which would cause a **stack overflow**).

**Example: Factorial**

Calculating factorial (:math:`n! = n \times (n-1) \times \dots \times 1`) is a classic example of recursion.

.. code-block:: cpp

   long long factorial(int n) {
       // Base Case: Stops the recursion
       if (n <= 1) {
           return 1;
       }
       // Recursive Step
       return n * factorial(n - 1);
   }

   int main() {
       long long result{factorial(4)};
       // result is 24
   }

How ``factorial(4)`` is resolved:

- ``factorial(4)`` calls ``factorial(3)``

  - ``factorial(3)`` calls ``factorial(2)``

    - ``factorial(2)`` calls ``factorial(1)``

      - ``factorial(1)`` hits the **base case** and returns ``1``.

    - ``factorial(2)`` gets ``1`` and returns ``2 * 1 = 2``.

  - ``factorial(3)`` gets ``2`` and returns ``3 * 2 = 6``.

- ``factorial(4)`` gets ``6`` and returns ``4 * 6 = 24``.

When to Use (and Avoid) Recursion
""""""""""""""""""""""""""""""""""

Recursion can be elegant, but often comes with tradeoffs.

.. grid:: 2

   .. grid-item-card:: Niche Use Cases

      - **Naturally Recursive Problems**: When the problem definition itself is recursive.

        - Tree or graph traversals (e.g., searching a folder structure).
        - Mathematical functions (e.g., factorial, Fibonacci sequences).
        - Divide and conquer algorithms (e.g., quicksort, mergesort).

      - **Readability**: Sometimes, a recursive solution is much clearer and more concise than an iterative one.

   .. grid-item-card:: General Avoidance
      :class-card: sd-border-warning

      - **Performance Overhead**: Each function call involves pushing a new stack frame, which takes time and memory. Iterative solutions are often faster.
      - **Stack Overflow Risk**: Deep recursion consumes a lot of stack space. If the base case is not reached quickly enough, you can run out of stack memory, crashing your program.
      - **Debugging Complexity**: Tracing the flow of a recursive function can be harder than debugging a simple loop.

Pitfalls and Best Practices
"""""""""""""""""""""""""""""

When using recursion, be mindful of these common issues:

.. warning::

   - **Missing/Incorrect Base Case**: The most common error. Without a proper base case, the recursion never stops, leading to a stack overflow.
   - **Infinite Recursion**: If the recursive step does not move closer to the base case, you also get a stack overflow.
   - **Redundant Calculations**: Naive recursive solutions can re-calculate the same subproblems repeatedly (e.g., a simple Fibonacci implementation). This can be solved with **memoization** (caching results).
   - **Large Inputs**: Even with a correct base case, very large inputs can still cause a stack overflow due to too many nested calls.

.. admonition:: Best Practice
   :class: important

   **Always ask yourself:** Can this be done easily and more efficiently with a loop? If yes, prefer iteration. If the recursive solution is significantly clearer for a complex problem, use it cautiously.


Part IV -- Conventions and Best Practices
------------------------------------------

Documentation with Doxygen
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Good code is not just functional, it is also understandable. Documentation explains **what** your function does and **how** to use it, without needing to read the implementation.

In this course, we will use **Doxygen**, a standard tool that generates professional documentation directly from special comments in your code.

Where to Write Documentation
""""""""""""""""""""""""""""""

Documentation belongs on the **function declaration** (in the ``.hpp`` file), not the definition.

**Why?** The header file is the public **interface** or "contract" of your code. Developers should only need to know what a function does and how to use it (``.hpp``), not how it is implemented (``.cpp``).

.. warning::

   Do not document both the declaration and the definition. This leads to duplicated effort and creates a high risk of the two becoming inconsistent over time.

How to Document with Doxygen
""""""""""""""""""""""""""""""

Doxygen comments start with ``/**`` and use special commands starting with ``@`` or ``\``.

.. code-block:: cpp

   /**
    * @brief Calculates the area of a rectangle.
    * @param length The length of the rectangle. Must be a positive value.
    * @param width The width of the rectangle. Must be a positive value.
    * @return The calculated area of the rectangle.
    */
   int calculate_area(int length, int width);

- ``@brief``: A short, one-line summary of what the function does.
- ``@param <name>``: Describes a specific parameter.
- ``@return``: Describes what the function returns.

.. seealso::

   `Doxygen Overview <https://www.doxygen.nl/manual/index.html>`_

.. note::

   Feel free to use AI as a tool for Doxygen documentation; however, you must always review, edit, and verify the generated comments for accuracy.

The main() Function
^^^^^^^^^^^^^^^^^^^^

Every C++ executable program has one special function that acts as its entry point: ``main()``. When you run your program, ``main()`` is the first function that gets called.

- It must have a return type of ``int``. By convention, ``return 0;`` signals that the program executed successfully.
- It can optionally take arguments from the command line, allowing you to pass information to your program when you launch it.

.. seealso::

   `F.46: int is the return type for main() <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html#f46-int-is-the-return-type-for-main>`_

Command-Line Arguments: argc and argv
"""""""""""""""""""""""""""""""""""""""

The ``main`` function can receive information from the command line through two parameters.

- ``int argc`` (**arg**\ ument **c**\ ount): An integer that stores the number of command-line arguments provided. It is **always at least 1**, because the name of the program itself is counted as the first argument.
- ``char* argv[]`` (**arg**\ ument **v**\ ector): An array of C-style strings. Each string is one of the arguments.

  - ``argv[0]`` is always the name of the executable.
  - ``argv[1]`` is the first actual argument.

.. code-block:: cpp

   int main(int argc, char* argv[]) {
       std::cout << "Number of arguments provided: " << argc << '\n';

       for (int i{0}; i < argc; ++i) {
           std::cout << "Argument " << i << ": " << argv[i] << '\n';
       }
   }

.. code-block:: bash

   ./week5_cpp --mode fast --file data.txt

**Output:**

.. code-block:: text

   Number of arguments provided: 5
   Argument 0: ./week5_cpp
   Argument 1: --mode
   Argument 2: fast
   Argument 3: --file
   Argument 4: data.txt
