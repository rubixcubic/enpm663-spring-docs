References
==========


.. dropdown:: Lecture 9
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM702 -- L9: OOP Advanced Topics**

        Covers advanced object-oriented programming in C++: class
        relationships (association, aggregation, composition, inheritance),
        inheritance types (single and multiple), generalization vs.
        specialization, inheritance access types, and constructor chaining.
        Polymorphism is covered in depth -- compile-time (method
        redefinition, function overloading) and runtime (``virtual``
        methods, dynamic dispatch, vtables). The lecture also covers the
        ``override`` keyword, ``auto`` vs. explicit base types for
        polymorphic objects, the container problem with ``auto``, object
        slicing, virtual destructors, the ``= default`` keyword,
        abstraction with pure virtual methods (``= 0``), abstract vs.
        concrete classes, and the ``final`` keyword for preventing
        inheritance and method overriding.

        **Before next class**: complete the shell exercises (final set
        before ROS 2), the C++ exercises on inheritance and polymorphism,
        and the quiz. Ensure your ROS 2 installation is complete.


.. dropdown:: cppreference -- Inheritance and Virtual Functions
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Inheritance
            :link: https://en.cppreference.com/w/cpp/language/derived_class
            :class-card: sd-border-secondary

            **cppreference -- Derived Classes**

            Complete reference for class inheritance in C++ including access
            specifiers, base class initialization, member access rules, and
            the interaction between base and derived class constructors.

            +++

            - Public, protected, and private inheritance
            - Base class member accessibility
            - Constructor and destructor ordering
            - Multiple inheritance and virtual base classes

        .. grid-item-card:: Virtual Functions
            :link: https://en.cppreference.com/w/cpp/language/virtual
            :class-card: sd-border-secondary

            **cppreference -- Virtual Functions**

            Reference for ``virtual`` method declarations, dynamic dispatch,
            vtable mechanics, and the ``override`` and ``final`` specifiers.

            +++

            - ``virtual`` keyword semantics
            - Dynamic dispatch and vtable
            - ``override`` specifier
            - ``final`` specifier
            - Covariant return types

        .. grid-item-card:: Abstract Classes
            :link: https://en.cppreference.com/w/cpp/language/abstract_class
            :class-card: sd-border-secondary

            **cppreference -- Abstract Classes**

            Reference for pure virtual functions (``= 0``), abstract class
            rules, and their role in defining interfaces and contracts.

            +++

            - Pure virtual function declaration
            - Abstract class instantiation rules
            - Concrete class requirements
            - Interface design patterns

        .. grid-item-card:: Destructors
            :link: https://en.cppreference.com/w/cpp/language/destructor
            :class-card: sd-border-secondary

            **cppreference -- Destructors**

            Complete reference for destructor semantics, virtual
            destructors, destruction order, and the ``= default`` keyword
            for compiler-generated destructors.

            +++

            - Destructor declaration and definition
            - Virtual destructors for polymorphic bases
            - Destruction order (derived before base)
            - ``= default`` and ``= delete``
            - RAII and resource management
