====================================================
Lecture
====================================================



C++ Overview
====================================================


.. card::
    :class-card: sd-border-info sd-shadow-sm

    **What is C++?**

    C++ is a **statically typed**, **compiled**, **multi-paradigm** programming
    language developed by **Bjarne Stroustrup** at Bell Labs in **1979**. It
    supports procedural, object-oriented, and generic programming paradigms and
    is widely used in systems programming, game development, embedded systems,
    and robotics.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: cppreference.com
        :class-card: sd-border-secondary

        `cppreference.com <https://en.cppreference.com/>`_

        Comprehensive reference for the C++ language and standard library.
        Highly recommended for looking up language features and functions.

    .. grid-item-card:: cplusplus.com
        :class-card: sd-border-secondary

        `cplusplus.com <https://cplusplus.com/>`_

        Another popular reference with tutorials and a searchable library
        reference. Good for beginners.

.. figure:: /_static/images/l2/cpp_timeline.png
   :align: center

   Timeline of C++ standards and evolution.


Hardware Interfacing
--------------------

C++ is widely used in robotics because it provides **low-level hardware
access** combined with **high-level abstractions**. The following
mechanisms enable hardware interfacing:

.. grid:: 1 2 2 3
    :gutter: 3

    .. grid-item-card:: Direct Memory Access
        :class-card: sd-border-secondary

        **Pointers** allow direct manipulation of memory addresses, enabling
        communication with hardware registers.

    .. grid-item-card:: Memory-Mapped I/O
        :class-card: sd-border-secondary

        Hardware registers are mapped to memory addresses that C++ code
        can read from and write to directly.

    .. grid-item-card:: Inline Assembly
        :class-card: sd-border-secondary

        C++ supports embedding assembly language instructions within
        source code for fine-grained hardware control.

    .. grid-item-card:: System Calls / APIs
        :class-card: sd-border-secondary

        Operating system APIs provide standardized interfaces for
        interacting with hardware devices.

    .. grid-item-card:: Specialized Libraries
        :class-card: sd-border-secondary

        Libraries such as ROS 2 and hardware abstraction layers
        simplify interfacing with sensors and actuators.


.. figure:: /_static/images/l2/development_process.png
   :align: center

   The C++ development process: Write, Build, Run.


Write
------

Hello World
^^^^^^^^^^^

The classic "Hello, World!" program demonstrates the minimal structure of
a C++ program.

.. code-block:: cpp

   #include <iostream>

   int main() {
       std::cout << "Hello, World!" << '\n';
       return 0;
   }

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Key Components**

    - ``#include <iostream>`` -- Preprocessor directive that includes the
      Input/Output stream library.
    - ``int main()`` -- The entry point of every C++ program. Execution
      begins here.
    - ``std::cout`` -- The standard character output stream, used to print
      text to the console.
    - ``'\n'`` -- The newline character, used to move to the next line.
    - ``return 0;`` -- Returns 0 to the operating system, indicating
      successful execution.
    - **Semicolons** (``;``) -- Every statement in C++ must end with a
      semicolon. A **statement** is an instruction that performs an action.


Basic I/O
^^^^^^^^^

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Output: std::cout**

    ``std::cout`` uses the **insertion operator** ``<<`` to send data to the
    standard output (console).

    - ``std`` is the **standard namespace**.
    - ``::`` is the **scope resolution operator**, which specifies that
      ``cout`` belongs to the ``std`` namespace.

.. dropdown:: std::cout Examples
    :class-container: sd-border-secondary
    :open:

    .. code-block:: cpp

       #include <iostream>

       int main() {
           // Output text
           std::cout << "Hello, World!" << '\n';

           // Output numbers
           std::cout << 42 << '\n';
           std::cout << 3.14 << '\n';

           // Chaining the insertion operator
           std::cout << "The answer is " << 42 << " and pi is " << 3.14 << '\n';

           return 0;
       }

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Input: std::cin**

    ``std::cin`` uses the **extraction operator** ``>>`` to read data from
    the standard input (keyboard).

.. dropdown:: std::cin Examples
    :class-container: sd-border-secondary
    :open:

    .. code-block:: cpp

       #include <iostream>

       int main() {
           int age;
           double height;

           std::cout << "Enter your age: ";
           std::cin >> age;

           std::cout << "Enter your height: ";
           std::cin >> height;

           std::cout << "Age: " << age << ", Height: " << height << '\n';

           return 0;
       }


Comments
^^^^^^^^

Comments are used to document code and are ignored by the compiler.

.. code-block:: cpp

   // This is a single-line comment

   /*
    * This is a multi-line comment.
    * It can span multiple lines.
    */


Build
------

.. figure:: /_static/images/l2/build.png
   :align: center

   The build process: Preprocessor, Compiler, Linker.

