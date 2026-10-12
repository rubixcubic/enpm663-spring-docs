====================================================
Code
====================================================

L5 has nine Python files and one shell script. Two files are modules the
others import: ``synth.py`` makes synthetic lidar scans of an ARIAC battery
cell, and ``detector.py`` is the lecture's eight-step defect detector. Six
scripts print the outputs shown in the :doc:`lecture notes <l5_lecture>`. One
of them, ``pc2_roundtrip.py``, uses ROS 2 Python packages (it builds a
``PointCloud2`` message and does a TF2 lookup), but it starts no node and
needs no simulator. ``mesh_depths.py`` reads ARIAC's own mesh files. The
outputs below come from running the scripts on 2026-10-12.

.. warning::

   **The data is synthetic.** Every point cloud and every voltage reading
   these scripts use is made in NumPy, not by ARIAC or Gazebo. Values taken
   from the ARIAC 2025 source are marked in the code with the file they come
   from. The only script that reads ARIAC data is ``mesh_depths.py``.

.. note::

   **What you need.** Ubuntu 24.04 with ROS 2 Jazzy, NumPy and PyYAML. The
   outputs come from these versions:

   .. literalinclude:: outputs/versions.txt
      :language: text

   On Ubuntu 24.04, ``sudo apt install python3-numpy python3-yaml`` installs
   NumPy and PyYAML for the system Python. Keep all ten files in one folder:
   the scripts import ``synth`` and ``detector`` from it.

   Open a terminal, source ROS 2 once, and go to the folder that holds the
   scripts:

   .. code-block:: bash

      source /opt/ros/jazzy/setup.bash
      cd lecture5/code

   Only ``pc2_roundtrip.py`` needs ROS 2. The other scripts run with plain
   ``python3`` whether ROS 2 is sourced or not.

   ``mesh_depths.py`` also needs the ARIAC 2025 source. Clone it once, for
   example into your home folder:

   .. code-block:: bash

      git clone -b ariac2025 https://github.com/usnistgov/ARIAC.git ~/ARIAC


.. list-table::
   :header-rows: 1
   :widths: 30 45 25
   :class: compact-table

   * - **File**
     - **What it does**
     - **Notes section**
   * - :download:`synth.py <code/synth.py>`
     - Module: synthetic scans of a cell, its defects and the lidars.
     - :ref:`l5-demo-setup`
   * - :download:`detector.py <code/detector.py>`
     - Module: the cylinder-fit detector, one function per step.
     - :ref:`l5-defects`
   * - :download:`pc2_roundtrip.py <code/pc2_roundtrip.py>`
     - Builds a ``PointCloud2``, reads it back, moves it to the world frame.
     - :ref:`l5-roundtrip`
   * - :download:`point_count.py <code/point_count.py>`
     - Counts the rays that hit a cell, for one scan and for a whole pass.
     - :ref:`l5-point-count`
   * - :download:`calibrate.py <code/calibrate.py>`
     - Sets the threshold from 20 good cells.
     - :ref:`l5-demo-setup`
   * - :download:`detect_one.py <code/detect_one.py>`
     - Runs the detector on one cell with a dent, a scratch and a bulge.
     - :ref:`l5-detect-one`
   * - :download:`precision_recall.py <code/precision_recall.py>`
     - Scores the detector on 200 cells, for two layouts and three
       thresholds.
     - :ref:`l5-pr-demo`
   * - :download:`voltage_average.py <code/voltage_average.py>`
     - Averages noisy voltage readings and skips invalid ones.
     - :ref:`l5-voltage`
   * - :download:`mesh_depths.py <code/mesh_depths.py>`
     - Measures the depth of ARIAC's training defects from the meshes.
     - :ref:`l5-mesh-depths`
   * - :download:`run_all.sh <code/run_all.sh>`
     - Runs all seven scripts and writes their outputs to ``../outputs/``.
     - See the last section


Synthetic Scans: ``synth.py``
-----------------------------

A module, not a script: the other files import it. It holds the cell
(radius 10.5 mm, length 70 mm), the belt (surface at :math:`z` = 0.422 m,
speed 0.1 m/s), the lidar range (0.04 to 0.2 m), the ``Lidar`` class, the
defect shapes, and the ray casting. ``two_lidars()`` places the two demo
lidars of the box figure (tag 8), at :math:`x` = 0.65 m, 0.1 m on each side of
the belt's center line. ``four_lidars()`` places two in each side box, turned
0.6 rad upstream and downstream. ``pass_cell()`` returns every world-frame
point of one cell passing the lidars, from 0 to 3 s after spawn, and the time
of the scan each point came from.

.. literalinclude:: code/synth.py
   :language: python
   :caption: synth.py


The Detector: ``detector.py``
-----------------------------

A module with one function per step of the detector: ``crop`` (step 1),
``undo_motion`` (step 3), ``fit_circle`` (step 4), ``residuals`` (step 5),
``clusters`` (step 7) and ``classify`` (step 8). ``detect`` runs them all,
and step 6 (threshold) is one line inside it. Step 2 (separate cells) has no
code: each synthetic run has one cell on the belt. Your GP2 node needs it.

.. literalinclude:: code/detector.py
   :language: python
   :caption: detector.py


PointCloud2 and TF2: ``pc2_roundtrip.py``
-----------------------------------------

