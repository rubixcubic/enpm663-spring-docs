====================================================
Ubuntu Installation
====================================================

This course requires **Ubuntu Desktop 24.04 LTS** (Noble Numbat).
Ubuntu 22.04 LTS (Jammy Jellyfish) is also supported.


Installation Options
--------------------

.. grid:: 1 2 2 3
    :gutter: 3

    .. grid-item-card:: Dual Boot (Recommended)
        :class-card: sd-border-success

        Run Ubuntu alongside Windows on the same machine. You choose
        which OS to boot into at startup. This provides near-native
        performance while keeping your existing OS.

        Follow the official installation guide for your version:

        - `Install Ubuntu 24.04 LTS <https://ubuntu.com/tutorials/install-ubuntu-desktop>`_
        - `Install Ubuntu 22.04 LTS <https://ubuntu.com/tutorials/install-ubuntu-desktop-2204>`_

        .. warning::

           Back up your data before modifying disk partitions.

    .. grid-item-card:: Virtual Machine
        :class-card: sd-border-info

        Run Ubuntu inside a virtual machine on Windows or Mac. Easier
        to set up but slower performance.

        1. Install `VirtualBox <https://www.virtualbox.org/>`_ or
           `VMware Workstation Player <https://www.vmware.com/products/workstation-player.html>`_.
        2. Create a new VM with at least:

           - 4 GB RAM (8 GB recommended)
           - 50 GB disk space
           - 2 CPU cores

        3. Follow the official installation guide:

           - `Install Ubuntu 24.04 LTS <https://ubuntu.com/tutorials/install-ubuntu-desktop>`_
           - `Install Ubuntu 22.04 LTS <https://ubuntu.com/tutorials/install-ubuntu-desktop-2204>`_

        .. tip::

           Enable hardware virtualization (VT-x / AMD-V) in your BIOS
           for better VM performance.

    .. grid-item-card:: Native Install
        :class-card: sd-border-secondary

        Install Ubuntu as the **only** operating system on your machine.
        This provides the best performance but removes your existing OS.

        Only choose this option if you do not need Windows or macOS
        on this machine.

        - `Install Ubuntu 24.04 LTS <https://ubuntu.com/tutorials/install-ubuntu-desktop>`_
        - `Install Ubuntu 22.04 LTS <https://ubuntu.com/tutorials/install-ubuntu-desktop-2204>`_


.. note::

   **WSL 2** (Windows Subsystem for Linux) can run Ubuntu on Windows
   but has limitations with GUI applications and Gazebo. It is not
   recommended for this course unless you are experienced with it.


Post-Installation
-----------------

After installing Ubuntu, update your system:

.. code-block:: bash

   sudo apt update
   sudo apt upgrade -y

Install basic utilities:

.. code-block:: bash

   sudo apt install -y curl wget software-properties-common


Verify Your Installation
------------------------

Open a terminal (``Ctrl + Alt + T``) and check your Ubuntu version:

.. code-block:: bash

   lsb_release -a

You should see output similar to:

.. code-block:: text

   Distributor ID: Ubuntu
   Description:    Ubuntu 24.04 LTS
   Release:        24.04
   Codename:       noble