The build process transforms human-readable source code into an executable
program. It consists of three stages: **preprocessing**, **compilation**,
and **linking**.


Preprocessor
^^^^^^^^^^^^

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **What the Preprocessor Does**

    The preprocessor modifies the source code **before** compilation. It:

    - Removes comments.
    - Processes directives that start with ``#``:

      - ``#include`` -- Inserts the contents of a header file.
      - ``#define`` -- Defines macros (text substitution).
      - ``#ifdef`` / ``#ifndef`` -- Conditional compilation.

.. code-block:: bash

   g++ -std=c++17 -E week2.cpp

.. note::

   The ``-E`` flag tells the compiler to stop after preprocessing and output
   the preprocessed source code.


Compiler
^^^^^^^^

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **What the Compiler Does**

    The compiler translates the preprocessed source code into **machine code**
    (also called **object code**). Machine code consists of binary instructions
    that the CPU can execute directly.

.. code-block:: bash

   g++ -std=c++17 -c week2.cpp

.. note::

   The ``-c`` flag tells the compiler to compile but **not** link, producing
   an object file (``week2.o``).


Linker
^^^^^^

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **What the Linker Does**

    The linker combines one or more object files and libraries into a single
    **executable** file. It resolves references between object files (e.g.,
    function calls defined in other files).

.. code-block:: bash

   g++ week2.o -o week2_cpp


Run
----

.. code-block:: bash

   ./week2_cpp

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **What Happens When You Run a Program**

    1. The operating system **loads** the executable into **RAM**.
    2. The CPU executes instructions through the **fetch-decode-execute**
       cycle:

       - **Fetch**: Retrieve the next instruction from memory.
       - **Decode**: Interpret the instruction.
       - **Execute**: Perform the operation.

.. figure:: /_static/images/l2/execution2.pdf
   :align: center

   The fetch-decode-execute cycle.


Bits, Bytes, and Words
====================================================

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Fundamental Units of Data**

    - **Bit**: The smallest unit of data, representing either ``0`` or ``1``.
    - **Byte**: A group of **8 bits**. This is the standard addressable unit
      of memory.
    - **Word**: A fixed-size group of bits that the CPU processes as a single
      unit. The size depends on the architecture (e.g., 32-bit or 64-bit).

.. figure:: /_static/images/l2/memory.pdf
   :align: center

   Bits, bytes, and words in memory.

.. figure:: /_static/images/l2/representation.png
   :align: center

   Binary representation of data.


Memory Segments
---------------

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Program Memory Layout**

    When a program is loaded into memory, it is organized into the following
    segments:

    - **Text (Code) Segment** -- Contains the compiled machine code
      instructions.
    - **Data Segment** -- Stores initialized global and static variables.
    - **BSS Segment** -- Stores uninitialized global and static variables
      (initialized to zero).
    - **Heap** -- Dynamic memory allocated at runtime (grows upward).
    - **Stack** -- Stores local variables and function call information
      (grows downward).
    - **Arguments** -- Stores command-line arguments and environment
      variables.


Variables
====================================================


.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Definition**

    A **variable** is a symbolic name associated with a **storage location**
    in memory. It holds a value that can be read and modified during program
    execution.

.. figure:: /_static/images/l2/Lecture2-variable1.pdf
   :align: center

   A variable maps a name to a memory location.


Characteristics
---------------

.. grid:: 1 2 2 3
    :gutter: 3

    .. grid-item-card:: Type
        :class-card: sd-border-secondary

        Determines what kind of data the variable can hold and how much
        memory is allocated for it.

    .. grid-item-card:: Name (Identifier)
        :class-card: sd-border-secondary

        The symbolic name used to refer to the variable in code.

    .. grid-item-card:: Scope
        :class-card: sd-border-secondary

        The region of the program where the variable is accessible.

    .. grid-item-card:: Lifetime
        :class-card: sd-border-secondary

        How long the variable exists in memory during program execution.

    .. grid-item-card:: Value
        :class-card: sd-border-secondary

        The data stored in the variable's memory location.


Naming (Identifiers)
---------------------

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Rules for Identifiers**

    - Can contain **letters**, **numbers**, and **underscores** (``_``).
    - Must **start** with a **letter** or **underscore** (not a number).
    - Are **case sensitive** (``myVar`` and ``myvar`` are different).
    - Cannot use **reserved keywords** (e.g., ``int``, ``return``, ``class``).

.. dropdown:: Valid and Invalid Identifiers
    :class-container: sd-border-secondary
    :open:

    .. code-block:: cpp

       // Valid identifiers
       int age;
       int _count;
       int student_name;
       int value2;

       // Invalid identifiers
       int 2value;         // starts with a number
       int my-variable;    // contains a hyphen
       int int;            // reserved keyword
       int my variable;    // contains a space

