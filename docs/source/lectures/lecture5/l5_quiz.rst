.. _l5_quiz:

================
Lecture 5 Quiz
================

Multiple Choice
----------------

.. admonition:: Question 1
   :class: hint

   What is the difference between a function **declaration** and a function **definition**?

   A. A declaration includes the function body; a definition does not
   B. A definition includes the function body; a declaration only specifies the return type, name, and parameters
   C. A declaration and definition are the same thing
   D. A definition must appear before the declaration

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. A definition includes the function body; a declaration only specifies the return type, name, and parameters**

      A function declaration (prototype) tells the compiler the function's signature -- its return type, name, and parameter types. The definition provides the actual implementation (the body). The declaration is a "promise" that the function will be defined elsewhere.

.. admonition:: Question 2
   :class: hint

   What is the output of the following code?

   .. code-block:: cpp

      void modify(int x) {
          x = 100;
      }

      int main() {
          int val{42};
          modify(val);
          std::cout << val << '\n';
      }

   A. 100
   B. 42
   C. 0
   D. Undefined behavior

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. 42**

      The function ``modify`` takes its parameter by value, so it receives a copy of ``val``. Changing ``x`` inside the function does not affect the original ``val`` in ``main()``.

.. admonition:: Question 3
   :class: hint

   Which parameter-passing method should be your **default choice** for passing a large, read-only object like ``std::vector<int>``?

   A. Pass-by-value
   B. Pass-by-reference
   C. Pass-by-const-reference
   D. Pass-by-pointer

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. Pass-by-const-reference**

      ``const&`` provides efficiency (no copy) and safety (the function cannot modify the original). This is the recommended default for large objects that the function only needs to read.

.. admonition:: Question 4
   :class: hint

   What determines whether two functions are valid **overloads** of each other?

   A. They must have different return types
   B. They must have different parameter names
   C. They must have different parameter lists (number, types, or order of parameters)
   D. They must be in different source files

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. They must have different parameter lists (number, types, or order of parameters)**

      A function's signature for overloading purposes is its name plus its parameter types. The return type and parameter names are NOT part of the signature. Two functions with the same name and same parameter types but different return types will cause a compilation error.

.. admonition:: Question 5
   :class: hint

   What is wrong with the following code?

   .. code-block:: cpp

      void greet(const std::string& name, int times = 3);

      void greet(const std::string& name, int times = 3) {
          for (int i{0}; i < times; ++i) {
              std::cout << "Hello, " << name << "!\n";
          }
      }

   A. Default parameters cannot be used with references
   B. The default value is specified in both the declaration and the definition
   C. The function should return ``int``, not ``void``
   D. There is nothing wrong with this code

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. The default value is specified in both the declaration and the definition**

      Default parameter values should only be specified in the function declaration (typically in the header file), not repeated in the definition. Specifying them in both places causes a compilation error ("redefinition of default argument").

.. admonition:: Question 6
   :class: hint

   What is the output of the following code?

   .. code-block:: cpp

      void count_calls() {
          static int count{0};
          count++;
          std::cout << count << " ";
      }

      int main() {
          count_calls();
          count_calls();
          count_calls();
      }

   A. ``1 1 1``
   B. ``1 2 3``
   C. ``0 1 2``
   D. ``3 3 3``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. 1 2 3**

      A ``static`` local variable is initialized only once (the first time the function is called) and retains its value between calls. Each call increments the same ``count`` variable.

.. admonition:: Question 7
   :class: hint

   What is **copy elision** (specifically RVO)?

   A. The compiler copies the return value twice for safety
   B. The compiler constructs the return value directly at the destination, avoiding unnecessary copies
   C. The programmer must manually optimize return values
   D. The function returns a pointer instead of a value

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. The compiler constructs the return value directly at the destination, avoiding unnecessary copies**

      Copy elision, including Return Value Optimization (RVO), is a compiler optimization where the returned object is constructed directly in the memory of the variable that will receive it. Since C++17, RVO for unnamed temporaries (prvalues) is guaranteed by the standard.

.. admonition:: Question 8
   :class: hint

   What happens if a non-``void`` function does not have a ``return`` statement on all execution paths?

   A. The function returns 0 by default
   B. The function returns the last computed value
   C. It causes undefined behavior
   D. The compiler automatically adds a return statement

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. It causes undefined behavior**

      Every execution path in a non-``void`` function must end with a ``return`` statement. If control reaches the end of a non-``void`` function without encountering a ``return``, the behavior is undefined. The compiler may warn about this, but the code can still compile.

.. admonition:: Question 9
   :class: hint

   What does the call stack do when a function is called?

   A. It deletes the calling function's data
   B. It pushes a new stack frame onto the top of the stack
   C. It copies the entire program into memory
   D. It creates a new thread for the function

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. It pushes a new stack frame onto the top of the stack**

      When a function is called, a new stack frame containing the function's local variables, parameters, and return address is pushed onto the call stack. When the function returns, its stack frame is popped off.

.. admonition:: Question 10
   :class: hint

   Which of the following is a valid reason to pass by **pointer** instead of by **reference**?

   A. Pointers are always faster than references
   B. The argument could be optional (the function should handle ``nullptr``)
   C. Pointers provide read-only access
   D. References cannot be used with built-in types

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. The argument could be optional (the function should handle nullptr)**

      The key advantage of pass-by-pointer over pass-by-reference is that a pointer can be ``nullptr``, which allows the function to handle the case where no argument is provided. References must always refer to a valid object.

True or False
--------------

.. admonition:: Question 11
   :class: hint

   True or False: The return type of a function is part of its signature for overloading purposes.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False**

      A function's signature for overloading is defined by its name and its parameter types only. The return type is NOT considered. Two functions that differ only in return type will cause a compilation error, not a valid overload.

.. admonition:: Question 12
   :class: hint

   True or False: A ``static`` local variable can be accessed from outside the function in which it is defined.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False**

      A ``static`` local variable has the **lifetime** of the entire program but its **scope** is limited to the function in which it is defined. It cannot be accessed from outside that function.

.. admonition:: Question 13
   :class: hint

   True or False: Every recursive function must have a base case to prevent infinite recursion.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True**

      Without a base case, a recursive function will keep calling itself indefinitely, eventually consuming all available stack space and causing a stack overflow. The base case is the condition that stops the recursion.

.. admonition:: Question 14
   :class: hint

   True or False: In C++17, Return Value Optimization (RVO) for unnamed temporary objects is guaranteed by the standard.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True**

      Since C++17, RVO for prvalues (unnamed temporary return values) is mandatory -- the standard guarantees that no copy or move will occur. Named Return Value Optimization (NRVO), however, is still an optional optimization.

.. admonition:: Question 15
   :class: hint

   True or False: Default parameters must be specified starting from the **rightmost** parameter and must be contiguous.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True**

      Default parameters must be trailing parameters. You cannot have a default parameter followed by a non-default parameter. For example, ``void func(int a = 1, int b)`` is invalid, while ``void func(int a, int b = 1)`` is valid.
