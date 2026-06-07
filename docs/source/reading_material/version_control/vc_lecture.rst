====================================================
Lecture
====================================================


Learning Objectives
====================================================

By the end of this session, you will be able to:

- Set up and configure Git for any project.
- Create repositories and track changes effectively.
- Use branching for feature development and hotfixes.
- Collaborate using GitHub and pull requests.
- Apply version control best practices to team projects.


Version Control
====================================================

Version control is a system that tracks changes to files over time,
allowing you to:

- **Track History**: See exactly what changed, when, and who made the
  change.
- **Revert Changes**: Go back to any previous version of your files.
- **Branch and Merge**: Work on different features simultaneously
  without conflicts.
- **Collaborate**: Multiple people can work on the same project without
  overwriting each other's work.
- **Backup**: Distributed copies serve as automatic backups.


Without Version Control
----------------------------------------------------

A typical project directory without version control might look like
this:

::

   my_project/
       final_version.doc
       final_version_v2.doc
       final_version_REALLY_FINAL.doc
       final_version_REALLY_FINAL_fixed.doc
       final_version_REALLY_FINAL_fixed_john_edits.doc


With Version Control
----------------------------------------------------

With version control, the same project looks like this:

::

   my_project/
       document.doc
       .git/        (tracks all versions automatically)

- ``document.doc`` has complete history.
- ``.git/`` tracks all versions automatically.


Types of Version Control Systems
----------------------------------------------------

1. **Local Version Control:**

   - Copies files to different directories.
   - Simple but error-prone.
   - *Example*: RCS (Revision Control System)

2. **Centralized Version Control:**

   - Single server contains all versions.
   - Clients check out files from central place.
   - *Examples*: CVS, Subversion (SVN), Perforce.

3. **Distributed Version Control:**

   - Every client has complete repository copy.
   - No single point of failure.
   - *Examples*: Git, Mercurial, Bazaar.


Centralized Version Control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/vc/centralized.pdf
   :align: center
   :width: 60%

   Centralized version control architecture.

- **Single source of truth**: Central server has master repository.
- **Client-server model**: Developers have working copies only.
- **Network dependent**: Most operations require server connection.

**Typical Workflow:**

.. code-block:: bash

   # SVN Example
   svn checkout https://server.com/repo/trunk # Get working copy
   svn update                                 # Get latest changes
   # Make changes...
   svn commit -m "My changes"                 # Save to server
   svn log                                    # View history (needs network)

.. grid:: 2

   .. grid-item-card:: Advantages

      - Simple mental model -- one central authority
      - Fine-grained access control
      - Storage efficient for clients
      - Easy administration and compliance

   .. grid-item-card:: Disadvantages

      - Single point of failure
      - Network required for most operations
      - Limited offline capabilities
      - Expensive branching operations


Distributed Version Control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/vc/distributed.pdf
   :align: center
   :width: 60%

   Distributed version control architecture.

- **Complete local repositories**: Full history everywhere.
- **Peer-to-peer model**: Repositories sync with any other.
- **Offline capable**: All operations work without network.

**Typical Workflow:**

.. code-block:: bash

   # Git Example
   git clone https://github.com/user/project.git   # Get complete repo
   git log                                         # View history (offline)
   git branch feature                              # Create branch (instant)
   git checkout feature                            # Switch branch (instant)
   # Make changes...
   git commit -m "My changes"                      # Save locally
   git push origin feature                         # Share when ready

.. grid:: 2

   .. grid-item-card:: Advantages

      - No single point of failure
      - Fast local operations
      - Excellent offline capabilities
      - Flexible workflows
      - Cheap branching and merging

   .. grid-item-card:: Disadvantages

      - Steeper learning curve
      - More complex concepts
      - Larger local storage requirements
      - Less granular access control


Git
====================================================

Git is a version control system that tracks changes in your files over
time.

- Save snapshots of your project at different points.
- See what changed between versions.
- Collaborate with others without overwriting each other's work.
- Revert to previous versions if something breaks.