.. warning::

   In this course, we use **snake_case** for naming variables. This means
   all lowercase letters with words separated by underscores.

   **Use:**

   - ``my_variable``
   - ``student_count``
   - ``max_temperature``
   - ``is_valid``

   **Avoid:**

   - ``camelCase`` (e.g., ``myVariable``)
   - ``PascalCase`` (e.g., ``MyVariable``)
   - ``ALL_CAPS`` (e.g., ``MY_VARIABLE``) -- reserved for constants and macros.


Variable Types
--------------

.. grid:: 1 2 2 3
    :gutter: 3

    .. grid-item-card:: Primitive Types
        :class-card: sd-border-secondary

        Built-in types provided by the language: ``int``, ``double``,
        ``char``, ``bool``, ``float``, etc.

    .. grid-item-card:: Standard Library Types
        :class-card: sd-border-secondary

        Types provided by the C++ Standard Library: ``std::string``,
        ``std::vector``, ``std::array``, etc.

    .. grid-item-card:: User-defined Types
        :class-card: sd-border-secondary

        Types created by the programmer using ``class``, ``struct``,
        ``enum``, etc.

.. note::

   The **type** of a variable tells the compiler **how much memory** to
   allocate and **what kind of value** the variable can store.


sizeof Operator
^^^^^^^^^^^^^^^

The ``sizeof`` operator returns the size (in bytes) of a type or
expression.

.. code-block:: cpp

   sizeof(type)
   sizeof(expression)

.. note::

   The sizes returned by ``sizeof`` are **platform-dependent**. They may
   differ across compilers and architectures.


Memory Allocation
-----------------

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **What Happens When You Write** ``int number = 20;``

    1. The CPU **reserves** a block of bytes (typically 4 for ``int``).
    2. The memory address of the first byte is **associated** with the
       variable name ``number``.
    3. The value ``20`` is **written** in binary to the reserved bytes.
    4. The type ``int`` **restricts** what operations can be performed
       on the variable.

.. tip::

   The **address operator** ``&`` returns the memory address of a variable:

   .. code-block:: cpp

      int number = 20;
      std::cout << &number << '\n';  // prints the memory address

.. figure:: /_static/images/l2/demo.pdf
   :align: center

   Memory allocation for ``int number = 20;``.

.. figure:: /_static/images/l2/visualization.pdf
   :align: center

   Visualization of variable storage in memory.


Declarations
^^^^^^^^^^^^

A **declaration** introduces a variable name and its type to the compiler,
reserving memory for it.

.. code-block:: cpp

   int number;  // declaration -- reserves memory for an int

.. note::

   **Guideline ES.10**: Declare one name per declaration. This improves
   readability and avoids subtle errors.

   .. code-block:: cpp

      // Good
      int width;
      int height;

      // Avoid
      int width, height;


Assignments
^^^^^^^^^^^

An **assignment** uses the **copy assignment operator** ``=`` to store a
value in a previously declared variable. Assigning a new value
**overwrites** the old one.

.. code-block:: cpp

   int number;
   number = 20;   // assignment
   number = 30;   // overwriting the previous value


Initializations
^^^^^^^^^^^^^^^

**Initialization** combines declaration and assignment in a single step.
C++ provides three forms of initialization:

.. list-table::
   :widths: 30 40 30
   :header-rows: 1
   :class: compact-table

   * - Form
     - Syntax
     - Example
   * - Copy Initialization
     - ``type name = value;``
     - ``int a = 1;``
   * - Direct Initialization
     - ``type name(value);``
     - ``int a(1);``
   * - Uniform Initialization
     - ``type name{value};``
     - ``int a{1};``

.. tip::

   **Best practice**: Use **uniform initialization** (also called brace
   initialization) whenever possible. It prevents narrowing conversions
   and works consistently across all types.

   .. code-block:: cpp

      int a{1};           // uniform initialization (preferred)
      double b{3.14};
      char c{'A'};


Zero Initialization
^^^^^^^^^^^^^^^^^^^

Uniform initialization with empty braces initializes a variable to its
**zero value** (``0`` for numeric types, ``false`` for ``bool``).

.. code-block:: cpp

   int a{};     // a is 0
   double b{};  // b is 0.0
   bool c{};    // c is false

.. tip::

   - Use ``{0}`` when you intend to **use** the zero value directly.
   - Use ``{}`` when the variable is **temporary** or will be assigned
     later.


Uninitialized Variables
^^^^^^^^^^^^^^^^^^^^^^^

.. warning::

   A variable that is declared but **not initialized** contains a
   **garbage value** -- whatever bits happen to be in the memory location.
   Reading an uninitialized variable is **undefined behavior**.

   .. code-block:: cpp

      int x;                    // uninitialized -- contains garbage
      std::cout << x << "\n";   // undefined behavior!


