# Git & GitHub hands-on guide (website version)

Work through the lessons in order. Each one builds on the last.

There are two places you work:

- 🖥️ **Your computer (terminal)**: you write code here and use `git` to save and upload it.
- 🌐 **github.com (browser)**: repos, issues, pull requests, reviews, merges and releases.

> **Mental model**
> - **Commit** = a saved snapshot of your files.
> - **Branch** = a movable label pointing to a line of commits. `main` is the "official" one.
> - **Remote** (`origin`) = the copy of your repo on GitHub.
> - **Push** = upload your commits to GitHub. **Pull** = download new commits from GitHub.
> - **Issue** = a to-do item or bug report for the project.
> - **Pull Request (PR)** = "please merge my branch into `main`", plus a place to review and discuss it.
> - **Tag** = a permanent label on one commit (e.g. `v0.2.0`).
> - **Release** = a GitHub page built on a tag, with notes and downloadable files.

Terminal commands you can use at any time:

```bash
git status                       # what changed? which branch am I on?
git log --oneline --graph --all  # picture of all branches and commits
git branch -a                    # list local + remote branches
```

---

## Lesson 0: Create the repo on GitHub and upload the project

### 🌐 On github.com

1. Log in at **https://github.com**.
2. In the top-right corner, click the **+** button → **New repository**.
3. Fill in the form:
   - **Repository name:** `github_use`
   - **Description** (optional): `Practice project for learning Git and GitHub`
   - Choose **Public** or **Private**.
   - ⚠️ Do **not** tick "Add a README file", ".gitignore" or "license". Your project already has
     these files, and if GitHub creates its own, the two copies of the history won't match.
4. Click the green **Create repository** button.
5. GitHub now shows a page titled "Quick setup". Make sure **SSH** is selected (not HTTPS), and
   copy the address. It looks like `git@github.com:cigdemahmet27/github_use.git`.

### 🖥️ In the terminal

Connect your local project to that GitHub repo and upload it:

```bash
git remote add origin git@github.com:cigdemahmet27/github_use.git   # "origin" = nickname for the GitHub copy
git push -u origin main                                             # upload main; -u remembers where to push
```

### 🌐 Back on github.com

Refresh the page. Your files are there, and `README.md` is shown under the file list.

- Click **Commits** (the clock icon with "2 Commits" above the file list) to see your history.
- Click the **Actions** tab. The **CI** workflow is running your tests. A green ✓ means they passed.
  This happens because of the file `.github/workflows/ci.yml`.

---

## Lesson 1: Create an issue

Issues are a to-do list for the project.

### 🌐 On github.com

1. Open your repo and click the **Issues** tab.
2. Click the green **New issue** button.
3. **Title:** `Add a 'remove' command`
   **Description:** `Users should be able to delete a todo.`
4. On the right side you can try:
   - **Assignees** → click "assign yourself".
   - **Labels** → choose `enhancement`.
5. Click **Submit new issue** (on some layouts the button is called **Create**).

Note the number GitHub gives it, shown as `#1` after the title. You will use it in Lesson 3.

---

## Lesson 2: Branch, commit, push

Don't work directly on `main`. Make a separate branch for each change.

### 🖥️ In the terminal

```bash
git switch -c feature/remove-command   # create a new branch and move to it
```

Open `todo.py`, and add this function under `complete`:

```python
def remove(todos, index):
    todos.pop(index)
    return todos
```

In the same file, inside `main()`, add this just before `elif argv[1] == "version":`:

```python
    elif argv[1] == "remove":
        save(remove(todos, int(argv[2]) - 1))
        print("Removed.")
```

Add a test at the end of the `TestTodo` class in `test_todo.py`:

```python
    def test_remove(self):
        from todo import remove
        self.assertEqual(remove(add([], "a"), 0), [])
```

Save the change as a commit and upload it:

```bash
python -m unittest                         # make sure the tests pass
git status                                 # modified files are shown in red
git diff                                   # shows exactly what changed
git add todo.py test_todo.py               # stage them (now shown in green)
git commit -m "Add remove command"
git push -u origin feature/remove-command  # upload the branch to GitHub
```

### 🌐 On github.com

- Click the **branch dropdown** at the top-left of the file list (it says `main`). Your new
  branch `feature/remove-command` is in the list. Choose it to see the files on that branch.
- Click **Branches** next to the dropdown to see all branches at once.

---

## Lesson 3: Pull request (PR)

### 🌐 Open the PR

1. Go to your repo's main page. A yellow banner appears:
   *"feature/remove-command had recent pushes"*. Click **Compare & pull request**.
   (If the banner is gone: open the **Pull requests** tab → **New pull request** → set
   **base: `main`** and **compare: `feature/remove-command`** → **Create pull request**.)
2. Check the arrow at the top: `base: main ← compare: feature/remove-command`.
   It means "merge my branch **into** main".