**Setup:**

.. code-block:: bash

   # Installation
   sudo apt update && sudo apt install git

   # Configure Git
   git config --global user.name "Your Full Name"
   git config --global user.email "your.email@university.edu"

   # Check
   git config --list


Why Git Dominates
----------------------------------------------------

.. grid:: 2

   .. grid-item-card:: Technical Advantages

      - **Speed** -- Operations like commits and diffs execute in
        milliseconds.
      - **Distributed Nature** -- Every developer has a complete copy of
        the project history.
      - **Branching Model** -- Creating and merging branches is
        lightweight and fast.
      - **Data Integrity** -- SHA-1 checksums ensure your code history
        cannot be corrupted.

   .. grid-item-card:: Ecosystem Advantages

      - **GitHub Integration** -- Seamless hosting with powerful
        collaboration features.
      - **Tool Support** -- Every major IDE and editor has excellent Git
        integration.
      - **Industry Adoption** -- Used by virtually all major tech
        companies and open source projects.


Common Git Commands
----------------------------------------------------

.. grid:: 2

   .. grid-item-card:: Daily Commands

      .. code-block:: bash

         git status              # Check status
         git add .               # Stage changes
         git commit -m "msg"     # Commit changes
         git push                # Upload to GitHub
         git pull                # Download updates

   .. grid-item-card:: Branching Commands

      .. code-block:: bash

         git branch          # List branches
         git checkout -b new # Create & switch
         git merge branch    # Merge branch
         git branch -d old   # Delete branch

.. note::

   Multiple Git cheat sheets are available on Canvas.


Example: A Day in the Life of a Robotics Engineer
----------------------------------------------------

.. admonition:: Scenario
   :class: note

   To illustrate how these concepts work in practice, we will walk
   through a realistic, day-long scenario. You will take on the role of
   a robotics engineer at ENPM702Tech Labs.

   Throughout the day, you will use Git to:

   - Initialize a new project for an autonomous robot's configuration.
   - Use branching to develop a new feature (GPS navigation).
   - Handle a critical hotfix for a performance bug.
   - Navigate and resolve a merge conflict that arises from these
     parallel lines of work.


Setting Up the Project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. card::
   :class-header: sd-bg-dark-orange sd-text-white

   Monday Morning -- Setting Up the Project
   ^^^

   You begin your week by creating the baseline configuration for a new
   autonomous delivery robot platform.

1. **Create a new project directory.**

   .. code-block:: bash

      # Create a new project directory
      mkdir robot-config   # note kebab-case

2. **Initialize version control.**

   .. code-block:: bash

      cd robot-config
      git init

   ``git init`` creates a new Git repository in your current directory.

   - Creates the ``.git`` directory: This hidden folder contains all of
     Git's internal files and metadata for the repository, including the
     object database, configuration files, and references.
   - Initializes an empty repository: The repository starts with no
     commits, branches, or tracked files. It is essentially a *blank
     slate* ready for you to start adding content.
   - Sets up the default branch: Modern Git versions create a default
     branch.

   .. admonition:: What is the default branch?
      :class: note

      Think of the default branch as the official, stable version of
      your project, like the **master copy** of a document that everyone
      refers to. The default branch is usually called ``master`` or
      ``main``.

   .. note::

      GitHub and many organizations switched from ``master`` to ``main``
      for inclusive language reasons. Git itself updated to allow
      configurable default branch names.

3. **Create the files you need to track in the current folder.**

   - ``robot_config.yaml`` -- Configuration file for autonomous delivery
     robot.
   - ``README.md`` -- File that serves as the front door for anyone
     encountering a project for the first time.
   - ``.gitignore`` -- File that tells Git which files and folders to
     ignore when tracking changes.

   .. code-block:: bash

      git status

