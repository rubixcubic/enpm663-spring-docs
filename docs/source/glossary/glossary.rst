====================================================
Glossary
====================================================

This glossary covers all key terms from the ENPM702 course. Entries are
organized alphabetically across all lectures. Click any letter to jump to
that section.

:ref:`A <g-a>` · :ref:`B <g-b>` · :ref:`C <g-c>` · :ref:`D <g-d>` ·
:ref:`E <g-e>` · :ref:`F <g-f>` · :ref:`H <g-h>` · :ref:`I <g-i>` ·
:ref:`K <g-k>` · :ref:`L <g-l>` · :ref:`M <g-m>` · :ref:`N <g-n>` ·
:ref:`O <g-o>` · :ref:`P <g-p>` · :ref:`R <g-r>` · :ref:`S <g-s>` ·
:ref:`T <g-t>` · :ref:`U <g-u>` · :ref:`V <g-v>` · :ref:`W <g-w>` ·
:ref:`Z <g-z>`

.. only:: html

   .. raw:: html

      <div id="glossary-search-wrap" style="margin: 1.2em 0 1.4em 0;">
        <input
          id="glossary-search"
          type="search"
          placeholder="Filter terms..."
          autocomplete="off"
          spellcheck="false"
          style="
            width: 100%;
            max-width: 480px;
            padding: 0.45em 0.75em;
            font-size: 1em;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
          "
        />
        <span
          id="glossary-search-count"
          style="margin-left: 0.8em; font-size: 0.88em; color: #666;"
        ></span>
      </div>

      <script>
      (function () {
        /* Run after the DOM is ready. */
        function initGlossarySearch() {
          var input  = document.getElementById('glossary-search');
          var count  = document.getElementById('glossary-search-count');
          if (!input) return;

          function getLetterSection(el) {
            var node = el;
            while (node && node !== document.body) {
              if (node.id && /^glossary-[a-z]$/i.test(node.id)) return node;
              node = node.parentElement;
            }
            return null;
          }

          function run() {
            var query = input.value.trim().toLowerCase();

            var allDt = document.querySelectorAll('dl.glossary dt');
            var visible = 0;

            allDt.forEach(function (dt) {
              var siblings = [];
              var node = dt.nextElementSibling;
              while (node && node.tagName === 'DD') {
                siblings.push(node);
                node = node.nextElementSibling;
              }

              var text = dt.textContent.toLowerCase();
              var match = !query || text.indexOf(query) !== -1;

              dt.style.display = match ? '' : 'none';
              siblings.forEach(function (dd) { dd.style.display = match ? '' : 'none'; });
              if (match) visible++;
            });

            var allDl = document.querySelectorAll('dl.glossary');
            allDl.forEach(function (dl) {
              var anyVisible = Array.prototype.some.call(
                dl.querySelectorAll('dt'),
                function (dt) { return dt.style.display !== 'none'; }
              );
              dl.style.display = anyVisible ? '' : 'none';

              var section = getLetterSection(dl);
              if (section) {
                section.style.display = anyVisible ? '' : 'none';
              } else {
                var prev = dl.previousElementSibling;
                while (prev) {
                  if (prev.tagName === 'H2' || prev.tagName === 'H1') {
                    prev.style.display = anyVisible ? '' : 'none';
                    break;
                  }
                  prev = prev.previousElementSibling;
                }
              }
            });

            if (query) {
              count.textContent = visible === 1
                ? '1 term found'
                : visible + ' terms found';
            } else {
              count.textContent = '';
            }
          }

          input.addEventListener('input', run);

          input.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') { input.value = ''; run(); input.blur(); }
          });
        }

        if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', initGlossarySearch);
        } else {
          initGlossarySearch();
        }
      })();
      </script>

----


.. _g-a:

A
=