Undefined Behavior
====================================================

.. card::
    :class-card: sd-border-danger sd-shadow-sm

    **Definition**

    **Undefined behavior** (UB) is the result of executing code whose
    behavior is not prescribed by the C++ standard. When UB occurs, the
    program has **no guarantees** -- it may crash, produce incorrect results,
    or appear to work correctly.

.. dropdown:: Common Examples of Undefined Behavior
    :class-container: sd-border-secondary
    :open:

    - **Array out-of-bounds access**: Accessing an element beyond the array's
      valid range.
    - **Null pointer dereference**: Accessing memory through a null pointer.
    - **Signed integer overflow**: Exceeding the range of a signed integer.
    - **Reading uninitialized variables**: Using a variable before assigning
      it a value.

.. tip::

   Enable compiler warnings to catch potential UB at compile time. Add
   ``-Wall -Wextra`` to your build flags.

   In ``CMakeLists.txt``:

   .. code-block:: cmake

      add_compile_options(-Wall -Wextra)


Integral Types
====================================================

**Integral types** represent **whole numbers** (no fractional part).

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Integral Types in C++**

    - ``int`` -- Standard integer.
    - ``char`` -- Character (also an integer type).
    - ``short`` -- Short integer.
    - ``long`` -- Long integer.
    - ``long long`` -- Extended long integer.
    - ``bool`` -- Boolean (``true`` or ``false``).
    - Each type has ``signed`` and ``unsigned`` variants.


Signedness Modifiers
--------------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: signed
        :class-card: sd-border-secondary

        Can store both **positive** and **negative** values.

        **Advantages:**

        - Represents a full range of numbers including negatives.
        - Default for most integral types.

    .. grid-item-card:: unsigned
        :class-card: sd-border-secondary

        Can store only **non-negative** values (zero and positive).

        **Advantages:**

        - Doubles the positive range compared to signed.
        - Useful for quantities that are never negative (e.g., sizes,
          counts).

.. note::

   **Trade-off**: Choosing ``unsigned`` doubles the positive range but
   sacrifices the ability to represent negative values.


Size Modifiers
--------------

.. list-table::
   :widths: 25 35 40
   :header-rows: 1
   :class: compact-table

   * - Modifier
     - Minimum Size
     - Notes
   * - ``short``
     - >= 16 bits (2 bytes)
     - Smaller range, saves memory.
   * - ``long``
     - >= 32 bits (4 bytes)
     - Extended range.
   * - ``long long``
     - >= 64 bits (8 bytes)
     - Very large range.

.. note::

   The C++ standard guarantees the following size relationships:

   ``sizeof(short) <= sizeof(int) <= sizeof(long) <= sizeof(long long)``


Type, Size, and Range
---------------------

.. list-table::
   :widths: 18 10 36 36
   :header-rows: 1
   :class: compact-table

   * - Type
     - Size (bytes)
     - Signed Range
     - Unsigned Range
   * - ``char``
     - 1
     - -128 to 127
     - 0 to 255
   * - ``short``
     - 2
     - -32,768 to 32,767
     - 0 to 65,535
   * - ``int``
     - 4
     - -2,147,483,648 to 2,147,483,647
     - 0 to 4,294,967,295
   * - ``long``
     - 8
     - -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807
     - 0 to 18,446,744,073,709,551,615
   * - ``long long``
     - 8
     - -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807
     - 0 to 18,446,744,073,709,551,615


Compiler Behavior Differences
------------------------------

.. card::
    :class-card: sd-border-warning sd-shadow-sm

    **Signed vs. Unsigned: Compiler Quirks**

    - The compiler generates **different instructions** for signed and
      unsigned operations.
    - **Comparison quirks**: Comparing signed and unsigned values can produce
      unexpected results. For example:

      .. code-block:: cpp

         // This comparison is FALSE!
         std::cout << (-1 < 1u) << '\n';  // prints 0 (false)

      The signed value ``-1`` is implicitly converted to unsigned, resulting
      in a very large positive number.

    - **Overflow treatment**: Signed overflow is **undefined behavior**;
      unsigned overflow is well-defined (wraps around).


Floating-point Number Types
====================================================

**Floating-point types** represent numbers with **fractional parts**.

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Floating-point Types in C++**

    - ``float`` -- Single precision.
    - ``double`` -- Double precision.
    - ``long double`` -- Extended precision.
    - Floating-point types are **always signed**.


Precision
---------