.. dropdown:: Why Use ``.gitignore``?
   :class-container: sd-border-info

   Avoid tracking files that:

   - Are generated automatically (build artifacts, compiled code).
   - Contain sensitive information (passwords, API keys).
   - Are user-specific (IDE settings, OS files).
   - Are too large or binary (datasets, videos, executables).
   - Change frequently but are not important (log files, cache).

   **Common .gitignore Patterns:**

   .. code-block:: bash

      # Compiled code and build artifacts
      *.o
      *.so
      *.exe
      build/
      dist/
      target/

      # IDE and editor files
      .vscode/

      # Operating system files
      .DS_Store        # macOS
      Thumbs.db        # Windows
      *.tmp

      # Configuration with secrets
      robot_secrets.yaml
      wifi_passwords.txt

   .. admonition:: Best Practices
      :class: tip

      - **Create early**: Add ``.gitignore`` before making your first
        commit.
      - **Already tracked files**: ``.gitignore`` will not affect files
        already being tracked.
      - **Remove tracked files**: Use ``git rm --cached filename`` to
        stop tracking.

        .. code-block:: bash

           # Remove file from tracking but keep locally
           git rm --cached sensitive_config.yaml

4. **Stage the files.**

   .. code-block:: bash

      git add .

   Staging puts your changes in a **draft box** called the *staging
   area*. You are preparing what you want to include in your next save
   point, but you have not saved it yet.

   - *Analogy*: Drafting an email -- your email is ready to be sent but
     not sent yet.

5. **Commit changes.**

   .. code-block:: bash

      git commit -m "Initial commit: Add basic robot configuration

      - Add robot_config.yaml with hardware and navigation settings
      - Add README.md with project description
      - Add .gitignore"

   Committing takes everything from your staging area (draft box) and
   creates a permanent save point in your project's history.

   - *Analogy*: Sending an email -- it is now permanently sent and
     becomes part of your email history.

   .. admonition:: Best Practice
      :class: tip

      Write detailed commit messages.

6. **Verify the commit.**

   .. code-block:: bash

      git log --oneline --graph

   You can pass other options to ``git log``. Run ``git log --help`` to
   get more information.

   .. note::

      Open the folder ``robot-config`` in VS Code and use the Git Graph
      extension to visualize branches and commits.


Adding GPS Navigation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. card::
   :class-header: sd-bg-dark-orange sd-text-white

   Feature Development -- Adding GPS Navigation
   ^^^

   **10:00 AM** -- You receive a task to add GPS navigation capabilities
   to the robot.

1. **Create a feature branch for GPS navigation.**

   .. code-block:: bash

      git checkout -b feature/gps-navigation

   - ``git checkout`` = "Switch to a branch"
   - ``-b`` = "But first, create a new branch from wherever you are
     right now"
   - **Combined:** "Create a new branch AND switch to it immediately"
   - ``feature/`` is a naming convention (like organizing folders).
   - ``gps-navigation`` describes what this branch is for.

   **Long way (two separate commands):**

   .. code-block:: bash

      git branch feature/gps-navigation     # Create the branch
      git checkout feature/gps-navigation   # Switch to it

   .. note::

      When you use ``git checkout -b <new-branch-name>``, the new
      branch is created from the current branch you are on. For
      instance, to create ``feature/gps-navigation`` from ``main``:

      .. code-block:: bash

         git checkout main                        # Switch to main
         git checkout -b feature/gps-navigation   # Create and switch

      Alternative:
      ``git checkout -b feature/gps-navigation main``

2. **Check you are on the current branch.**

   .. code-block:: bash

      git branch

      # output
      * feature/gps-navigation
        main

3. **Modify robot_config.yaml for GPS Feature.**

   - Implement GPS feature in ``robot_config.yaml``.
   - Fix any typos.

4. **Check what changed.**

   .. code-block:: bash

      git diff

   ``git diff`` shows changes between your working directory (current
   files) and the staging area (what is ready to commit).

5. **Stage and commit the changes.**

   .. code-block:: bash

      git add robot_config.yaml

      git commit -m "Feature: Add GPS navigation capabilities to the robot"

      # Check commit history or use Git Graph
      git log --oneline --all --graph