3. The title is filled in from your commit message. The description box is pre-filled from
   `.github/pull_request_template.md`. Fill it in, and on the last line write `Closes #1`.
   That links the PR to your issue, and the issue closes automatically when the PR is merged.
4. Click **Create pull request**.

### 🌐 Look around the PR

The PR page has tabs near the top:

- **Conversation**: the description, comments and a timeline of what happened.
  At the bottom you can see the **checks** box. Wait until "CI / test" shows a green ✓.
- **Commits**: the commits in this branch.
- **Files changed**: the diff. Green lines were added, red lines were removed.

### 🌐 Review your own code

1. Open **Files changed**.
2. Hover over a line and click the blue **+** that appears to its left.
3. Write a comment such as `Should we check that the number is valid?`, then click **Start a review**.
4. Click **Review changes** (top-right, green) → write a summary → choose **Comment** →
   **Submit review**.
   (GitHub won't let you choose "Approve" or "Request changes" on your own PR. Those are
   for other people reviewing your work.)

### 🖥️ Update the PR with another commit

A PR follows its branch. When you push more commits to the branch, the PR updates by itself.
In `todo.py`, change the usage line so it mentions `remove <number>`:

```bash
git commit -am "Mention remove in usage text"
git push
```

Refresh the PR page. The new commit appears, and the tests run again.

### 🌐 Merge the PR

1. Go back to the **Conversation** tab and scroll to the bottom.
2. Click the small **▾ arrow** next to the green merge button. You'll see three choices:
   - **Create a merge commit**: keeps every commit and adds a "merge" commit.
   - **Squash and merge**: combines all the PR's commits into one commit on `main`.
   - **Rebase and merge**: copies the commits onto `main` without a merge commit.
3. Choose **Squash and merge** → **Confirm squash and merge**.
4. Click **Delete branch**. The branch on GitHub is no longer needed.
5. Open the **Issues** tab. Issue #1 has closed by itself because of `Closes #1`.

### 🖥️ Bring your computer up to date

The merge happened on GitHub, so your computer doesn't have it yet:

```bash
git switch main
git pull                                   # download the merged change
git branch -d feature/remove-command       # delete your local copy of the branch
git log --oneline
```

(If `git branch -d` refuses with "not fully merged", that's normal after a squash merge.
Use `git branch -D feature/remove-command` instead.)

---

## Lesson 4: Change a file directly on GitHub

For small changes you don't need a terminal at all.

### 🌐 On github.com

1. On your repo page, click `README.md`.
2. Click the ✏️ **pencil icon** (top-right of the file) to edit it.
3. Under **Usage**, add the line `python todo.py remove 1`.
4. Click **Commit changes...** (green, top-right). A small window opens:
   - Write a commit message: `Document remove command`.
   - Choose **Create a new branch for this commit and start a pull request**, and give the
     branch a name, e.g. `docs/remove`.
5. Click **Propose changes**. You are taken straight to a new PR. Click **Create pull request**,
   then merge it as in Lesson 3.

### 🖥️ In the terminal

```bash
git switch main
git pull     # always pull after something was merged on GitHub
```

---

## Lesson 5: Merge conflicts (on purpose)

A conflict happens when two branches change **the same lines** in different ways.
Git can't guess which version you want, so it asks you.

### 🖥️ Create two branches that disagree

```bash
git switch main
git switch -c change-empty-a
# in todo.py, change "Nothing to do!" to "All clear!"
# in test_todo.py, change "Nothing to do!" to "All clear!"
git commit -am "Friendlier empty message"
git push -u origin change-empty-a

git switch main
git switch -c change-empty-b
# in todo.py, change "Nothing to do!" to "Your list is empty."
# in test_todo.py, change "Nothing to do!" to "Your list is empty."
git commit -am "Clearer empty message"
git push -u origin change-empty-b
```

### 🌐 Open both PRs

Create a PR for `change-empty-a` and one for `change-empty-b` (as in Lesson 3).

1. Merge the `change-empty-a` PR. There is no problem.
2. Open the `change-empty-b` PR. Near the bottom it now says
   **"This branch has conflicts that must be resolved"**.

### 🌐 Fix the conflict on GitHub

1. Click **Resolve conflicts**. An editor opens and shows something like:

   ```
   <<<<<<< change-empty-b
           return "Your list is empty."
   =======
           return "All clear!"
   >>>>>>> main
   ```

   - The part between `<<<<<<<` and `=======` is **your branch's version**.
   - The part between `=======` and `>>>>>>>` is **`main`'s version**.
2. Choose the text you want to keep, and delete the three marker lines
   (`<<<<<<<`, `=======` and `>>>>>>>`). Make sure the line keeps its indentation.
3. Click **Mark as resolved**. If another file also has a conflict (here `test_todo.py`),
   it's listed on the left. Fix it the same way.