Builds a ``PointCloud2`` from one synthetic scan of lidar A, reads it back into
NumPy, and moves the points to the world frame with a TF2 lookup. The static
transform is a stand-in for the one ARIAC publishes for each lidar. The script
needs ROS 2 sourced:

.. code-block:: bash

   python3 pc2_roundtrip.py

.. literalinclude:: code/pc2_roundtrip.py
   :language: python
   :caption: pc2_roundtrip.py

.. literalinclude:: outputs/pc2_roundtrip.txt
   :language: text


Counting Points: ``point_count.py``
-----------------------------------

First, one scan of each of three 400-sample layouts at a cell whose axis is
0.1 m in front of the lidar. Then the points of a whole pass, from the two
lidars and from the four. To try another layout, add a line to ``LAYOUTS``
(samples, minimum angle and maximum angle, for :math:`H` and then :math:`V`).

.. code-block:: bash

   python3 point_count.py

.. literalinclude:: code/point_count.py
   :language: python
   :caption: point_count.py

.. literalinclude:: outputs/point_count.txt
   :language: text


Setting the Threshold: ``calibrate.py``
---------------------------------------

Twenty good cells pass the two lidars, then twenty pass the four. For each
cell the script records the largest :math:`|d|`; the threshold is the largest
of these, rounded up to the next 0.1 mm. The range noise of 0.2 mm is chosen
for this example.

.. code-block:: bash

   python3 calibrate.py

.. literalinclude:: code/calibrate.py
   :language: python
   :caption: calibrate.py

.. literalinclude:: outputs/calibrate.txt
   :language: text


One Cell, Three Defects: ``detect_one.py``
------------------------------------------

One synthetic cell with a dent, a scratch and a bulge, each 2 mm deep, passes
the two lidars. The detector runs with the 0.9 mm threshold from
``calibrate.py`` and prints each step and what it found next to the truth.
With a file name as argument, the script also writes every point's
:math:`\theta`, :math:`z` and :math:`d` to that file; the residual map in the
notes is drawn from that file.

.. code-block:: bash

   python3 detect_one.py ../outputs/residuals.csv

.. literalinclude:: code/detect_one.py
   :language: python
   :caption: detect_one.py

.. literalinclude:: outputs/detect_one.txt
   :language: text

The residual file has one header line and one line per point
(:download:`residuals.csv <outputs/residuals.csv>`, 2862 points).


Precision and Recall: ``precision_recall.py``
---------------------------------------------

Set 1: 200 cells with defects 2 to 3 mm deep, scored with two lidars at three
thresholds and with four lidars at 0.9 mm. Set 2: 200 new cells with defects
0.8 to 2.5 mm deep, scored with four lidars at 0.9 mm. Each cell is defective
with probability 0.25. All random numbers come from one generator with a fixed
seed, so the output is the same on every run. Changing a threshold value does
not change the cells or the noise; adding or removing a run does. The script
casts every ray of 1000 cell passes, so it is slow: 252 s on the instructor's
PC (Intel Core i9-14900HX, 2026-10-12). ``calibrate.py`` took 9 s, and
``detect_one.py`` and ``point_count.py`` under 1 s each.

.. code-block:: bash

   python3 precision_recall.py

.. literalinclude:: code/precision_recall.py
   :language: python
   :caption: precision_recall.py

.. literalinclude:: outputs/precision_recall.txt
   :language: text


Voltage Readings: ``voltage_average.py``
----------------------------------------

Part 1 draws 100000 single readings and 100000 averages of 10 for a cell at
3.78 V and counts how often each lands above 3.8 V. Part 2 builds a stream of
17 readings from one tester (2 with no cell, 6 good, 3 during a malfunction, 6
good), keeps the valid ones, and averages the last 10.

.. code-block:: bash

   python3 voltage_average.py

.. literalinclude:: code/voltage_average.py
   :language: python
   :caption: voltage_average.py

.. literalinclude:: outputs/voltage_average.txt
   :language: text


Defect Depths in ARIAC's Meshes: ``mesh_depths.py``
---------------------------------------------------

Reads the li-ion cell meshes (``ariac_gz/models/battery_cell/meshes/li-ion``)
and ``ariac_setup/config/defects.yaml`` from the ARIAC 2025 source. Give it the
folder you cloned:

.. code-block:: bash

   python3 mesh_depths.py ~/ARIAC

.. literalinclude:: code/mesh_depths.py
   :language: python
   :caption: mesh_depths.py

.. literalinclude:: outputs/mesh_depths.txt
   :language: text

The output was measured on the ``ariac2025`` branch at commit ``0c3e722``
(2026-02-25), the branch's latest commit on 2026-10-12. If NIST changes the
meshes, the numbers change.


Run Everything: ``run_all.sh``
------------------------------

``run_all.sh`` runs every script and writes each output to ``../outputs/``. It
is how the outputs on this page were made. It needs ``ARIAC_SRC`` set to your
ARIAC source folder:

.. code-block:: bash

   ARIAC_SRC=~/ARIAC bash run_all.sh

It starts each script with ``env -i`` and runs ``pc2_roundtrip.py`` with
``ROS_DOMAIN_ID=85``, which keeps the course machine's other Python and ROS
settings out. On your machine, the plain commands above do the same job.

.. literalinclude:: code/run_all.sh
   :language: bash
   :caption: run_all.sh