Bug Alert -- Emergency Fix Needed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. card::
   :class-header: sd-bg-dark-orange sd-text-white

   Emergency Fix Needed
   ^^^

   **11:30 AM** -- You get an urgent message: the robot's overall
   responsiveness is sluggish! The default navigation ``update_rate`` of
   5Hz is too slow for real-time obstacle avoidance.

   .. warning::

      This is a critical issue. You must fix this on ``main``
      immediately.

1. Check what we are working on: ``git status``

   .. code-block:: bash

      # On branch feature/gps-navigation
      # nothing to commit, working tree clean

   Your GPS work is safe on its own branch. You can switch away without
   losing anything.

2. **Create and switch to the new branch.** The fix needs to be based
   on the official ``main`` branch, not your
   ``feature/gps-navigation`` branch.

   .. code-block:: bash

      git checkout main                         # switch to main
      git checkout -b hotfix/fix-navigation-rate

   Or, more concisely:
   ``git checkout -b hotfix/fix-navigation-rate main``

3. **Increase navigation update_rate to 10Hz.** Change the
   ``update_rate`` in ``robot_config.yaml`` from 5Hz to 10Hz.

4. **Check the changes:** ``git diff``

5. **Stage and commit.**

   .. code-block:: bash

      git add robot_config.yaml
      git commit -m "HOTFIX: Increase navigation update rate to 10Hz

      - Critical performance fix to improve robot responsiveness.
      - Increases the navigation update rate from 5Hz to 10Hz."

6. **Merge hotfix back to main.**

   .. code-block:: bash

      git checkout main                        # switch to main
      git merge hotfix/fix-navigation-rate

   a. Go to the ``main`` version of the project.
   b. Apply all the changes made on the
      ``hotfix/fix-navigation-rate`` branch into this ``main`` branch.

7. **Clean up the hotfix branch:**
   ``git branch -d hotfix/fix-navigation-rate``

8. **Check current state:**
   ``git log --oneline --all --graph``


Handling Merge Conflicts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. card::
   :class-header: sd-bg-dark-orange sd-text-white

   Handling Merge Conflicts
   ^^^

   **12:30 PM** -- After the hotfix is deployed, you return to your GPS
   feature. To stay up-to-date, you must merge the changes from ``main``
   into your feature branch.

1. **Switch back to the GPS feature branch:**
   ``git checkout feature/gps-navigation``

2. **Attempt the merge:** ``git merge main``

   .. code-block:: bash

      # Auto-merging robot_config.yaml
      # CONFLICT (content): Merge conflict in robot_config.yaml
      # Automatic merge failed; fix conflicts and then commit the result.

3. **Check the conflict status:** ``git status``

   .. code-block:: bash

      # On branch feature/gps-navigation
      # You have unmerged paths.
      #   (fix conflicts and run "git commit")
      #   (use "git merge --abort" to abort the merge)
      #
      # Unmerged paths:
      #   (use "git add <file>..." to mark resolution)
      #   both modified:    robot_config.yaml

.. warning::

   We have a **Merge Conflict** because both branches modified the same
   line in ``robot_config.yaml``. Instead of guessing, Git pauses the
   merge and inserts conflict markers into the file, asking you to
   resolve the situation manually.

.. code-block:: text

   navigation:
     # General navigation settings for the robot
   <<<<<<< HEAD
     update_rate: 5  # Hz. Lowered from 10 to 5 for GPS stability.
   =======
     update_rate: 20  # Hz. Increased from 10 to 20 for responsiveness.
   >>>>>>> main
     coordinate_system: "WGS84"

- ``<<<<<<< HEAD``: Marks the beginning of the change from your current
  branch (``feature/gps-navigation``).
- ``=======``: Separates the two conflicting changes.
- ``>>>>>>> main``: Marks the end of the change from the branch you are
  merging in (``main``).

4. Open ``robot_config.yaml`` in your editor to see the conflict
   markers.
5. Edit the file to contain only the final, correct code and remove all
   conflict markers.