.. glossary::

   Abstract Class
      A class with at least one pure virtual function. Cannot be instantiated directly; serves as an interface for derived classes.
      :doc:`L9 </lectures/lecture9/l9_lecture>`

   Access Specifier
      Keywords (``public``, ``private``, ``protected``) that control the visibility and accessibility of class members.
      :doc:`L8 </lectures/lecture8/l8_lecture>`

   Aggregation
      A "has-a" relationship where the part can exist independently of the whole. Represented by an empty diamond in UML.
      :doc:`L9 </lectures/lecture9/l9_lecture>`

   Alias
      A shell shortcut that maps a short identifier to a longer command.
      Defined with ``alias name='command'`` in a shell configuration file.
      Aliases are lost when the terminal session ends unless saved in the
      configuration file.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Alias (C++ Type)
      A type alias created with the ``using`` keyword that gives an
      alternative name to an existing type. Example:
      ``using Integer = int;``
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Arithmetic Conversion
      Implicit type conversion rules applied when binary operators have
      operands of different types. The operand with lower priority is
      converted to the higher-priority type.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Association
      A general relationship between classes where objects of one class use or interact with objects of another.
      :doc:`L9 </lectures/lecture9/l9_lecture>`

   auto
      A keyword that enables type deduction, allowing the compiler to
      deduce the type of a variable from its initializer. Requires an
      initializer; drops ``const`` by default.
      :doc:`L2 </lectures/lecture2/l2_lecture>`


.. _g-b:

B
=

.. glossary::

   Bash
      Bourne Again Shell. The default shell for most Linux distributions,
      widely used for scripting and interactive command-line use.
      :doc:`L1 </lectures/lecture1/l1_lecture>`


.. _g-c:

C
=

.. glossary::

   Capture Clause
      The ``[]`` part of a lambda expression that specifies which variables from the enclosing scope are available inside the lambda body.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Class
      A user-defined type that encapsulates data (attributes) and behavior (methods). A blueprint for creating objects.
      :doc:`L8 </lectures/lecture8/l8_lecture>`

   CMake
      An open-source, cross-platform build system used to build, test,
      and package C++ software. Uses ``CMakeLists.txt`` files to define
      build configurations.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   CMakeLists.txt
      The configuration file used by CMake to define how a project should
      be built, including source files to compile and libraries to link.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Command Line Interface (CLI)
      A text-based interface for interacting with the operating system by
      typing commands. Linux shells provide a CLI.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Command Palette
      A searchable list of all available commands in Visual Studio Code,
      accessed via ``Ctrl + Shift + P``. Includes built-in commands and
      those from installed extensions.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Composition
      A strong "has-a" relationship where the part cannot exist without the whole. The whole manages the lifetime of its parts.
      :doc:`L9 </lectures/lecture9/l9_lecture>`

   Compiler
      A program that translates preprocessed C++ source code into
      machine code (object files). Part of the build process between
      preprocessing and linking.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Compound Statement
      A group of zero or more statements enclosed in braces ``{}``.
      Also called a block. No semicolon needed after the closing brace.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Configuration File (Shell)
      A script that runs automatically each time a new shell session
      starts. Used to define aliases, functions, and environment
      variables. Examples: ``.bashrc`` (Bash), ``.zshrc`` (Zsh),
      ``config.fish`` (Fish).
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Constructor
      A special member function automatically called when an object is created. Initializes the object's data members.
      :doc:`L8 </lectures/lecture8/l8_lecture>`

   Copy Elision
      A compiler optimization that eliminates unnecessary copy/move operations when returning objects from functions. Guaranteed in C++17 for certain cases (RVO).
      :doc:`L5 </lectures/lecture5/l5_lecture>`

   const
      A qualifier that makes a variable read-only after initialization.
      May be evaluated at compile-time or runtime depending on the
      initializer.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   constexpr
      A specifier that guarantees a variable or expression is evaluated
      at compile-time. Provides better optimization than ``const`` alone.
      :doc:`L2 </lectures/lecture2/l2_lecture>`


.. _g-d:

D
=

.. glossary::

   Dangling Pointer
      A pointer that points to a memory location that has been
      deallocated. Dereferencing a dangling pointer is undefined
      behavior. Avoid by setting pointers to ``nullptr`` after
      ``delete`` or by using smart pointers.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Default Parameter
      A value provided in a function declaration that is used when no argument is supplied for that parameter. Must be specified from right to left.
      :doc:`L5 </lectures/lecture5/l5_lecture>`

   delete
      An operator that deallocates memory previously allocated with
      ``new``. Does not destroy the pointer variable itself. Calling
      ``delete`` on a ``nullptr`` is safe. Only ``delete`` what you
      ``new``.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Dereference Operator
      The unary ``*`` operator used to access the value stored at the
      memory address held by a pointer. Also called the indirection
      operator.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Dynamic Memory Allocation
      Reserving memory on the heap at runtime using ``new``. The
      programmer is responsible for freeing this memory with ``delete``
      (or using smart pointers). Allocated objects have no identifier
      and never go out of scope on their own.
      :doc:`L3 </lectures/lecture3/l3_lecture>`