.. list-table::
   :widths: 20 15 25 20
   :header-rows: 1
   :class: compact-table

   * - Type
     - Size (bytes)
     - Range
     - Precision (digits)
   * - ``float``
     - 4
     - ~1.2e-38 to ~3.4e+38
     - ~7
   * - ``double``
     - 8
     - ~2.2e-308 to ~1.8e+308
     - ~16
   * - ``long double``
     - 16
     - ~3.4e-4932 to ~1.1e+4932
     - ~33


Float Suffix
^^^^^^^^^^^^

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **The** ``f`` **Suffix**

    By default, a floating-point literal like ``1.05`` is of type ``double``.
    To explicitly make it a ``float``, append the ``f`` suffix:

    .. code-block:: cpp

       double d = 1.05;    // 1.05 is a double literal
       float f = 1.05f;    // 1.05f is a float literal


std::setprecision
^^^^^^^^^^^^^^^^^

Use ``std::setprecision()`` from the ``<iomanip>`` header to control the
number of significant digits displayed.

.. code-block:: cpp

   #include <iostream>
   #include <iomanip>

   int main() {
       double pi{3.141592653589793};

       std::cout << std::setprecision(3) << pi << '\n';   // 3.14
       std::cout << std::setprecision(7) << pi << '\n';   // 3.141593
       std::cout << std::setprecision(15) << pi << '\n';  // 3.14159265358979

       return 0;
   }


Boolean Type
====================================================

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **The bool Type**

    - Size: **1 byte**.
    - Values: ``true`` or ``false``.
    - Any **non-zero** value is treated as ``true``; ``0`` is ``false``.

.. dropdown:: Boolean Examples
    :class-container: sd-border-secondary
    :open:

    .. code-block:: cpp

       #include <iostream>

       int main() {
           bool is_valid{true};
           bool is_empty{false};

           std::cout << is_valid << '\n';    // prints 1
           std::cout << is_empty << '\n';    // prints 0

           // Use std::boolalpha to print "true" / "false"
           std::cout << std::boolalpha;
           std::cout << is_valid << '\n';    // prints true
           std::cout << is_empty << '\n';    // prints false

           // Use std::noboolalpha to revert to numeric output
           std::cout << std::noboolalpha;
           std::cout << is_valid << '\n';    // prints 1

           return 0;
       }


Type Conversion
====================================================

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Definition**

    **Type conversion** is the process of converting a value from one type
    to another. It can be **implicit** (automatic, performed by the compiler)
    or **explicit** (manually specified by the programmer).


Implicit Type Conversion
-------------------------

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Implicit Conversion**

    The compiler automatically converts types in the following contexts:

    - **Initialization**: When the initializer type differs from the
      variable type.
    - **Return values**: When the returned type differs from the function's
      return type.
    - **Binary operators**: When operands have different types.
    - **if-statements**: Non-boolean values are converted to ``bool``.
    - **Function arguments**: When the argument type differs from the
      parameter type.


typeid and c++filt
^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   #include <iostream>
   #include <typeinfo>

   int main() {
       auto x = 3.14;
       std::cout << typeid(x).name() << '\n';  // prints mangled type name
       return 0;
   }

.. tip::

   Use ``c++filt`` to demangle type names:

   .. code-block:: bash

      echo "_ZN3std4cout" | c++filt


Standard Conversions
---------------------

The C++ standard defines **four categories** of implicit conversions:

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: Numeric Promotions
        :class-card: sd-border-secondary

        Smaller types are promoted to larger types within the same family.

    .. grid-item-card:: Numeric Conversions
        :class-card: sd-border-secondary

        Additional conversions not covered by promotion.

    .. grid-item-card:: Arithmetic Conversions
        :class-card: sd-border-secondary

        Applied when binary operators have operands of different types.

    .. grid-item-card:: Other Conversions
        :class-card: sd-border-secondary

        Pointer conversions, boolean conversions, etc.


Numeric Promotion
^^^^^^^^^^^^^^^^^

**Numeric promotion** converts a smaller type to a larger type within the
**same family**, preserving the value exactly.

.. list-table::
   :widths: 50 50
   :header-rows: 1
   :class: compact-table

   * - From
     - To
   * - ``float``
     - ``double``
   * - ``char``
     - ``int``
   * - ``short``
     - ``int``
   * - ``bool``
     - ``int`` (``false`` -> 0, ``true`` -> 1)


Numeric Conversion
^^^^^^^^^^^^^^^^^^

**Numeric conversions** cover additional type conversions not handled by
promotion. These may result in **loss of data** or **precision**.

.. list-table::
   :widths: 50 50
   :header-rows: 1
   :class: compact-table

   * - From
     - To
   * - ``int``
     - ``short``
   * - ``double``
     - ``float``
   * - ``double``
     - ``int``
   * - ``int``
     - ``bool``