6. **Stage the file:** ``git add robot_config.yaml``
7. **Complete the merge with a descriptive commit message:**

   .. code-block:: bash

      git commit -m "Merge main into feature/gps-navigation

      Resolved navigation update_rate conflict:
      - The GPS feature required 5Hz, while a hotfix needed 20Hz.
      - Set the rate to 15Hz as a compromise between GPS stability
        and overall system responsiveness."

8. **Verify the merge history:** ``git log --oneline --graph``


Completing the Feature
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. card::
   :class-header: sd-bg-dark-orange sd-text-white

   Completing the Feature
   ^^^

   **2:00 PM** -- You add final touches to the GPS feature.

   - Add waypoint information to define how the robot handles mission
     destinations based on GPS coordinates.
   - Update ``README.md`` file.

1. Add GPS waypoint configuration in ``robot_config.yaml``.
2. Update ``README.md``.
3. Review all changes: ``git status``
4. Stage: ``git add .``
5. Commit:

   .. code-block:: bash

      git commit -m "Complete GPS navigation feature

      - Add waypoint navigation configuration
      - Set home coordinates for auto-return functionality
      - Update README with GPS feature documentation
      - Support up to 50 waypoints with 1-meter precision"

6. The feature is complete, merge back to ``main``:

   .. code-block:: bash

      git checkout main
      git merge feature/gps-navigation

7. Clean up feature branch: ``git branch -d feature/gps-navigation``


End of Day Review
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. card::
   :class-header: sd-bg-dark-orange sd-text-white

   End of Day Review
   ^^^

   **5:00 PM** -- You review your day's work.

1. View complete project history:
   ``git log --oneline --graph --all``
2. Check final file status: ``git status``
3. View the complete configuration file: ``cat robot_config.yaml``
4. Create a summary of what was accomplished:
   ``git log --oneline --since="1 day ago"``
5. View detailed changes for the day:
   ``git diff a1b2c3d..HEAD --stat``

.. note::

   Many Git commands are available directly within Visual Studio Code,
   typically located in the **Source Control** view or through the
   **Command Palette**.


GitHub
====================================================

GitHub is a cloud-based platform that hosts Git repositories online. It
adds features like:

- Remote storage for your projects.
- Collaboration tools.
- Issue tracking.
- Project management features.
- Portfolio showcase for your work.


Setup
----------------------------------------------------

1. **Create a GitHub account.**

   - Go to `github.com <https://github.com/>`_.
   - Sign up with your university email.
   - Verify your email address.

2. **Set up authentication.**

   .. code-block:: bash

      # Generate SSH key
      ssh-keygen -t ed25519 -C "your.email@university.edu"
      # Add to GitHub: Settings -> SSH and GPG keys -> New SSH key
      cat ~/.ssh/id_ed25519.pub

   .. note::

      - The ``-t`` flag specifies the type of cryptographic algorithm.
        ``ed25519`` is a modern, fast, and highly secure elliptic-curve
        algorithm recommended for new SSH keys.
      - The ``-C`` flag adds a label (comment) to your public key file
        to help identify the key later.


Public vs. Private Repositories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. grid:: 2

   .. grid-item-card:: Public Repository

      - Anyone can view
      - Anyone can clone/download
      - Shows up in search engines
      - Others can star/follow
      - Completely open source

   .. grid-item-card:: Private Repository

      - Only you can view
      - Only invited collaborators can access
      - Hidden from search engines
      - Cannot be cloned by public
      - Perfect for private work


Connect Local Repo to Remote
----------------------------------------------------

**Scenario 1** -- You already have a local repository.

1. Create an empty repository on GitHub: ``robot-config``

   - **IMPORTANT**: When creating on GitHub, **do not check**:

     - "Add a README file"
     - "Add .gitignore"
     - "Choose a license"

2. Connect local repository to GitHub:

   - Add GitHub as remote origin:

     .. code-block:: bash

        git remote add origin git@github.com:yourusername/robot-config.git

   - Verify the remote was added: ``git remote -v``