.. _g-e:

E
=

.. glossary::

   emplace_back
      A ``std::vector`` method that constructs an element in place at
      the end of the container, avoiding the creation of a temporary
      object. More efficient than ``push_back`` for complex types.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Encapsulation
      An OOP principle that bundles data and methods that operate on that data within a single class, restricting direct access to internal state.
      :doc:`L8 </lectures/lecture8/l8_lecture>`


.. _g-f:

F
=

.. glossary::

   Function (Shell)
      A reusable block of shell code that groups commands and can be
      executed by calling the function's name. Can accept arguments
      via positional parameters (``$1``, ``$2``, etc.).
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Function Overloading
      Defining multiple functions with the same name but different parameter lists. The compiler selects the correct overload based on the arguments.
      :doc:`L5 </lectures/lecture5/l5_lecture>`

   Function Pointer
      A variable that stores the address of a function. Used for callbacks and dynamic dispatch. Syntax: ``return_type (*name)(param_types)``.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Functor
      An object that can be called like a function by overloading the ``operator()``. Can maintain state between calls.
      :doc:`L6 </lectures/lecture6/l6_lecture>`


.. _g-h:

H
=

.. glossary::

   Heap
      A region of memory used for dynamic memory allocation at runtime.
      Memory on the heap persists until explicitly deallocated. Flexible
      in size but requires manual management (or smart pointers).
      :doc:`L3 </lectures/lecture3/l3_lecture>`


.. _g-i:

I
=

.. glossary::

   Implicit Type Conversion
      A type conversion performed automatically by the compiler when
      one data type is required but a different type is supplied.
      Does not change the original value or type.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Inheritance
      An OOP mechanism where a derived class acquires the properties and behaviors of a base class. Supports code reuse and hierarchical relationships.
      :doc:`L9 </lectures/lecture9/l9_lecture>`

   inline
      A specifier suggesting the compiler replace a function call with the function body. Required for functions defined in header files to satisfy the One Definition Rule.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Integral Type
      A C++ data type that represents whole numbers. Includes ``int``,
      ``char``, ``short``, ``long``, ``long long``, ``bool``, and
      their unsigned counterparts.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Iterator
      An object that facilitates traversal of a container. Behaves
      conceptually like a pointer. ``begin()`` returns the first
      position, ``end()`` returns past-the-end.
      :doc:`L4 </lectures/lecture4/l4_lecture>`


.. _g-k:

K
=

.. glossary::

   Ksh
      Korn Shell. A Unix shell with advanced scripting features,
      sometimes used in enterprise environments. Uses ``.kshrc`` as its
      configuration file.
      :doc:`L1 </lectures/lecture1/l1_lecture>`


.. _g-l:

L
=

.. glossary::

   Lambda
      An anonymous function object defined inline. Syntax: ``[capture](params) -> return_type { body }``. Can capture variables from the enclosing scope.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Linker
      A program that combines object files and libraries into a single
      executable program. Resolves dependencies and calculates memory
      addresses.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Local Scope
      The region within a pair of braces ``{}`` where a variable is
      accessible. Variables are destroyed when execution leaves the
      block.
      :doc:`L2 </lectures/lecture2/l2_lecture>`


.. _g-m:

M
=

.. glossary::

   Member Initialization List
      A constructor syntax that initializes data members before the constructor body executes. More efficient than assignment in the body. Required for ``const`` and reference members.
      :doc:`L8 </lectures/lecture8/l8_lecture>`

   Memory Leak
      Occurs when dynamically allocated memory is not freed. Reduces
      available memory and can cause performance degradation or crashes.
      Detected with tools like Valgrind.
      :doc:`L3 </lectures/lecture3/l3_lecture>`


.. _g-n:

N
=