.. warning::

   **Narrowing conversion**: A conversion that may lose data (e.g.,
   ``double`` to ``int``). **Uniform initialization** disallows narrowing
   conversions and will produce a compiler error.

   .. code-block:: cpp

      int a{3.5};  // ERROR: narrowing conversion from double to int

   Use ``static_cast`` for explicit narrowing:

   .. code-block:: cpp

      int a{static_cast<int>(3.5)};  // OK: explicit narrowing


Arithmetic Conversions
^^^^^^^^^^^^^^^^^^^^^^

When a binary operator has operands of **different types**, the compiler
converts them to a **common type** using the following priority list
(highest to lowest):

1. ``long double``
2. ``double``
3. ``float``
4. ``unsigned long long``
5. ``long long``
6. ``unsigned long``
7. ``long``
8. ``unsigned int``
9. ``int`` (lowest priority)

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Rules**

    - **Rule 1**: The operand with the **lower priority** type is promoted
      to the **higher priority** type.
    - **Rule 2**: If neither operand's type is on the priority list, both
      are promoted (e.g., ``short`` and ``char`` are promoted to ``int``).

.. dropdown:: Arithmetic Conversion Examples
    :class-container: sd-border-secondary
    :open:

    .. code-block:: cpp

       #include <iostream>
       #include <typeinfo>

       int main() {
           int i{5};
           double d{2.5};

           // i is promoted to double before addition
           auto result = i + d;
           std::cout << typeid(result).name() << '\n';  // double

           short s{10};
           char c{'A'};

           // both promoted to int before addition
           auto result2 = s + c;
           std::cout << typeid(result2).name() << '\n';  // int

           return 0;
       }


Constants
====================================================

C++ provides **three types** of constants:

.. grid:: 1 2 2 3
    :gutter: 3

    .. grid-item-card:: Literal Constants
        :class-card: sd-border-secondary

        Fixed values written directly in the source code.

    .. grid-item-card:: Constant Variables
        :class-card: sd-border-secondary

        Variables declared with ``const`` whose value cannot change.

    .. grid-item-card:: Symbolic Constants
        :class-card: sd-border-secondary

        Macros defined with ``#define`` (preprocessor).


Literal Constants
-----------------

**Literal constants** are fixed values that appear directly in the source
code. They include:

- **Integral literals**: ``42``, ``0xFF``, ``0b1010``
- **Floating-point literals**: ``3.14``, ``1.0e-5``
- **Character literals**: ``'A'``, ``'\n'``
- **String literals**: ``"Hello, World!"``
- **Boolean literals**: ``true``, ``false``


Constant Variables
------------------

A **constant variable** is declared with the ``const`` keyword. Its value
must be set at initialization and **cannot be changed** afterward.

.. code-block:: cpp

   const double pi{3.141598};

.. note::

   **West const** (``const`` before the type) is preferred in this course:

   .. code-block:: cpp

      const int max_size{100};    // west const (preferred)
      int const max_size{100};    // east const (also valid)

.. warning::

   A ``const`` variable **must** be initialized at declaration. Attempting
   to reassign a ``const`` variable will produce a compiler error.

   .. code-block:: cpp

      const int x{10};
      x = 20;  // ERROR: cannot assign to a const variable


Symbolic Constants
------------------

**Symbolic constants** are defined using the ``#define`` preprocessor
directive.

.. code-block:: cpp

   #define PI 3.14159

.. warning::

   **Avoid using** ``#define`` **for constants.** Macros have no type
   checking, no scope, and are difficult to debug. Use ``const`` or
   ``constexpr`` instead.


Constant Expressions
--------------------

A **constant expression** is an expression that can be evaluated entirely
at **compile time**. The compiler replaces the expression with its computed
result.

.. code-block:: cpp

   const int x{5};
   const int y{x + 3};  // constant expression: evaluated at compile time


constexpr
^^^^^^^^^^

The ``constexpr`` keyword **guarantees** that a variable or function is
evaluated at **compile time**. If a runtime value is used, the compiler
produces an error.

.. code-block:: cpp

   constexpr double pi{3.141592653589793};
   constexpr int square{5 * 5};

.. card::
    :class-card: sd-border-success sd-shadow-sm

    **Performance Benefits of constexpr**

    - **No runtime cost**: The value is computed during compilation.
    - **Reduced memory usage**: The compiler may replace the variable with
      its value directly.
    - **Better inlining**: The compiler has more optimization opportunities.

.. code-block:: cpp

   int x;
   std::cin >> x;
   constexpr int y{x};  // ERROR: x is not a compile-time constant


Type Deduction
====================================================

The ``auto`` keyword tells the compiler to **deduce** the variable's type
from its initializer.

.. code-block:: cpp

   auto a{42};       // int
   auto b{3.14};     // double
   auto c{'A'};      // char
   auto d{true};     // bool