3. Push your local ``main`` branch to GitHub:
   ``git push -u origin main``

   - This command pushes your local ``main`` branch to the remote
     repository named ``origin``, and establishes a tracking
     relationship so that in the future you can simply use
     ``git push``.

**Scenario 2** -- Start with GitHub repository first.

1. Create a repository on GitHub: ``new-project``

   - When creating on GitHub, check the following since you are
     starting fresh:

     - "Add a README file"
     - "Add .gitignore" (optional)
     - "Choose a license" (optional)

2. Clone to your local machine:

   .. code-block:: bash

      git clone https://github.com/yourusername/new-project.git

      # Move into the directory
      cd new-project

      # Start working
      echo "# My New Project" >> README.md
      git add README.md
      git commit -m "Update README"
      git push origin main


Collaboration Workflows
----------------------------------------------------

When working with teams, you need to choose between **branching** and
**forking** workflows. The choice depends on your team structure and
project permissions.

.. grid:: 2

   .. grid-item-card:: Branch Workflow (Private Repo)

      **Use when:** You have write access to the repository (team
      member, collaborator).

      - Direct access to main repository.
      - Simpler workflow for team members.
      - Better for small to medium teams.
      - Easier to manage releases.

   .. grid-item-card:: Fork Workflow (Public Repo)

      **Use when:** You do not have write access (open source
      contributor, external collaborator).

      - Works without write permissions.
      - Safe for open source projects.
      - Each contributor has complete copy.
      - Maintainers control what gets merged.


Branch Workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/vc/branch-workflow.png
   :align: center
   :width: 40%

   Branch workflow diagram.

1. Clone the main repository.

   .. code-block:: bash

      git clone git@github.com:team/robot-project.git
      cd robot-project

2. Create feature branch.

   .. code-block:: bash

      git checkout -b feature/sensor-integration

3. Work on your changes.

4. Commit and push to shared repository.

   .. code-block:: bash

      git add .
      git commit -m "Add ultrasonic sensor integration"
      git push origin feature/sensor-integration

5. Create Pull Request on GitHub: After review and approval, merge to
   main.

**Repository Structure:**