.. glossary::

   Namespace
      A declarative region that provides a scope to identifiers inside
      it. Used to organize code and avoid naming collisions. The C++
      Standard Library uses the ``std`` namespace.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Narrowing Conversion
      A type conversion where data loss may occur (e.g., ``double`` to
      ``int``). Disallowed by uniform initialization. Use
      ``static_cast`` for explicit narrowing.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   new
      An operator that dynamically allocates memory on the heap at
      runtime and returns a pointer to the allocated memory. Must be
      paired with ``delete`` to avoid memory leaks.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   noexcept
      A specifier declaring that a function does not throw exceptions. Enables compiler optimizations and is checked at compile time for ``std::move`` operations.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   nullptr
      A keyword representing a null pointer literal. Preferred over
      ``NULL`` or ``0`` for initializing pointers that do not yet point
      to a valid object. Deleting a ``nullptr`` is safe.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Numeric Promotion
      The conversion of a smaller numeric type to a larger type within
      the same family. Always safe (no data loss). Examples:
      ``float`` to ``double``, ``char`` to ``int``.
      :doc:`L2 </lectures/lecture2/l2_lecture>`


.. _g-o:

O
=

.. glossary::

   Object
      An instance of a class. Contains its own copy of the class's data members and can call the class's methods.
      :doc:`L8 </lectures/lecture8/l8_lecture>`

   Overhead
      Additional resources (time, memory, bandwidth) required to
      perform a task beyond the minimum necessary. Understanding
      overhead helps in writing efficient code.
      :doc:`L4 </lectures/lecture4/l4_lecture>`


.. _g-p:

P
=

