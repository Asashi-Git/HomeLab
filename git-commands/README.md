
# Git Command Reference Guide

A **practical, team-oriented reference** for daily Git usage.  
Think of it as your **survival guide** when working collaboratively.

---

## 1. Inspection & Awareness

*Answer the question: **“Where am I and what is happening?”***

| Command                 | What it does                                  | When to use it                       |
| :---------------------- | :-------------------------------------------- | :----------------------------------- |
| **`git status`**        | Shows modified, staged files + current branch | **Use constantly** before any action |
| **`git log --oneline`** | Displays compact commit history               | To quickly review recent activity    |
| **`git diff`**          | Shows exact code changes (unstaged)           | Before `git add`, to avoid mistakes  |
| **`git diff --staged`** | Shows staged changes                          | Before committing                    |

---

## 2. Synchronization (Talking to GitHub)

*Keep your local repo aligned with the team.*

| Command                           | What it does                 | When to use it                 |
| :-------------------------------- | :--------------------------- | :----------------------------- |
| **`git pull origin main`**        | Fetch + merge remote changes | Start of day / before new work |
| **`git fetch`**                   | Fetch without merging        | Safe check before pulling      |
| **`git push -u origin <branch>`** | Push branch to remote        | First push of a new branch     |
| **`git push`**                    | Push updates                 | After new commits              |

---

## 3. Branching (The Multiverse)

*Work safely in parallel without breaking `main`.*

| Command | What it does | When to use it |
| :--- | :--- | :--- |
| **`git branch`** | List local branches | Quick overview |
| **`git branch -a`** | List all branches (local + remote) | Debugging / discovery |
| **`git checkout -b <name>`** | Create + switch branch | New feature / fix |
| **`git checkout <name>`** | Switch branch | Change context |
| **`git switch <name>`** | Modern alternative to checkout | Preferred (cleaner) |
| **`git branch -d <name>`** | Delete branch | After merge cleanup |

---

## 4. Saving Work (The 2-Step Process)

*This is your **core workflow**.*

| Command | What it does | When to use it |
| :--- | :--- | :--- |
| **`git add .`** | Stage all changes | When everything is ready |
| **`git add <file>`** | Stage specific file | Selective commits |
| **`git commit -m "msg"`** | Save snapshot | After staging |

Good commit messages:
- `feat: add login endpoint`
- `fix: correct null pointer issue`
- `docs: update README`

---

## 5. Emergency & Undo (The Panic Button)

*Fix mistakes without making things worse.*

| Command                  | What it does                    | When to use it                  |
| :----------------------- | :------------------------------ | :------------------------------ |
| **`git checkout .`**     | ⚠️ Discards all local changes   | Hard reset of working directory |
| **`git reset HEAD~1`**   | Undo last commit (keep changes) | Fix last commit                 |
| **`git restore <file>`** | Restore file (modern safe way)  | Safer than checkout             |
| **`git stash`**          | Save work temporarily           | Switch tasks quickly            |
| **`git stash pop`**      | Restore stashed work            | Resume work                     |

---

## 6. Useful Shortcuts & Aliases

```bash
git config --global alias.tree "log --graph --oneline --all --decorate"
````

Use it with:

```bash
git tree
```

Visualizes your commit history as a graph (very useful for debugging branches)

---

## 7. Repository Configuration

### Set identity

```bash
git config --global user.name "YourName"
git config --global user.email "your@email.com"
```

### Check remotes

```bash
git remote -v
```

### Change remote URL

```bash
git remote set-url origin git@github.com:Asashi-Git/HomeLab.git
```

---

## 8. Cleaning & Security

### Remove sensitive files from tracking

```bash
git rm -r --cached secrets/
```

Use when you accidentally committed sensitive data

---

## 9. Nuclear Options (Use with Extreme Caution)

```bash
git push --force origin main
```

⚠️ **DANGER**

- Rewrites remote history
- Can break your team’s work
- Only use if you **fully understand the impact**

---

## Best Practices

- Always `git pull` before starting work
- Never commit directly to `main`
- Use branches (`feature/...`, `fix/...`)
- Commit often, but with **clear messages**
- Review changes with `git diff` before committing
- Avoid `--force` unless absolutely necessary

---

## Summary

> Git is not just a tool — it’s your **safety net, collaboration layer, and time machine**.  
> Use it carefully, and it will save you more times than you expect.

---
