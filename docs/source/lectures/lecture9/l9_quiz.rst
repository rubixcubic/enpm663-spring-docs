====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 9: OOP Advanced Topics.
Topics include class relationships (association, aggregation, composition),
inheritance (types, access specifiers, constructors), polymorphism
(compile-time and runtime), virtual methods and vtables, pure virtual
methods, abstract classes, virtual destructors, concrete classes, and the
``final`` keyword.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1--10)
====================================================

.. admonition:: Question 1
   :class: hint

   Which class relationship represents a strong "has-a" relationship where
   the contained object cannot exist independently of the container?

   A. Association

   B. Aggregation

   C. Composition

   D. Inheritance

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Composition

   In composition, the contained object is an integral part of the
   container. When the container is destroyed, all its parts are destroyed
   as well. For example, a ``Vehicle`` has ``Sensors`` -- if the vehicle is
   scrapped, its sensors are destroyed with it.


.. admonition:: Question 2
   :class: hint

   What is the default inheritance access type in C++ when no specifier is
   given?

   A. ``public``

   B. ``protected``

   C. ``private``

   D. ``friend``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``private``

   In C++, the default inheritance access type for classes is ``private``.
   This means that all ``public`` and ``protected`` members of the base
   class become ``private`` in the derived class.


.. admonition:: Question 3
   :class: hint

   Given the following code, what will be printed?

   .. code-block:: cpp

      class Base {
       public:
        virtual void speak() const { std::cout << "Base\n"; }
        virtual ~Base() = default;
      };

      class Derived : public Base {
       public:
        void speak() const override { std::cout << "Derived\n"; }
      };

      int main() {
          std::unique_ptr<Base> ptr = std::make_unique<Derived>();
          ptr->speak();
      }

   A. ``Base``

   B. ``Derived``

   C. Compile error

   D. Undefined behavior

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``Derived``

   Because ``speak()`` is declared ``virtual`` in the base class, C++ uses
   dynamic dispatch. The actual object type is ``Derived``, so
   ``Derived::speak()`` is called at runtime even though the pointer type
   is ``Base*``.


.. admonition:: Question 4
   :class: hint

   What mechanism does the C++ compiler use to implement runtime
   polymorphism?

   A. Template instantiation

   B. Function overloading resolution

   C. Virtual table (vtable) and dynamic dispatch

   D. Macro expansion

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Virtual table (vtable) and dynamic dispatch

   When a class has virtual methods, the compiler creates a vtable
   containing pointers to the actual implementations. Each object of that
   class contains a hidden pointer (vptr) to the vtable, enabling method
   calls to be resolved at runtime.


.. admonition:: Question 5
   :class: hint

   Which of the following correctly declares a pure virtual method?

   A. ``virtual void drive() = default;``

   B. ``virtual void drive() = 0;``

   C. ``void drive() = 0;``

   D. ``virtual void drive() override = 0;``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``virtual void drive() = 0;``

   A pure virtual method is declared with ``= 0`` after the function
   declaration. This makes the class abstract and requires derived classes
   to provide an implementation. Option C is wrong because pure virtual
   methods must be declared ``virtual``. Option A declares a defaulted
   virtual destructor/function, not a pure virtual.


.. admonition:: Question 6
   :class: hint

   A class has two pure virtual methods: ``drive()`` and ``stop()``. A
   derived class overrides only ``drive()``. What is the status of the
   derived class?

   A. It is a concrete class and can be instantiated.

   B. It is still abstract and cannot be instantiated.

   C. It causes a compile error in the base class.

   D. It causes undefined behavior.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It is still abstract and cannot be instantiated.

   A derived class must implement **all** pure virtual methods from the
   base class to become a concrete class. Since ``stop()`` was not
   overridden, the derived class is still abstract.