::

   main repository: team/robot-project
       main branch
       feature/sensor-integration (your branch)
       feature/camera-module (teammate's branch)
       hotfix/battery-issue (another branch)


Fork Workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/vc/fork-workflow.png
   :align: center
   :width: 40%

   Fork workflow diagram.

1. **Fork** the repository on GitHub (creates your copy).

   *Original*: ``zeidk/enpm702-summer-2025.git`` -->
   *Your fork*: ``yourusername/enpm702-summer-2025.git``

2. Clone **your** fork.

   .. code-block:: bash

      git clone git@github.com:yourusername/enpm702-summer-2025.git
      cd enpm702-summer-2025

3. Add original repository as upstream.

   .. code-block:: bash

      git remote add upstream https://github.com/zeidk/enpm702-summer-2025.git
      git remote -v
      # origin    git@github.com:yourusername/enpm702-summer-2025.git (your fork)
      # upstream  https://github.com/zeidk/enpm702-summer-2025.git (original)

4. Create feature branch:
   ``git checkout -b feature/new-algorithm``

5. Work on your changes.

6. Commit and push to **your** fork.

   .. code-block:: bash

      git add .
      git commit -m "Implement new pathfinding algorithm"
      git push origin feature/new-algorithm

7. Create Pull Request from your fork to original repository.


Keeping Your Fork Updated
""""""""""""""""""""""""""""""""""""""""""""""""""""

1. Fetch latest changes from original repository:
   ``git fetch upstream``
2. Switch to main branch: ``git checkout main``
3. Merge the latest changes from the upstream repository into your
   local repository: ``git merge upstream/main``
4. Push updates to your fork: ``git push origin main``
5. Now create new feature branches from updated main:
   e.g., ``git checkout -b feature/next-feature``

**Repository Structure:**

::

   Original: zeidk/enpm702-summer-2025 (upstream)
       main branch

   Your Fork: yourusername/enpm702-summer-2025 (origin)
       main branch (synced with upstream)
       feature/new-algorithm (your work)


When to Use Each Approach
""""""""""""""""""""""""""""""""""""""""""""""""""""

.. list-table::
   :widths: 50 50
   :header-rows: 1
   :class: compact-table

   * - **Scenario**
     - **Recommended Approach**
   * - Team member with repository access
     - Branch Workflow
   * - Contributing to open source project
     - Fork Workflow
   * - External contractor/collaborator
     - Fork Workflow
   * - Company internal project
     - Branch Workflow
   * - Public project accepting contributions
     - Fork Workflow
   * - Small team (< 10 people)
     - Branch Workflow
   * - Large community project
     - Fork Workflow


Best Practices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Best Practices
   :class: tip

   - **Clear branch naming**: ``feature/name``, ``bugfix/name``,
     ``hotfix/name``
   - **Regular commits**: Small, focused commits with clear messages.
   - **Pull requests**: Always use pull requests for code review.
   - **Stay updated**: Regularly sync with main branch/upstream.
   - **Test before merging**: Ensure changes do not break existing
     functionality.

**Action items:**

- Practice both workflows with your team.
- Set up proper branch protection rules.
- Establish team conventions for branch naming.
- Configure automated testing for pull requests.


Pull Requests
----------------------------------------------------

A Pull Request (PR) is a method of submitting contributions to a
project. It allows you to tell others about changes you have pushed to
a branch in a repository.

**Why Use Pull Requests?**

- **Code Review**: Team members can review changes before merging.
- **Discussion**: Collaborate and discuss proposed changes.
- **Testing**: Automated tests run on proposed changes.
- **Quality Control**: Maintain code standards and catch bugs.
- **Documentation**: Track what changes were made and why.

**Basic Workflow:**

.. code-block:: bash

   git checkout -b feature/add-lidar-support
   # Make changes, add, commit
   git push origin feature/add-lidar-support
   # Create PR on GitHub -> Review -> Merge -> Delete branch


Creating a Good Pull Request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Title: Add LiDAR sensor integration for obstacle detection

   ## What this PR does
   - Adds support for Velodyne VLP-16 LiDAR sensor
   - Implements point cloud processing for obstacle detection
   - Updates robot configuration with LiDAR parameters

   ## Testing
   - [x] Unit tests pass
   - [x] Integration tests with physical sensor

   ## Related Issues
   Fixes #123: Robot needs better obstacle detection

.. admonition:: Best Practices for PRs
   :class: tip

   - Use clear, descriptive titles and explain WHAT and WHY.
   - Include testing information and link to related issues.
   - Keep PRs focused and reasonably sized (< 400 lines).
   - Use "Draft PR" for work-in-progress to get early feedback.


PR Merge Strategies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. grid:: 3

   .. grid-item-card:: Merge Commit

      - Preserves branch history
      - Shows when merged
      - Can create "bubbles"

   .. grid-item-card:: Squash and Merge

      - Combines all commits
      - Cleaner history
      - **Recommended**

   .. grid-item-card:: Rebase and Merge

      - Linear history
      - Preserves commits
      - Advanced technique

.. warning::

   **Common Mistakes to Avoid:**

   - Mixing unrelated changes in one PR.
   - Vague descriptions or poor commit messages.
   - Not testing before submitting.
   - Ignoring review feedback or force-pushing after reviews.
   - Committing sensitive data (passwords, keys).

Set up branch protection rules requiring reviews before merging.


Pull Request Reviews
----------------------------------------------------

Pull request (PR) reviews are crucial for maintaining code quality and
knowledge sharing.

**Review Process:**

1. **Pre-Review Checklist** (2 minutes)

   - Check CI/CD status and understand context.
   - Verify no merge conflicts, correct target branch.

2. **High-Level Review** (5-10 minutes)

   - Architecture fit, security implications, overall approach.

3. **Detailed Review** (15-30 minutes)

   - Logic, code quality, performance, testing.