4. Click **Commit merge**.
5. The PR can now be merged. Merge it and delete the branch.

> If the conflict is too complicated for the web editor, GitHub only offers the
> command-line option. You can fix it in the terminal instead:
> `git switch change-empty-b`, then `git pull`, then `git merge origin/main`. Fix the files in
> your editor, then `git add .`, `git commit` and `git push`.

### 🖥️ In the terminal

```bash
git switch main
git pull
git branch -D change-empty-a change-empty-b
```

---

## Lesson 6: Releases

Releases use **semantic versioning**, written `MAJOR.MINOR.PATCH`:

- PATCH (0.1.**1**): a bug fix.
- MINOR (0.**2**.0): a new feature that doesn't break anything.
- MAJOR (**1**.0.0): a change that breaks how people used it before.

You added a feature, so the next version is **0.2.0**.

### 🖥️ Prepare the release in a PR

```bash
git switch -c release/v0.2.0
```

1. In `todo.py`, set `__version__ = "0.2.0"`.
2. In `CHANGELOG.md`, add a new section under `## [Unreleased]`:

   ```markdown
   ## [Unreleased]

   ## [0.2.0] - YYYY-MM-DD
   ### Added
   - `remove` command.
   ### Changed
   - New empty-list message.
   ```

```bash
git commit -am "Prepare release v0.2.0"
git push -u origin release/v0.2.0
```

### 🌐 Merge it on github.com

Open a PR for `release/v0.2.0` and merge it (as in Lesson 3).

### 🌐 Create the release

1. On your repo's main page, find **Releases** in the right-hand sidebar and click
   **Create a new release** (or go to **Releases** → **Draft a new release**).
2. Click **Choose a tag**, type `v0.2.0`, and click **+ Create new tag: v0.2.0 on publish**.
   GitHub creates the tag for you when you publish.
3. Check that **Target** is `main`.
4. **Release title:** `v0.2.0`
5. Click **Generate release notes**. GitHub writes a list of the PRs merged since the last
   release. You can also paste in the `0.2.0` section from `CHANGELOG.md`.
6. Leave **Set as the latest release** ticked.
   (**Set as a pre-release** is for test versions such as `v0.3.0-beta`.)
7. Click **Publish release**.

The release page now shows your notes and **Source code (zip)** / **(tar.gz)** downloads, which
GitHub adds automatically. You can also drag extra files into the release form before
publishing, and they appear as downloads.

### 🖥️ Get the tag on your computer

```bash
git switch main
git pull --tags
git tag                 # shows v0.2.0
git checkout v0.2.0     # view the project exactly as it was at this release
git switch main         # go back to main
```

---

## Lesson 7: Bonus challenges (all on github.com)

1. **Protect `main`:** go to **Settings** → **Branches** (newer layouts: **Settings** → **Rules** →
   **Rulesets**) → **Add rule**. Turn on **Require a pull request before merging** and
   **Require status checks to pass**, and choose the `test` check. Then try
   `git push origin main` from the terminal. GitHub rejects it.
2. **Revert a merged PR:** open an already-merged PR and click the **Revert** button near the
   bottom. GitHub makes a new PR that undoes it.
3. **Fork:** ask a friend to open your repo and click **Fork** (top-right). This makes their own
   copy. They change something there and open a PR back to your repo, and you review it.
4. **Projects board:** open the **Projects** tab → **New project** → **Board**. Add your issues and
   drag them between "Todo", "In Progress" and "Done".
5. **Milestone:** **Issues** → **Milestones** → **New milestone** `v0.3.0`. Add issues to it and
   watch the progress bar.
6. **Bug fix release:** create an issue "`done 99` crashes", fix it on a `fix/...` branch, merge
   the PR, and publish release **v0.2.1**.

---

## Cheat sheet

| Goal | Where | How |
|---|---|---|
| New branch | 🖥️ | `git switch -c name` |
| Save work | 🖥️ | `git add file` → `git commit -m "msg"` |
| Upload a new branch | 🖥️ | `git push -u origin name` |
| Get the latest changes | 🖥️ | `git switch main` → `git pull` |
| Create an issue | 🌐 | **Issues** → **New issue** |
| Open a PR | 🌐 | **Compare & pull request** banner, or **Pull requests** → **New pull request** |
| Review a PR | 🌐 | **Files changed** → **+** on a line → **Review changes** |
| Merge a PR | 🌐 | Bottom of **Conversation** → merge button → **Delete branch** |
| Fix a conflict | 🌐 | **Resolve conflicts** → edit → **Mark as resolved** → **Commit merge** |
| Edit a file in the browser | 🌐 | Open the file → ✏️ → **Commit changes...** |
| Release | 🌐 | **Releases** → **Draft a new release** → choose tag → **Publish release** |
| Undo edits to a file | 🖥️ | `git restore file` |
| Unstage a file | 🖥️ | `git restore --staged file` |
