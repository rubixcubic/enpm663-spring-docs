====================================================
Version Control -- Quiz
====================================================


.. admonition:: Question 1
   :class: hint

   What does ``git init`` do?

   a) Clones a remote repository to your local machine
   b) Creates a new Git repository in the current directory
   c) Initializes a connection to GitHub
   d) Installs Git on your system

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) Creates a new Git repository in the current directory**

      ``git init`` creates a ``.git`` directory in the current folder,
      which initializes an empty repository ready for tracking changes.


.. admonition:: Question 2
   :class: hint

   Which type of version control system gives every developer a
   complete copy of the repository?

   a) Local Version Control
   b) Centralized Version Control
   c) Distributed Version Control
   d) Cloud Version Control

   .. dropdown:: Answer
      :class-container: sd-border-success

      **c) Distributed Version Control**

      In a distributed version control system (like Git), every client
      has a complete copy of the repository including full history.
      There is no single point of failure.


.. admonition:: Question 3
   :class: hint

   What is the correct sequence to save changes in Git?

   a) ``git commit`` then ``git add``
   b) ``git add`` then ``git commit``
   c) ``git push`` then ``git add``
   d) ``git commit`` then ``git push`` then ``git add``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) git add then git commit**

      You first stage changes with ``git add`` (preparing them in the
      staging area), then create a permanent snapshot with
      ``git commit``.


.. admonition:: Question 4
   :class: hint

   What does ``git checkout -b feature/gps-navigation`` do?

   a) Deletes the branch ``feature/gps-navigation``
   b) Switches to an existing branch named ``feature/gps-navigation``
   c) Creates a new branch named ``feature/gps-navigation`` and
      switches to it
   d) Merges ``feature/gps-navigation`` into the current branch

   .. dropdown:: Answer
      :class-container: sd-border-success

      **c) Creates a new branch named feature/gps-navigation and
      switches to it**

      The ``-b`` flag tells Git to create a new branch before switching
      to it. This is equivalent to running ``git branch`` followed by
      ``git checkout``.


.. admonition:: Question 5
   :class: hint

   When does a merge conflict occur in Git?

   a) When you try to push to a remote that does not exist
   b) When two branches modify the same line in the same file
   c) When you forget to run ``git add`` before committing
   d) When you delete a branch that has not been merged

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) When two branches modify the same line in the same file**

      Git cannot automatically determine which change to keep when both
      branches have modified the same line, so it inserts conflict
      markers and asks you to resolve the conflict manually.


.. admonition:: Question 6
   :class: hint

   What is the purpose of ``git push -u origin main``?

   a) Deletes the ``main`` branch from the remote
   b) Pulls changes from the remote ``main`` branch
   c) Pushes the local ``main`` branch to the remote and sets up
      tracking
   d) Creates a new remote named ``origin``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **c) Pushes the local main branch to the remote and sets up
      tracking**

      The ``-u`` flag (short for ``--set-upstream``) establishes a
      tracking relationship so future ``git push`` and ``git pull``
      commands work without specifying the remote and branch.


.. admonition:: Question 7
   :class: hint

   In a fork workflow, what does ``upstream`` typically refer to?

   a) Your local repository
   b) Your fork on GitHub
   c) The original repository you forked from
   d) A branch in your repository

   .. dropdown:: Answer
      :class-container: sd-border-success

      **c) The original repository you forked from**

      In a fork workflow, ``origin`` refers to your fork and
      ``upstream`` refers to the original repository. You sync with
      ``upstream`` to stay up-to-date with the latest changes.


.. admonition:: Question 8
   :class: hint

   Which merge strategy is recommended for keeping a clean commit
   history in pull requests?

   a) Merge Commit
   b) Squash and Merge
   c) Rebase and Merge
   d) Fast-forward Merge

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) Squash and Merge**

      Squash and Merge combines all commits from the feature branch
      into a single commit, resulting in a cleaner history on the main
      branch.


.. admonition:: Question 9
   :class: hint

   What does ``git diff`` show?

   a) The list of all branches in the repository
   b) Changes between your working directory and the staging area
   c) The commit history of the repository
   d) The list of remote repositories

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) Changes between your working directory and the staging area**

      ``git diff`` shows the differences between the current state of
      your files and what has been staged. It helps you review changes
      before staging them.


.. admonition:: Question 10
   :class: hint

   What is the primary purpose of a ``.gitignore`` file?

   a) To list all files that should be committed
   b) To specify files and patterns that Git should not track
   c) To configure Git user settings
   d) To store the commit history

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) To specify files and patterns that Git should not track**

      ``.gitignore`` tells Git which files (build artifacts, IDE
      settings, sensitive data, etc.) should be excluded from version
      control.


.. admonition:: Question 11
   :class: hint

   True or False: In a centralized version control system, you can
   view the full commit history without a network connection.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      In a centralized system, most operations (including viewing
      history) require a connection to the central server. Only
      distributed systems like Git allow full offline access to history.


.. admonition:: Question 12
   :class: hint

   True or False: A pull request can only be created in the branch
   workflow, not in the fork workflow.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      Pull requests can be created in both workflows. In the branch
      workflow, the PR goes from a feature branch to the main branch
      within the same repository. In the fork workflow, the PR goes
      from your fork to the original repository.


.. admonition:: Question 13
   :class: hint

   True or False: ``git merge`` always results in a merge conflict.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      A merge conflict only occurs when both branches have modified the
      same line(s) in the same file(s). If changes are in different
      files or different parts of the same file, Git can merge
      automatically without conflicts.


.. admonition:: Question 14
   :class: hint

   True or False: After resolving a merge conflict, you must run
   ``git add`` on the resolved file before completing the merge with
   ``git commit``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True.**

      After editing the file to resolve conflicts (removing conflict
      markers and choosing the correct content), you must stage the
      resolved file with ``git add`` and then run ``git commit`` to
      complete the merge.


.. admonition:: Question 15
   :class: hint

   True or False: The ``git branch -d`` command will delete a branch
   even if it has not been merged into any other branch.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      ``git branch -d`` (lowercase ``d``) is a safe delete that refuses
      to delete a branch if it has not been merged. To force-delete an
      unmerged branch, you would use ``git branch -D`` (uppercase
      ``D``).