.. admonition:: Question 7
   :class: hint

   What happens when you delete a derived object through a base pointer
   that has a **non-virtual** destructor?

   A. Both destructors run correctly.

   B. Only the derived destructor runs.

   C. Undefined behavior -- only the base destructor runs, derived resources may leak.

   D. A compile error occurs.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Undefined behavior -- only the base destructor runs, derived
   resources may leak.

   Without a virtual destructor, the compiler uses static dispatch for
   the destructor call. Since the pointer type is ``Base*``, only
   ``~Base()`` runs. The derived class destructor never executes, which
   can cause resource leaks and undefined behavior.


.. admonition:: Question 8
   :class: hint

   Which relationship best describes "A ``Fleet`` contains ``Vehicles``,
   but if the ``Fleet`` is dissolved, the ``Vehicles`` continue to exist"?

   A. Association

   B. Aggregation

   C. Composition

   D. Inheritance

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Aggregation

   Aggregation represents a "has-a" relationship with weak ownership. The
   contained objects (``Vehicles``) can exist independently of the
   container (``Fleet``). This is the key difference from composition,
   where the parts are destroyed with the container.


.. admonition:: Question 9
   :class: hint

   What does the ``final`` keyword do when applied to a class?

   A. Makes all methods in the class ``virtual``.

   B. Prevents the class from being inherited by other classes.

   C. Makes the class abstract.

   D. Prevents all methods from being overridden.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Prevents the class from being inherited by other classes.

   When ``final`` is applied to a class (e.g., ``class RoboTaxi final : public Vehicle``),
   no other class can derive from it. Any attempt to inherit from a
   ``final`` class causes a compile error.


.. admonition:: Question 10
   :class: hint

   Which of the following is an example of compile-time polymorphism?

   A. Calling a ``virtual`` method through a base pointer

   B. Using dynamic dispatch via a vtable

   C. Method redefinition in a derived class called on a derived object directly

   D. Late binding

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Method redefinition in a derived class called on a derived
   object directly

   When you call a redefined method on a derived object directly (not
   through a base pointer/reference), the compiler resolves the call at
   compile time based on the static type. This is compile-time
   polymorphism (early binding). Options A, B, and D all describe runtime
   polymorphism.


----


True / False (Questions 11--15)
====================================================

.. admonition:: Question 11
   :class: hint

   **True or False:** In C++, ``private`` members of a base class are
   inherited by derived classes but are not accessible from the derived
   class.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   ``private`` members are inherited (they exist in the derived class
   object in memory), but they are hidden from the derived class. The
   derived class cannot access them directly. This is why the
   ``protected`` access specifier exists -- to allow derived classes to
   access base class members while keeping them hidden from external code.


.. admonition:: Question 12
   :class: hint

   **True or False:** You can instantiate an abstract class as long as
   you provide a constructor.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   An abstract class (one with at least one pure virtual method) cannot be
   instantiated regardless of whether it has a constructor. You must
   create a concrete derived class that implements all pure virtual methods
   before you can create objects.


.. admonition:: Question 13
   :class: hint

   **True or False:** The ``override`` keyword is required when overriding
   a virtual method in a derived class.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The ``override`` keyword is not *required* -- the code will compile
   and work correctly without it. However, it is a **best practice** to
   always use it because it provides compile-time safety: if the method
   signature does not match any virtual method in the base class, the
   compiler will report an error, catching typos and accidental hiding.


.. admonition:: Question 14
   :class: hint

   **True or False:** ``unique_ptr<Derived>`` is a subtype of
   ``unique_ptr<Base>`` because ``Derived`` is a subtype of ``Base``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Template instantiations do not inherit type relationships. Even though
   ``Derived*`` can be implicitly converted to ``Base*``,
   ``unique_ptr<Derived>`` is NOT a subtype of ``unique_ptr<Base>``. This
   is why storing ``auto``-typed smart pointers in containers of base
   pointers does not work directly. You must use explicit base type or
   direct insertion.


.. admonition:: Question 15
   :class: hint

   **True or False:** Applying ``final`` to a virtual method prevents it
   from being overridden in any further derived classes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   When ``final`` is applied to a virtual method (e.g.,
   ``virtual void move() final { ... }``), no derived class can override
   that method. Any attempt to do so causes a compile error. This is
   useful when you want to lock a specific behavior in the hierarchy.