.. warning::

   ``auto`` requires an initializer. The following are errors:

   .. code-block:: cpp

      auto a;    // ERROR: no initializer
      auto b{};  // ERROR: cannot deduce type from empty braces

.. note::

   ``auto`` drops the ``const`` qualifier. To preserve ``const``, use
   ``const auto`` or ``constexpr auto``:

   .. code-block:: cpp

      const int x{10};
      auto y{x};           // y is int (const dropped)
      const auto z{x};     // z is const int
      constexpr auto w{x}; // w is constexpr int


Compound Statements
====================================================

A **compound statement** (or **block**) is a group of statements enclosed
in curly braces ``{}``.

.. code-block:: cpp

   {
       int x{10};
       int y{20};
       std::cout << x + y << '\n';
   }

.. note::

   - There is **no semicolon** after the closing brace of a block.
   - Keep nesting levels to **3 or fewer** for readability.


Scopes
====================================================


Local Scope
-----------

Variables declared inside a function body or block have **local scope**.
They are created at the point of definition and **destroyed** when the
closing brace ``}`` is reached.

.. dropdown:: Local Scope Example
    :class-container: sd-border-secondary
    :open:

    .. code-block:: cpp

       #include <iostream>

       int main() {
           int x{10};  // x is in scope

           {
               int y{20};  // y is in scope (nested block)
               std::cout << x << '\n';  // OK: x is accessible
               std::cout << y << '\n';  // OK: y is accessible
           }  // y is destroyed here

           std::cout << x << '\n';  // OK: x is still in scope
           // std::cout << y << '\n';  // ERROR: y is out of scope

           return 0;
       }


Out of Scope
^^^^^^^^^^^^

When a variable goes **out of scope**, its memory is **deallocated**. However,
the garbage data may remain in that memory location until it is overwritten.

.. figure:: /_static/images/l2/outofscope.pdf
   :align: center

   Memory after a variable goes out of scope.


Global Scope
------------

Variables declared **outside** any function have **global scope**. They
are visible from the point of declaration to the **end of the file**.

.. dropdown:: Global Scope Example
    :class-container: sd-border-secondary
    :open:

    .. code-block:: cpp

       #include <iostream>

       int global_var{100};  // global variable

       int main() {
           std::cout << global_var << '\n';  // OK: accessible
           global_var = 200;
           std::cout << global_var << '\n';  // prints 200
           return 0;
       }

.. warning::

   **Global variables are evil.** They make code harder to understand,
   debug, and maintain because any function can modify them. If you need a
   global constant, use ``const`` or ``constexpr``.

.. figure:: /_static/images/l2/globalvars.pdf
   :align: center

   Why global variables are problematic.


Naming Collisions and Namespaces
====================================================


Naming Collisions
-----------------

A **naming collision** occurs when two or more identifiers with the
**same name** are introduced in the **same scope**, causing an ambiguity
error.


Namespaces
----------

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Definition**

    A **namespace** is a declarative region that provides a **scope** for
    the identifiers inside it. Namespaces prevent naming collisions by
    grouping related names together. The ``std`` namespace contains all
    C++ standard library identifiers.


Explicit Use
^^^^^^^^^^^^

Use the **scope resolution operator** ``::`` to explicitly access names
within a namespace.

.. code-block:: cpp

   namespace MyNamespace {
       int x{42};
       void print() {
           std::cout << "Hello from MyNamespace" << '\n';
       }
   }

   int main() {
       std::cout << MyNamespace::x << '\n';
       MyNamespace::print();
       return 0;
   }


using namespace
^^^^^^^^^^^^^^^

The ``using namespace`` directive makes **all** names in a namespace
available without qualification.

.. code-block:: cpp

   using namespace std;

   int main() {
       cout << "No need for std::" << '\n';
       return 0;
   }


using Directive (Individual Names)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``using`` directive can also import **individual** names from a
namespace.

.. code-block:: cpp

   using std::cout;

   int main() {
       cout << "Only cout imported" << '\n';
       return 0;
   }

.. warning::

   **Avoid** ``using namespace`` in production code. It can cause
   **ambiguity** when multiple namespaces define the same name.

   .. code-block:: cpp

      namespace MyNamespace {
          void cout() { /* ... */ }
      }

      using namespace std;
      using namespace MyNamespace;

      int main() {
          cout << "Hello";  // ERROR: ambiguous -- std::cout or MyNamespace::cout?
          return 0;
      }

.. tip::

   **Best practice**: Use explicit namespace qualification
   (e.g., ``std::cout``) or import individual names with ``using``.


Aliases
====================================================

**Type aliases** create alternative names for existing types, making code
more readable and maintainable.

.. code-block:: cpp

   using Integer = int;
   using Float = float;
   using uint = unsigned int;

