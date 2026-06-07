.. _l8_quiz:

================
Lecture 8 Quiz
================

Multiple Choice
----------------

.. admonition:: Question 1
   :class: hint

   Which of the following is **not** a core principle of OOP?

   A. Encapsulation
   B. Abstraction
   C. Compilation
   D. Polymorphism

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. Compilation**

      The four core principles of OOP are encapsulation, abstraction, inheritance, and polymorphism. Compilation is a build process, not an OOP principle.

.. admonition:: Question 2
   :class: hint

   What is the relationship between a class and an object?

   A. A class is an instance of an object
   B. An object is a blueprint for a class
   C. A class is a blueprint; an object is an instance of that class
   D. They are the same thing

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. A class is a blueprint; an object is an instance of that class**

      A class defines the structure (attributes) and behavior (methods) that objects of that type will have. An object is a concrete instance created from the class blueprint, with its own unique state.

.. admonition:: Question 3
   :class: hint

   What is the default access specifier for members of a ``class`` in C++?

   A. ``public``
   B. ``private``
   C. ``protected``
   D. ``friend``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. private**

      If no access specifier is provided, C++ makes all class members ``private`` by default. This is different from a ``struct``, where the default is ``public``.

.. admonition:: Question 4
   :class: hint

   Which access specifier allows a member to be accessed by derived classes but not by external code?

   A. ``public``
   B. ``private``
   C. ``protected``
   D. ``static``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. protected**

      ``protected`` members cannot be accessed from outside the class but can be accessed by derived (child) classes. This is useful for inheritance hierarchies.

.. admonition:: Question 5
   :class: hint

   What will happen if you try to compile the following code?

   .. code-block:: cpp

      class Vehicle {
      private:
          std::string color_;
      public:
          Vehicle(const std::string& color) : color_{color} {}
      };

      int main() {
          Vehicle car;
      }

   A. It compiles and runs successfully
   B. Compilation error: no default constructor available
   C. Compilation error: ``color_`` is private
   D. Runtime error: uninitialized variable

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. Compilation error: no default constructor available**

      When you define any constructor (here, a parameterized one), the compiler no longer generates a default constructor. Since ``Vehicle car;`` requires a default constructor and none exists, the code fails to compile.

.. admonition:: Question 6
   :class: hint

   Why should accessors (getters) be declared ``const``?

   A. To make them run faster
   B. To guarantee they do not modify the object's state and to allow calling on ``const`` objects
   C. To prevent the function from being inlined
   D. To allow them to modify ``static`` members

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. To guarantee they do not modify the object's state and to allow calling on const objects**

      Declaring a method ``const`` creates a compile-time contract that the method will not modify any member variables. This also enables the method to be called on ``const`` objects, which can only invoke ``const`` methods.

.. admonition:: Question 7
   :class: hint

   What is the correct way to initialize a ``const`` member variable in a class?

   A. Assign it in the constructor body
   B. Use a member initializer list
   C. Use a setter method
   D. Declare it as ``static``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. Use a member initializer list**

      ``const`` members cannot be assigned after construction -- they must be initialized when created. The member initializer list runs before the constructor body, making it the only way to initialize ``const`` and reference members.

.. admonition:: Question 8
   :class: hint

   In which order are member variables initialized in C++?

   A. In the order they appear in the member initializer list
   B. In the order they are declared in the class definition
   C. In alphabetical order
   D. In reverse order of declaration

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. In the order they are declared in the class definition**

      Members are always initialized in declaration order, regardless of the order in the member initializer list. This can lead to subtle bugs if the initializer list order does not match the declaration order.

.. admonition:: Question 9
   :class: hint

   What does the ``this`` pointer refer to inside a member function?

   A. The class definition
   B. The most recently created object of the class
   C. The object on which the member function was called
   D. A copy of the current object

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. The object on which the member function was called**

      The ``this`` pointer is an implicit parameter passed to every non-static member function. It points to the specific object that invoked the method, allowing methods to access the correct object's data.

.. admonition:: Question 10
   :class: hint

   Which statement about ``static`` members is correct?

   A. A ``static`` method can access non-``static`` member variables directly
   B. A ``static`` attribute has a separate copy for each object
   C. A ``static`` method does not have a ``this`` pointer
   D. ``static`` members can only be accessed through an object, not through the class name

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. A static method does not have a this pointer**

      ``static`` methods belong to the class, not to any individual object, so they do not have a ``this`` pointer. Consequently, they cannot access non-``static`` members. ``static`` attributes are shared across all instances, and ``static`` methods can be called using the class name (e.g., ``Vehicle::get_vehicle_count()``).


True/False
-----------

.. admonition:: Question 11
   :class: hint

   True or False: Encapsulation means making all class members ``public`` so they can be easily accessed.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False**

      Encapsulation means restricting direct access to an object's internal data by making attributes ``private`` (or ``protected``) and providing controlled access through ``public`` methods (accessors and mutators). Making everything ``public`` breaks encapsulation.

.. admonition:: Question 12
   :class: hint

   True or False: A ``const`` object can only call methods that are marked ``const``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True**

      When an object is declared ``const``, its state cannot be modified. Therefore, only ``const`` methods -- which guarantee they do not modify the object -- can be called on it. Non-``const`` methods become inaccessible.

.. admonition:: Question 13
   :class: hint

   True or False: Member initializer lists are required for initializing ``const`` members and reference members.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True**

      ``const`` members and reference members must be initialized at the point of creation. Since the constructor body executes after member construction, assignment in the body is too late. The member initializer list is the only way to initialize these types of members.

.. admonition:: Question 14
   :class: hint

   True or False: Each object of a class gets its own copy of the class's methods (member functions).

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False**

      All objects of a class share the same method code. There is only one copy of each method in memory. The ``this`` pointer is how methods know which object's attributes to access when called on a specific object.

.. admonition:: Question 15
   :class: hint

   True or False: A ``static`` data member exists even if no objects of the class have been created.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True**

      A ``static`` data member belongs to the class itself, not to any individual object. It is allocated when the program starts (or when the class is first used, depending on the initialization) and exists independently of any object instances.
