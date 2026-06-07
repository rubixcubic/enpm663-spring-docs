====================================================
Git/Github Exercises
====================================================


.. dropdown:: Exercise 1 -- Git Basics
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Practice the fundamental Git workflow: initialize a repository, add
   files, and make commits.

   1. Create a new directory called ``robot-project`` and initialize a
      Git repository inside it.
   2. Create a file called ``robot_config.yaml`` with some content.
   3. Stage the file and make your first commit.
   4. Modify the file by adding a new line.
   5. Check the status, view the diff, stage, and commit again.
   6. View the commit log.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         # Step 1: Create directory and initialize repo
         mkdir robot-project
         cd robot-project
         git init

         # Step 2: Create a file
         echo "robot_name: delivery_bot" > robot_config.yaml

         # Step 3: Stage and commit
         git add robot_config.yaml
         git commit -m "Initial commit: Add robot configuration"

         # Step 4: Modify the file
         echo "max_speed: 2.0" >> robot_config.yaml

         # Step 5: Check status, diff, stage, and commit
         git status
         git diff
         git add robot_config.yaml
         git commit -m "Add max speed to robot configuration"

         # Step 6: View log
         git log --oneline


.. dropdown:: Exercise 2 -- Branching
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Practice creating branches and switching between them.

   1. Starting from the repository created in Exercise 1, create a new
      branch called ``feature/sensor-config``.
   2. Switch to the new branch.
   3. Add a file called ``sensor_config.yaml`` with some sensor settings.
   4. Stage and commit the new file.
   5. Switch back to ``main`` and verify that ``sensor_config.yaml`` does
      not exist on ``main``.
   6. List all branches and view the log with ``--all --graph``.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         # Step 1-2: Create and switch to new branch
         git checkout -b feature/sensor-config

         # Step 3: Add a new file
         echo "lidar_range: 30.0" > sensor_config.yaml

         # Step 4: Stage and commit
         git add sensor_config.yaml
         git commit -m "Add sensor configuration file"

         # Step 5: Switch back to main and verify
         git checkout main
         ls sensor_config.yaml  # Should show: No such file or directory

         # Step 6: List branches and view log
         git branch
         git log --oneline --all --graph


.. dropdown:: Exercise 3 -- Merging
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Practice merging a feature branch into ``main``.

   1. Ensure you are on the ``main`` branch.
   2. Merge the ``feature/sensor-config`` branch into ``main``.
   3. Verify that ``sensor_config.yaml`` now exists on ``main``.
   4. View the log to see the merge.
   5. Delete the ``feature/sensor-config`` branch.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         # Step 1: Ensure on main
         git checkout main

         # Step 2: Merge the feature branch
         git merge feature/sensor-config

         # Step 3: Verify the file exists
         ls sensor_config.yaml
         cat sensor_config.yaml

         # Step 4: View the log
         git log --oneline --all --graph

         # Step 5: Delete the feature branch
         git branch -d feature/sensor-config


.. dropdown:: Exercise 4 -- Merge Conflict Resolution
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Intentionally create a merge conflict and resolve it.

   1. Create a new branch called ``feature/speed-update`` and switch to
      it.
   2. In ``robot_config.yaml``, change the ``max_speed`` value to
      ``3.0``. Stage and commit.
   3. Switch back to ``main``.
   4. On ``main``, change the ``max_speed`` value to ``1.5``. Stage and
      commit.
   5. Attempt to merge ``feature/speed-update`` into ``main``. This
      should produce a conflict.
   6. Open ``robot_config.yaml``, resolve the conflict by choosing an
      appropriate value, and remove all conflict markers.
   7. Stage the resolved file and complete the merge with a commit.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         # Step 1: Create and switch to branch
         git checkout -b feature/speed-update

         # Step 2: Edit max_speed to 3.0, then stage and commit
         # (edit robot_config.yaml so max_speed: 3.0)
         git add robot_config.yaml
         git commit -m "Increase max speed to 3.0"

         # Step 3: Switch back to main
         git checkout main

         # Step 4: Edit max_speed to 1.5 on main, stage and commit
         # (edit robot_config.yaml so max_speed: 1.5)
         git add robot_config.yaml
         git commit -m "Decrease max speed to 1.5 for safety"

         # Step 5: Merge -- this will conflict
         git merge feature/speed-update
         # CONFLICT (content): Merge conflict in robot_config.yaml

         # Step 6: Open the file and resolve the conflict
         # Remove <<<<<<< HEAD, =======, >>>>>>> markers
         # Choose the appropriate value (e.g., max_speed: 2.5)

         # Step 7: Stage and commit
         git add robot_config.yaml
         git commit -m "Merge feature/speed-update: set max speed to 2.5

         Resolved conflict between 1.5 (safety) and 3.0 (performance)."