.. glossary::

   Pointer
      A variable that holds a memory address as its value. The address
      belongs to a variable, literal, or function. Declared with
      ``type* identifier;``. Must be initialized to avoid undefined
      behavior.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Polymorphism
      The ability to process objects differently based on their type. Compile-time (overloading) and runtime (virtual functions) forms exist in C++.
      :doc:`L9 </lectures/lecture9/l9_lecture>`

   Preprocessor
      The first stage of the C++ build process. Modifies source code
      before compilation by processing directives (``#include``,
      ``#define``, etc.), removing comments, and adjusting whitespace.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Pure Virtual Function
      A virtual function declared with ``= 0`` that has no implementation in the base class. Forces derived classes to provide their own implementation.
      :doc:`L9 </lectures/lecture9/l9_lecture>`


.. _g-r:

R
=

.. glossary::

   RAII
      Resource Acquisition Is Initialization. A C++ idiom where resource
      management (memory, file handles, etc.) is tied to object lifetime.
      Smart pointers implement RAII for dynamic memory.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Recursion
      A programming technique where a function calls itself to solve a problem by breaking it into smaller subproblems. Requires a base case to terminate.
      :doc:`L5 </lectures/lecture5/l5_lecture>`

   Reference
      An alias for an existing variable. Must be initialized at
      declaration, cannot be null, and cannot be reseated. Shares the
      same memory address as the original variable. Syntax:
      ``type& identifier{existing_variable};``
      :doc:`L3 </lectures/lecture3/l3_lecture>`


.. _g-s:

S
=

.. glossary::

   Scope
      The region of code where a variable can be accessed. Variables
      are *in scope* when accessible and *out of scope* when not.
      Scope is a compile-time property.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Shell
      A program that provides a command-line interface for users to
      interact with the operating system, allowing them to execute
      commands, run scripts, manage files, and control processes.
      Common shells include Bash, Zsh, Fish, Csh, and Ksh.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Small String Optimization (SSO)
      A std::string optimization where short strings (typically < 15-22
      characters) are stored directly inside the string object rather
      than on the heap, avoiding expensive dynamic allocation.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   sizeof
      A C++ operator that returns the size (in bytes) of a type or
      variable. The result is platform-dependent.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   static_cast
      A C++ cast operator used for explicit type conversions. Preferred
      over C-style casts for safe, intentional narrowing conversions.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Stack
      A region of memory used for automatic memory allocation. Local
      variables and function parameters are stored here. Memory is
      automatically deallocated when variables go out of scope. Fast
      but limited in size.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Statement
      A complete instruction that tells the computer to perform a
      specific action. Terminated by a semicolon (``;``) in C++.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Static Variable
      A local variable that retains its value between function calls. Initialized once and persists for the program's lifetime.
      :doc:`L5 </lectures/lecture5/l5_lecture>`

   std::array
      A fixed-size container from ``<array>`` that stores elements in
      contiguous memory. Size must be a compile-time constant. Provides
      ``.at()``, ``.size()``, ``.front()``, ``.back()``, and
      ``.fill()`` methods.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   std::function
      A general-purpose polymorphic function wrapper from ``<functional>``. Can store any callable (function, lambda, functor, function pointer) with a matching signature.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   std::string
      The standard C++ string class from ``<string>``. Manages a
      dynamic sequence of characters with automatic memory management.
      Supports SSO for short strings.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   STL Container
      A class template from the Standard Template Library that manages
      a collection of objects. Categories: sequence, associative,
      unordered associative, and container adapters.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Structured Binding
      A C++17 feature that allows unpacking a struct, pair, or tuple into individual named variables. Syntax: ``auto [x, y] = my_pair;``.
      :doc:`L6 </lectures/lecture6/l6_lecture>`


.. _g-t:

T
=

.. glossary::

   Template
      A mechanism for writing generic code that works with any data type. The compiler generates specific versions (instantiations) for each type used.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Template Specialization
      A mechanism to provide a custom implementation of a template for a specific type. Full specialization handles one specific type.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   this Pointer
      An implicit pointer available inside non-static member functions that points to the object on which the method was called.
      :doc:`L8 </lectures/lecture8/l8_lecture>`

   Type Deduction
      A C++ feature that allows the compiler to deduce the type of a
      variable from its initializer using the ``auto`` keyword.
      :doc:`L2 </lectures/lecture2/l2_lecture>`


.. _g-u:

U
=

.. glossary::

   Undefined Behavior
      The result of executing code that violates the C++ language rules.
      The program may produce correct results, incorrect results, crash,
      or behave erratically. Common examples: reading uninitialized
      variables, array out-of-bounds access, null pointer dereference.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Uniform Initialization
      The modern C++ initialization syntax using braces: ``int a{1};``.
      Prevents narrowing conversions and provides consistent syntax
      across all types. Preferred in this course.
      :doc:`L2 </lectures/lecture2/l2_lecture>`


.. _g-v:

V
=

.. glossary::

   Valgrind
      A programming tool for memory management, memory error detection,
      and profiling. Detects memory leaks, use-after-free, and other
      memory errors. Essential for C++ development with raw pointers.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Variable
      A symbolic name for a storage location that holds data. Has five
      characteristics: type, name (identifier), scope, lifetime, and
      value.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Virtual Destructor
      A destructor declared ``virtual`` to ensure proper cleanup when deleting a derived object through a base class pointer.
      :doc:`L9 </lectures/lecture9/l9_lecture>`

   Virtual Function
      A member function declared with the ``virtual`` keyword that enables runtime polymorphism. The correct function is called based on the actual object type, not the pointer/reference type.
      :doc:`L9 </lectures/lecture9/l9_lecture>`

   std::vector
      A dynamic array from ``<vector>`` whose size can change at
      runtime. The object variable lives on the stack; its contents
      are stored on the heap. Manages size and capacity separately.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Visual Studio Code
      A free, cross-platform code editor by Microsoft. Supports virtually
      every programming language through extensions. Used in this course
      for C++ and ROS 2 development.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Wild Pointer
      A pointer that has not been initialized to a known memory
      address. Holds a garbage value pointing to an unknown location.
      Dereferencing a wild pointer is undefined behavior.
      :doc:`L3 </lectures/lecture3/l3_lecture>`


.. _g-w:

W
=

.. glossary::

   Workspace
      In VSCode, a container that holds a set of related projects or code
      files. Workspace-specific settings are stored in the ``.vscode``
      folder and take precedence over user settings.
      :doc:`L1 </lectures/lecture1/l1_lecture>`


.. _g-z:

Z
=

.. glossary::

   Zsh
      Z Shell. A shell similar to Bash with additional features like
      improved autocompletion and customization. Uses ``.zshrc`` as its
      configuration file.
      :doc:`L1 </lectures/lecture1/l1_lecture>`
