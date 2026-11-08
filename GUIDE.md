# Git & GitHub hands-on guide

Work through the lessons in order. Each one builds on the last.
Type the commands yourself — don't copy-paste everything; typing is how it sticks.

> **Mental model**
> - **Commit** = a saved snapshot of your files.
> - **Branch** = a movable label pointing to a line of commits. `main` is the "official" one.
> - **Remote** (`origin`) = the copy of the repo on GitHub.
> - **Pull Request (PR)** = "please merge my branch into `main`" + a place for review and discussion.
> - **Tag** = a permanent label on one commit (e.g. `v0.2.0`).
> - **Release** = a GitHub page built on a tag, with notes and downloadable files.

Useful at any time:

```bash
git status                     # what changed? which branch am I on?
git log --oneline --graph --all  # picture of all branches and commits
git branch -a                  # list local + remote branches
```

---

## Lesson 0 — Put the project on GitHub

The repo already has one commit on `main`. Create the GitHub copy and push:

```bash
gh repo create github_use --public --source=. --push
```

Open it in the browser: `gh repo view --web`.
Click **Actions** — you'll see the CI workflow (`.github/workflows/ci.yml`) running the tests.

---

## Lesson 1 — Issues

Issues are a to-do list for the *project*. Create one:

```bash
gh issue create --title "Add a 'remove' command" --body "Users should be able to delete a todo."
gh issue list
```

Remember its number (probably `#1`).

---

## Lesson 2 — Branch → commit → push

Never work directly on `main`. Make a branch for each change:

```bash
git switch -c feature/remove-command   # create + move to new branch
```

Edit `todo.py`: add this function under `complete`:

```python
def remove(todos, index):
    todos.pop(index)
    return todos
```

and inside `main()` add a new branch before `elif argv[1] == "version":`:

```python
    elif argv[1] == "remove":
        save(remove(todos, int(argv[2]) - 1))
        print("Removed.")
```

Add a test in `test_todo.py`:

```python
    def test_remove(self):
        from todo import remove
        self.assertEqual(remove(add([], "a"), 0), [])
```

Now save it as a commit:

```bash
python -m unittest           # make sure it passes
git status                   # see the modified files (red)
git diff                     # see exactly what changed
git add todo.py test_todo.py # stage (green)
git commit -m "Add remove command"
git push -u origin feature/remove-command   # -u: remember where to push this branch
```

---

## Lesson 3 — Pull Request

```bash
gh pr create --fill
```

(or on the website: a yellow "Compare & pull request" banner appears.)
Edit the description so it says `Closes #1` — that links the PR to the issue.

On the PR page, look at:
- **Files changed** — the diff. Click a line's `+` to leave a review comment.
- **Checks** — CI runs the tests on your branch. Wait for the green ✓.

Push another commit to the same branch and watch the PR update automatically:

```bash
# e.g. update the usage line in todo.py to mention "remove <number>"
git commit -am "Mention remove in usage text"
git push
```

Merge it:

```bash
gh pr merge --squash --delete-branch
```

Issue #1 closes itself. Bring your local `main` up to date:

```bash
git switch main
git pull
git log --oneline
```

> **Merge styles:** *merge commit* keeps every commit + a merge commit; *squash* turns the PR into one commit;
> *rebase* replays the commits on top of `main` without a merge commit.

---

## Lesson 4 — Merge conflicts (on purpose)

A conflict happens when two branches change the **same lines** differently.

```bash
git switch -c change-empty-a
# In todo.py change "Nothing to do!" to "All clear! 🎉"
git commit -am "Friendlier empty message"
git switch main

git switch -c change-empty-b
# In todo.py change "Nothing to do!" to "Your list is empty."
git commit -am "Clearer empty message"
git switch main
```

Merge the first one — clean:

```bash
git merge change-empty-a
```

Now the second — 💥 conflict:

```bash
git merge change-empty-b
```

Open `todo.py`. You'll see:

```
<<<<<<< HEAD
        return "All clear! 🎉"
=======
        return "Your list is empty."
>>>>>>> change-empty-b
```

Choose the final text, delete the `<<<<<<<`, `=======`, `>>>>>>>` lines, update the test in
`test_todo.py` to match, then:

```bash
python -m unittest
git add todo.py test_todo.py
git commit                # finishes the merge
git branch -d change-empty-a change-empty-b
git push
```

(Here you merged locally. The same conflict can happen in a PR — GitHub then shows
"This branch has conflicts"; you fix it by merging `main` into your branch and pushing.)

---

## Lesson 5 — Tags & Releases

Releases use **Semantic Versioning** `MAJOR.MINOR.PATCH`:
- PATCH (0.1.**1**) – bug fix
- MINOR (0.**2**.0) – new feature, nothing broken
- MAJOR (**1**.0.0) – breaking change

You added a feature, so the next version is **0.2.0**. Do it on a branch + PR like a pro:

```bash
git switch -c release/v0.2.0
```

1. In `todo.py` set `__version__ = "0.2.0"`.
2. In `CHANGELOG.md`, move items under a new heading:

   ```markdown
   ## [Unreleased]

   ## [0.2.0] - YYYY-MM-DD
   ### Added
   - `remove` command.
   ### Changed
   - New empty-list message.
   ```

```bash
git commit -am "Release v0.2.0"
git push -u origin release/v0.2.0
gh pr create --fill
gh pr merge --merge --delete-branch
git switch main && git pull
```

Now tag the release commit and publish a GitHub Release:

```bash
git tag -a v0.2.0 -m "Version 0.2.0"
git push origin v0.2.0
gh release create v0.2.0 --title "v0.2.0" --generate-notes
```

Look at the **Releases** section on the repo page. GitHub auto-attaches source-code zips,
and `--generate-notes` lists the merged PRs. 🎉

Try it: `git checkout v0.0.0` won't exist, but `git checkout v0.2.0` will — tags let you jump
back to any released version (`git switch main` to return).

---

## Lesson 6 — Bonus challenges

1. **Fork-style workflow:** ask a friend to fork your repo, make a PR to it, and you review it.
2. **Protect `main`:** Settings → Branches → add a rule "Require a pull request" and
   "Require status checks (CI) to pass". Now try `git push` directly to main — it's rejected.
3. **Revert a bad change:** `git revert <commit-hash>` creates a new commit that undoes an old one (safe for shared history).
4. **Rebase:** on a feature branch, run `git fetch && git rebase origin/main` to replay your work on the newest `main`.
5. **Stash:** half-done work but need to switch branch? `git stash`, switch, come back, `git stash pop`.
6. **Hotfix release:** fix a bug (e.g. `done 99` crashes) on `fix/...`, PR it, release **v0.2.1**.

---

## Cheat sheet

| Goal | Command |
|---|---|
| New branch | `git switch -c name` |
| Change branch | `git switch name` |
| Stage + commit | `git add file` → `git commit -m "msg"` |
| Push new branch | `git push -u origin name` |
| Update main | `git switch main && git pull` |
| Open PR | `gh pr create --fill` |
| See PRs | `gh pr list` / `gh pr view --web` |
| Merge PR | `gh pr merge --squash --delete-branch` |
| Tag | `git tag -a v1.0.0 -m "msg"` → `git push origin v1.0.0` |
| Release | `gh release create v1.0.0 --generate-notes` |
| Undo unstaged edits to a file | `git restore file` |
| Unstage a file | `git restore --staged file` |