.. dropdown:: Exercise 5 -- GitHub Remote
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Practice pushing to a remote repository and cloning.

   1. Create an empty repository on GitHub called ``robot-project``
      (do not add a README, .gitignore, or license).
   2. Add the GitHub repository as a remote named ``origin``.
   3. Push your local ``main`` branch to GitHub.
   4. Verify the push by checking GitHub in your browser.
   5. In a separate directory, clone the repository.
   6. In the cloned repo, make a change, commit, and push.
   7. In the original repo, pull the latest changes.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         # Step 1: Create repo on GitHub (do this in the browser)

         # Step 2: Add remote
         git remote add origin git@github.com:yourusername/robot-project.git
         git remote -v

         # Step 3: Push to GitHub
         git push -u origin main

         # Step 4: Verify on GitHub (browser)

         # Step 5: Clone in a separate directory
         cd /tmp
         git clone git@github.com:yourusername/robot-project.git robot-project-clone
         cd robot-project-clone

         # Step 6: Make a change, commit, and push
         echo "battery_capacity: 5000" >> robot_config.yaml
         git add robot_config.yaml
         git commit -m "Add battery capacity to configuration"
         git push origin main

         # Step 7: Pull changes in original repo
         cd ~/robot-project
         git pull origin main


.. dropdown:: Exercise 6 -- Challenge: Fork Workflow
   :icon: gear
   :class-container: sd-border-warning
   :class-title: sd-font-weight-bold

   Practice the complete fork workflow used in open source and in this
   course.

   1. Fork a classmate's repository (or use a public test repository)
      on GitHub.
   2. Clone **your fork** to your local machine.
   3. Add the original repository as an ``upstream`` remote.
   4. Create a feature branch called ``feature/add-readme-section``.
   5. Make changes (e.g., add a section to the README).
   6. Commit and push the feature branch to **your fork** (``origin``).
   7. On GitHub, create a Pull Request from your fork's feature branch
      to the original repository's ``main`` branch.
   8. After the PR is merged (or for practice), sync your fork:

      - Fetch from ``upstream``.
      - Merge ``upstream/main`` into your local ``main``.
      - Push the updated ``main`` to your fork.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         # Step 1: Fork on GitHub (do this in the browser)

         # Step 2: Clone your fork
         git clone git@github.com:yourusername/original-project.git
         cd original-project

         # Step 3: Add upstream remote
         git remote add upstream https://github.com/original-owner/original-project.git
         git remote -v
         # origin    git@github.com:yourusername/original-project.git (fetch)
         # origin    git@github.com:yourusername/original-project.git (push)
         # upstream  https://github.com/original-owner/original-project.git (fetch)
         # upstream  https://github.com/original-owner/original-project.git (push)

         # Step 4: Create feature branch
         git checkout -b feature/add-readme-section

         # Step 5: Make changes
         echo "## New Section" >> README.md
         echo "Added by contributor." >> README.md

         # Step 6: Commit and push to your fork
         git add README.md
         git commit -m "Add new section to README"
         git push origin feature/add-readme-section

         # Step 7: Create PR on GitHub (do this in the browser)
         # Go to your fork -> Compare & pull request

         # Step 8: Sync your fork after merge
         git checkout main
         git fetch upstream
         git merge upstream/main
         git push origin main