.. dropdown:: Alias Usage Example
    :class-container: sd-border-secondary
    :open:

    .. code-block:: cpp

       #include <iostream>

       using Integer = int;
       using Float = float;
       using uint = unsigned int;

       int main() {
           Integer count{10};
           Float temperature{98.6f};
           uint size{256};

           std::cout << "Count: " << count << '\n';
           std::cout << "Temperature: " << temperature << '\n';
           std::cout << "Size: " << size << '\n';

           return 0;
       }

.. note::

   Type aliases make code more readable and easier to maintain. If the
   underlying type needs to change, only the alias definition needs to be
   updated.


Scoped Enumerations
====================================================

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **What is** ``enum class`` **?**

    An ``enum class`` (scoped enumeration), introduced in **C++11**, is a
    **type-safe** enumeration. Unlike unscoped ``enum``, the enumerator values
    are **scoped to the enum name** and do **not** implicitly convert to
    integers. This prevents accidental misuse and name collisions.


Syntax
------

.. code-block:: cpp

   enum class Color {
       red,
       green,
       blue
   };

   Color my_color{Color::red};

Enumerator values are accessed using the **scope resolution operator**
(``::``), e.g., ``Color::red``.


Why ``enum class`` over ``enum``
---------------------------------

.. grid:: 1 2 2 3
    :gutter: 3

    .. grid-item-card:: Type Safety
        :class-card: sd-border-secondary

        Values do **not** implicitly convert to ``int``. You must use an
        explicit ``static_cast`` if an integer value is needed.

    .. grid-item-card:: Scoped Names
        :class-card: sd-border-secondary

        Enumerator names are scoped to the enum type, so ``Color::red``
        and ``TrafficLight::red`` can coexist without collision.

    .. grid-item-card:: Explicit Underlying Type
        :class-card: sd-border-secondary

        You can specify the underlying integer type. The default is
        ``int``, but any integral type can be used.

.. warning::

   **Avoid unscoped** ``enum`` **in modern C++.**

   Unscoped enumerations leak their enumerator names into the enclosing
   scope and implicitly convert to ``int``, which can cause subtle bugs:

   .. code-block:: cpp

      // Problem 1: Name collisions
      enum Color { red, green, blue };
      enum TrafficLight { red, yellow, green };  // ERROR: 'red' and 'green' already declared

      // Problem 2: Implicit conversion to int
      enum Direction { up, down };
      int value{up + 42};  // Compiles without warning -- likely a bug

   Use ``enum class`` to avoid both issues.


Underlying Type
----------------

The default underlying type of an ``enum class`` is ``int``. You can specify
a different integral type after a colon:

.. code-block:: cpp

   enum class Status : uint8_t {
       active,
       inactive
   };

This is useful when memory is constrained (e.g., embedded systems) or when
interfacing with hardware registers that expect a specific width.


Use Cases in Robotics
----------------------

Scoped enumerations are ideal for representing a **fixed set of named
constants**. Common robotics use cases include:

.. grid:: 1 2 2 3
    :gutter: 3

    .. grid-item-card:: Robot States
        :class-card: sd-border-secondary

        ``idle``, ``moving``, ``charging``, ``error``

    .. grid-item-card:: Sensor Types
        :class-card: sd-border-secondary

        ``lidar``, ``camera``, ``imu``

    .. grid-item-card:: Command Types
        :class-card: sd-border-secondary

        ``forward``, ``backward``, ``left``, ``right``, ``stop``


Code Example
-------------

.. dropdown:: Robot State Machine with ``enum class``
    :class-container: sd-border-secondary
    :open:

    .. code-block:: cpp

       #include <iostream>
       #include <cstdint>

       enum class RobotState : uint8_t {
           idle,
           moving,
           charging,
           error
       };

       int main() {
           RobotState state{RobotState::idle};

           // Switch statement with enum class
           switch (state) {
               case RobotState::idle:
                   std::cout << "Robot is idle" << '\n';
                   break;
               case RobotState::moving:
                   std::cout << "Robot is moving" << '\n';
                   break;
               case RobotState::charging:
                   std::cout << "Robot is charging" << '\n';
                   break;
               case RobotState::error:
                   std::cout << "Robot error!" << '\n';
                   break;
           }

           return 0;
       }

.. dropdown:: Explicit Conversion to Integer
    :class-container: sd-border-secondary

    If you need the underlying integer value, use ``static_cast``:

    .. code-block:: cpp

       #include <iostream>

       enum class SensorType {
           lidar,
           camera,
           imu
       };

       int main() {
           SensorType sensor{SensorType::camera};

           // static_cast is required -- no implicit conversion
           int sensor_id{static_cast<int>(sensor)};
           std::cout << "Sensor ID: " << sensor_id << '\n';  // Output: 1

           return 0;
       }
